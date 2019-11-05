from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import utils

from double_viewer import DoubleViewer



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.image_path = None

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
        wand_group = QGroupBox("Select wand")
        wand_group.setLayout(select_wand)

        # tools group
        self.show_feather_edges = QLabel("Feather edges:")

        #line_00 = QFrame()
        #line_00.setFrameShape(QFrame.VLine)

        #self.show_smooth_edges = QLabel("Smooth edges:")

        #self.smooth_edges = QCheckBox()

        line_01 = QFrame()
        line_01.setFrameShape(QFrame.VLine)

        self.threshold = QSpinBox()
        self.threshold.setMinimum(1)
        self.threshold.setMaximum(255)
        self.threshold.setValue(30)

        threshold = QHBoxLayout()
        threshold.addWidget(QLabel("Threshold: "))
        threshold.addWidget(self.threshold)

        line_02 = QFrame()
        line_02.setFrameShape(QFrame.VLine)

        self.replace = QRadioButton("Replace")
        self.add = QRadioButton("Add")
        self.add.setChecked(True)
        self.substract = QRadioButton("Subtract")
        self.intersect = QRadioButton("Intersect")

        fuzzy_modes = QHBoxLayout()
        fuzzy_modes.addWidget(QLabel("Mode: "))
        fuzzy_modes.addWidget(self.replace)
        fuzzy_modes.addWidget(self.add)
        fuzzy_modes.addWidget(self.substract)
        fuzzy_modes.addWidget(self.intersect)

        line_03 = QFrame()
        line_03.setFrameShape(QFrame.VLine)


        self.feather_edges = QSpinBox()
        self.feather_edges.setMinimum(1)
        self.feather_edges.setMaximum(33)
        self.feather_edges.setValue(1)
        self.feather_edges.setDisabled(True)
        self.feather_edges.setDisabled(False)


        tool_options = QHBoxLayout()
        #trimap_layout.addWidget(self.show_smooth_edges)
        #trimap_layout.addWidget(self.smooth_edges)
        #trimap_layout.addWidget(line_00)
        tool_options.addWidget(self.show_feather_edges)
        tool_options.addWidget(self.feather_edges)
        tool_options.addWidget(line_01)
        tool_options.addLayout(threshold)
        tool_options.addWidget(line_02)
        tool_options.addLayout(fuzzy_modes)
        tool_options.addWidget(line_03)
        tool_options.addWidget(self.btnClear)

        trimap_group = QGroupBox("Tool options")
        trimap_group.setLayout(tool_options)


        self.selection_criterion = QComboBox(self)
        self.selection_criterion.addItems(['composite', 'green', 'red', 'blue', 'hue', 'saturation', 'value'])


        predict_layout = QHBoxLayout()
        predict_layout.addWidget(self.selection_criterion)
        predict_group = QGroupBox("Selection criterion")
        predict_group.setLayout(predict_layout)


        # instruments panel
        instrument_layout = QHBoxLayout()
        instrument_layout.addWidget(wand_group)
        instrument_layout.addWidget(trimap_group)
        instrument_layout.addWidget(predict_group)
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
        self.viewer.setPhoto(utils.load_image(self.image_path))
        self.viewer.update()




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
'''
