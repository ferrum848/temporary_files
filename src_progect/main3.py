from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import utils

from double_viewer import DoubleViewer



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.image_path = None
        self.transp = 10
        self.number_of_parts = 48

        self.viewer = DoubleViewer(self)
        self.viewer.setUpdatesEnabled(True)

        # 'Load image' button
        self.btnLoad = QToolButton()
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)

        self.btnClear = QToolButton()
        self.btnClear.setText('Clear')
        self.btnClear.clicked.connect(self.clear)

        self.radio_image = QRadioButton("One object")
        self.radio_image.setChecked(True)
        self.radio_image.setEnabled(True)
        self.radio_image_all = QRadioButton("All objects")
        self.radio_image_all.setChecked(False)
        self.radio_image_all.setEnabled(True)

        select_wand = QHBoxLayout()
        select_wand.addWidget(self.radio_image)
        select_wand.addWidget(self.radio_image_all)
        zoom_group = QGroupBox("Zoom")
        zoom_group.setLayout(select_wand)

        self.show_denoise = QLabel("Denoise:")
        self.denoise = QCheckBox()
        self.denoise.setChecked(True)

        line_00 = QFrame()
        line_00.setFrameShape(QFrame.VLine)

        self.reduce_boundary = QToolButton()
        self.reduce_boundary.setText('-')
        self.reduce_boundary.clicked.connect(self.reduce_bound)

        self.boundary = QPushButton('Boundary', self)
        self.boundary.setCheckable(True)
        self.boundary.setChecked(False)
        self.boundary.clicked[bool].connect(self.show_boundary)

        self.increase_boundary = QToolButton()
        self.increase_boundary.setText('+')
        self.increase_boundary.clicked.connect(self.increase_bound)

        line_01 = QFrame()
        line_01.setFrameShape(QFrame.VLine)

        self.reduce_transparency = QToolButton()
        self.reduce_transparency.setText('-')
        self.reduce_transparency.clicked.connect(self.reduce_transp)

        self.image = QPushButton('Image', self)
        self.image.setCheckable(True)
        self.image.setChecked(True)
        self.image.clicked[bool].connect(self.show_image)

        self.increase_transparency = QToolButton()
        self.increase_transparency.setText('+')
        self.increase_transparency.clicked.connect(self.increase_transp)

        line_02 = QFrame()
        line_02.setFrameShape(QFrame.VLine)


        tool_options = QHBoxLayout()
        tool_options.addWidget(self.show_denoise)
        tool_options.addWidget(self.denoise)
        tool_options.addWidget(line_00)
        tool_options.addWidget(self.reduce_boundary)
        tool_options.addWidget(self.boundary)
        tool_options.addWidget(self.increase_boundary)
        tool_options.addWidget(line_01)
        tool_options.addWidget(self.reduce_transparency)
        tool_options.addWidget(self.image)
        tool_options.addWidget(self.increase_transparency)
        tool_options.addWidget(line_02)
        tool_options.addWidget(self.btnClear)

        options_group = QGroupBox("Options")
        options_group.setLayout(tool_options)

        undo = QToolButton()
        undo.setText('Undo')
        undo.clicked.connect(self.undo)
        redo = QToolButton()
        redo.setText('Redo')
        redo.clicked.connect(self.redo)

        undo_redo = QHBoxLayout()
        undo_redo.addWidget(undo)
        undo_redo.addWidget(redo)
        edit_group = QGroupBox("Edit")
        edit_group.setLayout(undo_redo)

        self.selection_criterion = QComboBox(self)
        self.selection_criterion.addItems(['background', 'green', 'blue', 'yellow', 'black', 'red'])


        color_option = QHBoxLayout()
        color_option.addWidget(self.selection_criterion)
        color_group = QGroupBox("Color option")
        color_group.setLayout(color_option)


        # instruments panel
        instrument_layout = QHBoxLayout()
        instrument_layout.addWidget(zoom_group)
        instrument_layout.addWidget(options_group)
        instrument_layout.addWidget(edit_group)
        instrument_layout.addWidget(color_group)
        instrument_layout.addWidget(self.btnLoad)
        instrument_layout.addStretch(10000)

        # Arrange layout
        VBlayout = QVBoxLayout()
        VBlayout.addLayout(instrument_layout)
        VBlayout.addWidget(self.viewer)

        self.setLayout(VBlayout)


    def loadImage(self):
        new_image_path = QFileDialog.getOpenFileName(self, "Pick an image")[0]
        self.image_path = new_image_path
        if utils.check_image_path(str(new_image_path)):
            #image_name = new_image_path.split('/')[-1].split('.')[0]
            self.viewer.setPhoto(utils.load_image(new_image_path))
            self.viewer.boundary()
            self.viewer.update()

    def clear(self):
        if self.image_path is None:
            image_path = QMessageBox()
            image_path.setIcon(QMessageBox.Critical)
            image_path.setWindowTitle("Warning")
            image_path.setText("Please, choise the image!")
            image_path.exec_()
        else:
            self.viewer.setPhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def show_image(self):
        if self.image_path is None:
            pass
        else:
            self.viewer.updatePhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def reduce_transp(self):
        if self.transp < 100:
            self.transp += 10
            self.viewer.updatePhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def increase_transp(self):
        if self.transp > 0:
            self.transp -= 10
            self.viewer.updatePhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def show_boundary(self):
        if self.image_path is None:
            pass
        else:
            self.viewer.updatePhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def reduce_bound(self):
        if self.number_of_parts > 1:
                self.number_of_parts //= 2
                self.viewer.boundary()
                self.show_boundary()


    def increase_bound(self):
        self.number_of_parts *= 2
        self.viewer.boundary()
        self.show_boundary()


    def undo(self):
        pass

    def redo(self):
        pass




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())


'''
import numpy as np
import cv2
import skimage.segmentation as seg

image = cv2.imread('1.jpeg')
image = cv2.medianBlur(image, 25)
number_of_segments = 24
image_slic = seg.slic(image, n_segments = number_of_segments) * 255 // number_of_segments
print(np.unique(image_slic))
cv2.imwrite('test.png', image_slic)
boundaries = seg.find_boundaries(image_slic,  mode='outer').astype(np.uint8) * 255
print(np.unique(boundaries), boundaries.shape)
cv2.imwrite('boundaries.png', boundaries)

'''


