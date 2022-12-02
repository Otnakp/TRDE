from DataDownloader import DataDownloader
from IndicatorsWidget import IndicatorsWidget
from DataPlotterWidget import DataPlotterWidget
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtGui import QPalette, QColor
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy
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
        self.data_downloader_widget = DataDownloader()
        self.indicators_widget = IndicatorsWidget()
        self.data_plotter_widget = DataPlotterWidget(self.data_downloader_widget)
        #self.data_downloader_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #self.indicators_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        #self.data_plotter_widget.setSizePolicy(QSizePolicy.Policy.MinimumExpanding,QSizePolicy.Policy.MinimumExpanding)
        
        self.data_downloader_widget.tfs_combo.currentTextChanged.connect(self.data_plotter_widget.tf_changed)
        self.data_downloader_widget.markets_combo.currentTextChanged.connect(self.data_plotter_widget.market_changed)

        layout.addWidget(self.data_downloader_widget, 0, 0)

        layout.addWidget(self.indicators_widget, 0, 1)
        layout.addWidget(self.data_plotter_widget, 0, 2)
        layout.addWidget(IndicatorsWidget(), 1, 0)
        layout.addWidget(IndicatorsWidget(), 1, 1)
        layout.addWidget(IndicatorsWidget(), 1, 2)
        


        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.showMaximized()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
