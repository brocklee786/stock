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

def RCI(x):
    n = len(x)
    d = ((np.arange(1,n+1)-np.array(pd.Series(x).rank()))**2).sum()
    rci = 1-6*d/(n*(n**2-1))
    return rci*100


st.set_page_config(layout="wide")
 
st.title('移動平均線、ボリンジャーバンド、RCI組み合わせ')
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (1,3,5, 10))
option = st.text_input('銘柄コードを入力してください')
if option:
        ticker = str(option) + '.T'
        tkr = yf.Ticker(ticker)
        hist = tkr.history(period='1000d')
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
        span01=5
        span02=25
        span03=50
 
        source['sma01'] = price.rolling(window=span01).mean()
        source['sma02'] = price.rolling(window=span02).mean()
        source['sma03'] = price.rolling(window=span03).mean()

        #ボリンジャーバンド
        # 標準偏差
        source["std"] = source["sma02"].rolling(window=25).std()
        
        # ボリンジャーバンド
        source["2upper"] = source["sma02"] + (2 * source["std"])
        source["2lower"] = source["sma02"] - (2 * source["std"])
        source["3upper"] = source["sma02"] + (3 * source["std"])
        source["3lower"] = source["sma02"] - (3 * source["std"])

        
        #RCI
        source['RCI_short'] = source["Close"].rolling(9).apply(RCI)
        source['RCI_long'] = source["Close"].rolling(14).apply(RCI)
        
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

        up = []
        all = []
        for i in range(50,950):
            price_dif = source['Close'][i+days] - source['Close'][i]
            rci_short = source['RCI_short'][i]
            rci_long = source['RCI_long'][i]
            bollinger_day = source['2upper'][i-2]
            bollinger_yesterday = source['2upper'][i-1]
            bollinger_today = source['3lower'][i]
            bollinger_direction = bollinger_today - bollinger_yesterday
            price_today = source['Close'][i]
            price_yesterday = source['High'][i-1]
            price_day = source['High'][i-2]
            price_direction = source['sma01'][i] - source['sma01'][i-1]
            price_direction2 = source['sma02'][i] - source['sma02'][i-1]
            price_direction3 = source['sma03'][i] - source['sma03'][i-1]
            RSI_today = source['RSI'][i]
            #if rci_short>90 and rci_long>90 and bollinger_direction>0 and price_today>bollinger_today and price_yesterday>bollinger_yesterday and price_day>bollinger_day and price_direction>0 and price_direction2>0 and price_direction3>0 and price_direction>price_direction2>price_direction3:
                #all.append(i)
                #if price_dif>0:
                    #up.append(i)
                    
            if rci_short<-80 and rci_long<-80 and RSI_today<30 and price_today<bollinger_today:
                all.append(i)
                if price_dif>0:
                    up.append(i)

        
        percent = len(up)*100 / len(all)

        st.subheader('確率は' + str(percent) + '%')

        expander1 = st.expander('条件')
        expander1.write('終値が+2シグマを超えている。RCIの値が70%以上。ボリンジャーバンドが拡大している。移動平均線が上向き。')
            




