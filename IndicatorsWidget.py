from FinancialDataRetriever import FDR
import pandas as pd
from PyQt6.QtWidgets import QWidget,QComboBox, QVBoxLayout, QPushButton
from PyQt6.QtCore import QThread, pyqtSignal
from pathlib import Path
import inspect
import Indicators.BaseIndicators as BaseIndicators
import Indicators.PersonalizedIndicators as PersonalizedIndicators
"""
A class to handle the Indicators widget. Define your personalized
indicators as python scripts in the Indicators folder.
"""

class IndicatorsWidget(QWidget):
    def __init__(self):
        super(IndicatorsWidget, self).__init__()
        Path("Indicators").mkdir(parents=True, exist_ok=True)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QPushButton("Hi"))
        self.base_indicators = dict(inspect.getmembers(BaseIndicators, inspect.isfunction))
        self.personalized_indicators = dict(inspect.getmembers(PersonalizedIndicators, inspect.isfunction))

