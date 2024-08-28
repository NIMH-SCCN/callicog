from psychopy import visual, core
import math, time, random

mywin = visual.Window(units='pix', size=[1280,720])
stim = visual.GratingStim(win=mywin, size=250, colorSpace='rgb255', color=[0,0,255], pos=[0,0], sf=0)
stim.draw(mywin)
mywin.update()
time.sleep(5)
