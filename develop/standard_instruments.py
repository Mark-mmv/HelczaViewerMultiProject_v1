import sys
import time
import numpy as np
import numba
import PIL
from skimage import transform
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from analysis_menu import InterfaceAnalysisMenu


class StandardInstruments:
    def __init__(self):
        """Attributes"""
        self.analysis_menu = InterfaceAnalysisMenu()
        self.fig, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.image = np.array([[0]])
        self.file_name = (str(time.strftime("%H%M%S")), '.tiff')
        self.id_connected_on_pick_1 = None
        self.id_connected_on_pick_2 = None
        self.shapes = None
        self.points = np.array([[0, 0], [0, 250], [250, 250], [250, 0]], dtype=np.float32)
        self.line_points = np.array([[0, 0], [250, 250]], dtype=np.float32)
        self.line_profile = []
        self.area_points = np.array([[0, 0], [0, 250], [250, 250], [250, 0]], dtype=np.float32)

    def import_image(self):
        try:
            self.file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Select images', '',
                                                          "Image files (*.jpg *.tiff *.tif *.png *.pgm *.bmp)")
            self.image = np.array(matplotlib.image.imread(self.file_name[0]))
        except:
            [print("\033[0;31;1m" + str(error) + '\033[0;0m') for error in sys.exc_info()]
            return

    def save_image(self, image):
        try:
            name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save', self.file_name[0], '*.tiff')
            mode = 'I;16'
            file = PIL.Image.fromarray(image, mode)
            file.save(name[0])
        except:
            self.error = 'Save error'

    def clear_canvas(self):
        self.axes.clear()
        self.canvas.draw()

    def show_image(self, image, color_map=None, axis='on', grid=False):
        self.axes.axis(axis)
        self.axes.grid(grid)
        frame = self.axes.imshow(image, cmap=color_map)
        self.canvas.draw()
        return frame

    def set_axes(self, left=None, right=None, bottom=None, top=None):
        self.axes.set_xlim(left, right)
        self.axes.set_ylim(bottom, top)

    def defined_points(self, b):
        if b.text() == "Line profile":
            self.points = self.line_points
        else:
            self.points = self.area_points

        if b.isChecked() is False:
            self.fig.canvas.mpl_disconnect(self.id_connected_on_pick_1)
            self.fig.canvas.mpl_disconnect(self.id_connected_on_pick_2)
            self.shapes.pop().remove()
            self.canvas.draw()
        else:
            points = np.append(self.points, [self.points[0]], axis=0)
            self.shapes = self.axes.plot(points[:, 0], points[:, 1], 'r', linewidth=1)
            self.canvas.draw()
            self.id_connected_on_pick_1 = self.fig.canvas.mpl_connect('motion_notify_event', self.on_pick_area)
            self.id_connected_on_pick_2 = self.fig.canvas.mpl_connect('button_press_event', self.on_pick_area)

    def on_pick_area(self, event):
        if (event.xdata is not None) and (event.button == 1):
            point = np.array([event.xdata, event.ydata])
            radius = np.subtract(self.points, point)**2
            self.points[(radius[:, 0] + radius[:, 1]).argmin()] = point
            points = np.append(self.points, [self.points[0]], axis=0)
            self.shapes.pop().remove()
            self.shapes = self.axes.plot(points[:, 0], points[:, 1], 'r', linewidth=1)
            self.canvas.draw()
            if len(self.points) == 2:
                self.select_profile()

    def select_area(self):
        try:
            src = np.array([[0, 0], [0, 250], [250, 250], [250, 0]])
            tform3 = transform.ProjectiveTransform()
            tform3.estimate(src, self.area_points)
            warped = transform.warp(self.image, tform3, output_shape=(250, 250), order=3)
            return warped
        except:
            pass

    def select_profile(self):
        try:
            length = ((self.points[1, 1] - self.points[0, 1])**2 + (self.points[1, 0] - self.points[0, 0])**2)**0.5
            sin = (self.points[1, 0] - self.points[0, 0]) / length
            cos = (self.points[1, 1] - self.points[0, 1]) / length
            self.line_profile = [self.image[int(cos * point + self.points[0, 1]), int(sin * point + self.points[0, 0])]
                                 for point in np.arange(0, length, 1)]
            self.analysis_menu.plot_graph(self.line_profile)
        except:
            pass



