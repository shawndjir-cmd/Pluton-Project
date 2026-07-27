import pandas as pd


def load_data(file_path):
    """
    Loads our historical market data from a CSV file 
    Returns clean historical data with no missing values
    """
    
    data = pd.read_csv(
        file_path,
        index_col="Date",
        parse_dates=True
    )

    return data
