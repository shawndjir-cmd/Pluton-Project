from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    Basic class for all the different trading strategies.
    """

    @abstractmethod
    def generate_signals(self, data):
        """
        Finds trading signals.

        Parameters
        ----------
        data : pandas.DataFrame
            Historical market data.

        Returns
        -------
        pandas.DataFrame
            DataFrame containing trading signals.
        """
        pass
