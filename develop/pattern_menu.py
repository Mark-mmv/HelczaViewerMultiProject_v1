import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut

from interfaces.interface_pattern_menu import Ui_interface_pattern_menu


class InterfacePatternMenu(QMainWindow, Ui_interface_pattern_menu):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)