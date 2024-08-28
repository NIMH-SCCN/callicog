from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
from itertools import combinations
import random
import copy

class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init__()
        self.init_parameters()

    def init_parameters(self):
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
        self.add_parameter(Parameter.TARGET, stimuli_list)
        self.add_parameter(Parameter.TARGET_NUMBER, ntargets_list)
        self.add_parameter(Parameter.DELAY, delays_list)

    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()
        positions_list = [(-200, 100), (200, 100), (-200, -100), (200, -100)]
        self.add_parameter(Parameter.POSITION, positions_list)
        
        new_trials = []
        for trial in self.trials:
            targets = trial[Parameter.TARGET_NUMBER]
            C = list(combinations(range(len(positions_list)), targets))
            for positions in C:
                new_trial = copy.copy(trial)
                new_trial[Parameter.POSITION] = [positions_list[position_index] for position_index in positions]
                new_trials.append(new_trial)
        self.trials = new_trials

    def build_trial(self, trial_parameters={}):
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
        w3 = Window(transition=WindowTransition.RELEASE, label='encoding')
        w3_stim = copy.copy(trial_parameters[Parameter.TARGET])
        w3_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
        w3.add_stimulus(w3_stim)

        # Window 4
        w4 = Window(blank=0.5, label='encoding')

        # Window 5
        w5 = Window(transition=WindowTransition.RELEASE, label='encoding')
        w5_stim = copy.copy(trial_parameters[Parameter.TARGET])
        w5_stim.position = (random.randint(-615, 615), random.randint(-335, 335)) # ???
        w5.add_stimulus(w5_stim)

        # Window 6
        w6_blank = trial_parameters[Parameter.DELAY]
        w6 = Window(blank=w6_blank, label='maintenance')

        # Window 7
        # set targets
        w7 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3, is_outside_fail=True, label='retrieval')
        targets = trial_parameters[Parameter.TARGET_NUMBER]
        for i in range(targets):
            target_stim = copy.copy(trial_parameters[Parameter.TARGET])
            target_stim.position = trial_parameters[Parameter.POSITION][i]
            target_stim.outcome = Outcome.SUCCESS
            target_stim.after_touch = [{'name': 'hide'}]
            target_stim.timeout_gain = 2
            target_stim.auto_draw = True
            w7.add_stimulus(target_stim)
        
        # set distractors
        distractors = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])
        distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=trial_parameters[Parameter.POSITION])
        for i in range(len(distractors)):
            distractor_stim = copy.copy(distractors[i])
            distractor_stim.position = distractor_positions[i]
            distractor_stim.outcome = Outcome.FAIL
            distractor_stim.auto_draw = True
            w7.add_stimulus(distractor_stim)

        # Window 8
        w8 = Window(blank=2, label='outcome')

        return [w1, w2, w3, w4, w5, w6, w7, w8]