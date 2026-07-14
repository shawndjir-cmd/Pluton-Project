import pandas as pd

from common_strategy import BaseStrategy

class SMAStrategy(BaseStrategy):

    def __init__(self, window=20):
        self.window = window

    def generate_signals(self, data):

        signals = data.copy()

        # Evaluates the SMA of the stock
        signals["SMA"] = (
            signals["Close"]
            .rolling(window=self.window)
            .mean()
        )

        # HOLD is used as the default
        signals["Signal"] = 0

        # Previous day's values
        prev_close = signals["Close"].shift(1)
        prev_sma = signals["SMA"].shift(1)

        # BUY crossover
        buy_signal = (
            (prev_close <= prev_sma) &
            (signals["Close"] > signals["SMA"])
        )

        # SELL crossover
        sell_signal = (
            (prev_close >= prev_sma) &
            (signals["Close"] < signals["SMA"])
        )

        signals.loc[buy_signal, "Signal"] = 1
        signals.loc[sell_signal, "Signal"] = -1

        return signals
