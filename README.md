# Pluton-Project

## ABSTRACT

This project develops and evaluates an algorithmic trading strategy on Python using a historical SPY data (April 2022 - April 2025). The strategy utilizes a Simple Moving Average (SMA) crossover to automatically buy and sell signals. A backtesting framework was developed by applying portfolio management, position sizing, take-profit threshold, and stop-loss threshold to optimize when a trader should start/stop buying signals. The project estimates itself by returning the Total Return, Maximum Drawdown and Sharpe Ratio of both the in-sample data and out-of-sample data.

## Introduction

The project's goal is to develop and evaluate a simple algorithmic trading strategy in Python that works for the US Market Data.

There are 3 main objectives. Firstly, the project creates a backtesting framework that can apply itself to a historical market data and replicate a portfolio performance. Secondly, it uses Optuna to optimize the backtesting's SMA window, take-profit threshold, and stop-loss threshold. Lastly, it tests itself on out-of-sample data that was not applied during optimization. This makes sure the project is not overfitting.

The main goal is not to just maximize profits, but to establish whether this trading strategy can produce a good performance while still accounting for risks in an unseen market data.


## Data

The strategy uses historical SPDR S&P 500 ETF Trust (SPY) market data stored as CSV files. It was downloaded using yfinance in the Python library.

The project separates the data into:

- `spy_in_sample.csv` — used for strategy development and optimization
- `spy_out_sample.csv` — used for out-of-sample validation

Place both files inside the `data/` directory:

data/
├── spy_in_sample.csv
└── spy_out_sample.csv

The in-sample dataset covers April 1, 2022 through April 1, 2024, and the out-of-sample dataset covers April 2, 2024 through April 1, 2025.

```sh
from clean_data import load_data

in_sample_data = load_data("data/spy_in_sample.csv")
out_sample_data = load_data("data/spy_out_sample.csv")
```

The strategy primarily uses the Close price to calculate the SMA and generates trading signals.

## Methods

The project uses buys and sell signals to make profits. Buy signals are prompted when the stock price crosses above the SMA, while sell signals are generated when the price crosses below the SMA. The strategy also includes take-profit and stop-loss rules to regulate risks.

A backtesting framework was then constructed to simulates trades and record portfolio performance. The portfolio begins with $10,000, invests 50% of available cash on each buy signal, and sells the entire position when a sell signal or risk-management rule is triggered. 

``` sh
def __init__(self, strategy, initial_cash=10000, take_profit=0.10, stop_loss=0.05): 
        
        self.strategy = strategy
        self.portfolio = Portfolio(initial_cash=initial_cash, take_profit=take_profit,
                                   stop_loss=stop_loss, position_size=0.50)
```

Portfolio performance is then evaluated using Total Return, Maximum Drawdown, Sharpe Ratio.

``` sh
def evaluate(portfolio_values, trade_count):
    #returns performance of metrics
    
    return {
        "Total Return": total_return(portfolio_values),
        "Maximum Drawdown": max_drawdown(portfolio_values),
        "Sharpe Ratio": sharpe_ratio(portfolio_values),
        "Completed Trades": trade_count
    }
```
