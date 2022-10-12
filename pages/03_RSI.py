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


st.set_page_config(layout="wide")

st.title('RSI分析')
option = st.text_input('銘柄コードを入力してください')
if option:
        days = st.slider('日数', 1, 2000, 500)
        ticker = str(option) + '.T'
        tkr = yf.Ticker(ticker)
        hist = tkr.history(period='2000d')
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

        #移動平均
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

        #RSIの日数を指定
        RSI_days = st.slider('RSIの日数', 1, 20, 14)
        # 期間14でそれぞれの平均を算出
        df_up_sma14 = df_up.rolling(window=RSI_days, center=False).mean()
        df_down_sma14 = df_down.rolling(window=RSI_days, center=False).mean()
        
      

        # RSIを算出
        source["RSI"] = 100.0 * (df_up_sma14 / (df_up_sma14 + df_down_sma14))
        source = source.loc[::-1]
        Price = []
        RSI_list = []

        
        for i in range(15,days):
                #上昇トレンドのとき
                
                sub1 = source['sma01'][2000-i] - source['sma01'][2000-i-1]
                sub2 = source['sma01'][2000-i-1] - source['sma01'][2000-i-2]
                sub3 = source['RSI'][2000-i-1+14]
                if sub1<0 and sub2>0:
                        if sub3 < 50:
                                Price.append(source['Close'][2000-i-1])
                                AVE_RSI = (source['RSI'][2000-i-1] + source['RSI'][2000-i] + source['RSI'][2000-i+1] + source['RSI'][2000-i+2] + source['RSI'][2000-i+3] + source['RSI'][2000-i+4] + source['RSI'][2000-i+5] + source['RSI'][2000-i+6] + source['RSI'][2000-i+7] + source['RSI'][2000-i+8]) / 10
                                RSI_list.append(AVE_RSI)
        
        
        
        figure, ax = plt.subplots()
        plt.scatter(Price, RSI_list)

        plt.xlabel("PRICE")
        plt.ylabel("RSI")

        figure.savefig('graph.png')	
        image = Image.open('graph.png')
        
        
        
        Price2= []
        RSI_list2 = []

        
        for i in range(15,days):
                #下降トレンド
                
                sub1 = source['sma01'][2000-i] - source['sma01'][2000-i-1]
                sub2 = source['sma01'][2000-i-1] - source['sma01'][2000-i-2]
                
                if sub1>0 and sub2<0:
                        if source['RSI'][2013-i] > 50:
                                Price2.append(source['Close'][2000-i-1])
                                AVE_RSI2 = (source['RSI'][2000-i-1] + source['RSI'][2000-i] + source['RSI'][2000-i+1] + source['RSI'][2000-i+2] + source['RSI'][2000-i+3] + source['RSI'][2000-i+4] + source['RSI'][2000-i+5] + source['RSI'][2000-i+6] + source['RSI'][2000-i+7] + source['RSI'][2000-i+8]) / 10
                                RSI_list2.append(AVE_RSI2)
                                
        
                        

        figure, ax = plt.subplots()
        plt.scatter(Price2, RSI_list2)

        plt.xlabel("PRICE")
        plt.ylabel("RSI")

        figure.savefig('graph2.png')	
        image2 = Image.open('graph2.png')
        

        left_column, right_column = st.columns(2)

        with left_column:
                st.write('上昇トレンドから下降トレンドへの転換時')
                st.image(image,use_column_width='TRUE')
        
        with right_column:
                st.write('下降トレンドから上昇トレンドへの転換時')
                st.image(image2,use_column_width='TRUE')

        sum_RSI = sum(RSI_list)
        AVEG_RSI = sum_RSI / len(RSI_list)
        st.write('上昇トレンドから下降トレンドへの転換時の平均RSIは'+str(AVEG_RSI))
        
        sum_RSI2 = sum(RSI_list2)
        AVEG_RSI2 = sum_RSI / len(RSI_list2)
        st.write('上昇トレンドから下降トレンドへの転換時の平均RSIは'+str(AVEG_RSI))
