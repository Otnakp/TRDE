from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QGridLayout, QVBoxLayout, QPushButton

#data = pd.read_csv("data/BTC_USDT/1d.csv",index_col = 0,parse_dates=True)

class DataDownloader(QWidget):
    def __init__(self):
        super(DataDownloader, self).__init__()
        fdr = FDR()
        layout = QVBoxLayout()
        tfs_combo = QComboBox()
        markets_combo = QComboBox()
        for tf in fdr.tfs:
            tfs_combo.addItem(tf)
        markets_combo.addItems(fdr.markets)

        layout.addWidget(markets_combo)
        layout.addWidget(tfs_combo)

        self.setLayout(layout)
