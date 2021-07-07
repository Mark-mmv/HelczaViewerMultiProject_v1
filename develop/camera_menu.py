import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut

from interfaces.interface_camera_menu import Ui_interface_camera_menu


class InterfaceCameraMenu(QMainWindow, Ui_interface_camera_menu):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)