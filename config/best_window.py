import optuna

from sma_strategy import SMAStrategy
from backtester import Backtester
from metrics import evaluate


class BestWindow:
    
    # Uses Optuna to find the best SMA window, take-profit threshold, and stop-loss threshold.

    def __init__(self, data, initial_cash=10000):

        self.data = data
        self.initial_cash = initial_cash

    def objective(self, trial):

        # -----------------------------
        # Searches Space
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

    def optimize(self, trials=30):
        
        # Runs the Optuna optimization.

        study = optuna.create_study(direction="maximize")

        study.optimize(self.objective, n_trials=trials)

        return study
