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
 
st.title('ATRの計算')
option = st.text_input('銘柄コードを入力してください')

if option:
        ticker = str(option) + '.T'
        tkr = yf.Ticker(ticker)
        hist = tkr.history(period='100d')
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
        source['tr'] = tr
        source['ATR'] = tr.rolling(20).mean()

        atr15= 1.5*source['ATR'][99]
        atr20=2*source['ATR'][99]
        atr25=2.5*source['ATR'][99]
        atr30=3*source['ATR'][99]

        st.subheader('1.5ATR:'+str(atr15))
        st.subheader('2.0ATR:'+str(atr20))
        st.subheader('2.5ATR:'+str(atr25))
        st.subheader('3ATR:'+str(atr30))