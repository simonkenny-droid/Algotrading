import ccxt
import ta
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

symbol = 'BTC/USDT'
timeframe='1m'
delay = 2 # seconds
#connect to exchange
exchange = ccxt.binance()
#print(dir(exchange))

#markets and tickers
markets = exchange.load_markets()
"""for market in markets:
    print(market)"""

ticker = exchange.fetch_ticker(symbol)
#print(ticker)

#data
# Fetch OHLCV data
ohlcv = exchange.fetch_ohlcv(symbol, timeframe)

# Convert OHLCV data to a pandas DataFrame
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Print the DataFrame
#print(df)

#order_book = exchange.fetch_order_book(symbol)
"""
for symbol in exchange.markets:
    print (exchange.fetch_order_book (symbol))
    time.sleep (delay)"""


print ('supertrend indicator calculation ongoing..')
time.sleep (delay)
print('Before moving to Supertrend stratergy we have to first understand ATR')

df['ATR'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
#print(df)
time.sleep (delay)

print('now supertrend indicator calculation goes as stated below-')
Multiplier = 3

df['basic_upper_bands'] = (df['high']+df['low']) / 2 + Multiplier * df['ATR']
df['basic_lower_bands'] = (df['high']+df['low']) / 2 - Multiplier * df['ATR']
#print(df)

time.sleep (delay)
print('finding upperbands')

"""FINAL UPPERBAND = 
IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or 
(Previous Close > Previous FINAL UPPERBAND)) THEN 
(Current BASIC UPPERBAND) ELSE (Previous FINALUPPERBAND)"""

df['previous_final_upper_bands'] = df['basic_upper_bands'].shift()
df['previous_close'] = df['close'].shift()
df['final_upper_bands'] = np.where(
    (df['basic_upper_bands'] < df['previous_final_upper_bands']) |
    (df['previous_close'] > df['previous_final_upper_bands']),
    df['basic_upper_bands'],
    df['previous_final_upper_bands']
)

time.sleep (delay)
print('finding lowerbands')

"""FINAL LOWERBAND = 
IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or
(Previous Close < Previous FINAL LOWERBAND)) THEN 
(Current BASIC LOWERBAND) ELSE 
(Previous FINAL LOWERBAND)"""

df['previous_final_lower_bands'] = df['basic_lower_bands'].shift()
df['previous_close'] = df['close'].shift()
df['final_lower_bands'] = np.where(
    (df['basic_lower_bands'] > df['previous_final_lower_bands']) |
    (df['previous_close'] < df['previous_final_lower_bands']),
    df['basic_lower_bands'],
    df['previous_final_lower_bands']
)

time.sleep(delay)
print('Calculating Supertrend')

"""SUPERTREND = IF(Current Close <= Current FINAL UPPERBAND ) THEN
Current FINAL UPPERBAND ELSE Current FINAL LOWERBAND"""

df['supertrend'] = np.where(
    df['close'] <= df['final_upper_bands'],
    df['final_upper_bands'],
    df['final_lower_bands']
)


df['trend'] = np.where(
    df['supertrend'] <= df['close'],
    'UPTREND',
    'DOWNTREND'
)


# Subset the data for plotting
uptrend_data = df[df['trend'] == 'UPTREND']
downtrend_data = df[df['trend'] == 'DOWNTREND']

# Plotting
plt.plot(df['timestamp'], df['close'], color='black', label='Close')
plt.plot(df['timestamp'], df['supertrend'], color='blue', label='Supertrend')
plt.scatter(uptrend_data['timestamp'], uptrend_data['close'], color='green', label='Uptrend')
plt.scatter(downtrend_data['timestamp'], downtrend_data['close'], color='red', label='Downtrend')
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.title('Supertrend Indicator')
plt.legend()
plt.show()

print('finishing ith datafrmae')
time.sleep(delay)
print(df)
