import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import matplotlib
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import os
import sys
import subprocess
from sklearn.linear_model import LinearRegression
import mplfinance.original_flavor as mpf
import datetime
import seaborn
from scipy.stats import linregress

# 高値の始点/支点を取得
def get_highpoint(start, end):
    chart = source[start:end+1]
    while len(chart)>3:
        regression = linregress(
            x = chart['time_id'],
            y = chart['RSI'],
        )
        chart = chart.loc[chart['RSI'] > regression[0] * chart['time_id'] + regression[1]]
    return chart

# 安値の始点/支点を取得
def get_lowpoint(start, end):
    chart = source[start:end+1]
    while len(chart)>3:
        regression = linregress(
            x = chart['time_id'],
            y = chart['RSI'],
        )
        chart = chart.loc[chart['RSI'] < regression[0] * chart['time_id'] + regression[1]]
    return chart


st.set_page_config(layout="wide")
RSI_day = 14
days = 1300
day_until_pay = 14
stage_number = 4

option = st.text_input('銘柄コードを入力してください')
col1, col2, col3 = st.columns(3)
with col1:
    RSI_day = st.selectbox(
        'RSIの日数を何日に設定しますか。',
        (14, 10,11,12,13,15,16,17,18,19,20))
with col2:
    day_until_pay = st.selectbox(
        '何日で決済しますか。',
        (14, 10,11,12,13,15,16,17,18,19,20))
with col3:
    stage_number = st.selectbox(
        'ステージの選択',
        (4,1,2,3,5,6))
    

if option:
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period=f'{days}d')
    hist = hist.reset_index()
    hist = hist.set_index(['Date'])
    hist = hist.rename_axis('Date').reset_index()
    hist = hist.T
    a = hist.to_dict()

    for items in a.values():
            time = items['Date']
            items['Date'] = time.strftime("%Y/%m/%d")

    b = [x for x in a.values()]

    source = pd.DataFrame(b)
    source['time_id'] = source.index + 1
    price = source['Close']

    source['time_id'] = source.index + 1

    #移動平均
    span01=5
    span02=25
    span03=50

    source['sma01'] = price.rolling(window=span01).mean()
    source['sma02'] = price.rolling(window=span02).mean()
    source['sma03'] = price.rolling(window=span03).mean()

    #RSI
    # 前日との差分を計算
    df_diff = source["Close"].diff(1)

    # 計算用のDataFrameを定義
    df_up, df_down = df_diff.copy(), df_diff.copy()

    # df_upはマイナス値を0に変換
    # df_downはプラス値を0に変換して正負反転
    df_up[df_up < 0] = 0
    df_down[df_down > 0] = 0
    df_down = df_down * -1


    # 期間14でそれぞれの平均を算出
    df_up_sma14 = df_up.rolling(window=RSI_day, center=False).mean()
    df_down_sma14 = df_down.rolling(window=RSI_day, center=False).mean()



    # RSIを算出
    source["RSI"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))

    #DMIの計算
    high = source['High']
    low = source['Low']
    close = source['Close']
    pDM = (high - high.shift(1))
    mDM = (low.shift(1) - low)
    pDM.loc[pDM<0] = 0
    pDM.loc[pDM-mDM < 0] = 0
    mDM.loc[mDM<0] = 0
    mDM.loc[mDM-pDM < 0] = 0
    # trの計算
    a = (high - low).abs()
    b = (high - close.shift(1)).abs()
    c = (low - close.shift(1)).abs()
    tr = pd.concat([a, b, c], axis=1).max(axis=1)
    source['tr'] = tr
    source['ATR'] = tr.rolling(20).mean()
    source["stage"] = 1
    
    for a in range(60,days-1):
    #ステージの決定
        if source['sma01'][a]>source['sma02'][a]>source['sma03'][a]:
            source["stage"][a] = 1
        if source['sma02'][a]>source['sma01'][a]>source['sma03'][a]:
            source["stage"][a] = 2
        if source['sma02'][a]>source['sma03'][a]>source['sma01'][a]:
            source["stage"][a] = 3
        if source['sma03'][a]>source['sma02'][a]>source['sma01'][a]:
            source["stage"][a] = 4
        if source['sma03'][a]>source['sma01'][a]>source['sma02'][a]:
            source["stage"][a] = 5
        if source['sma01'][a]>source['sma03'][a]>source['sma02'][a]:
            source["stage"][a] = 6

    
    span=20
    min_interval=3
    source2 = source[:-40]
    win_profit = []
     # 安値の上昇トレンドラインを生成
    for i in source2.index[::20]:
        lowpoint   = get_lowpoint(i, i + span)
        # ポイントが2箇所未満だとエラーになるので回避する
        if len(lowpoint) < 2:
            continue
        # 始点と支点が近過ぎたらトレンドラインとして引かない
        if abs(lowpoint.index[0] - lowpoint.index[1]) < min_interval:
            continue
        regression = linregress(
            x = lowpoint['time_id'],
            y = lowpoint['RSI'],
        )
        #print(regression[0] > 0.0, 'reg_low: ', regression[0], ', ', regression[1], )
        #st.write(lowpoint)
        RSI_lowpoint = pd.DataFrame(lowpoint)
        RSI_lowpoint = RSI_lowpoint.reset_index()
        

        if RSI_lowpoint['RSI'][0]<=30 and RSI_lowpoint['RSI'][1]>=30:
            high = 0
            point1 = RSI_lowpoint['index'][0]
            point2 = RSI_lowpoint['index'][1]
            for num in range(point1,point2):
                if source['High'][num] > high:
                    high = source['High'][num]
            
            for a in range(14):
            #     # if source['High'][point2+a] >= high and source['stage'][point2] == 5:
            #     #     profit = source['Close'][point2+a+14] - source['Close'][point2+a]
            #     #     win_profit.append(profit)
            #     #     break
                if source['High'][point2+a] >= high and source['stage'][point2] == stage_number:
                    after = source['Close'][point2+a+day_until_pay]
                    before = source['Close'][point2+a]
                    profit = after - before
                    win_profit.append(profit)
                    break
    column1, column2 = st.columns(2)
    with column1:
        st.subheader(str(source['Date'][0]) + 'から' + str(source['Date'][days-1]))
        st.subheader('RSIの日数が'+ str(RSI_day) + '日の時')
        st.subheader('儲けは'+str(int(sum(win_profit))*100)+'円')
        st.subheader('発生回数は'+ str(len(win_profit))+ '回')










    RSI_setday = []
    Profit_RSIday = []



    for d in range(8,20):
        RSI_days = d
        #RSI
        #前日との差分を計算
        df_diff = source["Close"].diff(1)

        # 計算用のDataFrameを定義
        df_up, df_down = df_diff.copy(), df_diff.copy()

        # df_upはマイナス値を0に変換
        # df_downはプラス値を0に変換して正負反転
        df_up[df_up < 0] = 0
        df_down[df_down > 0] = 0
        df_down = df_down * -1


        # 期間14でそれぞれの平均を算出
        df_up_sma14 = df_up.rolling(window=RSI_days, center=False).mean()
        df_down_sma14 = df_down.rolling(window=RSI_days, center=False).mean()



        # RSIを算出
        source["RSI2"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))



        
        span=20
        min_interval=3
        source = source[:-20]
        win_profit2 = []
        # 安値の上昇トレンドラインを生成
        for i in source.index[::20]:
            lowpoint   = get_lowpoint(i, i + span)
            # ポイントが2箇所未満だとエラーになるので回避する
            if len(lowpoint) < 2:
                continue
            # 始点と支点が近過ぎたらトレンドラインとして引かない
            if abs(lowpoint.index[0] - lowpoint.index[1]) < min_interval:
                continue
            regression = linregress(
                x = lowpoint['time_id'],
                y = lowpoint['RSI2'],
            )
            #print(regression[0] > 0.0, 'reg_low: ', regression[0], ', ', regression[1], )
            #st.write(lowpoint)
            RSI_lowpoint = pd.DataFrame(lowpoint)
            RSI_lowpoint = RSI_lowpoint.reset_index()
            

            if RSI_lowpoint['RSI2'][0]<=30 and RSI_lowpoint['RSI2'][1]>=30:
                high = 0
                point1 = RSI_lowpoint['index'][0]
                point2 = RSI_lowpoint['index'][1]
                for num in range(point1,point2):
                    if source['High'][num] > high:
                        high = source['High'][num]
                
                for a in range(14):
                #     # if source['High'][point2+a] >= high and source['stage'][point2] == 5:
                #     #     profit = source['Close'][point2+a+14] - source['Close'][point2+a]
                #     #     win_profit.append(profit)
                #     #     break
                    if source['High'][point2+a] >= high and source['stage'][point2] == stage_number:
                        after = source['Close'][point2+a+day_until_pay]
                        before = source['Close'][point2+a]
                        profit = after - before
                        win_profit2.append(profit)
                        break
                    else:
                        continue

        Profit_RSIday.append(sum(win_profit2)*100)
        RSI_setday.append(d)
       
    fig, ax = plt.subplots()
    ax.bar(RSI_setday, Profit_RSIday)
    ax.set_xlabel('Day')
    ax.set_ylabel('Profit Value')
    ax.set_title('RSI Profit Value')

    
    max_index = max(range(len(Profit_RSIday)), key=Profit_RSIday.__getitem__)
    
                
    
    with column1:

        st.subheader('最適なRSI日数は')
        st.subheader(str(RSI_setday[max_index])+ '日')

    with column2:
        st.pyplot(fig)

    

    st.write(RSI_setday)
    st.write(Profit_RSIday)

