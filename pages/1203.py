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
 
st.title('銘柄スキャン')
# date = st.selectbox(
#     '今日は平日ですか。土日ですか。',
#     ('平日','土日'))

# if date == '平日':
#     last = 99
# else:
#     last = 98

days = 5
last = 99


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

chance4_all = []
percent_list4 = []
win4 = []
win_price4 = []
day4 = []


codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6136','6141','6208','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9007','9076','9308','9401','9409','9502','9503','9511','9513','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3167','3161','3254','3319','3360','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4043','4045','4080','4088','4095','4204','4272','4331']
codes1 = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8909','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']
codes1_1 = ['5901']
codes1_2 = ['6810','6804','6779','6754','6752','6750','6724','6723','5727','5802','5929','5943','6055','6058','6062','6101','6113','6141','6250','6269','6287','6338','6395','6407','6463','6513','6630','6641','6666','6871','6925','6937','6941','6952','6995','6999','7202','7261','7270','7414','7453','7575','7606','7613','7616','7718','7730','7732','7731','7760','7906','7915','7965','7970','7981','7984','7994','8130','8133','8174','8253','8282','8341','8411','8699','8795','8909','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2433','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3407','3433','3436','3591','3604','3657','3661','3675','4042','4080','4095','4204','4331']

codes1_3 = ['6810','6807','6804','6779','6752','6750','6724','6723','5805','5929','5943','6055','6058','6101','6113','6141','6208','6250','6298','6338','6395','6407','6412','6463','6630','6641','6666','6871','6925','6952','6962','6997','6999','7202','7240','7261','7270','7296','7313','7483','7532','7545','7575','7606','7616','7718','7732','7731','7752','7760','7864','7906','7915','7965','7970','7994','8012','8020','8086','8130','8133','8174','8233','8253','8341','8411','8570','8595','8699','8802','8804','8905','8909','8920','8923','8929','8934','9005','9076','9308','9401','9409','9503','9511','9513','9692','1518','1712','1812','1826','1969','2001','2002','2154','2158','2212','2301','2309','2427','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2784','2910','2929','3003','3048','3076','3086','3099','3103','3105','3107','3161','3254','3319','3360','3377','3407','3433','3436','3591','3632','3657','3661','3675','4028','4042','4043','4095','4204','4272','4331']

codes2 = ['5901','6810','6804','6779','6770','6754','6753','6750','6724','6723','5727','5802','5929','5943','6055','6058','6062','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6871','6925','6941','6952','6962','6999','7202','7261','7270','7296','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7752','7760','7867','7906','7915','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8909','8923','8929','8934','9005','9007','9076','9401','9409','9503','9513','9692','9832','1712','1808','1826','2002','2154','2160','2301','2309','2389','2395','2427','2432','2433','2471','2503','2531','2579','2607','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3254','3319','3405','3407','3436','3591','3604','3632','3661','4028','4042','4045','4080','4095','4204','4331']
codes3 = ['5901','6810','6804','6770','6754','6753','6752','6750','6724','6723','5727','5802','5929','5943','6013','6055','6058','6062','6070','6101','6113','6208','6269','6298','6338','6395','6407','6513','6630','6641','6666','6871','6925','6941','6952','6962','6995','7270','7296','7313','7254','7414','7421','7453','7532','7545','7606','7616','7718','7730','7732','7731','7752','7867','7965','7970','7981','7984','7994','8129','8130','8133','8233','8253','8282','8411','8699','8795','8802','8909','8920','9005','9007','9076','9308','9401','9409','9511','9513','9625','9692','1712','1808','1826','1944','1969','2154','2158','2160','2301','2389','2395','2427','2432','2433','2438','2471','2531','2607','2678','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3254','3319','3377','3405','3407','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4331']
codes4 = ['6804','6779','6770','6754','6753','6750','6724','6723','5802','5943','6013','6055','6062','6070','6101','6141','6208','6250','6338','6395','6407','6463','6513','6630','6641','6666','6925','6937','6941','6962','6995','7202','7261','7313','7254','7453','7532','7545','7575','7606','7613','7616','7718','7731','7752','7760','7867','7906','7915','7965','7970','7981','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8795','8804','8909','8920','8923','8934','9005','9007','9076','9308','9401','9503','9511','9513','9625','9692','9832','1712','1808','1944','1969','2002','2154','2158','2160','2427','2432','2433','2438','2471','2503','2607','2613','2681','2730','2784','2910','2929','3003','3048','3076','3086','3099','3107','3161','3254','3319','3405','3407','3433','3436','3604','3632','3661','3675','4042','4080','4204']
if st.button('計算を行う'):
    for code in codes1_3:
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
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
        )

        # stochasticks D
        source["sct_d_price"] = (
            100*
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()
        )

        # slow stochasticks
        source["slow_sct_d_price"] = source["sct_d_price"].rolling(window=MDAY, min_periods=MDAY).mean()

        #GMMA
        exp3 = source['Close'].ewm(span=3, adjust=False).mean()
        exp8 = source['Close'].ewm(span=8, adjust=False).mean()
        exp10 = source['Close'].ewm(span=10, adjust=False).mean()
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp15 = source['Close'].ewm(span=15, adjust=False).mean()
        source['EMA3'] = exp3
        source['EMA5'] = exp5
        source['EMA8'] = exp8
        source['EMA10'] = exp10
        source['EMA12'] = exp12
        source['EMA15'] = exp15


        exp30 = source['Close'].ewm(span=30, adjust=False).mean()
        exp35 = source['Close'].ewm(span=35, adjust=False).mean()
        exp40 = source['Close'].ewm(span=40, adjust=False).mean()
        exp45 = source['Close'].ewm(span=45, adjust=False).mean()
        exp50 = source['Close'].ewm(span=50, adjust=False).mean()
        exp60 = source['Close'].ewm(span=60, adjust=False).mean()
        source['EMA30'] = exp30
        source['EMA35'] = exp35
        source['EMA40'] = exp40
        source['EMA45'] = exp45
        source['EMA50'] = exp50
        source['EMA60'] = exp60
      



    



        check1_all = []
        check1_up = []
        check1_down = []
        price_dif1 = []
        price1_win = []

   
        


        
        
        base_line = source['base_line'][last]
        conversion_line = source['conversion_line'][last]
        conversion_line_5daybefore = source['conversion_line'][last-3]
        base_line_5daybefore = source['base_line'][last-3]
        lagging_line = source['lagging_span'][last-25]
        lagging_line_yesterday = source['lagging_span'][last-26]
        price1 = source['Close'][last]
        price_lagging = source['Close'][last-25]
        price_lagging_yesterday = source['Close'][last-26]
        conversion_direction = source['conversion_line'][last] - source['conversion_line'][last-3:]
        RSI_today = source['RSI'][last]
        adx_direction = source['ADX'][last] - source['ADX'][last-1]
        volume_difference = source['Volume'][last-1] - source['Volume'][last-2]
        #出来高を1.5倍にすると100%になる。10回。
        #遅行スパンの好転
        if all([price_lagging<=lagging_line,price_lagging_yesterday>lagging_line_yesterday,conversion_line>base_line,conversion_line_5daybefore<base_line_5daybefore,conversion_direction>0,price1>conversion_line,RSI_today>60,adx_direction>0,volume_difference>0]):
            chance1_all.append(code)







    for code in codes2:
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
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
        )

        # stochasticks D
        source["sct_d_price"] = (
            100*
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()
        )

        # slow stochasticks
        source["slow_sct_d_price"] = source["sct_d_price"].rolling(window=MDAY, min_periods=MDAY).mean()

        #GMMA
        exp3 = source['Close'].ewm(span=3, adjust=False).mean()
        exp8 = source['Close'].ewm(span=8, adjust=False).mean()
        exp10 = source['Close'].ewm(span=10, adjust=False).mean()
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp15 = source['Close'].ewm(span=15, adjust=False).mean()
        source['EMA3'] = exp3
        source['EMA5'] = exp5
        source['EMA8'] = exp8
        source['EMA10'] = exp10
        source['EMA12'] = exp12
        source['EMA15'] = exp15


        exp30 = source['Close'].ewm(span=30, adjust=False).mean()
        exp35 = source['Close'].ewm(span=35, adjust=False).mean()
        exp40 = source['Close'].ewm(span=40, adjust=False).mean()
        exp45 = source['Close'].ewm(span=45, adjust=False).mean()
        exp50 = source['Close'].ewm(span=50, adjust=False).mean()
        exp60 = source['Close'].ewm(span=60, adjust=False).mean()
        source['EMA30'] = exp30
        source['EMA35'] = exp35
        source['EMA40'] = exp40
        source['EMA45'] = exp45
        source['EMA50'] = exp50
        source['EMA60'] = exp60


        check2_all = []
        check2_up = []
        check2_down = []
        price_dif2 = []
        price2_win = []


        #大循環MACD

        macd1 = source['MACD1'][last]
        macd1_direction = source['MACD1'][last] - source['MACD1'][last-3]
        macd2 = source['MACD2'][last]
        macd2_direction = source['MACD2'][last] - source['MACD2'][last-3]
        macd3 = source['MACD3'][last]
        macd3_yesterday = source['MACD3'][last-1]
        macd3_direction = source['MACD3'][last] - source['MACD3'][last-3]
        difference1 = source['MACD2'][last] - source['MACD1'][last]
        difference2 = source['MACD2'][last-1] - source['MACD1'][last-1]

        volume_difference = source['Volume'][last-1] - source['Volume'][last-2]*1.1

        if macd1>0 and macd2>0 and macd3>0 and macd3_yesterday<0 and macd1_direction>0 and macd2_direction>0 and difference1>difference2+5 and volume_difference>0:

            chance2_all.append(code)
    









    for code in codes3:
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

        KDAY = 20  # K算定用期間
        MDAY = 3  # D算定用期間

        # stochasticks K
        source["sct_k_price"] = (
            100*
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
        )

        # stochasticks D
        source["sct_d_price"] = (
            100*
            (source["Close"] - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()/
            (source["High"].rolling(window=KDAY, min_periods=KDAY).max() - source["Low"].rolling(window=KDAY, min_periods=KDAY).min())
            .rolling(window=MDAY, min_periods=MDAY).sum()
        )

        # slow stochasticks
        source["slow_sct_d_price"] = source["sct_d_price"].rolling(window=MDAY, min_periods=MDAY).mean()

        #GMMA
        exp3 = source['Close'].ewm(span=3, adjust=False).mean()
        exp8 = source['Close'].ewm(span=8, adjust=False).mean()
        exp10 = source['Close'].ewm(span=10, adjust=False).mean()
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp15 = source['Close'].ewm(span=15, adjust=False).mean()
        source['EMA3'] = exp3
        source['EMA5'] = exp5
        source['EMA8'] = exp8
        source['EMA10'] = exp10
        source['EMA12'] = exp12
        source['EMA15'] = exp15


        exp30 = source['Close'].ewm(span=30, adjust=False).mean()
        exp35 = source['Close'].ewm(span=35, adjust=False).mean()
        exp40 = source['Close'].ewm(span=40, adjust=False).mean()
        exp45 = source['Close'].ewm(span=45, adjust=False).mean()
        exp50 = source['Close'].ewm(span=50, adjust=False).mean()
        exp60 = source['Close'].ewm(span=60, adjust=False).mean()
        source['EMA30'] = exp30
        source['EMA35'] = exp35
        source['EMA40'] = exp40
        source['EMA45'] = exp45
        source['EMA50'] = exp50
        source['EMA60'] = exp60

        check3_all = []
        check3_up = []
        check3_down = []
        price_dif3 = []
        price3_win = []





        percentk = source['sct_k_price'][last]
        percentk_direction = source['sct_k_price'][last] - source['sct_k_price'][last-1]
        slow_percentd = source['slow_sct_d_price'][last]
        slow_percentd_yesterday = source['slow_sct_d_price'][last-1]
        slow_percentd_10day = source['slow_sct_d_price'][last-10]
        volume_difference = source['Volume'][last] - source['Volume'][last-1]*1.1

        if slow_percentd_yesterday<20 and slow_percentd>20 and percentk>70 and slow_percentd_10day<30 and volume_difference>0:

            chance3_all.append(code)













    st.title('一目×ADX×RSI')
    if len(chance1_all):
        st.table(chance1_all)
    else:
        st.subheader('該当なし')
    expander1 = st.expander('確率計算1')
    expander1.write('勝率:67.5%,回数:40回,1回あたりの勝ち額:2140円')


    st.title('大循環MACD×ADX')
    if len(chance2_all):
        st.table(chance2_all)
    else:
        st.subheader('該当なし')
    expander2 = st.expander('確率計算2')
    expander2.write('勝率:72%,回数:22回,1回あたりの勝ち額:5467円')

    st.title('ストキャスティクス')
    if len(chance3_all):
        st.table(chance3_all)
    else:
        st.subheader('該当なし')
    expander3 = st.expander('確率計算3')
    expander3.write('勝率:71%,回数:14回,1回あたりの勝ち額:6357円')
