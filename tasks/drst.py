from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy
from time import sleep

  class TaskInterface(TaskStructure):
    def __init__(self):
        super().__init()
        self.init_parameters()

# Defining possible stimuli
    def init_parameters(self):
        img1 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img1.jpg', color = (1,1,1) size_touch = (200,200))
        img2 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img2.jpg', color = (1,1,1) size_touch = (200,200))
        img3 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img3.jpg', color = (1,1,1) size_touch = (200,200))
        img4 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img4.jpg', color = (1,1,1) size_touch = (200,200))
        img5 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img5.jpg', color = (1,1,1) size_touch = (200,200))
        img6 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img6.jpg', color = (1,1,1) size_touch = (200,200))
        img7 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img7.jpg', color = (1,1,1) size_touch = (200,200))
        img8 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img8.jpg', color = (1,1,1) size_touch = (200,200))
        img9 = Stimulus(shape = StimulusShape.IMAGE, size = (200,200), image = 'tasks/images/drst_img9.jpg', color = (1,1,1) size_touch = (200,200))
        stimulus_list = [img1, img2, img3, img4, img5, img6, img7, img8, img9]
        self.add_parameter(Parameter.TARGET, stimulus_list)
    # Defining possible positions
        position_list = [(0,0), (-400, 0), (400, 0), (-400, -400), (-400, 400), (400, 400), (400, -400), (0, 400), (0, -400)]
        self.add_parameter(Parameter.POSITION, position_list)
    # Defining delay between stimuli?
        delay_list = [1]
        self.add_parameter(Parameter.DELAY, delay_list, pseudorandom = False) #Don't use DELAY, probably have to create a new parameter

# Generating trials based on parameters
    def generate_trials(self):
        self.trials = self.pseudorandomize_parameters()

# help
    def build_trial(self, trial_parameters={}):
    #Window 1: cue window
        w1 = Window(transition=WindowTransition.RELEASE)
        w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0,0))
        w1.add_stimulus(w1_square)

############

    #Window 2: main task window
        w2 = Window(transition=WindowTransition.TOUCH, is_outcome=True)
    #defining penalty stimuli
        penalty_stim = Stimulus(shape = StimulusShape.IMAGE, image = trial_parameters[Parameter.TARGET])
        penalty_stim.position = trial_parameters[Parameter.POSITION][0]
        penalty_stim.outcome = Outcome.FAIL
        penalty_stim.after_touch = [{'name': 'hide_other'}]
    #defining reward stimuli
        reward_stim = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])[0] 
        reward_stim.position= self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]])[0] 
        reward_stim.outcome = Outcome.SUCCESS
        reward_stim.after_touch = [{'name': 'hide_other'}]
        
############

    #populating window with stimuli
        current_objects = 0
        distractor_index = 8
        while current_objects < distractor_index:
            w2.add_stimulus(penalty_stim)
            current_objects += 1 
            sleep(1)
            if current_objects == distractor_index:
               w2.add_stimulus(reward_stim)
        #sleep()?

##############

        #necessary for 'hide'ing to work?
        for stimulus in w2.stimuli:
            stimulus.auto_draw = True

        #Window 3: Spacer
        w3 = Window(blank=0.5)

        # Penalty window
        pw = Window(blank=1)

        return [w1, w2, w3, pw]



# What I want for this task:
    # Main task has 9 possible positions for targets to appear 
    # targets will appear one at a time with a 1 second delay in between each, at the 9 possible positions 
    # both targets and positions will be randomized
    # all targets except for the last one will be distractors/result in a penalty when touched
    # any stimulus can be touched at any time, but only touching the last one that appears will result in a success outcone


# Questions
    #copy.copy()?
    
