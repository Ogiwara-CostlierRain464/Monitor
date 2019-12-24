import cv2
import imutils


class VideoCapture:
    """
    Handles getting frames from Web camera.
    """
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
