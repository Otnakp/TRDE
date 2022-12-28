from PyQt6.QtWidgets import QWidget,QComboBox,QLineEdit, QVBoxLayout, QLabel,QPushButton, QSizePolicy,QHBoxLayout, QListWidget, QListWidgetItem, QStackedLayout, QAbstractItemView
from PyQt6.QtCore import Qt
from Bots import Bots
from DataPlotterWidget import get_candles_num
import inspect

class BotSelectorWidget(QWidget):
    def __init__(self, data_plotter_widget, simulation_result_widget):
        super(BotSelectorWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.data_plotter_widget = data_plotter_widget
        self.simulation_result_widget = simulation_result_widget
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()
        self.lw_bots = QListWidget()
        self.bots = dict(inspect.getmembers(Bots, inspect.isfunction))
        self.l_title = QLabel("Bots")
        self.b_simulate = QPushButton("Simulate")
        self.t_fees = QLineEdit("0")
        self.fees = QHBoxLayout()
        self.fees.addWidget(QLabel("Fees"))
        self.fees.addWidget(self.t_fees)
        self.currency_1 = QHBoxLayout()
        self.t_currency_1 = QLineEdit("0")
        self.currency_1.addWidget(QLabel("Currency 1 amount"))
        self.currency_1.addWidget(self.t_currency_1)
        self.currency_2 = QHBoxLayout()
        self.t_currency_2 = QLineEdit("1000")
        self.currency_2.addWidget(QLabel("Currency 2 amount"))
        self.currency_2.addWidget(self.t_currency_2)
        self.b_simulate.pressed.connect(self.simulate)
        self.t_result = QLineEdit()
        #self.t_result.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
        self.t_result.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.l_title.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.t_search = QLineEdit()
        self.t_search.textChanged.connect(self.search)
        for k in self.bots:
            self.lw_bots.addItem(QListWidgetItem(k))
        
        self.left.addWidget(self.l_title)
        self.left.addWidget(self.t_search)
        self.left.addWidget(self.lw_bots)
        self.right.addLayout(self.fees)
        self.right.addLayout(self.currency_1)
        self.right.addLayout(self.currency_2)
        self.right.addWidget(self.b_simulate)
        #self.right.addWidget(self.t_result)
        self.up_layout = QHBoxLayout()
        self.up_layout.addLayout(self.left)
        self.up_layout.addLayout(self.right)
        self.down_layout = QHBoxLayout()
        #self.down_layout.addWidget(self.t_result)
        self.layout.addLayout(self.up_layout)
        self.layout.addLayout(self.down_layout)
        self.setLayout(self.layout)
    
    def search(self):
        res = [i for i,v in enumerate(self.bots.keys()) if v.lower().startswith(self.t_search.text().lower())]
        if res == []:
            self.t_search.setStyleSheet("color:red")
        else:
            self.t_search.setStyleSheet("")
            self.lw_bots.scrollToItem(self.lw_bots.item(res[0]))
    
    def simulate(self):
        try:
            # get df, start, end, fees, current bot, print result
            currency_1 = float(self.t_currency_1.text())
            currency_2 = float(self.t_currency_2.text())
            fees = float(self.t_fees.text()) # todo: add fee text field in this widget
            df = self.data_plotter_widget.df_getter.get_df()
            l = get_candles_num(df, self.data_plotter_widget.t_max_candles, self.data_plotter_widget.config)
            start = int(self.data_plotter_widget.t_start.text())
            end = start + l
            bot = self.bots[self.lw_bots.selectedItems()[0].text()]
            shb, final, holdings = bot(df = df, start = start, end = end, fees = fees, currency_1=currency_1, currency_2=currency_2, trading_amount = 0.1)
            self.simulation_result_widget.set_result(final)
        except Exception as e:
            print(e)
