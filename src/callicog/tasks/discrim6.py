from callicog.tasks import IMAGE_DIR
from callicog.task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from callicog.task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init__()
        self.init_parameters()

    def init_parameters(self):
        position_list = [(-382.5, 0), (382.5, 0)]
        self.add_parameter(Parameter.POSITION, position_list)        

    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()

    def build_trial(self, trial_parameters={}):
        # Window 1
        w1 = Window(transition=WindowTransition.RELEASE)
        w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0, 0))
        w1.add_stimulus(w1_square)

        # Window 2
        # In discrimination & reversal tasks, stimuli remain briefly after being touched to provide visual feedback. This is executed below.
        w2 = Window(transition=WindowTransition.MAINTAIN, is_outcome=True, timeout=2)
        w2.post_touch_delay = 1
        reward_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = IMAGE_DIR/'composite9-1.jpg', color = (1,1,1), size_touch=(250,250))
        reward_stim.after_touch = [{'name': 'hide_other'}]
        penalty_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = IMAGE_DIR/'composite9-2.jpg', color = (1,1,1), size_touch=(250,250))
        penalty_stim.after_touch = [{'name': 'hide_other'}]
        reward_stim.position = trial_parameters[Parameter.POSITION]
        reward_stim.outcome = Outcome.SUCCESS
        penalty_stim.position = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])[0]
        penalty_stim.outcome = Outcome.FAIL
        w2.add_stimulus(reward_stim)
        w2.add_stimulus(penalty_stim)

        # Required for 'hide' functionality
        for stimulus in w2.stimuli:
            stimulus.auto_draw = True

        # Window 3
        w3 = Window(blank=0.5)
        
        # Penalty window - conditional
        pw = Window(blank=1.5)

        return [w1, w2, w3, pw]