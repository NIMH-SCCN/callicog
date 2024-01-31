""" Listener, runs on miniPC, waits for and accepts communication from
control computer.
"""
# pylint: disable=W,C

from threading import Thread, Event

import argparse
import inspect
import json
import logging
import os
import pickle
import signal
import time
import queue

import numpy as np
import zmq

from communication import ZMQContextManager
from marmobox_interface import MarmoboxInterface


MAX_LENGTH = 4096
PORT = 10000
HOST = '0.0.0.0'

stop_event = Event()

logger = logging.getLogger(__name__)
log_queue = queue.Queue()


def thread_log(level, msg):
    """ Since this is a separate thread, logging doesn't work the same.
    We'll use a thread-safe queue to transmit log messages to the main
    thread where they can be logged.
    """
    assert hasattr(logging, level.upper())
    assert isinstance(msg, str)
    msg = f"ListenerThread: {msg}"
    context = {
        'filename': inspect.stack()[1].filename,
        'pathname': inspect.stack()[1].filename,
        'funcName': inspect.stack()[1].function,
        'lineno': inspect.stack()[1].lineno,
        'level': getattr(logging, level.upper()),
        'msg': msg,
    }
    log_queue.put(context)


def print_thread_log():
    """ Call from main thread to log queued listener thread messages.
    """
    while not log_queue.empty():
        context = log_queue.get()
        level = context.get("level")
        pathname = context.get("pathname")
        record = logging.makeLogRecord(context)
        record.filename = os.path.basename(pathname)
        record.module = os.path.splitext(record.filename)[0]
        record.levelno = level
        logger.handle(record)
        log_queue.task_done()


def dict_to_lines(obj):
    """ Convert a dictionary to a pretty-printed list of string lines, for
    legible logging.
    """
    import pprint
    return pprint.pformat(obj).splitlines()


def stop_listener(signum, frame):
    """ Invoked when Ctrl-C or Ctrl-D are pressed, sending a kill signal.
    Sets the `stop_event` flag, which indicates in a thread-safe way to the
    listener thread that it is time to stop.
    """
    stop_event.set()
    msg = f"Stopping listener, caught signal {signum}"
    logger.debug(msg)
    raise ListenerExit(msg)


class NumpyFloat32Encoder(json.JSONEncoder):
    """ Custom JSON encoder to correctly convert numpy floats to string.
    """
    # pylint: disable=no-value-for-parameter
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return json.JSONEncoder.default(obj)


class ListenerExit(Exception):
    """ Custom exception for ListenerThread to emit when quitting.
    Raised when a kill signal is received or ListenerThread.stop() is
    invoked (used in testing).
    """
    pass


class UnhandledMessage(ValueError):
    """ Raised when ListenerThread doesn't know how to handle the message.
    """
    pass


class ListenerThread(Thread):

    def __init__(
        self,
        host,
        port,
        marmobox_interface,
    ):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.mbox_interface = marmobox_interface
        self.socket = None
        thread_log("debug", "ListenerThread initiated")

    def pack_response(self, obj, success=1, error=False):
        """ Put response in dictionary with format expected by controller
        """
        if not error:
            response = {
                "success": success,
                "body": {
                    "data": obj,
                }
            }
        else:
            response = {
                "success": success,
                "error": 1,
                "body": {
                    "error": obj,
                }
            }
        return response

    def send(self, msg):
        """ Prepare message and send it out on the socket.
        """
        msg = self.pack_response(msg)
        msg = json.dumps(msg, cls=NumpyFloat32Encoder)
        msg_in_bytes = bytes(msg, "utf8")
        thread_log("debug", f"Listener sending {len(msg_in_bytes)} bytes")
        if len(msg_in_bytes) > MAX_LENGTH:
            raise Exception(f"Message too long: {len(msg_in_bytes)} bytes.")
        self.socket.send(msg_in_bytes)

    def recv(self):
        """ Check socket for new message; load into JSON dict or unpickle
        Python object before returning.
        """
        buf = self.socket.recv()
        if buf is None:
            return None
        else:
            try:
                msg = json.loads(buf.decode())
            except Exception as exc:
                thread_log("debug", f"{str(type(exc))} {str(exc)}")
                thread_log("debug", "Can't load JSON, trying pickle...")
                try:
                    msg = pickle.loads(buf)
                except pickle.UnpicklingError as exc:
                    thread_log("error", "Cannot unpickle message:")
                    thread_log("error", f"{buf.decode()}")
            return msg

    def run(self):
        """ Implement Thread.run(), called downstream of Thread.start().
        """
        # Terminate context when control flow exits `with` block:
        with ZMQContextManager(thread_log=thread_log) as zmq_context:
            # Close socket when control flow exits `with` block:
            with zmq_context.socket(zmq.REP) as socket:
                self.socket = socket
                self.socket.setsockopt(zmq.LINGER, 0)
                self.socket.bind(f"tcp://{self.host}:{self.port}")
                # Pass `self` because the strategy is a function, not a
                # class-bound method (does not automatically receive `self`):
                try:
                    self.start_trial_agent()
                    #self.send({'status': 'init success'})

                    poller = zmq.Poller()
                    poller.register(self.socket, zmq.POLLIN)
                    timeout = 300   # milliseconds
                    while not stop_event.is_set():
                        events = poller.poll(timeout)
                        if events:
                            msg = self.recv()
                            self.handle_message(msg)
                        else:
                            thread_log("debug", "No request received")

                except Exception as exc:
                    import traceback
                    tb = traceback.format_tb(exc.__traceback__)
                    error_lines = [f"Exception on listener-side (miniPC): {type(exc)} {str(exc)}"]
                    if hasattr(exc, "unhandled_message"):
                        error_lines.extend(exc.unhandled_message)
                    error_lines.extend(tb)
                    message = self.pack_response(error_lines, error=True, success=0)
                    self.socket.send(bytes(json.dumps(message), "utf-8"))
                    for line in error_lines:
                        thread_log("error", line)
                finally:
                    self.stop_trial_agent()

    def handle_message(self, msg):
        """ Iterate through message handlers in order, attempting to handle
        each message.
        """
        thread_log("debug", "Received message:")
        for line in dict_to_lines(msg):
            thread_log("debug", line)

        c = self.__class__.__name__
        if not isinstance(msg, dict):
            raise UnhandledMessage(f"{c} only handles dicts")
        if not "action" in msg:
            raise UnhandledMessage(f"{c} missing required key: 'action'")
        if msg["action"] == "run_trial":
            if "trial_params" in msg:
                trial_params = msg['trial_params']
                trial_data = self.run_trial(trial_params)
                self.send(trial_data)
            else:
                exc = f"{c} missing required key: 'trial_params'"
                raise UnhandledMessage(exc)
        elif msg["action"] == "heartbeat":
            # Let requester know listener is listening:
            self.send("listening")
        else:
            log = f"{c} could not interpret message:"
            thread_log("error", log)
            unhandled_message = dict_to_lines(msg)
            for line in unhandled_message:
                thread_log("error", line)
            exc = UnhandledMessage(log)
            exc.unhandled_message = unhandled_message
            raise exc

    def start_trial_agent(self):
        self.mbox_interface.initialize()

    def stop_trial_agent(self):
        self.mbox_interface.close()

    def run_trial(self, trial_params):
        trial_data = self.mbox_interface.run_trial(trial_params)
        return trial_data

    def stop(self):
        """ Method for manually stopping a ListenerThread, useful for testing.
        """
        msg = f"{self.__class__.__name__}.stop() called."
        thread_log("debug", msg)
        stop_event.set()
        raise ListenerExit(msg)


def main():
    parser = argparse.ArgumentParser(description='Marmobox server. \
        Waits for client then opens psychopy window and Arduino USB interface.')
    parser.add_argument('port', help='Arduino port (e.g. "ttyACM0")', type=str)
    parser.add_argument('--width', help='Width of the Psychopy window', type=int, default=1280)
    parser.add_argument('--height', help='Height of the Psychopy window', type=int, default=720)
    parser.add_argument('--dummy', help='Dummy box (no actuators)', dest='dummy', action='store_true')
    parser.add_argument('--fullscreen', help='Psychopy window is fullscreen', dest='fullscreen', action='store_true')
    parser.set_defaults(dummy=False, fullscreen=False)
    args = parser.parse_args()

    arduino_port = args.port
    width = args.width
    height = args.height
    dummy = args.dummy
    fullscreen = args.fullscreen
    _main(arduino_port, width, height, dummy, fullscreen)


def _main(arduino_port, width, height, dummy, fullscreen):
    assert arduino_port
    assert width
    assert height
    assert fullscreen
    window_size = (width, height)
    is_dummy = dummy
    is_fullscreen = fullscreen
    signal.signal(signal.SIGTERM, stop_listener)
    signal.signal(signal.SIGINT, stop_listener)

    print(f'Listening for incoming connections')
    thread = None
    while not stop_event.is_set():
        try:
            marmobox_interface = MarmoboxInterface(
                arduino_port,
                window_size,
                is_dummy,
                is_fullscreen,
            )
            thread = ListenerThread(
                HOST,
                PORT,
                marmobox_interface,
            )
            thread.start()
            print_thread_log()
        except ListenerExit as exc:
            if thread:
                thread.stop()
        finally:
            print_thread_log()
            thread.join()
        print('Exiting main thread')


if __name__ == '__main__':
    main()
