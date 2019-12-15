import cv2

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import utils
import math
import skimage.segmentation as seg



class BaseViewer(QLabel):
    # Signals
    zoom_changed: pyqtSignal = pyqtSignal([tuple, list])
    #move_drag: pyqtSignal = pyqtSignal([tuple, list])

    def __init__(self, parent, window):
        super().__init__()
        self.window = window
        self.zoom = 1.0
        self.pos_00 = [0, 0]
        self.image = None
        self.image_orig = None
        self.res_image = None
        self.image_name = None
        self.start_photo = None
        self.image_slic = None



    def paintEvent(self, event):
        if self.image is not None:
            painter = QPainter(self)
            img_to_draw = self.get_visual_image3()
            if img_to_draw is None:
                self.count_hw_pos(-100, 0, 0)
                img_to_draw = self.get_visual_image3()
            pixmap = QPixmap(utils.cvImage2QImage(self.image))
            painter.drawPixmap(QRect(0, 0, img_to_draw.shape[1], img_to_draw.shape[0]), pixmap)

    '''
    def wheelEvent(self, event):
        if self.image_orig is not None:
            if -self.pos_00[0] + event.pos().y() > self.zoom_hw[0] or -self.pos_00[1] + event.pos().x() > self.zoom_hw[
                1]:
                return
            if event.angleDelta().y() > 0:
                self.count_hw_pos(0.5, event.pos().y(), event.pos().x())
            else:
                self.count_hw_pos(-0.5, event.pos().y(), event.pos().x())

            self.update()


    def normalize_pos00(self):
        if self.pos_00[0] > 0 or self.pos_00[1] > 0:
            self.pos_00 = [0, 0]
    '''


    def get_visual_image3(self):
        r0 = -self.pos_00[0]
        c0 = -self.pos_00[1]

        r1 = min(r0 + self.height(), self.zoom_hw[0])
        c1 = min(c0 + self.width(), self.zoom_hw[1])

        if r0 >= r1 - 100 or c0 >= c1 - 100:
            return None

        # final_size = (self.zoom_hw[1], self.zoom_hw[0])
        if self.res_image is None or self.res_image.shape[0] != self.zoom_hw[0] or self.res_image.shape[1] != self.zoom_hw[1]:
            part_size = (c1 - c0, r1 - r0)
            img_h, img_w = self.image.shape[:2]
            r0, r1  = round(r0 / self.zoom_hw[0] * img_h), round(r1 / self.zoom_hw[0] * img_h)
            c0, c1  = round(c0 / self.zoom_hw[1] * img_w), round(c1 / self.zoom_hw[1] * img_w)
            self.res_image = cv2.resize(self.image[r0:r1, c0:c1], part_size, interpolation=cv2.INTER_CUBIC)
            res_image = self.res_image
        else:
            res_image = self.res_image[r0:r1, c0:c1]
        #print('draw shape: ', self.image.shape)
        return res_image


    def count_hw_pos(self, delta_zoom, r, c):
        self.zoom += delta_zoom
        self.zoom += delta_zoom

        if self.zoom > 6:
            self.zoom = 6

        if self.zoom < 1:
            self.zoom = 1

        if self.zoom == 1:
            h_scale = float(self.image.shape[0]) / self.height()
            w_scale = float(self.image.shape[1]) / self.width()
            final_scale = max(h_scale, w_scale)
            h = math.floor(self.image.shape[0] / final_scale)
            w = math.floor(self.image.shape[1] / final_scale)
            self.pos_00 = [0, 0]
        else:
            h = math.floor(self.image.shape[0] * self.zoom)
            w = math.floor(self.image.shape[1] * self.zoom)

            img_abs_r = -self.pos_00[0] + r
            img_abs_c = -self.pos_00[1] + c

            img_rel_r = img_abs_r / self.zoom_hw[0]
            img_rel_c = img_abs_c / self.zoom_hw[1]

            new_img_abs_r = img_rel_r * h
            new_img_abs_c = img_rel_c * w

            widget_r0 = math.floor(new_img_abs_r - r)
            widget_c0 = math.floor(new_img_abs_c - c)

            self.pos_00[0] = -widget_r0
            self.pos_00[1] = -widget_c0
            self.normalize_pos00()

        self.zoom_hw = (h, w)
        self.zoom_changed.emit(self.zoom_hw, self.pos_00)


    def setPhoto(self, image):
        self.image = image
        self.image_orig = image
        self.background = np.zeros(self.image.shape, dtype=np.uint8)
        self.image_trimap = np.ones(self.image.shape, dtype=np.uint8) * 255
        self.contruct_visualization_image()
        self.count_hw_pos(-5, 0, 0) # init fields
        self.stack = [self.image_trimap.copy()]
        self.undo_key = 0
        self.during_stack_index = 0


    def updatePhoto(self, image):
        self.image = image
        self.contruct_visualization_image()
        self.count_hw_pos(-5, 0, 0)  # init fields


    def widget_to_img_pos(self, r, c):
        if self.zoom == 1:
            h_scale = float(self.image.shape[0]) / self.height()
            w_scale = float(self.image.shape[1]) / self.width()
            point_zoom = max(h_scale, w_scale)
            img_abs_r = -self.pos_00[0] + math.floor(r * point_zoom)
            img_abs_c = -self.pos_00[1] + math.floor(c * point_zoom)
        else:
            img_abs_r = -self.pos_00[0] + r
            img_abs_c = -self.pos_00[1] + c

            img_rel_r = img_abs_r / self.zoom_hw[0]
            img_rel_c = img_abs_c / self.zoom_hw[1]

            img_abs_r = math.floor(img_rel_r * self.image_orig.shape[0])
            img_abs_c = math.floor(img_rel_c * self.image_orig.shape[1])

        return img_abs_r, img_abs_c


    def contruct_visualization_image(self):
        if self.window.image.isChecked():
            trimap_overlay = ((self.image_trimap[:, :, 0] != 0) | (self.image_trimap[:, :, 1] != 0) | (
                            self.image_trimap[:, :, 2] != 0)).astype(np.float32) \
                                 * self.window.transp / 100.0
            trimap_overlay = np.repeat(np.expand_dims(trimap_overlay, 2), 3, axis=2)
            self.image = self.image * (1.0 - trimap_overlay) + trimap_overlay * self.image_trimap
            self.image = self.image.astype(np.uint8)
            if self.window.boundary.isChecked():
                self.image = cv2.bitwise_or(self.background, self.image)
        else:
            trimap_overlay = ((self.image_trimap[:, :, 0] != 0) | (self.image_trimap[:, :, 1] != 0) | (
                    self.image_trimap[:, :, 2] != 0)).astype(np.float32) \
                             * self.window.transp / 100.0
            trimap_overlay = np.repeat(np.expand_dims(trimap_overlay, 2), 3, axis=2)
            self.image = self.background * (1.0 - trimap_overlay) + trimap_overlay * self.image_trimap
            self.image = self.image.astype(np.uint8)


    def boundary(self):
        self.background = np.zeros(self.image.shape, dtype=np.uint8)
        if self.window.denoise.isChecked():
            image = cv2.medianBlur(self.image_orig, 25)
        else:
            image = self.image_orig
        self.image_slic = seg.slic(image, n_segments=self.window.number_of_parts) * 255 // self.window.number_of_parts
        boundaries = seg.find_boundaries(self.image_slic, mode='outer').astype(np.uint8) * 255
        for i in range(3):
            self.background[:, :, i] = boundaries


    def save_mask(self, save_path):
        try:
            if self.image_trimap:
                cv2.imwrite(save_path, self.image_trimap)
        except AttributeError:
            pass


    def undo(self):
        if self.undo_key + 1 < len(self.stack):
            self.during_stack_index = len(self.stack) - 2 - self.undo_key
            self.image_trimap = self.stack[self.during_stack_index]
            self.undo_key += 1
            self.updatePhoto(self.image_orig)
            self.update()


    def redo(self):
        if self.undo_key >= -1 and self.during_stack_index + 1 < len(self.stack):
            self.image_trimap = self.stack[self.during_stack_index + 1]
            self.during_stack_index += 1
            self.undo_key -= 1
            self.updatePhoto(self.image_orig)
            self.update()



