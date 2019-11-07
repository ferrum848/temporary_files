import cv2, os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np

import utils, time
from base_viewer import BaseViewer




class PhotoViewer(BaseViewer):

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.mask = None
        self.FLAG = 0


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.image is not None:
                #start_image = self.image.copy()
                if self.window.replace.isChecked():
                    self.window.clear()
                if self.window.add.isChecked():
                    #self.image_orig = start_image.copy()
                    self.image = self.test.copy()
                    cv2.imwrite('start.png', self.image)
                    if self.FLAG == 0:
                        self.mask = np.zeros((self.image_orig.shape[0], self.image_orig.shape[1]), dtype=np.uint8)
                        self.FLAG += 1

                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                start_point = (cursor_coord_x, cursor_coord_y)
                gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                #mask = np.zeros(self.image_orig.shape, dtype=np.uint8) # is it need?
                start_pixel = gray_image[cursor_coord_y][cursor_coord_x]
                threshold = self.window.threshold.value()
                feather_edges = self.window.feather_edges.value()
                if feather_edges % 2 == 0:
                    feather_edges += 1
                gray_image = cv2.medianBlur(gray_image, feather_edges)
                gray_image = np.where(gray_image < start_pixel + threshold, gray_image, 0)
                gray_image = np.where(gray_image > start_pixel - threshold, gray_image, 0)
                gray_image = np.where(gray_image == 0, gray_image, 255)
                contours = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if self.window.radio_image.isChecked():

                    for contour in contours[1]:
                        min_left = (
                        min(contour, key=lambda x: x[0][0])[0][0], min(contour, key=lambda x: x[0][1])[0][1])
                        max_right = (
                        max(contour, key=lambda x: x[0][0])[0][0], max(contour, key=lambda x: x[0][1])[0][1])
                        if start_point[0] > min_left[0] and start_point[0] < max_right[0] and start_point[1] > min_left[
                            1] and start_point[1] < max_right[1]:

                            #cv2.drawContours(self.image_orig, [contour], -1, (0, 255, 0), 1)
                            #cv2.fillPoly(self.image_orig, [contour], (0, 255, 0)) # is it need? may be option?
                            cv2.fillPoly(self.mask, [contour], (255, 255, 255))
                            test = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                            for ccc in test[1]:
                                cv2.drawContours(self.image, [ccc], -1, (0, 255, 0), 1)

                    cv2.imwrite('ask.png', self.mask)
                    cv2.imwrite('test.png', self.image)
                    cv2.imwrite('test_self.png', self.test)
                    #cv2.imwrite('test_image.png', self.image)
                    try:
                        self.start_photo.updatePhoto(self.image)
                        self.start_photo.update()
                        print('image ready!')
                    except AttributeError:
                        pass


                else:
                    for contour in contours[1]:
                        cv2.drawContours(self.image_orig, [contour], -1, (0, 255, 0), 1)

                    #cv2.imwrite(self.image_name + '_mask.png', gray_image * 255) # is it need?
                    # for pixel -> color
                    #non_zero_coord = np.where(gray_image == 255)
                    #list_of_coord = list(zip(*non_zero_coord))
                    #for coord in list_of_coord:
                        #self.image_orig[coord[0]][coord[1]] = (0, 128, 64)
                    #cv2.imwrite(self.image_name + '_res.png', self.image_orig)
                    self.start_photo.updatePhoto(self.image_orig)
                    self.start_photo.update()
                    print('image ready!')



