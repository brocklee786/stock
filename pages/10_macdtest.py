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
 
        source['Signal'] = source['MACD'].ewm(span=9, adjust=False).mean()
 
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

        #DMIの確率を計算
        DMI_buy = []
        DMI_Nobuy = []
        price_dmi_win = []
        for i in range(20,490):
                #pDIとmDIがクロスしているかどうかを確認する。
                yesterday = source['pDI'][i-1] - source['mDI'][i-1]
                today = source['pDI'][i] - source['mDI'][i]
                sub = source['Close'][i+days+1] - source['Close'][i+1]
                adx_check = source['ADX'][i] - source['ADX'][i-1]
                price_days_before1 = source['Close'][i+days]
                price_days_before2 = source['Close'][i+days-1]
                price_days_before3 = source['Close'][i+days-2]
                price_days_before4 = source['Close'][i+days-3]
                price_99 = source['Close'][i+1] * 0.97
                price_percent3 = source['Close'][i+1] * 0.03 * -1
                RSI = source['RSI'][i]
                if yesterday<0 and today>0 and adx_check>0 :
                
                        if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99 and sub>0:
                                DMI_buy.append(i)
                                price_dmi_win.append(sub)
                        
                        elif price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99 or sub<0:
                                DMI_Nobuy.append(i)
                                price_dmi_win.append(price_percent3)

        #DMIが当たる確率
        if len(DMI_buy):
                percent_dmi = (len(DMI_buy) * 100) / (len(DMI_buy) + len(DMI_Nobuy))
                chance1 = len(DMI_buy) + len(DMI_Nobuy)
                chance1_all.append(chance1)
                DMI_percent_list.append(percent_dmi)
                DMI_win.append(len(DMI_buy))
                DMI_win_price.append(sum(price_dmi_win))

        
          

        #MACDの確率を計算
        MACD_buy = []
        MACD_Nobuy = []
        price_macd_win = []
        for i in range(20,490):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
                sub1 = source['Close'][i+days] - source['Close'][i]
                price_days_before1 = source['Close'][i+days]
                price_days_before2 = source['Close'][i+days-1]
                price_days_before3 = source['Close'][i+days-2]
                price_days_before4 = source['Close'][i+days-3]
                price_99 = source['Close'][i+1] * 0.97
                price_percent3 = source['Close'][i+1] * 0.03 * -1
                RSI = source['RSI'][i]
                if yesterday1<0 and today1>0 and RSI<30:
                        if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99 and sub>0:
                                MACD_buy.append(i)
                                price_macd_win.append(sub1)
                        elif price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99 or sub<0:
                                MACD_Nobuy.append(i)
                                price_macd_win.append(price_percent3)
        #st.table(MACD_buy)
        if len(MACD_buy):
                percent_macd = (len(MACD_buy) * 100) / (len(MACD_buy) + len(MACD_Nobuy))
                chance2 = len(MACD_buy) + len(MACD_Nobuy)
                chance2_all.append(chance2)
                MACD_percent_list.append(percent_macd)
                MACD_win.append(len(MACD_buy))
                MACD_win_price.append(sum(price_macd_win))



        #組み合わせた場合の確率を計算
        MACD_buy_check = []
        for i in range(20,490):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
                
                if yesterday1<0 and today1>0:
                        MACD_buy_check.append(i)
                
        #st.table(MACD_buy)

        MACD_DMI_check = []
        MACD_DMI_up_price = []
        MACD_DMI_down_price = []
        MACD_DMI_buy = []
        MACD_DMI_Nobuy = []
        price_macd_dmi_win = []
        for num in MACD_buy_check:
                for k in range(0,3):
                        
                        yesterday2 = source['pDI'][(num)+k-1] - source['mDI'][(num)+k-1]
                        today2 = source['pDI'][(num)+k] - source['mDI'][(num)+k]
                        adx_check2 = source['ADX'][num+k] - source['ADX'][num+k-1]
                        price_dif = source['Close'][(num)+k+days+1] - source['Close'][(num)+k+1]
                        price_days_before1 = source['Close'][i+days+k]
                        price_days_before2 = source['Close'][i+days-1+k]
                        price_days_before3 = source['Close'][i+days-2+k]
                        price_days_before4 = source['Close'][i+days-3+k]
                        price_99 = source['Close'][i+k+1] * 0.97
                        price_percent3 = source['Close'][i+k+1] * 0.03 * -1
                        if yesterday2<0 and today2>0 and adx_check2>0:
                                if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99 and price_dif>0:
                                        MACD_DMI_buy.append(i)
                                        price_macd_dmi_win.append(price_dif)
                                        break
                                if price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99 or price_dif<0:
                                        MACD_DMI_Nobuy.append(i)
                                        price_macd_dmi_win.append(price_dif)
                                        break

                for k in range(-3,-1):
                        
                        yesterday2 = source['pDI'][(num)+k-1] - source['mDI'][(num)+k-1]
                        today2 = source['pDI'][(num)+k] - source['mDI'][(num)+k]
                        adx_check2 = source['ADX'][num+k] - source['ADX'][num+k-1]
                        price_dif = source['Close'][(num)+days+1] - source['Close'][(num)+1]
                        price_days_before1 = source['Close'][i+days]
                        price_days_before2 = source['Close'][i+days-1]
                        price_days_before3 = source['Close'][i+days-2]
                        price_days_before4 = source['Close'][i+days-3]
                        price_99 = source['Close'][i+1] * 0.97
                        price_percent3 = source['Close'][i+1] * 0.03 * -1
                        if yesterday2<0 and today2>0 and adx_check2>0:
                                if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99 and price_dif>0:
                                        MACD_DMI_buy.append(i)
                                        price_macd_dmi_win.append(price_dif)
                                        break
                                if price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99 or price_dif<0:
                                        MACD_DMI_Nobuy.append(i)
                                        price_macd_dmi_win.append(price_dif)
                                        break






        if len(MACD_DMI_buy):
                percent_macd_dmi = (len(MACD_DMI_buy) * 100) / (len(MACD_DMI_buy) + len(MACD_DMI_Nobuy))
                chance3 = len(MACD_DMI_buy) + len(MACD_DMI_Nobuy)
                chance3_all.append(chance3)
                MACD_DMI_percent_list.append(percent_macd_dmi)
                MACD_DMI_win.append(len(MACD_DMI_buy))
                MACD_DMI_win_price.append(sum(price_macd_dmi_win))


#DMI
probability1 = sum(DMI_percent_list) / len(DMI_percent_list)
win_probability = sum(DMI_win)*100 / sum(chance1_all)
win1 = sum(DMI_win_price) * 100
st.title('DMI')
st.subheader('確率の平均:' + str(probability1))
st.subheader('勝率は:' + str(win_probability))
st.subheader('起きた回数:' + str(sum(chance1_all)))
st.subheader('儲け:' + str(win1))

#MACD
probability2 = sum(MACD_percent_list) / len(MACD_percent_list)
win_probability2 = sum(MACD_win)*100 / sum(chance2_all)
win2 = sum(MACD_win_price) * 100
st.title('MACD')
st.subheader('確率の平均:' + str(probability2))
st.subheader('勝率は:' + str(win_probability2))
st.subheader('起きた回数:' + str(sum(chance2_all)))
st.subheader('儲け:' + str(win2))

#DMIとMACD組み合わせ
probability3 = sum(MACD_DMI_percent_list) / len(MACD_DMI_percent_list)
win_probability3 = sum(MACD_DMI_win) *100 / sum(chance3_all)
win3 = sum(MACD_DMI_win_price) * 100
st.title('組み合わせ')
st.subheader('確率の平均:' + str(probability3))
st.subheader('勝率は:' + str(win_probability3))
st.subheader('起きた回数:' + str(sum(chance3_all)))
st.subheader('儲け:' + str(win3))

st.table(MACD_win_price)
