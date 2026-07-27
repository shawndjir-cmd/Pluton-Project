from clean_data import load_data
from sma_strategy import SMAStrategy
from backtester import Backtester
from metrics import evaluate
from best_window import BestWindow
from validation import Validator

def main():

    # Loads historical market data
    in_sample_data = load_data("data/spy_in_sample.csv")

    out_sample_data = load_data("data/spy_out_sample.csv")

    
    # Optimizes the strategy
    optimizer = BestWindow(in_sample_data)

    study = optimizer.optimize(trials=30)

    best_window = study.best_params["window"]
    best_take_profit = study.best_params["take_profit"]
    best_stop_loss = study.best_params["stop_loss"]

    print("Optimization Results")
    print("--------------------")
    print(f"Best SMA Window : {best_window}")
    print(f"Take Profit     : {best_take_profit:.2%}")
    print(f"Stop Loss       : {best_stop_loss:.2%}")
    print(f"Best Sharpe     : {study.best_value:.4f}")


    # ====================================
    # Builds up optimized strategy
    strategy = SMAStrategy(window=best_window)


    
    # =====================================
    # Build backtester
    backtester = Backtester(strategy=strategy, initial_cash=10000,
                            take_profit=best_take_profit, stop_loss=best_stop_loss)

   
    
    # =====================================
    # In-sample backtest
    in_sample_results = backtester.run(in_sample_data)

    # sends only the portfolio column to metrics.py to find the total return, MDD and Sharpe
    in_sample_metrics = evaluate(in_sample_results["Portfolio Value"])

    print("\nIn Sample Data Performance")
    print("---------------------")

    for metric, value in in_sample_metrics.items():

        if metric == "Sharpe Ratio":
            print(f"{metric}: {value:.4f}")
        else:
            print(f"{metric}: {value:.2%}")

    
    # =====================================
    # Out-of-sample validation
    validator = Validator(backtester)

    out_sample_results, out_sample_metrics = validator.validate(out_sample_data)

    print("\nOut-of-Sample Performance")
    print("-------------------------")

    for metric, value in out_sample_metrics.items():

        if metric == "Sharpe Ratio":
            print(f"{metric}: {value:.4f}")
        else:
            print(f"{metric}: {value:.2%}")


if __name__ == "__main__":
    main()
