from psychopy import visual, event, logging
import time

ppy_window = visual.Window([1280, 720], monitor='test', units='pix', pos=(0,0))

rect = visual.Rect(
    win=ppy_window,
    units="pix",
    width=200,
    height=100,
    fillColor=[1, -1, -1],
    lineColor=[-1, -1, 1]
)

rect.draw()
ppy_window.flip()
time.sleep(2)