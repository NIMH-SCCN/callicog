from numpy import random
from datetime import datetime
import time
import math

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

class StimulusShape:
	SQUARE = 'square'
	CIRCLE = 'circle'
	STAR = 'star'
	DIAMOND = 'diamond'
	ARROW_N = 'arrow_n'
	IMAGE = 'image'
	ARROW_S = 'arrow_s'
	ARROW_E = 'arrow_e'
	ARROW_W = 'arrow_w'
	ARROW_NE = 'arrow_ne'
	ARROW_NW = 'arrow_nw'
	ARROW_SE = 'arrow_se'
	ARROW_SW = 'arrow_sw'
	TRIANGLE = 'triangle'

class Window:
	def __init__(self, blank=0, transition=None, is_outcome=False, timeout=0):
		self.blank = blank
		self.transition = transition
		self.is_outcome = is_outcome
		self.timeout = timeout
		self.ppy_window = None
		self.stimuli = []

	def add_stimulus(self, stimulus):
		self.stimuli.append(stimulus)
		stimulus.window = self

	def reset(self):
		for stimulus in self.stimuli:
			stimulus.ppy_show_stim.autoDraw = False
			stimulus.ppy_touch_stim.autoDraw = False

	def pack_data(self):
		return {
			'is_outcome': self.is_outcome,
			'delay': self.blank,
			'transition': self.transition,
			'timeout': self.timeout
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
		self.auto_draw = False
		self.after_touch = []
		self.timeout_gain = 0

	def draw(self):
		self.ppy_show_stim.draw()
		self.ppy_touch_stim.draw()

	def on_touch(self):
		for func in self.after_touch:
			if func["name"] == 'hide':
				self.__hide()

	def pack_data(self):
		return {
			'shape': self.shape,
			'size': self.size,
			'position': self.position,
			'outcome': self.outcome,
			'color': self.color,
			'image': self.image,
			'timeout_gain': self.timeout_gain
		}

	def __hide(self):
		self.ppy_show_stim.autoDraw = False
		self.ppy_touch_stim.autoDraw = False
		self.window.ppy_window.flip()
