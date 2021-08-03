from task_builder import Outcome
from datetime import datetime
import time

def wait_for_click(mouse, timeout=0):
	print('waiting')
	start = time.time()
	while not mouse.getPressed()[0]:
		time.sleep(0.001)
		if timeout > 0 and (time.time() - start) > timeout:
			return True
	return False

def check_stim_click(mouse, window):
	while True:
		timed_out = wait_for_click(mouse, window.timeout)
		if timed_out:
			print('timed out')
			return Outcome.NULL
		else:
			print('clicked')
			for stimulus in window.stimuli:
				if mouse.isPressedIn(stimulus.ppy_stim.stim_object):
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

def run_trial(task_name, trial_config, box, ppy_window, ppy_mouse):
	ppy_window.flip()
	mod = __import__(f'tasks.{task_name}', fromlist=['TaskStructure'])
	task = getattr(mod, 'TaskStructure')
	windows, params = task.load()

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