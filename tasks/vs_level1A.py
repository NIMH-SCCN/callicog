from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		ndistractors_list = [1]
		positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]

		blue_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(0, 0.7, 1),
					size_touch= (160,160))
		blue_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7,0.7),
					color=(0, 0.7, 1),
					size_touch= (160,160))
		blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(140,140),
					color=(0, 0.7, 1),
					size_touch= (160,160))
		blue_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120,120),
					color=(0, 0.7, 1),
					size_touch= (160,160))
		distractor_list = [blue_triangle, blue_star, blue_circle, blue_diamond]

		self.add_parameter(Parameter.DISTRACTOR, distractor_list, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR_NUMBER, ndistractors_list)
		self.add_parameter(Parameter.POSITION, positions_list)

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

	def build_trial(self, trial_parameters={}):
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_square = Stimulus(shape=StimulusShape.SQUARE,
					 size=(200, 200),
					 color=(-1, -1, -1),
					 position=(0, 0))
		w1.add_stimulus(w1_square)
		
		# Window 2
		w2 = Window(blank=0.5)

		# Window 3
		# set targets
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=5)
		target_stim = Stimulus(shape=StimulusShape.ARROW_N,
				size=(25,25), 
				color = (1, 1, 0),
				size_touch=(160,160))
		target_stim.position = trial_parameters[Parameter.POSITION]
		target_stim.outcome = Outcome.SUCCESS
		w3.add_stimulus(target_stim)
		
		# set distractors
		distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER])
		for position in distractor_positions:
			distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR]['values'], size=1)
			distractor_stim = copy.copy(distractor[0])
			distractor_stim.position = position
			distractor_stim.outcome = Outcome.FAIL
			w3.add_stimulus(distractor_stim)

		# Window 8
		w4 = Window(blank=2)

		pw = Window(blank=2)   

		return [w1, w2, w3, w4, pw]