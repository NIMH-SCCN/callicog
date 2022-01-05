from marmobox_schema import Animal, Protocol, Experiment, Task, Session, Trial, Template, WindowObject, StimulusObject
from task_builder import Progression, Outcome
from datetime import datetime
from numpy import random
import socket
import select
import pickle
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
			print(json.dumps(status, indent=2)) # status report, return fail status if arduino fails

	def disconnect(self):
		self.client_socket.close()

	def send(self, message):
		if self.client_socket:
			self.client_socket.send(bytes(json.dumps(message), 'utf8'))

	def send_binary(self, message):
		if self.client_socket:
			self.client_socket.send(message)

	def receive(self, timeout=None):
		if self.client_socket:
			ready = select.select([self.client_socket], [], [], timeout)
			if ready[0]:
				response = self.client_socket.recv(self.TX_MAX_LENGTH)
				return json.loads(response.decode())
		return None

	def get_animal(self, animal_code):
		animal = self.db_session.query(Animal).filter(Animal.animal_code == animal_code).all()[0]
		return animal

	def get_template(self, template_name):
		template = self.db_session.query(Template).filter(Template.template_name == template_name).all()[0]
		return template

	def get_experiment(self, experiment_id):
		experiment = self.db_session.query(Experiment).filter(Experiment.experiment_id == experiment_id).all()[0]
		return experiment

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

	def run_trial(self, trial_windows):
		message = {
			'action': 'run_trial',
			'trial_params': {
				'trial_windows': trial_windows # serialize properly (pickle)
			}
		}
		self.send_binary(pickle.dumps(message))
		try:
			response = self.receive()
		except KeyboardInterrupt:
			print('/ninterrupted, exiting gracefully')
			return None
		if response and response['success'] == 1:
			body = response['body']
			trial_data = body['data']
			print(json.dumps(trial_data, indent=2))
			return trial_data
		return None

	def run_session_based_trials(self, current_task, task_interface):
		while not current_task.complete:
			session = Session(task=current_task, session_start=datetime.now())
			trial_indices, iter_trials = self.shuffle_trials(task_interface.trials, current_task.template_protocol.target_trials)

			valid_trials = []
			while len(valid_trials) < current_task.template_protocol.target_trials:
				try:
					next_trial = next(iter_trials)
					trial_windows = task_interface.build_trial(next_trial)
				except StopIteration:
					trial_indices, iter_trials = self.shuffle_trials(task_interface.trials)
					continue

				new_trial = Trial(session=session, trial_start=datetime.now())
				trial_data = self.run_trial(trial_windows)
				new_trial.trial_status = trial_data['trial_outcome']
				new_trial.trial_end = trial_data['trial_end']
				trial_events = trial_data['events']
				if len(trial_events) > 0:
					self.save_trial_events(trial_events, new_trial)
				if new_trial.trial_status == Outcome.NULL:
					trial_indices.append(next_trial)
				valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()

			# all trials, included null repetitions, complete
			session.session_end = datetime.now()
			# check valid trials in session

			#valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
			success_trials = sum([1 for trial in valid_trials if trial.trial_status == Outcome.SUCCESS])
			if (success_trials / len(valid_trials)) >= current_task.template_protocol.success_rate:
				session.session_status = Outcome.SUCCESS
				last_sessions = current_task.sessions[-current_task.template_protocol.target_sessions:]
				if len(last_sessions) == current_task.template_protocol.target_sessions:
					if all([se.session_status == Outcome.SUCCESS for se in last_sessions]):
						# all n_sessions are success
						current_task.complete = True
			else:
				session.session_status = Outcome.FAIL
			self.db_session.commit()

	def save_trial_events(self, windows, trial):
		for window in windows:
			trial_window = WindowObject(
				trial=trial,
				is_outcome=window['is_outcome'],
				is_outside_fail=window['is_outside_fail'],
				window_delay=window['delay'],
				window_label=window['label'],
				window_transition=window['transition'],
				window_timeout=window['timeout'],
				flip_timestamp=window['flip'])
			for stimulus in window['stimuli']:
				window_stimulus = StimulusObject(
					window=trial_window,
					stimulus_shape=stimulus['shape'],
					stimulus_size_x=stimulus['size'][0],
					stimulus_size_y=stimulus['size'][1],
					stimulus_position_x=stimulus['position'][0],
					stimulus_position_y=stimulus['position'][1],
					stimulus_outcome=stimulus['outcome'],
					stimulus_color_r=stimulus['color'][0],
					stimulus_color_g=stimulus['color'][1],
					stimulus_color_b=stimulus['color'][2],
					stimulus_image_file=stimulus['image'],
					stimulus_timeout_gain=stimulus['timeout_gain'],
					stimulus_touched=stimulus['touched'],
					stimulus_flip_timestamp=stimulus['flip'],
					stimulus_touch_timestamp=stimulus['touch'],
					stimulus_release_timestamp=stimulus['release'])
				if stimulus['touch_pos']:
					window_stimulus.stimulus_touch_x = stimulus['touch_pos'][0]
					window_stimulus.stimulus_touch_y = stimulus['touch_pos'][1]
		#self.db_session.commit()

	def run_target_based_trials(self, current_task, task_interface):
		session = Session(task=current_task, session_start=datetime.now())
		trial_indices, iter_trials = self.shuffle_trials(task_interface.trials, current_task.template_protocol.target_trials)

		while not current_task.complete:
			try:
				next_trial = next(iter_trials)
				trial_windows = task_interface.build_trial(next_trial)
			except StopIteration:
				trial_indices, iter_trials = self.shuffle_trials(task_interface.trials)
				continue

			new_trial = Trial(session=session, trial_start=datetime.now())
			trial_data = self.run_trial(trial_windows)
			if not trial_data:
				self.db_session.commit()
				raise Exception # invalid trial, abort
			new_trial.trial_status = trial_data['trial_outcome']
			new_trial.trial_end = trial_data['trial_end']
			trial_events = trial_data['events']
			if new_trial.trial_status == Outcome.NULL:
				trial_indices.append(next_trial)
			if len(trial_events) > 0:
				self.save_trial_events(trial_events, new_trial)

			# check if task is over
			valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
			#success_trials = sum([1 for trial in valid_trials if trial.trial_status == Outcome.SUCCESS])
			if len(valid_trials) == current_task.template_protocol.target_trials:
				session.session_end = datetime.now()
				current_task.complete = True
			self.db_session.commit()

	def run_rolling_average_trials(self, current_task, task_interface):
		session = Session(task=current_task, session_start=datetime.now())
		trial_indices, iter_trials = self.shuffle_trials(task_interface.trials)

		while not current_task.complete:
			try:
				next_trial = next(iter_trials)
				trial_windows = task_interface.build_trial(next_trial)
			except StopIteration:
				trial_indices, iter_trials = self.shuffle_trials(task_interface.trials)
				continue

			new_trial = Trial(session=session, trial_start=datetime.now())
			trial_data = self.run_trial(trial_windows)
			new_trial.trial_status = trial_data['trial_outcome']
			new_trial.trial_end = trial_data['trial_end']
			trial_events = trial_data['events']
			if new_trial.trial_status == Outcome.NULL:
				trial_indices.append(next_trial)
			if len(trial_events) > 0:
				self.save_trial_events(trial_events, new_trial)

			# check if task is over
			valid_trials = session.trials.filter(Trial.trial_status != Outcome.NULL).all()
			if len(valid_trials) >= current_task.template_protocol.rolling_window_size:
				window = valid_trials[-current_task.template_protocol.rolling_window_size:]
				success_trials = sum([1 for trial in window if trial.trial_status == Outcome.SUCCESS])
				if (success_trials / len(window)) >= current_task.template_protocol.success_rate:
					session.session_end = datetime.now()
					current_task.complete = True
			self.db_session.commit()

	def shuffle_trials(self, trials, target=0):
		trial_indices = list(range(len(trials)))
		random.shuffle(trial_indices)
		iter_trials = iter(trial_indices)
		if target > 0 and len(trials) >= target:
			trial_subset = trial_indices[:target]
			return trial_subset, iter(trial_subset)
		return trial_indices, iter_trials

	def new_experiment(self, animal, template):
		experiment = Experiment(animal=animal, template=template, experiment_start=datetime.now())
		for protocol in template.protocols:
			task = Task(experiment=experiment, 
						template_protocol=protocol)
		self.db_session.commit()
		return experiment

	def continue_task_experiment(self, experiment):
		exit_code = 0
		# check tasks
		open_tasks = [task for task in experiment.tasks if not task.complete] # already sorted
		if len(open_tasks) == 0:
			print('\n\n\nall tasks complete, experiment done')
			return
		for current_task in open_tasks:
			progression = current_task.template_protocol.progression
			print(f'new task: {current_task.template_protocol.protocol.protocol_name}, progression: {progression}')

			mod = __import__(f'tasks.{current_task.template_protocol.protocol.protocol_name}', fromlist=['TaskInterface'])
			task_interface = getattr(mod, 'TaskInterface')()
			task_interface.generate_trials()

			if progression == Progression.ROLLING_AVERAGE:
				self.run_rolling_average_trials(current_task, task_interface)
			elif progression == Progression.SESSION_BASED:
				self.run_session_based_trials(current_task, task_interface)
			elif progression == Progression.TARGET_BASED:
				try:
					self.run_target_based_trials(current_task, task_interface)
				except:
					self.db_session.commit()
					print('\n\n\ncaught kill signal, experiment interrupted')
					return

			if current_task.complete:
				print('task complete')
			else:
				print('tasks incomplete')

		if all([task.complete for task in open_tasks]):
			experiment.experiment_end = datetime.now()
			self.db_session.commit()
			print('\n\n\nall tasks complete, experiment done')
