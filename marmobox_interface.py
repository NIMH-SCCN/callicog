import logging
import time
import marmobox_stimuli as st
from marmobox_IO import MarmoboxIO
from serial.serialutil import SerialException
from psychopy import visual, event
from psychopy import logging as ppy_logging

logger = logging.getLogger(__name__)


class MarmoboxInterface:
    def __init__(self, arduino_port, window_size, is_dummy, is_fullscreen):
        self.arduino_port = arduino_port
        self.window_size = window_size
        self.is_dummy = is_dummy
        self.is_fullscreen = is_fullscreen
        self.box = None
        self.ppy_window = None
        self.ppy_mouse = None

    def initialize(self):
        logger.debug("MarmoboxInterface.initialize()")
        self.box = MarmoboxIO(self.arduino_port, dummy=self.is_dummy)
        wait = 2    # seconds
        max_wait = 30
        connected = False
        while not connected:
            try:
                self.box.connect()
                connected = True
            except SerialException as exc:
                print("Reward module not detected, check USB connection.")
                print(f"Retrying in {wait} seconds...") 
                time.sleep(wait)
                wait = wait + 1 if (wait < max_wait) else max_wait

        self.ppy_window = visual.Window(self.window_size, monitor='test', units='pix', pos=(0,0), fullscr=self.is_fullscreen)
        self.ppy_mouse = event.Mouse(win=self.ppy_window, visible=self.is_dummy)
        ppy_logging.console.setLevel(ppy_logging.ERROR)
        logger.debug("Marmobox interface initialized")
        return True

    def close(self):
        if self.box:
            self.box.disconnect()
        if self.ppy_window:
            self.ppy_window.close()
        self.ppy_mouse = None

    def run_trial(self, trial_params):
        return st.process_stimulus(trial_params, self.box, self.ppy_window, self.ppy_mouse)
