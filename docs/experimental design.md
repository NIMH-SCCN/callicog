# Experimental design using CalliCog

## Summary

CalliCog provides a fast, easy, yet flexible way to design behavioral experiments. This can be achieved with 2 approaches as detailed below: **writing new protocols**, which involves using the in-built web app to create experiments based on pre-made parameters; and **writing new tasks and stimuli**, which requires basic programming knowledge to create new experiments from scratch. 

### Hierarchy

CalliCog uses a special hierarchy that must be understood to design or run experiments. Modifications at each level of the hierarchy allows for fine control of automated training protocols, from adjustments of a visual stimulus through to a behavioral task and the criteria for automated task progression (i.e. the progression criteria). Each level is summarised below:

- **Stimulus:** A visual stimulus presented to the test subject. Example: "A red square"
- **Window:** A visual display presented to the test subject on a touchscreen for a duration, usually containing Stimuli. Example: "Display containing a red square"
- **Trial:** A linear sequence of windows presented to a test subject that results in an Outcome (e.g. success, fail, or timeout). Example: "Window 1: present red square. Window 2: present blank display"
- **Task:** A behavioral task that follows a stereotyped structure. Tasks comprise multiple trials and specifies parameters to be changed between trials. Example: "Present a square that may be red, yellow or blue on different trials (i.e. `touch1.py`)"
- **Template:** An instance of a complete experimental protocol, applied to a specific Animal. Contains individual tasks and their progression criteria. Example: "Present coloured squares that gradually reduce in size with successful performance (i.e. touchscreen training)"


## Writing new protocols

Protocols are designed in the CalliCog web app under the `MANAGE` tabs. Each protocol consists of a template containing one or more tasks.

Before building a template, the tasks to be ran in that template must be imported in `Tasks`. To enter a task, specify the task name and select `Add`. It will then be appended to a list of imported tasks.
**Note:** the task must exist as a python script in `/src/callicog/tasks` in order to be imported. Ensure the filename is also added in `TASKS` without the extension `.py`.

Templates are constructed in `Templates`. To initialise a new template, choose a name (e.g. "touch_training") and select `Add` to import it to a list. Next, select the template from the list to edit it.
Templates consist of a list of tasks to be run in order, each of which has its own progression criteria that determines when a test subject should be progressed to the subsequent task. There are currently 3 types of progression criteria:

- `Target based`: Progression occurs after a set number of trials are performed, regardless of the outcome (success or fail). Example: “50 trials”.
- `Session based`: Progression occurs after a consecutive number of sessions (i.e. groups of trials) are performed to a specified level of proficiency. Example: “> 80% success in 3 consecutive sessions of 50 trials”.
- `Rolling average`: Progression occurs after a certain proficiency has been achieved over a rolling window of multiple trials, continuing in perpetuity until the criterion is reached. Example: “90% success within the last 100 trials”.

Adjust the following parameters to import a task and its progression criterion. **Note:** a 'trial' as defined below includes only valid trials, i.e. trials ending in a success or fail outcome.
- `task`: The task to be imported.
- `Progression`: The type of progression criterion. Selecting a criterion will automatically display only the relevant fields to that criterion type.
- `# trials`: (Target-based or session-based) The number of trials to be executed, either in total or per session.
- `# sessions`: (Session-based only) The number of consecutive sessions to be considered in progression logic. 
- `Success rate`: (Session-based or rolling average) The percentage of successful trials for progression. Values are expressed as a float between 0 and 1.
- `Window size`: (Rolling average) The size (in trials) of a rolling window.

## Writing new tasks and stimuli

### Writing stimuli

Visual displays using CalliCog are powered by PyschoPy, a powerful open-source psychophysics toolbox in Python. Currently, CalliCog can implement any static visual stimulus that can be defined using PsychoPy. For further instructions, see [here](https://psychopy.org/api/visual/index.html).

You do not need to create/modify stimuli to run CalliCog. Stimuli that are used for default tasks are already provided, including various shapes (square, circle, star, diamond, arrow, triangle) and images.

To define a new shape stimulus:
- Navigate to `/src/callicog` and edit `task_builder.py`. Choose a name for the new stimulus and define it under class `StimulusShape`. e.g. `SQUARE = 'square'`
- Edit `trial_interface.py`. Under class `WindowRuntime` and function `__get_ppy_stim_from_shape()`, define the stimulus using the variable in `task_builder.py` based on parameters from PychoPy. **IMPORTANT**: Only include fixed parameters that will NEVER change between trials in any task calling the stimulus. All other parameters are written into individual task files. Here is an example:

```
def __get_ppy_stim_from_shape(self, shape, ppy_window):
    if shape == StimulusShape.DIAMOND:
        return visual.Rect(win=ppy_window, ori=45, colorSpace='rgb')

# The color space for this stimulus and its orientation are defined here as they will never change, whenever the stimulus is initialised in any task. Other parameters (e.g. color, position, size) will.
```
To define a new image stimulus, import the chosen image into `/src/callicog/tasks/images`. This can then be called directly from a task file (see further for more detail).

### Writing tasks

Tasks are Python scripts that contain the instructions for a trial structure, in addition to the parameters that change between each trial in the task. To create or modify a task, a user must directly write to the Python script. Thankfully, these scripts are organised according to a standardised structure of 3 editable functions, which follow an intuitive workflow. 

Below is a task file skeleton. Copy and paste to begin creating a new task.

```
from callicog.task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from callicog.task_structure import TaskStructure
import random
import copy

class TaskInterface(TaskStructure):
	def __init__(self):
		super().__init__()
		self.init_parameters()

	def init_parameters(self):
		pass

	def generate_trials(self):
		pass

	def build_trial(self, trial_parameters={}):
		return []
```

#### Defining dynamic parameters: `init_parameters()`

Used to define dynamic parameters that will change between trials. If trials do not use dynamic parameters, simply return `pass`.
In the following example, a "correct" stimulus will be sampled from a pair of stimuli (a red square or blue circle) on a given trial, using the dynamic parameter `TARGET`. The function `init_parameters()` will contain:

```
red_square = Stimulus(shape=StimulusShape.SQUARE,
			size=(100, 100),
			color=(1, 0, 0))
blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
			size=(100, 100),
			color=(0, 0, 1))
stimulus_list = [red_square, blue_circle]

self.add_parameter(Parameter.TARGET, stimulus_list)
```

By default, parameters are **pseudorandom**, meaning that trials will be generated depending on all the possible combinations of added parameters. For instance, if we add a delay parameter to the task:

```
delay_list = [1, 2, 4]
self.add_parameter(Parameter.DELAY, delay_list)
```

The task will generate trials for all 6 (2x3) combinations of `stimulus_list` and `delay_list`. If you do not want to use a parameter for the generation of trials, simply indicate `pseudorandom=False` when calling the function `self.add_parameter()`. 

**Note:** `init_parameters()` does not return a value. Simply finish the function with `self.add_parameter()` calls or `pass` if the task is static.

#### Pseudorandomization: `generate_trials()`

If the task does not have parameters, simply place `pass`. Otherwise, this function is in charge of generating the trials based on the combinations of pseudorandom parameters. If that is the case, just write

```
self.trials = self.pseudorandomize_parameters()
```

#### Building the trial: `build_trial()`

This function contains the configuration for the trial structure. It defines the windows and consituent Stimuli that are to be sequentially presented in each trial.

##### Usage

To configure a window, first define the window and its constituent stimuli, then add Stimuli to the window. The following example displays a window containing a single predefined target stimulus that is positioned randomly within a specified area.

```
w1 = Window(transition=WindowTransition.RELEASE, label='window_1')
w1_stim = copy.copy(trial_parameters[Parameter.TARGET])
w1_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
w1.add_stimulus(w1_stim)
```
**Note:** All stimulus variables must be copied using `copy.copy()` when added to windows. If your task has dynamic parameters, these will be stored in the `trial_parameters` variable. For example, you can access which target to show in the trial by using `trial_parameters[Parameter.TARGET]`.

In addition, stimulus parameters can be static and not retrieved from a parameter list. For example:

```
w2 = Window(transition=WindowTransition.RELEASE)
w2_square = Stimulus(shape=StimulusShape.SQUARE,
			size=(100, 100),
			color=(-1, -1, -1),
			position=(0, 0))
w2.add_stimulus(w1_square)
```
##### Windows

Windows are objects that can contain be defined using the following parameters.

- `transition` (default=`None`). Controls whether to trigger the next window with a touch or release from the touchscreen. Possible values: `WindowTransition.RELEASE` and `WindowTransition.TOUCH`.
- `blank` (default=`0`). Defines the duration (in seconds) of a blank window.
- `is_outcome` (default=`False`). Defines the outcome window that will trigger the reward module. It requires Stimuli with associated outcomes (i.e. success, fail or null).
- `timeout` (default=`0`). Duration (in seconds) for the window to timeout. A timeout will result in the current trial being categorised as null, and the next trial will commence. Note: the default value `0` is symbolic; it will never timeout.
- `is_outside_fail` (default=`False`). Flag that instructs the window to mark the trial as fail if the background is touched.
- `label` (default=`''`). A custom field (string) to associate any information with the current window. Useful for labelling and extracting important timestamps for task-related neural recording.


Per convention, windows should be defined in the order that they are presented using the nomenclature `w1`, `w2`, `w3`, etc., and then returned as a list at the end of the function. However, the sequence of window presentation in the trial is **actually** dependent on the order of the returned list.
**Important**: The final window in the list is a special instance that is only executed if the trial ends in a failure, and is typically implemented as a blank display for a duration as a penalty timeout for the test subject. This window should be conventionally defined as `pw`, the penalty window. **Note** If the user desires to exclude a penalty from the task, `pw` **must** still be used, but should be assigned `blank=0`.

##### Stimuli

Stimuli are objects that can contain be currently defined using the following parameters.

- `shape`. Must be a member of `StimulusShape` (see `task_builder.py`).
- `size`. Must be a tuple of two elements (e.g. (100, 100)). Refers to the width and height (in pixels) of the stimuli. PsychoPy automatically adjusts depending on the geometry (e.g. circle taking 100 as its radius).
- `size_touch` (default `None`). Controls the size of the touch area for the stimulus. Also a tuple of two elements.
- `position` (default `None`). Stimulus coordinates (in pixels). PsychoPy considers the center of the screen as (0, 0). Also a tuple of two elements.
- `outcome` (default `None`). Assigns the outcome of the trial to the stimulus. Values are: `Outcome.SUCCESS`, `Outcome.FAIL` and `Outcome.NULL`.
- `color` (default `None`). RGB tuple (e.g. (0,0,1) for blue). -1 refers to black. Check 'RGB color space' [here](https://www.psychopy.org/general/colours.html) for more info.
- `image` (default `None`). Relative path (string) to an image file if the stimulus is an image. For example, a value can be `src/callicog/tasks/images/composite1-1.jpg`.
- `auto_draw` (default `False`). If `True`, the stimulus will appear even if it has not been explicitly drawn. Useful for the `hide` functionality.
- `after_touch` (default `[]`). (BETA) A list of objects like `{'name': 'FUNC'}`. `FUNC` will be executed after touching (or releasing, depending on transition) the stimulus. `FUNC` must be referenced in the `Stimulus` class, function `on_touch`, and also be implemented accordingly.
- `timeout_gain` (default `0`). (BETA) Adds the number of specified seconds to the window timeout value when the stimulus is touched (or released, depending on transition).


##### A useful function: `randomize_from()`

As the name suggests, it randomizes from a list. The function parameters are:

- `sample`. List of values to randomize from.
- `exclude` (default `[]`). List of values to exclude from `sample`.
- `size` (default `0`). Number of random values to get. The value `0` is symbolic, by default the function returns any number of values.

Most importantly, the return value is a list by default, even if only one random value is returned. You will then have to index `[0]` in order to retrieve the value.
Normally, one would randomize from a list of parameters that are not pseudorandom, but it can be any list. In order to access any parameter list previously defined in the task you write

```
self.pseudorandom_parameters[Parameter.PARAMETER_NAME]['values']
```

Always use the string `values` to get the list. The variable `self.pseudorandom_parameters` also contains parameters that are not pseudorandom, so ignore the poor choice of name.

Putting things together, assume we want to put random distractors in a window that contains a target. Obviously, we do not want the target to be repeated as a distractor. We also want to randomize the positions of those distractors. Assuming the following parameters: `Parameter.TARGET` and `Parameter.POSITION`, and a `Window` object, the distractors are

```
distractors = self.randomize_from(self.pseudorandom_parameters[Parameter.TARGET]['values'], exclude=[trial_parameters[Parameter.TARGET]])
distractor_positions = self.randomize_from(self.pseudorandom_parameters[Parameter.POSITION]['values'], exclude=[trial_parameters[Parameter.POSITION]], size=len(distractors))

for i in range(len(distractors)):
	distractor_stim = copy.copy(distractors[i])
	distractor_stim.position = distractor_positions[i]
	distractor_stim.outcome = Outcome.FAIL
	window.add_stimulus(distractor_stim)
```

Distractors are randomized from the list of targets (`self.pseudorandom_parameters[Parameter.TARGET]['values']`), excluding the current target for the trial (`trial_parameters[Parameter.TARGET]`). Since `exclude` must be a list, the stimulus is placed in brackets.
The positions are randomized from the list of positions (`self.pseudorandom_parameters[Parameter.POSITION]['values']`), excluding the current target position (`trial_parameters[Parameter.POSITION]`), again placed in brackets because is just one value and `exclude` must be a list.
In this case, we want to match the number of random positions with the number of distractors, hence `size=len(distractors)`.
Finally, we iterate through the list of distractors to add them to the current window object.


