from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QSizePolicy, QVBoxLayout,QLabel, QLineEdit,QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView, QCalendarWidget
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, QRunnable, QThreadPool
from pathlib import Path
import inspect
import datetime
import plotly.graph_objects as go
import Indicators.BaseIndicators as BaseIndicators
import json
import Indicators.PersonalizedIndicators as PersonalizedIndicators
from DataDownloader import DataDownloader
import Indicators.BaseIndicators as BaseIndicators
import Indicators.PersonalizedIndicators as PersonalizedIndicators

"""
plots the data
"""

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
    def __init__(self, df_getter, data_downloader, t_max_candles, config):
        super(PlotRunnable, self).__init__()
        self.data_downloader = data_downloader
        self.t_max_candles = t_max_candles
        self.config = config
        self.df_getter = df_getter

    def run(self):
        try:
            df = self.df_getter.get_df()
            l = get_candles_num(df, t_max_candles=self.t_max_candles, config = self.config)
            fig = go.Figure(data = [go.Candlestick(x=pd.to_datetime(df.index[-l:], unit='ms'),
                                    open = df.iloc[-l:,0], high = df.iloc[-l:,1], 
                                    low = df.iloc[-l:,2], close = df.iloc[-l:,3])])
            fig.show()
        except Exception as e:
            print(e)

class ChangeTextDateRunnable(QRunnable):
    def __init__(self, df_getter,data_downloader, t_max_candles, config, t_start_date, t_end_date):
        super(ChangeTextDateRunnable, self).__init__()
        self.df_getter = df_getter
        self.data_downloader = data_downloader
        self.t_max_candles = t_max_candles
        self.config = config
        self.t_start_date = t_start_date
        self.t_end_date = t_end_date
        
    def run(self):
        try:
            df = self.df_getter.get_df()
            l = get_candles_num(df = df, t_max_candles=self.t_max_candles, config = self.config)
            self.t_start_date.setText(str(ms_to_datetime(df.index[-1])))
            self.t_end_date.setText(str(ms_to_datetime(df.index[-l])))
        except Exception as e:
            self.t_end_date.setText("DD/MM/YYYY")
            self.t_start_date.setText("DD/MM/YYYY")
            print(e)

class DataPlotterWidget(QWidget):
    def __init__(self, data_downloader):
        super(DataPlotterWidget, self).__init__()
        self.config = json.load(open("config.json"))
        self.data_downloader = data_downloader
        self.layout = QVBoxLayout()
        self.default_num_candles = 2000
        self.df_getter = DfGetter(self.data_downloader)

        #self.start_calendar = QCalendarWidget()
        #self.stop_calendar = QCalendarWidget()
        #self.calendar_layout = QVBoxLayout()
        #self.start_calendar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #self.stop_calendar.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #self.calendar_layout.addWidget(self.start_calendar)
        #self.calendar_layout.addWidget(self.stop_calendar)
        #self.layout.addLayout(self.calendar_layout)

        self.t_start_date = QLineEdit("DD/MM/YYYY")
        self.t_end_date = QLineEdit("DD/MM/YYYY")
        try:
            df = self.df_getter.get_df()
            self.t_start_date.setText(str(ms_to_datetime(df.index[-1])))
        except Exception as e:
            print(e)

        self.date_layout = QVBoxLayout()
        self.date_layout.addWidget(self.t_start_date)
        self.date_layout.addWidget(self.t_end_date)
        self.layout.addLayout(self.date_layout)

        self.t_max_candles = QLineEdit(str(self.default_num_candles))
        self.t_max_candles.textChanged.connect(self._change_dates)
        self.b_plot = QPushButton("PLOT")
        self.b_plot.pressed.connect(self.plot)
        self.in_layout = QHBoxLayout()
        self.in_layout.addWidget(QLabel("Max candles"))
        self.in_layout.addWidget(self.t_max_candles)
        self.layout.addLayout(self.in_layout)
        self.layout.addWidget(self.b_plot)
        self.setLayout(self.layout)

    def plot(self):
        runnable = PlotRunnable(df_getter = self.df_getter, data_downloader=self.data_downloader, t_max_candles=self.t_max_candles, config=self.config)
        QThreadPool.globalInstance().start(runnable)
    
    def _change_dates(self):
        runnable = ChangeTextDateRunnable(df_getter = self.df_getter, data_downloader=self.data_downloader, t_max_candles=self.t_max_candles, config=self.config, t_start_date=self.t_start_date, t_end_date=self.t_end_date)
        QThreadPool.globalInstance().start(runnable)

    def tf_changed(self, t):
        self._change_dates()
        
    def market_changed(self, a):
        self._change_dates()
