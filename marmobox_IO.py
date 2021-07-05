import serial
import time

class MarmoboxIO:
	def __init__(self, COM_PORT):
		self.board = None
		self.port = COM_PORT

	def connect(self):
		self.board = serial.Serial(port='/dev/' + self.port, baudrate=9600)

	def disconnect(self):
		if self.board:
			self.board.close()

	def send(self, byte_command):
		self.board.write(byte_command)

	def correct(self):
		self.send(b'C')

	def incorrect(self):
		self.send(b'I')