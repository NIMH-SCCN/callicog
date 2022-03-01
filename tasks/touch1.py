from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init__()
        self.init_parameters()

    def init_parameters(self):
        color_list = [(0,0,1), (1,0,0), (1,1,0)]
        self.add_parameter(Parameter.COLOR, color_list)

    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()

    def build_trial(self, trial_parameters={}):
        # Window 1
        w1 = Window(transition=WindowTransition.TOUCH, is_outcome=True, is_outside_fail=True)
        w1_square = Stimulus(shape=StimulusShape.SQUARE,
                     size=(1280,720),
                     position=(0, 0))
        w1_square.color = trial_parameters[Parameter.COLOR]
        w1.add_stimulus(w1_square)
        w1_square.outcome = Outcome.SUCCESS
        # Window 2
        w2 = Window(blank=0.5)

        return [w1, w2]
