from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome
import random
import numpy as np
from itertools import combinations
import copy

class TaskInterface:
	def __init__(self):
		red_square = Stimulus(shape=StimulusShape.SQUARE,
					size=(100, 100),
					color=(1, 0, 0))
		blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
					size=(100, 100),
					color=(0, 0, 1))

		self.stim_list = [red_square, blue_circle]
		self.position_list = [(-200, 100), (200, 100), (-200, -100), (200, -100)]
		self.ntarget_list = [1, 2, 3]
		self.delay_list = [1, 2, 4]

	def get_trial(self, trial_index):
		

		trial_configs = np.array(np.meshgrid(range(len(self.stim_list)), 
											 range(len(self.ntarget_list)), 
											 range(len(self.delay_list))
											 )
								).T.reshape(-1, 3) # 3 dimensions (3 lists)

		trials = []
		for config in trial_configs:
			ntargets_idx = config[1] # second dimension
			ntargets = self.ntarget_list[ntargets_idx]
			C = combinations(range(len(self.position_list)), ntargets)
			for positions in list(C):
				trial = np.concatenate((config, positions))
				trials.append(trial)
		idx = trials[trial_index]
		
		# order (stim_list, ntarget, delay, target1_pos, ..., target_ntarget_pos)
		trial_config = [self.stim_list[idx[0]], self.ntarget_list[idx[1]], self.delay_list[idx[2]]]
		for i in range(trial_config[1]):
			trial_config.append(self.position_list[idx[3 + i]])
		return trial_config, idx
		
	def load(self, trial_index):
		# trial_config
		trial_config, idx = self.get_trial(trial_index)
		print(trial_config)
		# Window 1
		w1 = Window(transition=WindowTransition.RELEASE)
		w1_square = Stimulus(shape=StimulusShape.SQUARE,
					 size=(100, 100),
					 color=(-1, -1, -1),
					 position=(0, 0))
		#w1.stimuli.append(w1_square)
		w1.add_stimulus(w1_square)
		
		# Window 2
		w2 = Window(blank=0.5)
		
		# Window 3
		w3 = Window(transition=WindowTransition.RELEASE)
		w3_stim = copy.copy(trial_config[0])
		w3_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
		#w3.stimuli.append(w3_stim)
		w3.add_stimulus(w3_stim)

		# Window 4
		w4 = Window(blank=0.5)

		# Window 5
		w5 = Window(transition=WindowTransition.RELEASE)
		w5_stim = copy.copy(trial_config[0])
		w5_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
		#w5.stimuli.append(w5_stim)
		w5.add_stimulus(w5_stim)

		# Window 6
		w6_blank = trial_config[2]
		w6 = Window(blank=w6_blank)

		# Window 7
		# set targets
		w7 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=5)
		ntargets = trial_config[1]
		positions = list(range(len(self.position_list)))
		for i in range(ntargets):
			target_stim = copy.copy(trial_config[0])
			target_stim.position = trial_config[-(i + 1)]
			target_stim.outcome = Outcome.SUCCESS
			target_stim.after_touch = [{'name': 'hide'}]
			target_stim.timeout_gain = 2
			target_stim.auto_draw = True
			positions.remove(idx[-(i + 1)])
			w7.add_stimulus(target_stim)
			#w7.stimuli.append(target_stim)
		
		# set distractors
		ndistractors = random.randint(1, len(self.position_list) - ntargets)
		distractors = list(range(len(self.stim_list)))
		distractors.remove(idx[0])
		for i in range(ndistractors):
			distractor_stim = copy.copy(self.stim_list[random.sample(distractors, k=1)[0]])
			distractor_idx = random.sample(positions, k=1)[0]
			distractor_stim.position = self.position_list[distractor_idx]
			print('distractor position:')
			print(distractor_stim.position)
			distractor_stim.outcome = Outcome.FAIL
			distractor_stim.auto_draw = True
			positions.remove(distractor_idx)
			#w7.stimuli.append(distractor_stim)
			w7.add_stimulus(distractor_stim)
		print(f'{ntargets} targets, {ndistractors} distractors')

		# Window 8
		w8 = Window(blank=2)

		return [w1, w2, w3, w4, w5, w6, w7, w8]