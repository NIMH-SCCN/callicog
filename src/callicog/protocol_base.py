from psychopy import visual, event
from datetime import datetime
from marmobox_IO import MarmoboxIO
import time

class Stimulus:
	def __init__(self, size, position, color, outcome):
		self.size = size
		self.position = position
		self.color = color
		self.outcome = outcome
		self.grating = None

class TouchEvent:
	def __init__(self, trial_index, position):
		self.trial_index = trial_index
		self.position = position
		self.stimulus = None
		self.outcome = None

	def set_stimulus(self, stimulus):
		self.stimulus = stimulus
		if self.stimulus:
			self.outcome = self.stimulus.outcome

	def record_timestamps(self, on_touch, on_release, on_stimulus):
		self.on_touch = on_touch
		self.on_release = on_release
		self.on_stimulus = on_stimulus

	def export(self):
		event_obj = {}
		first_reaction = (self.on_touch - self.on_stimulus).total_seconds()
		touch_elapsed = (self.on_release - self.on_touch).total_seconds()

		event_obj['trial_index'] = self.trial_index
		event_obj['stim_timestamp'] = str(self.on_stimulus)
		event_obj['xcoor'] = self.position[0]
		event_obj['ycoor'] = self.position[1]
		event_obj['reaction'] = first_reaction
		event_obj['touch_elapsed'] = touch_elapsed
		event_obj['outcome'] = self.outcome
		#event_obj['success'] = True # should depend on outcome or be scrapped
		return event_obj

	def print(self):
		print(f'touchEvent->pressed @({self.position[0]},{self.position[1]}, outcome={self.outcome})')

class Window:
	def __init__(self, window_size, stimuli, max_trials):
		self.window_size = window_size
		self.stimuli = stimuli
		self.max_trials = max_trials
		self.events = [] # or trials

	def load(self):
		# open Marmobox connection
		self.box = MarmoboxIO('ttyACM0')
		self.box.connect() # test for exceptions
		# define window
		self.window = visual.Window(self.window_size, monitor='test', units='pix', pos=(0,0))
		# define mouse
		self.mouse = event.Mouse(win=self.window)
		# define and append objects
		for stimulus in self.stimuli:
			grating = visual.GratingStim(
				win=self.window,
				size=stimulus.size,
				pos=stimulus.position,
				sf=0,
				color=stimulus.color,
				colorSpace='rgb')
			stimulus.grating = grating
		return self

	def save_touch_event(self, touch_event):
		self.events.append(touch_event)

	def reset_window(self):
		self.mouse.clickReset()
		self.window.flip(clearBuffer=True) # assuming it clears the screen

	def draw_window(self):
		for stimulus in self.stimuli:
			stimulus.grating.draw()
		self.window.flip(clearBuffer=False) # shows all stimuli



	def run(self):
		# window start
		run_start = datetime.now()
		self.reset_window()
		self.draw_window()
		timestamp_stimulus = datetime.now() # stimuli timestamp
		# record any touch
		while not self.mouse.getPressed()[0]:
			time.sleep(0.001)
		timestamp_touch = datetime.now()

		for ti in range(self.max_trials):
			self.reset_window()
			self.draw_window()
			



			# wait for response
			while not self.mouse.getPressed()[0]:
				time.sleep(0.001)
			timestamp_touch = datetime.now()

			# record touch event
			touch_event = TouchEvent(ti, self.mouse.getPos())
			for stimulus in self.stimuli:
				if self.mouse.isPressedIn(stimulus.grating):
					while self.mouse.getPressed()[0]:
						time.sleep(0.001)
					timestamp_release = datetime.now()
					touch_event.set_stimulus(stimulus)
					if stimulus.outcome:
						# give reward
						print('Correct! Reward given.')
						self.box.correct()
						time.sleep(2) # delay after reward
						#box.dosage(1000)

						#box.write_digital_pin(13, 1)
						# correct beep
						# record x,y pos at release (nop)
					break
				else:
					while self.mouse.getPressed()[0]:
						time.sleep(0.001)
					timestamp_release = datetime.now()
					print('Incorrect!')
					self.box.incorrect()
					time.sleep(2) # delay after incorrect attempt
			touch_event.record_timestamps(timestamp_touch, timestamp_release, timestamp_stimulus)

			# save touch event
			self.save_touch_event(touch_event.export())
			touch_event.print()
		# finish
		self.box.disconnect()
		self.window.close()
		run_end = datetime.now()
		return (run_start, run_end, self.events)

class StageOne(Window):
	def __init__(self, window_size, stimuli):
		super().__init__(window_size, stimuli)

class Task(Window):
	def __init__(self, window_size, stimuli, max_trials):
		super().__init__(window_size, stimuli, max_trials)
