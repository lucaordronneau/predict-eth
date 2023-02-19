import os

import warnings
warnings.filterwarnings("ignore")

import data
import data_kitchen as dk

import helpers
import model

DATADIR = "../data/binance"

PAIR = "ETH_USDT"
TIMEFRAME = "1h"
PERIODS_1H = [2, 3, 5, 8, 13, 21, 23]

SEED = 2202
OPTIM = False

CORR_PAIRS = [PAIR, "BTC_USDT", "ETH_BTC"]
INPUT_PAIR = os.path.join(DATADIR, f"{PAIR}-{TIMEFRAME}.json")

if __name__ == "__main__":
    df_pair = data.load_pair_data(INPUT_PAIR)
    df_pair = dk.create_target(df_pair)

    df_corr_pairs_dict = data.load_corr_pair(DATADIR, CORR_PAIRS, TIMEFRAME)
    df_corr_pairs_dict = dk.populate_pairs_indicators(df_corr_pairs_dict, PAIR, PERIODS_1H)

    df = dk.merge_pairs_and_target(df_pair, PAIR, df_corr_pairs_dict)
    selected_features = [col for col in df if col.startswith('feature_')]
    df = df.set_index('date')
    
    df_train, df_eval = helpers.split_train_eval(df)

    predictions = model.run_prediction(df_train, df_eval, selected_features)

    file_name = "../data/predictions.csv"
    helpers.save_list(predictions, file_name)

    