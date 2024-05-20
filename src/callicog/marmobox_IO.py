import serial


class MarmoboxIO:
    """ Encapsulates the interfaces and responsibilities of the reward module.
    """

    def __init__(self, com_port, dummy=False):
        self.board = None
        self.port = com_port
        self.dummy = dummy

    def connect(self):
        if not self.dummy:
            if not self.board:
                self.board = serial.Serial(
                    port='/dev/' + self.port,
                    baudrate=9600,
                )

    def disconnect(self):
        if self.board:
            self.board.close()
            self.board = None

    def send(self, byte_command):
        if self.board:
            self.board.write(byte_command)

    def correct(self):
        self.send(b'C')

    def incorrect(self):
        self.send(b'I')

    def flush():
        """ Run the reward module pump indefinitely. Useful for flushing the
        lines.  Terminate using Ctrl-c.
        """
        try:
            self.connect()
            time.sleep(2)
            print('Flushing reward module. Press Ctrl+C to stop.')
            while True:
                self.correct()
                time.sleep(1)
        except KeyboardInterrupt:
            # print('Stopped gracefully!')
            pass
        finally:
            self.disconnect()
