# Experimental design using CalliCog

## Summary

CalliCog provides a fast, easy, yet flexible way to design behavioral experiments. This can be achieved over 2 levels as detailed below: writing new protocols, which involves using the in-built web app to create experiments based on pre-made parameters; and writing new tasks and stimuli, which requires basic programming knowledge to create new experiments from scratch. 

### (IMPORTANT) Hierarchy

CalliCog uses a special hierarchy that must be understood to design or run experiments. Modifcations at each level of the hierarchy allows for fine control of automated training protocols, from adjustments of a visual stimulus through to a behavioral task and the criteria for automated task progression (i.e. the progression criteria). Each level is summarised below:

- **Stimulus:** A visual stimulus presented to the test subject. Example: "A red square"
- **Window:** A visual display presented to the test subject on a touchscreen for a duration, usually containing Stimuli. Example: "Display containing a red square"
- **Trial:** A linear sequence of Windows presented to a test subject that results in an Outcome (e.g. success, fail, or timeout). Example: "Window 1: present red square. Window 2: present blank display"
- **Task:** A behavioral task that follows a stereotyped structure. Tasks comprise multiple Trials and specifies parameters to be changed between trials. Example: "Present a square that may be red, yellow or blue on different trials (i.e. `touch1.py`)"
- **Template:** An instance of a complete experimental protocol, applied to a specific Animal. Contains individual Tasks and their progression criteria. Example: "Present coloured squares that gradually reduce in size with successful performance (i.e. touchscreen training)"

## 1. Writing new protocols

Protocols are designed in the CalliCog web app under the `MANAGE` tabs. Each protocol consists of a Template containing one or more Tasks.

Before building a Template, the Tasks to be ran in that Template must be imported in `Tasks`. To enter a task, specify the task name and select `Add`. It will then be appended to a list of imported tasks.
**Note:** the task must exist as a python script in `/src/callicog/tasks` in order to be imported. Ensure the filename is also added in `TASKS` without the extension `.py`.

Templates are constructed in `Templates`. To initialise a new template, choose a name (e.g. "touch_training") and select `Add` to import it to a list. Next, select the Template from the list to edit it.
Templates consist of a list of Tasks to be run in order, each of which has its own progression criteria that determines when a test subject should be progressed to the subsequent Task. There are currently 3 types of progression criteria:

- `Target based`: Progression occurs after a set number of Trials are performed, regardless of the outcome (success or fail). Example: “50 trials”.
- `Session based`: Progression occurs after a consecutive number of sessions (i.e. groups of Trials) are performed to a specified level of proficiency. Example: “> 80% success in 3 consecutive sessions of 50 trials”.
- `Rolling average`: Progression occurs after a certain proficiency has been achieved over a rolling window of multiple Trials, continuing in perpetuity until the criterion is reached. Example: “90% success within the last 100 trials”.

Adjust the following parameters to import a task and its progression criterion. **Note:** a 'Trial' as defined below includes only valid Trials, i.e. Trials ending in a success or fail outcome.
- `Task`: The task to be imported.
- `Progression`: The type of progression criterion. Selecting a criterion will automatically display only the relevant fields to that criterion type.
- `# trials`: (Target-based or session-based) The number of Trials to be executed, either in total or per session.
- `# sessions`: (Session-based only) The number of consecutive sessions to be considered in progression logic. 
- `Success rate`: (Session-based or rolling average) The percentage of successful Trials for progression. Values are expressed as a float between 0 and 1.
- `Window size`: (Rolling average) The size (in Trials) of a rolling window.

## 2. Writing new tasks and stimuli

# Writing stimuli

Visual displays using CalliCog are powered by PyschoPy, a powerful open-source psychophysics toolbox in Python. Currently, CalliCog can implement any static visual stimulus that can be defined using PsychoPy. For further instructions, see [here](https://psychopy.org/api/visual/index.html).

You do not need to create/modify stimuli to run CalliCog. Stimuli that are used for default Tasks are already provided, including various shapes (square, circle, star, diamond, arrow, triangle) and images.

To define a new shape Stimulus:
- Navigate to `/src/callicog` and edit `task_builder.py`. Choose a name for the new Stimulus and define it under class `StimulusShape`. e.g. `SQUARE = 'square'`
- Edit `trial_interface.py`. Under class `WindowRuntime` and function `__get_ppy_stim_from_shape()`, define the Stimulus using the variable in `task_builder.py` based on parameters from PychoPy. **IMPORTANT**: Only include fixed parameters that will NEVER change between Trials in any Task calling the Stimulus. All other parameters are written into individual Task files. Here is an example:

```
def __get_ppy_stim_from_shape(self, shape, ppy_window):
    if shape == StimulusShape.DIAMOND:
        return visual.Rect(win=ppy_window, ori=45, colorSpace='rgb')

# The color space for this Stimulus and its orientation are defined here as they will never change, whenever the Stimulus is initialised in any Task. Other parameters (e.g. color, position, size) will.
```
To define a new image Stimulus, import the chosen image into `/src/callicog/tasks/images`. This can then be called directly from a Task file (see further for more detail).

# Writing a task

Tasks are Python scripts that contain the instructions for a Trial structure, in addition to the parameters that change between each Trial in the Task. To create or modify a Task, a user must directly write to the Python script. Thankfully, these scripts are organised according to a standardised structure of 3 editable functions, which follow an intuitive workflow. 

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

#### The function `init_parameters()`

Used to define dynamic parameters that will change between Trials. If Trials do not use dynamic parameters, simply return `pass`.
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

By default, parameters are **pseudorandom**, meaning that trials will be generated depending on all the possible combinations of added parameters. For instance, if we add a delay parameter to the Task:

```
delay_list = [1, 2, 4]
self.add_parameter(Parameter.DELAY, delay_list)
```

The task will generate trials for all 6 (2x3) combinations of `stimulus_list` and `delay_list`. If you do not want to use a parameter for the generation of trials, simply indicate `pseudorandom=False` when calling the function `self.add_parameter()`. 

**Note:** `init_parameters()` does not return a value. Simply finish the function with `self.add_parameter()` calls or `pass` if the task is static.

#### The function `generate_trials()`

If the task does not have parameters, simply place `pass`. Otherwise, this function is in charge of generating the trials based on the combinations of pseudorandom parameters. If that is the case, just write

```
self.trials = self.pseudorandomize_parameters()
```

#### The function `build_trial()`

This function contains the configuration for the Trial structure. It defines the Windows and consituent Stimuli that are to be sequentially presented in each trial.


~~~~~Everything below is work in progress. Note to self: shift text below around to make a logical order~~~~~







Per convention, Windows should be defined in the order that they are presented using the nomenclature `w1`, `w2`, `w3`, etc., and then returned as a list at the end of the function. However, the sequence of Window presentation in the trial is **actually** solely dependent on the order of the returned list.
**Important**: The final Window in the list is a special instance that is only executed if the trial ends in a failure, and is typically implemented as a blank display for a duration as a penalty timeout for the test subject. This Window should be conventionally defined as `pw`, the penalty Window. **Note** If the user desires to exclude a penalty from the task, `pw` **must** still be defined, but should be assigned `blank=0`



If your task has pseudorandom parameters, the values will be stored in the `trial_parameters` variable. For example, you can access which target to show in the trial by using `trial_parameters[Parameter.TARGET]`.

```
w1 = Window(transition=WindowTransition.RELEASE, label='encoding')
w1_stim = copy.copy(trial_parameters[Parameter.TARGET])
w1_stim.position = (random.randint(-615, 615), random.randint(-335, 335))
w1.add_stimulus(w1_stim)
```

Remember to `copy.copy()` all stimulus variables when adding them to windows.
Window objects can have the following user-defined parameters:

- `transition` (default=`None`). Controls whether to trigger the next window with a touch or release. Possible values: `WindowTransition.RELEASE` and `WindowTransition.TOUCH`.
- `blank` (default=`0`). Defines the duration (in seconds) of a blank window.
- `is_outcome` (default=`False`). Defines the outcome window that will trigger the reward system. It will need stimuli with pre defined outcomes (success, fail or null).
- `timeout` (default=`0`). Duration (in seconds) for the window timeout. The value `0` is symbolic, it will never timeout.
- `is_outside_fail` (default=`False`). Flag that instructs the window to mark the trial as fail if touched anything but stimuli.
- `label` (default=`''`). Window description in terms of behavioral phases (e.g. 'encoding', 'outcome', etc). It can also be used as a custom field (string) to associate any information with the current window.

In addition, stimulus can be static and not retrieved from a parameter list. For example:

```
w2 = Window(transition=WindowTransition.RELEASE)
w2_square = Stimulus(shape=StimulusShape.SQUARE,
			size=(100, 100),
			color=(-1, -1, -1),
			position=(0, 0))
w2.add_stimulus(w1_square)
```

Stimulus objects can have the following user-defined parameters:

- `shape`. Must be a member of `StimulusShape`. The values are defined in the file `task_builder.py` and more can be added.
- `size`. Must be a tuple of two elements (e.g. (100, 100)). Refers to the width and height (in pixels) of the stimuli. PsychoPy automatically adjusts depending on the geometry (e.g. circle taking 100 as its radius).
- `size_touch` (default `None`). Controls the size of the touch area for the stimulus. Also a tuple of two elements.
- `position` (default `None`). Stimulus coordinates (in pixels). PsychoPy considers the center of the screen as (0, 0). Also a tuple of two elements.
- `outcome` (default `None`). Assigns the outcome of the trial to the stimulus. Values are: `Outcome.SUCCESS`, `Outcome.FAIL` and `Outcome.NULL`.
- `color` (default `None`). RGB tuple (e.g. (0,0,1) for blue). -1 refers to black. Check 'RGB color space' [here](https://www.psychopy.org/general/colours.html) for more info.
- `image` (default `None`). Relative path (string) to an image file if the stimulus is an image. For example, a value can be `'tasks/images/composite4-1.jpg'`.
- `auto_draw` (default `False`). If `True`, the stimulus will appear even if it has not been explicitly drawn. Useful for the `hide` functionality.
- `after_touch` (default `[]`). A list of objects like `{'name': 'FUNC'}`. `FUNC` will be executed after touching (or releasing, depending on transition) the stimulus. `FUNC` must be referenced in the `Stimulus` class, function `on_touch`, and also be implemented accordingly.
- `timeout_gain` (default `0`). Adds the number of specified seconds to the window timeout value when the stimulus is touched (or released, depending on transition).

Remember that the function `build_trial()` returns a list of windows (e.g. `return [w1, w2]`).

#### Other useful function: `randomize_from()`

As the name suggests, it randomizes from a list. The function parameters are:

- `sample`. List of values to randomize from.
- `exclude` (default `[]`). List of values to exclude from `sample`.
- `size` (default `0`). Number of random values to get. The value `0` is symbolic, by default the function returns any number of values.

Most importantly, the return value is a list by default, even if only one random value is returned. You will then have to index `[0]` in order to retrieve the value.
Normally, one would randomize from a list of parameters that are not pseudorandom, but it can be any list. In order to access any parameter list previously defined in the task you write

```
self.pseudorandom_parameters[Parameter.PARAMETER_NAME]['values']
```

Always use the string `values` to get the list. The variable `self.pseudorandom_parameters` also contains parameters that are not pseudorandom so ignore the poor choice of name.

Putting things together, assume we want to put random distractors in a window that contains a target. Obviously, we do not want the target to be repeated as a distractor. We also want to randomize the positions of those distractors. Assuming the following parameters: `Parameter.TARGET` and `Parameter.POSITION`, and a `window` object, the distractors are

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


