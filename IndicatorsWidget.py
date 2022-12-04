from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox,QLineEdit, QVBoxLayout, QLabel,QPushButton, QSizePolicy,QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal,QModelIndex
from pathlib import Path
import inspect
import Indicators.BaseIndicators as BaseIndicators
import Indicators.PersonalizedIndicators as PersonalizedIndicators
"""
A class to handle the Indicators widget. Define your personalized
indicators in Indicators/PersonalizedIndicators.py as function.
"""

class IndicatorsWidget(QWidget):
    def __init__(self):
        super(IndicatorsWidget, self).__init__()
        Path("Indicators").mkdir(parents=True, exist_ok=True)
        self.layout = QHBoxLayout()
        self.lw_base_indicators = QListWidget()
        self.lw_personalized_indicators = QListWidget()
        self.base_indicators = dict(inspect.getmembers(BaseIndicators, inspect.isfunction))
        self.personalized_indicators = dict(inspect.getmembers(PersonalizedIndicators, inspect.isfunction))
        self.base_indicators_qitems = []
        self.personalized_indicators_qitems = []

        self.t_search_base = QLineEdit()
        self.t_search_personalized = QLineEdit()

        self.l_base_indicators = QLabel("Base Indicators")
        self.l_personalized_indicators = QLabel("Personalized Indicators")

        for k in self.base_indicators:
            item = QListWidgetItem(k)
            self.lw_base_indicators.addItem(item)
        for k in self.personalized_indicators:
            self.lw_personalized_indicators.addItem(QListWidgetItem(k))
        
        self.lw_personalized_indicators.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.lw_base_indicators.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        
        #self.title_layout = QHBoxLayout()
        #self.title_layout.addWidget(self.l_base_indicators)
        #self.title_layout.addWidget(self.l_personalized_indicators)

        #self.search_layout = QHBoxLayout()
        #self.search_layout.addWidget(self.t_search_base)
        #self.search_layout.addWidget(self.t_search_personalized)

        #self.list_view_layout = QHBoxLayout()
        #self.list_view_layout.addWidget(self.lw_base_indicators)
        #self.list_view_layout.addWidget(self.lw_personalized_indicators)

        self.base = QVBoxLayout()
        self.base.addWidget(self.l_base_indicators)
        self.base.addWidget(self.t_search_base)
        self.base.addWidget(self.lw_base_indicators)

        self.personalized = QVBoxLayout()
        self.personalized.addWidget(self.l_personalized_indicators)
        self.personalized.addWidget(self.t_search_personalized)
        self.personalized.addWidget(self.lw_personalized_indicators)
        
        self.t_search_base.textChanged.connect(self.search_in_base_indicators)
        self.t_search_personalized.textChanged.connect(self.search_in_personalized_indicators)

        #self.layout.addLayout(self.title_layout)
        #self.layout.addLayout(self.search_layout)
        #self.layout.addLayout(self.list_view_layout)

        self.layout.addLayout(self.base)
        self.layout.addLayout(self.personalized)
        
        self.setLayout(self.layout)
    
    def search_in_base_indicators(self):
        res = [i for i,v in enumerate(self.base_indicators.keys()) if v.lower().startswith(self.t_search_base.text().lower())]
        if res == []:
            self.t_search_base.setStyleSheet("color:red")
        else:
            self.t_search_base.setStyleSheet("")
            self.lw_base_indicators.scrollToItem(self.lw_base_indicators.item(res[0]))
            #self.lw_base_indicators.item(res[0]).setSelected(True)
            
    def search_in_personalized_indicators(self):
        res = [i for i,v in enumerate(self.personalized_indicators.keys()) if v.lower().startswith(self.t_search_personalized.text().lower())]
        if res == []:
            self.t_search_personalized.setStyleSheet("color:red")
        else:
            self.t_search_personalized.setStyleSheet("")
            self.lw_personalized_indicators.scrollToItem(self.lw_base_indicators.item(res[0]))
    