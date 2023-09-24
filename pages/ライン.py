import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import linregress

# タイトルと説明
st.title('Interactive Candlestick Chart with Support, Resistance, and Trend Lines')
st.write('This application displays a candlestick chart for the selected stock symbol with calculated support, resistance, and trend lines.')

# ユーザー入力の取得
ticker_symbol = st.text_input('Enter Stock Symbol:', '7004.T')
start_date = st.date_input('Start Date', pd.to_datetime('2023-08-01'))
end_date = st.date_input('End Date', pd.to_datetime('2023-09-22'))

# データの取得
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
stock_data.reset_index(inplace=True)
stock_data['time_id'] = range(len(stock_data))

# 高値の始点/支点を取得
def get_highpoint(source, start, end):
    chart = source[start:end+1]
    while len(chart)>3:
        regression = linregress(x=chart['time_id'], y=chart['High'])
        chart = chart.loc[chart['High'] > regression.slope * chart['time_id'] + regression.intercept]
    return chart

# 安値の始点/支点を取得
def get_lowpoint(source, start, end):
    chart = source[start:end+1]
    while len(chart)>3:
        regression = linregress(x=chart['time_id'], y=chart['Low'])
        chart = chart.loc[chart['Low'] < regression.slope * chart['time_id'] + regression.intercept]
    return chart

def g_trendlines(source, span=20, min_interval=3):
    trendlines = []
    for i in range(0, len(source), 10):
        if i + span >= len(source):
            break
        highpoint = get_highpoint(source, i, i + span)
        if len(highpoint) >= 2 and abs(highpoint.index[0] - highpoint.index[1]) >= min_interval:
            regression = linregress(x=highpoint['time_id'], y=highpoint['High'])
            if regression.slope < 0.0:
                start_y = regression.slope * highpoint['time_id'].iloc[0] + regression.intercept
                end_y = regression.slope * highpoint['time_id'].iloc[-1] + regression.intercept
                trendlines.append(((highpoint['Date'].iloc[0], start_y), (highpoint['Date'].iloc[-1], end_y)))
        
        lowpoint = get_lowpoint(source, i, i + span)
        if len(lowpoint) >= 2 and abs(lowpoint.index[0] - lowpoint.index[1]) >= min_interval:
            regression = linregress(x=lowpoint['time_id'], y=lowpoint['Low'])
            if regression.slope > 0.0:
                start_y = regression.slope * lowpoint['time_id'].iloc[0] + regression.intercept
                end_y = regression.slope * lowpoint['time_id'].iloc[-1] + regression.intercept
                trendlines.append(((lowpoint['Date'].iloc[0], start_y), (lowpoint['Date'].iloc[-1], end_y)))
    return trendlines

# ローソク足チャートの作成
candlestick = go.Candlestick(x=stock_data['Date'],
                             open=stock_data['Open'],
                             high=stock_data['High'],
                             low=stock_data['Low'],
                             close=stock_data['Close'],
                             name='Candlesticks')

# サポートラインと抵抗線の計算
window_size = 30
stock_data['Short_Term_Support'] = stock_data['Low'].rolling(window=window_size, min_periods=1).min()
stock_data['Short_Term_Resistance'] = stock_data['High'].rolling(window=window_size, min_periods=1).max()

# サポートラインと抵抗線の作成
support_line = go.Scatter(x=stock_data['Date'], y=stock_data['Short_Term_Support'],
                          mode='lines', name='Support Line',
                          line=dict(color='green', width=2, dash='dash'))
resistance_line = go.Scatter(x=stock_data['Date'], y=stock_data['Short_Term_Resistance'],
                             mode='lines', name='Resistance Line',
                             line=dict(color='red', width=2, dash='dash'))

# データの追加とプロット
fig = go.Figure(data=[candlestick, support_line, resistance_line],
                layout=go.Layout(title='Candlestick Chart with Support, Resistance, and Trend Lines',
                                 xaxis=dict(title='Date'),
                                 yaxis=dict(title='Price'),
                                 autosize=False,
                                 width=1000,
                                 height=500))

# トレンドラインの計算と作成
trendlines = g_trendlines(stock_data)
for i, (start, end) in enumerate(trendlines):
    trend_line = go.Scatter(x=[start[0], end[0]], y=[start[1], end[1]], mode='lines', name=f'Trend Line {i}',
                            line=dict(color='blue', width=2))
    fig.add_trace(trend_line)

# Streamlitでのプロットの表示
st.plotly_chart(fig)
