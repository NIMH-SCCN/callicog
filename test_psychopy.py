from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
from trial_interface import WindowRuntime
import random
import copy
from psychopy import visual, event, logging, core, monitors

window_size = [1280, 720]
fullscreen = True
# ppy_window = visual.Window(window_size, units='pix', color=(0,0,0), pos=(0,0), fullscr=fullscreen)
ppy_window = visual.Window(window_size, monitor='testMonitor', units='pix', color=(0,0,0), pos=(0,0), fullscr=fullscreen)
ppy_mouse = event.Mouse(win=ppy_window, visible=True)

# Window 1
w1 = Window(transition=WindowTransition.RELEASE)
w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0, 0))
w1.add_stimulus(w1_square)

# Window 2
# set targets
w2 = Window(transition=WindowTransition.MAINTAIN, is_outcome=True, timeout=4)
reward_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite4-2.jpg', color = (1,1,1), size_touch=(250,250))
reward_stim.after_touch = [{'name': 'hide'}]
penalty_stim = Stimulus(shape=StimulusShape.IMAGE, size=(250,250), image = 'tasks/images/composite4-1.jpg', color = (1,1,1), size_touch=(250,250))
penalty_stim.after_touch = [{'name': 'hide'}]
reward_stim.position = (-382.5, 0)
reward_stim.outcome = Outcome.SUCCESS
penalty_stim.position = (382.5, 0) 
penalty_stim.outcome = Outcome.FAIL
w2.add_stimulus(reward_stim)
w2.add_stimulus(penalty_stim)
#this is necessary for 'hide'ing to work?
#for stimulus in w2.stimuli:
#    stimulus.auto_draw = True

# Window 3
w3 = Window(blank=0.5)

# Penalty window - conditional
pw = Window(blank=1.5)

w1.timeout = 2
w2.timeout = 4
w3.timeout = 4
pw.timeout = 1

windows = [w1, w2, w3, pw]

ppy_runtime = WindowRuntime()
for window in windows[:-1]:
    flip_time = ppy_runtime.run_window(window, ppy_window)
    window.flip_tstamp = flip_time

    if window.is_outcome:
        targets = [stimulus for stimulus in window.stimuli if stimulus.outcome == Outcome.SUCCESS]
        while not all([target.touched for target in targets]):
            outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)
            if (outcome == Outcome.FAIL) or (outcome == Outcome.NULL):
                break

        if outcome == Outcome.SUCCESS:
            print('box: correct')
        elif outcome == Outcome.FAIL:
            print('box: incorrect')
        elif outcome == Outcome.NULL:
            pass

        elif window.timeout > 0 and not window.is_outcome:
            outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)    

        elif window.blank == 0:
            outcome = ppy_runtime.get_touch_outcome(window, flip_time, ppy_mouse)


#successes = 0
#touched = False
#time_limit = 4
#start_time = core.getTime()
#elapsed = 0
#print("flip 1")
#w1.ppy_window.flip()
#core.wait(1)
#for s in w1.stimuli:
#    print("draw")
#    s.draw()
#print("flip 2")
#w1.ppy_window.flip()

#while elapsed > time_limit:
#    ppy_window.flip()
#    ppy_window.flip()
#    elapsed = core.getTime() - start_time

# # List all available monitors
# available_monitors = monitors.getAllMonitors()
# 
# # Print information about each monitor
# for monitor in available_monitors:
#     print(monitor)
#     print(type(monitor))
#     #print(f"Monitor Name: {monitor['name']}")
#     #print(f"Width (pixels): {monitor['width']}")
#     #print(f"Height (pixels): {monitor['height']}")
#     #print(f"Distance (cm): {monitor['distance']}")
#     #print(f"Gamma: {monitor['gamma']}")
#     #print(f"Use this monitor for: {monitor['notes']}\n")
# 
# # Alternatively, you can use a loop to print only the monitor names
# # for monitor in available_monitors:
# #     print(f"Monitor Name: {monitor['name']}")
# 
# # Select a specific monitor by name if needed
# # my_monitor = monitors.Monitor(name='YourMonitorName')
