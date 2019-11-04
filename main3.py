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

        self.radio_image = QRadioButton("One object")
        self.radio_image.setChecked(True)
        self.radio_image.setEnabled(True)
        self.radio_image_all = QRadioButton("All objects")
        self.radio_image_all.setChecked(False)
        self.radio_image_all.setEnabled(True)

        self.brush_size_box = QSpinBox()
        self.brush_size_box.setMinimum(1)
        self.brush_size_box.setMaximum(255)
        self.brush_size_box.setValue(30)
        self.threshold = QLabel("    Threshold:")


        self.btnClear = QToolButton()
        self.btnClear.setText('Clear')
        self.btnClear.clicked.connect(self.clear)
        '''
        test_layout = QHBoxLayout()
        self.test = QRadioButton("test")
        self.test.setChecked(True)
        self.test.setEnabled(True)
        test_layout.addWidget(self.test)
        #test_group = QGroupBox()
        #test_group.setLayout(test_layout)
        '''


        #instruments panel
        instrument_layout = QHBoxLayout()
        instrument_layout.addWidget(self.btnLoad)
        instrument_layout.addWidget(self.radio_image)
        instrument_layout.addWidget(self.radio_image_all)
        instrument_layout.addWidget(self.threshold)
        instrument_layout.addWidget(self.brush_size_box)
        instrument_layout.addWidget(self.btnClear)
        #instrument_layout.addLayout(test_layout)
        instrument_layout.addStretch(10000) #-------------------------------------  button place


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
