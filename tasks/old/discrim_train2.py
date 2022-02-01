from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome
import random
import numpy as np
from itertools import combinations
import copy

class TaskInterface:
    def __init__(self):
        self.pseudorandom_parameters = {}
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
        # e.g.
        # self.__add_pseudorandom_parameter_list('delay', delays_list)
        position_list = [(-382.5, 0), (382.5, 0)]

        # add them to task
        self.__add_pseudorandom_parameter_list('position', position_list)

    def get_trial(self, trial_index):
        trials = self.__pseudorandomize_parameters()
        # additional pseudorandom parameters (e.g. supertask - positions depending on targets)
        print('trials are ' + str(trials))
        print('list contains ' + str(trials.count) + 'elements')
        return trials[trial_index]


    def load(self, trial_index):
        # get pseudorandom parameters for the current trial

        print('trial index is ' + str(trial_index))
        trial_parameters = self.get_trial(trial_index)
        
        # Window 1
        w1 = Window(transition=WindowTransition.RELEASE)
        w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0, 0))
        w1.add_stimulus(w1_square)	
        
        # Window 2
        w2 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=2)
        reward_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = '/media/sf_callicog/tasks/images/composite2-1.jpg', color = (1,1,1), size_touch=(250,250)) #will need to change path
        penalty_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = '/media/sf_callicog/tasks/images/composite2-2.jpg', color = (1,1,1), size_touch=(250,250)) #will need to change path
        reward_stim.position = trial_parameters['position']
        penalty_stim.position = self.__randomize_from(self.pseudorandom_parameters['position'], exclude=[trial_parameters['position']])
        reward_stim.outcome = Outcome.SUCCESS
        penalty_stim.outcome = Outcome.FAIL
        w2.add_stimulus(reward_stim)	
        w2.add_stimulus(penalty_stim)	        
        return [w1, w2]