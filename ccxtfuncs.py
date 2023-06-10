"""
only 7 ccxt functions needed to algotrading

"""

import ccxt
import config
import time
import pandas as pd

exchange = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': config.BINANCE_API_KEY, 
    'secret': config.BINANCE_SECRET_KEY
})

# Load the markets (tickers) from the exchange
markets = exchange.load_markets()

# Get a list of symbols for all available tickers
symbols = list(markets.keys())

# Print the symbols
for symbol in symbols:
    print(symbol)

# 7- creating a limit order
symbol = 'ETH/BTC'
size = 1
price = 1600

exchange.create_limit_buy_order(symbol, size, price)

#6- fetch open positions
exchange.create_market_buy_order(symbol, size)

print(exchange.fetch_positions())
print(exchange.fetch_open_orders(symbol))

#5- cancel orders and conditional orders
exchange.cancel_all_orders(symbol)
exchange.cancel_all_orders(symbol=symbol, params={'untriggered':True})

#3- get the orderbook
order_book = exchange.fetch_order_book(symbol)
print(order_book)
#for order in order_book:
#    print(order)
#    
#print(order_book)
bid = order_book["bids"][0][0]
ask = order_book["asks"][0][0]
print(f'BID: {bid} ASK: {ask}')
#get OHLCV
bars = exchange.fetch_ohlcv(symbol, timeframe='1m', since=None, limit=200)

#format ohlcv to df
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
print(df)