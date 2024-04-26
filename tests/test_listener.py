import pytest
import threading
import time
import json
import logging

from unittest.mock import patch
from unittest.mock import MagicMock

import zmq

# from communication import ZMQContextManager
from callicog.marmobox_listener import ListenerThread
from callicog.marmobox_listener import ListenerExit
from callicog.marmobox_listener import stop_event
from callicog.marmobox_listener import print_thread_log
from callicog.marmobox_interface import MarmoboxInterface


logger = logging.getLogger(__name__)


host = "127.0.0.1"
port = "5555"


@pytest.fixture
def ctx():
    context = zmq.Context()
    yield context
    context.term()
    logger.debug("context terminated")


@pytest.fixture
def listener_thread():
    if stop_event.is_set():
        stop_event.clear()
    logger.debug("listener_thread fixture invoked")
    marmobox_interface = None
    thread = ListenerThread(host, port, marmobox_interface)
    yield thread
    try:
        thread.stop()
    except ListenerExit:
        thread.join()
    logger.debug("listener_thread fixture teardown complete")


# Uses Python's mock module to provide a mock object that mimics a
# MarmoboxInterface, allowing us to test the ListenerThread independently of
# the actual trial logic, Psychopy, carried out via MarmoboxInterface 
@patch("marmobox_interface.MarmoboxInterface")
def test_default_run_strategy(marmobox_interface, ctx, listener_thread):
    mock_trial_results = {"result": "success"}
    marmobox_interface.run_trial.return_value = mock_trial_results
    listener_thread.mbox_interface = marmobox_interface
    with pytest.raises(ListenerExit):
        with ctx.socket(zmq.REQ) as client_socket:
            client_socket.setsockopt(zmq.LINGER, 0)
            listener_thread.start()
            client_socket.connect(f"tcp://{host}:{port}")
            poller = zmq.Poller()
            poller.register(client_socket, zmq.POLLIN)
            timeout = 1000   # milliseconds

            logger.debug("Testing heartbeat:")
            request = {"action": "heartbeat"}
            for i in range(1, 5):
                client_socket.send_string(json.dumps(request))
                events = poller.poll(timeout)
                if events:
                    response = client_socket.recv()
                    response = json.loads(response.decode())
                    print_thread_log()
                    if "error" in response:
                        error_lines = response["body"]["error"]
                        for line in error_lines:
                            logger.error(line)
                        raise ValueError("Error in listener thread.")
                    else:
                        assert response["success"]
                        assert response["body"]["data"] == "listening"
                        # logger.debug(str(response))
                else:
                    raise ValueError("No response received")

            logger.debug("Testing run_trial:")
            request = {"action": "run_trial", "trial_params": ["test"]}
            for i in range(1, 5):
                client_socket.send_string(json.dumps(request))
                events = poller.poll(timeout)
                if events:
                    response = client_socket.recv()
                    response = json.loads(response.decode())
                    print_thread_log()
                    if "error" in response:
                        error_lines = response["body"]["error"]
                        for line in error_lines:
                            logger.error(line)
                        raise ValueError("Error in listener thread.")
                    else:
                        assert response["success"]
                        assert response["body"]["data"] == mock_trial_results
                        # logger.debug(str(response))
                else:
                    raise ValueError("No response received")

            logger.debug("Testing bad request:")
            request = {"action": "bad_request"}
            client_socket.send_string(json.dumps(request))
            events = poller.poll(timeout)
            if events:
                response = client_socket.recv()
                response = json.loads(response.decode())
                print_thread_log()
                assert not response["success"]
                assert "error" in response
                error_lines = response["body"]["error"]
                for line in error_lines:
                    logger.debug(line)
            else:
                raise ValueError("No response received")
            
            listener_thread.stop()
            time.sleep(0.1)

    listener_thread.join()
