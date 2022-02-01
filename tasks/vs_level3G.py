from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		ndistractors_list = [6, 7]
		positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]

		yellow_arrow_ne = Stimulus(shape=StimulusShape.ARROW_NE,
					size=(25,25), 
					color = (1, 1, 0),
					size_touch=(160,160))
		yellow_arrow_nw = Stimulus(shape=StimulusShape.ARROW_NW,
					size=(25,25), 
					color = (1, 1, 0),
					size_touch=(160,160))
		yellow_arrow_se = Stimulus(shape=StimulusShape.ARROW_SE,
					size=(25,25), 
					color = (1, 1, 0),
					size_touch=(160,160))
		yellow_arrow_sw = Stimulus(shape=StimulusShape.ARROW_SW,
					size=(25,25), 
					color = (1, 1, 0),
					size_touch=(160,160))
		blue_arrow_s = Stimulus(shape=StimulusShape.ARROW_S,
					size=(25,25), 
					color = (0, 0.7, 1),
					size_touch=(160,160))
		blue_arrow_n = Stimulus(shape=StimulusShape.ARROW_N,
					size=(25,25), 
					color = (0, 0.7, 1),
					size_touch=(160,160))
		distractor_list = [yellow_arrow_ne, yellow_arrow_nw, yellow_arrow_se, yellow_arrow_sw, blue_arrow_s, blue_arrow_n]

		self.add_parameter(Parameter.DISTRACTOR, distractor_list, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR_NUMBER, ndistractors_list)
		self.add_parameter(Parameter.POSITION, positions_list)

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

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

		return [w1, w2, w3, w4]