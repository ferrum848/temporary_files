import cv2, os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np


import utils, time
from base_viewer import BaseViewer
from main_function import main_function
from enum import Enum


class PhotoViewer(BaseViewer):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.mask = None


    #def enterEvent(self, event):
        #cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
        #start_point = (cursor_coord_x, cursor_coord_y)
        #print(start_point)


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.image is not None:
                current_color = self.colors[self.window.selection_criterion.currentText()].value
                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                target_pixel = self.image_slic[cursor_coord_y][cursor_coord_x]
                if target_pixel == 0:
                    current_image_slic = np.where(self.image_slic == target_pixel, self.image_slic, 777)
                    current_image_slic = np.where(current_image_slic != target_pixel, current_image_slic, 1)
                    current_image_slic = np.where(current_image_slic == 1, current_image_slic, 0)
                else:
                    current_image_slic = np.where(self.image_slic == target_pixel, self.image_slic, 0) // target_pixel
                temp_trimap = self.image_trimap[cursor_coord_y][cursor_coord_x]
                current_image_slic_3 = np.zeros(self.image.shape, dtype=np.uint8)

                if temp_trimap[0] != 255 or temp_trimap[1] != 255 or temp_trimap[2] != 255:
                    self.image_trimap = self.image_trimap.astype(np.int32)
                    for i in range(3):
                        self.image_trimap[:, :, i] = self.image_trimap[:, :, i] + current_image_slic * 255
                        self.image_trimap[:, :, i] = np.where(self.image_trimap[:, :, i] < 255,
                                                              self.image_trimap[:, :, i], 255)
                    self.image_trimap = self.image_trimap.astype(np.uint8)

                for i in range(3):
                    current_image_slic_3[:, :, i] = current_image_slic
                    self.image_trimap[:, :, i] = self.image_trimap[:, :, i] + current_image_slic

                color_mask = (current_color * current_image_slic_3).astype(np.uint8)
                self.image_trimap = self.image_trimap + color_mask
                trimap_for_stack = self.image_trimap.copy()
                self.stack.append(trimap_for_stack)
                if len(self.stack) > 10:
                    self.stack = self.stack[1:]
                self.updatePhoto(self.image_orig)
                self.update()

                #============================================================================================

                #image_bytes = self.image.tobytes()
                #shape0, shape1, shape2 = self.image.shape
                #result_image_bytes = main_function(image_bytes, cursor_coord_x, cursor_coord_y, wand, antialiasing, edges, threshold, mode, criterion, shape0, shape1, shape2)
                #self.image = np.frombuffer(result_image_bytes, dtype = np.uint8).reshape(self.image.shape)
                # ============================================================================================
                try:

                    self.start_photo.updatePhoto(self.image)
                    self.start_photo.update()
                    print('image ready!')
                except AttributeError:
                    pass



