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
 
st.title('一目均衡表×RSI勝負銘柄')

codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6047','6055','6058','6062','6083','6070','6088','6101','6113','6136','6141','6208','6238','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6544','6556','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7072','7078','7187','7198','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7803','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8370','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9024','9007','9076','9099','9308','9401','9409','9416','9434','9502','9503','9511','9513','9517','9519','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','2975','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3134','3167','3161','3197','3222','3254','3319','3360','3377','3405','3407','3433','3436','3479','3482','3491','3591','3604','3632','3657','3661','3675','3681','3683','3691','3694','3902','3926','3962','3990','3997','4028','4042','4043','4045','4053','4054','4056','4057','4080','4088','4095','4204','4272','4331','4394','4395','4423']

day1_sanyaku = []
day1_kinkouhyou = []
day1_chikouspan = []
day2_sanyaku = []
day2_kinkouhyou = []
day2_chikouspan = []
day3_sanyaku = []
day3_kinkouhyou = []
day3_chikouspan = []




for code in codes:
    option = code
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
    

    # 基準線
    high26 = source["High"].rolling(window=26).max()
    low26 = source["Low"].rolling(window=26).min()
    source["base_line"] = (high26 + low26) / 2
    
    # 転換線
    high9 = source["High"].rolling(window=9).max()
    low9 = source["Low"].rolling(window=9).min()
    source["conversion_line"] = (high9 + low9) / 2
    
    # 先行スパン1
    leading_span1 = (source["base_line"] + source["conversion_line"]) / 2
    source["leading_span1"] = leading_span1.shift(25)
    
    # 先行スパン2
    high52 = source["High"].rolling(window=52).max()
    low52 = source["Low"].rolling(window=52).min()
    leading_span2 = (high52 + low52) / 2
    source["leading_span2"] = leading_span2.shift(25)
    
    # 遅行スパン
    source["lagging_span"] = source["Close"].shift(-25)

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

    #当日
    today=99
    yesterday=98

    price1 = source['Close'][today]
    price_lag1 = source['Close'][today-25]
    price_yesterday_lag1 = source['Close'][today-26]
    conversion_direction1 = source['conversion_line'][today] - source['conversion_line'][96]
    RSI_today1 = source['RSI'][today]
    lagging1 = source['lagging_span'][today-25]
    lagging_yesterday1 = source['lagging_span'][today-26]
    baseline_direction1 = source['base_line'][today] - source['base_line'][97]
    dif1 = source['conversion_line'][today] - source['base_line'][today]
    dif12 = source['conversion_line'][today-2] - source['base_line'][today-2]
    RSI_today1 = source['RSI'][today]

        

    #遅行スパンの好転
    if price_lag1<lagging1 and price_yesterday_lag1>lagging_yesterday1 and conversion_direction1>0 and dif12<dif1 and baseline_direction1>0 and RSI_today1>60:
        day1_chikouspan.append(code)
        for i in range(-5,0):
            conversion_line1 = source['conversion_line'][today+i]
            base_line1 = source['base_line'][today+i]
            conversion_line_yesterday1 = source['conversion_line'][yesterday+i]
            base_line_yesterday1 = source['base_line'][yesterday+i]
            price2 = source['Close'][today+i]
            conversion_direction1 = source['conversion_line'][today+i] - source['conversion_line'][96+i]
            RSI_today2 = source['RSI'][today+i]
        #均衡表の好転
        if conversion_line1>=base_line1 and conversion_line_yesterday1<base_line_yesterday1 and price2>conversion_line1 and conversion_direction1>0 and RSI_today2>60:
            day1_kinkouhyou.append(code)

    #前日
    today=98
    yesterday=97

    price1 = source['Close'][today]
    price_lag1 = source['Close'][today-25]
    price_yesterday_lag1 = source['Close'][today-26]
    conversion_direction1 = source['conversion_line'][today] - source['conversion_line'][96]
    RSI_today1 = source['RSI'][today]
    lagging1 = source['lagging_span'][today-25]
    lagging_yesterday1 = source['lagging_span'][today-26]
    baseline_direction1 = source['base_line'][today] - source['base_line'][97]
    dif1 = source['conversion_line'][today] - source['base_line'][today]
    dif12 = source['conversion_line'][today-2] - source['base_line'][today-2]
    RSI_today1 = source['RSI'][today]



    #遅行スパンの好転
    if price_lag1<lagging1 and price_yesterday_lag1>lagging_yesterday1 and conversion_direction1>0 and dif12<dif1 and baseline_direction1>0 and RSI_today1>60:
        day1_chikouspan.append(code)
        for i in range(-5,0):
            conversion_line1 = source['conversion_line'][today+i]
            base_line1 = source['base_line'][today+i]
            conversion_line_yesterday1 = source['conversion_line'][yesterday+i]
            base_line_yesterday1 = source['base_line'][yesterday]
            price2 = source['Close'][today+i]
            conversion_direction1 = source['conversion_line'][today] - source['conversion_line'][96]
            RSI_today2 = source['RSI'][today]
        #均衡表の好転
        if conversion_line1>=base_line1 and conversion_line_yesterday1<base_line_yesterday1 and price2>conversion_line1 and conversion_direction1>0 and RSI_today2>60:
            day2_kinkouhyou.append(code)

    #2日前
    today=97
    yesterday=96

    price1 = source['Close'][today]
    price_lag1 = source['Close'][today-25]
    price_yesterday_lag1 = source['Close'][today-26]
    conversion_direction1 = source['conversion_line'][today] - source['conversion_line'][96]
    RSI_today1 = source['RSI'][today]
    lagging1 = source['lagging_span'][today-25]
    lagging_yesterday1 = source['lagging_span'][today-26]
    baseline_direction1 = source['base_line'][today] - source['base_line'][97]
    dif1 = source['conversion_line'][today] - source['base_line'][today]
    dif12 = source['conversion_line'][today-2] - source['base_line'][today-2]
    RSI_today1 = source['RSI'][today]


        

    #遅行スパンの好転
    if price_lag1<lagging1 and price_yesterday_lag1>lagging_yesterday1 and conversion_direction1>0 and dif12<dif1 and baseline_direction1>0 and RSI_today1>60:
        day1_chikouspan.append(code)
        for i in range(-5,0):
            conversion_line1 = source['conversion_line'][today+i]
            base_line1 = source['base_line'][today+i]
            conversion_line_yesterday1 = source['conversion_line'][yesterday+i]
            base_line_yesterday1 = source['base_line'][yesterday]
            price2 = source['Close'][today+i]
            conversion_direction1 = source['conversion_line'][today] - source['conversion_line'][96]
            RSI_today2 = source['RSI'][today]
        #均衡表の好転
        if conversion_line1>=base_line1 and conversion_line_yesterday1<base_line_yesterday1 and price2>conversion_line1 and conversion_direction1>0 and RSI_today2>60:
            day3_kinkouhyou.append(code)


st.subheader('今日。遅行スパンの好転(5日前までに均衡表の好転)')
st.table(day1_kinkouhyou)
st.subheader('昨日。遅行スパンの好転(5日前までに均衡表の好転)')
st.table(day2_kinkouhyou)
st.subheader('2日前。遅行スパンの好転(5日前までに均衡表の好転)')
st.table(day3_kinkouhyou)






