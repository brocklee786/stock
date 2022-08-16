import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from pandas_datareader.data import DataReader
import datetime

start = datetime.date(2010,1,1)
end = datetime.date(2021,1,1)
data_train = DataReader('^N225', 'yahoo', start, end)

data_train['ds'] = data_train.index
data_train = data_train.rename({'Adj Close':'y'}, axis=1)

data_train['y'] = np.log(data_train['y'])


params = {'growth': 'linear',
          'changepoints': None,
          'n_changepoints': 25,
          'changepoint_range': 0.8,
          'yearly_seasonality': 'auto',
          'weekly_seasonality': 'auto',
          'daily_seasonality': 'auto',
          'holidays': None,
          'seasonality_mode': 'additive',
          'seasonality_prior_scale': 10.0,
          'holidays_prior_scale': 10.0,
          'changepoint_prior_scale': 0.05,
          'mcmc_samples': 0,
          'interval_width': 0.8,
          'uncertainty_samples': 1000,
          'stan_backend': None}

model = Prophet(**params)
model.fit(data_train)

future = model.make_future_dataframe(
    periods=600, 
    freq = 'd'  
)

pred = model.predict(future)
fig_pred = model.plot(pred)

fig_components = model.plot_components(pred)

start = datetime.date(2021,1,1)
end = datetime.date(2022,7,1)

data_test = DataReader('^N225', 'yahoo', start, end)

data_test['ds'] = data_test.index
data_test = data_test.rename({'Adj Close':'y'} ,axis=1)
data_test['y'] = np.log(data_test['y'])

model = Prophet()
model.fit(data_test)

fig_test = model.plot(pred)
