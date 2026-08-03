# Pluton-Project

## ABSTRACT

This project develops and evaluates an algorithmic trading strategy on Python using a historical SPY data (April 2022 - April 2025). The strategy utilizes a Simple Moving Average (SMA) crossover to automatically buy and sell signals. A backtesting framework was developed by applying portfolio management, position sizing, take-profit threshold, and stop-loss threshold to optimize when a trader should start/stop buying signals. The project estimates itself by returning the Total Return, Maximum Drawdown and Sharpe Ratio of both the in-sample data and out-of-sample data.

Results of the strategy show it achieved similar ending portfolio values to buy-and-hold during the in-sample test while undergoing significantly less instability. For the out--of-sample period, the trading strategy maintained a value higher, but still close, to its starting level while buy-and-hold experienced a sharp decline, implying that the strategy's risk-management approach provided much better protection.

## Introduction

The project's goal is to develop and evaluate a simple algorithmic trading strategy in Python that works for the US Market Data.

There are 3 main objectives. Firstly, the project creates a backtesting framework that can apply itself to a historical market data and replicate a portfolio performance. Secondly, it uses `Optuna` to optimize the backtesting's SMA window, take-profit threshold, and stop-loss threshold. Lastly, it tests itself on out-of-sample data that was not applied during optimization. This makes sure the project is not overfitting.

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

A backtesting framework was then constructed to simulates trades and record portfolio performance. The portfolio begins with $10,000, invests 50% of available cash on each buy signal, and sells the entire position when a sell signal or risk-management rule is triggered in `portfolio.py`. 

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

## Optimization

To enhance the strategy's performance, Optuna was implemented to the SMA, take-profit threshold, and stop-loss threshold. For each trial, Optuna picked a new parameter combination, ran it through the backtesting framework, and evaluated it using Sharpe Ratio.

``` sh
def objective(self, trial):

        # -----------------------------
        # Search Space
        # -----------------------------

        window = trial.suggest_int( "window", 5, 50)

        take_profit = trial.suggest_float("take_profit", 0.03, 0.20)

        stop_loss = trial.suggest_float("stop_loss", 0.01, 0.10)

        
        # Builds up strategy
        strategy = SMAStrategy(window=window)

        # Run Backtest
        backtester = Backtester(strategy=strategy, initial_cash=self.initial_cash,
                                take_profit=take_profit, stop_loss=stop_loss)

        results = backtester.run(self.data)

        # Evaluate
        performance = evaluate(results["Portfolio Value"], backtester.portfolio.trade_count)

        # Maximize Sharpe Ratio
        return performance["Sharpe Ratio"]
```

Optimization was performed only on the in-sample dataset (April 2022–April 2024). The optimized parameters were then applied to the out-of-sample dataset (April 2024–April 2025) to evaluate how well the strategy performed on unseen market data.

``` sh
def validate(self, data):
        """
        Runs the trading strategy with out-of-sample data.
        """

        results = self.backtester.run(data)

        performance = evaluate(results["Portfolio Value"],
                               self.backtester.portfolio.trade_count)

        return results, performance
```

## Results

The in-sample results show that the SMA strategy grew from the initial $10,000 portfolio to approximately $11,500, producing 15% increase in return. The strategy performed similar to the buy-and-hold approach without having as much declines as the buy-and-hold.

<img width="1380" height="677" alt="image" src="https://github.com/user-attachments/assets/51047af2-5f6e-4f6f-904b-bf3bf2df995d" />

The out-of-sample results show a bigger difference. The out-of-sample show that the SMA strategy grew the initial $10,000 to approximately $11,500 while the buy-and-hold portfolio declined to about $10,800 by the end of the market's time period.

<img width="1387" height="667" alt="image" src="https://github.com/user-attachments/assets/4fdca477-b520-4095-9937-211defe52e14" />

## Discussion

The results show that the SMA strategy biggest strength is it's risk management. During the in-sample period, it performed a similar profit increase as the buy-and-hold portfolio without being as risky and suffering as much declines during the time period. The out-of-sample results further demonstrates the potential benefit of exiting positions during unfavorable market conditions.

Results are also only tested on the SPY market. Since it's only been tested on a historical backtest, it does not guarantee for future performance.

## Conclusion

This project developed a complete algorithmic trading system that combines SMA signals, portfolio management, risk controls, backtesting, `Optuna` optimization, and out-of-sample validation. The results demonstrate that this strategy can participate and perform well in the US market data while having greater protection against downside movements than a simple buy-and-hold approach. Most importantly, the strategy's value is not necessarily in producing the highest possible return, but in balancing returns with risk.

Additionally, testing across different assets and market environments would be necessary to determine its broader effectiveness.
