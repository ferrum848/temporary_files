from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from photo_viewer import PhotoViewer


class DoubleViewer(QLabel):

    def __init__(self, window):
        super().__init__(window)
        self.left_viewer = PhotoViewer(self, window)

        # Debug styling
        self.setStyleSheet("border: 2px solid gray")
        self.left_viewer.setStyleSheet("border: 2px solid blue")
        self.left_viewer.setUpdatesEnabled(True)

        layout = QHBoxLayout(self)
        layout.addWidget(self.left_viewer)
        self.setLayout(layout)


    def setPhoto(self, image, image_name = None):
        self.left_viewer.setPhoto(image, image_name, self.left_viewer)
        self.update()



