from min_task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome
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

		#ntargets_list = [1]
		ndistractors_list = [2,3,4,5,6,7]
		#delays_list = [1, 2, 4]
		positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]
		
		
		# add them to task
		#self.__add_pseudorandom_parameter_list('distractor', distractor_list)
		#self.__add_pseudorandom_parameter_list('targets', ntargets_list)
		self.__add_pseudorandom_parameter_list('ndistractor', ndistractors_list)
		#self.__add_pseudorandom_parameter_list('delay', delays_list)
		self.__add_pseudorandom_parameter_list('positions', positions_list)
#IF I DONT WANT AN ELEMENT TO BE PSEUDORANDOMISED, ADD IT AFTER TRIALS = SELF.__PSEUDORANDOMISE PARAMETERS
	def generate_trials(self):
		trials = self.__pseudorandomize_parameters()
		
		
		
		blue_arrow2 = Stimulus(shape=StimulusShape.ARROW2,
					size=(20,20),
					color=(0, 0.7, 1),
					size_touch= (120,120))
		yellow_triangle = Stimulus(shape=StimulusShape.TRIANGLE,
					size=(15,15),
					color=(1, 1, 0),
					size_touch= (120,120))
		blue_arrow3 = Stimulus(shape=StimulusShape.ARROW3,
					size=(20,20),
					color=(0, 0.7, 1),
					size_touch= (120,120))

		distractor_list = [blue_arrow2, yellow_triangle, blue_arrow3]
		self.__add_pseudorandom_parameter_list('distractors', distractor_list)
		# additional pseudorandom parameters
		# e.g. Supertask: positions depending on 'targets'
		#positions_list = [(-465, 155), (-155, 155), (155, 155), (465, 155),(-465, -155), (-155, -155), (155, -155), (465, -155)]
		#self.__add_pseudorandom_parameter_list('positions', positions_list)
		
		#new_trials = []
		#for trial in trials:
		#	distractors = trial['distractors']
		#	C = list(combinations(range(len(positions_list)), distractors))
		#	for positions in C:
		#		new_trial = copy.copy(trial)
		#		new_trial['positions'] = [positions_list[position_index] for position_index in positions]
		#		new_trials.append(new_trial)

		self.trials = trials
		
	def build_trial(self, trial_index):
		# get pseudorandom parameters for the current trial
		trial_parameters = self.trials[trial_index]

		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_square = Stimulus(shape=StimulusShape.SQUARE,
					 size=(100, 100),
					 color=(-1, -1, -1),
					 position=(0, 0))
		w1.add_stimulus(w1_square)
		
		# Window 2
		w2 = Window(blank=0.5)

		# Window 3
		# set targets
		w3 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=5)
		#targets = trial_parameters['targets']
		target_stim = Stimulus(shape=StimulusShape.ARROW,
				size=(20,20), 
				color = (1, 1, 0),
				size_touch=(120,120))
		target_stim.position = trial_parameters['positions']
		target_stim.outcome = Outcome.SUCCESS
		#target_stim.after_touch = [{'name': 'hide'}]
		#target_stim.timeout_gain = 2
		#target_stim.auto_draw = True
		w3.add_stimulus(target_stim)
		
		# set distractors
		#distractors = self.__randomize_from(self.pseudorandom_parameters['distractors'])
		#distractor_positions = self.__randomize_from(self.pseudorandom_parameters['positions'], exclude=trial_parameters['positions'])
		distractor_positions = self.__randomize_from(self.pseudorandom_parameters['positions'], exclude=[trial_parameters['positions']], size=trial_parameters['ndistractor'])
		for position in distractor_positions: #i in range(trial_parameters['ndistractor']):
			distractor = self.__randomize_from(self.pseudorandom_parameters['distractors'], size=1)
			distractor_stim = copy.copy(distractor[0])
			#position=self.__randomize_from(self.pseudorandom_parameters['positions'], exclude=[trial_parameters['positions']], size=1)
			distractor_stim.position = position
			distractor_stim.outcome = Outcome.FAIL
			#distractor_stim.auto_draw = True
			w3.add_stimulus(distractor_stim)

		# Window 8
		w4 = Window(blank=2)

		return [w1, w2, w3, w4]