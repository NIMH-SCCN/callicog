from numpy import size
from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy


class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		ndistractors_list = [1, 2, 3,4]
		ndistractors_list2 = [2,3]
		positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]
		yellow_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15, 15),
					color=(1, 1, 0),
					size_touch=(160, 160))

		yellow_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7, 0.7),
					color=(1, 1, 0),
					size_touch=(160, 160))
		yellow_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120, 120),
					color=(1, 1, 0),
					size_touch=(160, 160))
					
		distractor_list = [yellow_triangle, yellow_star, yellow_diamond]
		
		blue_arrow_e = Stimulus(shape=StimulusShape.ARROW_E,
					size=(25, 25),
					color=(0, 0.7, 1),
					size_touch=(160, 160))
		blue_arrow_w = Stimulus(shape=StimulusShape.ARROW_W,
					size=(25, 25),
					color=(0, 0.7, 1),
					size_touch=(160, 160))
		distractor_list2 = [blue_arrow_e, blue_arrow_w]

		self.add_parameter(Parameter.DISTRACTOR, distractor_list, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR2,distractor_list2, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR_NUMBER, ndistractors_list)
		self.add_parameter(Parameter.DISTRACTOR_NUMBER2, ndistractors_list2)
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
				size=(25, 25),
				color=(1, 1, 0),
				size_touch=(160, 160))
		target_stim.position = trial_parameters[Parameter.POSITION]
		target_stim.outcome = Outcome.SUCCESS
		w3.add_stimulus(target_stim)

		# set distractors
		
		tasklist = ["1A", "1B", "2A", "2B"]
		task_randomiser = random.Random(tasklist)
		if task_randomiser == "1A":
			distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER])
			for position in distractor_positions:
				distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR]['values'], size=1)
				distractor_stim = copy.copy(distractor[0])
				distractor_stim.position = position
				distractor_stim.outcome = Outcome.FAIL
				w3.add_stimulus(distractor_stim)
		
		elif task_randomiser == "1B":
			distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER])
			for position in distractor_positions:
				distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR]['values'], size=1)
				distractor_stim = copy.copy(distractor[0])
				distractor_stim.position = position
				distractor_stim.outcome = Outcome.FAIL
				w3.add_stimulus(distractor_stim)

		elif task_randomiser == "2A":
			distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER2])
			for position in distractor_positions:
					distractor2 = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR2]['values'], size=1)
					distractor_stim = copy.copy(distractor2[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim) 
		
		else:
			distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER2])
			for position in distractor_positions:
					distractor2 = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR2]['values'], size=1)
					distractor_stim = copy.copy(distractor2[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim) 	

		# Window 8
		w4 = Window(blank=2)

		return [w1, w2, w3, w4]