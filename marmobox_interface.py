import time
#import marmobox_hardware as hw
import marmobox_stimuli as st
from marmobox_IO import MarmoboxIO
from psychopy import visual, event, logging

#def wait_for_animal(timeout):
#	rfid_tag = None
#	duetime = time.time() + timeout
#	while rfid_tag is None and time.time() < duetime:
#		rfid_tag = hw.read_rfid()
#		time.sleep(0.5)
#	return rfid_tag

class MarmoboxInterface:
	def __init__(self, arduino_port, window_size):
		self.arduino_port = arduino_port
		self.window_size = window_size

	def initialize(self):
		try:
			self.box = MarmoboxIO(self.arduino_port, dummy=True)
			self.box.connect()
		except:
			print('Failed to connect to Arduino')
			return False
		self.ppy_window = visual.Window(self.window_size, monitor='test', units='pix', pos=(0,0), fullscr=False)
		self.ppy_mouse = event.Mouse(win=self.ppy_window)
		logging.console.setLevel(logging.ERROR)
		return True

	def close(self):
		self.box.disconnect()
		self.ppy_window.close()
		self.ppy_mouse = None

	def run_trial(self, trial_params):
		return st.process_stimulus(trial_params, self.box, self.ppy_window, self.ppy_mouse)