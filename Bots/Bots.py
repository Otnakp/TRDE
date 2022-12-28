"""
receive kwargs
df
start
end
fees
currency_1 = how much of curr 1 you have
currency_2 = how much of curr 2 you have
trading_amount = percentage of portfolio to invest every trade
returns sell-hold-buy array shb
every number in the shb is a real in the range -1, 1
-1 means that it sells with all the trading amount
0 means that it does nothing. 1 means that it buys with all the trading amount

returns also the final value (what would happen if it closed all positions)
"""

def bot1(**kwargs):
    df = kwargs['df'] # pandas df as created by the DataDownloader.py script
    start = kwargs['start']
    end = kwargs['end']
    exchange_fees = kwargs['fees'] # can be 0, 0.01 means 1% fee
    currency_1 = kwargs['currency_1'] # could be 0, maybe you have 0 btc
    currency_2 = kwargs['currency_2'] # could be 1000, maybe you have 1000 dollar
    # how much you want to spend per trade at max. This is a proportion, for example 0.1 of portfolio means 10%.
    trading_amount = kwargs['trading_amount'] 
    shb = []
    final_value = -1 
    holdings = []
    # actual bot logic. this is a stupid bot. buys if the price goes below 20k and 
    # sells if it goes above 40k
    data = df.iloc[start:end, 3].to_numpy() # open high low close volume, 3 = close
    for el in data:
        if el < 20000:
            # check if have money, then buy
            if currency_2 > 0:
                currency_1 += ((trading_amount - trading_amount*exchange_fees) * currency_2) / el
                currency_2 -= trading_amount * currency_2
                shb.append(1)
        elif el > 40000:
            # check if have money, then sell
            if currency_1 > 0:
                currency_2 += ((trading_amount - trading_amount*exchange_fees) * currency_1) * el
                currency_1 -= trading_amount*currency_1
                shb.append(-1)
        else:
            shb.append(0)
        holdings.append((currency_1, currency_2))

    final_value = currency_1 * data[-1] + currency_2 # final value expressed in curr 2
    return shb, final_value, holdings
    

def bot2(**kwargs):
    pass