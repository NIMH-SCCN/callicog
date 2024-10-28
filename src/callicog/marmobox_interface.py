import logging
import time
# import marmobox_stimuli as st
from serial.serialutil import SerialException
from psychopy import visual, event
from psychopy import logging as ppy_logging

from callicog.marmobox_IO import MarmoboxIO
from callicog.trial_interface import run_trial as run_trial_interface

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
                if "permission denied" in str(exc).lower():
                    logger.error(
                        f"Permission denied on USB serial port ({self.arduino_port})."
                        " Make sure user is in `dialout` group:"
                        "    `sudo usermod -a -G dialout sccn`"
                    )
                    raise exc
                print("Reward module not detected, check USB connection.")
                print(f"Retrying in {wait} seconds...") 
                time.sleep(wait)
                wait = wait + 1 if (wait < max_wait) else max_wait

        self.ppy_window = visual.Window(size=self.window_size, monitor='test', units='pix', pos=(0,0), fullscr=self.is_fullscreen, checkTiming=False)
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

    def process_stimulus(self, trial_params, box, ppy_window, ppy_mouse):
        trial_windows = trial_params['trial_windows']
        (run_end, trial_outcome, events, box_status) = run_trial_interface(trial_windows, box, ppy_window, ppy_mouse)
        return {'trial_end': str(run_end), 'trial_outcome': trial_outcome, 'events': events, 'box_status': box_status}

    def run_trial(self, trial_params):
        return self.process_stimulus(trial_params, self.box, self.ppy_window, self.ppy_mouse)
