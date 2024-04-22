from psychopy import visual, event, logging
from datetime import datetime
from numpy import random
import time

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

def wait_for_click(mouse, timeout=0):
	print('waiting')
	start = time.time()
	while not mouse.getPressed()[0]:
		time.sleep(0.001)
		if timeout > 0 and (time.time() - start) > timeout:
			return True
	return False

def pack_event_data(description, timestamp, position=None):
	event_dict = {}
	if position:
		event_dict["position"] = {
			"xcoor": position[0],
			"ycoor": position[1]
		}
	event_dict["description"] = description
	event_dict["timestamp"] = timestamp
	return event_dict

def check_stim_click(mouse, window):
	#event = {}
	while True:
		timed_out = wait_for_click(mouse, window.timeout)
		if timed_out:
			print('timed out')
			return Outcome.NULL
		else:
			print('clicked')
			for stimulus in window.stimuli:
				if mouse.isPressedIn(stimulus.ppy_stim.stim_object):
					#event['touch_pos'] = mouse.getPosition()
					if window.transition == 'on_click':
						print(f'in object {stimulus.stim_id}, on click')
						return stimulus.outcome
					elif window.transition == 'on_release':
						print(f'in object {stimulus.stim_id}, waiting to release')
						while mouse.getPressed()[0]:
							time.sleep(0.001)
						print('released')
						return stimulus.outcome
			print('outside, waiting to release')
			while mouse.getPressed()[0]:
				time.sleep(0.001)
			print('released')

def load_task(task_name):
	print(f'loading task: {task_name}')
	
	shape_list = [StimShape.RECT, StimShape.CIRCLE]
	timeout_list = [2, 4, 6]
	blue = [0, 0, 1]
	red = [1, 0, 0]
	yellow = [1, 1, 0]
	P1 = StimParam(Param.SHAPE, ParamType.PSEUDORANDOM)
	P2 = StimParam(Param.TIMEOUT, ParamType.PSEUDORANDOM)
	params = [P1, P2]
	
	w1 = Window('on_release', [PseudoStim(P1, [
											StimParam(Param.POSITION, 
												ParamType.CONSTANT, 
												[0, 0]),
											StimParam(Param.COLOR,
												ParamType.CONSTANT,
												yellow),
											StimParam(Param.WIDTH,
												ParamType.CONSTANT,
												200),
											StimParam(Param.HEIGHT,
												ParamType.CONSTANT,
												200),
											StimParam(Param.RADIUS,
												ParamType.CONSTANT,
												100)
											]
						)]
	)
	w2 = Window('blank', [], [ StimParam(Param.TIMEOUT, ParamType.CONSTANT, 2) ])
	w3 = Window('on_click', [PseudoStim(P1, [
											StimParam(Param.POSITION, 
												ParamType.CONSTANT, 
												[0, 0]),
											StimParam(Param.COLOR,
												ParamType.CONSTANT,
												yellow),
											StimParam(Param.WIDTH,
												ParamType.CONSTANT,
												200),
											StimParam(Param.HEIGHT,
												ParamType.CONSTANT,
												200),
											StimParam(Param.RADIUS,
												ParamType.CONSTANT,
												100)
											]
						)]
	)
	w4 = Window('blank', [], [P2])
	w5 = Window('on_release', [PseudoStim(P1, [
											StimParam(Param.POSITION, 
												ParamType.CONSTANT, 
												[-300, 0]),
											StimParam(Param.COLOR,
												ParamType.CONSTANT,
												yellow),
											StimParam(Param.WIDTH,
												ParamType.CONSTANT,
												200),
											StimParam(Param.HEIGHT,
												ParamType.CONSTANT,
												200),
											StimParam(Param.RADIUS,
												ParamType.CONSTANT,
												100)
											], outcome=Outcome.SUCCESS),
							RandomStim([
											StimParam(Param.POSITION, 
												ParamType.CONSTANT, 
												[300, 0]),
											StimParam(Param.COLOR,
												ParamType.CONSTANT,
												red),
											StimParam(Param.WIDTH,
												ParamType.CONSTANT,
												200),
											StimParam(Param.HEIGHT,
												ParamType.CONSTANT,
												200),
											StimParam(Param.RADIUS,
												ParamType.CONSTANT,
												100)
											], shape_list, [P1], outcome=Outcome.FAIL)
						], [P2]
	)

	windows = [w1, w2, w3, w4, w5]
	return windows, params

def run_trial(task_name, trial_config, box, ppy_window, ppy_mouse):
	
	ppy_window.flip()
	windows, params = load_task(task_name)

	for i, param in enumerate(params):
		param.set_value(trial_config[i])

	ppy_mouse.clickReset()
	
	outcome = Outcome.NULL
	event = None
	for i in range(len(windows)):
		window = windows[i]
		window.load()
		# new window, clear screen
		ppy_window.flip()
		for stimulus in window.stimuli:
			stimulus.load(ppy_window).draw()
		# show all stimuli
		print('--- new window!') #EVENT
		ppy_window.flip()

		if window.transition == 'blank':
			time.sleep(window.timeout)
			print(f'blank for {window.timeout} seconds') # EVENT
		else:
			outcome = check_stim_click(ppy_mouse, window) # MAIN EVENT

	if outcome == Outcome.SUCCESS:
		print('box: correct')
		box.correct()
	elif outcome == Outcome.FAIL:
		print('box: incorrect')
		box.incorrect()

	return datetime.now(), outcome
	# this is the last outcome from all windows

# np.array(np.meshgrid([1,2,3],[10,20,30,40,50,60],[-1,-2,-3,-4,-5,-6])).T.reshape(-1,3)
