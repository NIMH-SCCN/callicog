from marmobox_schema import Experiment, TrialParameter, db
from task_builder import Outcome, Parameter


experiments = db.session.query(Experiment).filter(Experiment.animal_id == 2).all()
if len(experiments) > 0:
	for experiment in experiments:
		for task in experiment.tasks:
			task_params = task.template_protocol.protocol.parameters
			if len(task_params) > 0:
				for session in task.sessions:
					for trial in session.trials:
						decision_window = [window for window in trial.windows if window.is_outcome]
						if len(decision_window) == 1:
							window = decision_window[0]
							targets = [target for target in window.stimuli if target.stimulus_outcome == Outcome.SUCCESS]
							if len(targets) == 1:
								target = targets[0]
								for param in task_params:
									if param.parameter_name == Parameter.POSITION:
										trial_param = TrialParameter(trial=trial, protocol_parameter=param, parameter_value=str((target.stimulus_position_x, target.stimulus_position_y)))
									elif param.parameter_name == Parameter.TARGET:
										trial_param = TrialParameter(trial=trial, protocol_parameter=param, stimulus=target)
									elif param.parameter_name == Parameter.DELAY:
										if param.protocol.protocol_name == 'dmts':
											trial_param = TrialParameter(trial=trial, protocol_parameter=param, parameter_value=str(trial.windows[5].window_delay))
									elif param.parameter_name == Parameter.COLOR:
										trial_param = TrialParameter(trial=trial, protocol_parameter=param, parameter_value=str((target.stimulus_color_r, target.stimulus_color_g, target.stimulus_color_b)))
									elif param.parameter_name == Parameter.DISTRACTOR_NUMBER:
										trial_param = TrialParameter(trial=trial, protocol_parameter=param, parameter_value=str(len([distractor for distractor in window.stimuli if distractor.stimulus_outcome == Outcome.FAIL])))
									else:
										continue
									db.session.add(trial_param)

db.session.commit()
print('done')

