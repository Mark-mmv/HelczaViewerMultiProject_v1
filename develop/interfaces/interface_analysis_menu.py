# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface_analysis_menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface_analysis_menu(object):
    def setupUi(self, interface_analysis_menu):
        interface_analysis_menu.setObjectName("interface_analysis_menu")
        interface_analysis_menu.resize(590, 439)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/icon2.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        interface_analysis_menu.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(interface_analysis_menu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.companovka = QtWidgets.QGridLayout()
        self.companovka.setObjectName("companovka")
        self.verticalLayout.addLayout(self.companovka)

        self.retranslateUi(interface_analysis_menu)
        QtCore.QMetaObject.connectSlotsByName(interface_analysis_menu)

    def retranslateUi(self, interface_analysis_menu):
        _translate = QtCore.QCoreApplication.translate
        interface_analysis_menu.setWindowTitle(_translate("interface_analysis_menu", "Analysis menu"))
import icon_resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interface_analysis_menu = QtWidgets.QDialog()
    ui = Ui_interface_analysis_menu()
    ui.setupUi(interface_analysis_menu)
    interface_analysis_menu.show()
    sys.exit(app.exec_())
