import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from callicog.task_builder import Outcome


db = SQLAlchemy()

Base = db.Model
Column = db.Column
Integer = db.Integer
event = db.event
Float = db.Float
Boolean = db.Boolean
DateTime = db.DateTime
String = db.String
ForeignKey = db.ForeignKey

relationship = db.relationship


@db.event.listens_for(sqlalchemy.orm.Mapper, 'init')
def auto_add(target, args, kwargs):
    """ Listen for the creation of new ORM instances (e.g. Trial, Animal etc).
    Immediately add the new object to the database session.
    """
    db.session.add(target)


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
            duration = (self.session_end - self.session_start).total_seconds()
            mins = duration // 60
            secs = duration % 60
            return f'{mins:.0f} min {secs:.0f} sec'
        else:
            return ''

    def getTrials(self):
        return self.getHits() + self.getFails()

    def getHits(self):
        return len([trial for trial in self.trials if trial.trial_status == Outcome.SUCCESS])

    def getFails(self):
        return len([trial for trial in self.trials if trial.trial_status == Outcome.FAIL])

    def getNulls(self):
        # e.g. Timeouts
        return len([trial for trial in self.trials if trial.trial_status == Outcome.NULL])

    def getSuccessRate(self):
        n_trials = self.getTrials()
        n_hits = self.getHits()

        if n_trials == 0:
            return 0
        else:
            success_rate = n_hits / n_trials * 100
            return f"{success_rate:.1f}"


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
    # not used but kept:
    tasks = relationship('Task', back_populates='template_protocol')

    def __repr__(self):
        return '<TemplateProtocol(template_protocol_id=%s>' % self.template_protocol_id


class Protocol(Base):
    __tablename__ = 'protocol'
    protocol_id = Column(Integer, primary_key=True)
    protocol_name = Column(String, nullable=False)

    # not very useful, but kept here:
    templates = relationship('TemplateProtocol', back_populates='protocol')
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


def search(
    trial_id=None,
    session_id=None,
    experiment_id=None,
    template_name=None,
    task_name=None,
    animal_code=None,
    trial_start=None,
    trial_end=None,
    timeout=None,
    ntargets=None,
    ndistractors=None,
    outcome=None,
    target_shape=None,
    target_color=None,
    trial_delay=None,
):
    params = {
        'param_trial_id': (None if trial_id == '' else trial_id),
        'param_session_id': (None if session_id == '' else session_id),
        'param_experiment_id': (None if experiment_id == '' else experiment_id),
        'param_template_name': (None if template_name == '' else template_name),
        'param_task_name': (None if task_name == '' else task_name),
        'param_animal_code': (None if animal_code == '' else animal_code),
        'param_trial_start': (None if trial_start == '' else trial_start),
        'param_trial_end': (None if trial_end == '' else trial_end),
        'param_timeout': (None if timeout == '' else timeout),
        'param_ntargets': (None if ntargets == '' else ntargets),
        'param_ndistractors': (None if ndistractors == '' else ndistractors),
        'param_outcome': (None if outcome == '' else outcome),
        'param_target_shape': (None if target_shape == '' else target_shape),
        'param_target_color': (None if target_color == '' else target_color),
        'param_trial_delay': (None if trial_delay == '' else trial_delay)
    }
    results = db.session.execute(db.text(SEARCH_SQL), params)
    return results


SEARCH_SQL = """
with ttable as
(
    select
        an.animal_code as animal
        ,te.template_name as template
        ,pr.protocol_name as task
        ,ex.experiment_id as experiment
        ,se.session_id as session
        ,tr.trial_id as trial
        ,tr.trial_start as start
        ,case when (tr.trial_end is not null) then extract(epoch from (tr.trial_end - tr.trial_start)) else null end as duration
        ,tr.trial_status as outcome
        ,wo.flip_timestamp as flip
        ,wo.outside_fail_position_x as out_x
        ,wo.outside_fail_position_y as out_y
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_shape from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as target
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_color_r from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as color_r
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_color_g from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as color_g
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_color_b from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as color_b
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_position_x from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as pos_x
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_position_y from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as pos_y
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_size_x from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as size_x
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_size_y from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as size_y
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_touch_x from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as touch_x
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_touch_y from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as touch_y
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select extract(epoch from (so.stimulus_touch_timestamp - so.stimulus_flip_timestamp)) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as touch_response
        ,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select extract(epoch from (so.stimulus_release_timestamp - so.stimulus_touch_timestamp)) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as release_response
        ,(select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') as ntargets
        ,(select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'fail') as ndistractors
        ,(select trp.parameter_value from trial_parameter trp inner join protocol_parameter pp on pp.protocol_parameter_id = trp.protocol_parameter_id where pp.parameter_name = 'delay' and trp.trial_id = tr.trial_id) as delay
        ,wo.window_timeout as timeout
    from trial tr
    inner join window_object wo on wo.trial_id = tr.trial_id
    inner join session se on se.session_id = tr.session_id
    inner join task ta on ta.task_id = se.task_id
    inner join template_protocol tp on tp.template_protocol_id = ta.template_protocol_id
    inner join protocol pr on pr.protocol_id = tp.protocol_id
    inner join template te on te.template_id = tp.template_id
    inner join experiment ex on ex.experiment_id = ta.experiment_id
    inner join animal an on an.animal_id = ex.animal_id
    where wo.is_outcome = True
    and (:param_timeout is null or wo.window_timeout = :param_timeout)
    and (:param_outcome is null or tr.trial_status = :param_outcome)
    and (:param_trial_id is null or tr.trial_id = :param_trial_id)
    and (:param_session_id is null or se.session_id = :param_session_id)
    and (:param_task_name is null or pr.protocol_name = :param_task_name)
    and (:param_experiment_id is null or ex.experiment_id = :param_experiment_id)
    and (:param_template_name is null or te.template_name = :param_template_name)
    and (:param_animal_code is null or an.animal_code = :param_animal_code)
    and ((:param_trial_start is null and :param_trial_end is null) or (tr.trial_start >= :param_trial_start and tr.trial_start <= :param_trial_end))
)
select *
from ttable tt
where (:param_ntargets is null or tt.ntargets = :param_ntargets)
and (:param_ndistractors is null or tt.ndistractors = :param_ndistractors)
and (:param_target_shape is null or tt.target = :param_target_shape)
and (:param_target_color is null or concat('(', tt.color_r, ',', tt.color_g, ',', tt.color_b, ')') = :param_target_color)
and (:param_trial_delay is null or tt.delay = :param_trial_delay)
;
"""
