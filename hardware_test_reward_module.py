# Hardware test for reward subsystem.
#
# To run this test:
#
#    1. plug in the reward subsystem directly into the computer you're running the test from, then
#    2. activate the virtual environment, and finally
#    3. run:
#
#         `pytest --capture=no callicog/hardware_test_reward_module.py`
#

from marmobox_IO import MarmoboxIO
import time


def test_direct_correct():
    import serial
    device_location = '/dev/ttyACM0'
    try:
        device = serial.Serial(device_location, baudrate=9600)
        time.sleep(2)
        for i in range(5):
            time.sleep(2)
            correct = device.write(b'C')
            print("wrote C")
    finally:
        device.close()
        print("closed")


def test_direct_incorrect():
    import serial
    device_location = '/dev/ttyACM0'
    try:
        device = serial.Serial(device_location, baudrate=9600)
        time.sleep(2)
        for i in range(5):
            time.sleep(2)
            incorrect = device.write(b'I')
            print("wrote I")
    finally:
        device.close()
        print("closed")


def test_correct():
    port = 'ttyACM0'
    box = MarmoboxIO(port)
    try:
        box.connect()
        time.sleep(2)
        for i in range(3):
            time.sleep(2)
            box.correct()
    finally:
        box.disconnect()


def test_incorrect():
    port = 'ttyACM0'
    box = MarmoboxIO(port)
    try:
        box.connect()
        time.sleep(2)
        for i in range(3):
            time.sleep(2)
            box.incorrect()
    finally:
        box.disconnect()
