from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QSizePolicy, QVBoxLayout,QLabel, QLineEdit,QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView, QCalendarWidget
import PyQt6.QtWidgets as QtWidgets
from plotly.subplots import make_subplots
from PyQt6.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool
from pathlib import Path
import inspect
import numpy as np
import datetime
import plotly.graph_objects as go
import Indicators.BaseIndicators as BaseIndicators
import json
from bisect import bisect_left
import Utilities
import Indicators.PersonalizedIndicators as PersonalizedIndicators
from DataDownloader import DataDownloader
import Indicators.BaseIndicators as BaseIndicators
import Indicators.PersonalizedIndicators as PersonalizedIndicators

"""
plots the data
"""

base_time_string = "yyyy-mm-dd hh:mm:ss"
def ms_to_datetime(ms):
    return datetime.datetime.fromtimestamp(ms/1000.0)

class DfGetter:
    def __init__(self, data_downloader):
        ticker, tf = data_downloader.get_current_config()
        self.p = Path("data") / Path(ticker.replace('/', '_')) / Path(tf+'.csv')
        self.df = None
        self.data_downloader = data_downloader

    def get_df(self):
        ticker, tf = self.data_downloader.get_current_config()
        new_p = Path("data") / Path(ticker.replace('/', '_')) / Path(tf+'.csv')
        if new_p == self.p and self.df is not None:
            return self.df
        else:
            self.df = pd.read_csv(new_p,index_col = 0)
            self.p = new_p
            return self.df

def get_candles_num(df, t_max_candles, config):
    l = len(df.index)
    l = l if l < int(t_max_candles.text()) else int(t_max_candles.text()) 
    if l > int(config["max_candles"]):
        l = int(config["max_candles"])
        t_max_candles.setText(str(l))
    return l

class PlotRunnable(QRunnable):
    def __init__(self, df_getter, data_downloader, t_max_candles, config, t_start, indicators_widget):
        super(PlotRunnable, self).__init__()
        self.data_downloader = data_downloader
        self.t_max_candles = t_max_candles
        self.config = config
        self.df_getter = df_getter
        self.t_start = t_start
        self.indicators_widget = indicators_widget

    def run(self):
        try:
            df = self.df_getter.get_df()
            l = get_candles_num(df, self.t_max_candles, self.config)
            s = int(self.t_start.text())
            data = [go.Candlestick(x=pd.to_datetime(df.index[s:s+l], unit='ms'),
                                    open = df.iloc[s:s+l,0], high = df.iloc[s:s+l,1], 
                                    low = df.iloc[s:s+l,2], close = df.iloc[s:s+l,3], name = "Candles")]
            #fig = go.Figure(data = data)
            rows_graphs = []
            num_rows = 1
            for indicator in self.indicators_widget.lw_base_indicators.selectedItems():
                f = self.indicators_widget.base_indicators[indicator.text()]
                ind, on_main = f(df = df, start = s, end = s + l)
                rows_graphs.append((ind, on_main))
                num_rows += int(not on_main)
            fig = make_subplots(rows=num_rows, cols=1, shared_xaxes=True)
            fig.add_trace(data[0])
            fig.update_layout(xaxis_rangeslider_visible=False)
            row = 1
            for el in rows_graphs:
                ind, on_main = el
                if on_main:
                    for i in range(len(ind)):
                        fig.add_trace(ind[i], row = 1, col = 1)
                else:
                    row += 1
                    for i in range(len(ind)):
                        fig.add_trace(ind[i], row = row, col = 1)
            fig.show()
        except Exception as e:
            print(e)

class ChangeTextDateRunnable(QRunnable):
    def __init__(self, df_getter,data_downloader, t_max_candles, config):
        super(ChangeTextDateRunnable, self).__init__()
        self.df_getter = df_getter
        self.data_downloader = data_downloader
        self.t_max_candles = t_max_candles
        self.config = config
        
    def run(self):
        try:
            df = self.df_getter.get_df()
            l = get_candles_num(df = df, t_max_candles=self.t_max_candles, config = self.config)
        except Exception as e:
            print(e)

class DataPlotterWidget(QWidget):
    def __init__(self, data_downloader, indicators_widget):
        super(DataPlotterWidget, self).__init__()
        self.config = json.load(open("config.json"))
        self.data_downloader = data_downloader
        self.indicators_widget = indicators_widget
        self.layout = QVBoxLayout()
        self.default_num_candles = 2000

        self.df_getter = DfGetter(self.data_downloader)
        try:
            df = self.df_getter.get_df()
        except Exception as e:
            print(e)

        self.date_layout = QVBoxLayout()
        self.layout.addLayout(self.date_layout)
        self.t_start = QLineEdit("0")
        self.l_start_date = QLabel("")
        self.l_start_date.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

        self.t_max_candles = QLineEdit(str(self.default_num_candles))
        self.t_max_candles.textChanged.connect(self._change_dates)
        self.b_plot = QPushButton("PLOT")
        self.b_plot.pressed.connect(self.plot)
        self.candles_layout = QVBoxLayout()
        self.in_layout = QHBoxLayout()
        self.in_layout.addWidget(QLabel("Start"))
        self.in_layout.addWidget(self.t_start)
        self.in_layout.addWidget(QLabel("Amount"))
        self.in_layout.addWidget(self.t_max_candles)
        self.candles_layout.addLayout(self.in_layout)
        self.candles_layout.addWidget(self.l_start_date)
        #self.start_layout = QHBoxLayout()
        #self.start_layout.addWidget(QLabel("Start"))
        #self.start_layout.addWidget(self.t_start)
        #self.layout.addLayout(self.start_layout)
        self.layout.addLayout(self.candles_layout)
        self.layout.addWidget(self.b_plot)
        self.setLayout(self.layout)

        self.t_start.textChanged.connect(self.check_candle_start)


    def plot(self):
        runnable = PlotRunnable(df_getter = self.df_getter, data_downloader=self.data_downloader, t_max_candles=self.t_max_candles, config=self.config, t_start=self.t_start, indicators_widget = self.indicators_widget)
        QThreadPool.globalInstance().start(runnable)
    
    def _change_dates(self):
        runnable = ChangeTextDateRunnable(df_getter = self.df_getter, data_downloader=self.data_downloader, t_max_candles=self.t_max_candles, config=self.config)
        QThreadPool.globalInstance().start(runnable)

    def tf_changed(self, t):
        self._change_dates()
        
    def market_changed(self, a):
        self._change_dates()

    def recalculate_candles_num(self):
        # todo: need to recalculate the number of candles but
        # this needs to take into account the current time frame

        pass
    
    def check_candle_start(self):
        try:
            df = self.df_getter.get_df()
            if df is not None:
                l = get_candles_num(df, self.t_max_candles,self.config)
                if len(df.index) - l < int(self.t_start.text()):
                    self.t_start.setText(str(len(df.index) - l))
                self.l_start_date.setText(str(Utilities.ms_to_datetime(df.index[int(self.t_start.text())])))
        except Exception as e:
            print(e)
            self.l_start_date.setText("")

