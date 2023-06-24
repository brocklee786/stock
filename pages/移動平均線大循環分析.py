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
days = 100
option = st.text_input('銘柄コードを入力してください')
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

    #st.table(source)

    #移動平均
    span01=5
    span02=25
    span03=50

    source['sma01'] = price.rolling(window=span01).mean()
    source['sma02'] = price.rolling(window=span02).mean()
    source['sma03'] = price.rolling(window=span03).mean()
    
    

    last=99
    source['x'] = source["sma01"] - source["sma02"]
    source['y'] = source["sma03"] - source["sma01"]
    source['z'] = source["sma03"] - source["sma02"]
    
    source["stage"] = 1
    stage6_list = []
    stage4_list = []
    stage5_list = []

    for a in range(last+1):
        #ステージの決定
        if source['sma01'][a]>source['sma02'][a]>source['sma03'][a]:
            source["stage"][a] = 1
        if source['sma02'][a]>source['sma01'][a]>source['sma03'][a]:
            source["stage"][a] = 2
        if source['sma02'][a]>source['sma03'][a]>source['sma01'][a]:
            source["stage"][a] = 3
        if source['sma03'][a]>source['sma02'][a]>source['sma01'][a]:
            source["stage"][a] = 4
            stage4_list.append(a)
        if source['sma03'][a]>source['sma01'][a]>source['sma02'][a]:
            source["stage"][a] = 5
            stage5_list.append(a)
        if source['sma01'][a]>source['sma03'][a]>source['sma02'][a]:
            source["stage"][a] = 6
            stage6_list.append(a)



    stage6_end = stage6_list[-1]
    stage4_end = stage4_list[-1]
    stage5_end = stage5_list[-1]
        

    stage1_now = []
    stage5_now = []
    stage6_now = []
    #ステージ１
    if source['sma01'][last]>source['sma02'][last]>source['sma03'][last]:
        stage="第1ステージ"
        st.write("第1ステージ")
        for a in range(stage6_end+1, last+1):
            stage1_now.append(a)

        sma02_sma01 = []
        for num in stage1_now:
            sma02_sma01.append(source["x"][num])

        

        x = pd.DataFrame(stage1_now)
        y = pd.DataFrame(sma02_sma01)
                    
        model = LinearRegression()
        model.fit(x,y)

        figure, ax = plt.subplots(figsize=(8,4))
        plt.plot(x,y,'o')
        plt.plot(x,model.predict(x))
        
        a = model.coef_
        b = model.intercept_
        #st.write('a = ', model.coef_) 
        #st.write('b = ', model.intercept_)
        st.pyplot(figure)
        days_until6 = -b/a - last
        st.write('第2ステージまで',int(days_until6))
        #短期の傾き
        tilt_short = source['sma01'][last] - source['sma01'][last-1]
        tilt_short2 = (source['sma01'][last] - source['sma01'][last-3]) / 3
        #中期の傾き
        tilt_mid = source['sma02'][last] - source['sma02'][last-1]
        tilt_mid2 = (source['sma02'][last] - source['sma02'][last-3]) / 3
        #長期の傾き
        tilt_long = source['sma03'][last] - source['sma03'][last-1]
        tilt_long2 = (source['sma03'][last] - source['sma03'][last-3]) / 3
        st.write("短期の傾き", tilt_short, tilt_short2)
        st.write("中期の傾き", tilt_mid, tilt_mid2)
        st.write("長期の傾き", tilt_long, tilt_long2)
    #ステージ２
    if source['sma02'][last]>source['sma01'][last]>source['sma03'][last]:
        stage="第2ステージ"
        st.write("第2ステージ")
    #ステージ３
    if source['sma02'][last]>source['sma03'][last]>source['sma01'][last]:
        stage="第3ステージ"
        st.write("第3ステージ")
    #ステージ４
    if source['sma03'][last]>source['sma02'][last]>source['sma01'][last]:
        stage="第4ステージ"
        st.write("第4ステージ")
    #ステージ５
    if source['sma03'][last]>source['sma01'][last]>source['sma02'][last]:
        stage="第5ステージ"
        st.write("第5ステージ")
        for a in range(stage4_end+1, last+1):
            stage5_now.append(a)

        sma03_sma01 = []
        for num in stage5_now:
            sma03_sma01.append(source["y"][num])

        

        x = pd.DataFrame(stage5_now)
        y = pd.DataFrame(sma03_sma01)
                    
        model = LinearRegression()
        model.fit(x,y)

        figure, ax = plt.subplots(figsize=(8,4))
        plt.plot(x,y,'o')
        plt.plot(x,model.predict(x))
        
        a = model.coef_
        b = model.intercept_
        #st.write('a = ', model.coef_) 
        #st.write('b = ', model.intercept_)
        st.pyplot(figure)
        days_until6 = -b/a - last
        st.write('第6ステージまで',int(days_until6))
        #短期の傾き
        tilt_short = source['sma01'][last] - source['sma01'][last-1]
        tilt_short2 = (source['sma01'][last] - source['sma01'][last-3]) / 3
        #中期の傾き
        tilt_mid = source['sma02'][last] - source['sma02'][last-1]
        tilt_mid2 = (source['sma02'][last] - source['sma02'][last-3]) / 3
        #長期の傾き
        tilt_long = source['sma03'][last] - source['sma03'][last-1]
        tilt_long2 = (source['sma03'][last] - source['sma03'][last-3]) / 3
        st.write("短期の傾き", tilt_short, tilt_short2)
        st.write("中期の傾き", tilt_mid, tilt_mid2)
        st.write("長期の傾き", tilt_long, tilt_long2)


    #ステージ６
    if source['sma01'][last]>source['sma03'][last]>source['sma02'][last]:
        stage="第6ステージ"
        st.write("第6ステージ")
        for a in range(stage5_end+1, last+1):
            stage6_now.append(a)

        sma03_sma02 = []
        for num in stage6_now:
            sma03_sma02.append(source["z"][num])

        

        x = pd.DataFrame(stage6_now)
        y = pd.DataFrame(sma03_sma02)
                    
        model = LinearRegression()
        model.fit(x,y)

        figure, ax = plt.subplots(figsize=(8,4))
        plt.plot(x,y,'o')
        plt.plot(x,model.predict(x))
        
        a = model.coef_
        b = model.intercept_
        #st.write('a = ', model.coef_) 
        #st.write('b = ', model.intercept_)
        st.pyplot(figure)
        days_until1 = -b/a - last
        st.write('第1ステージまで',int(days_until1))
        #短期の傾き
        tilt_short = source['sma01'][last] - source['sma01'][last-1]
        tilt_short2 = (source['sma01'][last] - source['sma01'][last-3]) / 3
        #中期の傾き
        tilt_mid = source['sma02'][last] - source['sma02'][last-1]
        tilt_mid2 = (source['sma02'][last] - source['sma02'][last-3]) / 3
        #長期の傾き
        tilt_long = source['sma03'][last] - source['sma03'][last-1]
        tilt_long2 = (source['sma03'][last] - source['sma03'][last-3]) / 3
        st.write("短期の傾き", tilt_short, tilt_short2)
        st.write("中期の傾き", tilt_mid, tilt_mid2)
        st.write("長期の傾き", tilt_long, tilt_long2)

            ## チャートを単回帰分析し、得られる単回帰直線よりも上（下）の値だけで再度単回帰分析...
        ## これを繰り返し、高値（安値）を2～3点に絞り込む

    # 高値の始点/支点を取得
    def get_highpoint(start, end):
        chart = source[start:end+1]
        while len(chart)>3:
            regression = linregress(
                x = chart['time_id'],
                y = chart['High'],
            )
            chart = chart.loc[chart['High'] > regression[0] * chart['time_id'] + regression[1]]
        return chart

    # 安値の始点/支点を取得
    def get_lowpoint(start, end):
        chart = source[start:end+1]
        while len(chart)>3:
            regression = linregress(
                x = chart['time_id'],
                y = chart['Low'],
            )
            chart = chart.loc[chart['Low'] < regression[0] * chart['time_id'] + regression[1]]
        return chart

    def g_trendlines(span=20, min_interval=3):
        trendlines = []

        # 高値の下降トレンドラインを生成
        for i in source.index[::10]:
            highpoint = get_highpoint(i, i + span)
            # ポイントが2箇所未満だとエラーになるので回避する
            if len(highpoint) < 2:
                continue
            # 始点と支点が近過ぎたらトレンドラインとして引かない
            if abs(highpoint.index[0] - highpoint.index[1]) < min_interval:
                continue
            regression = linregress(
                x = highpoint['time_id'],
                y = highpoint['High'],
            )
            print(regression[0] < 0.0, 'reg_high: ', regression[0], ', ', regression[1], )

            # 下降してるときだけ
            if regression[0] < 0.0:
                trendlines.append(regression[0] * source['time_id'][i:i+span*2] + regression[1])

        # 安値の上昇トレンドラインを生成
        for i in source.index[::10]:
            lowpoint   = get_lowpoint(i, i + span)
            # ポイントが2箇所未満だとエラーになるので回避する
            if len(lowpoint) < 2:
                continue
            # 始点と支点が近過ぎたらトレンドラインとして引かない
            if abs(lowpoint.index[0] - lowpoint.index[1]) < min_interval:
                continue
            regression = linregress(
                x = lowpoint['time_id'],
                y = lowpoint['Low'],
            )
            print(regression[0] > 0.0, 'reg_low: ', regression[0], ', ', regression[1], )

            # 上昇してるときだけ
            if regression[0] > 0.0:
                trendlines.append(regression[0] * source['time_id'][i:i+span*2] + regression[1])

        return trendlines


    figure, axis1 = plt.subplots(figsize=(15,7))

    # ローソク足
    mpf.candlestick2_ohlc(
        axis1,
        opens  = source.Open.values,
        highs  = source.High.values,
        lows   = source.Low.values,
        closes = source.Close.values,
        width=0.6, colorup='#77d879', colordown='#db3f3f'
    )

    # トレンドラインたちを引く
    for i, line in enumerate(g_trendlines()):
        axis1.plot(line, label=i)

    # X軸の見た目を整える
    xticks_number  = 12 # 12本刻みに目盛りを書く
    xticks_index   = range(0, len(source), xticks_number)


    # axis1を装飾 ( plt.sca(axis): set current axis )
    plt.sca(axis1)

    plt.legend()
    st.pyplot(figure,use_container_width=True)


    
