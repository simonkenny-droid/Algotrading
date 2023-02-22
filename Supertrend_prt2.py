import ccxt
import pandas as pd
from datetime import datetime
import pytz

exchange = ccxt.binance()

bars = exchange.fetchOHLCV('ETH/USDT', timeframe= '15m', limit=30)

df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize(pytz.utc).dt.tz_convert(pytz.timezone('America/Los_Angeles')).dt.tz_localize(None)
print (df)