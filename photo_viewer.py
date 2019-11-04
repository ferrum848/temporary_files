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


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.image is not None:
                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                start_point = (cursor_coord_x, cursor_coord_y)
                print(start_point)
                gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                #mask = np.zeros(self.image_orig.shape, dtype=np.uint8) # is it need?
                start_pixel = gray_image[cursor_coord_y][cursor_coord_x]
                threshold = self.window.brush_size_box.value()
                #step_pixels = self.window.step_pixels.value()
                if self.window.radio_image.isChecked():

                    gray_image = np.where(gray_image < start_pixel + threshold, gray_image, 0)
                    gray_image = np.where(gray_image > start_pixel - threshold, gray_image, 0)
                    gray_image = np.where(gray_image == 0, gray_image, 255)
                    contours = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    for contour in contours[1]:
                        min_left = (
                        min(contour, key=lambda x: x[0][0])[0][0], min(contour, key=lambda x: x[0][1])[0][1])
                        max_right = (
                        max(contour, key=lambda x: x[0][0])[0][0], max(contour, key=lambda x: x[0][1])[0][1])
                        if start_point[0] > min_left[0] and start_point[0] < max_right[0] and start_point[1] > min_left[
                            1] and start_point[1] < max_right[1]:
                            '''
                            epsilon = 0.005 * cv2.arcLength(contour, True)
                            approx = cv2.approxPolyDP(contour, epsilon, True)
                            '''
                            cv2.drawContours(self.image_orig, [contour], -1, (0, 255, 0), 1)
                            #cv2.fillPoly(self.image_orig, [contour], (0, 255, 0)) # is it need? may be option?
                            #cv2.fillPoly(mask, [contour], (255, 255, 255)) # is it need?

                    #cv2.imwrite(self.image_name + '_mask.png', mask) # is it need?
                    try:
                        self.start_photo.updatePhoto(self.image_orig)
                        self.start_photo.update()
                        print('image ready!')
                    except AttributeError:
                        pass


                else:
                    gray_image = np.where(gray_image < start_pixel + threshold, gray_image, 0)
                    gray_image = np.where(gray_image > start_pixel - threshold, gray_image, 0)
                    gray_image = np.where(gray_image == 0, gray_image, 255)
                    # for draw counturs
                    contours = cv2.findContours(gray_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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



