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


    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            if self.image is not None:
                print(self.window.selection_criterion.currentText())
                if self.window.replace.isChecked():
                    self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                    self.window.clear()
                if self.window.add.isChecked():
                    self.image = self.test.copy()
                    if self.FLAG == 0:
                        self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                        self.FLAG += 1

                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                start_point = (cursor_coord_x, cursor_coord_y)

                if self.window.radio_image.isChecked():
                    #cv2.fillPoly(self.image_orig, [contour], (0, 255, 0)) # is it need? may be option?
                    contour = self.find_countur_of_threshold(start_point)
                    if self.window.substract.isChecked() and self.mask is not None:
                        self.window.clear()
                        mask_substract = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                        cv2.fillPoly(mask_substract, [contour], (1, 1, 1))
                        self.mask += mask_substract
                        self.mask = np.where(self.mask > 1, self.mask, 0)

                    elif self.window.intersect.isChecked() and self.mask is not None:
                        self.window.clear()
                        mask_substract = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                        cv2.fillPoly(mask_substract, [contour], (2, 2, 2))
                        self.mask += mask_substract
                        self.mask = np.where(self.mask < 2, self.mask, 0)
                        self.mask *= 255

                    elif self.mask is None:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setWindowTitle("Warning")
                        msg.setText("Please, choise the area on image!")
                        msg.exec_()

                    else:
                        cv2.fillPoly(self.mask, [contour], (255, 255, 255))

                else:
                    contours = self.find_all_counturs_of_threshold(start_point)
                    if self.window.substract.isChecked() and self.mask is not None:
                        self.window.clear()
                        mask_substract = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                        for contour in contours[1]:
                            cv2.fillPoly(mask_substract, [contour], (1, 1, 1))
                        self.mask += mask_substract
                        self.mask = np.where(self.mask > 1, self.mask, 0)

                    elif self.window.intersect.isChecked() and self.mask is not None:
                        self.window.clear()
                        mask_substract = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                        for contour in contours[1]:
                            cv2.fillPoly(mask_substract, [contour], (2, 2, 2))
                        self.mask += mask_substract
                        self.mask = np.where(self.mask < 2, self.mask, 0)
                        self.mask *= 255
                        cv2.imwrite('test.png', self.mask)

                    elif self.mask is None:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setWindowTitle("Warning")
                        msg.setText("Please, choise the area on image!")
                        msg.exec_()
                    else:
                        for contour in contours[1]:
                            cv2.fillPoly(self.mask, [contour], (255, 255, 255))
                        #cv2.drawContours(self.image, [contour], -1, (0, 255, 0), 1)

                contours_from_mask = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour_from_mask in contours_from_mask[1]:
                    if cv2.contourArea(contour_from_mask) > 15:
                        cv2.drawContours(self.image, [contour_from_mask], -1, (0, 255, 0), 1)
                    # for pixel -> color
                    #non_zero_coord = np.where(gray_image == 255)
                    #list_of_coord = list(zip(*non_zero_coord))
                    #for coord in list_of_coord:
                        #self.image_orig[coord[0]][coord[1]] = (0, 128, 64)
                    #cv2.imwrite(self.image_name + '_res.png', self.image_orig)
                try:
                    self.start_photo.updatePhoto(self.image)
                    self.start_photo.update()
                    print('image ready!')
                except AttributeError:
                    pass


    def find_countur_of_threshold(self, start_point):
        x, y = start_point
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
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
                return contour


    def find_all_counturs_of_threshold(self, start_point):
        x, y = start_point
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
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

