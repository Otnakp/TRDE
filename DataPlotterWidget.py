from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QVBoxLayout,QLabel, QLineEdit,QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from pathlib import Path
import inspect
import plotly.graph_objects as go
import Indicators.BaseIndicators as BaseIndicators
import Indicators.PersonalizedIndicators as PersonalizedIndicators
from DataDownloader import DataDownloader
import Indicators.BaseIndicators as BaseIndicators
import Indicators.PersonalizedIndicators as PersonalizedIndicators

"""
plots the data
"""

class DataPlotterWidget(QWidget):
    def __init__(self, data_downloader):
        super(DataPlotterWidget, self).__init__()
        self.data_downloader = data_downloader
        self.layout = QVBoxLayout()
        self.t_max_candles = QLineEdit("2000")
        self.b_plot = QPushButton("PLOT")
        self.b_plot.pressed.connect(self.plot)
        self.layout.addWidget(QLabel("Max candles"))
        self.layout.addWidget(self.t_max_candles)
        self.layout.addWidget(self.b_plot)
        self.setLayout(self.layout)

    def plot(self):
        ticker, tf = self.data_downloader.get_current_config()
        try:
            p = Path("data") / Path(ticker.replace('/', '_')) / Path(tf+'.csv')
            df = pd.read_csv(p,index_col = 0)
            l = len(df.index)
            l = l if l < int(self.t_max_candles.text()) else int(self.t_max_candles.text()) 
            fig = go.Figure(data = [go.Candlestick(x=pd.to_datetime(df.index[-l:], unit='ms'),
                                    open = df.iloc[-l:,0], high = df.iloc[-l:,1], 
                                    low = df.iloc[-l:,2], close = df.iloc[-l:,3])])
            fig.show()
        except Exception as e:
            print(e)

        