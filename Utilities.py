import datetime
from bisect import bisect_left
import numpy as np
import pandas as pd
def ms_to_datetime(ms):
    return datetime.datetime.fromtimestamp(ms/1000.0)
    
def datetime_to_ms(d : str):
    dt_obj = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
    millisec = dt_obj.timestamp() * 1000
    return millisec

def BinarySearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

tf_to_sec = {'1m': 60, '3m': 3 * 60, '5m':5*60, '15m': 15 * 60, '30m': 30*60,
             '1h':60*60, '2h':2*60*60, '4h': 4*60*60, '6h':6*60*60,'8h': 8*60*60, '12h': 12*60*60,
             '1d': 24 * 60*60, '3d': 3 * 24 * 60 * 60,
             '1w': 7 * 24 * 60 * 60, '1M': 30*24*60*60 # 1 month is ambigous
            }

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def std_dev(a, n):
    index = np.array([i for i in range(len(a))])
    df = pd.DataFrame(data=a, index=index)
    std = df.rolling(n).std().values
    return std
