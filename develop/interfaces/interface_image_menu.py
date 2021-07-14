# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_image_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface_image_menu(object):
    def setupUi(self, interface_image_menu):
        interface_image_menu.setObjectName("interface_image_menu")
        interface_image_menu.resize(674, 720)
        interface_image_menu.setStyleSheet("QWidget#centralwidget_image_menu{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:1 rgb(113, 139, 152), stop:0 rgb(40, 75, 92));}\n"
"\n"
"")
        self.centralwidget_image_menu = QtWidgets.QWidget(interface_image_menu)
        self.centralwidget_image_menu.setObjectName("centralwidget_image_menu")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget_image_menu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_work = QtWidgets.QWidget(self.centralwidget_image_menu)
        self.widget_work.setObjectName("widget_work")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_work)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_image_in = QtWidgets.QWidget(self.widget_work)
        self.widget_image_in.setObjectName("widget_image_in")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_image_in)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.companovka_image_in = QtWidgets.QVBoxLayout()
        self.companovka_image_in.setObjectName("companovka_image_in")
        self.verticalLayout_2.addLayout(self.companovka_image_in)
        self.gridLayout.addWidget(self.widget_image_in, 0, 0, 1, 1)
        self.widget_image_out = QtWidgets.QWidget(self.widget_work)
        self.widget_image_out.setObjectName("widget_image_out")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_image_out)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.companovka_image_out = QtWidgets.QVBoxLayout()
        self.companovka_image_out.setObjectName("companovka_image_out")
        self.verticalLayout_3.addLayout(self.companovka_image_out)
        self.gridLayout.addWidget(self.widget_image_out, 1, 0, 1, 1)
        self.widget_controle = QtWidgets.QWidget(self.widget_work)
        self.widget_controle.setMaximumSize(QtCore.QSize(200, 16777215))
        self.widget_controle.setObjectName("widget_controle")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_controle)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.widget_controle)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton)
        self.gridLayout.addWidget(self.widget_controle, 0, 1, 2, 1)
        self.verticalLayout.addWidget(self.widget_work)
        interface_image_menu.setCentralWidget(self.centralwidget_image_menu)
        self.menubar = QtWidgets.QMenuBar(interface_image_menu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 674, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        interface_image_menu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(interface_image_menu)
        self.statusbar.setObjectName("statusbar")
        interface_image_menu.setStatusBar(self.statusbar)
        self.action_open_image = QtWidgets.QAction(interface_image_menu)
        self.action_open_image.setObjectName("action_open_image")
        self.action_save_image = QtWidgets.QAction(interface_image_menu)
        self.action_save_image.setObjectName("action_save_image")
        self.menu_file.addAction(self.action_open_image)
        self.menu_file.addAction(self.action_save_image)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslateUi(interface_image_menu)
        QtCore.QMetaObject.connectSlotsByName(interface_image_menu)

    def retranslateUi(self, interface_image_menu):
        _translate = QtCore.QCoreApplication.translate
        interface_image_menu.setWindowTitle(_translate("interface_image_menu", "MainWindow"))
        self.pushButton.setText(_translate("interface_image_menu", "some button"))
        self.menu_file.setTitle(_translate("interface_image_menu", "File"))
        self.action_open_image.setText(_translate("interface_image_menu", "Open image"))
        self.action_save_image.setText(_translate("interface_image_menu", "Save image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interface_image_menu = QtWidgets.QMainWindow()
    ui = Ui_interface_image_menu()
    ui.setupUi(interface_image_menu)
    interface_image_menu.show()
    sys.exit(app.exec_())
