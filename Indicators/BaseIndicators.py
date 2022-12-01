"""
**kwargs contains

'ticker': the coin ticker
'tf': time frame
'indicator_name': the name of the indicator
'path': path where to save
'save': if True save the indicator

'df': a pandas dataframe as downloaded y DataDownloader.py 
    the columns should be
    unix time ms
    open
    high
    low
    close
"""
import pandas as pd
def MA10(**kwargs):
    # moving average 10
    df = kwargs['df'] # pandas df as created by the DataDownloader.py script
    back = 10
    ma = df.rolling(30).mean()
    ma.dropna(inplace=True)

def indicator2(a):
    pass
def indicator3(a):
    pass
def indicator4(a):
    pass
def indicator5(a):
    pass
def indicator6(a):
    pass
def indicator7(a):
    pass
def indicator8(a):
    pass
def indicator9(a):
    pass
def indicator10(a):
    pass
def indicator11(a):
    pass
def indicator12(a):
    pass
def indicator13(a):
    pass
def indicator14(a):
    pass
def indicator15(a):
    pass
def indicator16(a):
    pass
def indicator17(a):
    pass
def indicator18(a):
    pass
def indicator19(a):
    pass
def indicator20(a):
    pass
