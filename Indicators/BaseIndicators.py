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

'start': index where to start from
'end': index where to end from
"""
import pandas as pd
import numpy as np
import Utilities
def MA10(**kwargs):
    # moving average 10
    back = 10
    df = kwargs['df'] # pandas df as created by the DataDownloader.py script
    start = kwargs['start']
    end = kwargs['end']
    #ma = df.iloc[start:end, 3].rolling(window=back).mean()# 3 is close
    ma = df.iloc[start:end, 3].to_numpy()
    ma = Utilities.moving_average(ma, back)
    index = np.array(df.index[start + back - 1: end])
    return pd.DataFrame(data = ma, index = index)

def MA100(**kwargs):
    # moving average 10
    back = 100
    df = kwargs['df'] # pandas df as created by the DataDownloader.py script
    start = kwargs['start']
    end = kwargs['end']
    #ma = df.iloc[start:end, 3].rolling(window=back).mean()# 3 is close
    ma = df.iloc[start:end, 3].to_numpy()
    ma = Utilities.moving_average(ma, back)
    index = np.array(df.index[start + back - 1: end])
    return pd.DataFrame(data = ma, index = index)


def EMA100(**kwargs):
    back = 100
    df = kwargs['df']
    start = kwargs['start']
    end = kwargs['end']
    ema = df.iloc[start:end, 3].ewm(span = back).mean()
    ema.dropna(inplace = True)
    return pd.DataFrame(data = ema.values, index = ema.index)

def BOLL(**kwargs):
    pass

