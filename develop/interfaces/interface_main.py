# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface_main(object):
    def setupUi(self, interface_main):
        interface_main.setObjectName("interface_main")
        interface_main.resize(777, 595)
        interface_main.setStyleSheet("QWidget#centralwidget{border-image: url(:/image/image/fon.jpg);}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(interface_main)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_open_camera_menu = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_open_camera_menu.sizePolicy().hasHeightForWidth())
        self.button_open_camera_menu.setSizePolicy(sizePolicy)
        self.button_open_camera_menu.setMaximumSize(QtCore.QSize(80, 80))
        self.button_open_camera_menu.setObjectName("button_open_camera_menu")
        self.horizontalLayout.addWidget(self.button_open_camera_menu)
        self.button_open_pattern_menu = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_open_pattern_menu.sizePolicy().hasHeightForWidth())
        self.button_open_pattern_menu.setSizePolicy(sizePolicy)
        self.button_open_pattern_menu.setMaximumSize(QtCore.QSize(80, 80))
        self.button_open_pattern_menu.setObjectName("button_open_pattern_menu")
        self.horizontalLayout.addWidget(self.button_open_pattern_menu)
        self.button_open_image_menu = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_open_image_menu.sizePolicy().hasHeightForWidth())
        self.button_open_image_menu.setSizePolicy(sizePolicy)
        self.button_open_image_menu.setMaximumSize(QtCore.QSize(80, 80))
        self.button_open_image_menu.setObjectName("button_open_image_menu")
        self.horizontalLayout.addWidget(self.button_open_image_menu)
        interface_main.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(interface_main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 777, 21))
        self.menubar.setStyleSheet("background-color: rgb(90, 131, 151);")
        self.menubar.setObjectName("menubar")
        interface_main.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(interface_main)
        self.statusbar.setStyleSheet("background-color: rgb(90, 131, 151);")
        self.statusbar.setObjectName("statusbar")
        interface_main.setStatusBar(self.statusbar)

        self.retranslateUi(interface_main)
        QtCore.QMetaObject.connectSlotsByName(interface_main)

    def retranslateUi(self, interface_main):
        _translate = QtCore.QCoreApplication.translate
        interface_main.setWindowTitle(_translate("interface_main", "MainWindow"))
        self.button_open_camera_menu.setText(_translate("interface_main", "Open camera"))
        self.button_open_pattern_menu.setText(_translate("interface_main", "Pattern"))
        self.button_open_image_menu.setText(_translate("interface_main", "Open image"))
import icon_resource_rc
import image_resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interface_main = QtWidgets.QMainWindow()
    ui = Ui_interface_main()
    ui.setupUi(interface_main)
    interface_main.show()
    sys.exit(app.exec_())