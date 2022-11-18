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

percent_step1 = []
price_step1 = []
steps1 = []
price1_win = []
check1_all_sum = []
check1_up_sum = []
percent_step2 = []
price_step2 = []
price2_win = []
steps2 = []
check2_all_sum = []
check2_up_sum = []
percent_step3 = []
price_step3 = []
price3_win = []
steps3 = []
check3_all_sum = []
check3_up_sum = []

codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6047','6055','6058','6062','6083','6070','6088','6101','6113','6136','6141','6208','6238','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6544','6556','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7187','7198','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8370','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9024','9007','9076','9099','9308','9401','9409','9416','9434','9502','9503','9511','9513','9517','9519','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3134','3167','3161','3197','3222','3254','3319','3360','3377','3405','3407','3433','3436','3479','3482','3491','3591','3604','3632','3657','3661','3675','3681','3683','3691','3694','3902','3926','3962','3966','3990','3997','4028','4042','4043','4045','4080','4088','4095','4204','4272','4331','4394','4395','4423']
for code in codes:
    option = code
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
    check1_all = []
    check1_up = []
    price_dif1 = []
    
    for i in range(27,485):
        conversion_line = source['conversion_line'][i]
        conversion_line_yesterday = source['conversion_line'][i-1]
        base_line = source['base_line'][i]
        base_line_yesterday = source['base_line'][i-1]
        price = source['Close'][i]
        price_buy = source['Close'][i+1]
        price_days = source['Close'][i+days+1]
        price_days_before1 = source['Close'][i+days]
        price_days_before2 = source['Close'][i+days-1]
        price_days_before3 = source['Close'][i+days-2]
        price_days_before4 = source['Close'][i+days-3]
        price_change = price_days - price_buy
        price_26before = source['Close'][i-26]
        price_9before = source['Close'][i-9]
        conversion_direction = source['conversion_line'][i] - source['conversion_line'][i-3]
        baseline_direction = source['base_line'][i+1] - source['base_line'][i]
        RSI_today = source['RSI'][i]
        price_buy_percent3 = source['Close'][i+1] * 0.01 * -1
        price_99 = source['Close'][i+1] * 0.99
        #均衡表の好転
        if conversion_line>=base_line and conversion_line_yesterday<base_line_yesterday and price>conversion_line and conversion_direction>0 and RSI_today>60:
            check1_all.append(i)
            steps1.append(1)
            if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_change>price_buy_percent3:
                check1_up.append(i)
                price_dif1.append(price_change)
                price1_win.append(price_change)

            elif price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99  or price_change<price_buy_percent3:
                price1_win.append(price_buy_percent3)
                    
         

    
    


    if len(check1_up)>0:
        percent1 = len(check1_up)*100 / len(check1_all)
        length = len(check1_up)
        percent_step1.append(percent1)
        int_price1 = int(sum(price_dif1)/len(price_dif1))
        price_step1.append(int_price1)
        check1_all_sum.append(len(check1_all))
        check1_up_sum.append(len(check1_up_sum))


    check2_all=[]
    check2_up = []
    price_dif2 = []
    #遅行スパンが価格を上抜け
    for i in check1_all:
        for k in range(0,5):
            a = i+k-25
            b= i+k
            price_today = source['Close'][i]
            price_buy = source['Close'][i+1+k]
            price_buy_percent3 = source['Close'][i+1+k] * 0.01 * -1
            price = source['Close'][a]
            price_yesterday = source['Close'][a-1]
            price_days = source['Close'][i+days+k+1]
            price_change = price_days-price_buy
            lagging = source['lagging_span'][a]
            lagging_yesterday = source['lagging_span'][a-1]
            conversion_direction = source['conversion_line'][i+k] - source['conversion_line'][i]
            baseline_direction = source['base_line'][a+1] - source['base_line'][i]
            dif = source['conversion_line'][i] - source['base_line'][i]
            dif2 = source['conversion_line'][i-2] - source['base_line'][i-2]
            RSI_today = source['RSI'][i]
            price_days_before1 = source['Close'][b+days]
            price_days_before2 = source['Close'][b+days-1]
            price_days_before3 = source['Close'][b+days-2]
            price_days_before4 = source['Close'][b+days-3]
            price_99 = source['Close'][b+1] * 0.99
            if price<lagging and price_yesterday>lagging_yesterday and conversion_direction>0 and dif2<dif and baseline_direction>0 and RSI_today>60:
                check2_all.append(i)
                steps2.append(1)
                if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_change>price_buy_percent3:
                    check2_up.append(i)
                    price_dif2.append(price_change)
                    price2_win.append(price_change)
                    break
                elif price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99  or price_change<price_buy_percent3:
                    price2_win.append(price_buy_percent3)
                    break
               
                    

    if len(check2_up)>0:
        percent2 = len(check2_up)*100 / len(check2_all)

        length2 = len(check2_up)
        percent_step2.append(percent2)
        int_price2 = int(sum(price_dif2)/len(price_dif2))
        price_step2.append(int_price2)
        check2_all_sum.append(len(check2_all))
        check2_up_sum.append(len(check2_up_sum))

    check3_all = []
    check3_up = []
    price_dif3 = []
    for i in check2_all:
        for k in range(0,5):
            a = i+k
            price_today = source['Close'][i]
            price = source['Close'][a]
            price_buy = source['Close'][a+1]
            price_yesterday = source['Close'][a-1]
            price_days = source['Close'][a+days+1]
            price_change = price_days - price_buy
            lagging = source['lagging_span'][a]
            lagging_yesterday = source['lagging_span'][a-1]
            conversion_direction = source['conversion_line'][a+1] - source['conversion_line'][i]
            baseline_direction = source['base_line'][a+1] - source['base_line'][i]
            dif = source['conversion_line'][i] - source['base_line'][i]
            dif2 = source['conversion_line'][i-2] - source['base_line'][i-2]
            price_days_before1 = source['Close'][a+days]
            price_days_before2 = source['Close'][a+days-1]
            price_days_before3 = source['Close'][a+days-2]
            price_days_before4 = source['Close'][a+days-3]
            price_99 = source['Close'][b+1] * 0.99
            price_buy_percent3 = source['Close'][i+1+k] * 0.01 * -1
            if source['leading_span1'][a]>source['leading_span2'][a]:
                yesterday = source['Close'][a-1] - source['leading_span1'][a-1]
                today = source['Close'][a] - source['leading_span1'][a]
                if yesterday<0 and today>0 and conversion_direction>0 and dif2<dif and baseline_direction>0:
                    check3_all.append(i)
                    steps3.append(1)
                    price3_win.append(price_change)
                    if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_change>price_buy_percent3:
                        check3_up.append(i)
                        price_dif3.append(price_change)
                        price3_win.append(price_change)
                        break
                    elif price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99  or price_change<price_buy_percent3:
                        price3_win.append(price_buy_percent3)
                        break
            else:
                yesterday = source['Close'][a-1] - source['leading_span2'][a-1]
                today = source['Close'][a] - source['leading_span2'][a]
                if yesterday<0 and today>0 and conversion_line>0 and dif2<dif and baseline_direction>0:
                    check3_all.append(i)
                    steps3.append(1)
                    if price_days_before1>price_99 and price_days_before2>price_99 and price_days_before3>price_99 and price_days_before4>price_99  and price_change>price_buy_percent3:
                        check3_up.append(i)
                        price_dif3.append(price_change)
                        break
                    elif price_days_before1<price_99 or price_days_before2<price_99 or price_days_before3<price_99 or price_days_before4<price_99  or price_change<price_buy_percent3:
                        price3_win.append(price_buy_percent3)
                        break
    if len(check3_up)>0:
        percent3 = len(check3_up)*100 / len(check3_all)
        length3 = len(check3_all)
        percent_step3.append(percent3)
        int_price3 = int(sum(price_dif3)/len(price_dif3))
        price_step3.append(int_price3)
        check3_all_sum.append(len(check3_all))
        check3_up_sum.append(len(check3_up_sum))

   
step1 = sum(percent_step1)/len(percent_step1)
step2 = sum(percent_step2)/len(percent_step2)
step3 = sum(percent_step3)/len(percent_step3)
price1 = sum(price_step1)/len(price_step1)
price2 = sum(price_step2)/len(price_step2)
price3 = sum(price_step3)/len(price_step3)
win1 = sum(price1_win) * 100
win2 = sum(price2_win) * 100
win3 = sum(price3_win) * 100
win_percent1 = sum(check1_up_sum) / sum(check1_all_sum)
win_percent2 = sum(check2_up_sum) / sum(check2_all_sum)
win_percent3 = sum(check3_up_sum) / sum(check3_all_sum)

#勝率の平均
st.subheader('均衡表の好転が起きたときに上がる確率の平均は'+ str(step1) + '%')
st.subheader('均衡表の好転が起きたときの勝率は'+ str(win_percent1) + '%')
st.subheader('上がり幅の平均は' + str(price1) + '円')
st.subheader('起きた回数は' + str(len(steps1)) + '回')
st.subheader('500日運用した場合' + str(win1) +'円')
st.subheader('遅行スパンが好転したときに上がる確率の平均は'+ str(step2) + '%')
st.subheader('遅行スパンの好転が起きたときの勝率は'+ str(win_percent2) + '%')
st.subheader('上がり幅の平均は' + str(price2) + '円')
st.subheader('起きた回数は' + str(len(steps2)) + '回')
st.subheader('500日運用した場合' + str(win2) +'円')
st.subheader('三役好転のときに上がる確率の平均は'+ str(step3) + '%')
st.subheader('三役好転が起きたときの勝率は'+ str(win_percent3) + '%')
st.subheader('上がり幅の平均は' + str(price3) + '円')
st.subheader('起きた回数は' + str(len(steps3)) + '回')
st.subheader('500日運用した場合' + str(win3) +'円')
