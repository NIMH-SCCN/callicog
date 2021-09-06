from task_builder import Outcome
from datetime import datetime
import random

def run_trial(task_name, trial_config, box, ppy_window, ppy_mouse):
	mod = __import__(f'tasks.{task_name}', fromlist=['TaskInterface'])
	task = getattr(mod, 'TaskInterface')()
	#windows, params = task.load()
	windows = task.load(random.randint(0, 50))
	
	#for i, param in enumerate(params):
	#	param.set_value(trial_config[i])

	ppy_mouse.clickReset()

	outcome = Outcome.NULL
	touch_event = None
	for window in windows:
		#window.load()
		# new window, clear screen
		#ppy_window.flip()
		#for stimulus in window.stimuli:
		#	stimulus.load(ppy_window).draw()
		# show all stimuli
		#print('--- new window!')
		#ppy_window.flip()

		#if window.transition == 'blank':
		#	time.sleep(window.timeout)
		#	print(f'blank for {window.timeout} seconds')
		#else:
			#touch_event, outcome = check_stim_click(ppy_mouse, window, datetime.now())
		window.run(ppy_window)
		if window.is_outcome:
			#import pdb; pdb.set_trace()
			targets = [stimulus for stimulus in window.stimuli if stimulus.outcome == Outcome.SUCCESS]
			while not all([target.touched for target in targets]):
				touch_event, outcome = window.get_touch_outcome(ppy_window, ppy_mouse)
				if (outcome == Outcome.FAIL) or (outcome == Outcome.NULL):
					break
		elif window.blank == 0:
			window.get_touch_outcome(ppy_window, ppy_mouse)
		window.reset(ppy_window)

	if outcome == Outcome.SUCCESS:
		print('box: correct')
		box.correct()
	elif outcome == Outcome.FAIL:
		print('box: incorrect')
		box.incorrect()

	return datetime.now(), outcome, touch_event
	# this is the last outcome from all windows