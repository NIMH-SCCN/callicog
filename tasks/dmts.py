from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init__()
        self.init_parameters()

    def init_parameters(self):
        red_diamond = Stimulus(shape=StimulusShape.DIAMOND, size=(176.78,176.78), color=(1,1,-1), position=(0,0), size_touch=(250,250))
        blue_star = Stimulus(shape=StimulusShape.STAR, size = (1,1), color=(-1, -1, 1), position=(0,0), size_touch=(250,250))

        stimulus_list = [red_diamond, blue_star]
        delay_list = [0.5, 1, 2, 4]
        position_list = [(-382.5, 0), (382.5, 0)]

        self.add_parameter(Parameter.TARGET, stimulus_list)
        self.add_parameter(Parameter.DELAY, delay_list)
        self.add_parameter(Parameter.POSITION, position_list)

    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()

    def build_trial(self, trial_parameters={}):        
        # Window 1
        w1 = Window(transition=WindowTransition.RELEASE)
        w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0, 0))
        w1.add_stimulus(w1_square)	
        
        # Window 2
        w2 = Window(blank=0.5)

        # Window 3
        w3 = Window(transition=WindowTransition.RELEASE)
        w3_stim = copy.copy(trial_parameters[Parameter.TARGET])
        w3.add_stimulus(w3_stim)

        # Window 4
        w4 = Window(blank=0.5)

        # Window 5
        w5 = Window(transition=WindowTransition.RELEASE)
        w5_stim = copy.copy(trial_parameters[Parameter.TARGET])
        w5.add_stimulus(w5_stim)        

        # Window 6
        w6_blank = trial_parameters[Parameter.DELAY]
        w6 = Window(blank=w6_blank)

        # Window 7
        # define target
        w7 = Window(transition=WindowTransition.TOUCH, is_outcome=True, timeout=3)  
        w7_target = copy.copy(trial_parameters[Parameter.TARGET])
        w7_target.position = trial_parameters[Parameter.POSITION]
        w7_target.outcome = Outcome.SUCCESS
        # define distractor      
        distractors = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])
        distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])
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