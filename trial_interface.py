from task_builder import Outcome
from datetime import datetime
import random

def run_trial(task_name, trial_config, box, ppy_window, ppy_mouse):
	mod = __import__(f'tasks.{task_name}', fromlist=['TaskInterface'])
	task = getattr(mod, 'TaskInterface')()

	windows = task.load(random.randint(0, 9))
	ppy_mouse.clickReset()

	outcome = Outcome.NULL
	touch_event = None
	for window in windows:
		flip_time = window.run(ppy_window)
		if window.is_outcome:
			targets = [stimulus for stimulus in window.stimuli if stimulus.outcome == Outcome.SUCCESS]
			while not all([target.touched for target in targets]):
				touch_event, outcome = window.get_touch_outcome(flip_time, ppy_mouse)
				if (outcome == Outcome.FAIL) or (outcome == Outcome.NULL):
					break
		elif window.blank == 0:
			window.get_touch_outcome(flip_time, ppy_mouse)
		window.reset()

	if outcome == Outcome.SUCCESS:
		print('box: correct')
		box.correct()
	elif outcome == Outcome.FAIL:
		print('box: incorrect')
		box.incorrect()

	return datetime.now(), outcome, touch_event
	# this is the last outcome from all windows