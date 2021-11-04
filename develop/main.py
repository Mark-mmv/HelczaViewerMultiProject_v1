import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from PyQt5.QtGui import QFont, QKeySequence, QPixmap

from interfaces.interface_main import Ui_interface_main
from interfaces.dialog_select_camera import Ui_dialog_select_camera
from camera_menu import InterfaceCameraMenu
from pattern_menu import InterfacePatternMenu
from image_menu import InterfaceImageMenu


class InterfaceMain(QMainWindow, QDialog, QApplication, Ui_interface_main):
    def __init__(self):
        QMainWindow.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)

        """Global variables"""
        self.polynomial = ['x', 'y']
        self.frame_of_stream = np.array([])

        """Buttons"""
        self.button_open_camera_menu.clicked.connect(lambda: self.dialog_select_camera.show())
        self.button_open_pattern_menu.clicked.connect(lambda: self.interface_pattern_menu.show())
        self.button_open_image_menu.clicked.connect(lambda: self.interface_image_menu.show())

        """Attributes of classes"""
        self.interface_camera_menu_andor = InterfaceCameraMenu(self, camera="andor")
        self.interface_camera_menu_vimba = InterfaceCameraMenu(self, camera="vimba")
        self.interface_pattern_menu = InterfacePatternMenu(self)
        self.interface_image_menu = InterfaceImageMenu(self)
        self.dialog_select_camera = QtWidgets.QDialog()
        self.dialog_camera = Ui_dialog_select_camera()
        self.dialog_camera.setupUi(self.dialog_select_camera)
        self.dialog_camera.command_link_button_andor.clicked.connect(lambda: self.open_camera_menu("andor"))
        self.dialog_camera.command_link_button_vimba.clicked.connect(lambda: self.open_camera_menu("vimba"))

    def open_camera_menu(self, camera=None):
        self.interface_camera_menu_andor.show() if camera == "andor" else self.interface_camera_menu_vimba.show()
        self.dialog_select_camera.close()


def main():
    app = QApplication(sys.argv)
    interface_main = InterfaceMain()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


