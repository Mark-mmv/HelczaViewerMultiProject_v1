import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from PyQt5.QtGui import QFont, QKeySequence, QPixmap

from interfaces.interface_main import Ui_interface_main
from camera_menu import InterfaceCameraMenu
from pattern_menu import InterfacePatternMenu
from image_menu import InterfaceImageMenu


class InterfaceMain(QMainWindow, Ui_interface_main):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        """Buttons"""
        self.button_open_camera_menu.clicked.connect(self.open_camera_menu)
        self.button_open_pattern_menu.clicked.connect(self.open_pattern_menu)
        self.button_open_image_menu.clicked.connect(self.open_image_menu)

        """Attributes of classes"""
        self.interface_camera_menu = InterfaceCameraMenu()
        self.interface_pattern_menu = InterfacePatternMenu()
        self.interface_image_menu = InterfaceImageMenu()

    def open_camera_menu(self):
        self.interface_camera_menu.show()

    def open_pattern_menu(self):
        self.interface_pattern_menu.show()

    def open_image_menu(self):
        self.interface_image_menu.show()


def main():
    app = QApplication(sys.argv)
    interface_main = InterfaceMain()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

