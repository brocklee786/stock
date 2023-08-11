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
from sklearn.linear_model import LinearRegression
import mplfinance.original_flavor as mpf
import datetime
import seaborn
from scipy.stats import linregress

st.set_page_config(layout="wide")
codes1 = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']

st.title("移動平均線大循環分析")
days = 1000
option = st.text_input('銘柄コードを入力してください')
if option:
    ticker = str(option) + '.T'
    tkr = yf.Ticker(ticker)
    hist = tkr.history(period=f'{days}d')
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
    source['time_id'] = source.index + 1
    price = source['Close']

    #st.table(source)

    #移動平均
    span01=5
    span02=25
    span03=50

    source['sma01'] = price.rolling(window=span01).mean()
    source['sma02'] = price.rolling(window=span02).mean()
    source['sma03'] = price.rolling(window=span03).mean()
    
    

    last=999
    source['x'] = source["sma01"] - source["sma02"]
    source['y'] = source["sma03"] - source["sma01"]
    source['z'] = source["sma03"] - source["sma02"]
    
    source["stage"] = 1
    stage6_list = []
    stage4_list = []
    stage5_list = []
    for a in range(last+1):
        #ステージの決定
        if source['sma01'][a]>source['sma02'][a]>source['sma03'][a]:
            source["stage"][a] = 1
        if source['sma02'][a]>source['sma01'][a]>source['sma03'][a]:
            source["stage"][a] = 2
        if source['sma02'][a]>source['sma03'][a]>source['sma01'][a]:
            source["stage"][a] = 3
        if source['sma03'][a]>source['sma02'][a]>source['sma01'][a]:
            source["stage"][a] = 4
            stage4_list.append(a)
        if source['sma03'][a]>source['sma01'][a]>source['sma02'][a]:
            source["stage"][a] = 5
            stage5_list.append(a)
        if source['sma01'][a]>source['sma03'][a]>source['sma02'][a]:
            source["stage"][a] = 6
            stage6_list.append(a)

    
    stage_now = source['stage'][last]
    #st.table(source)
    


    for num in range(last+1):
        index_num = last - num
        if stage_now == source['stage'][index_num]:
            continue
        if stage_now != source['stage'][index_num]:
            changed_when = index_num
            break

    #st.write(changed_when)

        



        

    stage1_now = []
    stage5_now = []
    stage6_now = []
    #ステージ１
    if source['sma01'][last]>source['sma02'][last]>source['sma03'][last]:
        st.subheader("現在のステージ:第1ステージ")
        st.subheader(str(source['Date'][changed_when])+'から')
        for a in range(changed_when+1, last+1):
            stage1_now.append(a)

        sma02_sma01 = []
        for num in stage1_now:
            sma02_sma01.append(source["x"][num])

        

        x = pd.DataFrame(stage1_now)
        y = pd.DataFrame(sma02_sma01)
                    
        model = LinearRegression()
        model.fit(x,y)

        figure, ax = plt.subplots(figsize=(8,4))
        #plt.plot(x,y,'o')
        #plt.plot(x,model.predict(x))
        
        a = model.coef_
        b = model.intercept_
        #st.write('a = ', model.coef_) 
        #st.write('b = ', model.intercept_)
        #st.pyplot(figure)
        days_until6 = -b/a - last
        if a > 0:
            st.subheader('上昇トレンド継続中')
        else:
            st.subheader('予想では第2ステージまで'+ str(int(days_until6)) + '日間')
            
        #短期の傾き
        tilt_short = source['sma01'][last] - source['sma01'][last-1]
        tilt_short2 = (source['sma01'][last] - source['sma01'][last-3]) / 3
        #中期の傾き
        tilt_mid = source['sma02'][last] - source['sma02'][last-1]
        tilt_mid2 = (source['sma02'][last] - source['sma02'][last-3]) / 3
        #長期の傾き
        tilt_long = source['sma03'][last] - source['sma03'][last-1]
        tilt_long2 = (source['sma03'][last] - source['sma03'][last-3]) / 3
        col1, col2, col3 = st.columns(3)
        #帯の広さ
        width = source['sma02'][last] - source['sma03'][last]
        if last - changed_when > 3:
            width2 = source['sma02'][changed_when+3] - source['sma03'][changed_when+3]
        else:
            width2 = source['sma02'][changed_when] - source['sma03'][changed_when]
        width_change = width - width2
        if width_change>0:
            st.subheader('帯拡大中')
        else:
            st.subheader('帯縮小の可能性')
        with col1:
            st.subheader("短期の傾き")
            st.subheader("1日:" + str(round(tilt_short)))
            st.subheader("3日:" + str(round(tilt_short2)))
        with col2:
            st.subheader("中期の傾き")
            st.subheader("1日:" + str(round(tilt_mid)))
            st.subheader("3日:" + str(round(tilt_mid2)))
        with col3:
            st.subheader("長期の傾き")
            st.subheader("1日:" + str(round(tilt_long)))
            st.subheader("3日:" + str(round(tilt_long2)))
        
    #ステージ２
    if source['sma02'][last]>source['sma01'][last]>source['sma03'][last]:
        st.subheader("第2ステージ")
    #ステージ３
    if source['sma02'][last]>source['sma03'][last]>source['sma01'][last]:
        st.subheader("第3ステージ")
    #ステージ４
    if source['sma03'][last]>source['sma02'][last]>source['sma01'][last]:
        st.subheader("第4ステージ")
    #ステージ５
    if source['sma03'][last]>source['sma01'][last]>source['sma02'][last]:
        st.subheader("第5ステージ")
        for a in range(changed_when+1, last+1):
            stage5_now.append(a)

        sma03_sma01 = []
        for num in stage5_now:
            sma03_sma01.append(source["y"][num])

        

        x = pd.DataFrame(stage5_now)
        y = pd.DataFrame(sma03_sma01)
                    
        model = LinearRegression()
        model.fit(x,y)

        figure, ax = plt.subplots(figsize=(8,4))
        #plt.plot(x,y,'o')
        #plt.plot(x,model.predict(x))
        
        a = model.coef_
        b = model.intercept_
        st.write('a = ', model.coef_) 
        st.write('b = ', model.intercept_)
        #st.pyplot(figure)
        days_until6 = -b/a - last
        if a < 0:
            st.subheader('第6ステージまで',str(int(days_until6)))
        else:
            st.subheader('逆行の可能性')
        #短期の傾き
        tilt_short = source['sma01'][last] - source['sma01'][last-1]
        tilt_short2 = (source['sma01'][last] - source['sma01'][last-3]) / 3
        #中期の傾き
        tilt_mid = source['sma02'][last] - source['sma02'][last-1]
        tilt_mid2 = (source['sma02'][last] - source['sma02'][last-3]) / 3
        #長期の傾き
        tilt_long = source['sma03'][last] - source['sma03'][last-1]
        tilt_long2 = (source['sma03'][last] - source['sma03'][last-3]) / 3
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("短期の傾き")
            st.subheader("1日:" + str(round(tilt_short)))
            st.subheader("3日:" + str(round(tilt_short2)))
        with col2:
            st.subheader("中期の傾き")
            st.subheader("1日:" + str(round(tilt_mid)))
            st.subheader("3日:" + str(round(tilt_mid2)))
        with col3:
            st.subheader("長期の傾き")
            st.subheader("1日:" + str(round(tilt_long)))
            st.subheader("3日:" + str(round(tilt_long2)))


    #ステージ６
    if source['sma01'][last]>source['sma03'][last]>source['sma02'][last]:
        st.subheader("第6ステージ")
        for a in range(changed_when+1, last+1):
            stage6_now.append(a)

        sma03_sma02 = []
        for num in stage6_now:
            sma03_sma02.append(source["z"][num])

        

        x = pd.DataFrame(stage6_now)
        y = pd.DataFrame(sma03_sma02)
                    
        model = LinearRegression()
        model.fit(x,y)

        figure, ax = plt.subplots(figsize=(8,4))
        #plt.plot(x,y,'o')
        #plt.plot(x,model.predict(x))
        

        a = model.coef_
        b = model.intercept_
        st.write('a = ', model.coef_) 
        st.write('b = ', model.intercept_)
        #st.pyplot(figure)
        days_until6 = -b/a - last
        if a < 0:
            st.subheader('第1ステージまで' + str(int(days_until6)) + '日間')
        else:
            st.subheader('逆行の可能性')
        #短期の傾き
        tilt_short = source['sma01'][last] - source['sma01'][last-1]
        tilt_short2 = (source['sma01'][last] - source['sma01'][last-3]) / 3
        #中期の傾き
        tilt_mid = source['sma02'][last] - source['sma02'][last-1]
        tilt_mid2 = (source['sma02'][last] - source['sma02'][last-3]) / 3
        #長期の傾き
        tilt_long = source['sma03'][last] - source['sma03'][last-1]
        tilt_long2 = (source['sma03'][last] - source['sma03'][last-3]) / 3
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("短期の傾き")
            st.subheader("1日:" + str(round(tilt_short)))
            st.subheader("3日:" + str(round(tilt_short2)))
        with col2:
            st.subheader("中期の傾き")
            st.subheader("1日:" + str(round(tilt_mid)))
            st.subheader("3日:" + str(round(tilt_mid2)))
        with col3:
            st.subheader("長期の傾き")
            st.subheader("1日:" + str(round(tilt_long)))
            st.subheader("3日:" + str(round(tilt_long2)))


st.subheader('ステージを探す')
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('ステージ５を探す'):
        for code in codes1:
            ticker = str(code) + '.T'
            tkr = yf.Ticker(ticker)
            hist = tkr.history(period=f'{days}d')
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
            source['time_id'] = source.index + 1
            price = source['Close']

            #st.table(source)

            #移動平均
            span01=5
            span02=25
            span03=50

            source['sma01'] = price.rolling(window=span01).mean()
            source['sma02'] = price.rolling(window=span02).mean()
            source['sma03'] = price.rolling(window=span03).mean()
            
            

            last=999
            source['x'] = source["sma01"] - source["sma02"]
            source['y'] = source["sma03"] - source["sma01"]
            source['z'] = source["sma03"] - source["sma02"]
            
            source["stage"] = 1
            stage6_list = []
            stage4_list = []
            stage5_list = []
            for a in range(last+1):
                #ステージの決定
                if source['sma01'][a]>source['sma02'][a]>source['sma03'][a]:
                    source["stage"][a] = 1
                if source['sma02'][a]>source['sma01'][a]>source['sma03'][a]:
                    source["stage"][a] = 2
                if source['sma02'][a]>source['sma03'][a]>source['sma01'][a]:
                    source["stage"][a] = 3
                if source['sma03'][a]>source['sma02'][a]>source['sma01'][a]:
                    source["stage"][a] = 4
                    stage4_list.append(a)
                if source['sma03'][a]>source['sma01'][a]>source['sma02'][a]:
                    source["stage"][a] = 5
                    stage5_list.append(a)
                if source['sma01'][a]>source['sma03'][a]>source['sma02'][a]:
                    source["stage"][a] = 6
                    stage6_list.append(a)

            stage_now = source['stage'][last]
            #st.table(source)
            


            for num in range(last+1):
                index_num = last - num
                if stage_now == source['stage'][index_num]:
                    continue
                if stage_now != source['stage'][index_num]:
                    changed_when = index_num
                    break

            
            stage_now = source['stage'][last]
            if stage_now == 5:
                st.subheader(code)
                st.write(str(source['Date'][changed_when])+'からこのステージ')
                


with col2:
    if st.button('ステージ6を探す'):
        for code in codes1:
            ticker = str(code) + '.T'
            tkr = yf.Ticker(ticker)
            hist = tkr.history(period=f'{days}d')
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
            source['time_id'] = source.index + 1
            price = source['Close']

            #st.table(source)

            #移動平均
            span01=5
            span02=25
            span03=50

            source['sma01'] = price.rolling(window=span01).mean()
            source['sma02'] = price.rolling(window=span02).mean()
            source['sma03'] = price.rolling(window=span03).mean()
            
            

            last=999
            source['x'] = source["sma01"] - source["sma02"]
            source['y'] = source["sma03"] - source["sma01"]
            source['z'] = source["sma03"] - source["sma02"]
            
            source["stage"] = 1
            stage6_list = []
            stage4_list = []
            stage5_list = []
            for a in range(last+1):
                #ステージの決定
                if source['sma01'][a]>source['sma02'][a]>source['sma03'][a]:
                    source["stage"][a] = 1
                if source['sma02'][a]>source['sma01'][a]>source['sma03'][a]:
                    source["stage"][a] = 2
                if source['sma02'][a]>source['sma03'][a]>source['sma01'][a]:
                    source["stage"][a] = 3
                if source['sma03'][a]>source['sma02'][a]>source['sma01'][a]:
                    source["stage"][a] = 4
                    stage4_list.append(a)
                if source['sma03'][a]>source['sma01'][a]>source['sma02'][a]:
                    source["stage"][a] = 5
                    stage5_list.append(a)
                if source['sma01'][a]>source['sma03'][a]>source['sma02'][a]:
                    source["stage"][a] = 6
                    stage6_list.append(a)

            stage_now = source['stage'][last]
            #st.table(source)
            


            for num in range(last+1):
                index_num = last - num
                if stage_now == source['stage'][index_num]:
                    continue
                if stage_now != source['stage'][index_num]:
                    changed_when = index_num
                    break

            
            stage_now = source['stage'][last]
            if stage_now == 6:
                st.subheader(code)
                st.write(str(source['Date'][changed_when])+'からこのステージ')
with col3:
    if st.button('ステージ1を探す'):
        for code in codes1:
            ticker = str(code) + '.T'
            tkr = yf.Ticker(ticker)
            hist = tkr.history(period=f'{days}d')
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
            source['time_id'] = source.index + 1
            price = source['Close']

            #st.table(source)

            #移動平均
            span01=5
            span02=25
            span03=50

            source['sma01'] = price.rolling(window=span01).mean()
            source['sma02'] = price.rolling(window=span02).mean()
            source['sma03'] = price.rolling(window=span03).mean()
            
            

            last=999
            source['x'] = source["sma01"] - source["sma02"]
            source['y'] = source["sma03"] - source["sma01"]
            source['z'] = source["sma03"] - source["sma02"]
            
            source["stage"] = 1
            stage6_list = []
            stage4_list = []
            stage5_list = []
            for a in range(last+1):
                #ステージの決定
                if source['sma01'][a]>source['sma02'][a]>source['sma03'][a]:
                    source["stage"][a] = 1
                if source['sma02'][a]>source['sma01'][a]>source['sma03'][a]:
                    source["stage"][a] = 2
                if source['sma02'][a]>source['sma03'][a]>source['sma01'][a]:
                    source["stage"][a] = 3
                if source['sma03'][a]>source['sma02'][a]>source['sma01'][a]:
                    source["stage"][a] = 4
                    stage4_list.append(a)
                if source['sma03'][a]>source['sma01'][a]>source['sma02'][a]:
                    source["stage"][a] = 5
                    stage5_list.append(a)
                if source['sma01'][a]>source['sma03'][a]>source['sma02'][a]:
                    source["stage"][a] = 6
                    stage6_list.append(a)

            stage_now = source['stage'][last]
            #st.table(source)
            


            for num in range(last+1):
                index_num = last - num
                if stage_now == source['stage'][index_num]:
                    continue
                if stage_now != source['stage'][index_num]:
                    changed_when = index_num
                    break

            
            stage_now = source['stage'][last]
            if stage_now == 1:
                st.subheader(code)
                st.write(str(source['Date'][changed_when])+'からこのステージ')




    


