# Ocean Data Challenge :: ETH Prediction
## Round 3
Predict with the lowest prediction error the next 12 hours of ETH price (USDT).
- Submission deadline: Sun Feb 19, 2023 at 23:59 UTC
- Prediction at times: Mon Feb 20, 2023 at 1:00 UTC, 2:00, ..., 12:00 (12 predictions total).
- Requirement for submission : .csv prediction file + 10-15 slides + proper submission flow.

In order to forecast the price of ETH, I made the strategic decision to utilize the **log return** of ETH as the target variable for prediction. To achieve this, 12 distinct targets were formulated to estimate the upcoming 12-hour period from the most recent data point available.

The data source used was the *ETH/USDT* pair downloaded from **freqtrade** (data from 2017 until now), which was supplemented with correlated pairs of *BTC/USDT* and *ETH/BTC*.

To handle the complexity of the dataset and its non-linear relationships, **Gradient Boosting** was chosen as the machine learning algorithm, specifically using *LightGBM* and *XGBoost*. To further enhance the performance of the model, several customized features were included from TA-Lib, such as **momentum**, **time**, **volatility**, and **volume indicators**, captured at different time intervals.

Hyperparameter search was conducted using **Weights & Biases** Sweeps, which employed **Bayesian inference** to efficiently find the optimal parameters.

See slides : round3-slides.pdf for more informations
