from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
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
        self.lw_personalized_indicators = QListWidget();
        self.base_indicators = dict(inspect.getmembers(BaseIndicators, inspect.isfunction))
        self.personalized_indicators = dict(inspect.getmembers(PersonalizedIndicators, inspect.isfunction))
        
        for k in self.base_indicators:
            self.lw_base_indicators.addItem(k)
        for k in self.personalized_indicators:
            self.lw_personalized_indicators.addItem(k)
        
        self.lw_personalized_indicators.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.lw_base_indicators.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.layout.addWidget(self.lw_base_indicators)
        self.layout.addWidget(self.lw_personalized_indicators)
        
        self.setLayout(self.layout)
