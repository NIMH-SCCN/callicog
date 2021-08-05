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

def check_stim_click(mouse, window, stim_time):
	touch_event = None
	while True:
		timed_out = wait_for_click(mouse, window.timeout)
		if timed_out:
			print('timed out')
			return touch_event, Outcome.NULL
		else:
			print('clicked')
			for stimulus in window.stimuli:
				if mouse.isPressedIn(stimulus.ppy_stim.stim_object):
					position = mouse.getPos()
					touch_event = {'xcoor': position[0], 
						'ycoor': position[1], 
						'delay': (datetime.now() - stim_time).total_seconds()}
					if window.transition == 'on_click':
						print(f'in object {stimulus.stim_id}, on click')
						return touch_event, stimulus.outcome
					elif window.transition == 'on_release':
						print(f'in object {stimulus.stim_id}, waiting to release')
						while mouse.getPressed()[0]:
							time.sleep(0.001)
						print('released')
						touch_event['delay'] = (datetime.now() - stim_time).total_seconds()
						return touch_event, stimulus.outcome
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
	touch_event = None
	for i in range(len(windows)):
		window = windows[i]
		window.load()
		# new window, clear screen
		ppy_window.flip()
		for stimulus in window.stimuli:
			stimulus.load(ppy_window).draw()
		# show all stimuli
		print('--- new window!')
		ppy_window.flip()

		if window.transition == 'blank':
			time.sleep(window.timeout)
			print(f'blank for {window.timeout} seconds')
		else:
			touch_event, outcome = check_stim_click(ppy_mouse, window, datetime.now())

	if outcome == Outcome.SUCCESS:
		print('box: correct')
		box.correct()
	elif outcome == Outcome.FAIL:
		print('box: incorrect')
		box.incorrect()

	return datetime.now(), outcome, touch_event
	# this is the last outcome from all windows