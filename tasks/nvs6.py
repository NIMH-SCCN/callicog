from sqlalchemy import true
from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		ndistractors_list = [1,2,3,4]
		positions_list = [(-466, 233), (-233, 233), (0, 233), (233, 233), (466, 233), (-466, 0), (-233, 0), (0, 0), (233, 0), (466, 0),(-466, -233), (-233, -233), (0, -233), (233, -233), (466, -233)]
		
		blue_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(0, 255, 255),
					size_touch= (160,160))
		blue_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7,0.7),
					color=(0, 255, 255),
					size_touch= (160,160))
		blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(140,140),
					color=(0, 255, 255),
					size_touch= (160,160))
		yellow_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(140,140),
					color=(220,220,0),
					size_touch= (160,160))
		blue_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120,120),
					color=(0, 255, 255),
					size_touch= (160,160))
		yellow_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(220,220,0),
					size_touch= (160,160))
		blue_arrow_e = Stimulus(shape=StimulusShape.ARROW_E,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		blue_arrow_w = Stimulus(shape=StimulusShape.ARROW_W,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		yellow_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7,0.7),
					color=(220,220,0),
					size_touch= (160,160))
		yellow_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120,120),
					color=(220,220,0),
					size_touch= (160,160))
		yellow_arrow_ne = Stimulus(shape=StimulusShape.ARROW_NE,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		blue_arrow_ne = Stimulus(shape=StimulusShape.ARROW_NE,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		yellow_arrow_nw = Stimulus(shape=StimulusShape.ARROW_NW,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		blue_arrow_nw = Stimulus(shape=StimulusShape.ARROW_NW,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		yellow_arrow_se = Stimulus(shape=StimulusShape.ARROW_SE,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		yellow_arrow_w = Stimulus(shape=StimulusShape.ARROW_W,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		yellow_arrow_e = Stimulus(shape=StimulusShape.ARROW_E,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		yellow_arrow_sw = Stimulus(shape=StimulusShape.ARROW_SW,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		blue_arrow_sw = Stimulus(shape=StimulusShape.ARROW_SW,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		blue_arrow_s = Stimulus(shape=StimulusShape.ARROW_S,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		yellow_arrow_s = Stimulus(shape=StimulusShape.ARROW_S,
					size=(25,25), 
					color=(220,220,0),
					size_touch=(160,160))
		blue_arrow_n = Stimulus(shape=StimulusShape.ARROW_N,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		blue_arrow_se = Stimulus(shape=StimulusShape.ARROW_SE,
					size=(25,25), 
					color=(0, 255, 255),
					size_touch=(160,160))
		blue_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(0, 255, 255),
					size_touch= (160,160))
		blue_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.7,0.7),
					color=(0, 255, 255),
					size_touch= (160,160))
		blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(140,140),
					color=(0, 255, 255),
					size_touch= (160,160))
		blue_diamond = Stimulus(shape=StimulusShape.DIAMOND,
					size=(120,120),
					color=(0, 255, 255),
					size_touch= (160,160))

		blueshapes = [blue_triangle, blue_star, blue_circle, blue_diamond, blue_triangle, blue_star, blue_circle, blue_diamond, blue_triangle, blue_star, blue_circle, blue_diamond]
		bluearrowsyellowshapes = [blue_arrow_e, blue_arrow_n, blue_arrow_nw, blue_arrow_se, blue_arrow_sw, blue_arrow_s, blue_arrow_sw, blue_arrow_w, blue_arrow_ne, yellow_circle, yellow_diamond, yellow_star, yellow_triangle, yellow_star, yellow_circle, yellow_star, yellow_triangle, yellow_star]
		bluearrowsyellowarrows = [blue_arrow_e, blue_arrow_n, blue_arrow_nw, blue_arrow_se, blue_arrow_sw, blue_arrow_sw, blue_arrow_w, yellow_arrow_ne, yellow_arrow_nw, yellow_arrow_s, yellow_arrow_se, yellow_arrow_sw, yellow_arrow_e, yellow_arrow_w]
		yellowarrows=[yellow_arrow_ne, yellow_arrow_nw, yellow_arrow_s, yellow_arrow_se, yellow_arrow_sw, yellow_arrow_e, yellow_arrow_w]
		self.add_parameter(Parameter.BLUESHAPES, blueshapes, pseudorandom= True)
		self.add_parameter(Parameter.BLUEARROWSYELLOWSHAPES, bluearrowsyellowshapes, pseudorandom= True)
		self.add_parameter(Parameter.BLUEARROWSYELLOWARROWS, bluearrowsyellowarrows, pseudorandom= True)
		self.add_parameter(Parameter.YELLOWARROWS, yellowarrows, pseudorandom= True)
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
				color = (220,220,0),
				size_touch=(160,160))
		target_stim.position = trial_parameters[Parameter.POSITION]
		target_stim.outcome = Outcome.SUCCESS
		w3.add_stimulus(target_stim)
		
		# set distractors
		distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=trial_parameters[Parameter.DISTRACTOR_NUMBER])
		if len(distractor_positions) == 1:
				for position in distractor_positions:
					distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.BLUEARROWSYELLOWARROWS]['values'], size=1)
					distractor_stim = copy.copy(distractor[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim)

		if len(distractor_positions) == 2:
				for position in distractor_positions:
					distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.BLUEARROWSYELLOWARROWS]['values'], size=2)
					distractor_stim = copy.copy(distractor[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim)

		if len(distractor_positions) == 3:
				for position in distractor_positions:
					distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.BLUEARROWSYELLOWSHAPES]['values'], size=3)
					distractor_stim = copy.copy(distractor[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim)
		elif len(distractor_positions) == 4:
				for position in distractor_positions:
					distractor2 = self.randomize_from(self.pseudorandom_parameters[Parameter.BLUESHAPES]['values'], size=4)
					distractor_stim = copy.copy(distractor2[0])
					distractor_stim.position = position
					distractor_stim.outcome = Outcome.FAIL
					w3.add_stimulus(distractor_stim) 

		# Window 8
		w4 = Window(blank=2)

		#penalty window
		pw = Window(blank=3)
		

		return [w1, w2, w3, w4, pw]