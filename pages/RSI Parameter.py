import yfinance as yf
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def calculate_rsi(data, window):
    delta = data['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


st.title('RSI Parameter Optimization')

ticker = st.text_input('Enter the stock symbol:', 'AAPL')
start_date = st.date_input('Start date', pd.to_datetime('2015-01-01'))
end_date = st.date_input('End date', pd.to_datetime('2022-12-31'))

data = yf.download(ticker, start=start_date, end=end_date)

best_window = None
best_performance = -np.inf

for window in range(1, 31):
    data['RSI'] = calculate_rsi(data, window)
    data['Signal'] = 0
    data.loc[data['RSI'] > 70, 'Signal'] = -1
    data.loc[data['RSI'] < 30, 'Signal'] = 1

    data['Daily Return'] = data['Close'].pct_change()
    data['Strategy Return'] = data['Signal'].shift(1) * data['Daily Return']
    performance = data['Strategy Return'].cumsum().iloc[-1]

    if performance > best_performance:
        best_performance = performance
        best_window = window

# 最適なウィンドウサイズでのRSIとシグナルを計算
data['RSI'] = calculate_rsi(data, best_window)
data['Signal'] = 0
data.loc[data['RSI'] > 70, 'Signal'] = -1
data.loc[data['RSI'] < 30, 'Signal'] = 1
data['Strategy Return'] = data['Signal'].shift(1) * data['Daily Return']
data['Strategy Cumulative Return'] = (1 + data['Strategy Return']).cumprod()

# インタラクティブなグラフの描画
fig = px.line(data, x=data.index, y='Strategy Cumulative Return', title='Strategy Cumulative Return over time')
st.plotly_chart(fig)

st.write(f"The best RSI window size for {ticker} from {start_date} to {end_date} is {best_window}")
