from task_builder import StimulusShape, Outcome, WindowTransition
from datetime import datetime
from psychopy import visual
import math
import time

class WindowRuntime:
	def __get_ppy_stim_from_shape(self, shape, ppy_window):
		if shape == StimulusShape.SQUARE:
			return visual.Rect(win=ppy_window, colorSpace='rgb')
		elif shape == StimulusShape.CIRCLE:
			return visual.Circle(win=ppy_window, colorSpace='rgb')
		elif shape == StimulusShape.STAR:
			star_vertices = []
			outer_radius = 131
			inner_radius = 65
			for vertex in range(0,5):
				x = outer_radius*math.cos(math.radians(90+vertex*72))
				y = outer_radius*math.sin(math.radians(90+vertex*72))
				star_vertices.append([x,y]); x = inner_radius*math.cos(math.radians(126+vertex*72))
				y = inner_radius*math.sin(math.radians(126+vertex*72))
				star_vertices.append([x,y])
			return visual.ShapeStim(win=ppy_window, vertices=star_vertices, units = 'pix', colorSpace='rgb')
		elif shape == StimulusShape.DIAMOND:
			return visual.Rect(win=ppy_window, ori=45, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_N:
			arrow_vertices = [(0,4), (-3,0), (-1,0), (-1,-3), (1,-3), (1,0), (3,0)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.IMAGE:
			return visual.ImageStim(win=ppy_window, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_E:
			arrow_vertices = [(4, 0), (0,-3), (0,-1), (-3,-1), (-3, 1), (0, 1), (0, 3)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_W:
			arrow_vertices = [(-4, 0), (0,-3), (0,-1), (3,-1), (3, 1), (0, 1), (0, 3)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_S:
			arrow_vertices = [(0,-4), (-3,0), (-1,0), (-1,3), (1,3), (1,0), (3,0)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.TRIANGLE:
			triangle_vertices = [(-5,4), (5,4), (0, -4)]
			return visual.ShapeStim(win=ppy_window, vertices=triangle_vertices, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_NE:
			arrow_vertices = [(2.83,2.83), (-2.12,2.12), (-0.71,0.71), (-2.83,-1.41), (-1.41,-2.83), (0.71,-0.71), (2.12,-2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_NW:
			arrow_vertices = [(-2.83,2.83), (2.12,2.12), (0.71,0.71), (2.83,-1.41), (1.41,-2.83), (-0.71,-0.71), (-2.12,-2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_SE:
			arrow_vertices = [(2.83,-2.83), (-2.12,-2.12), (-0.71,-0.71), (-2.83,1.41), (-1.41,2.83), (0.71,0.71), (2.12,2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_SW:
			arrow_vertices = [(-2.83,-2.83), (2.12,-2.12), (0.71,-0.71), (2.83,1.41), (1.41,2.83), (-0.71,0.71), (-2.12,2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb')

	def __load_stimulus(self, stimulus, ppy_window):
		stimulus.ppy_touch_stim = visual.Rect(win=ppy_window, opacity=0)
		if stimulus.size_touch:
			stimulus.ppy_touch_stim.size = stimulus.size_touch
		else:
			stimulus.ppy_touch_stim.size = stimulus.size
		stimulus.ppy_touch_stim.pos = stimulus.position
		stimulus.ppy_touch_stim.autoDraw = stimulus.auto_draw

		stimulus.ppy_show_stim = self.__get_ppy_stim_from_shape(stimulus.shape, ppy_window)
		stimulus.ppy_show_stim.size = stimulus.size
		stimulus.ppy_show_stim.color = stimulus.color
		stimulus.ppy_show_stim.pos = stimulus.position
		stimulus.ppy_show_stim.image = stimulus.image
		stimulus.ppy_show_stim.autoDraw = stimulus.auto_draw

	def run_window(self, window, ppy_window):
		window.ppy_window = ppy_window
		ppy_window.flip()
		print('--- new window!')
		if window.blank > 0:
			time.sleep(window.blank)
			print(f'blank for {window.blank} seconds')
			#return
		if len(window.stimuli) > 0:
			for stimulus in window.stimuli:
				self.__load_stimulus(stimulus, ppy_window)
				stimulus.draw()
				print('stim drawn')
			ppy_window.flip()
		return datetime.now()

	def get_touch_outcome(self, window, flip_time, ppy_mouse):
		stimulus, touch_event, outcome = self.__check_touch(window, flip_time, ppy_mouse)
		if stimulus and len(stimulus.after_touch) > 0:
			stimulus.on_touch()
		return stimulus, touch_event, outcome

	def __check_touch(self, window, flip_time, ppy_mouse):
		touch_event = None
		while True:
			touch_time, touch_elapsed, timed_out =  self.__wait_touch(window, ppy_mouse)
			if timed_out:
				print('timed out')
				return None, touch_event, Outcome.NULL
			else:
				print('touched')
				for stimulus in window.stimuli:
					if ppy_mouse.isPressedIn(stimulus.ppy_touch_stim):
						stimulus.touched = True
						if stimulus.outcome == Outcome.SUCCESS and stimulus.timeout_gain > 0:
							window.timeout = (window.timeout - touch_elapsed) + stimulus.timeout_gain

						position = ppy_mouse.getPos()
						touch_event = {
							'xcoor': position[0],
							'ycoor': position[1],
							#'delay': (touch_time - flip_time).total_seconds()
							'touch_time': touch_time
						}
						if window.transition == WindowTransition.TOUCH:
							print(f'in object, on touch, waiting for release')
							while ppy_mouse.getPressed()[0]:
								time.sleep(0.001)
							release_time = datetime.now()
							touch_event['release_time'] = release_time
							print('released')
							return stimulus, touch_event, stimulus.outcome
						elif window.transition == WindowTransition.RELEASE:
							print(f'in object, waiting for release')
							while ppy_mouse.getPressed()[0]:
								time.sleep(0.001)
							release_time = datetime.now()
							#touch_event['delay'] = (release_time - flip_time).total_seconds()
							touch_event['release_time'] = release_time
							print('released')
							return stimulus, touch_event, stimulus.outcome
				print('outside, waiting for release')
				while ppy_mouse.getPressed()[0]:
					time.sleep(0.001)
				print('released')

	def __wait_touch(self, window, ppy_mouse):
		print('waiting')
		start = datetime.now()
		while not ppy_mouse.getPressed()[0]:
			time.sleep(0.001)
			if window.timeout > 0 and (datetime.now() - start).total_seconds() > window.timeout:
				return 0, 0, True
		touch_time = datetime.now()
		return touch_time, (touch_time - start).total_seconds(), False

def pack_event_data(stimulus=None, window=None, x=None, y=None, flip=None, touch=None, release=None, timeout=None):
	event = {
		'stimulus': stimulus,
		'window': window,
		'x': x,
		'y': y,
		'flip': str(flip) if flip else None,
		'touch': str(touch) if touch else None,
		'release': str(release) if release else None,
		'timeout': str(timeout) if timeout else None
	}
	return event

def run_trial(windows, box, ppy_window, ppy_mouse):
	ppy_runtime = WindowRuntime()
	ppy_mouse.clickReset()

	outcome = Outcome.NULL
	#touch_event = None

	events = []
	for window in windows:
		flip_time = ppy_runtime.run_window(window, ppy_window)
		events.append(pack_event_data(flip=flip_time, window=window.pack_data()))
		
		if window.is_outcome:
			targets = [stimulus for stimulus in window.stimuli if stimulus.outcome == Outcome.SUCCESS]
			while not all([target.touched for target in targets]):
				stimulus, touch_event, outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)
				if stimulus:
					events.append(
						pack_event_data(
							stimulus=stimulus.pack_data(), 
							x=touch_event['xcoor'], 
							y=touch_event['ycoor'], 
							flip=flip_time,
							touch=touch_event['touch_time'],
							release=touch_event['release_time']))
				if (outcome == Outcome.FAIL) or (outcome == Outcome.NULL):
					break
			# evaluate window outcome
			if outcome == Outcome.SUCCESS:
				print('box: correct')
				box.correct()
			elif outcome == Outcome.FAIL:
				print('box: incorrect')
				box.incorrect()
		elif window.blank == 0:
			stimulus, touch_event, outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)
			if stimulus:
				events.append(
					pack_event_data(
						stimulus=stimulus.pack_data(), 
						x=touch_event['xcoor'], 
						y=touch_event['ycoor'], 
						flip=flip_time,
						touch=touch_event['touch_time'],
						release=touch_event['release_time']))
		window.reset()

	return datetime.now(), outcome, events
	# this is the last outcome from all windows