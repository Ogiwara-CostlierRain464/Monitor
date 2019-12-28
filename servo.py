import logging

from pyfirmata import ArduinoNano
import threading


class Servo:
    # 0.4s, +10 is 90degrees.
    delay_time = 0.4

    def __init__(self, port_number, pin_number, base_degrees):
        self.base_degrees = base_degrees
        self.board = ArduinoNano("/dev/cu.usbserial-{0}".format(port_number))
        self.servo = self.board.get_pin("d:{0}:s".format(pin_number))
        self.moving = False

        self.stop()

    def write(self, degrees):
        assert 0 <= degrees <= 180, "degrees should within 0~180."
        try:
            self.servo.write(degrees)
        except IOError as e:
            print("Error: {0}".format(e))
        except:
            print("SOMETHING??")

    def stop(self):
        self.write(self.base_degrees)

    def exit(self):
        self.board.exit()

    def turn_left(self):
        if self.moving:
            print("WAIT")
            return

        self.write(self.base_degrees + 10)
        print("TURN LEFT")
        self.moving = True
        threading.Timer(self.delay_time, self.__moving_and_stop).start()

    def turn_right(self):
        if self.moving:
            print("WAIT")
            return

        self.write(self.base_degrees - 10)
        print("TURN RIGHT")
        self.moving = True
        threading.Timer(self.delay_time, self.__moving_and_stop).start()

    def __moving_and_stop(self):
        self.moving = False
        self.stop()

    def rotate(self, degrees):
        # Rotate specified degrees.
        # Have to wait until rotate finish.
        # Use timer to cancel operation while rotating.
        pass


class DummyServo():
    """
    Dummy class used for debugging.
    """

    def write(self, degrees):
        print("Write {0}".format(degrees))

    def stop(self):
        print("Stop")

    def exit(self):
        print("Exit")

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def rotate(self, degrees):
        pass
