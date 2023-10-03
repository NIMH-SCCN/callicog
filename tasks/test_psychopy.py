from task_builder import Window, Stimulus, WindowTransition, StimulusShape, Outcome, Parameter
from task_structure import TaskStructure
import random
import copy
from psychopy import visual, event, logging

# window 1
window_size = [1280, 720]
fullscreen = True
ppy_window = visual.Window(window_size, monitor='test', units='pix', pos=(0,0), fullscr=fullscreen)
ppy_mouse = event.Mouse(win=ppy_window, visible=True)
w1 = Window(transition=WindowTransition.RELEASE)
w1.ppy_window = ppy_window
w1_square = Stimulus(shape=StimulusShape.SQUARE, size=(250, 250), color=(-1, -1, -1), position=(0, 0))
w1.add_stimulus(w1_square)
ppy_window.flip()
