from DataDownloader import DataDownloader
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPalette, QColor
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout
from PyQt6.QtGui import QPalette, QColor

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")

        layout = QGridLayout()

        layout.addWidget(DataDownloader(), 0, 0)

        layout.addWidget(Color("green"), 0, 1)
        layout.addWidget(Color('green'), 0, 2)
        layout.addWidget(Color('blue'), 1, 0)
        layout.addWidget(Color('purple'), 1, 1)
        layout.addWidget(Color('purple'), 1, 2)


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.showMaximized()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
