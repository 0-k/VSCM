import pandas as pd
from sklearn import linear_model
from src.data import Data
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    data = Data().values
    features = pd.DataFrame(data, columns=['Forcing', 'Irradiance', 'SO2', 'Aerosols'])
    target = pd.DataFrame(data, columns=['Temperature'])

    features_train = features.iloc[:120]  # let the model train with the first 100 years of data (1850-1969)
    target_train = target.iloc[:120]
    features_test = features.iloc[120:]  # predict the rest of years (1970 - 2010)
    target_test = target.iloc[120:]

    lm = linear_model.LinearRegression()
    model = lm.fit(features_train, target_train)
    predictions = lm.predict(features_test)

    years_full = np.arange(1850, 2011)
    years_prediction = np.arange(1970, 2011)
    print(years_full)

    plt.plot(years_full, target.values)
    plt.plot(years_prediction, predictions)

    plt.show()