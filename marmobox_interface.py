import time
import marmobox_stimuli as st
from marmobox_IO import MarmoboxIO
from psychopy import visual, event, logging

class MarmoboxInterface:
    def __init__(self, arduino_port, window_size, is_dummy, is_fullscreen):
        self.arduino_port = arduino_port
        self.window_size = window_size
        self.is_dummy = is_dummy
        self.is_fullscreen = is_fullscreen

    def initialize(self):
        self.box = MarmoboxIO(self.arduino_port, dummy=self.is_dummy)
        self.box.connect()
        self.ppy_window = visual.Window(self.window_size, monitor='test', units='pix', pos=(0,0), fullscr=self.is_fullscreen)
        self.ppy_mouse = event.Mouse(win=self.ppy_window, visible=self.is_dummy)
        logging.console.setLevel(logging.ERROR)
        return True

    def close(self):
        self.box.disconnect()
        self.ppy_window.close()
        self.ppy_mouse = None

    def run_trial(self, trial_params):
        return st.process_stimulus(trial_params, self.box, self.ppy_window, self.ppy_mouse)
