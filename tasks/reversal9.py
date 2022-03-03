from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		position_list = [(-382.5, 0), (382.5, 0)]
		self.add_parameter(Parameter.POSITION, position_list)		

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

	def build_trial(self, trial_parameters={}):
		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(0, 0, 0), position=(0, 0))
		w1.add_stimulus(w1_square)

		# Window 2
		# set targets
		w2 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=2)
		reward_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite12-2.jpg', color = (1,1,1), size_touch=(250,250))
		penalty_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite12-1.jpg', color = (1,1,1), size_touch=(250,250))
		reward_stim.position = trial_parameters[Parameter.POSITION]
		reward_stim.outcome = Outcome.SUCCESS
		penalty_stim.position = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])[0] #index required as variable is a list
		penalty_stim.outcome = Outcome.FAIL
		w2.add_stimulus(reward_stim)
		w2.add_stimulus(penalty_stim)

		# Window 3
		w3 = Window(blank=0.5)
		
		# Penalty window - conditional
		pw = Window(blank=1.5)

		return [w1, w2, w3, pw]