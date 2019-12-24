from pyfirmata import ArduinoNano


class Servo:
    def __init__(self, port, pin_number):
        self.board = ArduinoNano(port)
        self.servo = self.board.get_pin("d:{0}:s".format(pin_number))

    def write(self, degrees):
        assert 0 <= degrees <= 180, "degrees should within 0~180."
        try:
            self.servo.write(degrees)
        except IOError as e:
            print("Error: {0}".format(e))

    def stop(self):
        self.write(90)

    def exit(self):
        self.board.exit()


class DummyServo:
    """
    Dummy class used for debugging.
    """
    def write(self):
        pass

    def stop(self):
        pass

    def exit(self):
        pass
