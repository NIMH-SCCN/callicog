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
        red_square = Stimulus(shape=StimulusShape.SQUARE,
                    size=(100, 100),
                    color=(1, 0, 0))
        blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
                    size=(100, 100),
                    color=(0, 0, 1))

        stimuli_list = [red_square, blue_circle]
        ntargets_list = [1, 2, 3]
        delays_list = [1, 2, 4]

        # add them to task
        self.__add_pseudorandom_parameter_list('stimulus', stimuli_list)
        self.__add_pseudorandom_parameter_list('targets', ntargets_list)
        self.__add_pseudorandom_parameter_list('delay', delays_list)

    def generate_trials(self):
        trials = self.__pseudorandomize_parameters()
        
        # additional pseudorandom parameters
        # e.g. Supertask: positions depending on 'targets'
        positions_list = [(-200, 100), (200, 100), (-200, -100), (200, -100)]
        self.__add_pseudorandom_parameter_list('positions', positions_list)
        
        new_trials = []
        for trial in trials:
            targets = trial['targets']
            C = list(combinations(range(len(positions_list)), targets))
            for positions in C:
                new_trial = copy.copy(trial)
                new_trial['positions'] = [positions_list[position_index] for position_index in positions]
                new_trials.append(new_trial)
        self.trials = new_trials
        
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
        w3 = Window(transition=WindowTransition.RELEASE)
        w3_stim = copy.copy(trial_parameters['stimulus'])
        w3_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
        w3.add_stimulus(w3_stim)

        # Window 4
        w4 = Window(blank=0.5)

        # Window 5
        w5 = Window(transition=WindowTransition.RELEASE)
        w5_stim = copy.copy(trial_parameters['stimulus'])
        w5_stim.position = (random.randint(-615, 615), random.randint(-335, 335)) # ???
        w5.add_stimulus(w5_stim)

        # Window 6
        w6_blank = trial_parameters['delay']
        w6 = Window(blank=w6_blank)

        # Window 7
        # set targets
        w7 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3, is_outside_fail=True)
        targets = trial_parameters['targets']
        for i in range(targets):
            target_stim = copy.copy(trial_parameters['stimulus'])
            target_stim.position = trial_parameters['positions'][i]
            target_stim.outcome = Outcome.SUCCESS
            target_stim.after_touch = [{'name': 'hide'}]
            target_stim.timeout_gain = 2
            target_stim.auto_draw = True
            w7.add_stimulus(target_stim)
        
        # set distractors
        distractors = self.__randomize_from(self.pseudorandom_parameters['stimulus'], exclude=[trial_parameters['stimulus']])
        distractor_positions = self.__randomize_from(self.pseudorandom_parameters['positions'], exclude=trial_parameters['positions'])
        for i in range(len(distractors)):
            distractor_stim = copy.copy(distractors[i])
            distractor_stim.position = distractor_positions[i]
            distractor_stim.outcome = Outcome.FAIL
            distractor_stim.auto_draw = True
            w7.add_stimulus(distractor_stim)

        # Window 8
        w8 = Window(blank=2)

        return [w1, w2, w3, w4, w5, w6, w7, w8]