from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import utils

from double_viewer import DoubleViewer



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.image_path = None
        self.transp = 50

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
            self.viewer.setPhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def reduce_transp(self):
        if self.transp < 100:
            self.transp += 10
            self.viewer.setPhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def increase_transp(self):
        if self.transp > 0:
            self.transp -= 10
            self.viewer.setPhoto(utils.load_image(self.image_path))
            self.viewer.update()


    def show_boundary(self):
        pass


    def reduce_bound(self):
        pass

    def increase_bound(self):
        pass


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
import cv2, time

start = time.time()
img = cv2.imread('IMG_1942.jpeg')
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (738, 384, 932, 612)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
#cv2.rectangle(img, (738, 384), (932, 612), (255, 255, 255), 2)
cv2.imwrite('test.png', img)
print(time.time() - start)

import numpy as np
import cv2, time
img = cv2.imread("IMG_1942.jpeg")
imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
print(imgHLS.shape)
Lchannel = imgHLS[:,:,1]
cv2.imwrite('light.png', Lchannel)
Hchannel = imgHLS[:,:,0]
cv2.imwrite('hue.png', Hchannel)
Schannel = imgHLS[:,:,2]
cv2.imwrite('satur.png', Schannel)


import numpy as np
import cv2

img = cv2.imread("IMG_1942.jpeg")
print(img.shape, img.dtype)
b = img.tobytes()
res = np.frombuffer(b, dtype = np.uint8)
res = res.reshape(800, 1067, 3)
print(res.shape)
print(np.array_equal(res, img))
'''