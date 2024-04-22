import random
import numpy as np

class TaskStructure:
	def __init__(self):
		self.pseudorandom_parameters = {}
		self.trials = []

	def add_parameter(self, parameter_name, parameter_values, pseudorandom=True):
		self.pseudorandom_parameters[parameter_name] = {'values': parameter_values, 'pseudorandom': pseudorandom}

	def pseudorandomize_parameters(self):
		valid_parameters = [key for key in self.pseudorandom_parameters if self.pseudorandom_parameters[key]['pseudorandom']]
		if len(valid_parameters) == 0:
			return []
		list_indices = []
		for key in self.pseudorandom_parameters:
			if self.pseudorandom_parameters[key]['pseudorandom']:
				list_indices.append(range(len(self.pseudorandom_parameters[key]['values'])))

		trials = []
		trial_configs = np.array(np.meshgrid(*list_indices)).T.reshape(-1, len(valid_parameters))

		for config in trial_configs:
			trial_dic = {}
			for i, key in enumerate(valid_parameters):
				value = self.pseudorandom_parameters[key]['values'][config[i]]
				trial_dic[key] = value
			trials.append(trial_dic)
		return trials

	def randomize_from(self, sample, exclude=[], size=0):
		exclude_idx = [sample.index(item) for item in exclude]
		new_sample_idx = [i for i in range(len(sample)) if i not in exclude_idx]
		if size > 0:
			result = random.sample(new_sample_idx, k=size)
		else:
			result = random.sample(new_sample_idx, k=random.randint(1, len(new_sample_idx)))
		return [sample[i] for i in result]

	def get_trial_config(self, trial_index):
		if len(self.trials) > 0:
			return self.trials[trial_index]
		return []

	def get_task_parameters(self):
		return self.pseudorandom_parameters
