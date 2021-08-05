from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Event(Base):
	__tablename__ = 'event'
	event_id = Column(Integer, primary_key=True)
	trial_id = Column(Integer, ForeignKey('trial.trial_id'))
	#event_timestamp = Column(DateTime, nullable=False)
	press_xcoor = Column(Integer)
	press_ycoor = Column(Integer)
	delay = Column(Float)

	trial = relationship('Trial', back_populates='events')

	def __repr__(self):
		return '<Event(event_id=%s)>' % str(self.event_id)

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
	protocol_id = Column(Integer, ForeignKey('protocol.protocol_id'))
	task_order = Column(Integer, nullable=False)
	progression = Column(String, nullable=False)
	complete = Column(Boolean, default=False)

	experiment = relationship('Experiment', back_populates='tasks')
	protocol = relationship('Protocol', back_populates='tasks')
	sessions = relationship('Session', order_by=Session.session_start, back_populates='task')

	def __repr__(self):
		return '<Task(task_id=%s>' % str(self.task_id)

class Experiment(Base):
	__tablename__ = 'experiment'
	experiment_id = Column(Integer, primary_key=True)
	animal_id = Column(Integer, ForeignKey('animal.animal_id'))
	experiment_start = Column(DateTime, nullable=False)
	experiment_end = Column(DateTime)

	animal = relationship('Animal', back_populates='experiments')
	tasks = relationship('Task', order_by=Task.task_order, back_populates='experiment')

	def __repr__(self):
		return '<Experiment(experiment_id=%s)>' % str(self.experiment_id)

class Animal(Base):
	__tablename__ = 'animal'
	animal_id = Column(Integer, primary_key=True)
	animal_code = Column(String, nullable=False)
	
	experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='animal')
	
	def __repr__(self):
		return '<Animal(animal_code=%s)>' % self.animal_code

class Protocol(Base):
	__tablename__ = 'protocol'
	protocol_id = Column(Integer, primary_key=True)
	protocol_name = Column(String, nullable=False)

	tasks = relationship('Task', back_populates='protocol') # not very useful, but kept here

	def __repr__(self):
		return '<Protocol(protocol_name=%s)>' % self.protocol_name

#Animal.experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='animal')
#Protocol.experiments = relationship('Experiment', order_by=Experiment.experiment_start, back_populates='protocol')
#Protocol.levels  = relationship('Level', order_by=Level.level_number, back_populates='protocol')
#Experiment.sessions = relationship('Session', order_by=Session.session_number, back_populates='experiment')
#Session.trials = relationship('Trial', order_by=Trial.trial_number, back_populates='session')
#Trial.events = relationship('Event', order_by=Event.event_timestamp, back_populates='trial')
