from numpy import random
from datetime import datetime
import time
import math
import traceback

from pkg_resources import Distribution

class Parameter:
    #Define new parameters for stimuli
    POSITION = 'position'
    TARGET = 'target'
    DISTRACTOR = 'distractor'
    DELAY = 'delay'
    COLOR = 'color'

class Progression:
    SESSION_BASED = 'session_based'
    ROLLING_AVERAGE = 'rolling_average'
    TARGET_BASED = 'target_based'

class Outcome:
    SUCCESS = 'success'
    FAIL = 'fail'
    NULL = 'null'

class WindowTransition:
    RELEASE = 'release'
    TOUCH = 'touch'
    MAINTAIN = 'maintain'

class StimulusShape:
    SQUARE = 'square'
    CIRCLE = 'circle'
    STAR = 'star'
    DIAMOND = 'diamond'
    ARROW = 'arrow'
    IMAGE = 'image'
    TRIANGLE = 'triangle'

class Window:
    def __init__(self, blank=0, transition=None, is_outcome=False, timeout=0, is_outside_fail=False, label=''):
        self.blank = blank
        self.transition = transition
        self.aborted = False
        self.is_outcome = is_outcome
        self.is_outside_fail = is_outside_fail
        self.fail_position = None
        self.timeout = timeout
        self.label = label
        self.active_timeout = timeout
        self.ppy_window = None
        self.flip_tstamp = None
        self.stimuli = []
        self.post_touch_delay = None # Time in seconds to continue displaying stimuli after touch (i.e. for tasks that "hide" stimuli after a touch)
        self.is_delayed_after_touch = False

    def add_stimulus(self, stimulus):
        self.stimuli.append(stimulus)
        stimulus.window = self

    def reset(self):
        for stimulus in self.stimuli:
            stimulus.ppy_show_stim.autoDraw = False
            stimulus.ppy_touch_stim.autoDraw = False

    def pack_data(self):
        return {
            'label': self.label,
            'delay': self.blank,
            'transition': self.transition,
            'is_outcome': self.is_outcome,
            'is_outside_fail': self.is_outside_fail,
            'fail_position': self.fail_position,
            'timeout': self.timeout,
            'flip': str(self.flip_tstamp) if self.flip_tstamp else None
        }

class Stimulus:
    def __init__(self, shape, size, size_touch=None, position=None, outcome=None, color=None, window=None, image=None):
        self.shape = shape
        self.size = size
        self.size_touch = size_touch
        self.position = position
        self.outcome = outcome
        self.color = color
        self.window = window
        self.image = image

        self.ppy_show_stim = None
        self.ppy_touch_stim = None
        self.touched = False
        self.touch_pos = None
        self.flip_tstamp = None
        self.touch_tstamp = None
        self.release_tstamp = None

        self.auto_draw = False
        self.after_touch = []
        self.timeout_gain = 0

    def record_touch_data(self, touch_x, touch_y, flip, touch, release):
        self.touch_pos = (touch_x, touch_y)
        self.flip_tstamp = flip
        self.touch_tstamp = touch
        self.release_tstamp = release

    def draw(self):
        self.ppy_show_stim.draw()
        self.ppy_touch_stim.draw()

    def on_touch(self):
        for func in self.after_touch:
            if func["name"] == 'hide':
                self.__hide()
            if func["name"] == 'hide_other':
                self.__hide_other()

    def pack_data(self):
        return {
            'shape': self.shape,
            'size': self.size,
            'position': self.position,
            'outcome': self.outcome,
            'color': self.color,
            'image': self.image,
            'touched': self.touched,
            'touch_pos': self.touch_pos,
            'flip': str(self.flip_tstamp) if self.flip_tstamp else None,
            'touch': str(self.touch_tstamp) if self.touch_tstamp else None,
            'release': str(self.release_tstamp) if self.release_tstamp else None,
            'timeout_gain': self.timeout_gain
        }

    def __hide(self):
        self.ppy_show_stim.autoDraw = False
        self.ppy_touch_stim.autoDraw = False
        self.window.ppy_window.flip()
    
    def __hide_other(self):
        stimuli = self.window.stimuli
        for stimulus in stimuli:
            if stimulus is not self:
                stimulus.ppy_show_stim.autoDraw = False
                stimulus.ppy_touch_stim.autoDraw = False
        self.window.is_delayed_after_touch = True
        self.window.ppy_window.flip()