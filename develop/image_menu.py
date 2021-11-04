import sys
import time
import numpy as np
from skimage import transform
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from standard_instruments import StandardInstruments
from interfaces.interface_image_menu import Ui_interface_image_menu
from image_correction import InterfaceImageCorrection


class InterfaceImageMenu(StandardInstruments, QMainWindow, Ui_interface_image_menu):
    def __init__(self, parent=None):
        StandardInstruments.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.main = parent

        """Buttons"""
        self.button_select_area.clicked.connect(self.select_area)
        self.button_open_analysis_window.clicked.connect(lambda: self.analysis_menu.show())
        self.menu_file.triggered[QAction].connect(self.process_trigger_menu_bar)
        self.checkbox_select_area.stateChanged.connect(lambda: self.defined_area(self.checkbox_select_area))
        self.checkbox_line_profile.stateChanged.connect(lambda: self.defined_line(self.checkbox_line_profile))

        """Attributes"""
        self.interface_image_correction = InterfaceImageCorrection(self.main)

        """Create canvas for showing images"""
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.companovka_image_in.addWidget(self.toolbar)
        self.companovka_image_in.addWidget(self.canvas)

    def process_trigger_menu_bar(self, q):
        if q.iconText() == 'Open image':
            self.import_image()
            self.show_image(self.image)
        if q.iconText() == 'Save image':
            self.save_image(self.image)

    def defined_line(self, b):
        if b.isChecked() is True:
            self.checkbox_select_area.setChecked(False)
        super().defined_points(b)

    def defined_area(self, b):
        if b.isChecked() is True:
            self.checkbox_line_profile.setChecked(False)
        super().defined_points(b)

    def select_area(self):
        try:
            warped = super().select_area()
            self.interface_image_correction.image = np.array(warped, dtype=np.float32)
            self.interface_image_correction.set_axes(left=-50, right=300, bottom=300, top=-50)
            self.interface_image_correction.show_image(warped, color_map='bone')
            self.interface_image_correction.show()
        except:
            pass


def main():
    app = QApplication(sys.argv)
    interface_main = InterfaceImageMenu()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
