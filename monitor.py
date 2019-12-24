import tkinter
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk

from human_list import HumanList
from servo import *
from video_capture import VideoCapture

CASCADE_PATH = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(CASCADE_PATH)

class App:
    def __init__(self, window, servo):
        self.window = window
        self.window.title(u"Monitor")

        self.canvas = tkinter.Canvas(window, width=500, height=400)
        self.canvas.grid(columnspan=4)

        self.edit_box = tkinter.Entry(window)
        self.edit_box.grid(row=1, column=0)

        self.btn_snapshot = tkinter.Button(window, text="Write", command=self.write_to_servo)
        self.btn_snapshot.grid(row=1, column=1)

        self.btn_move = tkinter.Button(window, text="MOVE", command=self.move_camera)
        self.btn_move.grid(row=1, column=2)

        self.btn_stop = tkinter.Button(window, text="STOP", command=self.stop_camera)
        self.btn_stop.grid(row=1, column=3)

        self.human_list = HumanList(window)

        self.vid = VideoCapture()
        self.servo = servo

        self.delay = 15
        self.update()

        self.window.mainloop()

    def write_to_servo(self):
        try:
            degrees = int(self.edit_box.get())
            self.servo.write(degrees)
        except ValueError:
            print("Enter number.")


    def move_camera(self):
        self.servo.write(120)

    def stop_camera(self):
        self.servo.stop()

    def update(self):
        ret, frame = self.vid.get_frame()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.human_list.update(faces)

        self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)

    def __del__(self):
        self.servo.exit()
        self.vid.exit()


App(tkinter.Tk(), DummyServo())
