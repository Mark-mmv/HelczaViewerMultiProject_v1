import numpy as np
from scipy.optimize import curve_fit
from threading import Thread
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from interfaces.interface_image_correction import Ui_interface_image_correction
from standard_instruments import StandardInstruments
import fitting


class InterfaceImageCorrection(StandardInstruments, QMainWindow, Ui_interface_image_correction):
    def __init__(self, parent=None, image_dialog=None):
        StandardInstruments.__init__(self)
        QDialog.__init__(self)
        self.setupUi(self)
        self.main = parent
        self.image = image_dialog

        """Buttons"""
        self.menu_file.triggered[QAction].connect(self.process_trigger_menu_bar)
        self.horizontal_slider_scale.valueChanged.connect(self.scaler_areas)
        self.button_submit_area.clicked.connect(self.submit_area)
        self.button_back_submit.clicked.connect(self.back_submit)
        self.button_forward_submit.clicked.connect(self.forward_submit)
        self.button_fit.clicked.connect(self.fit_area)
        #self.button_fit.clicked.connect(lambda: Thread(target=self.fit_area).start())
        self.checkbox_submit_area.stateChanged.connect(lambda: self.defined_submit_area(self.checkbox_submit_area))

        """Attributes"""
        self.square = None
        self.scale = 50
        self.area_history = []
        self.area_history_forward = []

        """Create canvas for showing images"""
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.companovka_dialog_image.addWidget(self.toolbar)
        self.companovka_dialog_image.addWidget(self.canvas)

    def process_trigger_menu_bar(self, q):
        if q.iconText() == 'Open image':
            self.import_image_correction()
        if q.iconText() == 'Save image':
            self.save_image_correction()

    def import_image_correction(self):
        self.import_image()
        self.image = np.array(self.image / 2**16, dtype=np.float32)
        self.clear_canvas()
        self.set_axes(left=-50, right=300, bottom=300, top=-50)
        self.show_image(self.image, color_map='bone')

    def save_image_correction(self):
        self.image = np.array(self.image * 2 ** 16, dtype=np.uint16)
        self.save_image(self.image)

    def defined_submit_area(self, b):
        if b.isChecked() is False:
            self.fig.canvas.mpl_disconnect(self.id_connected_onpick_area_1)
            self.fig.canvas.mpl_disconnect(self.id_connected_onpick_area_2)
        else:
            self.square = self.axes.plot(0, 0)
            self.id_connected_onpick_area_1 = self.fig.canvas.mpl_connect('motion_notify_event', self.onpick_submit_area)
            self.id_connected_onpick_area_2 = self.fig.canvas.mpl_connect('button_press_event', self.onpick_submit_area)

    def onpick_submit_area(self, event):
        if (event.xdata is not None) and (event.button == 1):
            self.area_points[0] = np.array([event.xdata, event.ydata], dtype=np.int32)
            self.area_points[1, 0] = self.area_points[0, 0]
            self.area_points[3, 1] = self.area_points[0, 1]
            self.square.pop().remove()
            self.square = self.axes.plot([self.area_points[0, 0], self.area_points[0, 0]],
                                         [self.area_points[0, 1], self.area_points[0, 1]],
                                             'r', marker='.', markersize=6)
            self.canvas.draw()

        if (event.xdata is not None) and (event.button == 3):
            self.area_points[2] = np.array([event.xdata, event.ydata], dtype=np.int32)
            self.area_points[1, 1] = self.area_points[2, 1]
            self.area_points[3, 0] = self.area_points[2, 0]
            area_points = np.append(self.area_points, [self.area_points[0]], axis=0)
            self.square.pop().remove()
            self.square = self.axes.plot(area_points[:, 0], area_points[:, 1], 'r', linewidth=1)
            self.canvas.draw()

    def submit_area(self):
        data = [min_0, min_1, max_0, max_1] = self.area_points[:, 0].min(), self.area_points[:, 1].min(),\
                                              self.area_points[:, 0].max(), self.area_points[:, 1].max()

        rect = matplotlib.patches.Rectangle((min_0, min_1), max_0 - min_0, max_1 - min_1,
                                            alpha=0.2, edgecolor='r', facecolor='r')
        self.axes.add_patch(rect)
        self.set_axes(left=-50, right=300, bottom=300, top=-50)
        self.canvas.draw()
        self.area_history.append([data, rect])
        self.area_history_forward = []

    def back_submit(self):
        try:
            self.area_history_forward.append(self.area_history.pop())
            self.clear_canvas()
            self.set_axes(left=-50, right=300, bottom=300, top=-50)
            self.show_image(self.image, color_map='bone')
            for [data, rect] in self.area_history:
                self.axes.add_patch(rect)
            self.canvas.draw()
        except:
            pass

    def forward_submit(self):
        try:
            self.area_history.append(self.area_history_forward.pop())
            self.clear_canvas()
            for [data, rect] in self.area_history:
                self.axes.add_patch(rect)
            self.set_axes(left=-50, right=300, bottom=300, top=-50)
            self.show_image(self.image, color_map='bone')
        except:
            pass

    def scaler_areas(self, value):
        area_history = []
        delta = (value - self.scale)/4
        self.scale = value
        self.area_history_forward = []
        self.clear_canvas()
        for [data, rect] in self.area_history:
            data = [int(data[0] - delta), int(data[1] - delta), int(data[2] + delta), int(data[3] + delta)]

            rect = matplotlib.patches.Rectangle((data[0], data[1]), data[2] - data[0], data[3] - data[1],
                                                alpha=0.2, edgecolor='r', facecolor='r')
            self.axes.add_patch(rect)
            area_history.append([data, rect])

        self.set_axes(left=-50, right=300, bottom=300, top=-50)
        self.show_image(self.image, color_map='bone')
        self.area_history = area_history

    def fit_area(self):
        sub_image = np.array(self.image)
        for [data, rect] in self.area_history:
            for i in range(int(data[0]), int(data[2])):
                for j in range(int(data[1]), int(data[3])):
                    try:
                        sub_image[j, i] = 0
                    except:
                        pass
        self.image = sub_image
        self.clear_canvas()
        self.set_axes(left=-50, right=300, bottom=300, top=-50)
        self.show_image(sub_image, color_map='bone')

        self.main.polynomial, fit_kof = fitting.fit(sub_image)

        mesh = np.meshgrid(*[np.linspace(-1, 1, sub_image.shape[0])] * 2)
        new = fitting.func(mesh, *fit_kof)
        self.save_image(np.array(new * 2**16, dtype=np.uint16))
        self.analysis_menu.show()
        self.analysis_menu.axes.imshow(new)
        #self.analysis_menu.axes.imshow(sub_image)
        #ax.scatter(mesh[0], mesh[1], self.image, marker='X')
        #ax.plot_surface(mesh[0], mesh[1], new, cmap='viridis')
        self.analysis_menu.canvas.draw()






