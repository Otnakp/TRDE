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

class SimulationResultWidget(QWidget):
    def __init__(self):
        super(SimulationResultWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.l_final = QLabel("Final")
        self.t_final = QLineEdit()
        self.final = QHBoxLayout()
        self.final.addWidget(self.l_final)
        self.final.addWidget(self.t_final)
        self.layout.addLayout(self.final)
        self.setLayout(self.layout)
    
    def set_result(self, final_amount):
        self.t_final.setText(str(final_amount))
