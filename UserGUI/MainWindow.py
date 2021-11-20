import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QApplication

from PostAnalyzer.UserGUI.FormBuilder import *

WINDOW_HEIGHT = 300
WINDOW_WIDTH = 300
WINDOW_NAME = 'Post Analyzer'
WINDOW_ICON_NAME = 'Images\\MainLogo.png'

MAIN_FONT = 'Times'
FONT_HEADER_SIZE = 13
FONT_BODY_SIZE = 8


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.build_skeleton_with_basic_settings()
        self.create_and_connect_grid()

    def build_skeleton_with_basic_settings(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle(WINDOW_NAME)
        self.setWindowIcon(QIcon(WINDOW_ICON_NAME))

    def create_and_connect_grid(self):
        self.main_grid = QGridLayout(self.centralWidget)
        form_builder_object = FormBuilder()
        self.main_grid.addWidget(form_builder_object, 0, 0, Qt.AlignTop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
