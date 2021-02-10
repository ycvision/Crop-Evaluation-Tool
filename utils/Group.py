from PyQt5 import QtWidgets, QtGui, QtCore
from typing import List


class Group:
    def __init__(self, gv_crop: QtWidgets.QGraphicsView, rbs: List[QtWidgets.QRadioButton], label: QtWidgets.QLabel):
        self.gvCrop = gv_crop
        self.rbs = rbs
        self.label = label
        self._btnGroup = QtWidgets.QButtonGroup()
        self._set_up_image_window()
        self._set_up_radio_buttons()

    def __getitem__(self, item):
        pass

    def _set_up_image_window(self):
        self.gvCrop.setRenderHint(QtGui.QPainter.Antialiasing)
        self.gvCrop.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gvCrop.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def _set_up_radio_buttons(self):
        self._btnGroup.setExclusive(True)
        self._btnGroup.addButton(self.rbs[0])
        self._btnGroup.addButton(self.rbs[1])

    def clear_radio_buttons(self):
        self._btnGroup.setExclusive(False)
        self.rbs[0].setChecked(False)
        self.rbs[1].setChecked(False)
        self._btnGroup.setExclusive(True)

    def at_least_one_checked(self):
        return self.rbs[0].isChecked() or self.rbs[1].isChecked()

    def display(self, cvImg):
        height, width, channel = cvImg.shape
        qImg = QtGui.QImage(cvImg.data, width, height, 3 * width, QtGui.QImage.Format_RGB888).rgbSwapped()
        image = QtWidgets.QGraphicsScene(self.gvCrop)
        image.addItem(QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(qImg).scaled(self.gvCrop.width(), self.gvCrop.height(), QtCore.Qt.KeepAspectRatio)))
        self.gvCrop.setScene(image)
        self.gvCrop.show()