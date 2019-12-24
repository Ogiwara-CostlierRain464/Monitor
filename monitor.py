import tkinter
import cv2
from PIL import Image, ImageTk
import time
import imutils
from pyfirmata import ArduinoNano, util
from video_capture import VideoCapture

CASCADE_PATH = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(CASCADE_PATH)


class App:
    def __init__(self, window):
        self.window = window
        self.vid = VideoCapture()
        self.canvas = tkinter.Canvas(window, width=600, height=600)
        self.canvas.pack()

        self.btn_snapshot = tkinter.Button(window, text="Snap", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_move = tkinter.Button(window, text="MOVE", width=50, command=self.move_camera)
        self.btn_move.pack(anchor=tkinter.CENTER, expand=True)

        self.btn_stop = tkinter.Button(window, text="STOP", width=50, command=self.stop_camera)
        self.btn_stop.pack(anchor=tkinter.CENTER, expand=True)

        self.board = ArduinoNano('/dev/cu.usbserial-1410')
        self.servo = self.board.get_pin('d:9:s')

        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        print("Snapshot!")

    def move_camera(self):
        try:
            self.servo.write(120)
        except IOError as e:
            print("Error: {0}".format(e))

    def stop_camera(self):
        try:
            self.servo.write(90)
        except IOError as e:
            print("Error: {0}".format(e))

    def update(self):
        ret, frame = self.vid.get_frame()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def __del__(self):
        self.board.exit()


App(tkinter.Tk())
