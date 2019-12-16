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


    def setPhoto(self, image):
        self.left_viewer.setPhoto(image)
        self.update()

    def boundary(self):
        self.left_viewer.boundary()


    def updatePhoto(self, image):
        self.left_viewer.updatePhoto(image)
        self.update()


    def save_mask(self, save_path):
        self.left_viewer.save_mask(save_path)


    def undo(self):
        self.left_viewer.undo()


    def redo(self):
        self.left_viewer.redo()


    def change_color(self):
        self.left_viewer.change_color()





