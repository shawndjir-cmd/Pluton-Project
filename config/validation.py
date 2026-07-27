from metrics import evaluate


class Validator:

    def __init__(self, backtester):
        self.backtester = backtester

    def validate(self, data):
        """
        Runs the trading strategy with out-of-sample data.
        """

        results = self.backtester.run(data)

        performance = evaluate(results["Portfolio Value"],
                               self.backtester.portfolio.trade_count)

        return results, performance
