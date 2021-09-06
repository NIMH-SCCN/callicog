import sys
sys.path.append('./test')

from marmobox_schema import Animal, Protocol, Experiment, Task, Session, Trial, Event
from new_stim import StimShape, Progression, Outcome
from datetime import datetime
from numpy import random
import socket
import select
import json

class Marmobox:
	RX_TIMEOUT = 10
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

		status = self.receive(self.RX_TIMEOUT)
		if status:
			print(status) # status report

	def disconnect(self):
		self.client_socket.close()

	def send(self, message):
		if self.client_socket:
			self.client_socket.send(bytes(json.dumps(message), 'utf8'))

	def receive(self, timeout=None):
		if self.client_socket:
			ready = select.select([self.client_socket], [], [], timeout)
			if ready[0]:
				response = self.client_socket.recv(self.TX_MAX_LENGTH)
				return json.loads(response.decode())
		return None

	def wait_for_animal(self):
		message = {
			'action': 'wait_for_animal'
		}
		self.send(message)
		response = self.receive()
		if response and response['success'] == 1:
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
		if response and response['success'] == 1:
			body = response['body']
			trial_data = body['data']
			print(trial_data)
			return trial_data
		return None

	def run_session_based_trials(self, current_task, n_trials, success_rate, n_sessions):
		shape_list = [StimShape.RECT, StimShape.CIRCLE] # list of lists in order to generate random trial_configs
		timeout_list = [2, 4, 6]

		trial_1 = [StimShape.RECT, 4]
		trial_2 = [StimShape.CIRCLE, 8]
		trial_3 = [StimShape.CIRCLE, 2]
		trials = [trial_1, trial_2, trial_3]

		if len(trials) < n_trials:
			new_trials = [[random.choice(shape_list), int(random.choice(timeout_list))] for i in range(n_trials - len(trials))]
			trials.extend(new_trials)
		elif len(trials) > n_trials:
			trials = trials[:n_trials]

		while not current_task.complete:
			# always a new session, previous could be not success so basically a start over
			session = Session(task=current_task, session_start=datetime.now())
			for trial_config in trials:
				new_trial = Trial(session=session, trial_start=datetime.now())
				trial_data = self.run_trial(current_task.protocol.protocol_name, trial_config)
				new_trial.trial_status = trial_data['trial_outcome']
				new_trial.trial_end = trial_data['trial_end']
				touch_event = trial_data['trial_touch']
				if touch_event:
					event = Event(trial=new_trial, 
						press_xcoor=touch_event['xcoor'],
						press_ycoor=touch_event['ycoor'],
						delay=touch_event['delay'])
			session.session_end = datetime.now()
			# check valid trials in session
			valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
			success_trials = sum([1 for trial in valid_trials if trial.trial_status == Outcome.SUCCESS])
			if (success_trials / len(valid_trials)) >= success_rate:
				session.session_status = Outcome.SUCCESS
				if all([se.session_status == Outcome.SUCCESS for se in current_task.sessions[-n_sessions:]]): # wrong
					# all n_sessions are success
					current_task.complete = True
			else:
				session.session_status = Outcome.FAIL
			self.db_session.commit()

	def run_target_based_trials(self, current_task, target): # pass full list of trials if resume
		shape_list = [StimShape.RECT, StimShape.CIRCLE] # list of lists in order to generate random trial_configs
		timeout_list = [2, 4, 6]

		if len(current_task.sessions) > 0:
			session = current_task.sessions[0] # I think always a new session until task complete
		else:
			session =  Session(task=current_task, session_start=datetime.now())

		while not current_task.complete:
			trial_config = [random.choice(shape_list), int(random.choice(timeout_list))]
			new_trial = Trial(session=session, trial_start=datetime.now())
			trial_data = self.run_trial(current_task.protocol.protocol_name, trial_config)
			new_trial.trial_status = trial_data['trial_outcome']
			new_trial.trial_end = trial_data['trial_end']
			touch_event = trial_data['trial_touch']
			if touch_event:
				event = Event(trial=new_trial, 
					press_xcoor=touch_event['xcoor'],
					press_ycoor=touch_event['ycoor'],
					delay=touch_event['delay'])

			# check if task is over
			valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
			success_trials = sum([1 for trial in valid_trials if trial.trial_status == Outcome.SUCCESS])
			if success_trials >= target:
				session.session_end = datetime.now()
				current_task.complete = True
			self.db_session.commit()

	def run_rolling_average_trials(self, current_task, threshold, window_size): # pass entire list of trials on resume
		shape_list = [StimShape.RECT, StimShape.CIRCLE] # list of lists in order to generate random trial_configs
		timeout_list = [2, 4, 6]

		if len(current_task.sessions) > 0:
			session = current_task.sessions[0] # I think always a new session until task complete
		else:
			session = Session(task=current_task, session_start=datetime.now())

		while not current_task.complete:
			trial_config = [random.choice(shape_list), int(random.choice(timeout_list))]
			new_trial = Trial(session=session, trial_start=datetime.now())
			trial_data = self.run_trial(current_task.protocol.protocol_name, trial_config)
			new_trial.trial_status = trial_data['trial_outcome']
			new_trial.trial_end = trial_data['trial_end']
			touch_event = trial_data['trial_touch']
			if touch_event:
				event = Event(trial=new_trial,
					press_xcoor=touch_event['xcoor'],
					press_ycoor=touch_event['ycoor'],
					delay=touch_event['delay'])

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
			self.run_session_based_trials(current_task, 3, 0.8, 2)
		elif progression == Progression.TARGET_BASED:
			self.run_target_based_trials(current_task, 10)

		# run trials
		if current_task.complete:
			print('task complete')
		else:
			print('taks incomplete')
		return
