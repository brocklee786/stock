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

days = st.selectbox(
    '何日間の取引を想定していますか？',
    (5,1, 3, 10))


DMI_percent_list = []
chance1_all = []
DMI_win = []
DMI_win_price = []
MACD_percent_list = []
chance2_all = []
MACD_win = []
MACD_win_price = []

MACD_DMI_percent_list = []
chance3_all = []
MACD_DMI_win = []
MACD_DMI_win_price = []

codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6047','6055','6058','6062','6083','6070','6088','6101','6113','6136','6141','6208','6238','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6544','6556','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7187','7198','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8370','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9024','9007','9076','9099','9308','9401','9409','9416','9434','9502','9503','9511','9513','9517','9519','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3134','3167','3161','3197','3222','3254','3319','3360','3377','3405','3407','3433','3436','3479','3482','3491','3591','3604','3632','3657','3661','3675','3681','3683','3691','3694','3902','3926','3962','3966','3990','3997','4028','4042','4043','4045','4080','4088','4095','4204','4272','4331','4394','4395','4423']
for code in codes:
        ticker = str(code) + '.T'
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
 
        # MACD計算
 
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp26 = source['Close'].ewm(span=26, adjust=False).mean()
        source['MACD'] = exp12 - exp26
 
        # シグナル計算
 
        source['Signal'] = source['MACD'].rolling(window=9).mean()
 
        # ヒストグラム(MACD - シグナル)
 
        source['Hist'] = source['MACD'] - source['Signal']


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



        #MACDの確率を計算
        MACD_buy = []
        MACD_Nobuy = []
        price_macd_win = []
        #MACDとシグナルがクロスしているかどうかを確認する。
        yesterday1 = source['MACD'][498] - source['Signal'][498]
        today1 = source['MACD'][499] - source['Signal'][499]
        #sub1 = source['Close'][i+days] - source['Close'][i]
        price_days_before1 = source['Close'][i+days]
        price_days_before2 = source['Close'][i+days-1]
        price_days_before3 = source['Close'][i+days-2]
        price_days_before4 = source['Close'][i+days-3]
        price_99 = source['Close'][i+1] * 0.97
        price_percent3 = source['Close'][i+1] * 0.03 * -1
        if yesterday1<0 and today1>0:
           MACD_buy.append(code)
        #st.table(MACD_buy)
        if len(MACD_buy):
            st.table(MACD_buy)    

