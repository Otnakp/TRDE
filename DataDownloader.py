from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QVBoxLayout, QPushButton, QLabel, QSizePolicy
from PyQt6.QtCore import QThread, pyqtSignal
from pathlib import Path
import Utilities

class AllTfsDownloader(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(float)
    string_progress = pyqtSignal(str)
    def __init__(self, fdr, ticker):
        super(AllTfsDownloader, self).__init__()
        self.fdr = fdr
        self.ticker = ticker

    def run(self):
        self.fdr.retrieve_all_tfs(ticker = self.ticker, save = True, progress = self.progress, string_progress = self.string_progress)
        self.finished.emit()

class TfDownloaderWorker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(float)
    def __init__(self, fdr, tf, ticker):
        super(TfDownloaderWorker, self).__init__()
        self.fdr = fdr
        self.tf = tf
        self.ticker = ticker

    def run(self):
        self.fdr.retrieve_all_data(tf=self.tf, ticker = self.ticker, save = True, progress = self.progress)
        self.finished.emit()

class DataDownloader(QWidget):
    def __init__(self):
        super(DataDownloader, self).__init__()
        self.fdr = FDR()
        self.layout = QVBoxLayout()
        self.tfs_combo = QComboBox()
        self.markets_combo = QComboBox()
        for tf in self.fdr.tfs:
            self.tfs_combo.addItem(tf)
        self.markets_combo.addItems(self.fdr.markets)
        self.markets_combo.setEditable(True)

        self.b_download_selected = QPushButton("Download or Update")
        self.b_download_all_tfs = QPushButton("Download or Update all TFs")

        self.b_download_selected.pressed.connect(self.download_selected_tf)
        self.b_download_all_tfs.pressed.connect(self.retrieve_all_timeframes)

        self.l_download_status = QLabel("")
        self.l_downloading = QLabel("")
        self.l_ticker_tf_report = QLabel("")
        self.l_download_status.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.l_downloading.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.l_ticker_tf_report.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)

        self.markets_combo.currentTextChanged.connect(self.check_downloaded)
        self.tfs_combo.currentTextChanged.connect(self.check_downloaded)

        self.market_layout = QVBoxLayout()
        self.market_layout.addWidget(self.markets_combo)
        self.market_layout.addWidget(self.tfs_combo)
        self.market_layout.addWidget(self.l_download_status)

        self.layout.addLayout(self.market_layout)
        self.layout.addWidget(self.b_download_selected)
        self.layout.addWidget(self.b_download_all_tfs)
        self.layout.addWidget(self.l_downloading)
        self.layout.addWidget(self.l_ticker_tf_report)
        self.setLayout(self.layout)
        self.check_downloaded()
    
    def download_selected_tf(self):
        self.thread = QThread()
        self.start_download()
        ticker = self.markets_combo.currentText()
        tf = self.tfs_combo.currentText()
        self.worker = TfDownloaderWorker(fdr = self.fdr, tf = tf, ticker = ticker)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_download_progress)
        self.b_download_selected.setEnabled(False)
        self.b_download_all_tfs.setEnabled(False)
        self.thread.start()
        self.thread.finished.connect(lambda: self.download_ended())
    
    def download_ended(self):
        self.b_download_selected.setEnabled(True)
        self.b_download_all_tfs.setEnabled(True)
        self.check_downloaded()
        self.l_downloading.setText("Downloaded!")

    def retrieve_all_timeframes(self):
        self.thread = QThread()
        self.start_download()
        ticker = self.markets_combo.currentText()
        self.worker = AllTfsDownloader(fdr = self.fdr, ticker=ticker)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_download_progress)
        self.worker.string_progress.connect(self.report_downloading_ticker_tf)
        self.b_download_selected.setEnabled(False)
        self.b_download_all_tfs.setEnabled(False)
        self.thread.start()
        self.thread.finished.connect(lambda: self.download_ended())

    def start_download(self):
        self.l_downloading.setText("Download Starting...")

    def get_current_config(self):
        ticker = self.markets_combo.currentText()
        tf = self.tfs_combo.currentText()
        return ticker, tf

    def check_downloaded(self):
        try:
            open(self.get_path()).close()
            self.l_download_status.setText("Present")
            self.l_download_status.setStyleSheet("color:green")
        except Exception:
            self.l_download_status.setText("Not Downloaded")
            self.l_download_status.setStyleSheet("color:red")
    
    def get_path(self):
        return Path("data") / Path(self.markets_combo.currentText().replace("/","_").upper()) / Path(self.tfs_combo.currentText()+'.csv')

    def report_download_progress(self, ms):
        self.l_downloading.setText(f"Got until {Utilities.ms_to_datetime(ms)}")

    def report_downloading_ticker_tf(self, s):
        self.l_ticker_tf_report.setText(s)
