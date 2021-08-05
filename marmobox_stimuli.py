import sys
from trial_interface import run_trial

def process_stimulus(trial_params, box, ppy_window, ppy_mouse):
	task_name = trial_params['protocol_name']
	trial_config = trial_params['trial_config']
	(run_end, trial_outcome, trial_touch) = run_trial(task_name, trial_config, box, ppy_window, ppy_mouse)
	return {'trial_end': str(run_end), 'trial_outcome': trial_outcome, 'trial_touch': trial_touch}
