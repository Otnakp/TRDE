import ccxt
from pathlib import Path
import pandas as pd


class FDR:
    def __init__(self):
        binance = ccxt.binance()
        self.tfs = binance.timeframes
        # self.tfs = ['1w', '1M'] for testing this is good
        self.markets_data = binance.load_markets()
        self.markets = list(self.markets_data.keys())

    def retrieve_all_data(self,ticker, tf, save = False, path = "data", verbose = False, date_index = False):
        if verbose:
            print("Starting")
        if ticker not in self.markets:
            raise ValueError(f"Cannot find {ticker}")
        if tf not in self.tfs:
            raise ValueError(f"Cannot find {tf}")
        binance = ccxt.binance()
        since = 1
        prev_since = since
        data = {} # Using a dictionary is good because it automatically removes duplicates
        if verbose:
            print(f"Starting to retrieve for {ticker}, tf: {tf}")
        while True:
            d = binance.fetch_ohlcv(ticker,tf,since=since,limit=1000)
            prev_since = since
            for candle in d:
                data[candle[0]] = candle[1:]
                since = candle[0]
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
                return df
    
    def retrieve_all_tfs(self,ticker, save = False, path = "data", verbose = False):
        for tf in self.tfs:
            self.retrieve_all_data(ticker = ticker, tf = tf, path = path, save = save, verbose = verbose)
    