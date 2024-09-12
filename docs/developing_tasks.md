# Developing new tasks for CalliCog

### Writing new tasks

Tasks are Python files that contain the instructions for trial-based stimuli presentation. New files are created in `~/callicog/tasks`. Make sure the filename is also added in the database (via 'Tasks' in the web app) without the extension `.py`.

This is the task file skeleton. Copy and paste to start with a new task.

```
from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
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

Used to define general purpose parameters. If task trials do not use parameters, simply return `pass`.
Alternatively, trials can use parameters to vary the presentation of stimuli. For example, if we want trials to show a target stimulus from a  list, the function `init_parameters()` will contain:

```
red_square = Stimulus(shape=StimulusShape.SQUARE,
			size=(100, 100),
			color=(1, 0, 0))
blue_circle = Stimulus(shape=StimulusShape.CIRCLE,
			size=(100, 100),
			color=(0, 0, 1))
stimuli_list = [red_square, blue_circle]

self.add_parameter(Parameter.TARGET, stimuli_list)
```

By default, the parameter added is **pseudorandom**, meaning that trials will be generated depending on all the possible combinations of the added parameters. For instance if we add a delay parameter:

```
delays_list = [1, 2, 4]
self.add_parameter(Parameter.DELAY, delays_list)
```

The task will generate trials for all combinations of `TARGET` and `DELAY`. If you do not want to use a parameter for the generation of trials, simply indicate `pseudorandom=False` when calling the function `self.add_parameter()`. For example:

```
self.add_parameter(Parameter.DELAY, delays_list, pseudorandom=False)
```

Hence, the trials will only be generated from shuffling `stimuli_list`.

The function `init_parameters()` does not return a value. Simply finish the function with `self.add_parameter()` calls or `pass` if the task is static.

#### The function `generate_trials()`

If the task does not have parameters, simply place `pass`. Otherwise, this function is in charge of generating the trials based on the combinations of pseudorandom parameters. If that is the case, just write

```
self.trials = self.pseudorandomize_parameters()
```

There are instances where parameters depend on others. For example, we add the parameter `Parameter.TARGET_NUMBER` which controls the number of stimuli in the trial. If we also want to pseudorandomize the positions of those targets, the number of parameters per trial will be dynamic, making it difficult to calculate the combinations.

For such scenarios, you can modify `self.trials` as you see fit after calling `self.pseudorandomize_parameters()`. The task `supertask_min` does this by going through all generated trials and appending pseudorandom positions based on the number of targets.

However, if no post-processing of trials is necessary, no further code is required.

#### The function `build_trial(trial_parameters={})`

This function returns a list of windows for the current trial. Windows are designed by placing stimuli and controlling the presentation via the use of parameters.
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


