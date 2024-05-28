from callicog.task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from callicog.task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		position_list = [(-382.5, 0), (250, 0)]
		self.add_parameter(Parameter.POSITION, position_list)		

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

	def build_trial(self, trial_parameters={}):

	# Window 1
	# set targets
		w1 = Window(transition=WindowTransition.MAINTAIN, is_outcome=True)
		# Duration for stimuli to remain displayed after screen is touched
		w1.post_touch_delay = 1
		reward_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite1-1.jpg', color = (1,1,1), size_touch=(250,250))
		reward_stim.after_touch = [{'name': 'hide_other'}]
		penalty_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite1-2.jpg', color = (1,1,1), size_touch=(250,250))
		penalty_stim.after_touch = [{'name': 'hide_other'}]
		reward_stim.position = trial_parameters[Parameter.POSITION]
		reward_stim.outcome = Outcome.SUCCESS
		penalty_stim.position = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])[0] #index required as variable is a list
		penalty_stim.outcome = Outcome.FAIL
		w1.add_stimulus(reward_stim)
		w1.add_stimulus(penalty_stim)
		#this is necessary for 'hide'ing to work?
		for stimulus in w1.stimuli:
			stimulus.auto_draw = True

		# Window 2
		w2 = Window(blank=0.5)
	
		# Penalty window - conditional
		pw = Window(blank=1.5)

		return [w1, w2, pw]
