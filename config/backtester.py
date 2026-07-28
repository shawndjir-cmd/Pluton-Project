import pandas as pd

from portfolio import Portfolio


class Backtester:
    
    #Runs trading strategy on dowloaded historical data
    def __init__(self, strategy, initial_cash=10000, take_profit=0.10, stop_loss=0.05): 
        
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash=initial_cash, take_profit=take_profit,
                                   stop_loss=stop_loss, position_size=0.50)

    def run(self, data):

        # Generates the BUY and SELL signals
        signals = self.strategy.generate_signals(data)

        portfolio_values = []

        # Loops through each trading day
        for _, row in signals.iterrows():

            price = row["Close"]
            signal = row["Signal"]

            # ----------------------------------
            # Check Take Profit / Stop Loss
            # ----------------------------------

            if self.portfolio.should_sell(price):
                self.portfolio.sell(price)

            # ----------------------------------
            # Executes the SMA Signals
            # ----------------------------------

            if signal == 1:
                self.portfolio.buy(price)

            elif signal == -1:
                self.portfolio.sell(price)

            # ----------------------------------
            # Records Portfolio Value in the list
            # ----------------------------------

            value = self.portfolio.value(price)

            portfolio_values.append(value)

        signals["Portfolio Value"] = portfolio_values

        return signals
