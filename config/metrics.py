import numpy as np
import pandas as pd


def total_return(portfolio_values):
    """
    This code calculates the total return of the portfolio.
    
    It starts by finding the first value price and then finds the last valued price.
    
    Divides their summation by the starting price. Measures the profit percentage increase.
    """

    starting_value = portfolio_values.iloc[0]
    ending_value = portfolio_values.iloc[-1]

    return (ending_value - starting_value) / starting_value


def max_drawdown(portfolio_values):
    """
    This calculates the maximum drawdown. Measures the risk.
    """

    highest_value = portfolio_values.cummax()

    drawdown = (portfolio_values - highest_value) / highest_value

    return drawdown.min()

def sharpe_ratio(portfolio_values):
    """
    This calculates the annualized Sharpe Ratio.
    """

    returns = portfolio_values.pct_change().dropna()

    # Avoid division by zero
    if returns.std() == 0:
        return 0

    # std.() measures volatility
    # 252 for the 252 trading days in a trading year
    sharpe = (np.sqrt(252) * returns.mean() / returns.std())

    return sharpe


def evaluate(portfolio_values, trade_count):
    #returns performance of metrics
    
    return {
        "Total Return": total_return(portfolio_values),
        "Maximum Drawdown": max_drawdown(portfolio_values),
        "Sharpe Ratio": sharpe_ratio(portfolio_values),
        "Completed Trades": trade_count
    }
