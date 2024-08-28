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
		# Window 3
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, is_outside_fail=True)
		target_stim = Stimulus(shape=StimulusShape.ARROW_N, size=(25,25), color = (1, 1, 0), size_touch=(160,160))
		target_stim.position = (0,0)
		target_stim.outcome = Outcome.SUCCESS
		w3.add_stimulus(target_stim)
		
		# Window 4
		w4 = Window(blank=1)

		return [w3, w4]
