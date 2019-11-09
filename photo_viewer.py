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
                if self.window.replace.isChecked():
                    self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                    self.window.clear()
                if self.window.add.isChecked():
                    self.image = self.image_orig.copy()
                    if self.FLAG == 0:
                        self.mask = np.zeros((self.image.shape[0], self.image.shape[1]), dtype=np.uint8)
                        self.FLAG += 1

                cursor_coord_x, cursor_coord_y = self.widget_to_img_pos(event.pos().x(), event.pos().y())
                start_point = (cursor_coord_x, cursor_coord_y)
                gray_image = self.choise_selection_mask()
                if self.window.radio_image.isChecked():
                    all_contours, contour = self.find_countur_of_threshold(start_point, gray_image)
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
                        for cnt in all_contours:
                            if len(cnt) == len(contour):
                                cv2.fillPoly(self.mask, [cnt], (255, 255, 255))
                            else:
                                cv2.fillPoly(self.mask, [cnt], (0, 0, 0))
                        #cv2.imwrite('massss.png', self.mask)

                else:
                    contours = self.find_all_counturs_of_threshold(start_point, gray_image)
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

                    elif self.mask is None:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setWindowTitle("Warning")
                        msg.setText("Please, choise the area on image!")
                        msg.exec_()
                    else:
                        for contour in contours[1]:
                            cv2.fillPoly(self.mask, np.int32([contour]), (255, 255, 255))

                contours_from_mask = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for contour_from_mask in contours_from_mask[1]:
                    if self.window.smooth_edges.isChecked():
                        if cv2.contourArea(contour_from_mask) > 20:
                            cv2.drawContours(self.image, [contour_from_mask], -1, (0, 255, 0), 1)
                    else:
                        cv2.drawContours(self.image, [contour_from_mask], -1, (0, 255, 0), 1)
                try:
                    self.start_photo.updatePhoto(self.image)
                    self.start_photo.update()
                    print('image ready!')
                except AttributeError:
                    pass


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

