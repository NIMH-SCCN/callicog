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
        red_diamond = Stimulus(shape=StimulusShape.DIAMOND, size=(176.78,176.78), color=(1,1,-1), position=(0,0), size_touch=(250,250))
        blue_star = Stimulus(shape=StimulusShape.STAR, size = (1,1), color=(-1, -1, 1), position=(0,0), size_touch=(250,250))

        stimulus_list = [red_diamond, blue_star]
        delay_list = [0.5, 1, 2, 4]
        position_list = [(-382.5, 0), (382.5, 0)]

        # add them to task
        self.__add_pseudorandom_parameter_list('stimulus', stimulus_list)
        self.__add_pseudorandom_parameter_list('delay', delay_list)
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
        
        # Window 1
        w2 = Window(transition=WindowTransition.RELEASE)
        w2_square = Stimulus(shape=StimulusShape.IMAGE, image = '/media/sf_callicog/tasks/composite1-1.jpg', size=(250, 250), position=(0,0), color=(1,1,1))
        w2.add_stimulus(w2_square)	
        
        return [w1, w2]