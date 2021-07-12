import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
import numexpr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QShortcut, QLabel
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
        self.button_approximate.clicked.connect(self.approximate)
        self.button_rotation.clicked.connect(self.rotation_pattern)

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
            files = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select pattern', '', "Text files (*.txt)")

            if files[0] != list():
                pattern_shots = []
                data = []
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
        step_x = 1. / (float(self.textedit_rozx.toPlainText()) + 1)
        step_y = 1. / (float(self.textedit_rozy.toPlainText()) + 1)
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

        self.normalization_pattern()
        self.print_pattern()

    def approximate(self):
        pattern_x = []
        pattern_y = []
        function_y = self.textedit_formule_y.toPlainText()
        function_x = self.textedit_formule_x.toPlainText()
        x0 = (self.pattern[0][0] + self.pattern[0][-1]) / 2
        y0 = (self.pattern[1][0] + self.pattern[1][-1]) / 2

        for pattern_spot_x in self.pattern[0]:
            pattern_x.append(quad(lambda x: numexpr.evaluate(function_x), x0, pattern_spot_x)[0])

        for pattern_spot_y in self.pattern[1]:
            pattern_y.append(quad(lambda x: numexpr.evaluate(function_y), y0, pattern_spot_y)[0])

        self.pattern = np.array([pattern_x, pattern_y])
        self.normalization_pattern()
        self.print_pattern()

    def rotation_pattern(self):
        beta = float(self.textedit_beta.toPlainText()) * np.pi / 180
        alpha = float(self.textedit_alpha.toPlainText()) * np.pi / 180
        horizontal = float(self.textedit_horizontal.toPlainText())
        horizontal_shift = float(self.textedit_horizontalshift.toPlainText())
        vertical = float(self.textedit_vertical.toPlainText())
        vertical_shift = float(self.textedit_verticalshift.toPlainText())
        h0 = float(self.textedit_h0.toPlainText())
        d0 = float(self.textedit_d0.toPlainText())
        d1 = float(self.textedit_d1.toPlainText())

        self.pattern[0] *= horizontal / 2
        self.pattern[0] += horizontal_shift
        self.pattern[1] *= vertical / 2
        self.pattern[1] += vertical_shift

        self.pattern[0] = d0 * (self.pattern[0] + d1 * np.tan(beta))*np.cos(beta) /\
                          (d0 + (self.pattern[0] + d1 * np.tan(beta)) * np.sin(beta))
        self.pattern[1] = d0 * self.pattern[1] / (d0 + (self.pattern[0] + d1 * np.tan(beta)) * np.sin(beta))

        self.pattern[0] = d0 * (self.pattern[0] / (d0 - d1 / np.cos(alpha) - (h0 + self.pattern[1] - d1 * np.tan(alpha))
                                                   * np.sin(alpha) + d1))
        self.pattern[1] = d0 * (((h0 + self.pattern[1] - d1 * np.tan(alpha)) * np.cos(alpha) - h0) /
                                (d0 - d1 / np.cos(alpha) - (h0 + self.pattern[1] - d1 * np.tan(alpha))
                                 * np.sin(alpha) + d1))

        self.normalization_pattern()
        self.print_pattern()

    def normalization_pattern(self):
        self.pattern[0] -= (self.pattern[0].max() + self.pattern[0].min()) / 2
        self.pattern[1] -= (self.pattern[1].max() + self.pattern[1].min()) / 2
        self.pattern[0] /= np.abs(self.pattern[0]).max()
        self.pattern[1] /= np.abs(self.pattern[1]).max()

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
