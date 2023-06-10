"""

            Trading Strategy using Bollinger Bands and RSI

            This program implements a simple trading strategy using 
            Bollinger Bands and Relative Strength Index (RSI) indicators. 
            The code utilizes the yfinance library to download historical stock data,
            pandas for data manipulation,
            numpy for numerical computations, ta for technical analysis indicators, 
            and matplotlib for data visualization.

"""


import yfinance as yf
import pandas as pd
import numpy as np
import ta
import matplotlib.pyplot as plt


#Download historical stock data:
df = yf.download('SQ', start='2019-01-01')

#Calculate Bollinger Bands:
print('calculating bollinger bands')
df['ma_20'] = df.Close.rolling(20).mean()
df['vol'] = df.Close.rolling(20).std()
df['upper_bb'] = df.ma_20 + (2*df.vol)
df['lower_bb'] = df.ma_20 - (2*df.vol)

#Plot Bollinger Bands:
df[['Close', 'ma_20', 'vol', 'upper_bb', 'lower_bb']].plot()


#Calculate RSI:
print('calculating rsi...')
df['rsi'] = ta.momentum.rsi(df.Close, window=6)


#Generate trading signals based on RSI and Bollinger Bands:
conditions = [(df.rsi < 30) & (df.Close < df.lower_bb),
              (df.rsi > 70) & (df.Close > df.upper_bb)]
choices = ['Buy', 'Sell']
print('this will contain signals')
df['signal'] = np.select(conditions, choices)


#Process and visualize the trading signals:
df.dropna(inplace=True)
df.signal = df.signal.shift()
df['shifted_Close'] = df.Close.shift()

position = False
buydate, selldates = [],[]
buyprices, sellprices = [],[]

for index, row in df.iterrows():
    if not position and row['signal'] == 'Buy':
        buydate.append(index)
        buyprices.append(row.Open)
        position = True
        
    if position:
        if row['signal'] == 'Sell' or row.shifted_Close < 0.98 * buyprices[-1]:
            selldates.append(index)
            sellprices.append(row.Open)
            position = False
        
plt.figure(figsize=(10,5))
plt.plot(df.Close)
plt.scatter(df.loc[buydate].index, df.loc[buydate].Close, marker='^', c='g')
plt.scatter(df.loc[selldates].index, df.loc[selldates].Close, marker='^', c='r')


#Calculate the overall return of the trading strategy:
return_percentage = (pd.Series([(sell - buy) / buy for sell, buy in zip(sellprices,buyprices)]) + 1).prod() - 1


"""The trading logic for the code you provided is as follows:

Bollinger Bands Calculation:

The code calculates the 20-day moving average (ma_20) of the closing prices.
It also calculates the standard deviation (vol) of the closing prices over the same 20-day period.
The upper Bollinger Band (upper_bb) is obtained by adding twice the standard deviation to the moving average.
The lower Bollinger Band (lower_bb) is obtained by subtracting twice the standard deviation from the moving average.
Relative Strength Index (RSI) Calculation:

The code calculates the RSI indicator using a window of 6 days and the closing prices.
Trading Signal Generation:

Based on the calculated RSI and Bollinger Bands, the code generates trading signals.
If the RSI is below 30 and the closing price is below the lower Bollinger Band, it generates a "Buy" signal.
If the RSI is above 70 and the closing price is above the upper Bollinger Band, it generates a "Sell" signal.
Trading Position and Logging:

The code processes the generated signals and maintains a trading position.
It initializes the position as False.
It keeps track of the buy date, sell dates, buy prices, and sell prices.
When a "Buy" signal is generated and there is no existing position, it logs the buy date and buy price, 
and updates the position to True.
While in a position, if a "Sell" signal is generated or the previous day's closing price drops below 98% of the last buy price, 
it logs the sell date and sell price, and updates the position to False.
Visualization:

The code plots the closing prices of the stock.
It also marks the buy dates with green triangles and the sell dates with red triangles on the plot.
The trading strategy aims to take advantage of potential price reversals indicated by low RSI values
and price deviations from the Bollinger Bands. It generates buy signals when the stock is deemed oversold (RSI < 30)
and the price is below the lower Bollinger Band, and sell signals when the stock is overbought (RSI > 70)
and the price is above the upper Bollinger Band.
Additionally, it considers selling if the stock price drops below 98% of the previous buy price."""