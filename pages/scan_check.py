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
last = 999


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

chance5_all = []
percent_list5 = []
win5 = []
win_price5 = []
day5 = []

chance6_all = []
percent_list6 = []
win6 = []
win_price6 = []
day5 = []

chance7_all = []
percent_list7 = []
win7 = []
win_price7 = []
day7 = []



codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6136','6141','6208','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8570','8595','8699','8795','8802','8804','8876','8905','8920','8923','8929','8934','9005','9006','9007','9076','9308','9401','9409','9502','9503','9511','9513','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3167','3161','3254','3319','3360','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4043','4045','4080','4088','4095','4204','4272','4331']
codes1 = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6666','6871','6925','6937','6941','6952','6962','6995','6999','7202','7261','7270','7296','7313','7254','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4080','4095','4204','4331']
codes1_1 = ['5901']
codes1_2 = ['6810','6804','6779','6754','6752','6750','6724','6723','5727','5802','5929','5943','6055','6058','6062','6101','6113','6141','6250','6269','6287','6338','6395','6407','6463','6513','6630','6641','6666','6871','6925','6937','6941','6952','6995','6999','7202','7261','7270','7414','7453','7575','7606','7613','7616','7718','7730','7732','7731','7760','7906','7915','7965','7970','7981','7984','7994','8130','8133','8174','8253','8282','8341','8411','8699','8795','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2158','2160','2301','2309','2389','2395','2433','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3407','3433','3436','3591','3604','3657','3661','3675','4042','4080','4095','4204','4331']

codes1_3 = ['6810','6807','6804','6779','6752','6750','6724','6723','5805','5929','5943','6055','6058','6101','6113','6141','6208','6250','6298','6338','6395','6407','6412','6463','6630','6641','6666','6871','6925','6952','6962','6997','6999','7202','7240','7261','7270','7296','7313','7483','7532','7545','7575','7606','7616','7718','7732','7731','7752','7760','7864','7906','7915','7965','7970','7994','8012','8020','8086','8130','8133','8174','8233','8253','8341','8411','8570','8595','8699','8802','8804','8905','8920','8923','8929','8934','9005','9076','9308','9401','9409','9503','9511','9513','9692','1518','1712','1812','1826','1969','2001','2002','2154','2158','2212','2301','2309','2427','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2784','2910','2929','3003','3048','3076','3086','3099','3103','3105','3107','3161','3254','3319','3360','3377','3407','3433','3436','3591','3632','3657','3661','3675','4028','4042','4043','4095','4204','4272','4331']

codes2 = ['5901','6810','6804','6779','6770','6754','6753','6750','6724','6723','5727','5802','5929','5943','6055','6058','6062','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6463','6513','6630','6871','6925','6941','6952','6962','6999','7202','7261','7270','7296','7414','7421','7453','7532','7545','7575','7606','7613','7616','7718','7730','7732','7752','7760','7867','7906','7915','7970','7981','7984','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8923','8929','8934','9005','9007','9076','9401','9409','9503','9513','9692','9832','1712','1808','1826','2002','2154','2160','2301','2309','2389','2395','2427','2432','2433','2471','2503','2531','2579','2607','2678','2681','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3254','3319','3405','3407','3436','3591','3604','3632','3661','4028','4042','4045','4080','4095','4204','4331']
codes3 = ['5901','6810','6804','6770','6754','6753','6752','6750','6724','6723','5727','5802','5929','5943','6013','6055','6058','6062','6070','6101','6113','6208','6269','6298','6338','6395','6407','6513','6630','6641','6666','6871','6925','6941','6952','6962','6995','7270','7296','7313','7254','7414','7421','7453','7532','7545','7606','7616','7718','7730','7732','7731','7752','7867','7965','7970','7981','7984','7994','8129','8130','8133','8233','8253','8282','8411','8699','8795','8802','8920','9005','9007','9076','9308','9401','9409','9511','9513','9625','9692','1712','1808','1826','1944','1969','2154','2158','2160','2301','2389','2395','2427','2432','2433','2438','2471','2531','2607','2678','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3254','3319','3377','3405','3407','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4331']
codes4 = ['6804','6779','6770','6754','6753','6750','6724','6723','5802','5943','6013','6055','6062','6070','6101','6141','6208','6250','6338','6395','6407','6463','6513','6630','6641','6666','6925','6937','6941','6962','6995','7202','7261','7313','7254','7453','7532','7545','7575','7606','7613','7616','7718','7731','7752','7760','7867','7906','7915','7965','7970','7981','7994','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8411','8795','8804','8920','8923','8934','9005','9007','9076','9308','9401','9503','9511','9513','9625','9692','9832','1712','1808','1944','1969','2002','2154','2158','2160','2427','2432','2433','2438','2471','2503','2607','2613','2681','2730','2784','2910','2929','3003','3048','3076','3086','3099','3107','3161','3254','3319','3405','3407','3433','3436','3604','3632','3661','3675','4042','4080','4204']
codes5 = ['5901','6810','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6055','6058','6062','6070','6101','6113','6141','6208','6250','6269','6287','6298','6338','6395','6407','6513','6630','6641','6666','6871','6925','6937','6941','6952','6995','6999','7202','7261','7270','7296','7313','7414','7421','7453','7532','7545','7606','7613','7616','7718','7730','7732','7731','7752','7760','7867','7906','7915','7965','7981','7984','7994','8020','8129','8130','8133','8174','8233','8253','8282','8341','8411','8699','8795','8802','8804','8920','8923','8929','8934','9005','9007','9076','9308','9401','9409','9503','9511','9513','9625','9692','9832','1712','1808','1826','1944','1969','2002','2154','2160','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2685','2730','2784','2792','2910','2929','3003','3048','3076','3086','3099','3105','3107','3161','3254','3319','3377','3405','3407','3433','3436','3591','3604','3632','3657','3661','3675','4028','4042','4045','4095','4204','4331']
good_codes = [1430, 1431, 1434, 1436, 1438, 1451, 1491, 1739, 1780, 1789, 1802, 1803, 1808, 1879, 1905, 1914, 1921, 1934, 1942, 1960, 1965, 2001, 2002, 2114, 2136, 2148, 2150, 2164, 2179, 2180, 2185, 2186, 2193, 2195, 2215, 2266, 2303, 2317, 2329, 2330, 2332, 2335, 2349, 2353, 2359, 2372, 2376, 2411, 2425, 2436, 2437, 2438, 2445, 2449, 2453, 2459, 2471, 2480, 2481, 2483, 2488, 2491, 2497, 2652, 2666, 2668, 2683, 2694, 2734, 2749, 2754, 2792, 2795, 2820, 2884, 2903, 2917, 2922, 2924, 2926, 2930, 2936, 2970, 2975, 2978, 2999, 3003, 3023, 3064, 3065, 3121, 3143, 3157, 3181, 3192, 3195, 3204, 3236, 3238, 3241, 3245, 3252, 3271, 3276, 3284, 3293, 3294, 3316, 3317, 3350, 3352, 3355, 3359, 3361, 3371, 3375, 3388, 3392, 3405, 3409, 3435, 3441, 3449, 3452, 3457, 3464, 3475, 3482, 3486, 3489, 3495, 3512, 3513, 3537, 3538, 3553, 3558, 3566, 3580, 3622, 3623, 3640, 3661, 3672, 3676, 3677, 3679, 3681, 3690, 3723, 3744, 3747, 3762, 3766, 3784, 3802, 3804, 3816, 3834, 3836, 3841, 3842, 3844, 3845, 3848, 3851, 3858, 3864, 3878, 3896, 3900, 3902, 3903, 3916, 3917, 3920, 3927, 3929, 3933, 3939, 3963, 3964, 3969, 3974, 3978, 3979, 3981, 3983, 3988, 3992, 3997,4005, 4012, 4017, 4026, 4027, 4056, 4057, 4058, 4060, 4076, 4082, 4093, 4097, 4124, 4165, 4167, 4171, 4174, 4177, 4220, 4224, 4237, 4243, 4245, 4251, 4256, 4260, 4272, 4275, 4286, 4287, 4290, 4293, 4298, 4299, 4326, 4331, 4333, 4345, 4346, 4356, 4360, 4372, 4380, 4386, 4389, 4391, 4392, 4421, 4430, 4433, 4437, 4447, 4448, 4449, 4463, 4482, 4486, 4489, 4495, 4524, 4531, 4554, 4556, 4579, 4591, 4592, 4611, 4621, 4636, 4645, 4662, 4674, 4687, 4689, 4709, 4718, 4736, 4743, 4750, 4752, 4761, 4767, 4769, 4777, 4784, 4792, 4800, 4809, 4820, 4847, 4882, 4884, 4886, 4888, 4902, 4931, 4936, 4955, 4977, 4979, 4987, 4992, 5036, 5074, 5121, 5126, 5138, 5199, 5202, 5243, 5277, 5363, 5449, 5476, 5527, 5542, 5563, 5610, 5660, 5715, 5802, 5803, 5817, 5821, 5929, 5930, 5936, 5969, 5975, 5989, 5991, 5992, 5994, 6018, 6038, 6039, 6049, 6058, 6059, 6062, 6063, 6088, 6091, 6099, 6113, 6131, 6151, 6161, 6164, 6166, 6171, 6177, 6183, 6184, 6186, 6188, 6189, 6193, 6197, 6199, 6208, 6218, 6226, 6229, 6232, 6237, 6247, 6265, 6269, 6276, 6287, 6289, 6293, 6325, 6330, 6335, 6336, 6363, 6364, 6376, 6381, 6395, 6416, 6418, 6459, 6464, 6473, 6480, 6486, 6518, 6522, 6535, 6537, 6539, 6540, 6544, 6546, 6555, 6557, 6564, 6570, 6578, 6625, 6633, 6640, 6653, 6658, 6696, 6715, 6744, 6745, 6779, 6817, 6819, 6836, 6838, 6862, 6879, 6904, 6914, 6955, 7004, 7014, 7030, 7031, 7042, 7049, 7057, 7074, 7080, 7082, 7085, 7092, 7110, 7112, 7126, 7131, 7134, 7162, 7177, 7191, 7196, 7199, 7201, 7224, 7291, 7315, 7343, 7352, 7354, 7357, 7359, 7367, 7374, 7378, 7379, 7427, 7434, 7438, 7444, 7455, 7504, 7510, 7523, 7524, 7527, 7567, 7570, 7590, 7599, 7605, 7608, 7613, 7619, 7624, 7638, 7709, 7711, 7723, 7730, 7739, 7745, 7774, 7777, 7781, 7792, 7793, 7804, 7807, 7818, 7819, 7823, 7831, 7833, 7837, 7840, 7847, 7857, 7865, 7875, 7879, 7888, 7897, 7898, 7922, 7939, 7953, 7957, 7972, 7976, 7985, 7994, 8020, 8023, 8037, 8061, 8065, 8066, 8070, 8081, 8095, 8103, 8107, 8125, 8133, 8135, 8139, 8141, 8147, 8151, 8157, 8163, 8168, 8219, 8230, 8256, 8281, 8291, 8511, 8570, 8617, 8704, 8798, 8802, 8804, 8844, 8860, 8869, 8876, 8893, 8897, 8904, 8905, 8908, 8929, 8931, 8946, 8995, 9029, 9034, 9055, 9069, 9115, 9212, 9221, 9233, 9240, 9242, 9245, 9249, 9259, 9273, 9275, 9310, 9312, 9319, 9322, 9351, 9360, 9368, 9369, 9381, 9408, 9416, 9421, 9424, 9432, 9444, 9450, 9466, 9470, 9504, 9511, 9519, 9551, 9561, 9562, 9563, 9564, 9613, 9619, 9633, 9651, 9702, 9717, 9765, 9768, 9782, 9783, 9791, 9795, 9799, 9812, 9832, 9845, 9856, 9872, 9882, 9895, 9900, 9908, 9919, 9928, 9930, 9959, 9980, 9982]

if st.button('計算を行う'):
    for code in good_codes:
        option = code
        ticker = str(option) + '.T'
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

        if source.index[-1] == 999:
  
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
          exp20 = source['Close'].ewm(span=20, adjust=False).mean()
          source['EMA3'] = exp3
          source['EMA5'] = exp5
          source['EMA8'] = exp8
          source['EMA10'] = exp10
          source['EMA12'] = exp12
          source['EMA15'] = exp15
          source['EMA20'] = exp20
  
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
          #ボリンジャーバンド
          # 移動平均線
          source["SMA20"] = source["Close"].rolling(window=20,min_periods=20).mean()
          # 標準偏差
          source["std"] = source["Close"].rolling(window=20,min_periods=20).std()
          # ボリンジャーバンド
          source["2upper"] = source["SMA20"] + (2 * source["std"])
          source["2lower"] = source["SMA20"] - (2 * source["std"])
          source["3upper"] = source["SMA20"] + (3 * source["std"])
          source["3lower"] = source["SMA20"] - (3 * source["std"])
          source['bandwidth'] = (source['2upper'] - source['2lower']) / source['SMA20']
          source['percent_b'] = (source['Close'] - source['2lower']) / (source['2upper'] - source['2lower'])
          minimum20 = source["Low"].rolling(window=30).min()
          source["minimum"] = minimum20
          minimum_band = source["bandwidth"].rolling(window=120).min()
          source["minimum_band"] = minimum_band
          maximum30 = source["Close"].rolling(window=120).max()
          source["maximum"] = maximum30
  
  
      
  
  
  
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
          conversion_direction = source['conversion_line'][last] - source['conversion_line'][last-3]
          RSI_today = source['RSI'][last]
          adx_direction = source['ADX'][last] - source['ADX'][last-1]
          volume_difference = source['Volume'][last-1] - source['Volume'][last-2]
          volume = source['Volume'][last-1]
          #出来高を1.5倍にすると100%になる。10回。
          #遅行スパンの好転
          if price_lagging<=lagging_line and price_lagging_yesterday>lagging_line_yesterday and conversion_line>base_line and conversion_line_5daybefore<base_line_5daybefore and conversion_direction>0 and price1>conversion_line and RSI_today>60 and adx_direction>0 and volume_difference>0 and volume>10000:
              if code==any(['6941', '8905', '2792', '6807', '6997', '1812', '7730', '7864', '4272', '8795', '7613', '2395', '8570', '5802', '6754', '1518', '8595', '2389', '7254', '7453', '6287', '7984', '7240', '2160', '1808', '4043', '3604', '7414', '2212', '9007', '8012', '2001', '2432', '4045', '6062', '8129', '7483', '2730', '8282', '7867', '5901', '7981', '3103', '3405', '5727', '6013', '4080', '6937', '1944', '6753', '6513', '6412', '9625', '9832', '6995', '6070', '3360', '6269', '7421', '6770']):
                  continue
              else:
                  chance1_all.append(code)
  
  
  
  
  
  
  
  
   
  
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
              if code==any(['5805', '2158', '7965', '8920', '7313', '3377', '3657', '6641', '2613', '7254', '2438', '6752', '7731', '9308', '6013', '1969', '6937', '1944', '6666', '3675', '9511', '9625', '3433', '6995', '6070', '3161']):
                  continue
              else:
                  chance2_all.append(code)
      
  
  
  
  
  
  
  
  
  
   
  
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
              if code==any(['5805', '6463', '2579', '6779', '7915', '8020', '7613', '7760', '8341', '2002', '8804', '8174', '7202', '2613', '9503', '6287', '2681', '6250', '6999', '8934', '8929', '7906', '8086', '7261', '8923', '6141', '7575', '4080', '4204', '6937', '4095', '9832', '3433', '2503', '2309', '3161']):
                  continue
              else:
                  chance3_all.append(code)
  
  
   
  
  
          check4_all = []
          check4_up = []
          check4_down = []
          price_dif4 = []
          price4_win = []
        
  
  
  
          price1 = source['Close'][last]
          RSI_today = source['RSI'][last]
          volume_difference = source['Volume'][last-1] - source['Volume'][last-2]
          base_line = source['base_line'][last]
          base_line_yesterday = source['base_line'][last-11]
          base_line_yesterday2 = source['base_line'][last-22]
          minimum = source['minimum'][last]
  
          if -15<base_line-base_line_yesterday<15 and -15<base_line-base_line_yesterday2<15 and -5<price1-minimum<5 and 45<RSI_today<55 and volume_difference>0:
              chance4_all.append(code)
  
   
   
   
          check5_all = []
          check5_up = []
          check5_down = []
          price_dif5 = []
          price5_win = []
   
   
   
   
   
  
          bandwidth = source['bandwidth'][last]
          bandwidth_yesterday = source['bandwidth'][last-1]
          percent_b = source['percent_b'][last]
          percent_b_yesterday = source['percent_b'][last-1]
          volume_difference = source['Volume'][last] - source['Volume'][last-1]*1.5
          midband = source['SMA20'][last]
          midband_yesterday = source['SMA20'][last-1]
  
  
          if percent_b>1 and percent_b_yesterday<1 and bandwidth_yesterday<bandwidth and midband>midband_yesterday:
              for k in range(-5,0):
                  bandwidth = source['bandwidth'][last+k]
                  bandwidth_yesterday = source['bandwidth'][last-1+k]
                  minimum_bandwidth = source['minimum_band'][last+k]
                  minimum_bandwidth_yesterday = source['minimum_band'][last-1+k]
                  percent_b2 = source['percent_b'][last+k]
                  ema20 = source['EMA20'][last+k]
                  ema50 = source['EMA50'][last+k]
                  if bandwidth == minimum_bandwidth and 0.45<percent_b2<0.55:
                      if code==any(['6463', '2158', '7970', '6962', '7254', '2681', '8086', '7575', '4080']):
                          continue
                      else:
                          chance5_all.append(code)
  
   
   
  
  
                 
  
  
   
  
          
  
  
          check6_all = []
          check6_up = []
          check6_down = []
          price_dif6 = []
          price6_win = []
          price6_win_only=[]
          price6_lose_only=[]
  
  
  
  
  
  
  
          bandwidth = source['bandwidth'][last]
          bandwidth_yesterday = source['bandwidth'][last-1]
          percent_b = source['percent_b'][last]
          percent_b_yesterday = source['percent_b'][last-1]
          price = source['Close'][last]
          price_yesterday = source['Close'][last-1]
          adx_direction = source['ADX'][last] - source['ADX'][last-1]
          maximum = source['maximum'][last]
          maximum_yesterday = source['maximum'][last-1]
  
          if price_yesterday!=maximum_yesterday and price==maximum and adx_direction>0 and bandwidth>bandwidth_yesterday and percent_b>percent_b_yesterday:
              check6_all.append(code)
              
  
   
   
  


    



    



    st.title('一目×ADX×RSI')
    if len(chance1_all):
        st.table(chance1_all)
    else:
        st.subheader('該当なし')
    expander1 = st.expander('確率計算1')
    expander1.write('日数:10日,損切り:0.8ATR,,勝率:64%,期待値:2,080円')


    st.title('大循環MACD×ADX')
    if len(chance2_all):
        st.table(chance2_all)
    else:
        st.subheader('該当なし')
    expander2 = st.expander('確率計算2')
    expander2.write('日数:5日,損切り:0.8ATR,,勝率:54%,期待値:2,145円')

    st.title('ストキャスティクス')
    if len(chance3_all):
        st.table(chance3_all)
    else:
        st.subheader('該当なし')
    expander3 = st.expander('確率計算3')
    expander3.write('日数:5日,損切り:0.8ATR,,勝率:70%,期待値:5,447円')


    st.title('もみ合い相場(底取り)')
    if len(chance4_all):
        st.table(chance4_all)
    else:
        st.subheader('該当なし')
    expander3 = st.expander('確率計算4')
    expander3.write('日数:5日,損切り:1.4ATR,,勝率:57%,期待値:1,099円')


    st.title('ボリンジャーバンド')
    if len(chance5_all):
        st.table(chance5_all)
    else:
        st.subheader('該当なし')
    expander5 = st.expander('確率計算5')
    expander5.write('日数:20日,損切り:1.5ATR,,勝率:63%,期待値:3,193円')


    st.title('高値ブレイク')
    if len(chance6_all):
        st.table(chance6_all)
    else:
        st.subheader('該当なし')
    expander6 = st.expander('確率計算6')
    expander6.write('日数:20日,損切り:1.5ATR,,勝率:52%,期待値:4,861円')
          
          
          
   
