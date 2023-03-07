import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from pandas_datareader import data
import datetime
import streamlit as st

st.set_page_config(layout="wide")
st.title('機械学習')
option = st.text_input('銘柄コードを入力してください')

if option:
          start = datetime.date(2015,1,1)
          end = datetime.date.today()
          data_train = data.DataReader(option + '.JP','stooq').sort_values('Date', ascending=True)

          data_train['ds'] = data_train.index
          data_train = data_train.rename({'Close':'y'}, axis=1)
#           data_train['y'] = np.log(data_train['y'])
         


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
              periods=60, 
              freq = 'd'  
          )

          pred = model.predict(future)
          st.write(pred.tail(-65:))
          fig_pred = model.plot(pred)
          st.pyplot(fig_pred)
          st.pyplot(model.plot_components(forecast_data))
          
