import numpy as np
from itertools import combinations

# lists
stim_list = ["red_square", "blue_circle", "yellow_arrow"]
position_list = [(-200, 100), (200, 100), (-200, -100), (200, -100)]
ntarget_list = [1, 2, 3]
delay_list = [1, 2, 4]

trial_configs = np.array(np.meshgrid(range(len(stim_list)), 
									 range(len(ntarget_list)), 
									 range(len(delay_list))
									 )
						).T.reshape(-1, 3) # 3 dimensions (3 lists)

trials = []
for config in trial_configs:
	ntargets_idx = config[1] # second dimension
	ntargets = ntarget_list[ntargets_idx]
	C = combinations(range(len(position_list)), ntargets)
	for positions in list(C):
		trial = np.concatenate((config, positions))
		trials.append(trial)

print(trials)
#np.array(np.meshgrid([1,2,3],[10,20,30,40,50,60],[-1,-2,-3,-4,-5,-6])).T.reshape(-1,3)