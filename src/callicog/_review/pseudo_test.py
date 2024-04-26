import random

def shuffle_trials(ntrials):
	trial_indices = list(range(ntrials))
	#random.shuffle(trial_indices)
	iter_trials = iter(trial_indices)
	return trial_indices, iter_trials	

ntrials = 3
target_trials = 4
outcomes = ['success', 'null', 'fail']

trial_indices, iter_trials = shuffle_trials(ntrials)
task_complete = False
n_success = 0

while not task_complete:
	try:
		next_trial = next(iter_trials)
	except StopIteration:
		trial_indices, iter_trials = shuffle_trials(ntrials)
		continue

	trial_outcome = random.sample(outcomes, 1)[0]
	print(f'running trial {next_trial}, outcome: {trial_outcome}, n_success: {n_success}')
	if trial_outcome == 'null':
		trial_indices.append(next_trial)
	elif trial_outcome == 'success':
		n_success += 1

	if n_success >= target_trials:
		task_complete = True
print('finished')