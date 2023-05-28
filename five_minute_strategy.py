#Here's the complete code for the trading bot using the 
# CCXT library for Binance and implementing the 
# 5-minute Bollinger Bands strategy:

import ccxt
import time
import numpy as np

# Set up Binance exchange connection
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET_KEY',
})

def calculate_bollinger_bands(prices, period, deviation):
    rolling_mean = np.mean(prices[-period:])
    rolling_std = np.std(prices[-period:])
    upper_band = rolling_mean + (rolling_std * deviation)
    lower_band = rolling_mean - (rolling_std * deviation)
    return upper_band, lower_band

def execute_trade(symbol, action):
    quantity = 0.001  # Quantity to trade
    if action == 'buy':
        # Place buy order
        order = exchange.create_market_buy_order(symbol, quantity)
        print(f'Buy {quantity} of {symbol} at market price')
    elif action == 'sell':
        # Place sell order
        order = exchange.create_market_sell_order(symbol, quantity)
        print(f'Sell {quantity} of {symbol} at market price')

def run_bot(symbol, period, deviation, buy_threshold, sell_threshold):
    prices = []
    while True:
        try:
            # Fetch candlestick data for the symbol
            candles = exchange.fetch_ohlcv(symbol, timeframe='5m', limit=period)
            # Extract closing prices
            close_prices = [candle[4] for candle in candles]
            current_price = close_prices[-1]
            prices.append(current_price)
            if len(prices) > period:
                upper_band, lower_band = calculate_bollinger_bands(prices, period, deviation)
                last_price = prices[-2]
                if last_price < lower_band * (1 - buy_threshold):
                    execute_trade(symbol, 'buy')
                elif current_price > last_price * (1 + sell_threshold):
                    execute_trade(symbol, 'sell')
            time.sleep(300)  # Wait for 5 minutes
        except Exception as e:
            print(f'An error occurred: {str(e)}')

# Set bot parameters
symbol = 'BTC/USDT'  # Symbol to trade
period = 10  # Bollinger Bands period
deviation = 2  # Bollinger Bands deviation
buy_threshold = 0.03  # Buy threshold as a percentage below the lower band
sell_threshold = 0.01  # Sell threshold as a percentage profit target

# Run the bot
run_bot(symbol, period, deviation, buy_threshold, sell_threshold)
