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
import time
from math import nan
 
#データフレームを画像に変換
def TablePlot(df,outputPath,w,h):
    fig, ax = plt.subplots(figsize=(w,h))
    ax.axis('off')
    ax.table(cellText=df.values,
            colLabels=df.columns,
            loc='center')
    plt.savefig(outputPath)
 
#画像とメッセージをLINEに送信
def main_gazo1():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = '逆張り'
    payload = {"message" :  message}
    files = {"imageFile":open('./table1.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
 
def main_gazo2():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = '順張り'
    payload = {"message" :  message}
    files = {"imageFile":open('./table2.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
 
def main_gazo3():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = 'DMI'
    payload = {"message" :  message}
    files = {"imageFile":open('./table3.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
 
def main_gazo4():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = 'MACD'
    payload = {"message" :  message}
    files = {"imageFile":open('./table4.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
   
st.set_page_config(layout="wide")
 
st.title('LINEに通知')
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (1,3, 5, 10))
codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6047','6055','6058','6062','6083','6070','6088','6101','6113','6136','6141','6208','6238','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6544','6556','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7072','7078','7187','7198','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7803','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8370','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9024','9007','9076','9099','9308','9401','9409','9416','9434','9502','9503','9511','9513','9517','9519','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','2975','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3134','3167','3161','3197','3222','3254','3319','3360','3377','3405','3407','3433','3436','3479','3482','3491','3591','3604','3632','3657','3661','3675','3681','3683','3691','3694','3902','3926','3962','3966','3990','3997','4028','4042','4043','4045','4053','4054','4056','4057','4080','4088','4095','4204','4272','4331','4394','4395','4423']
 
useful_code = []
percent_50 = []
st.subheader('RSIによる分析')
#リストに入っているすべてのコードでRSIが一番高い際の値とそのRSIの日数を計算
if st.button('LINEに通知する1'):
    st.write('calculating...')
     
    for code in codes:
           
            ticker = str(code) + '.T'
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
            #移動平均
            span01=5
            span02=25
            span03=50
   
            source['sma01'] = price.rolling(window=span01).mean()
            source['sma02'] = price.rolling(window=span02).mean()
            source['sma03'] = price.rolling(window=span03).mean()
   
            change3_probability = []
            probability_50  = []
            #フィッティングした際にRSIが一番高くなるものを算出
            for i in range(1,20):
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
                    df_up_sma_random = df_up.rolling(window=i, center=False).mean()
                    df_down_sma_random = df_down.rolling(window=i, center=False).mean()
                    source["RSI"] = 100.0 * (df_up_sma_random / (df_up_sma_random + df_down_sma_random))
               
                    change3 =  []
                    no_change3 = []
               
                    for k in range(20,490):
                            #下降トレンドから上昇トレンドのとき
                           
                            sub1 = source['RSI'][500-k] - source['RSI'][500-k-1]
                            sub2 = source['RSI'][500-k-1] - source['RSI'][500-k-2]
                            #sub3 = source['RSI'][500-k-1+14]
                           
                            if sub1>0 and sub2<0 and source['RSI'][500-k-3] < 40:
                                    for a in range(1,5):
                                            trend_change = source['sma01'][500-k+a] - source['sma01'][500-k-1+a]
                                            if trend_change > 0:
                                                    change3.append(1)
                                                    break
                                            else:
                                                    no_change3.append(1)
   
                    probability3 = len(change3) * 100 / (len(change3) + len(no_change3))
                    probability3 = int(probability3)
                    change3_probability.append(probability3)
   
                    percent50_raise = []
                    percent50_unraise = []
                    #50%を超えたときに上昇が続いているか(順張り)
                    for j in range(20,500):
                            raise_continue = source['sma01'][500-j+days] - source['sma01'][500-j-1]
                            if source['RSI'][500-j-1] > 50 and source['RSI'][500-j-2] < 50:
                                    if raise_continue > 0:
                                            percent50_raise.append(1)
                                    else:
                                            percent50_unraise.append(1)
   
                    percent50_probability = len(percent50_raise) * 100 / (len(percent50_raise) + len(percent50_unraise))
                    percent50_probability = int(percent50_probability)
                    probability_50.append(percent50_probability)
   
            max_num = max(change3_probability)
            max_day = change3_probability.index(max_num) + 1
            max_num2 = max(probability_50)
            max_day2 = probability_50.index(max_num2) + 1
       
   
       
            if max_num > 50 and source['RSI'][499] < 40:
                    useful_code.append({
                    'Company Code':code,
                    'Maximum Percent':max_num,
                    'RSI Days':max_day,
                    'RSI Now':source['RSI'][499],
                    'Price':source['Close'][499]})
   
            if max_num2 > 70 and 45 < source['RSI'][499] < 50 and source['sma01'][499] - source['sma01'][498] > 0:
                    percent_50.append({'Company Code':code,'Maximum Percent':max_num2,'RSI Days':max_day2,'RSI Now':source['RSI'][499],'Price':source['Close'][499]})
 
     
 
 
    useful_code = pd.DataFrame(useful_code)
    TablePlot(useful_code,'table1.png',10,10)
    percent_50 = pd.DataFrame(percent_50)
    TablePlot(percent_50,'table2.png',10,10)
 
    main_gazo1()
    main_gazo2()
    st.subheader('逆張り')
    st.table(useful_code)
    st.subheader('順張り')
    st.table(percent_50)
    st.balloons()
    st.balloons()
expander1 = st.sidebar.expander('逆張り')
expander1.write('RSIが30%以下で反転した際に 5日以内に移動平均線が転換している確率が50%より大きい&現在のRSIが30%未満')
expander1 = st.sidebar.expander('順張り')
expander1.write('現在のRSIが45%~50%&その確率が80%よりも大きい')
 
MACD_buy2 = []
DMI_buy2 = []
#MACDとDMIによる通知
st.subheader('DMIとMACDによる分析')
if st.button('LINEに通知する2'):
    for code in codes:
        ticker = str(code) + '.T'
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
        for i in range(20,489):
                #pDIとmDIがクロスしているかどうかを確認する。
                yesterday = source['pDI'][i-1] - source['mDI'][i-1]
                today = source['pDI'][i] - source['mDI'][i]
                sub = source['Close'][i+days] - source['Close'][i]
                adx_check = source['ADX'][i] - source['ADX'][i-1]
                if yesterday<0 and today>0 and sub > 0 and adx_check>0:
                        DMI_buy.append(i)
                elif yesterday<0 and today>0 and sub<0 and adx_check>0:
                        DMI_Nobuy.append(i)
 
       
       
        DMI_buy = pd.DataFrame(DMI_buy)
        correct_DMI = []
       
        MACD_buy = []
        MACD_Nobuy = []
        for i in range(20,489):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
                sub1 = source['Close'][i+days] - source['Close'][i]
                if yesterday1<0 and today1>0 and sub1>0:
                        MACD_buy.append(i)
                if yesterday1<0 and today1>0 and sub1<0:
                        MACD_Nobuy.append(i)
       
       
 
        MACD_buy_check = []
        for i in range(20,489):
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
        if len(DMI_buy)>0:
            DMI_possibility = int(len(DMI_buy) * 100 / (len(DMI_buy) + len(DMI_Nobuy)))
        if len(MACD_buy)>0:
            MACD_possibility = int(len(MACD_buy) * 100 / (len(MACD_buy) + len(MACD_Nobuy)))
        #colab_possibility = int(len(buy) * 100 / len(MACD_DMI_check))
 
       
        MACD_today = source['MACD'][499] - source['Signal'][499]
        MACD_yesterday = source['MACD'][498] - source['MACD'][498]
        dif = MACD_today - MACD_yesterday
        if -5<MACD_today<0 and dif<0 and MACD_possibility>60:
                    MACD_buy2.append({'Company Code':code,'Maximum Percent':MACD_possibility,'Price':source['Close'][499]})
       
        DMI_today = source['pDI'][499] - source['mDI'][499]
        DMI_yesterday = source['pDI'][498] - source['mDI'][498]
        adx_trend = source['ADX'][499] - source['ADX'][498]
        dif2 = DMI_today - DMI_yesterday
        if -5<DMI_today<0 and dif2<0 and adx_trend>0 and DMI_possibility>60:
                    DMI_buy2.append({'Company Code':code,'Maximum Percent':DMI_possibility,'Price':source['Close'][499]})
    if len(DMI_buy2)>0
        DMI_buy2 = pd.DataFrame(DMI_buy2)
        TablePlot(DMI_buy2,'table3.png',10,10)
        main_gazo3()
        st.subheader('DMI')
        st.table(DMI_buy2)
        
    if len(MACD_buy2)>0:
        MACD_buy2 = pd.DataFrame(MACD_buy2)
        TablePlot(MACD_buy2,'table4.png',10,10)
        main_gazo4()
        st.subheader('MACD')
        st.table(MACD_buy2)
        
    st.balloons()
    st.balloons()
    
    
    
    
