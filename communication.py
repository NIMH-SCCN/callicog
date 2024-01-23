import zmq
import logging


logger = logging.getLogger(__name__)


class ZMQContextManager(object):
    """ Context manager for providing a zmq context object in a `with` block,
    ensuring the context will always terminate, even if an exception occurs.
    """
    def __init__(self, *args, thread_log=None, **kwargs):
        self.context = zmq.Context(*args, **kwargs)
        # Special function to transmit logging from child thread to parent:
        self.thread_log = thread_log

    def __enter__(self):
        return self.context

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.context.term()
        if self.thread_log:
            self.thread_log("debug", "ZMQ context terminated")
        else:
            logger.debug("ZMQ context terminated")
