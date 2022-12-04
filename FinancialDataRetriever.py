import ccxt
from pathlib import Path
import pandas as pd
class FDR:
    def __init__(self):
        binance = ccxt.binance()
        self.tfs = binance.timeframes
        self.markets_data = binance.load_markets()
        self.markets = list(self.markets_data.keys())
        self.tfs.pop('1s', None)
        # self.tfs = ['1w', '1M'] #for testing this is good

    def retrieve_all_data(self,ticker, tf, save = False, path = "data", verbose = True, date_index = False, progress = None, string_progress = None):
        if verbose:
            print("Starting")
        if ticker not in self.markets:
            raise ValueError(f"Cannot find {ticker}")
        if tf not in self.tfs:
            raise ValueError(f"Cannot find {tf}")
        d = 0
        binance = ccxt.binance()
        since = 1
        prev_since = since
        data = {} # Using a dictionary is good because it automatically removes duplicates
        try:
            df = pd.read_csv(Path(path) / Path(ticker.replace('/','_') / Path(tf+'.csv')), index_col = 0)
            since = df.index[-1]
            prev_since = since
            if progress is not None:
                progress.emit(since)
            data = df.T.to_dict("list")
        except Exception:
            if verbose:
                print("pass")
            pass # data has never been retrieved before
        if verbose:
            print(f"Starting to retrieve for {ticker}, tf: {tf}")
        while True:
            if string_progress is not None:
                string_progress.emit(f"{ticker} {tf}")
            d = binance.fetch_ohlcv(ticker,tf,since=since,limit=1000)
            prev_since = since
            for candle in d:
                data[candle[0]] = candle[1:]
                since = candle[0]
            if progress is not None:
                progress.emit(since)
            if prev_since == since:
                if verbose:
                    print(f"Done Retrieving.")
                df = pd.DataFrame.from_dict(data, orient='index')
                if date_index:
                    df.index = pd.to_datetime(df.index, unit='ms')
                    df = df.set_index(pd.to_datetime(df.index))
                    df.columns = ['Open', 'High', 'Low','Close','Volume']
                if save:
                    if verbose:
                        print("Saving...")
                    p = Path(path) / Path(ticker.replace('/','_'))
                    p.mkdir(parents=True, exist_ok=True)
                    p = p / Path(tf + '.csv')
                    df.to_csv(p)
                    if verbose:
                        print("Saved")
                return df
    
    def retrieve_all_tfs(self,ticker, save = False, path = "data", verbose = False, progress = None, string_progress = None):
        for tf in self.tfs:
            self.retrieve_all_data(ticker = ticker, tf = tf, path = path, save = save, verbose = verbose, progress = progress, string_progress=string_progress)
    