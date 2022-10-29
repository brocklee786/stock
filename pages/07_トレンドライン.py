from math import nan
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
import datetime
import seaborn
from scipy.stats import linregress
import mplfinance.original_flavor as mpf


 
st.set_page_config(layout="wide")
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (50,100,150))
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


        figure, (axis1,axis2) = plt.subplots(2, 1, figsize=(20,10), dpi=200, gridspec_kw = {'height_ratios':[3, 1]})

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
