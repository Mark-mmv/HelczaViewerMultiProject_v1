import sys
import numpy as np
from threading import Thread
try:
    from pymba import *
except:
    pass


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut

from interfaces.interface_camera_menu import Ui_interface_camera_menu


class InterfaceCameraMenu(QMainWindow, Ui_interface_camera_menu):
    def __init__(self, parent=None, camera=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        """Buttons"""
        self.button_start_stream.clicked.connect(self.start_stream)

        """Attributes"""
        self.stream_start_stop = False
        self.stream_process = camera
        self.image_for_save = 0

    def start_stream(self):
        if self.stream_start_stop is False:
            self.stream_start_stop = True
            self.button_start_stream.setStyleSheet(
                'border-image: url('':/icon/icon/baseline_pause_circle_outline_black_36dp.png)')
            self.text_edit_exposure_gain.setText(
                '_'+str(int(self.spinbox_exposure.value()*1000))+'us'+'_'+str(self.spinbox_gain.value())+'g')
            self.stream_process = Thread(target=self.stream_vimba)
            self.stream_process.start()
        else:
            self.stream_start_stop = False
            self.button_start_stream.setStyleSheet(
                'border-image: url('':/icon/icon/baseline_play_circle_outline_black_36dp.png)')
            self.stream_process.join()
            print(self.image_for_save)

    def stream_vimba(self):
        Axis = 'off'
        vimba = Vimba()
        vimba.startup()
        cameraIds = vimba.camera_ids()
        camera0 = vimba.camera(cameraIds[0])
        camera0.open()
        feature0 = camera0.feature('ExposureTimeAbs')
        feature1 = camera0.feature('PixelFormat')
        feature2 = camera0.feature('Gain')
        feature1.value = 'Mono12'

        while self.stream_start_stop is True:
            feature0.value = self.spinbox_exposure.value() * 1000
            feature2.value = self.spinbox_gain.value()
            frame0 = camera0.new_frame()
            frame0.announce()
            camera0.arm('SingleFrame')
            frame0.queue_for_capture()
            camera0.acquire_frame(round(1000 / self.spinbox_fps.value()))
            Frame_of_stream = np.ndarray(
                buffer=frame0.buffer_data(), dtype=np.uint16, shape=(1038, 1388))
            self.FrameOfStream = np.array(config.FrameOfStream)
            camera0.revoke_all_frames()
            camera0.disarm()

            try:
                self.OneFrame.remove()
            except:
                pass

            if self.checkBox_Axis.isChecked() == True:
                if Axis == 'off':
                    Axis = 'on'
                    self.toolbarStream.configure_subplots_stream()._tight_layout()
                else:
                    pass
            else:
                if Axis == 'on':
                    Axis = 'off'
                    self.toolbarStream.configure_subplots_stream()._tight_layout_fullscreen()
                else:
                    pass

            if self.checkBox_GrayColor.isChecked() == True:
                cmap = 'gray'
            else:
                cmap = None

            if self.checkBox_GridStream.isChecked() == True:
                grid = True
            else:
                grid = False

            if self.checkBox_ImplementReference.isChecked() == True:
                config.FrameOfStream = GPUReference.StreamFastRef(config.FrameOfStream, config.ImageReference)

            self.axesStream.axis(Axis)
            self.axesStream.grid(grid)
            self.OneFrame = self.axesStream.imshow(config.FrameOfStream, cmap)
            self.canvasStream.draw()

            try:
                self.CatchDataLine()
            except:
                pass

        camera0.close()
        vimba.shutdown()