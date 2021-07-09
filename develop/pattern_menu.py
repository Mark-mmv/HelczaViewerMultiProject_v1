import sys
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from interfaces.interface_pattern_menu import Ui_interface_pattern_menu


class InterfacePatternMenu(QMainWindow, Ui_interface_pattern_menu):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        """Buttons"""
        self.button_import_pattern.clicked.connect(self.import_pattern)
        self.button_save_pattern.clicked.connect(self.save_pattern)
        self.button_create_pattern.clicked.connect(self.create_pattern)

        """Attributes"""
        self.pattern = np.array([])

        """Create canvas for showing pattern"""
        self.fig_pattern, self.axes_pattern = plt.subplots()
        self.canvas_pattern = FigureCanvas(self.fig_pattern)
        self.toolbar_pattern = NavigationToolbar(self.canvas_pattern, self)
        self.companovka_patern.addWidget(self.toolbar_pattern)
        self.companovka_patern.addWidget(self.canvas_pattern)

    def import_pattern(self):
        try:
            pattern_shots = []
            data = []
            files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select pattern', '', "Text files (*.txt)")

            for f in files[0]:
                file = open(f, 'r')
                data += file.readlines()
                file.close()
            for line in data:
                pattern_shots.append([float(line.split()[0]), float(line.split()[1])])

            self.pattern = np.array(pattern_shots).transpose()
            self.print_pattern()
        except:
            print('Import error')

    def save_pattern(self):
        try:
            if len(self.pattern[0]) >= 2500:
                number_file = int(len(self.pattern[0]) / 2)
                i = 2
            else:
                number_file = len(self.pattern[0])
                i = 1
            for cl in np.arange(0, i, 1):
                files = QtWidgets.QFileDialog.getSaveFileName(
                    self, 'Save', str(int(self.textedit_rozx.toPlainText())) + 'x' +
                                  str(int(self.textedit_rozy.toPlainText())) + '_pattern', '*.txt')

                file = open(str(files[0]), 'w')
                for cl2 in np.arange(number_file * cl, number_file * (cl + 1), 1):
                    file.write(str(self.pattern[0, cl2]))
                    file.write(str('    '))
                    file.write(str(self.pattern[1, cl2]))
                    file.write(str('\n'))
        except:
            print('Save error')

    def create_pattern(self):
        pattern_trace = [[0, 0]]
        pattern_shots = []
        step_x = 1. / float(self.textedit_rozx.toPlainText())
        step_y = 1. / float(self.textedit_rozy.toPlainText())
        position_current_x, position_current_y = (0., 0.)
        circle = False

        for _ in range(10**6):
            position_current_x += step_x
            position_current_y += step_y
            ifx = round(round(position_current_x, 6) - 1, 6)
            ify = round(round(position_current_y, 6) - 1, 6)
            if ifx == 0 or ifx == -2:
                position_current_x -= step_x
                position_current_y -= step_y
                step_x *= -1.
            elif ify == 0 or ify == -2:
                position_current_x -= step_x
                position_current_y -= step_y
                step_y *= -1.
            else:
                pattern_shots.append(
                    [(position_current_x + pattern_trace[-1][0])/2, (position_current_y + pattern_trace[-1][1])/2])
                pattern_trace.append([position_current_x, position_current_y])

            if round(position_current_x, 6) == 0 and round(position_current_y, 6) == 0:
                if circle is True:
                    break
                circle = True

        self.pattern = np.array(pattern_shots).transpose()
        self.pattern[0] /= self.pattern[0].max()
        self.pattern[1] /= self.pattern[1].max()
        self.print_pattern()

    def print_pattern(self):
        self.axes_pattern.clear()
        self.axes_pattern.plot([1, 1], [-1, 1], [-1, -1], [-1, 1], [-1, 1], [1, 1], [-1, 1], [-1, -1], color='k')
        self.axes_pattern.plot(self.pattern[0], self.pattern[1])
        self.axes_pattern.plot(self.pattern[0], self.pattern[1], '.')
        self.canvas_pattern.draw()


def main():
    app = QApplication(sys.argv)
    interface_main = InterfacePatternMenu()
    interface_main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
