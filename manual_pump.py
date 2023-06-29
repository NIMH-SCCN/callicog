import serial
import time

box = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
time.sleep(2)
try:
    while True:
        box.write(b'C')
        time.sleep(1)
except KeyboardInterrupt:
    print('Stopped gracefully!')

box.close()
