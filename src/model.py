import helpers

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

def init_xgb_model():
    params = {
        "colsample_bytree":0.3,
        "max_depth":4,
        "learning_rate":0.028,
        "n_estimators":2250,# 2250,
        "subsample":0.75,
        "reg_lambda":0.0, # L2 Regularization
        "reg_alpha":0.0,
        "objective":"reg:squarederror",
        "eval_metric":"rmse",
        "early_stopping_rounds":100
    }
    model = XGBRegressor(**params)
    return model

def init_lgbm_model():
    params = {
        "early_stopping_round":100,
        "colsample_bytree":0.12,
        "max_depth":8,
        "learning_rate":0.028,
        "n_estimators":1400,
        "subsample":0.8,
        "reg_lambda":1.8, # L2 Regularization
        "reg_alpha":0.1,
        "objective":"mean_squared_error",
    }
    model = LGBMRegressor(**params)
    return model

def train_xgb_model(model, df_train, selected_features, target):
    model.fit(df_train[selected_features], df_train[target],
          eval_set=[(df_train[selected_features], df_train[target])], verbose=500)
    return model

def train_lgbm_model(model, df_train, selected_features, target):
    model.fit(df_train[selected_features], df_train[target],
          eval_set=[(df_train[selected_features], df_train[target])], verbose=500)
    return model

def predict_eth_price(df_test, model, i, selected_features):
    print('Evaluation on', df_test.index[0], 'for the next', i, 'hours')
    y_pred = model.predict(df_test[selected_features].astype('float64'))
    df_test.loc[:, f'target_{i}_pred'] = y_pred
    df_test.loc[:, f'price_{i}_pred'] = df_test.apply(lambda x: helpers.convert_log_return_to_price(x[f'target_{i}_pred'], x['close']), axis=1)
    df_test.loc[:, f'price_{i}_true'] = df_test.apply(lambda x: helpers.convert_log_return_to_price(x[f'target_{i}'], x['close']), axis=1)
    off_log_return = df_test.iloc[-1][f'target_{i}_pred']
    off_price = df_test.iloc[-1][f'price_{i}_pred']
    
    print('Log return pred', off_log_return, '|', 'Price pred', off_price)
    return off_log_return, off_price

def run_prediction(df_train, df_eval, selected_features):
    off_log_return_result_lgbm = []
    off_price_result_lgbm = []
    off_log_return_result = []
    off_price_result = []

    model = init_xgb_model()
    model_lgbm = init_lgbm_model()

    for i in range(2, 14):
        print(f'--- {i}h ---')

        target = f"target_{i}"
        
        print('XGBoost')
        model = train_xgb_model(model, df_train, selected_features, target)
        off_log_return, off_price = predict_eth_price(df_eval, model, i, selected_features)
        print()
        print('LightLGBM')
        model_lgbm = train_lgbm_model(model_lgbm, df_train, selected_features, target)
        off_log_return_lgbm, off_price_lgbm = predict_eth_price(df_eval, model_lgbm, i, selected_features)
        
        off_log_return_result.append(off_log_return)
        off_price_result.append(off_price)
        
        off_log_return_result_lgbm.append(off_log_return_lgbm)
        off_price_result_lgbm.append(off_price_lgbm)

    ensemble_xgb_lgbm = [(g + h) / 2 for g, h in zip(off_price_result, off_price_result_lgbm)]

    print(f'--- log return xgb: {off_log_return_result} ---')
    print(f'--- price xgb: {off_price_result} ---')
    print()
    print(f'--- log return lgbm: {off_log_return_result_lgbm} ---')
    print(f'--- price lgbm: {off_price_result_lgbm} ---')
    print()
    print(f'--- price ensemble: {ensemble_xgb_lgbm} ---')
    print()

    return ensemble_xgb_lgbm