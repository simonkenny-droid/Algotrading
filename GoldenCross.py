import math
import backtrader as bt

class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), ("order_percentage", 0.95), ('ticker', 'SPY'))
    # Initialize the strategy with the specified parameters
    
    def __init__(self):
                
        # Create a simple moving average indicator for the fast moving average
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname='50 day moving average'
        )
        
        # Create a simple moving average indicator for the slow moving average
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname='200 day moving average'
        )
        
        # Create a crossover indicator to detect the golden cross
        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)
        
    def next(self):
        # Execute the strategy logic for each trading period
        
        if self.position.size == 0:
            # If no position is open, check for a golden cross and generate a buy signal
            
            if self.crossover > 0:
                # Calculate the amount to invest based on the order percentage and available cash
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                
                # Calculate the number of shares to buy based on the available cash and closing price
                self.size = math.floor(amount_to_invest / self.data.close)
                
                # Print the buy signal with the number of shares, ticker, and closing price
                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                
                # Open a position by buying the specified number of shares
                self.buy(size=self.size)
                
        if self.position.size > 0:
            # If a position is open, check for a death cross and generate a sell signal
            
            if self.crossover < 0:
                # Print the sell signal with the number of shares, ticker, and closing price
                print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
                
                # Close the position by selling all shares
                self.close()
 