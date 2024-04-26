import pytest
import threading
import time
import json
import logging

from timeit import default_timer as timer
from unittest.mock import patch
from unittest.mock import MagicMock

import zmq

from callicog.communication import ZMQContextManager
from callicog.marmobox import Marmobox
# from marmobox_listener import ListenerThread
# from marmobox_listener import ListenerExit
# from marmobox_listener import stop_event
# from marmobox_listener import ZMQContextManager
# from marmobox_listener import print_thread_log
# from marmobox_interface import MarmoboxInterface


logger = logging.getLogger(__name__)


stop_event = threading.Event()
host = "127.0.0.1"
port = "5563"


def test_marmobox_communication():
    attempts = 3
    with ReplySocketThread(host, port) as thread:
        with Marmobox(host, port, db_session=None) as controller:
            assert controller.socket
            time.sleep(0.1)
            for i in range(1, attempts+1):
                msg = {"attempt": i, "hello": "world"}
                controller.send(msg)
                time.sleep(0.1)
                reply = controller.receive(timeout=3)
                assert reply
                assert reply["received"] == msg
                # print(reply)
            thread.join()


class ReplySocketThread(threading.Thread):
    """ Listen on a ZMQ Reply socket similar to the listener, for testing
    messaging.
    """
    def __init__(self, host, port, max_duration=3):
        threading.Thread.__init__(self, name='ReplySocketThread')
        assert host
        assert port
        self.threadname = threading.current_thread()
        self.host = host
        self.port = port
        self.ctx = None
        self.max_duration = 3   # seconds

    def run(self):
        host = self.host
        port = self.port
        max_duration = self.max_duration
        threadname = self.threadname
        if stop_event.is_set():
            stop_event.clear()
        with ZMQContextManager() as ctx:
            with ctx.socket(zmq.REP) as socket:
                logging.debug(f"{threadname} running")
                # Close socket when control flow exits `with` block
                socket.bind(f"tcp://{host}:{port}")
                logging.debug(f"{threadname} socket bound")
                # Close socket when control flow exits `with` block
                poller = zmq.Poller()
                poller.register(socket, zmq.POLLIN)
                poll_timeout = 300   # milliseconds
                msg_count = 0
                start = timer()
                elapsed = 0
                while not (stop_event.is_set() or (elapsed > max_duration)):
                    logging.debug(f"{threadname} entered msg polling loop")
                    events = poller.poll(poll_timeout)
                    if events:
                        msg = socket.recv_json()
                        logging.debug(f"{threadname} received {str(msg)}")
                        msg_count += 1
                        reply = {"received": msg, "count": msg_count}
                        reply = json.dumps(reply)
                        reply = bytes(reply, "utf8")
                        socket.send(reply)
                    elapsed = timer() - start
                logging.debug(f"{threadname} run complete")
                self.stop()

    def stop(self):
        if not stop_event.is_set():
            stop_event.set()
        logging.debug(f"{self.threadname} stopped")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
