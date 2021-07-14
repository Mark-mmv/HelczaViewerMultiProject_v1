import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from interfaces.interface_image_menu import Ui_interface_image_menu


class InterfaceImageMenu(QMainWindow, Ui_interface_image_menu):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        """Buttons"""
        self.menu_file.triggered[QAction].connect(self.process_trigger_menu_bar)

        """Create canvas for showing images"""
        self.fig_img_in, self.axes_img_in = plt.subplots()
        self.canvas_img_in = FigureCanvas(self.fig_img_in)
        self.toolbar_img_in = NavigationToolbar(self.canvas_img_in, self)
        self.companovka_image_in.addWidget(self.toolbar_img_in)
        self.companovka_image_in.addWidget(self.canvas_img_in)

        self.fig_img_out, self.axes_img_out = plt.subplots()
        self.canvas_img_out = FigureCanvas(self.fig_img_out)
        self.toolbar_img_out = NavigationToolbar(self.canvas_img_out, self)
        self.companovka_image_out.addWidget(self.toolbar_img_out)
        self.companovka_image_out.addWidget(self.canvas_img_out)

    def process_trigger_menu_bar(self, q):
        if q.iconText() == 'Open image':
            self.import_image_in()

    def import_image_in(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Select images', '',
                                                      "Image files (*.jpg *.tiff *.tif *.png *.pgm *.bmp)")
        image_in = matplotlib.image.imread(file[0])
        self.image_in = np.array(image_in)
        #self.image_in = 2**2**2**(2**(self.image_in / self.image_in.max()))
        self.axes_img_in.clear()
        self.axes_img_in.imshow(self.image_in)
        self.canvas_img_in.draw()


def main():
    app = QApplication(sys.argv)
    interface_main = InterfaceImageMenu()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()