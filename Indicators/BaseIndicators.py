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
    return pd.DataFrame(data = ma, index = index,columns=['MA10']), True

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
    return pd.DataFrame(data = ma, index = index, columns=['MA100']), True


def EMA100(**kwargs):
    back = 100
    df = kwargs['df']
    start = kwargs['start']
    end = kwargs['end']
    ema = df.iloc[start:end, 3].ewm(span = back).mean()
    ema.dropna(inplace = True)
    return pd.DataFrame(data = ema.values, index = ema.index, columns=['EMA100']), True

def BOLL(**kwargs):
    df = kwargs['df']
    start = kwargs['start']
    end = kwargs['end']
    n = 20
    m = 2

    high = df.iloc[start:end, 1].to_numpy()
    low = df.iloc[start:end, 2].to_numpy()
    close = df.iloc[start:end, 3].to_numpy()
    tp = (high + low + close) / 3

    ma = Utilities.moving_average(tp, n)
    ma = ma.reshape((ma.shape[0], 1))

    std_dev = Utilities.std_dev(tp, n)[n-1:]
    upper = ma + m * std_dev
    lower = ma - m * std_dev

    cols = ['BOLL upper', 'BOLL mid', 'BOLL lower']
    index = np.array(df.index[start + n - 1: end])
    m = np.c_[upper, ma, lower]
    return pd.DataFrame(data = m, index=index, columns=cols), True


def MACD(**kwargs):
    pass