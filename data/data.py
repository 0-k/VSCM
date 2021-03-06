import pandas as pd
import matplotlib.pyplot as plt


def __resample(data):
    return data.resample('Y').mean().interpolate(method='linear')


def ch4():
    data = pd.read_csv('ch4-concentration.csv', index_col=0, names=['CH4'], header=0,  parse_dates=True, squeeze=True)
    return __resample(data)


def co2():
    data = pd.read_csv('global-co-concentration-ppm.csv', index_col=0, names=['CO2'], header=0, parse_dates=True,
                      skiprows=range(1, 1732), squeeze=True)
    return __resample(data)


def irradiance():
    data = pd.read_csv('irradiance.csv', index_col=0, names=['Irradiance'], header=0,  parse_dates=True,
                             skiprows=range(1, 141), squeeze=True)
    return __resample(data)


def so2():
    data = pd.read_csv('so-emissions-by-world-region-in-million-tonnes.csv', index_col=2, header=0,
                      parse_dates=True, names=['.', '..', 'SO2'], skiprows=range(1, 86))
    data = data['SO2']
    return __resample(data)


def aerosols():
    dates = pd.date_range(start='1/1/1850', periods=1953, freq='M')
    data = pd.read_csv('tau.line_2012.12.txt', header=None, sep='  ', skiprows=range(0, 4),
                           names=['.', 'Aerosols', '..', '...'])
    data = data.set_index(dates)
    data = data['Aerosols']
    return __resample(data)


def temperature():
    t1 = __temperature_dataset1()
    t2 = __temperature_dataset2()
    t3 = __temperature_dataset3()
    t = pd.DataFrame([t1, t2, t3]).transpose()
    return t.mean(axis=1)


def __temperature_dataset1():
    data = pd.read_csv('temperature-anomaly.csv', index_col=1, header=0,
                                       parse_dates=True, squeeze=True, skiprows=range(171, 681),
                                       names=['.', 'Temperature1', '..', '...'])
    data = data['Temperature1']
    return __resample(data)


def __temperature_dataset2():
    data = pd.read_csv('temperature-NASA.csv', index_col=0, header=2, parse_dates=True, squeeze=True,
                        names=['Temperature2', '.'])
    data = data['Temperature2']
    return __resample(data)


def __temperature_dataset3():
    data = pd.read_csv('temperature-NOAA.csv', index_col=0, header=4, parse_dates=True, squeeze=True,
                        names=['Temperature3'])
    return __resample(data)


if __name__ == '__main__':
    t = temperature()
    plt.plot(t)
    plt.show()