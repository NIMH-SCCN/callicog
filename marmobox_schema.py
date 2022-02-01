from database import Base
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from task_builder import Outcome

class WindowObject(Base):
	__tablename__ = 'window_object'
	window_object_id = Column(Integer, primary_key=True)
	trial_id = Column(Integer, ForeignKey('trial.trial_id'))
	is_outcome = Column(Boolean, default=False)
	is_outside_fail = Column(Boolean, default=False)
	outside_fail_position_x = Column(Integer, nullable=True)
	outside_fail_position_y = Column(Integer, nullable=True)
	window_delay = Column(Float, nullable=False)
	window_label = Column(String, nullable=True)
	window_timeout = Column(Float, nullable=False)
	window_transition = Column(String, nullable=True)
	flip_timestamp = Column(DateTime, nullable=False)

	trial = relationship('Trial', back_populates='windows')
	stimuli = relationship('StimulusObject', back_populates='window', cascade="all, delete")

	def __repr__(self):
		return '<WindowObject(window_object_id=%s)>' % str(self.window_object_id)

class StimulusObject(Base):
	__tablename__ = 'stimulus_object'
	stimulus_object_id = Column(Integer, primary_key=True)
	window_object_id = Column(Integer, ForeignKey('window_object.window_object_id'))
	stimulus_shape = Column(String)
	stimulus_size_x = Column(Integer)
	stimulus_size_y = Column(Integer)
	stimulus_position_x = Column(Integer)
	stimulus_position_y = Column(Integer)
	stimulus_outcome = Column(String)
	stimulus_color_r = Column(Float)
	stimulus_color_g = Column(Float)
	stimulus_color_b = Column(Float)
	stimulus_image_file = Column(String)
	stimulus_timeout_gain = Column(Float)
	stimulus_touched = Column(Boolean, default=False)
	stimulus_touch_x = Column(Integer)
	stimulus_touch_y = Column(Integer)
	stimulus_flip_timestamp = Column(DateTime)
	stimulus_touch_timestamp = Column(DateTime)
	stimulus_release_timestamp = Column(DateTime)

	window = relationship('WindowObject', back_populates='stimuli')
	trial_parameter = relationship('TrialParameter', back_populates='stimulus')

	def __repr__(self):
		return '<StimulusObject(stimulus_object_id=%s)>' % str(self.stimulus_object_id)

	def getStimulusSummary(self):
		return f'{self.stimulus_shape}, color=({self.stimulus_color_r},{self.stimulus_color_g},{self.stimulus_color_b})'

class Trial(Base):
	__tablename__ = 'trial'
	trial_id = Column(Integer, primary_key=True)
	session_id = Column(Integer, ForeignKey('session.session_id'))
	trial_start = Column(DateTime, nullable=True)
	trial_end = Column(DateTime, nullable=True)
	trial_status = Column(String, default='new')

	session = relationship('Session', back_populates='trials')
	windows = relationship('WindowObject', back_populates='trial', cascade='all, delete')
	parameters = relationship('TrialParameter', back_populates='trial', cascade='all, delete')

	def __repr__(self):
		return '<Trial(trial_id=%s)>' % self.trial_id

	def getTargets(self):
		return len([stimulus for window in self.windows for stimulus in window.stimuli if window.is_outcome and stimulus.stimulus_outcome == Outcome.SUCCESS])

	def getDistractors(self):
		return len([stimulus for window in self.windows for stimulus in window.stimuli if window.is_outcome and stimulus.stimulus_outcome == Outcome.FAIL])


class TrialParameter(Base):
	__tablename__ = 'trial_parameter'
	trial_parameter_id = Column(Integer, primary_key=True)
	protocol_parameter_id = Column(Integer, ForeignKey('protocol_parameter.protocol_parameter_id'))
	parameter_value = Column(String, nullable=True)
	stimulus_object_id = Column(Integer, ForeignKey('stimulus_object.stimulus_object_id'), nullable=True)
	trial_id = Column(Integer, ForeignKey('trial.trial_id'), nullable=False)

	trial = relationship('Trial', back_populates='parameters')
	stimulus = relationship('StimulusObject', back_populates='trial_parameter')
	protocol_parameter = relationship('ProtocolParameter', back_populates='trial_parameters')

	def __repr__(self):
		return '<TrialParameter(trial_parameter_id=%s)>' % self.trial_parameter_id

	def getParameterValue(self):
		if self.parameter_value:
			return self.parameter_value
		elif self.stimulus:
			return self.stimulus.getStimulusSummary()
		else:
			return ''

class Session(Base):
	__tablename__ = 'session'
	session_id = Column(Integer, primary_key=True)
	task_id = Column(Integer, ForeignKey('task.task_id'))
	session_start = Column(DateTime, nullable=True)
	session_end = Column(DateTime, nullable=True)
	session_status = Column(String, default='new')

	task = relationship('Task', back_populates='sessions')
	trials = relationship('Trial', order_by=Trial.trial_start, back_populates='session', cascade="all, delete")

	def __repr__(self):
		return '<Session(session_id=%s)>' % self.session_id

	def getDuration(self):
		if self.session_start and self.session_end:
			duration_secs = (self.session_end - self.session_start).total_seconds()
			return f'{duration_secs // 60} min {duration_secs % 60} sec'
		else:
			return ''

	def getTrials(self):
		return len([trial for trial in self.trials if trial.trial_status != 'new'])

	def getHits(self):
		return len([trial for trial in self.trials if trial.trial_status == Outcome.SUCCESS])

	def getFails(self):
		return len([trial for trial in self.trials if trial.trial_status == Outcome.FAIL])

	def getNulls(self):
		return len([trial for trial in self.trials if trial.trial_status == Outcome.NULL])

	def getSuccessRate(self):
		return self.getHits() / self.getTrials() * 100

class Task(Base):
	__tablename__ = 'task'
	task_id = Column(Integer, primary_key=True)
	experiment_id = Column(Integer, ForeignKey('experiment.experiment_id'))
	template_protocol_id = Column(Integer, ForeignKey('template_protocol.template_protocol_id'))
	complete = Column(Boolean, default=False)

	experiment = relationship('Experiment', back_populates='tasks')
	template_protocol = relationship('TemplateProtocol', back_populates='tasks')
	sessions = relationship('Session', order_by=Session.session_start, back_populates='task', cascade="all, delete")

	def __repr__(self):
		return '<Task(task_id=%s)>' % str(self.task_id)

class Experiment(Base):
	__tablename__ = 'experiment'
	experiment_id = Column(Integer, primary_key=True)
	animal_id = Column(Integer, ForeignKey('animal.animal_id'))
	template_id = Column(Integer, ForeignKey('template.template_id'))
	experiment_start = Column(DateTime, nullable=False)
	experiment_end = Column(DateTime)

	animal = relationship('Animal', back_populates='experiments')
	template = relationship('Template', back_populates='experiments')
	tasks = relationship('Task', back_populates='experiment', cascade="all, delete")

	def __repr__(self):
		return '<Experiment(experiment_id=%s)>' % str(self.experiment_id)

	def getCompletion(self):
		return sum([True for task in self.tasks if task.complete]) / len(self.tasks) * 100

class Animal(Base):
	__tablename__ = 'animal'
	animal_id = Column(Integer, primary_key=True)
	animal_code = Column(String, nullable=False)
	
	experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='animal')
	
	def __repr__(self):
		return '<Animal(animal_code=%s)>' % self.animal_code

class TemplateProtocol(Base):
	__tablename__ = 'template_protocol'
	template_protocol_id = Column(Integer, primary_key=True)
	template_id = Column(Integer, ForeignKey('template.template_id'))
	protocol_id = Column(Integer, ForeignKey('protocol.protocol_id'))
	task_order = Column(Integer, nullable=False)
	progression = Column(String, nullable=False)
	target_trials = Column(Integer, nullable=True)
	target_sessions = Column(Integer, nullable=True)
	success_rate = Column(Float, nullable=True)
	rolling_window_size = Column(Integer, nullable=True)

	protocol = relationship('Protocol', back_populates='templates')
	template = relationship('Template', back_populates='protocols')
	tasks = relationship('Task', back_populates='template_protocol') # not used but kept

	def __repr__(self):
		return '<TemplateProtocol(template_protocol_id=%s>' % self.template_protocol_id

class Protocol(Base):
	__tablename__ = 'protocol'
	protocol_id = Column(Integer, primary_key=True)
	protocol_name = Column(String, nullable=False)

	templates = relationship('TemplateProtocol', back_populates='protocol') # not very useful, but kept here
	parameters = relationship('ProtocolParameter', back_populates='protocol')

	def __repr__(self):
		return '<Protocol(protocol_name=%s)>' % self.protocol_name

class ProtocolParameter(Base):
	__tablename__ = 'protocol_parameter'
	protocol_parameter_id = Column(Integer, primary_key=True)
	parameter_name = Column(String, nullable=False)
	protocol_id = Column(Integer, ForeignKey('protocol.protocol_id'))

	protocol = relationship('Protocol', back_populates='parameters')
	trial_parameters = relationship('TrialParameter', back_populates='protocol_parameter')

	def __repr__(self):
		return '<ProtocolParameter(protocol_parameter_id=%s)>' % self.protocol_parameter_id

class Template(Base):
	__tablename__ = 'template'
	template_id = Column(Integer, primary_key=True)
	template_name = Column(String, nullable=False)

	protocols = relationship('TemplateProtocol', back_populates='template', cascade="all, delete")
	experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='template', cascade="all, delete")

	def __repr__(self):
		return '<Template(template_name=%s)>' % self.template_name
