import numpy as np

from pathlib import Path

def log_return(list_stock_prices, period):
    return np.log(list_stock_prices).diff(periods=period)

def convert_log_return_to_price(log_return_pred, price):
    # Log return prediction at i future period and actual price will return the price at i future price
    return np.exp(log_return_pred + np.log(price))

def split_train_eval(df):
    return df.dropna().tail(13149), df.tail(1)

def save_list(list_: list, file_name: str):
    """Save a file shaped: [1.2, 3.4, 5.6, ..]"""
    p = Path(file_name)
    p.write_text(str(list_))