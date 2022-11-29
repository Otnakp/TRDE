from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QVBoxLayout, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal

class AllTfsDownloader(QThread):
    finished = pyqtSignal()
    def __init__(self, fdr, ticker):
        super(AllTfsDownloader, self).__init__()
        self.fdr = fdr
        self.ticker = ticker

    def run(self):
        self.fdr.retrieve_all_tfs(ticker = self.ticker, save = True)
        self.finished.emit()

class TfDownloaderWorker(QThread):
    finished = pyqtSignal()
    def __init__(self, fdr, tf, ticker):
        super(TfDownloaderWorker, self).__init__()
        self.fdr = fdr
        self.tf = tf
        self.ticker = ticker

    def run(self):
        self.fdr.retrieve_all_data(tf=self.tf, ticker = self.ticker, save = True)
        self.finished.emit()


class DataDownloader(QWidget):
    def __init__(self):
        super(DataDownloader, self).__init__()
        self.fdr = FDR()
        layout = QVBoxLayout()
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

        layout.addWidget(self.markets_combo)
        layout.addWidget(self.tfs_combo)
        layout.addWidget(self.b_download_selected)
        layout.addWidget(self.b_download_all_tfs)
        self.setLayout(layout)
    
    def download_selected_tf(self):
        self.thread = QThread()
        ticker = self.markets_combo.currentText()
        tf = self.tfs_combo.currentText()
        self.worker = TfDownloaderWorker(fdr = self.fdr, tf = tf, ticker = ticker)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.b_download_selected.setEnabled(False)
        self.b_download_all_tfs.setEnabled(False)
        self.thread.start()
        self.thread.finished.connect(lambda: self.enable_buttons())
    
    def enable_buttons(self):
        self.b_download_selected.setEnabled(True)
        self.b_download_all_tfs.setEnabled(True)

    def retrieve_all_timeframes(self):
        self.thread = QThread()
        ticker = self.markets_combo.currentText()
        self.worker = AllTfsDownloader(fdr = self.fdr, ticker=ticker)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.b_download_selected.setEnabled(False)
        self.b_download_all_tfs.setEnabled(False)
        self.thread.start()
        self.thread.finished.connect(lambda: self.enable_buttons())
