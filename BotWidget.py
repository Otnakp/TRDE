from PyQt6.QtWidgets import QWidget,QComboBox,QLineEdit, QVBoxLayout, QLabel,QPushButton, QSizePolicy,QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView
from Bots import Bots
import inspect

class BotSelectorWidget(QWidget):
    def __init__(self):
        super(BotSelectorWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.lw_bots = QListWidget()
        self.bots = dict(inspect.getmembers(Bots, inspect.isfunction))
        self.l_title = QLabel("Bots")
        self.l_title.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.t_search = QLineEdit()
        self.t_search.textChanged.connect(self.search)
        for k in self.bots:
            self.lw_bots.addItem(QListWidgetItem(k))
        
        self.layout.addWidget(self.l_title)
        self.layout.addWidget(self.t_search)
        self.layout.addWidget(self.lw_bots)
        self.setLayout(self.layout)
    
    def search(self):
        res = [i for i,v in enumerate(self.bots.keys()) if v.lower().startswith(self.t_search.text().lower())]
        if res == []:
            self.t_search.setStyleSheet("color:red")
        else:
            self.t_search.setStyleSheet("")
            self.lw_bots.scrollToItem(self.lw_bots.item(res[0]))
