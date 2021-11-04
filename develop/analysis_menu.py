import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from interfaces.interface_analysis_menu import Ui_interface_analysis_menu


class InterfaceAnalysisMenu(QDialog, Ui_interface_analysis_menu):
    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.main = parent

        self.fig, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.companovka.addWidget(self.toolbar)
        self.companovka.addWidget(self.canvas)

    def plot_graph(self, data):
        self.axes.clear()
        self.axes.plot(data)
        self.canvas.draw()
