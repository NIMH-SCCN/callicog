import sys
sys.path.append('./test')

from marmobox_schema import Animal, Protocol, Experiment, Task, Session, Trial, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from new_stim import StimShape, Progression, Outcome, run_trial
from marmobox_IO import MarmoboxIO
from numpy import random

def new_experiment(db_session, animal, tasks):
	experiment = Experiment(animal=animal, experiment_start=datetime.now())
	for order, task in enumerate(tasks):
		protocol = db_session.query(Protocol).filter(Protocol.protocol_name == task['name']).all()[0]
		task = Task(experiment=experiment, protocol=protocol, task_order=order, progression=task['progression'])
	db_session.commit()
	return experiment
	print('New experiment and tasks saved.')

def run_rolling_average_trials(box, current_task, threshold, window_size):
	shape_list = [StimShape.RECT, StimShape.CIRCLE] # list of lists in order to generate random trial_configs
	timeout_list = [2, 4, 6]

	if len(current_task.sessions) > 0:
		session = current_task.sessions[0]
	else:
		session = Session(task=current_task, session_start=datetime.now())
	while not current_task.complete:
		trial_config = [random.choice(shape_list), random.choice(timeout_list)]
		new_trial = Trial(session=session, trial_start=datetime.now())
		trial_outcome = run_trial(current_task.protocol.protocol_name, trial_config, box)
		new_trial.trial_status = trial_outcome
		new_trial.trial_end = datetime.now()

		# check if task is over
		valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
		if len(valid_trials) >= window_size:
			window = valid_trials[-window_size:]
			#print([trial.trial_status for trial in window])
			success_trials = sum([1 for trial in window if trial.trial_status == Outcome.SUCCESS])
			if (success_trials / len(window)) >= threshold:
				session.session_end = datetime.now()
				current_task.complete = True
		db_session.commit()

def continue_task_experiment(db_session, experiment, trials, box):
	# check tasks
	open_tasks = [task for task in experiment.tasks if not task.complete] # already sorted
	if len(open_tasks) == 0:
		print('\n\n\nall tasks complete, experiment done')
		return
	#for current_task in open_tasks
	current_task = open_tasks[0]
	progression = current_task.progression

	if progression == Progression.ROLLING_AVERAGE:
		run_rolling_average_trials(box, current_task, 0.8, 2)
	elif progression == Progression.SESSION_BASED:
		run_session_based_trials(current_task)
	#elif progression == Progression.TARGET_BASED:
	#	run_target_based_trials(current_task)

	# run trials
	if current_task.complete:
		print('task complete')
	else:
		print('taks incomplete')
	return

DATABASE_NAME = 'marmodb'
MARMOBOX_HOST = 'localhost'

db_engine = create_engine('postgresql:///%s' % DATABASE_NAME, echo=True)
DatabaseSession = sessionmaker()
DatabaseSession.configure(bind=db_engine)
db_session = DatabaseSession()
#import pdb; pdb.set_trace()
box = MarmoboxIO('cu.usbmodem14701')

animal = db_session.query(Animal).filter(Animal.animal_code == 'MSIMD-2123').all()[0]
tasks = [
			{
				'name': 'tasks.dmts',
				'progression': 'rolling_average'
			}
		]

# new experiment or open experiment and continue
trial_1 = [StimShape.RECT, 4]
trial_2 = [StimShape.CIRCLE, 8]
trial_3 = [StimShape.CIRCLE, 2]

trials = [trial_1, trial_2, trial_3]

if len(animal.experiments) > 0:
	experiment = animal.experiments[0]
else:
	experiment = new_experiment(db_session, animal, tasks)

continue_task_experiment(db_session, experiment, trials, box)

print('done')
db_session.close()

# case 1: fixed number of trials per session, if # combinations > trials then discard else fill with random
# case 2: all random, no pseudorandom, one long session until progression (done)
# case 3: target, session trials is # combinations, new session repeats all pseudorandom but different sequence
#         progress when X number of valid trials are reached