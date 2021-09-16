from psychopy import visual
from numpy import random
import time
from datetime import datetime
import math

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

class WindowOld:
	def __init__(self, transition, stimuli, params=[]):
		self.transition = transition
		self.stimuli = stimuli
		self.parameters = params
		self.timeout = 0

	def load(self):
		for param in self.parameters:
			if param.param == Param.TIMEOUT:
				self.timeout = param.get_value()

# new classes
class WindowTransition:
	RELEASE = 'release'
	TOUCH = 'touch'

class StimulusShape:
	SQUARE = 'square'
	CIRCLE = 'circle'
	STAR = 'star'
	DIAMOND = 'diamond'
	ARROW = 'arrow'

class Window:
	def __init__(self, blank=0, transition=None, is_outcome=False, timeout=0):
		self.blank = blank
		self.transition = transition
		self.is_outcome = is_outcome
		self.timeout = timeout
		#self.ppy_window = None
		#self.ppy_mouse = None
		self.stimuli = []

	def add_stimulus(self, stimulus):
		self.stimuli.append(stimulus)
		stimulus.window = self

	def run(self, ppy_window):
		self.ppy_window =  ppy_window

		self.ppy_window.flip()
		print('--- new window!')
		if self.blank > 0:
			time.sleep(self.blank)
			print(f'blank for {self.blank} seconds')
			#return
		if len(self.stimuli) > 0:
			for stimulus in self.stimuli:
				stimulus.load()
				stimulus.draw()
				print('stim drawn')
			self.ppy_window.flip()
		return datetime.now()
		#touch_event, outcome = self.__check_touch(ppy_mouse, datetime.now())
		#return touch_event, outcome

	def get_touch_outcome(self, flip_time, ppy_mouse):
		stimulus, touch_event, outcome = self.__check_touch(ppy_mouse, flip_time)
		if stimulus and len(stimulus.after_touch) > 0:
			stimulus.on_touch()
		return touch_event, outcome

	def __wait_touch(self, ppy_mouse):
		print('waiting')
		start = datetime.now()
		while not ppy_mouse.getPressed()[0]:
			time.sleep(0.001)
			if self.timeout > 0 and (datetime.now() - start).total_seconds() > self.timeout:
				return 0, 0, True
		touch_time = datetime.now()
		return touch_time, (touch_time - start).total_seconds(), False

	def reset(self):
		for stimulus in self.stimuli:
			stimulus.ppy_show_stim.autoDraw = False
			stimulus.ppy_touch_stim.autoDraw = False

	def __check_touch(self, ppy_mouse, flip_time):
		touch_event = None
		while True:
			touch_time, touch_elapsed, timed_out =  self.__wait_touch(ppy_mouse)
			if timed_out:
				print('timed out')
				return None, touch_event, Outcome.NULL
			else:
				print('touched')
				for stimulus in self.stimuli:
					if ppy_mouse.isPressedIn(stimulus.ppy_touch_stim):
						stimulus.touched = True
						if stimulus.outcome == Outcome.SUCCESS and stimulus.timeout_gain > 0:
							self.timeout = (self.timeout - touch_elapsed) + stimulus.timeout_gain

						position = ppy_mouse.getPos()
						touch_event = {
							'xcoor': position[0],
							'ycoor': position[1],
							'delay': (touch_time - flip_time).total_seconds()
						}
						if self.transition == WindowTransition.TOUCH:
							print(f'in object, on touch, waiting for release')
							while ppy_mouse.getPressed()[0]:
								time.sleep(0.001)
							print('released')
							return stimulus, touch_event, stimulus.outcome
						elif self.transition == WindowTransition.RELEASE:
							print(f'in object, waiting for release')
							while ppy_mouse.getPressed()[0]:
								time.sleep(0.001)
							release_time = datetime.now()
							print('released')
							touch_event['delay'] = (release_time - flip_time).total_seconds()
							return stimulus, touch_event, stimulus.outcome
				print('outside, waiting for release')
				while ppy_mouse.getPressed()[0]:
					time.sleep(0.001)
				print('released')

class Stimulus:
	def __init__(self, shape, size, size_touch=None, position=None, outcome=None, color=None, window=None):
		self.shape = shape
		self.size = size
		self.size_touch = size_touch
		self.color = color
		self.position = position
		self.touched = False
		self.outcome = outcome
		self.ppy_show_stim = None
		self.ppy_touch_stim = None
		self.auto_draw = False
		self.after_touch = []
		self.timeout_gain = 0
		self.window = window

	def __assign_shape(self):
		if self.shape == StimulusShape.SQUARE:
			return visual.Rect(win=self.window.ppy_window, colorSpace='rgb')
		elif self.shape == StimulusShape.CIRCLE:
			return visual.Circle(win=self.window.ppy_window, colorSpace='rgb')
		elif self.shape == StimulusShape.STAR:
			star_vertices = []
			outer_radius = 131
			inner_radius = 65
			for vertex in range(0,5):
				x = outer_radius*math.cos(math.radians(90+vertex*72))
				y = outer_radius*math.sin(math.radians(90+vertex*72))
				star_vertices.append([x,y]); x = inner_radius*math.cos(math.radians(126+vertex*72))
				y = inner_radius*math.sin(math.radians(126+vertex*72))
				star_vertices.append([x,y])
			return visual.ShapeStim(self.window.ppy_window, vertices=star_vertices, colorSpace='rgb')
		elif self.shape == StimulusShape.DIAMOND:
			return visual.Rect(win=self.window.ppy_window, ori=45, colorSpace='rgb')
		elif self.shape == StimulusShape.ARROW:
			arrow_vertices = [(0,4), (-3,0), (-1,0), (-1,-3), (1,-3), (1,0), (3,0)]
			return visual.ShapeStim(win=self.window.ppy_window, vertices=arrow_vertices, colorSpace='rgb')

	def load(self):
		self.ppy_touch_stim = visual.Rect(win=self.window.ppy_window, opacity=0)
		if self.size_touch:
			self.ppy_touch_stim.size = self.size_touch
		else:
			self.ppy_touch_stim.size = self.size
		self.ppy_touch_stim.pos = self.position
		self.ppy_touch_stim.autoDraw = self.auto_draw

		self.ppy_show_stim = self.__assign_shape()
		self.ppy_show_stim.size = self.size
		self.ppy_show_stim.color = self.color
		self.ppy_show_stim.pos = self.position
		self.ppy_show_stim.autoDraw = self.auto_draw

	def draw(self):
		self.ppy_show_stim.draw()
		self.ppy_touch_stim.draw()

	def on_touch(self):
		for func in self.after_touch:
			if func["name"] == 'hide':
				self.__hide()

	def __hide(self):
		self.ppy_show_stim.autoDraw = False
		self.ppy_touch_stim.autoDraw = False
		self.window.ppy_window.flip()






