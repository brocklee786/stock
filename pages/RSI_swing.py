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

st.set_page_config(layout="wide")

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


codes1 = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']
codes2 = ['6141']

win_profit = []


#option = st.text_input('銘柄コードを入力してください')
for code in codes1:
    option = code
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='1300d')
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
    df_up_sma14 = df_up.rolling(window=14, center=False).mean()
    df_down_sma14 = df_down.rolling(window=14, center=False).mean()



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
    
    for a in range(80,1299):
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
    source = source[:-40]
    
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
            y = lowpoint['RSI'],
        )
        #print(regression[0] > 0.0, 'reg_low: ', regression[0], ', ', regression[1], )
        #st.write(lowpoint)
        RSI_lowpoint = pd.DataFrame(lowpoint)
        RSI_lowpoint = RSI_lowpoint.reset_index()
        #st.write(RSI_lowpoint)
        if RSI_lowpoint['RSI'][0]<=30 and RSI_lowpoint['RSI'][1]>=30:
            st.write(RSI_lowpoint)
            high = 0
            point1 = RSI_lowpoint['index'][0]
            point2 = RSI_lowpoint['index'][1]
            for num in range(point1,point2):
                if source['High'][num] > high:
                    high = source['High'][num]
            st.write(code)
            for a in range(14):
                # if source['High'][point2+a] >= high and source['stage'][point2] == 5:
                #     profit = source['Close'][point2+a+14] - source['Close'][point2+a]
                #     win_profit.append(profit)
                #     break
                if source['High'][point2+a] >= high and source['stage'][point2] == 4:
                    profit = source['Close'][point2+a+14] - source['Close'][point2+a]
                    win_profit.append(profit)
                    break


    

st.write(sum(win_profit))
st.write(len(win_profit))
st.write(sum(win_profit/len(win_profit)))
                
            




    
