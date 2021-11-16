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

        color_list = [(1,0,0), (1,1,0), (0,0.7,1),(1,1,0), (0,0.7,1),(1,0,0),(-1, -1, -1),(1,1,0),(1,0,0), (1,1,0), (-1, -1, -1)]
        self.__add_pseudorandom_parameter_list('colours', color_list)
#IF I DONT WANT AN ELEMENT TO BE PSEUDORANDOMISED, ADD IT AFTER TRIALS = SELF.__PSEUDORANDOMISE PARAMETERS
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
        w1 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=5)
        w1_square = Stimulus(shape=StimulusShape.SQUARE,
                     size=(200,200))
        w1_square.color = trial_parameters['colours']
        w1_square.position = (random.randint(-520, 520), random.randint(-220, 220))
        w1.add_stimulus(w1_square)
        w1_square.outcome = Outcome.SUCCESS
        
        # Window 2
        w2 = Window(blank=0.5)

        return [w1, w2]
