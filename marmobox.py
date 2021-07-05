import sys
sys.path.append('./test')

from marmobox_schema import Animal, Protocol, Experiment, Task, Session, Trial, Event
from new_stim import StimShape, Progression, Outcome
from datetime import datetime
from numpy import random
import socket
import json

class Marmobox:
	TX_MAX_LENGTH = 4096
	DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

	def __init__(self, host, port, db_session):
		self.host = host
		self.port = port
		self.client_socket = None
		self.db_session = db_session

	def connect(self):
		self.client_socket = socket.socket()
		self.client_socket.settimeout(None)
		self.client_socket.connect((self.host, self.port))

	def disconnect(self):
		self.client_socket.close()

	def send(self, message):
		if self.client_socket:
			self.client_socket.send(bytes(json.dumps(message), 'utf8'))

	def receive(self):
		if self.client_socket:
			response = self.client_socket.recv(self.TX_MAX_LENGTH)
			return json.loads(response.decode())
		return None

	def wait_for_animal(self):
		message = {
			'action': 'wait_for_animal'
		}
		self.send(message)
		response = self.receive()
		if response['success'] == 1:
			body = response['body']
			animal_code = body['data']
			animal = self.db_session.query(Animal).filter(Animal.animal_code == animal_code).all()[0]
			return animal
		return None

	def run_trial(self, protocol_name, trial_config):
		message = {
			'action': 'run_trial',
			'trial_params': {
				'protocol_name': protocol_name,
				'trial_config': trial_config
			}
		}
		#import pdb; pdb.set_trace()
		self.send(message)
		response = self.receive()
		if response['success'] == 1:
			body = response['body']
			trial_data = body['data']
			return trial_data
		return None

	#def run_session_based_trials(self, current_task, n_trials, success_rate, n_sessions):
	#	trial_1 = [StimShape.RECT, 4]
	#	trial_2 = [StimShape.CIRCLE, 8]
	#	trial_3 = [StimShape.CIRCLE, 2]

	#	trials = [trial_1, trial_2, trial_3]

		
	#	while not current_task.complete:
	#		session = Session(task=current_task, session_start=datetime.now())
	#		if len(trials) < n_trials:




	def run_rolling_average_trials(self, current_task, threshold, window_size):
		shape_list = [StimShape.RECT, StimShape.CIRCLE] # list of lists in order to generate random trial_configs
		timeout_list = [2, 4, 6]

		if len(current_task.sessions) > 0:
			session = current_task.sessions[0]
		else:
			session = Session(task=current_task, session_start=datetime.now())
		while not current_task.complete:
			trial_config = [random.choice(shape_list), int(random.choice(timeout_list))]
			new_trial = Trial(session=session, trial_start=datetime.now())
			trial_data = self.run_trial(current_task.protocol.protocol_name, trial_config)
			new_trial.trial_status = trial_data['trial_outcome']
			new_trial.trial_end = trial_data['trial_end']

			# check if task is over
			valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
			if len(valid_trials) >= window_size:
				window = valid_trials[-window_size:]
				#print([trial.trial_status for trial in window])
				success_trials = sum([1 for trial in window if trial.trial_status == Outcome.SUCCESS])
				if (success_trials / len(window)) >= threshold:
					session.session_end = datetime.now()
					current_task.complete = True
			self.db_session.commit()

	def new_experiment(self, animal, tasks):
		experiment = Experiment(animal=animal, experiment_start=datetime.now())
		for order, task in enumerate(tasks):
			protocol = self.db_session.query(Protocol).filter(Protocol.protocol_name == task['name']).all()[0]
			task = Task(experiment=experiment, protocol=protocol, task_order=order, progression=task['progression'])
		self.db_session.commit()
		return experiment
		print('New experiment and tasks saved.')

	def continue_task_experiment(self, experiment):
		# check tasks
		open_tasks = [task for task in experiment.tasks if not task.complete] # already sorted
		if len(open_tasks) == 0:
			print('\n\n\nall tasks complete, experiment done')
			return
		#for current_task in open_tasks
		current_task = open_tasks[0]
		progression = current_task.progression

		if progression == Progression.ROLLING_AVERAGE:
			self.run_rolling_average_trials(current_task, 0.8, 2)
		elif progression == Progression.SESSION_BASED:
			self.run_session_based_trials(current_task)
		#elif progression == Progression.TARGET_BASED:
		#	run_target_based_trials(current_task)

		# run trials
		if current_task.complete:
			print('task complete')
		else:
			print('taks incomplete')
		return
