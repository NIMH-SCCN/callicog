from database import Base
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, String, ForeignKey, Table
from sqlalchemy.orm import relationship

#class Event(Base):
#	__tablename__ = 'event'
#	event_id = Column(Integer, primary_key=True)
#	trial_id = Column(Integer, ForeignKey('trial.trial_id'))
	#event_timestamp = Column(DateTime, nullable=False)
#	press_xcoor = Column(Integer)
#	press_ycoor = Column(Integer)
#	delay = Column(Float)

#	trial = relationship('Trial', back_populates='events')

#	def __repr__(self):
#		return '<Event(event_id=%s)>' % str(self.event_id)

class WindowObject(Base):
	__tablename__ = 'window_object'
	window_object_id = Column(Integer, primary_key=True)
	is_outcome = Column(Boolean, default=False)
	window_delay = Column(Float, nullable=False)
	window_transition_type = Column(String)
	window_timeout = Column(Float, nullable=False)

	event = relationship('Event', back_populates='window_object', uselist=False)

	def __repr__(self):
		return '<WindowObject(window_object_id=%s)>' % str(self.window_object_id)

class StimulusObject(Base):
	__tablename__ = 'stimulus_object'
	stimulus_object_id = Column(Integer, primary_key=True)
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

	event = relationship('Event', back_populates='stimulus_object', uselist=False)

	def __repr__(self):
		return '<StimulusObject(stimulus_object_id=%s)>' % str(self.stimulus_object_id)

class Event(Base):
	__tablename__ = 'event'
	event_id = Column(Integer, primary_key=True)
	trial_id = Column(Integer, ForeignKey('trial.trial_id'))
	flip_timestamp = Column(DateTime, nullable=True)
	touch_timestamp = Column(DateTime, nullable=True)
	release_timestamp = Column(DateTime, nullable=True)
	input_xcoor = Column(Integer, nullable=True)
	input_ycoor = Column(Integer, nullable=True)
	stimulus_object_id = Column(Integer, ForeignKey('stimulus_object.stimulus_object_id'))
	window_object_id = Column(Integer, ForeignKey('window_object.window_object_id'))

	trial = relationship('Trial', back_populates='events')
	stimulus_object = relationship('StimulusObject', back_populates='event')
	window_object = relationship('WindowObject', back_populates='event')

class Trial(Base):
	__tablename__ = 'trial'
	trial_id = Column(Integer, primary_key=True)
	session_id = Column(Integer, ForeignKey('session.session_id'))
	trial_start = Column(DateTime, nullable=True)
	trial_end = Column(DateTime, nullable=True)
	trial_status = Column(String, default='new')

	session = relationship('Session', back_populates='trials')
	events = relationship('Event', back_populates='trial')

	def __repr__(self):
		return '<Trial(trial_id=%s)>' % self.trial_id

class Session(Base):
	__tablename__ = 'session'
	session_id = Column(Integer, primary_key=True)
	task_id = Column(Integer, ForeignKey('task.task_id'))
	session_start = Column(DateTime, nullable=True)
	session_end = Column(DateTime, nullable=True)
	session_status = Column(String, default='new')

	task = relationship('Task', back_populates='sessions')
	trials = relationship('Trial', order_by=Trial.trial_start, back_populates='session', lazy='dynamic')

	def __repr__(self):
		return '<Session(session_id=%s)>' % self.session_id

class Task(Base):
	__tablename__ = 'task'
	task_id = Column(Integer, primary_key=True)
	experiment_id = Column(Integer, ForeignKey('experiment.experiment_id'))
	template_protocol_id = Column(Integer, ForeignKey('template_protocol.template_protocol_id'))
	complete = Column(Boolean, default=False)

	experiment = relationship('Experiment', back_populates='tasks')
	template_protocol = relationship('TemplateProtocol', back_populates='tasks')
	sessions = relationship('Session', order_by=Session.session_start, back_populates='task')

	def __repr__(self):
		return '<Task(task_id=%s>' % str(self.task_id)

class Experiment(Base):
	__tablename__ = 'experiment'
	experiment_id = Column(Integer, primary_key=True)
	animal_id = Column(Integer, ForeignKey('animal.animal_id'))
	template_id = Column(Integer, ForeignKey('template.template_id'))
	experiment_start = Column(DateTime, nullable=False)
	experiment_end = Column(DateTime)

	animal = relationship('Animal', back_populates='experiments')
	template = relationship('Template', back_populates='experiments')
	tasks = relationship('Task', back_populates='experiment')

	def __repr__(self):
		return '<Experiment(experiment_id=%s)>' % str(self.experiment_id)

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

	def __repr__(self):
		return '<Protocol(protocol_name=%s)>' % self.protocol_name

class Template(Base):
	__tablename__ = 'template'
	template_id = Column(Integer, primary_key=True)
	template_name = Column(String, nullable=False)

	protocols = relationship('TemplateProtocol', back_populates='template')
	experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='template')

	def __repr__(self):
		return '<Template(template_name=%s)>' % self.template_name

#TemplateProtocol = Table('template_protocol', Base.metadata,
#	Column('template_protocol_id', Integer, primary_key=True),
#	Column('template_id', Integer, ForeignKey('template.template_id')),
#	Column('protocol_id', Integer, ForeignKey('protocol.protocol_id')),
#	Column('task_order', Integer, nullable=False))

#Animal.experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='animal')
#Protocol.experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='protocol')
#Protocol.levels  = relationship('Level', order_by=Level.level_number, back_populates='protocol')
#Experiment.sessions = relationship('Session', order_by=Session.session_number, back_populates='experiment')
#Session.trials = relationship('Trial', order_by=Trial.trial_number, back_populates='session')
#Trial.events = relationship('Event', order_by=Event.event_timestamp, back_populates='trial')

# t = Template(template_name='t1')
# a = TemplateProtocol(task_order=1)
# a.protocol = db.query(Protocol).all()[0]
# t.protocols.append(a)