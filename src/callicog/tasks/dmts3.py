from callicog.task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from callicog.task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		red_diamond = Stimulus(shape=StimulusShape.DIAMOND, size=(176.78,176.78), color=[1,-1,-1], size_touch=(250,250))
		yellow_circle = Stimulus(shape=StimulusShape.CIRCLE, size = (250,250), color=[1,1,-1], size_touch=(250,250))
		blue_star = Stimulus(shape=StimulusShape.STAR, size = (1,1), color = [-1,-1,1], size_touch=(250,250))
		stimulus_list = [red_diamond, yellow_circle, blue_star]
		delay_list = [0.5, 1, 2, 4, 8, 12]
		
		# Positions are listed as [sample_pos,distractor_pos]
		left = (-382.5, 0)
		right = (382.5, 0)
		centre = (0,0)
		position_list = [[left, centre],[left,right],[centre,left],[centre,right],[right,left],[right,centre]]
		
		self.add_parameter(Parameter.POSITION, position_list)
		self.add_parameter(Parameter.TARGET, stimulus_list)
		self.add_parameter(Parameter.DELAY, delay_list)

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

	def build_trial(self, trial_parameters={}):
		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE, label = 'encoding1')
		w1_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w1_sample.position = (0,0)
		w1.add_stimulus(w1_sample)

		# Window 2
		w2 = Window(blank=0.5) 

		# Window 3
		w3 = Window(transition=WindowTransition.RELEASE, label = 'encoding2', timeout=3, is_outcome=False)
		w3_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w3_sample.position = (0,0)
		w3.add_stimulus(w3_sample)

		# Window 4
		w4_blank = trial_parameters[Parameter.DELAY]
		w4 = Window(blank=w4_blank, label = 'maintenance')

		# Window 5
		w5 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3, label = 'retrieval')
		w5_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w5_sample.position = trial_parameters[Parameter.POSITION][0]
		w5_sample.outcome = Outcome.SUCCESS
		
		w5_distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])[0]
		w5_distractor.position = trial_parameters[Parameter.POSITION][1]
		w5_distractor.outcome = Outcome.FAIL

		w5.add_stimulus(w5_sample)
		w5.add_stimulus(w5_distractor)

		# Window 6
		w6 = Window(blank=1.0, label = 'outcome1')

		# Window 7 - placeholder for timestamping
		w7 = Window(blank=0.00000001, label = 'outcome2')
		
		# Penalty window - conditional
		pw = Window(blank=1.0)

		return [w1, w2, w3, w4, w5, w6, w7, pw]
