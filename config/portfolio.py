class Portfolio:
    """
    Simulates a trading portfolio.
    """

    def __init__(self, initial_cash=10000, take_profit=0.10, stop_loss=0.05, position_size=0.50):

        # Portfolio information
        self.initial_cash = initial_cash
        self.cash = initial_cash

        # Current position
        self.position = 0          # Number of shares owned
        self.entry_price = None

        # Risks for profit and loss threshold
        self.take_profit = take_profit
        self.stop_loss = stop_loss

        # Percentage of available cash that can be invested (50%)
        self.position_size = position_size

        # Number of completed trades
        self.trade_count = 0

    def buy(self, price):
        """
        Invest 50% of available cash.
        """

        if self.position == 0:

            investment = self.cash * self.position_size

            shares = int(investment // price)

            if shares > 0:

                self.position = shares
                self.entry_price = price

                self.cash -= shares * price

    def sell(self, price):
        """
        Sell every owned share that we currently have.
        """

        if self.position > 0:

            self.cash += self.position * price

            self.position = 0
            self.entry_price = None

            self.trade_count += 1

    def should_sell(self, current_price):
        """
        Check whether take-profit or stop-loss has been reached.
        """

        if self.position == 0:
            return False

        percent_change = (
            current_price - self.entry_price
        ) / self.entry_price

        if percent_change >= self.take_profit:
            return True

        if percent_change <= -self.stop_loss:
            return True

        return False

    def value(self, current_price):
        """
        Current portfolio value.
        """

        return self.cash + self.position * current_price
