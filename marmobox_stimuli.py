import sys
from trial_interface import run_trial

def process_stimulus(trial_params, box, ppy_window, ppy_mouse):
	trial_windows = trial_params['trial_windows']
	(run_end, trial_outcome, events, box_status) = run_trial(trial_windows, box, ppy_window, ppy_mouse)
	return {'trial_end': str(run_end), 'trial_outcome': trial_outcome, 'events': events, 'box_status': box_status}
