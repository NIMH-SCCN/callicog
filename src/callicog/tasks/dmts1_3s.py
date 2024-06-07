from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		red_diamond = Stimulus(shape=StimulusShape.DIAMOND, size=(176.78,176.78), color=(1,-1,-1), size_touch=(250,250))
		yellow_circle = Stimulus(shape=StimulusShape.CIRCLE, size = (250,250), color=(1,1,-1), size_touch=(250,250))
		blue_star = Stimulus(shape=StimulusShape.STAR, size = (1,1), color = (-1,-1,1), size_touch=(250,250))
		stimulus_list = [red_diamond, yellow_circle, blue_star]
		delay_list = [0.5, 1, 2, 4]
		
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
		w1 = Window(transition=WindowTransition.TOUCH)
		w1_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w1_sample.position = (0,0)
		w1.add_stimulus(w1_sample)
  
  		# Window 2
		w2 = Window(transition=WindowTransition.TOUCH, label = 'encoding1')
		w2_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w2_sample.position = (0,0)
		w2.add_stimulus(w2_sample)

		# Window 3
		w3 = Window(blank=0.5)

		# Window 4
		w4 = Window(transition=WindowTransition.RELEASE, label = 'encoding2', timeout=2, is_outcome=False)
		w4_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w4_sample.position = (0,0)
		w4.add_stimulus(w4_sample)

		# Window 5
		w5_blank = trial_parameters[Parameter.DELAY]
		w5 = Window(blank=w5_blank, label = 'maintenance')

		# Window 6
		w6 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3, label = 'retrieval')
		w6_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w6_sample.position = trial_parameters[Parameter.POSITION][0]
		w6_sample.outcome = Outcome.SUCCESS
		
		w6_distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])[0]
		w6_distractor.position = trial_parameters[Parameter.POSITION][1]
		w6_distractor.outcome = Outcome.FAIL

		w6.add_stimulus(w6_sample)
		w6.add_stimulus(w6_distractor)

		# Window 7
		w7 = Window(blank=1.0, label = 'outcome1')
	
 		# Window 8 - placeholder for eeg timing
		w8 = Window(blank=0.00000001, label = 'outcome2')	
		
  		# Penalty window - conditional
		pw = Window(blank=1.0)

		return [w1, w2, w3, w4, w5, w6, w7, w8, pw]