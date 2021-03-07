import pandas as pd
from sklearn import linear_model
from src.data import Data
import matplotlib.pyplot as plt


if __name__ == '__main__':
    data = Data().values
    features = pd.DataFrame(data, columns=['Forcing', 'Irradiance', 'SO2', 'Aerosols'])
    target = pd.DataFrame(data, columns=['Temperature'])
    lm = linear_model.LinearRegression()
    model = lm.fit(features, target)
    predictions = lm.predict(features)
    plt.plot(predictions)
    plt.plot(target.values)
    plt.show()