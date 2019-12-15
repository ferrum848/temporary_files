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
                class Color(Enum):
                    background = (255, 255, 255)
                    green = (0, 255, 0)
                    blue = (255, 0, 0)
                    yellow = (0, 255, 255)
                    black = (1, 1, 1)
                    red = (0, 0, 255)
                for color in Color:
                    if color.name == self.window.selection_criterion.currentText():
                        current_color = color.value
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



    '''
    def find_countur_of_threshold(self, start_point, gray_image):
        x, y = start_point
        start_pixel = gray_image[y][x]
        threshold = self.window.threshold.value()
        feather_edges = self.window.feather_edges.value()
        if feather_edges % 2 == 0:
            feather_edges += 1
        gray_image = cv2.medianBlur(gray_image, feather_edges)
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
                target_contour = contour
        target_mask = np.zeros(gray_image.shape, dtype=np.uint8)
        cv2.fillPoly(target_mask, np.int32([target_contour]), (127, 127, 127))
        result_mask = target_mask + gray_image
        result_mask = np.where(result_mask != 255, result_mask, 0)
        result_mask = np.where(result_mask != 127, result_mask, 0)
        _, contours, hierarchy = cv2.findContours(result_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(self.image, contours, -1, (0, 255, 0), 1, cv2.LINE_AA, hierarchy, 2)
        return contours, target_contour



    def find_all_counturs_of_threshold(self, start_point, gray_image):
        x, y = start_point
        start_pixel = gray_image[y][x]
        threshold = self.window.threshold.value()
        feather_edges = self.window.feather_edges.value()
        if feather_edges % 2 == 0:
            feather_edges += 1
        gray_image = cv2.medianBlur(gray_image, feather_edges)
        gray_image = np.where(gray_image < start_pixel + threshold, gray_image, 0)
        gray_image = np.where(gray_image > start_pixel - threshold, gray_image, 0)
        gray_image = np.where(gray_image == 0, gray_image, 255)
        contours = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours


    def choise_selection_mask(self):
        selection_criterion = self.window.selection_criterion.currentText()
        if selection_criterion == 'composite':
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        elif selection_criterion == 'red':
            gray_image = self.image[:, :, 0]
        elif selection_criterion == 'green':
            gray_image = self.image[:, :, 1]
        elif selection_criterion == 'blue':
            gray_image = self.image[:, :, 2]
        else:
            temp_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HLS)
            if selection_criterion == 'hue':
                gray_image = temp_image[:, :, 0]
            elif selection_criterion == 'lightness':
                gray_image = temp_image[:, :, 1]
            elif selection_criterion == 'saturation':
                gray_image = temp_image[:, :, 2]
        return gray_image
    '''





