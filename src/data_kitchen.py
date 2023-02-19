import helpers

import talib

import numpy as np
import pandas as pd
from math import ceil

def create_target(data):
    for i in range(2, 14):
        data[f'target_{i}'] = helpers.log_return(data['close'], period=i)
        data[f'target_{i}'] = data[f'target_{i}'].shift(-i)
    return data

def week_of_month(dt):
    first_day = dt.replace(day=1)

    dom = dt.day
    adjusted_dom = dom + first_day.weekday()

    return int(ceil(adjusted_dom/7.0))

def get_time_indicators(df):
    df['hour'] = df['date'].dt.hour
    df['day_week'] = df['date'].dt.dayofweek
    df['day'] = df['date'].dt.day - 1
    df['week'] = df['date'].apply(week_of_month) - 1
    df['month'] = df['date'].dt.month
    return df

def encode_time_indicators(data, col, max_val):
    data[f'feature_{col}_sin'] = np.sin(2 * np.pi * data[col]/max_val)
    data[f'feature_{col}_cos'] = np.cos(2 * np.pi * data[col]/max_val)
    return data

def populate_time_indicators(df):
    df = encode_time_indicators(df, 'hour', 23)
    df = encode_time_indicators(df, "day_week", 6)
    df = encode_time_indicators(df, 'day', 30)
    df = encode_time_indicators(df, 'week', 5)
    # df = encode_time_indicators(df, 'month', 12)
    return df

def populate_indicators(df, pair, periods):
    df['log_return_1'] = np.log(df['close']).diff(periods=1)
    for i in periods:
        # Own features        
        df[f'feature_{pair}_ema_{i}'] = talib.EMA(df['close'], timeperiod=i)
        df[f'feature_{pair}_sma_{i}'] = talib.SMA(df['close'], timeperiod=i)
        df[f'feature_{pair}_log_return_{i}'] = np.log(df['close']).diff(periods=i)
        df[f'feature_{pair}_rsi_{i}'] = talib.RSI(df['close'], timeperiod=i)
        
        df[f'feature_{pair}_atr_{i}'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=i)
        df[f'feature_{pair}_volatility_{i}'] = df['log_return_1'].rolling(window=i).std() * np.sqrt(8766)
        df[f'feature_{pair}_willr_{i}'] = talib.WILLR(df['high'], df['low'], df['close'], timeperiod=i)
                
    df[f'feature_{pair}_obv'] = talib.OBV(df['close'], df['volume'])    

    return df

def populate_pairs_indicators(df_corr_pairs_dict, pair, periods_1h):
    for key, value in df_corr_pairs_dict.items():
        # Do time encoding for only one pair (the main)
        if key == pair:
            df_corr_pairs_dict[key] = get_time_indicators(value)
            df_corr_pairs_dict[key] = populate_time_indicators(df_corr_pairs_dict[key])
        df_corr_pairs_dict[key] = populate_indicators(df_corr_pairs_dict[key], key, periods_1h)
    
    return df_corr_pairs_dict

def renaming_corr_pairs(x, pair):
    if "feature_" not in x:
        return pair + "_" + x # or None
    return x

def merge_pairs_and_target(data, pair, df_corr_pairs_dict):
    first_idx = data.iloc[0]['date']
    last_idx  = data.iloc[-1]['date']

    for key, value in df_corr_pairs_dict.items():
        df_corr_pairs_dict[key] = value.loc[(value['date'] >= first_idx) & (value['date'] <= last_idx)]
        df_corr_pairs_dict[key] = df_corr_pairs_dict[key].reset_index(drop=True)
        if key != pair:
            df_corr_pairs_dict[key].columns = [renaming_corr_pairs(col, key) for col in df_corr_pairs_dict[key].columns]

    df_merge = pd.DataFrame()
    for key, _ in df_corr_pairs_dict.items():
        df_merge = pd.concat([df_merge, df_corr_pairs_dict[key]], axis=1)

    for i in range(2, 14):
        target = f"target_{i}"
        df_merge[target] = data[target]

    return df_merge