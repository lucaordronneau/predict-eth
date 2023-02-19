import os 
import pandas as pd

def load_pair_data(input_pair):
    df = pd.read_json(input_pair, orient='values')
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df = df.astype(dtype={'open': 'float', 'high': 'float',
                          'low': 'float', 'close': 'float', 'volume': 'float'})
    df['date'] = pd.to_datetime(df['date'],
                                unit='ms',
                                utc=True,
                                infer_datetime_format=True)
    return df

def load_corr_pair(datadir, corr_pairs, timeframe):
    df_corr_pairs_dict = {}
    for corr_pair in corr_pairs:
        input_pair = os.path.join(datadir, f"{corr_pair}-{timeframe}.json")
        df_corr_pairs_dict[corr_pair] = load_pair_data(input_pair)
    return df_corr_pairs_dict