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

st.set_page_config(layout="wide")
 
st.title('MACDとDMI分析')
option = st.text_input('銘柄コードを入力してください')
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (1, 3, 5, 10))
if option:
        ticker = str(option) + '.T'
        tkr = yf.Ticker(ticker)
        hist = tkr.history(period='500d')
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
 
        # MACD計算
 
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp26 = source['Close'].ewm(span=26, adjust=False).mean()
        source['MACD'] = exp12 - exp26
 
        # シグナル計算
 
        source['Signal'] = source['MACD'].rolling(window=9).mean()
 
        # ヒストグラム(MACD - シグナル)
 
        source['Hist'] = source['MACD'] - source['Signal']
 
        #DMIの計算
        # DMIの計算
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
        source['pDI'] = pDM.rolling(14).sum()/tr.rolling(14).sum() * 100
        source['mDI'] = mDM.rolling(14).sum()/tr.rolling(14).sum() * 100
        # ADXの計算
        DX = (source['pDI']-source['mDI']).abs()/(source['pDI']+source['mDI']) * 100
        DX = DX.fillna(0)
        source['ADX'] = DX.rolling(14).mean()
        
        DMI_buy = []
        DMI_Nobuy = []
        for i in range(20,490):
                #pDIとmDIがクロスしているかどうかを確認する。
                yesterday = source['pDI'][i-1] - source['mDI'][i-1]
                today = source['pDI'][i] - source['mDI'][i]
                sub = source['Close'][i+days] - source['Close'][i]
                adx_check = source['ADX'][i] - source['ADX'][i-1]
                if yesterday<0 and today>0 and sub > 0 and adx_check>0:
                        DMI_buy.append(i)
                elif yesterday<0 and today>0 and sub<0 and adx_check>0:
                        DMI_Nobuy.append(i)
        for i in range(0,499):
                source['DMI_buy'] = nan
        for num in DMI_buy:
                source['DMI_buy'][num] = source['Close'][num]

        for i in range(0,499):
                source['DMI_Nobuy'] = nan
        for num in DMI_Nobuy:
                source['DMI_Nobuy'][num] = source['Close'][num]

        
        
        DMI_buy = pd.DataFrame(DMI_buy)
        correct_DMI = []
        
        MACD_buy = []
        MACD_Nobuy = []
        for i in range(20,490):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
                sub1 = source['Close'][i+days] - source['Close'][i]
                if yesterday1<0 and today1>0 and sub1>0:
                        MACD_buy.append(i)
                if yesterday1<0 and today1>0 and sub1<0:
                        MACD_Nobuy.append(i)
        #st.table(MACD_buy)
        for i in range(0,499):
                source['MACD_buy'] = nan
        for num in MACD_buy:
                source['MACD_buy'][num] = source['Close'][num]

        for i in range(0,499):
                source['MACD_Nobuy'] = nan
        for num in MACD_Nobuy:
                source['MACD_Nobuy'][num] = source['Close'][num]
        
        

        MACD_buy_check = []
        for i in range(20,490):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
                
                if yesterday1<0 and today1>0:
                        MACD_buy_check.append(i)
                
        #st.table(MACD_buy)

        MACD_DMI_check = []
        for num in MACD_buy_check:
                for k in range(-3,3):
                        
                        yesterday2 = source['pDI'][(num)+k-1] - source['mDI'][(num)+k-1]
                        today2 = source['pDI'][(num)+k] - source['mDI'][(num)+k]
                        adx_check2 = source['ADX'][num+k] - source['ADX'][num+k-1]
                        if yesterday2<0 and today2>0 and adx_check2>0:
                                MACD_DMI_check.append(num)
                                break

        buy = []
        for num in MACD_DMI_check:
                sub2 = source['Close'][num+days] - source['Close'][num]
                if sub2 > 0:
                        buy.append({'Number':num,'Date':source['Date'][num],'Price':source['Close'][num]})

        #st.table(buy)
        
        #st.table(correct)

        #それぞれの正答率を求める
        piece = len(DMI_buy) + len(DMI_Nobuy)
        DMI_possibility = int(len(DMI_buy) * 100 / (len(DMI_buy) + len(DMI_Nobuy)))
        MACD_possibility = int(len(MACD_buy) * 100 / (len(MACD_buy) + len(MACD_Nobuy)))
        colab_possibility = int(len(buy) * 100 / len(MACD_DMI_check))
        
        
        # open_close_color = alt.condition("datum.Open <= datum.Close",
        #                              alt.value("#06982d"),
        #                              alt.value("#ae1325"))
        # MACD_color = alt.value('#fdc086')
        # base = alt.Chart(source).encode(
        # alt.X('Date:T',
        #       axis=alt.Axis(
        #       format='%y/%m/%d',
        #       labelAngle=-45,
        #       title='Date'
        #       )
        # ),
        # color=open_close_color).properties(height=600)

        # rule = base.mark_rule().encode(
        #         alt.Y(
        #         'Low:Q',
        #         title='Price',
        #         scale=alt.Scale(zero=False),
        #         ),
        #         alt.Y2('High:Q')
        #         ).interactive().properties(height=600)

        # bar = base.mark_bar().encode(
        # alt.Y('Open:Q'),
        # alt.Y2('Close:Q')
        #         ).interactive().properties(height=600)

        # DMI_plot = base.mark_circle(size=300).encode(
        # alt.Y('DMI_buy'),
        # color=MACD_color
        
        #         ).interactive().properties(height=600)

        

        # st.altair_chart(rule + bar + DMI_plot, use_container_width=True)

        

        # plot = alt.Chart(source).mark_line().encode(
        # alt.X('Date:T',
        #       axis=alt.Axis(
        #       format='%y/%m/%d',
        #       labelAngle=-45,
        #       title='Date'
        #       )
        # ),
        # alt.Y(
        #         'Close:Q',
        #         title='Price',
        #         scale=alt.Scale(zero=False),
        #         )
        
        #         ).interactive().properties(height=600)
        
        
       

        # st.altair_chart(plot, use_container_width=True)

        st.subheader('DMIの正答率は' + str(DMI_possibility) + '%')
        if st.button('DMI正答率のグラフを表示する'):
                figure1, ax = plt.subplots()
                plt.rcParams["figure.figsize"] = (10, 4)
                plt.plot(source['Date'], source['Close'],label='Close')
                plt.scatter(source['Date'],source['DMI_buy'],color='r',label='DMI_buy')
                plt.scatter(source['Date'],source['DMI_Nobuy'],color='g',label='DMI_Nobuy')
                plt.xlabel("DATE")
                plt.ylabel("PRICE")
                plt.title('DMI')
                ax.legend()
                st.pyplot(figure1)
        

        st.subheader('MACDの正答率は' + str(MACD_possibility) + '%')
        if st.button('MACD正答率のグラフを表示する'):
                figure2, ax = plt.subplots()
                plt.rcParams["figure.figsize"] = (10, 4)
                plt.plot(source['Date'], source['Close'],label='Close')
                plt.scatter(source['Date'],source['MACD_buy'],color='r',label='MACD_buy')
                plt.scatter(source['Date'],source['MACD_Nobuy'],color='g',label='MACD_Nobuy')
                plt.xlabel("DATE")
                plt.ylabel("PRICE")
                plt.title('MACD')
                ax.legend()
                st.pyplot(figure2)

        
        st.subheader('DMIとMACDの組み合わせの正答率は' + str(colab_possibility) + '%')
