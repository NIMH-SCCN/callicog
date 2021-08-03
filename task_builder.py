from psychopy import visual
from numpy import random

class Progression:
	SESSION_BASED = 'session_based'
	ROLLING_AVERAGE = 'rolling_average'
	TARGET_BASED = 'target_based'

class Outcome:
	SUCCESS = 'success'
	FAIL = 'fail'
	NULL = 'null'

class Param:
	POSITION = 'pos'
	COLOR = 'color'
	WIDTH = 'width'
	HEIGHT = 'height'
	RADIUS = 'radius'
	SHAPE = 'shape'
	TIMEOUT = 'timeout'

class ParamType:
	CONSTANT = 'const'
	PSEUDORANDOM = 'pseudo'
	RANDOM = 'rand'

class StimShape:
	RECT = 'rect'
	CIRCLE = 'circle'

class PPYStim:
	def __init__(self, ppy_window, shape, stim_params):
		self.ppy_window = ppy_window
		self.stim_object = self.__set_stim_object(ppy_window, shape, stim_params)

	def __set_stim_object(self, ppy_window, shape, stim_params):
		if shape == StimShape.RECT:
			stimulus = visual.Rect(win=self.ppy_window, colorSpace='rgb')
		elif shape == StimShape.CIRCLE:
			stimulus = visual.Circle(win=self.ppy_window, colorSpace='rgb')
		for param in stim_params:
			if param.param == Param.POSITION:
				stimulus.pos = param.get_value()
			if param.param == Param.COLOR:
				stimulus.fillColor = param.get_value()
				stimulus.lineColor = param.get_value()
			if param.param == Param.WIDTH:
				stimulus.width = param.get_value()
			if param.param == Param.HEIGHT:
				stimulus.height = param.get_value()
			if param.param == Param.RADIUS:
				stimulus.radius = param.get_value()
		return stimulus

class PseudoStim:
	def __init__(self, shape_param, stim_params, outcome=None):
		self.shape_param = shape_param
		self.stim_params = stim_params
		self.ppy_stim = None
		self.stim_id = '?'
		self.outcome = outcome

	def load(self, ppy_window):
		self.ppy_stim = PPYStim(ppy_window, self.shape_param.get_value(), self.stim_params)
		return self.ppy_stim.stim_object # change it perhaps?

class RandomStim: # use a Base Class perhaps
	def __init__(self, stim_params, options, exclude=[], outcome=None):
		self.options = options
		self.exclude = exclude
		self.stim_params = stim_params
		self.ppy_stim = None
		self.stim_id = '?'
		self.outcome = outcome

	def load(self, ppy_window):
		exclude_list = [param.get_value() for param in self.exclude]
		final_options = [shape for shape in self.options if shape not in exclude_list]
		self.ppy_stim = PPYStim(ppy_window, random.choice(final_options), self.stim_params)
		return self.ppy_stim.stim_object

class StimParam:
	def __init__(self, param, param_type, param_value=None):
		self.param = param
		self.param_type = param_type
		self.param_value = param_value

	def set_value(self, param_value):
		self.param_value = param_value

	def get_value(self):
		return self.param_value

class Window:
	def __init__(self, transition, stimuli, params=[]):
		self.transition = transition
		self.stimuli = stimuli
		self.parameters = params
		self.timeout = 0

	def load(self):
		for param in self.parameters:
			if param.param == Param.TIMEOUT:
				self.timeout = param.get_value()