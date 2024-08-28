from protocol_base import Window, Stimulus, StageOne

# define list of stimulus
stimuli = []
stimuli.append(Stimulus(size=700, position=[0, 0], color=[-1, -1, 1], outcome='correct'))

# create window, append stimuli, load and run
(success, run_start, run_end, events) = StageOne(window_size=[1280, 720], stimuli=stimuli).load().run()
if success:
	print('success')
	print(events)