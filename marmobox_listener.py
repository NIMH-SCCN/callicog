import socket
import serial
import sys
import json
import marmobox_interface as mbox
from threading import Thread

MAX_LENGTH = 4096
PORT = 10000
HOST = '0.0.0.0'
#ARDUINO_PORT = 'ttyACM0'

class ThreadReturns(Thread):
	def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
		Thread.__init__(self, group, target, name, args, kwargs)
		self._return = None

	def run(self):
		#print(type(self._target))
		if self._target is not None:
			self._return = self._target(*self._args, **self._kwargs)

	def join(self, *args):
		Thread.join(self, *args)
		return self._return

def pack_response(response_object):
	response = { 'success': 0 }
	if response_object:
		response['success'] = 1
		response['body'] = {
			'data': response_object
		}
	return response

def parse_msg(msg, client_socket):
	if msg['action'] == 'wait_for_animal': # clean this
		animal_code = mbox.wait_for_animal(timeout = 3)
		response = pack_response(animal_code)
	elif msg['action'] == 'run_trial':
		# in a thread
		process = ThreadReturns(target=mbox.run_trial, args=[msg['trial_params']])
		process.start()
		trial_data = process.join()
		# end of thread
		response = pack_response(trial_data)
	client_socket.send(bytes(json.dumps(response), 'utf8'))

def handle(client_socket):
	while True:
		buf = client_socket.recv(MAX_LENGTH)
		if buf is None:
			return
		try:
			msg = json.loads(buf.decode())
			parse_msg(msg, client_socket)
		except json.decoder.JSONDecodeError:
			return

#class MarmoboxServer:
#	def __init__(self, host, port, timeout, max_clients, arduino_port_prefix):
#		self.host = host
#		self.port = port
#		self.timeout = timeout
#		self.max_clients = max_clients
#		self.arduino_port_prefix = arduino_port_prefix
#		self.clients = []
#		self.arduino_port = None
#		self.server_socket = None
#
#	def _get_arduino_port(self, prefix):
#		ports = glob.glob(self.arduino_port_prefix + '[0-9]*')
#		for port in ports:
#			try:
#				s = serial.Serial(port)
#				s.close()
#				return port
#			except:
#				pass
#		return None
#	
#	def start(self):
#		#self.arduino_port = self._get_arduino_port('/dev/ttyACM')
#		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#		self.server_socket.bind((self.host, self.port))
#		self.server_socket.listen(self.max_clients)
#		self.server_socket.settimeout(self.timeout)
#
#		while True:
#			(client_socket, address) = self.server_socket.accept()
#			self.clients.append(client_socket)
#			ct = Thread(target=self.handle, args=(client_socket, ))
#			ct.start()

#try:
#	s = serial.Serial(port=ARDUINO_PORT, baudrate=9600)
#	s.close()
#except serial.SerialException:
#	print(f'No Arduino connection @/dev/{ARDUINO_PORT}. Exiting.')
#	sys.exit()

print(f'Listening for incoming connections.')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(None)
server_socket.bind((HOST, PORT))
server_socket.listen(1) # up to 1 connection(s)


while True:
	(client_socket, address) = server_socket.accept()
	ct = Thread(target = handle, args = (client_socket, ))
	ct.start()
