import tkinter
import cv2
from PIL import Image, ImageTk
import time
import imutils
from pyfirmata import ArduinoNano, util

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


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

        self.board = ArduinoNano('/dev/cu.usbserial-1430')
        self.servo = self.board.get_pin('d:9:s')

        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        print("Snapshot!")

    def move_camera(self):
        self.servo.write(120)

    def stop_camera(self):
        self.servo.write(90)

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


class VideoCapture:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source")

    def get_frame(self):
        ret, frame = self.vid.read()
        frame = imutils.resize(frame, width=500)
        return ret, frame

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(tkinter.Tk())
