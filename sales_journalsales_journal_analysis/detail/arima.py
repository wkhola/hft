#!/usr/bin/python
# encoding:utf-8
import pandas as pd
import numpy as np
import common
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

conn = common.conn_mysql

data = pd.read_csv('../templates/daily_order.csv', index_col='datefmt')


def test_stationarity(timeseries):
    # 决定起伏统计
    rolmean = pd.rolling_mean(timeseries, window=12)  # 对size个数据进行移动平均
    rol_weighted_mean = pd.ewma(timeseries, span=12)  # 对size个数据进行加权移动平均
    rolstd = pd.rolling_std(timeseries, window=12)  # 偏离原始值多少
    # 画出起伏统计
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    weighted_mean = plt.plot(rol_weighted_mean, color='green', label='weighted Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    # 进行df测试
    print 'Result of Dickry-Fuller test'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical value(%s)' % key] = value
    print dfoutput


ts = data['amounts']
plt.plot(ts)
# plt.show()
test_stationarity(ts)
plt.show()
