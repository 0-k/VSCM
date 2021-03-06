import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import constants


class Data:

    def __init__(self):
        self.values = self.__prepare_data()

    def __prepare_data(self):
        temperature = self.__temperature()
        forcing = self.__forcing()
        co2 = self.__co2()
        ch4 = self.__ch4()
        irradiance = self.__irradiance()
        so2 = self.__so2()
        aerosols = self.__aerosols()
        return pd.DataFrame([temperature, forcing, co2, ch4, irradiance, so2, aerosols]).transpose()

    def __temperature(self):
        t1 = self.__temperature_dataset1()
        t2 = self.__temperature_dataset2()
        t3 = self.__temperature_dataset3()
        t = pd.DataFrame([t1, t2, t3]).transpose()
        return t.mean(axis=1).rename('Temperature')

    def __temperature_dataset1(self):
        df = pd.read_csv('temperature-anomaly.csv', index_col=1, header=0, parse_dates=True, squeeze=True,
                         skiprows=range(171, 681), names=['.', 'Temperature1', '..', '...'])
        df = df['Temperature1']
        return self.__resample(df)

    def __temperature_dataset2(self):
        df = pd.read_csv('temperature-NASA.csv', index_col=0, header=2, parse_dates=True, squeeze=True,
                           names=['Temperature2', '.'])
        df = df['Temperature2']
        return self.__resample(df)

    def __temperature_dataset3(self):
        df = pd.read_csv('temperature-NOAA.csv', index_col=0, header=4, parse_dates=True, squeeze=True,
                           names=['Temperature3'])
        return self.__resample(df)

    def __forcing(self):
        co2 = self.__co2()
        co2 = co2 - constants.PRE_INDUSTRIAL_CO2
        ch4 = self.__ch4()
        ch4 = (ch4 - constants.PRE_INDUSTRIAL_CH4)/1000 * constants.GWP_CH4
        forcing = co2 + ch4
        return forcing.rename('Forcing')

    def __co2(self):
        data = pd.read_csv('global-co-concentration-ppm.csv', index_col=0, names=['CO2'], header=0, parse_dates=True,
                          skiprows=range(1, 1732), squeeze=True)
        return self.__resample(data)

    def __ch4(self):
        data = pd.read_csv('ch4-concentration.csv', index_col=0, names=['CH4'], header=0,  parse_dates=True, squeeze=True)
        return self.__resample(data)

    def __irradiance(self):
        data = pd.read_csv('irradiance.csv', index_col=0, names=['Irradiance'], header=0,  parse_dates=True,
                                 skiprows=range(1, 141), squeeze=True)
        return self.__resample(data)

    def __so2(self):
        data = pd.read_csv('so-emissions-by-world-region-in-million-tonnes.csv', index_col=2, header=0,
                          parse_dates=True, names=['.', '..', 'SO2'], skiprows=range(1, 86))
        data = data['SO2']
        return self.__resample(data)

    def __aerosols(self):
        dates = pd.date_range(start='1/1/1850', periods=1953, freq='M')
        data = pd.read_csv('tau.line_2012.12.txt', header=None, sep='  ', skiprows=range(0, 4),
                               names=['.', 'Aerosols', '..', '...'])
        data = data.set_index(dates)
        data = data['Aerosols']
        return self.__resample(data)

    @staticmethod
    def __resample(dataframe):
        return dataframe.resample('Y').mean().interpolate(method='linear')


if __name__ == '__main__':
    data = Data().values
    data = data.dropna()
    print('Correlation coefficient: ' + str(np.corrcoef(data.Temperature, data.Forcing)[0,1].round(3)))
    plt.scatter(data.Temperature, data.Forcing)
    plt.show()

