from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy
from time import sleep
import logging

logger = logging.getLogger(__name__)

class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init__()
        self.init_parameters()

# Defining possible stimuli
    def init_parameters(self):
        stimulus_list = [
            Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/composite1-1.jpg', color = (1,1,1), size_touch = (200,200)),
            Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/composite1-2.jpg', color = (1,1,1), size_touch = (200,200)),
            Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/composite2-1.jpg', color = (1,1,1), size_touch = (200,200)),
            # Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/composite2-2.jpg', color = (1,1,1), size_touch = (200,200)),
            # Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img5.jpg', color = (1,1,1), size_touch = (200,200)),
            # Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img6.jpg', color = (1,1,1), size_touch = (200,200)),
            # Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img7.jpg', color = (1,1,1), size_touch = (200,200)),
            # Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img8.jpg', color = (1,1,1), size_touch = (200,200)),
            # Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img9.jpg', color = (1,1,1), size_touch = (200,200)),
        ]
        self.stimulus_count = len(stimulus_list)

        self.add_parameter(Parameter.TARGET, stimulus_list)
    # Defining possible positions
        position_list = [(0,0), (-200, 0), (200, 0), (-200, -200)]
        #, (-200, 200), (200, 200), (200, -200), (0, 200), (0, -200)]
        self.add_parameter(Parameter.POSITION, position_list)
        
        # self.add_parameter(Parameter.TARGET_NUMBER, 1)
        # self.add_parameter(Parameter.DISTRACTOR_NUMBER, 3)
    # Defining delay between stimuli?
        # delay_list = [1]
        # self.add_parameter(Parameter.DELAY, delay_list, pseudorandom = False) #Don't use DELAY, probably have to create a new parameter

# Generating trials based on parameters
    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()

# help
    def build_trial(self, trial_parameters={}):        
        #Window 1: cue window
        w1 = Window(transition=WindowTransition.RELEASE)
        w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0,0))
        w1.add_stimulus(w1_square)
        
        # Build trial window sequence. Starting with no distractors, each successive window displays all prior stimuli.
        # The last window's target stimulus becomes a distractor in all subsequent windows
        
        # NOTE This while loop is a workaround. The `psuedorandom_parameters()` function is unexpectedly returning
        # a variable number of stimuli, instead of simply rearranging the list in a psuedorandom way as we expected,
        # so we re-try the selection until we come up with the desired number of stimuli.
        # IMPORTANT: this may not be statistically valid. 
        stimuli = []
        while len(stimuli) != self.stimulus_count:
            stimuli = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'])
            # deep copy all stimuli per README.md
            stimuli = [copy.copy(stimulus) for stimulus in stimuli]
            stimuli_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], size=len(stimuli))
            print("="*60)
            logger.info(f"stimuli {len(stimuli)}")
            logger.info(f"positions {len(stimuli_positions)}")
            print("="*60)

        trial_sequence = []
        distractors = []
        for (stimulus, position) in zip(stimuli, stimuli_positions):
            stimulus.position = position
            target = stimulus
            target.outcome = Outcome.SUCCESS
            window = Window(transition=WindowTransition.TOUCH, is_outcome=False)
            for distractor in distractors:
                window.add_stimulus(distractor)
            window.add_stimulus(target)
            trial_sequence.append(window)
        
            # Set up distractor for subsequent window:
            distractor = copy.copy(target)
            distractor.outcome = Outcome.FAIL
            distractors.append(distractor)    

        trial_sequence[-1].is_outcome = True

        # Spacer
        spacer = Window(blank=0.5)

        # Penalty window
        pw = Window(blank=1)

        return [w1] + trial_sequence + [spacer, pw]


# What I want for this task:
    # TODO update this to reflect revised understanding
    
    # random targets from a list of possible targets will appear one at a time
    #   at a random position from a list of 6 possible positions 
    
    # TODO 2 seconds of a blank window between each stimulus window (each novel stimulus appearing)
        # could be pseudorandomized per trial
    
    # TODO maybe have a long timeout period? Paper says 12s, but try 5s?
    # TODO reward after each correct touch?
    
    # all targets except for the novel one one will be distractors/result in a penalty when touched
    # any stimulus can be touched at any time, but only touching the novel one that appears will result in a success outcone
    
    # TODO make list comprehension for stimulus list