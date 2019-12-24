from pyfirmata import ArduinoNano


class Servo:
    def __init__(self, port, pin_number):
        board = ArduinoNano(port)
        self.servo = board.get_pin("d:{0}:s".format(pin_number))

    def write(self, degrees):
        assert 0 <= degrees <= 180, "degrees should within 0~180."
        try:
            self.servo.write(degrees)
        except IOError as e:
            print("Error: {0}".format(e))

    def stop(self):
        self.write(90)
