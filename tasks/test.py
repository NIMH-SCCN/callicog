from psychopy import visual
import math
import random

#mywin = visual.Window(monitor='test', units='pix', size=(1280,720))
#stim = visual.Rect(win=mywin, size=300, colorSpace='rgb', color=[0,0,1])
#stim.draw(mywin)


star_vertices = []
outer_radius = 131
inner_radius = 65
for vertex in range(0,5):
    x = outer_radius*math.cos(math.radians(90+vertex*72))
    y = outer_radius*math.sin(math.radians(90+vertex*72))
    star_vertices.append([x,y]); x = inner_radius*math.cos(math.radians(126+vertex*72))
    y = inner_radius*math.sin(math.radians(126+vertex*72))
    star_vertices.append([x,y])

print(star_vertices)

position=(random.randint(-135,135), random.randint(-65,65))
print(position)