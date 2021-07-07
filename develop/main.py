import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from PyQt5.QtGui import QFont, QKeySequence, QPixmap

from interface_main import Ui_interface_main


class Ui_interface_main(QMainWindow, Ui_interface_main):
    def __init__(self, parent=None):
        super().__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    main = Ui_interface_main()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


