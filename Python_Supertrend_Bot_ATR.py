# Supertrend bot using ATR to calculate the Supertrend and CCXT to access Binance exchange data.

# Step 1: Import libraries and define bot settings
# 
# Let's start by importing the necessary libraries and setting some parameters for our bot:
import ccxt
import ta
import time
import pandas as pd 


# Exchange and Symbol Settings
exchange = ccxt.binance()
symbol = 'BTC/USDT'


# Bot Settings
supertrend_period = 10
buy_percentage = 0.02
sell_percentage = 0.01
#Here we're using the CCXT library to connect to the Binance exchange, 
# and we're defining the symbol we want to trade. 
# We're also setting the period for the Supertrend calculation, 
# as well as the percentage values for buying and selling.

#Step 2: Define the Supertrend function
# 
# Next, we'll define the calculate_supertrend() function using the Technical Analysis library:
def calculate_supertrend(df, period):
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], period)
    df['upper_basic'] = (df['high'] + df['low']) / 2 + (2 * df['atr'])
    df['lower_basic'] = (df['high'] + df['low']) / 2 - (2 * df['atr'])
    df['upper_band'] = df['upper_basic']
    df['lower_band'] = df['lower_basic']
    for i in range(period, len(df)):
        if df['close'][i] <= df['upper_band'][i - 1]:
            df['upper_band'][i] = min(df['upper_basic'][i], df['upper_band'][i - 1])
        else:
            df['upper_band'][i] = df['upper_basic'][i]
        if df['close'][i] >= df['lower_band'][i - 1]:
            df['lower_band'][i] = max(df['lower_basic'][i], df['lower_band'][i - 1])
        else:
            df['lower_band'][i] = df['lower_basic'][i]
    df['supertrend'] = 0.00
    for i in range(period, len(df)):
        if df['close'][i - 1] <= df['supertrend'][i - 1] and df['close'][i] > df['supertrend'][i]:
            df['supertrend'][i] = df['lower_band'][i]
        elif df['close'][i - 1] > df['supertrend'][i - 1] and df['close'][i] <= df['supertrend'][i]:
            df['supertrend'][i] = df['upper_band'][i]
        else:
            df['supertrend'][i] = df['supertrend'][i - 1]
    return df

#This function takes a Pandas DataFrame of OHLC data and the Supertrend period as inputs. 
# It returns the same DataFrame with the Supertrend column added.

#Step 3: Define the trading loop
#Now let's define the trading loop that will run indefinitely and check the Supertrend every minute:
import time

def run_bot():
    # Connect to Binance exchange
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'

    # Define Supertrend settings
    supertrend_period = 10
    atr_multiplier = 3.0
    buy_percentage = 0.01
    sell_percentage = 0.01

    while True:
        try:
            # Get OHLC data from exchange
            ohlcv = exchange.fetch_ohlcv(symbol, '1m')
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

            # Calculate Supertrend and check for signals
            # (code for this step is shown in Step 4)
        except Exception as e:
            print(e)
            time.sleep(60)
#In this loop, we're first connecting to the Binance exchange using the ccxt.binance() function 
# and defining the trading symbol as 'BTC/USDT'.

#Next, we're setting the Supertrend parameters including the period, ATR multiplier, and buy/sell percentages.

#Then we're entering a while loop that will run indefinitely.
# Within this loop, we're fetching the OHLC (Open-High-Low-Close) data for the symbol from the exchange 
# using fetch_ohlcv() function and creating a pandas DataFrame with the data.

#Finally, we're calling the calculate_supertrend() function and checking for buy/sell signals. 
# Any exceptions that occur will be caught and printed, and the loop will wait for 1 minute before trying again



#Step 4: Calculate the Supertrend and check for signals
# 
# Once we have the OHLC data, we can calculate the Supertrend and check for buy/sell signals:
# Calculate Supertrend
    df = calculate_supertrend(df, supertrend_period)

    # Get last Supertrend value
    last_supertrend = df['supertrend'].iloc[-1]

    # Get last close price
    last_close = df['close'].iloc[-1]

    # Calculate buy and sell prices
    buy_price = last_close * (1 - buy_percentage)
    sell_price = last_close * (1 + sell_percentage)

    # Check for signals
    if last_close > last_supertrend and last_close >= buy_price:
        print('Buy signal detected!')
        # Implement buy order here
    elif last_close < last_supertrend and last_close <= sell_price:
        print('Sell signal detected!')
        # Implement sell order here

    # Wait for 1 minute before checking again
    time.sleep(60)
    
    
# Here we're calculating the Supertrend using the calculate_supertrend() function, 
# and then getting the last Supertrend value and the last close price. 
# We're also calculating the buy and sell prices based on the percentage settings we defined earlier.
# Then we check if the close price is above the Supertrend and above the buy price, indicating a buy signal,
# or if it's below the Supertrend and below the sell price, indicating a sell signal. If a signal is detected,
# we print a message and implement the buy or sell order.
# 
# Finally, we wait for 1 minute before checking again.

#Step 5: Run the bot
#To run the bot, we can simply call the trading loop:
if __name__ == '__main__':
    while True:
        try:
            run_bot()
        except Exception as e:
            print(e)
            time.sleep(60)
            
#This loop will keep running indefinitely, checking for buy and sell signals every minute. 
# We've also added some exception handling in case there are any errors or connection issues with the exchange.