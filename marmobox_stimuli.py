#from protocol_base import Window, Stimulus, StageOne, Task
import sys
sys.path.append('./test')
from new_stim import StimShape, Progression, Outcome, run_trial

def process_stimulus(trial_params, box):
	task_name = trial_params['protocol_name']
	trial_config = trial_params['trial_config']
	(run_end, trial_outcome) = run_trial(task_name, trial_config, box)
	return {'trial_end': str(run_end), 'trial_outcome': trial_outcome}
