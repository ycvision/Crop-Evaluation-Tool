from PyQt5 import QtWidgets, QtGui, QtCore
from utils.mydesign import Ui_MainWindow  # importing our generated file
import sys
import os
import cv2
import pickle
import numpy as np
from utils.Crop import Crop
from utils.Group import Group


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self-defined variables
        self.idx = -1
        self.folder_path = "dataset"
        self.log_path = "results.pkl"
        self.result = {}
        if os.path.exists(self.log_path):
            with open(self.log_path, "rb") as f:
                self.result = pickle.load(f)
            print("File {} exists and is loaded.".format(self.log_path))
            self.idx = len(self.result) - 1
        self.original_image_paths, \
        self.qian_image_paths, \
        self.gaic_image_paths, \
        self.ours_image_paths, \
        self.shaoyuan_image_paths,\
        self.centercrop_image_paths, \
        self.ours_no_person_image_paths, \
        self.vfn_image_paths = self.get_images(self.folder_path)

        self.num_max = 7
        self.num_available = len(self.original_image_paths) - 1

        self.d = {}

        # ui setup
        self.ui.pbProgress.setValue((self.idx + 1) / len(self.original_image_paths) * 100)
        self.set_up_image_window(self.ui.gvOriginal)

        self.group1 = Group(self.ui.gvCrop1, [self.ui.rbYes1, self.ui.rbNo1], self.ui.lblCrop1)
        self.group2 = Group(self.ui.gvCrop2, [self.ui.rbYes2, self.ui.rbNo2], self.ui.lblCrop2)
        self.group3 = Group(self.ui.gvCrop3, [self.ui.rbYes3, self.ui.rbNo3], self.ui.lblCrop3)
        self.group4 = Group(self.ui.gvCrop4, [self.ui.rbYes4, self.ui.rbNo4], self.ui.lblCrop4)
        self.group5 = Group(self.ui.gvCrop5, [self.ui.rbYes5, self.ui.rbNo5], self.ui.lblCrop5)
        self.group6 = Group(self.ui.gvCrop6, [self.ui.rbYes6, self.ui.rbNo6], self.ui.lblCrop6)
        self.group7 = Group(self.ui.gvCrop7, [self.ui.rbYes7, self.ui.rbNo7], self.ui.lblCrop7)
        self.groups = [self.group1, self.group2, self.group3, self.group4, self.group5, self.group6, self.group7]

        self.crop1 = Crop(self.qian_image_paths)
        self.crop2 = Crop(self.gaic_image_paths)
        self.crop3 = Crop(self.ours_image_paths)
        self.crop4 = Crop(self.shaoyuan_image_paths)
        self.crop5 = Crop(self.centercrop_image_paths)
        self.crop6 = Crop(self.ours_no_person_image_paths)
        self.crop7 = Crop(self.vfn_image_paths)
        self.crops = [self.crop1, self.crop2, self.crop3, self.crop4, self.crop5, self.crop6, self.crop7]

        self.ui.btnNext.clicked.connect(self.retrieve_next)

        # initialize
        self.retrieve_next(True)

    @staticmethod
    def set_up_image_window(window):
        window.setRenderHint(QtGui.QPainter.Antialiasing)
        window.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        window.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    @staticmethod
    def display(window, cvImg):
        height, width, channel = cvImg.shape
        qImg = QtGui.QImage(cvImg.data, width, height, 3 * width, QtGui.QImage.Format_RGB888).rgbSwapped()
        image = QtWidgets.QGraphicsScene(window)
        image.addItem(QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(qImg).scaled(window.width(), window.height(), QtCore.Qt.KeepAspectRatio)))
        window.setScene(image)
        window.show()

    @staticmethod
    def get_images(root_folder_path):
        original_image_paths = []
        qian_image_paths = []
        gaic_image_paths = []
        ours_image_paths = []
        shaoyuan_image_paths = []
        centercrop_image_paths = []
        ours_no_person_image_paths = []
        vfn_image_paths = []

        original_folder_paths = [os.path.join(root_folder_path, "demo")]
        qian_folder_paths = [os.path.join(root_folder_path, "method1")]
        gaic_folder_paths = [os.path.join(root_folder_path, "method2")]
        ours_folder_paths = [os.path.join(root_folder_path, "method3")]
        shaoyuan_folder_paths = [os.path.join(root_folder_path, "method4")]
        centercrop_folder_paths = [os.path.join(root_folder_path, "method5")]
        ours_no_person_folder_paths = [os.path.join(root_folder_path, "method6")]
        vfn_folder_paths = [os.path.join(root_folder_path, "method7")]

        for original_folder_path, qian_folder_path, gaic_folder_path, ours_folder_path, shaoyuan_folder_path, centercrop_folder_path, ours_no_person_folder_path, vfn_folder_path in zip(original_folder_paths, qian_folder_paths, gaic_folder_paths, ours_folder_paths, shaoyuan_folder_paths,
                                                                                                                                                                                         centercrop_folder_paths, ours_no_person_folder_paths, vfn_folder_paths):
            image_names = os.listdir(original_folder_path)
            image_names = sorted(image_names)
            original_image_names = [os.path.join(original_folder_path, image_name) for image_name in image_names]
            original_image_paths += original_image_names

            qian_image_names = [os.path.join(qian_folder_path, "{}_aspect-ratio_1.00.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            qian_image_paths += qian_image_names

            gaic_image_names = [os.path.join(gaic_folder_path, "{}_no_crop_1.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            gaic_image_paths += gaic_image_names

            ours_image_names = [os.path.join(ours_folder_path, "{}_no_crop_1.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            ours_image_paths += ours_image_names

            shaoyuan_image_names = [os.path.join(shaoyuan_folder_path, "{}.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            shaoyuan_image_paths += shaoyuan_image_names

            centercrop_image_names = [os.path.join(centercrop_folder_path, "{}.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            centercrop_image_paths += centercrop_image_names

            ours_no_person_image_names = [os.path.join(ours_no_person_folder_path, "{}_no_crop_1.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            ours_no_person_image_paths += ours_no_person_image_names

            vfn_image_names = [os.path.join(vfn_folder_path, "{}.{}".format('.'.join(image_name.split(".")[:-1]), image_name.split(".")[-1])) for image_name in image_names]
            vfn_image_paths += vfn_image_names

        for original_image_path in original_image_paths:
            assert os.path.exists(original_image_path)
        for qian_image_path in qian_image_paths:
            assert os.path.exists(qian_image_path), print(qian_image_path)
        for gaic_image_path in gaic_image_paths:
            assert os.path.exists(gaic_image_path), print(gaic_image_path)
        for ours_image_path in ours_image_paths:
            assert os.path.exists(ours_image_path)
        for shaoyuan_image_path in shaoyuan_image_paths:
            assert os.path.exists(shaoyuan_image_path)
        for centercrop_image_path in centercrop_image_paths:
            assert os.path.exists(centercrop_image_path)
        for ours_no_person_image_path in ours_no_person_image_paths:
            assert os.path.exists(ours_no_person_image_path), print(ours_no_person_image_path)
        for vfn_image_path in vfn_image_paths:
            assert os.path.exists(vfn_image_path), print(vfn_image_path)
        return original_image_paths, qian_image_paths, gaic_image_paths, ours_image_paths, shaoyuan_image_paths, centercrop_image_paths, ours_no_person_image_paths, vfn_image_paths

    def retrieve_next(self, start=False):
        if not start:
            for group in self.groups:
                if not group.at_least_one_checked():
                    return
            for group in self.groups:
                self.d[group].likes.append(1 if group.rbs[0].isChecked() else 0)
            self.result[self.original_image_paths[self.idx]] = []
            for crop in self.crops:
                self.result[self.original_image_paths[self.idx]].append(crop.likes[-1])
            with open(self.log_path, "wb") as f:
                pickle.dump(self.result, f)
            # print(self.crops[0], self.crops[1], self.crops[2], self.crops[3], self.crops[4])

        for group in self.groups:
            group.clear_radio_buttons()

        self.idx += 1
        self.ui.pbProgress.setValue((self.idx + 1) / len(self.original_image_paths) * 100)
        if self.idx == len(self.original_image_paths):
            print("Evaluation is now complete.")
            quit()

        random_indices = list(np.random.permutation(len(self.crops)))
        for i in range(len(self.groups)):
            self.d[self.groups[i]] = self.crops[random_indices[i]]

        self.display(self.ui.gvOriginal, cv2.imread(self.original_image_paths[self.idx]))

        for group in self.groups:
            group.display(cv2.imread(self.d[group][self.idx]))
            # group.label.setText(self.d[group][self.idx].split("/")[-2])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())