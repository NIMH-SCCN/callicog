from marmobox_IO import MarmoboxIO

box = MarmoboxIO('/dev/ttyACM0')
box.connect()
box.correct()
box.disconnect()