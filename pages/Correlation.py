import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

option1 = st.text_input('1つ目の銘柄コードを入力してください')
option2 = st.text_input('２つ目の銘柄コードを入力してください')
if option1 and option2:
    #一つ目のデータ
    ticker = str(option1) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='1700d')
    hist = hist.reset_index()
    hist = hist.set_index(['Date'])
    hist = hist.rename_axis('Date').reset_index()
    hist = hist.T
    a = hist.to_dict()

    for items in a.values():
            time = items['Date']
            items['Date'] = time.strftime("%Y/%m/%d")

    b = [x for x in a.values()]

    source1 = pd.DataFrame(b)
    Date1 = source1['Date']
    stock_data1 = source1['Close']
    #二つ目のデータ
    ticker = str(option2) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='1700d')
    hist = hist.reset_index()
    hist = hist.set_index(['Date'])
    hist = hist.rename_axis('Date').reset_index()
    hist = hist.T
    a = hist.to_dict()

    for items in a.values():
            time = items['Date']
            items['Date'] = time.strftime("%Y/%m/%d")

    b = [x for x in a.values()]

    source2 = pd.DataFrame(b)
    Date2 = source2['Date']
    stock_data2 = source2['Close']

    code1 = option1
    code2 = option2

    correlation = np.corrcoef(stock_data1, stock_data2)[1, 0]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(Date1.values, stock_data1.values, label=f" {code1}")
    ax.plot(Date2.values, stock_data2.values, label=f" {code2}")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title("Correlation")
    plt.legend()
    plt.grid()
    st.pyplot(fig)

    st.subheader('相関係数は' + str(correlation))
    
