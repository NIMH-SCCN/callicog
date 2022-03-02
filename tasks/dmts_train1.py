from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		red_diamond = Stimulus(shape=StimulusShape.DIAMOND, size=(176.78,176.78), color=(255,0,0), size_touch=(250,250))
		yellow_circle = Stimulus(shape=StimulusShape.CIRCLE, size = (250,250), color=(255,255,0), size_touch=(250,250)) #check size
		stimulus_list = [red_diamond, yellow_circle]
		position_list = [(-382.5, 0), (382.5, 0)]
		
		self.add_parameter(Parameter.POSITION, position_list)
		self.add_parameter(Parameter.TARGET, stimulus_list)		

	def generate_trials(self):
		self.trials = self.pseudorandomize_parameters()

	def build_trial(self, trial_parameters={}):
		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(0, 0, 0), position=(0, 0))
		w1.add_stimulus(w1_square)

		# Window 2
		w2 = Window(blank=0.5)

		# Window 3
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3)
		sample = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite4-1.jpg', color = (1,1,1), size_touch=(250,250))
		sample.position = trial_parameters[Parameter.POSITION]
		sample.outcome = Outcome.SUCCESS
		distractor = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite4-2.jpg', color = (1,1,1), size_touch=(250,250))
		distractor.position = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])[0] #index required as variable is a list
		distractor.outcome = Outcome.FAIL
		w3.add_stimulus(sample)
		w3.add_stimulus(distractor)

		# Window 3
		w3 = Window(blank=0.5)
		
		# Penalty window - conditional
		pw = Window(blank=1.5)

		return [w1, w2, w3, pw]