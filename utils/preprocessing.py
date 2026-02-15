import numpy as np
from sklearn.preprocessing import MinMaxScaler

LOOK_BACK = 12


def prepare_lstm_data(series):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(series.reshape(-1, 1))

    X, y = [], []
    for i in range(LOOK_BACK, len(scaled)):
        X.append(scaled[i - LOOK_BACK:i, 0])
        y.append(scaled[i, 0])

    X = np.array(X).reshape(-1, LOOK_BACK, 1)
    y = np.array(y)

    return X, y, scaler
