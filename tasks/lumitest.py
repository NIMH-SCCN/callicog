from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init__()
        self.init_parameters()

    def init_parameters(self):
        color_list = [(-1,-1,1), (1,-1,-1), (1,1,-1)]
        self.add_parameter(Parameter.COLOR, color_list)

    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()
    def build_trial(self, trial_parameters={}):
        # Window 1
        w1 = Window(transition=WindowTransition.RELEASE, is_outcome=True, is_outside_fail=True)
       #yellow
        w1_a1 = Stimulus(shape=StimulusShape.SQUARE,
                     size=(-466,233),
                     position=(0, 0),
                     color=(255, 255, 0))
        w1_a2 = Stimulus(shape=StimulusShape.SQUARE,
                     size=(-466,0),
                     position=(0, 0),
                     color=(0, 200, 255))            

        w1.add_stimulus(w1_a1)
        w1_a1.outcome = Outcome.SUCCESS
        w1.add_stimulus(w1_a2)
        w1_a2.outcome = Outcome.SUCCESS
        # Window 2
        w2 = Window(blank=1)

        # Penalty window (n/a)
        pw = Window(blank=1)

        return [w1, w2, pw]
