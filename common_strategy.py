from abc import ABC, abstractmethod


class BaseStrategy(ABC):  
    #Basic class for all the different trading strategies.
    
    @abstractmethod
    
    def generate_signals(self, data):
        #To check which strategy to use like RSI, SMA or MACD   
        pass
