from task_builder import StimulusShape, Outcome, WindowTransition
from datetime import datetime
from psychopy import visual
import math
import time
from serial import SerialException

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
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.IMAGE:
			return visual.ImageStim(win=ppy_window, colorSpace='rgb')
		elif shape == StimulusShape.ARROW_E:
			arrow_vertices = [(4, 0), (0,-3), (0,-1), (-3,-1), (-3, 1), (0, 1), (0, 3)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.ARROW_W:
			arrow_vertices = [(-4, 0), (0,-3), (0,-1), (3,-1), (3, 1), (0, 1), (0, 3)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.ARROW_S:
			arrow_vertices = [(0,-4), (-3,0), (-1,0), (-1,3), (1,3), (1,0), (3,0)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.TRIANGLE:
			triangle_vertices = [(-5,4), (5,4), (0, -4)]
			return visual.ShapeStim(win=ppy_window, vertices=triangle_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.ARROW_NE:
			arrow_vertices = [(2.83,2.83), (-2.12,2.12), (-0.71,0.71), (-2.83,-1.41), (-1.41,-2.83), (0.71,-0.71), (2.12,-2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.ARROW_NW:
			arrow_vertices = [(-2.83,2.83), (2.12,2.12), (0.71,0.71), (2.83,-1.41), (1.41,-2.83), (-0.71,-0.71), (-2.12,-2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.ARROW_SE:
			arrow_vertices = [(2.83,-2.83), (-2.12,-2.12), (-0.71,-0.71), (-2.83,1.41), (-1.41,2.83), (0.71,0.71), (2.12,2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')
		elif shape == StimulusShape.ARROW_SW:
			arrow_vertices = [(-2.83,-2.83), (2.12,-2.12), (0.71,-0.71), (2.83,1.41), (1.41,2.83), (-0.71,0.71), (-2.12,2.12)]
			return visual.ShapeStim(win=ppy_window, vertices=arrow_vertices, colorSpace='rgb255')

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
		window_flip = datetime.now()
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
			window_flip = datetime.now()
		return window_flip

	def get_touch_outcome(self, window, flip_time, ppy_mouse):
		stimulus, touch_event, outcome = self.__check_touch(window, flip_time, ppy_mouse)
		if stimulus: #NB: flip time is recorded here (JS 3/5/2022)
			if len(stimulus.after_touch) > 0:
				stimulus.on_touch()
			stimulus.record_touch_data(
				touch_event['xcoor'],
				touch_event['ycoor'],
				flip_time,
				touch_event['touch_time'],
				touch_event['release_time'])
		elif not stimulus: #test
			stimulus.record_touch_data(flip_time) #test
		elif window.is_outside_fail and touch_event:
			window.fail_position = (touch_event['xcoor'], touch_event['ycoor'])
		return outcome

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
							window.active_timeout = (window.timeout - touch_elapsed) + stimulus.timeout_gain

						position = ppy_mouse.getPos()
						touch_event = {
							'xcoor': position[0],
							'ycoor': position[1],
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
							touch_event['release_time'] = release_time
							print('released')
							return stimulus, touch_event, stimulus.outcome
				print('outside, waiting for release')
				position = ppy_mouse.getPos()
				touch_event = {
					'xcoor': position[0],
					'ycoor': position[1],
					'touch_time': touch_time
				}
				while ppy_mouse.getPressed()[0]:
					time.sleep(0.001)
				print('released')
				if window.is_outside_fail:
					return None, touch_event, Outcome.FAIL

	def __wait_touch(self, window, ppy_mouse):
		print('waiting')
		start = datetime.now()
		while not ppy_mouse.getPressed()[0]:
			time.sleep(0.001)
			if window.active_timeout > 0 and (datetime.now() - start).total_seconds() > window.active_timeout: # Here, the variable 'start' is refreshed after each touch, so touching outside stimuli resets timeout - need to fix (JS (02/03/2022))
				return 0, 0, True
		touch_time = datetime.now()
		return touch_time, (touch_time - start).total_seconds(), False

def run_trial(windows, box, ppy_window, ppy_mouse):
	ppy_runtime = WindowRuntime()
	ppy_mouse.clickReset()

	outcome = Outcome.NULL
	box_status = "CalliCog OK"

	trial_data = []
	for window in windows[:-1]:
		flip_time = ppy_runtime.run_window(window, ppy_window)
		window.flip_tstamp = flip_time

		if window.is_outcome or window.timeout > 0:
			targets = [stimulus for stimulus in window.stimuli if stimulus.outcome == Outcome.SUCCESS]
			while not all([target.touched for target in targets]):
				outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)
				if (outcome == Outcome.FAIL) or (outcome == Outcome.NULL):
					break
			
			if window.timeout > 0:
				outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)

			# evaluate window outcome - this is likely where the bug is currently (JS 3/5/2022)
			if outcome == Outcome.SUCCESS:
				print('box: correct')
				try:
					box.correct()
				except SerialException:
					box_status = 'SerialException. ARDUINO CONNECTION LOST. NO REWARD/FEEDBACK GIVEN.'
			elif outcome == Outcome.FAIL:
				print('box: incorrect')
				try:
					box.incorrect()
				except:
					box_status = 'SerialException. ARDUINO CONNECTION LOST. NO REWARD/FEEDBACK GIVEN.'
			elif window.is_outcome == False:
				pass	

		elif window.blank is not None: #test
			outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)

		# save to JSON
		window_obj = window.pack_data()
		window_obj['stimuli'] = []
		for stimulus in window.stimuli:
			window_obj['stimuli'].append(stimulus.pack_data())
		trial_data.append(window_obj)
		window.reset()

		if outcome == Outcome.NULL: #new
			break #new

	# Penalty timeout. NB: touch or window data is not currently recorded, nor the added delay displayed in terminal.
	if outcome == Outcome.FAIL:
		flip_time = ppy_runtime.run_window(windows[-1], ppy_window)
		windows[-1].flip_tstamp = flip_time
		windows[-1].reset()

	return datetime.now(), outcome, trial_data, box_status
	# this is the last outcome from all windows