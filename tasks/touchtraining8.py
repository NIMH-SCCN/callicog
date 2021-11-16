from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome
from itertools import combinations
import numpy as np
import random
import copy

class TaskInterface:
	def __init__(self):
		self.pseudorandom_parameters = {}
		self.trials = []

		self.initialize_pseudorandom_parameters()

	def __add_pseudorandom_parameter_list(self, parameter_name, parameter_values):
		self.pseudorandom_parameters[parameter_name] = parameter_values

	def __pseudorandomize_parameters(self):
		list_indices = []
		for key in self.pseudorandom_parameters:
			list_indices.append(range(len(self.pseudorandom_parameters[key])))

		trials = []
		trial_configs = np.array(np.meshgrid(*list_indices)).T.reshape(-1, len(self.pseudorandom_parameters))

		for config in trial_configs:
			trial_dic = {}
			for i, key in enumerate(self.pseudorandom_parameters):
				value = self.pseudorandom_parameters[key][config[i]]
				trial_dic[key] = value
			trials.append(trial_dic)
		return trials

	def __randomize_from(self, sample, exclude=[], size=0):
		exclude_idx = [sample.index(item) for item in exclude]
		new_sample_idx = [i for i in range(len(sample)) if i not in exclude_idx]
		if size > 0:
			result = random.sample(new_sample_idx, k=size)
		else:
			result = random.sample(new_sample_idx, k=random.randint(1, len(new_sample_idx)))
		return [sample[i] for i in result]

	def __randomize(self):
		pass

	def initialize_pseudorandom_parameters(self):
		# define list of pseudorandom parameters


		ndistractors_list = [1,2,3]
		positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]
		

		self.__add_pseudorandom_parameter_list('ndistractor', ndistractors_list)
		self.__add_pseudorandom_parameter_list('positions', positions_list)

	def generate_trials(self):
		trials = self.__pseudorandomize_parameters()
		
		
		

		blue_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(0, 0.7, 1),
					size_touch= (120,120))
		blue_star = Stimulus(shape=StimulusShape.STAR,
					size=(0.6,0.6),
					color=(0, 0.7, 1),
					size_touch= (120,120))
		blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(120,120),
					color=(0, 0.7, 1),
					size_touch= (120,120))

		distractor_list = [blue_triangle, blue_star, blue_circle]
		self.__add_pseudorandom_parameter_list('distractors', distractor_list)

		self.trials = trials
		
	def build_trial(self, trial_index):
		# get pseudorandom parameters for the current trial
		trial_parameters = self.trials[trial_index]

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
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=2)
		#targets = trial_parameters['targets']
		target_stim = Stimulus(shape=StimulusShape.ARROW_N,
				size=(25,25), 
				color = (1, 1, 0),
				size_touch=(160,160))
		target_stim.position = (random.randint(-520, 520), random.randint(-220, 220))
		target_stim.outcome = Outcome.SUCCESS
		#target_stim.after_touch = [{'name': 'hide'}]
		#target_stim.timeout_gain = 2
		#target_stim.auto_draw = True
		w3.add_stimulus(target_stim)
		
		# Window 8
		w4 = Window(blank=1)

		return [w1, w2, w3, w4]