from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome
import random
import numpy as np
from itertools import combinations
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

    def generate_trials(self):
        trials = self.__pseudorandomize_parameters()
        # additional pseudorandom parameters (e.g. supertask - positions depending on targets)
        print('trials are ' + str(trials))
        print('list contains ' + str(trials.count) + 'elements')
        self.trials = trials


    def build_trial(self, trial_index):
        # get pseudorandom parameters for the current trial

        print('trial index is ' + str(trial_index))
        trial_parameters = self.trials[trial_index]
        
        # Window 1
        w1 = Window(transition=WindowTransition.RELEASE)
        w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0, 0))
        w1.add_stimulus(w1_square)	
        
        # Window 2
        w2 = Window(blank=0.5)

        # Window 3
        w3 = Window(transition=WindowTransition.RELEASE)
        w3_stim = copy.copy(trial_parameters['stimulus'])
        w3.add_stimulus(w3_stim)

        # Window 4
        w4 = Window(blank=0.5)

        # Window 5
        w5 = Window(transition=WindowTransition.RELEASE)
        w5_stim = copy.copy(trial_parameters['stimulus'])
        w5.add_stimulus(w5_stim)        

        # Window 6
        w6_blank = trial_parameters['delay']
        w6 = Window(blank=w6_blank)

        # Window 7
        # define target
        w7 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3)  
        w7_target = copy.copy(trial_parameters['stimulus'])
        w7_target.position = trial_parameters['position']
        w7_target.outcome = Outcome.SUCCESS
        # define distractor      
        distractors = self.__randomize_from(self.pseudorandom_parameters['stimulus'], exclude=[trial_parameters['stimulus']])
        distractor_positions = self.__randomize_from(self.pseudorandom_parameters['position'], exclude=[trial_parameters['position']])
        for i in range(len(distractors)):
            w7_distractor = copy.copy(distractors[i])
            w7_distractor.position = distractor_positions[i]
            w7_distractor.outcome = Outcome.FAIL
            w7_distractor.auto_draw = True
        w7.add_stimulus(w7_distractor)      
      
        w7.add_stimulus(w7_target)

        # Window 8
        w8 = Window(blank=2)
        
        return [w1, w2, w3, w4, w5, w6, w7, w8]