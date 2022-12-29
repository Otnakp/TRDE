# TRDE - create and test crypto bots fast
Download crypto financial data. Setup your own personalized indicators. Plot the data. Create your bots and simulate them on the financial data.
To use the GUI please clone the repo and install the needed libraries from `requirements.txt`. This program was developed with python 3.10.6, but it will probably work with lower versions too.
## Download
![download](/images/download.png "Download")
Download cryptocurrency data from Binance. Select the pair, select the time frame and click "Download or Update". **Be careful** that this has two main issues:

 - Downloading the 1 minute data is extremely slow because Binance throttles the requests. Leave it there and just wait, it will end eventually
 - There are dropped candles for the 1m (and maybe 3m) candles. I haven't figured out this yet, it could be a problem with long downloads. Please contribute!

You can also download or update all the data. The "or update" part means that if you already downloaded it all it won't download it all over again, it will just get the latest candles. The data is stored in the `/data` folder.
## Indicators
![indicators](/images/indicators.png "Indicators")
Select the indicators you would like to plot. You can select multiple or none. You can choose from the base indicators column or the personalized indicators column.
### Write your own indicators
Go in `Indicators/PersonalizedIndicators.py` and add a function. That will be your new indicator. To see examples go in `Indicators/BaseIndicators.py`. Your personalized indicator must return a list containing plotly `graph_object` entries and if the indicator stays on the main window (where the candles are) or below (for example the volume or MACD). Check out this example for exponential moving average. 
```python
def  EMA100(**kwargs):
	back  =  100
	df  =  kwargs['df']
	start  =  kwargs['start']
	end  =  kwargs['end']
	ema  =  df.iloc[start:end, 3].ewm(span  =  back).mean()
	ema.dropna(inplace  =  True)
	df  =  pd.DataFrame(data  =  ema.values, index  =  ema.index, 	columns=['EMA100'])
	data  = [go.Scatter(x  =  pd.to_datetime(df.index, unit='ms'), y  =  df.iloc[:,0], opacity  =  0.8, line=dict(width=2), name  =  "EMA100")]
	return  data, True # data and True because it stays on main window
```
## Plotting
![plot](/images/plot.png  "Plot")
Select the starting candle (by modifying it you will also see the date) and the amount of candles you want to plot. By default the maximum number is 3000 but you can change it in the `config.json`. This will also plot the indicators you have selected.
## Bots
![bots](/images/bots.png  "Bots")
Build your own bot in `Bots/Bots.py` where you can also find an example. In the GUI select the amount of currency you want to give to your bot and the exchange fees, then press simulate.
## Disclaimer
Nothing here is financial advice. Do your own research. Only invest what you can afford to lose. Investing may result in loss of all your money.


