class Portfolio:
    """
    Simulates a trading portfolio.
    """

    def __init__(self, initial_cash=10000, take_profit=0.10, stop_loss=0.05):

        # Portfolio information
        self.initial_cash = initial_cash
        self.cash = initial_cash

        # Current position
        self.position = 0
        self.entry_price = None

        # Risk thresholds
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def buy(self, price):
        """
        Buy one share if no position is currently open.
        """

        if self.position == 0:

            self.position = 1
            self.entry_price = price
            self.cash -= price

    def sell(self, price):
        """
        Sell the current share if one is owned.
        """

        if self.position == 1:

            self.position = 0
            self.cash += price
            self.entry_price = None

    def should_sell(self, current_price):
        """
        Determines whether the current position should close
        since take-profit or stop-loss threshold have been reached.
        """
        
        # No open position
        if self.position == 0:
            return False

        # Percentage gain/loss since entering the trade
        percent_change = (current_price - self.entry_price) / self.entry_price

        # Take Profit
        if percent_change >= self.take_profit:
            return True

        # Stop Loss
        if percent_change <= -self.stop_loss:
            return True

        return False

    def value(self, current_price):
        """
        Calculates the current portfolio value.
        """
        
        return self.cash + (self.position * current_price)
