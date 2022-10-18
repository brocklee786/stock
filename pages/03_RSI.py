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
                        #if sub3 < 50:
                        if source['RSI'][2000-i-1] > 50:
                                Price.append(source['Close'][2000-i-1])
                                AVE_RSI = (source['RSI'][2000-i-3] + source['RSI'][2000-i-2] + source['RSI'][2000-i-1]) / 3
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
                        #if source['RSI'][2013-i] > 50:
                        if source['RSI'][2000-i-1] < 50:
                                Price2.append(source['Close'][2000-i-1])
                                AVE_RSI2 = (source['RSI'][2000-i-3] + source['RSI'][2000-i-2] + source['RSI'][2000-i-1]) / 3
                                RSI_list2.append(AVE_RSI2)
                                
        
                        

        figure, ax = plt.subplots()
        plt.scatter(Price2, RSI_list2)

        plt.xlabel("PRICE")
        plt.ylabel("RSI")

        figure.savefig('graph2.png')	
        image2 = Image.open('graph2.png')
        

        left_column, right_column = st.columns(2)

        

        sum_RSI = sum(RSI_list)
        AVEG_RSI = sum_RSI / len(RSI_list)
        AVEG_RSI = int(AVEG_RSI)
        
        sum_RSI2 = sum(RSI_list2)
        AVEG_RSI2 = sum_RSI2 / len(RSI_list2)
        AVEG_RSI2 = int(AVEG_RSI2)
        
        
        #RSIが転換した時に移動平均線も転換しているか

        change = []
        no_change = []
        change2 = []
        no_change2 = []
        
        for i in range(15,days):
                #上昇トレンドから下降トレンドのとき
                
                sub1 = source['RSI'][2000-i] - source['RSI'][2000-i-1]
                sub2 = source['RSI'][2000-i-1] - source['RSI'][2000-i-2]
                sub3 = source['RSI'][2000-i-1+14]
                if sub1<0 and sub2>0 and source['RSI'][2000-i-3] > 60:
                        for a in range(1,5):
                                trend_change = source['sma01'][2000-i+a] - source['sma01'][2000-i-1+a]
                                if trend_change < 0:
                                        change.append(1)
                                        break
                                else:
                                        no_change.append(1)


        for i in range(15,days):
                #下降トレンドから上昇トレンドのとき
                
                sub1 = source['RSI'][2000-i] - source['RSI'][2000-i-1]
                sub2 = source['RSI'][2000-i-1] - source['RSI'][2000-i-2]
                sub3 = source['RSI'][2000-i-1+14]
                if sub1>0 and sub2<0 and source['RSI'][2000-i-3] < 40:
                        for a in range(1,5):
                                trend_change = source['sma01'][2000-i+a] - source['sma01'][2000-i-1+a]
                                if trend_change > 0:
                                        change2.append(1)
                                        break
                                else:
                                        no_change2.append(1)

        
        probability = len(change) * 100 / (len(change) + len(no_change))
        probability = int(probability)
        probability2 = len(change2) * 100 / (len(change2) + len(no_change2))
        probability2 = int(probability2)

        percent50_raise = []
        percent50_unraise = []

        #50%を超えたときに上昇が続いているか(順張り)
        for i in range(15,days):
                raise_continue = source['sma01'][2000-i+4] - source['sma01'][2000-i-1]
                if source['RSI'][2000-i-1] > 50 and source['RSI'][2000-i-2] < 50:
                        if raise_continue > 0:
                                percent50_raise.append(1)
                        else:
                                percent50_unraise.append(1)

        percent50_probability = len(percent50_raise) * 100 / (len(percent50_raise) + len(percent50_unraise))
        percent50_probability = int(percent50_probability)
        
        
        
        

        with left_column:
                st.write('<span style="color:green">上昇トレンドから下降トレンドへの転換時</span>', unsafe_allow_html=True)
                st.image(image,use_column_width='TRUE')
                st.write('上昇トレンドから下降トレンドへの転換時の平均RSIは'+str(AVEG_RSI) + '%')
                st.write('確率は' + str(probability) + '%')
        with right_column:
                st.write('<span style="color:green">下降トレンドから上昇トレンドへの転換時</span>', unsafe_allow_html=True)
                st.image(image2,use_column_width='TRUE')
                st.write('下降トレンドから上昇トレンドへの転換時の平均RSIは'+str(AVEG_RSI2) + '%')
                st.write('確率は' + str(probability2) + '%')
        
        
        st.write('RSI50%を超えた時、上昇トレンドが続く確率は'+str(percent50_probability) + '%')
        
        change5_probability = []
        #フィッティングした際にRSIが一番高くなるものを算出
        for i in range(1,20):
                #RSI
                # 前日との差分を計算
                source = source.loc[::-1]
                
                df_diff = source["Close"].diff(1)

                # 計算用のDataFrameを定義
                df_up, df_down = df_diff.copy(), df_diff.copy()

                # df_upはマイナス値を0に変換
                # df_downはプラス値を0に変換して正負反転
                df_up[df_up < 0] = 0
                df_down[df_down > 0] = 0
                df_down = df_down * -1

                # 期間14でそれぞれの平均を算出
                df_up_sma_random = df_up.rolling(window=i, center=False).mean()
                df_down_sma_random = df_down.rolling(window=i, center=False).mean()
                source["RSI"] = 100.0 * (df_up_sma_random / (df_up_sma_random + df_down_sma_random))
                source = source.loc[::-1]
                change3 =  []
                no_change3 = []
                for k in range(15,days):
                        #下降トレンドから上昇トレンドのとき
                        
                        sub1 = source['RSI'][2000-k] - source['RSI'][2000-k-1]
                        sub2 = source['RSI'][2000-k-1] - source['RSI'][2000-k-2]
                        sub3 = source['RSI'][2000-k-1+14]
                        if sub1>0 and sub2<0 and source['RSI'][2000-k-3] < 40:
                                for a in range(1,5):
                                        trend_change = source['sma01'][2000-k+a] - source['sma01'][2000-k-1+a]
                                        if trend_change > 0:
                                                change3.append(1)
                                                break
                                        else:
                                                no_change3.append(1)

                probability3 = len(change3) * 100 / (len(change3) + len(no_change3))
                probability3 = int(probability3)
                change5_probability.append(probability3)

        max = max(change5_probability)
        max_day5 = change5_probability.index(max)
        st.write('RSIが' + str(max_day5 + 1) + '日間のとき、確率が最大で' + str(max) + '%です')
