import time
import marmobox_hardware as hw
import marmobox_stimuli as st
from marmobox_IO import MarmoboxIO

# dummy agent

def wait_for_animal(timeout):
	rfid_tag = None
	duetime = time.time() + timeout
	while rfid_tag is None and time.time() < duetime:
		rfid_tag = hw.read_rfid()
		time.sleep(0.5)
	return rfid_tag

def run_trial(trial_params):
	#box = MarmoboxIO('ttyACM0')
	return st.process_stimulus(trial_params, None)