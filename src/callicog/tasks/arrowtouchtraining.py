from callicog.task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from callicog.task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		pass

	def generate_trials(self):
		pass

	def build_trial(self, trial_parameters={}):
		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_square = Stimulus(shape=StimulusShape.SQUARE,
					 size=(200, 200),
					 color=(-1, -1, -1),
					 position=(0, 0))
		w1.add_stimulus(w1_square)
		
		# Window 2
		w2 = Window(blank=0.5)

		# Window 3
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=2)
		target_stim = Stimulus(shape=StimulusShape.ARROW_N,
				size=(25,25), 
				color = (1, 1, 0),
				size_touch=(160,160))
		target_stim.position = (random.randint(-520, 520), random.randint(-220, 220))
		target_stim.outcome = Outcome.SUCCESS
		w3.add_stimulus(target_stim)
		
		# Window 4
		w4 = Window(blank=1)

		return [w1, w2, w3, w4]