import datetime
from bisect import bisect_left
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