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

def MA100(**kwargs):
    pass

def EMA100(**kwargs):
    pass

def BOLL(**kwargs):
    pass

