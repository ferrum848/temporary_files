import cv2, os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np


import utils, time
from base_viewer import BaseViewer
from main_function import main_function


import grpc
import wand_pb2
import wand_pb2_grpc



class PhotoViewer(BaseViewer):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.mask = None


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.image is not None:
                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                if self.mask is None or self.FLAG == 0:
                    self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                    self.FLAG = 1
                #============================================================================================
                if self.window.radio_image.isChecked():
                    wand = 1
                else:
                    wand = 0
                if self.window.smooth_edges.isChecked():
                    antialiasing = 1
                else:
                    antialiasing = 0
                edges = self.window.feather_edges.value()
                threshold = self.window.threshold.value()
                if self.window.replace.isChecked():
                    mode = 1
                    self.window.clear()
                    self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                if self.window.add.isChecked():
                    mode = 2
                    self.image = self.image_orig.copy()
                if self.window.substract.isChecked():
                    mode = 3
                    self.window.clear()
                    self.FLAG = 1
                if self.window.intersect.isChecked():
                    mode = 4
                    self.window.clear()
                    self.FLAG = 1
                criterion = self.window.selection_criterion.currentText()
                image_bytes = self.image.tobytes()
                shape0, shape1, shape2 = self.image.shape
                mask_bytes = self.mask.tobytes()

                channel = grpc.insecure_channel('localhost:50051')
                stub = wand_pb2_grpc.magic_wandStub(channel)
                response = wand_pb2.Mask(image = image_bytes, x = cursor_coord_x, y = cursor_coord_y, wand = wand, antialiasing=antialiasing, edges=edges, threshold=threshold, mode=mode, criterion=criterion, shape0=shape0, shape1=shape1, shape2=shape2, mask=mask_bytes)
                result_image_bytes = stub.find_mask(response)
                self.image = np.frombuffer(result_image_bytes.image, dtype=np.uint8).reshape(self.image.shape)
                self.mask = np.frombuffer(result_image_bytes.mask, dtype=np.uint8).reshape(self.mask.shape)
                # ============================================================================================
                try:
                    self.start_photo.updatePhoto(self.image)
                    self.start_photo.update()
                    print('image ready!')
                except AttributeError:
                    pass
