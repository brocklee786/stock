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
 
st.title('一目均衡表×RSI検証')
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (5,1,3,10))


chance1_all = []
percent_list = []
win = []
win_price = []

chance2_all = []
percent_list2 = []
win2 = []
win_price2 = []

chance3_all = []
percent_list3 = []
win3 = []
win_price3 = []
day3 = []


codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6047','6055','6058','6062','6083','6070','6088','6101','6113','6136','6141','6208','6238','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6544','6556','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7187','7198','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8370','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9024','9007','9076','9099','9308','9401','9409','9416','9434','9502','9503','9511','9513','9517','9519','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3134','3167','3161','3197','3222','3254','3319','3360','3377','3405','3407','3433','3436','3479','3482','3491','3591','3604','3632','3657','3661','3675','3681','3683','3691','3694','3902','3926','3962','3966','3990','3997','4028','4042','4043','4045','4080','4088','4095','4204','4272','4331','4394','4395','4423']
for code in codes:
    option = code
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period='240d')
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

    #DMIの計算
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

    #大循環macd
    exp5 = source['Close'].ewm(span=5, adjust=False).mean()
    exp20 = source['Close'].ewm(span=20, adjust=False).mean()
    source['MACD1'] = exp5 - exp20


    exp40 = source['Close'].ewm(span=40, adjust=False).mean()
    source['MACD2'] = exp5 - exp40

    source['MACD3'] = exp20 - exp40

    KDAY = 26  # K算定用期間
    MDAY = 3  # D算定用期間

    # stochasticks K
    source["sct_k_price"] = (
        100*
        (source["Close"] - source["Close"].rolling(window=KDAY, min_periods=KDAY).min())/
        (source["Close"].rolling(window=KDAY, min_periods=KDAY).max() - source["Close"].rolling(window=KDAY, min_periods=KDAY).min())
    )

    # stochasticks D
    source["sct_d_price"] = (
        100*
        (source["Close"] - source["Close"].rolling(window=KDAY, min_periods=KDAY).min())
        .rolling(window=MDAY, min_periods=MDAY).sum()/
        (source["Close"].rolling(window=KDAY, min_periods=KDAY).max() - source["Close"].rolling(window=KDAY, min_periods=KDAY).min())
        .rolling(window=MDAY, min_periods=MDAY).sum()
    )

    # slow stochasticks
    source["slow_sct_d_price"] = source["sct_d_price"].rolling(window=MDAY, min_periods=MDAY).mean()


    check1_all = []
    check1_up = []
    check1_down = []
    price_dif1 = []
    price1_win = []
    
    for i in range(27,225):
        conversion_line = source['conversion_line'][i]
        conversion_line_yesterday = source['conversion_line'][i-1]
        base_line = source['base_line'][i]
        base_line_yesterday = source['base_line'][i-1]
        price = source['Close'][i]
        price_buy = source['Close'][i+1]
        price_days = source['Low'][i+days+1]
        price_days_before1 = source['Low'][i+days]
        price_days_before2 = source['Low'][i+days-1]
        price_days_before3 = source['Low'][i+days-2]
        price_days_before4 = source['Low'][i+days-3]
        price_change = price_days - price_buy
        price_26before = source['Close'][i-26]
        price_9before = source['Close'][i-9]
        conversion_direction = source['conversion_line'][i] - source['conversion_line'][i-3]
        baseline_direction = source['base_line'][i+1] - source['base_line'][i]
        RSI_today = source['RSI'][i]
        price_buy_percent3 = source['Close'][i+1] * 0.03 * -1
        price_99 = source['Close'][i+1] * 0.97
        adx_direction = source['ADX'][i] - source['ADX'][i-1]
        RSI_direction = source['RSI'][i] - source['RSI'][i-1]
        pdm = source['pDI'][i]
        mdm = source['mDI'][i] + 25
        #均衡表の好転
        if conversion_line>=base_line and conversion_line_yesterday<base_line_yesterday and price>conversion_line and conversion_direction>0 and pdm>mdm and adx_direction>0 and RSI_direction>0 and RSI_today>60:
            check1_all.append(i)

            
            if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_days>price_99:
                check1_up.append(i)
               # price_dif1.append(price_change)
                price1_win.append(price_change)

            else:
                check1_down.append(i)
                price1_win.append(price_buy_percent3)
                    
         
    check2_all = []
    check2_up = []
    check2_down = []
    price_dif2 = []
    price2_win = []
    
        
    if len(check1_up):
            percent1 = (len(check1_up)* 100) / (len(check1_up)+ len(check1_down)))
            chance1 = len(check1_up) + len(check1_down)
            chance1_all.append(chance1)
            percent_list.append(percent1)
            win.append(len(check1_up))
            win_price.append(sum(price1_win))

    #大循環MACD
    for i in range(27,225):
        macd1 = source['MACD1'][i]
        macd1_direction = source['MACD1'][i] - source['MACD1'][i-3]
        macd2 = source['MACD2'][i]
        macd2_direction = source['MACD2'][i] - source['MACD2'][i-3]
        macd3 = source['MACD3'][i]
        macd3_yesterday = source['MACD3'][i-1]
        macd3_direction = source['MACD3'][i] - source['MACD3'][i-3]
        price = source['Close'][i]
        price_buy = source['Close'][i+1]
        price_days = source['Low'][i+days+1]
        price_days_before1 = source['Low'][i+days]
        price_days_before2 = source['Low'][i+days-1]
        price_days_before3 = source['Low'][i+days-2]
        price_days_before4 = source['Low'][i+days-3]
        price_buy_percent3 = source['Close'][i+1] * 0.03 * -1
        price_99 = source['Close'][i+1] * 0.97
        price_change = price_days - price_buy
        adx_direction = source['ADX'][i] - source['ADX'][i-1]

        if macd1>0 and macd2>0 and macd3>0 and macd3_yesterday<0 and macd1_direction>0 and macd2_direction>0 and adx_direction>0:

            if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_days>price_99:
                check2_up.append(i)
               # price_dif1.append(price_change)
                price2_win.append(price_change)

            else:
                check2_down.append(i)
                price2_win.append(price_buy_percent3)

    if len(check2_up):
            percent2 = (len(check2_up)* 100) / (len(check2_up)+ len(check2_down)))
            chance2 = len(check2_up) + len(check2_down)
            chance2_all.append(chance2)
            percent_list2.append(percent2)
            win2.append(len(check2_up))
            win_price2.append(sum(price2_win))

            
    check3_all = []
    check3_up = []
    check3_down = []
    price_dif3 = []
    price3_win = []

    for i in range(27,225):
        percentk = source['sct_k_price'][i]
        percentk_direction = source['sct_k_price'][i] - source['sct_k_price'][i-1]
        slow_percentd = source['slow_sct_d_price'][i]
        slow_percentd_yesterday = source['slow_sct_d_price'][i-1]
        price = source['Close'][i]
        price_buy = source['Close'][i+1]
        price_days = source['Close'][i+days+1]
        price_days_before1 = source['Low'][i+days]
        price_days_before2 = source['Low'][i+days-1]
        price_days_before3 = source['Low'][i+days-2]
        price_days_before4 = source['Low'][i+days-3]
        price_buy_percent3 = source['Close'][i+1] * 0.03 * -1
        price_99 = source['Close'][i+1] * 0.97
        price_change = price_days - price_buy
        adx_direction = source['ADX'][i] - source['ADX'][i-1]

        if slow_percentd_yesterday<20 and slow_percentd>20 and percentk_direction>0 and percentk>70:
            check3_all.append(i)
            

            
            if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_days>price_buy:
                check3_up.append(i)
               # price_dif1.append(price_change)
                price3_win.append(price_change)

            else:
                check3_down.append(i)
                price3_win.append(price_buy_percent3)

        
    if len(check3_up):
        percent3 = (len(check3_up)* 100) / (len(check3_up)+ len(check3_down)))
        chance3 = len(check3_up) + len(check3_down)
        chance3_all.append(len(check3_all))
        percent_list3.append(percent3)
        win3.append(len(check3_up))
        win_price3.append(sum(price3_win))
            
            






probability1 = sum(percent_list) / len(percent_list)
win_probability1 = sum(win) *100 / sum(chance1_all)
win1 = sum(win_price) * 100
st.title('均衡表の好転')
st.subheader('確率の平均:' + str(probability1))
st.subheader('勝率は:' + str(win_probability1))
st.subheader('起きた回数:' + str(sum(chance1_all)))
st.subheader('儲け:' + str(win1))

probability2 = sum(percent_list2) / len(percent_list2)
win_probability2 = sum(win2) *100 / sum(chance2_all)
win2_1 = sum(win_price2) * 100
st.title('大循環MACD')
st.subheader('確率の平均:' + str(probability2))
st.subheader('勝率は:' + str(win_probability2))
st.subheader('起きた回数:' + str(sum(chance2_all)))
st.subheader('儲け:' + str(win2_1))

probability3 = sum(percent_list3) / len(percent_list3)
win_probability3 = sum(win3) *100 / sum(chance3_all)
win3_1 = sum(win_price3) * 100
st.title('ストキャスティクス')
st.subheader('確率の平均:' + str(probability3))
st.subheader('勝率は:' + str(win_probability3))
st.subheader('起きた回数:' + str(sum(chance3_all)))
st.subheader('儲け:' + str(win3_1))

