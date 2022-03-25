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
		ndistractors_list = [3, 4, 5, 6]
		positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]
		blue_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(120, 216, 255),
					size_touch= (160,160))
		blue_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7,0.7),
					color=(120, 216, 255),
					size_touch= (160,160))
		blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(140,140),
					color=(120, 216, 255),
					size_touch= (160,160))
		yellow_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(140,140),
					color=(255, 255, 100),
					size_touch= (160,160))
		blue_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120,120),
					color=(120, 216, 255),
					size_touch= (160,160))
		yellow_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(255, 255, 100),
					size_touch= (160,160))
		blue_arrow_e = Stimulus(shape=StimulusShape.ARROW_E,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		blue_arrow_w = Stimulus(shape=StimulusShape.ARROW_W,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		yellow_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7,0.7),
					color=(255, 255, 100),
					size_touch= (160,160))
		yellow_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120,120),
					color=(255, 255, 100),
					size_touch= (160,160))
		yellow_arrow_ne = Stimulus(shape=StimulusShape.ARROW_NE,
					size=(25,25), 
					color = (255, 255, 100),
					size_touch=(160,160))
		blue_arrow_ne = Stimulus(shape=StimulusShape.ARROW_NE,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		yellow_arrow_nw = Stimulus(shape=StimulusShape.ARROW_NW,
					size=(25,25), 
					color = (255, 255, 100),
					size_touch=(160,160))
		blue_arrow_nw = Stimulus(shape=StimulusShape.ARROW_NW,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		yellow_arrow_se = Stimulus(shape=StimulusShape.ARROW_SE,
					size=(25,25), 
					color = (255, 255, 100),
					size_touch=(160,160))
		yellow_arrow_sw = Stimulus(shape=StimulusShape.ARROW_SW,
					size=(25,25), 
					color = (255, 255, 100),
					size_touch=(160,160))
		blue_arrow_sw = Stimulus(shape=StimulusShape.ARROW_SW,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		blue_arrow_s = Stimulus(shape=StimulusShape.ARROW_S,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		yellow_arrow_s = Stimulus(shape=StimulusShape.ARROW_S,
					size=(25,25), 
					color = (255, 255, 100),
					size_touch=(160,160))
		blue_arrow_n = Stimulus(shape=StimulusShape.ARROW_N,
					size=(25,25), 
					color = (120, 216, 255),
					size_touch=(160,160))
		
		level1_list = [blue_triangle, blue_star, blue_circle, blue_diamond, blue_triangle, blue_star, blue_circle, blue_diamond]
		#all blue
		level2_list = [yellow_triangle,  blue_arrow_w, yellow_star, yellow_diamond, blue_arrow_sw, blue_arrow_ne, yellow_circle, blue_arrow_nw]
		#half blue half yellow
		level3_list = [yellow_arrow_ne, yellow_arrow_nw, yellow_arrow_se, yellow_arrow_sw, blue_arrow_s, blue_arrow_n, blue_arrow_n, blue_arrow_s]
		#half  blue half yellow
		level4_list = [yellow_arrow_s, yellow_arrow_s, yellow_arrow_ne, yellow_arrow_nw, yellow_arrow_se, yellow_arrow_sw, yellow_arrow_s, yellow_arrow_s,]
		#all yellow

		self.add_parameter(Parameter.DISTRACTOR, level1_list, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR2,level2_list, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR3,level3_list, pseudorandom=False)
		self.add_parameter(Parameter.DISTRACTOR4,level4_list, pseudorandom=False)
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
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3)
		target_stim = Stimulus(shape=StimulusShape.ARROW_N,
				size=(25, 25),
				color=(1, 1, 0),
				size_touch=(160, 160))
		target_stim.position = trial_parameters[Parameter.POSITION]
		target_stim.outcome = Outcome.SUCCESS
		w3.add_stimulus(target_stim)

		# set distractors
		distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER])
		if len(distractor_positions) == 3:
				for position in distractor_positions:
					distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR4]['values'], size=3)
					distractor_stim = copy.copy(distractor[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim)
		elif len(distractor_positions) == 4:
				for position in distractor_positions:
					distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR3]['values'], size=4)
					distractor_stim = copy.copy(distractor[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim)
		elif len(distractor_positions) == 5:
				for position in distractor_positions:
					distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR2]['values'], size=5)
					distractor_stim = copy.copy(distractor[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim)
		else:
				for position in distractor_positions:
					distractor2 = self.randomize_from(self.pseudorandom_parameters[Parameter.DISTRACTOR]['values'], size=6)
					distractor_stim = copy.copy(distractor2[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim) 

		# Window 8
		w4 = Window(blank=2)

		#penalty window
		pw = Window(blank=3)
		

		return [w1, w2, w3, w4, pw]