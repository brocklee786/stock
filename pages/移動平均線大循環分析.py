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
good_codes = [1430, 1431, 1434, 1436, 1438, 1451, 1491, 1739, 1780, 1789, 1802, 1803, 1808, 1879, 1905, 1914, 1921, 1934, 1942, 1960, 1965, 2001, 2002, 2114, 2136, 2148, 2150, 2164, 2179, 2180, 2193, 2195, 2215, 2266, 2303, 2317, 2329, 2330, 2332, 2335, 2349, 2353, 2359, 2372, 2376, 2411, 2425, 2436, 2437, 2438, 2445, 2449, 2453, 2459, 2471, 2480, 2481, 2483, 2488, 2491, 2497, 2652, 2666, 2668, 2683, 2694, 2734, 2749, 2754, 2792, 2795, 2820, 2884, 2903, 2917, 2924, 2926, 2930, 2936, 2970, 2975, 2978, 2999, 3003, 3023, 3064, 3065, 3121, 3143, 3157, 3181, 3192, 3195, 3204, 3236, 3238, 3241, 3245, 3252, 3271, 3276, 3284, 3293, 3294, 3316, 3317, 3350, 3352, 3355, 3359, 3361, 3371, 3375, 3388, 3392, 3405, 3409, 3435, 3441, 3452, 3457, 3464, 3475, 3482, 3486, 3489, 3495, 3512, 3513, 3537, 3538, 3553, 3558, 3566, 3580, 3622, 3623, 3640, 3661, 3672, 3676, 3677, 3679, 3681, 3690, 3723, 3744, 3747, 3762, 3766, 3784, 3802, 3804, 3816, 3834, 3836, 3841, 3842, 3844, 3845, 3848, 3851, 3858, 3864, 3878, 3896, 3902, 3903, 3916, 3917, 3920, 3927, 3929, 3933, 3939, 3963, 3964, 3969, 3974, 3978, 3979, 3981, 3983, 3988, 3992, 3997,4005, 4012, 4017, 4026, 4027, 4056, 4057, 4058, 4060, 4076, 4082, 4093, 4097, 4124, 4165, 4167, 4171, 4174, 4177, 4220, 4224, 4237, 4243, 4245, 4251, 4256, 4260, 4272, 4275, 4286, 4287, 4290, 4293, 4298, 4299, 4326, 4331, 4333, 4345, 4346, 4356, 4360, 4372, 4389, 4391, 4392, 4421, 4430, 4433, 4437, 4447, 4448, 4449, 4463, 4482, 4486, 4489, 4495, 4524, 4531, 4554, 4556, 4579, 4591, 4592, 4611, 4621, 4636, 4645, 4662, 4674, 4687, 4689, 4709, 4718, 4736, 4743, 4750, 4752, 4761, 4767, 4769, 4777, 4784, 4792, 4800, 4809, 4820, 4847, 4882, 4884, 4886, 4902, 4931, 4936, 4955, 4977, 4979, 4987, 4992, 5036, 5074, 5121, 5126, 5138, 5199, 5202, 5243, 5277, 5363, 5449, 5476, 5527, 5542, 5563, 5610, 5660, 5715, 5802, 5803, 5817, 5821, 5929, 5930, 5936, 5969, 5975, 5989, 5991, 5992, 5994, 6018, 6038, 6039, 6049, 6058, 6059, 6062, 6063, 6088, 6091, 6099, 6113, 6131, 6151, 6161, 6164, 6166, 6171, 6177, 6183, 6184, 6186, 6188, 6189, 6197, 6199, 6208, 6218, 6226, 6229, 6232, 6237, 6247, 6265, 6269, 6276, 6287, 6289, 6293, 6325, 6330, 6335, 6336, 6363, 6364, 6376, 6381, 6395, 6416, 6418, 6459, 6464, 6473, 6480, 6486, 6518, 6522, 6535, 6537, 6539, 6540, 6544, 6546, 6555, 6557, 6564, 6570, 6578, 6625, 6633, 6640, 6653, 6658, 6696, 6715, 6744, 6745, 6779, 6817, 6819, 6836, 6838, 6862, 6879, 6904, 6914, 6955, 7004, 7014, 7030, 7031, 7042, 7049, 7057, 7074, 7080, 7082, 7085, 7092, 7110, 7112, 7126, 7131, 7134, 7162, 7177, 7191, 7196, 7199, 7201, 7224, 7291, 7315, 7343, 7352, 7354, 7357, 7359, 7367, 7374, 7378, 7379, 7427, 7434, 7438, 7444, 7455, 7504, 7510, 7523, 7524, 7527, 7567, 7570, 7590, 7599, 7605, 7608, 7613, 7619, 7624, 7638, 7709, 7711, 7723, 7730, 7739, 7745, 7774, 7777, 7781, 7792, 7793, 7804, 7807, 7818, 7819, 7823, 7831, 7833, 7837, 7840, 7847, 7857, 7865, 7875, 7879, 7888, 7897, 7898, 7922, 7939, 7953, 7957, 7972, 7976, 7985, 7994, 8020, 8023, 8037, 8061, 8065, 8066, 8070, 8081, 8095, 8103, 8107, 8125, 8133, 8135, 8139, 8141, 8147, 8151, 8157, 8163, 8168, 8219, 8230, 8256, 8281, 8291, 8511, 8570, 8617, 8704, 8798, 8802, 8804, 8844, 8860, 8869, 8876, 8893, 8897, 8904, 8905, 8908, 8929, 8931, 8946, 8995, 9029, 9034, 9055, 9069, 9115, 9212, 9221, 9233, 9240, 9242, 9245, 9249, 9259, 9273, 9275, 9310, 9312, 9319, 9322, 9351, 9360, 9368, 9369, 9381, 9408, 9416, 9421, 9424, 9432, 9444, 9450, 9466, 9470, 9504, 9511, 9551, 9562, 9563, 9564, 9613, 9619, 9633, 9651, 9702, 9717, 9765, 9768, 9782, 9783, 9791, 9795, 9799, 9812, 9832, 9845, 9856, 9872, 9882, 9895, 9900, 9908, 9919, 9928, 9930, 9959, 9980, 9982]

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
        for code in good_codes:
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
        for code in good_codes:
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
        for code in good_codes:
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




    


