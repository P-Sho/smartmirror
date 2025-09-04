# webcam_thread/webcam.py

import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage

# webcam_thread/webcam.py
class WebcamThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage, object)

    def __init__(self, parent=None, rotate=True, mirror=True):
        super().__init__(parent)
        self.running = True
        self.rotate = rotate
        self.mirror = mirror

    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("Error: 웹캠을 열 수 없습니다.")
            self.running = False
            return

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                if self.rotate:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                if self.mirror:
                    frame = cv2.flip(frame, 1)

                h, w, ch = frame.shape
                qimg = QImage(frame.data, w, h, ch * w, QImage.Format_BGR888)
                self.change_pixmap_signal.emit(qimg, frame)

        self.cap.release()


    def stop(self):
        self.running = False
        self.wait()