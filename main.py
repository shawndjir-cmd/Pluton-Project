from sma_strategy import SMAStrategy

print("Import successful!")

import pandas as pd

from sma_strategy import SMAStrategy


# Example of potential data code
data = pd.DataFrame({
    "Close": [100, 101, 102, 103, 101, 99, 98, 100, 103, 105]
})

strategy = SMAStrategy(window=3)

signals = strategy.generate_signals(data)

print(signals)
print(signals[["Close", "SMA"]])
