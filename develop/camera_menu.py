import random
import sys
import os
import time
import numpy as np
from threading import Thread
try:
    from pymba import *
except:
    pass
import PIL
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from standard_instruments import StandardInstruments
from interfaces.interface_camera_menu import Ui_interface_camera_menu
from image_correction import InterfaceImageCorrection
from analysis_menu import InterfaceAnalysisMenu


class InterfaceCameraMenu(StandardInstruments, QMainWindow, Ui_interface_camera_menu):
    def __init__(self, parent=None, camera=None):
        StandardInstruments.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.main = parent
        self.camera = camera

        """Buttons 1 tab"""
        self.button_start_stream.clicked.connect(self.start_stream)
        self.button_save_image_stream.clicked.connect(self.save_image_stream)
        self.button_zoom_stream.clicked.connect(lambda: self.toolbar_stream_method(self.button_zoom_stream))
        self.button_posun_stream.clicked.connect(lambda: self.toolbar_stream_method(self.button_posun_stream))
        self.button_up_to_stream.clicked.connect(lambda: self.toolbar_stream_method(self.button_up_to_stream))
        self.button_down_to_stream.clicked.connect(lambda: self.toolbar_stream_method(self.button_down_to_stream))
        self.button_home_stream.clicked.connect(lambda: self.toolbar_stream_method(self.button_home_stream))
        self.shortcut_Save = QShortcut(QtGui.QKeySequence('Ctrl+s'), self)
        self.shortcut_Save.activated.connect(self.save_image_directory)

        """Buttons 2 tab"""
        self.button_open_analysis_window.clicked.connect(lambda: self.analysis_menu.show())
        self.button_select_area.clicked.connect(self.select_area)
        self.button_catch_reference.clicked.connect(self.catch_reference)
        self.checkbox_select_area.stateChanged.connect(lambda: self.defined_area(self.checkbox_select_area))
        self.checkbox_line_profile.stateChanged.connect(lambda: self.defined_line(self.checkbox_line_profile))

        """Create canvas for showing images"""
        self.fig_stream, self.axes_stream = plt.subplots()
        self.canvas_stream = FigureCanvas(self.fig_stream)
        self.toolbar_stream = NavigationToolbar(self.canvas, self)
        self.toolbar_stream.setVisible(False)
        self.companovka_stream.addWidget(self.toolbar_stream)
        self.companovka_stream.addWidget(self.canvas)

        """Attributes"""
        self.image_reference = np.array(self.image)
        self.stream_start_stop = False
        self.stream_process = camera
        self.one_frame = self.axes_stream.imshow([[0]])
        self.interface_image_correction = InterfaceImageCorrection(self.main)

    def start_stream(self):
        if self.stream_start_stop is False:
            self.stream_start_stop = True
            self.button_start_stream.setStyleSheet(
                'border-image: url('':/icon/icon/baseline_pause_circle_outline_black_36dp.png)')
            self.text_edit_exposure_gain.setText(
                '_'+str(int(self.spinbox_exposure.value()*1000))+'us'+'_'+str(self.spinbox_gain.value())+'g')
            self.stream_process = Thread(target=self.stream_test)
            self.stream_process.start()
        else:
            self.stream_start_stop = False
            self.button_start_stream.setStyleSheet(
                'border-image: url('':/icon/icon/baseline_play_circle_outline_black_36dp.png)')
            self.stream_process.join()

    def stream_test(self):
        while self.stream_start_stop is True:
            self.image = self.main.interface_image_menu.image
            self.image[:, 10] = random.randint(1, 64000)
            time.sleep(0.1)
            color_map = "bone" if self.checkbox_gray_color.isChecked() is False else None
            axis = "off" if self.checkbox_grid_stream.isChecked() is False else "on"
            grid = self.checkbox_grid_stream.isChecked()
            self.select_profile() if self.checkbox_line_profile.isChecked() is True else None
            if self.checkbox_implement_reference.isChecked() is True:
                mask = self.image > self.image_reference
                self.image = np.array(self.image - self.image_reference) * mask

            self.one_frame.remove()
            #self.fig.tight_layout()
            #self.set_axes(left=0, right=self.image.shape[1], bottom=self.image.shape[0], top=0)
            self.one_frame = self.show_image(self.image, color_map, grid, axis)
            self.main.frame_of_stream = self.image

    def stream_vimba(self):
        self.toolbar_stream.configure_subplots_stream()._tight_layout()
        vimba = Vimba()
        vimba.startup()
        camera0 = vimba.camera(vimba.camera_ids()[0])
        camera0.open()
        feature_exposure = camera0.feature('ExposureTimeAbs')
        feature_gain = camera0.feature('Gain')
        camera0.feature('PixelFormat').value = 'Mono12'

        while self.stream_start_stop is True:
            feature_exposure.value = self.spinbox_exposure.value() * 1000
            feature_gain.value = self.spinbox_gain.value()
            frame0 = camera0.new_frame()
            frame0.announce()
            camera0.arm('SingleFrame')
            frame0.queue_for_capture()
            camera0.acquire_frame(int(self.spinbox_exposure.value() + self.spinbox_interupt.value()))
            frame_of_stream = np.ndarray(buffer=frame0.buffer_data(), dtype=np.uint16, shape=(1038, 1388))
            camera0.revoke_all_frames()
            camera0.disarm()

            color_map = "bone" if self.checkbox_gray_color.isChecked() is False else None
            axis = "off" if self.checkbox_grid_stream.isChecked() is False else "on"
            grid = self.checkbox_grid_stream.isChecked()
            self.select_profile() if self.checkbox_line_profile.isChecked() is True else None
            if self.checkbox_implement_reference.isChecked() is True:
                mask = self.image > self.image_reference
                self.image = np.array(self.image - self.image_reference) * mask

            self.one_frame.remove()
            #self.fig.tight_layout()
            #self.set_axes(left=0, right=self.image.shape[1], bottom=self.image.shape[0], top=0)
            self.one_frame = self.show_image(self.image, color_map, grid, axis)
            self.main.frame_of_stream = frame_of_stream

            try:
                self.CatchDataLine()
            except:
                pass

        camera0.close()
        vimba.shutdown()

    def stream_andor(self):
        pass

    def save_image_stream(self):
        try:
            if not os.path.exists(str(time.strftime("%Y%m%d"))):
                os.makedirs(str(time.strftime("%Y%m%d")))
            mode = 'I;16'
            name = str(time.strftime("%Y%m%d")) + '/' + str(time.strftime("%H%M%S")) + '_' + str(
                self.text_edit_name_image.toPlainText()) + str(self.text_edit_exposure_gain.toPlainText() + str('.tiff'))
            file = PIL.Image.fromarray(self.main.frame_of_stream, mode)
            file.save(name)
        except:
            pass

    def save_image_directory(self):
        try:
            name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save', str(self.text_edit_name_image.toPlainText()) +
                                                         str(self.text_edit_exposure_gain.toPlainText()), '*.tiff')
            mode = 'I;16'
            file = PIL.Image.fromarray(self.main.frame_of_stream, mode)
            file.save(name[0])
        except:
            self.error = 'Save error'

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

    def catch_reference(self):
        self.image_reference = np.array(self.image)

    def toolbar_stream_method(self, b):
        if b.objectName() == 'button_zoom_stream' and b.styleSheet() == "border-image: url(:/icon/icon/baseline_search_black_24dp.png);":
            self.button_posun_stream.setStyleSheet("border-image: url(:/icon/icon/baseline_pan_tool_black_24dp.png);")
            self.button_zoom_stream.setStyleSheet("border-image: url(:/icon/icon/baseline_search_black_24dp2.png);")
            self.toolbar_stream.zoom()
        elif b.objectName() == 'button_zoom_stream':
            self.button_zoom_stream.setStyleSheet("border-image: url(:/icon/icon/baseline_search_black_24dp.png);")
            self.toolbar_stream.zoom()

        if b.objectName() == 'button_posun_stream' and b.styleSheet() == "border-image: url(:/icon/icon/baseline_pan_tool_black_24dp.png);":
            self.button_zoom_stream.setStyleSheet("border-image: url(:/icon/icon/baseline_search_black_24dp.png);")
            self.button_posun_stream.setStyleSheet("border-image: url(:/icon/icon/baseline_pan_tool_black_24dp2.png);")
            self.toolbar_stream.pan()
        elif b.objectName() == 'button_posun_stream':
            self.button_posun_stream.setStyleSheet("border-image: url(:/icon/icon/baseline_pan_tool_black_24dp.png);")
            self.toolbar_stream.pan()

        if b.objectName() == 'button_up_to_stream':
            self.toolbar_stream.back()

        if b.objectName() == 'button_down_to_stream':
            self.toolbar_stream.forward()

        if b.objectName() == 'button_home_stream':
            self.toolbar_stream.home()


def main():
    app = QApplication(sys.argv)
    interface_main = InterfaceCameraMenu()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
