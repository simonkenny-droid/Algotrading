"""The warning message you encountered is a SettingWithCopyWarning from pandas.
This warning occurs when you modify a DataFrame using chained indexing, such as df[xxx][yyy]. 
To eliminate the warning, you can replace all instances of df[xxx][yyy] with df.loc[yyy, xxx].
Here's the updated code with the modifications:"""


import ccxt
import pandas as pd
pd.set_option('display.max_rows', None)  # display as many rows/columns as possible
pd.set_option('display.max_columns', None)

from datetime import datetime
import pytz

exchange = ccxt.binance()
bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='1d', limit=365)
df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize(pytz.utc).dt.tz_convert(pytz.timezone('America/Los_Angeles')).dt.tz_localize(None)

def tr(df):
    df['previous_close'] = df['close'].shift(1)
    df['high-low'] = df['high'] - df['low']
    df['high-pc'] = abs(df['high'] - df['previous_close'])
    df['low-pc'] = abs(df['low'] - df['previous_close'])
    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr

def atr(df, period):
    df['tr'] = tr(df)
    atr = df['tr'].rolling(period).mean()

    return atr

def supertrend(df, period=7, multiplier=3):
    print('calculate supertrend')
    df['atr'] = atr(df, period=period)
    df['upper_band'] = ((df['high'] + df['low']) / 2) + (multiplier * df['atr'])
    df['lower_band'] = ((df['high'] + df['low']) / 2) - (multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df.loc[current, 'close'] > df.loc[previous, 'upper_band']:
            df.loc[current, 'in_uptrend'] = True
        elif df.loc[current, 'close'] < df.loc[previous, 'lower_band']:
            df.loc[current, 'in_uptrend'] = False
        else:
            df.loc[current, 'in_uptrend'] = df.loc[previous, 'in_uptrend']

            if df.loc[current, 'in_uptrend'] and df.loc[current, 'lower_band'] < df.loc[previous, 'lower_band']:
                df.loc[current, 'lower_band'] = df.loc[previous, 'lower_band']

            if not df.loc[current, 'in_uptrend'] and df.loc[current, 'upper_band'] > df.loc[previous, 'upper_band']:
                df.loc[current, 'upper_band'] = df.loc[previous, 'upper_band']

    print(df)

supertrend(df)

"""Explicit indexing: With .loc, you explicitly specify the row and column labels, 
making your code more readable and self-explanatory. It enhances the clarity of your code and 
helps prevent ambiguity.

Performance optimization: In certain cases, using .loc can also 
improve the performance of your code because it allows pandas to optimize the indexing operation.

In general, it's recommended to use .loc for assigning values or modifying DataFrame content 
to ensure clarity, avoid potential issues, and improve code maintainability.
However, for simple read-only operations, chained indexing like df[xxx][yyy] may be acceptable.

It's important to note that the warning is informative and does not necessarily mean 
your code is incorrect. However, eliminating the warning by using .loc is 
considered good practice and can help you write more reliable and maintainable code."""






