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
		yellow_circle = Stimulus(shape=StimulusShape.CIRCLE, size = (250,250), color=(1,1,-1), size_touch=(250,250)) #check size
		stimulus_list = [red_diamond, yellow_circle]
		position_list = [(-382.5, 0), (382.5, 0)]
		
		self.add_parameter(Parameter.POSITION, position_list)
		self.add_parameter(Parameter.TARGET, stimulus_list)		

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

	def build_trial(self, trial_parameters={}):
		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w1_sample.position = (0,0)
		w1.add_stimulus(w1_sample)

		# Window 2
		w2 = Window(blank=0.5)

		# Window 3
		w3 = Window(transition=WindowTransition.MAINTAIN, is_outcome=True, timeout=3)
		w3.post_touch_delay = 1
		w3_sample = copy.copy(trial_parameters[Parameter.TARGET])
		w3_sample.after_touch = [{'name': 'hide_other'}]
		w3_sample.position = trial_parameters[Parameter.POSITION]
		w3_sample.outcome = Outcome.SUCCESS
		
		w3_distractor = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])[0]
		w3_distractor.position = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])[0]
		w3_distractor.outcome = Outcome.FAIL
		w3_distractor.after_touch = [{'name': 'hide_other'}]

		w3.add_stimulus(w3_sample)
		w3.add_stimulus(w3_distractor)

		#this is necessary for 'hide'ing to work?
		for stimulus in w3.stimuli:
			stimulus.auto_draw = True

		# Window 4
		w4 = Window(blank=0.5)
		
		# Penalty window - conditional
		pw = Window(blank=1.5)

		return [w1, w2, w3, w4, pw]
