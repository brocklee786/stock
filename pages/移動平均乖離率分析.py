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
import mplfinance.original_flavor as mpf
from scipy.stats import linregress
import seaborn as sns


st.set_page_config(layout="wide")

st.title("移動平均乖離率分析")
codes1_3 = ['6810','6807','6804','6779','6752','6750','6724','6723','5805','5929','5943','6055','6058','6101','6113','6141','6208','6250','6298','6338','6395','6407','6412','6463','6630','6666','6871','6925','6952','6962','6997','6999','7202','7240','7261','7270','7296','7313','7483','7532','7545','7575','7606','7616','7718','7732','7731','7752','7760','7864','7906','7915','7965','7970','7994','8012','8020','8086','8130','8133','8174','8233','8253','8341','8411','8570','8595','8699','8802','8804','8905','8920','8923','8929','8934','9005','9076','9308','9401','9409','9503','9511','9513','9692','1518','1712','1812','1826','1969','2001','2002','2154','2158','2212','2301','2309','2427','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2784','2910','2929','3003','3048','3076','3086','3099','3103','3105','3107','3161','3254','3319','3360','3377','3407','3433','3436','3591','3632','3657','3661','3675','4028','4042','4043','4095','4204','4272','4331']
good_codes = [1430, 1431, 1434, 1436, 1438, 1451, 1491, 1739, 1780, 1789, 1802, 1803, 1808, 1879, 1905, 1914, 1921, 1934, 1942, 1960, 1965, 2001, 2002, 2114, 2136, 2148, 2150, 2164, 2179, 2180, 2185, 2186, 2193, 2195, 2215, 2266, 2303, 2317, 2329, 2330, 2332, 2335, 2349, 2353, 2359, 2372, 2376, 2411, 2425, 2436, 2437, 2438, 2445, 2449, 2453, 2459, 2471, 2480, 2481, 2483, 2488, 2491, 2497, 2652, 2666, 2668, 2683, 2694, 2734, 2749, 2754, 2792, 2795, 2820, 2884, 2903, 2917, 2922, 2924, 2926, 2930, 2936, 2970, 2975, 2978, 2999, 3003, 3023, 3064, 3065, 3121, 3143, 3157, 3181, 3192, 3195, 3204, 3236, 3238, 3241, 3245, 3252, 3271, 3276, 3284, 3293, 3294, 3316, 3317, 3350, 3352, 3355, 3359, 3361, 3371, 3375, 3388, 3392, 3405, 3409, 3435, 3441, 3449, 3452, 3457, 3464, 3475, 3482, 3486, 3489, 3495, 3512, 3513, 3537, 3538, 3553, 3558, 3566, 3580, 3622, 3623, 3640, 3661, 3672, 3676, 3677, 3679, 3681, 3690, 3723, 3744, 3747, 3762, 3766, 3784, 3802, 3804, 3816, 3834, 3836, 3841, 3842, 3844, 3845, 3848, 3851, 3858, 3864, 3878, 3896, 3900, 3902, 3903, 3916, 3917, 3920, 3927, 3929, 3933, 3939, 3963, 3964, 3969, 3974, 3978, 3979, 3981, 3983, 3988, 3992, 3997,4005, 4012, 4017, 4026, 4027, 4056, 4057, 4058, 4060, 4076, 4082, 4093, 4097, 4124, 4165, 4167, 4171, 4174, 4177, 4220, 4224, 4237, 4243, 4245, 4251, 4256, 4260, 4272, 4275, 4286, 4287, 4290, 4293, 4298, 4299, 4326, 4331, 4333, 4345, 4346, 4356, 4360, 4372, 4380, 4386, 4389, 4391, 4392, 4421, 4430, 4433, 4437, 4447, 4448, 4449, 4463, 4482, 4486, 4489, 4495, 4524, 4531, 4554, 4556, 4579, 4591, 4592, 4611, 4621, 4636, 4645, 4662, 4674, 4687, 4689, 4709, 4718, 4736, 4743, 4750, 4752, 4761, 4767, 4769, 4777, 4784, 4792, 4800, 4809, 4820, 4847, 4882, 4884, 4886, 4888, 4902, 4931, 4936, 4955, 4977, 4979, 4987, 4992, 5036, 5074, 5121, 5126, 5138, 5199, 5202, 5243, 5277, 5363, 5449, 5476, 5527, 5542, 5563, 5610, 5660, 5715, 5802, 5803, 5817, 5821, 5929, 5930, 5936, 5969, 5975, 5989, 5991, 5992, 5994, 6018, 6038, 6039, 6049, 6058, 6059, 6062, 6063, 6088, 6091, 6099, 6113, 6131, 6151, 6161, 6164, 6166, 6171, 6177, 6183, 6184, 6186, 6188, 6189, 6193, 6197, 6199, 6208, 6218, 6226, 6229, 6232, 6237, 6247, 6265, 6269, 6276, 6287, 6289, 6293, 6325, 6330, 6335, 6336, 6363, 6364, 6376, 6381, 6395, 6416, 6418, 6459, 6464, 6473, 6480, 6486, 6518, 6522, 6535, 6537, 6539, 6540, 6544, 6546, 6555, 6557, 6564, 6570, 6578, 6625, 6633, 6640, 6653, 6658, 6696, 6715, 6744, 6745, 6779, 6817, 6819, 6836, 6838, 6862, 6879, 6904, 6914, 6955, 7004, 7014, 7030, 7031, 7042, 7049, 7057, 7074, 7080, 7082, 7085, 7092, 7110, 7112, 7126, 7131, 7134, 7162, 7177, 7191, 7196, 7199, 7201, 7224, 7291, 7315, 7343, 7352, 7354, 7357, 7359, 7367, 7374, 7378, 7379, 7427, 7434, 7438, 7444, 7455, 7504, 7510, 7523, 7524, 7527, 7567, 7570, 7590, 7599, 7605, 7608, 7613, 7619, 7624, 7638, 7709, 7711, 7723, 7730, 7739, 7745, 7774, 7777, 7781, 7792, 7793, 7804, 7807, 7818, 7819, 7823, 7831, 7833, 7837, 7840, 7847, 7857, 7865, 7875, 7879, 7888, 7897, 7898, 7922, 7939, 7953, 7957, 7972, 7976, 7985, 7994, 8020, 8023, 8037, 8061, 8065, 8066, 8070, 8081, 8095, 8103, 8107, 8125, 8133, 8135, 8139, 8141, 8147, 8151, 8157, 8163, 8168, 8219, 8230, 8256, 8281, 8291, 8511, 8570, 8617, 8704, 8798, 8802, 8804, 8844, 8860, 8869, 8876, 8893, 8897, 8904, 8905, 8908, 8929, 8931, 8946, 8995, 9029, 9034, 9055, 9069, 9115, 9212, 9221, 9233, 9240, 9242, 9245, 9249, 9259, 9273, 9275, 9310, 9312, 9319, 9322, 9351, 9360, 9368, 9369, 9381, 9408, 9416, 9421, 9424, 9432, 9444, 9450, 9466, 9470, 9504, 9511, 9519, 9551, 9561, 9562, 9563, 9564, 9613, 9619, 9633, 9651, 9702, 9717, 9765, 9768, 9782, 9783, 9791, 9795, 9799, 9812, 9832, 9845, 9856, 9872, 9882, 9895, 9900, 9908, 9919, 9928, 9930, 9959, 9980, 9982]

def get_kessan(option):
    # 指定URLのHTMLデータを取得
    code = int(option)
    url = "https://minkabu.jp/stock/{0:d}/settlement".format(code)
    html = requests.get(url)
    # BeautifulSoupのHTMLパーサーを生成
    soup = BeautifulSoup(html.content, "html.parser")
 
    # 全<table>要素を抽出
    table_all = soup.find_all('table')
 
    # 決算情報の<table>要素を検索する。
    fin_table1 = None
    for table in table_all:
   
        # <caption>要素を取得
        caption = table.find('caption')
        if caption is None:
            continue
   
        # <caption>要素の文字列が目的のものと一致したら終了
        if caption.text == '決算情報':
            fin_table1 = table
            break
 
    # <table>要素内のヘッダ情報を取得する。
    headers = []
    thead_th = fin_table1.find('thead').find_all('th')
    for th in thead_th:
        headers.append(th.text)
 
    # <table>要素内のデータを取得する。
    rows = []
    tbody_tr = fin_table1.find('tbody').find_all('tr')
    for tr in tbody_tr:
   
        # 1行内のデータを格納するためのリスト
        row = []
   
        # <tr>要素内の<th>要素を取得する。
        th = tr.find('th')
        row.append(th.text)
   
        # <tr>要素内の<td>要素を取得する。
        td_all = tr.find_all('td')
        for td in td_all:
            row.append(td.text)
   
        # 1行のデータを格納したリストを、リストに格納
        rows.append(row)
 
    # DataFrameを生成する
    df2 = pd.DataFrame(rows, columns=headers)
 
    # 先頭の列(決算期)をインデックスに指定する
    df2 = df2.set_index(headers[0])
    return(df2)

# 数値のカンマを削除する関数
def trim_camma_kessan(x):
    # 2,946,639.3のようなカンマ区切り、小数点有りの数値か否か確認する
    comma_re = re.search(r"(\d{1,3}(,\d{3})*(\.\d+){0,1})", x)
    if comma_re:
        value = comma_re.group(1)
        value = value.replace(',', '') # カンマを削除
        return value
   
    return x
 
option = st.text_input('銘柄コードを入力してください')

if option:
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

    #移動平均
    span01=5
    span02=25
    span03=50

    source['sma01'] = price.rolling(window=span01).mean()
    source['sma02'] = price.rolling(window=span02).mean()
    source['sma03'] = price.rolling(window=span03).mean()

    # 移動平均線乖離率
    source["SMA5_乖離率"] = (source["Close"] - source["sma01"]) / source["sma01"] * 100
    source["SMA25_乖離率"] = (source["Close"] - source["sma02"]) / source["sma02"] * 100
    source["SMA50_乖離率"] = (source["Close"] - source["sma03"]) / source["sma03"] * 100

    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    sns.histplot(source["SMA5_乖離率"], ax=ax[0])
    sns.histplot(source["SMA25_乖離率"], ax=ax[1])
    sns.histplot(source["SMA50_乖離率"], ax=ax[2])
    st.pyplot(fig)
    

    info = source[["SMA5_乖離率", "SMA25_乖離率", "SMA50_乖離率"]].describe().round(2)
    st.table(info)

    # 今日の乖離率
    last = 999
    today_short = (source["Close"][last] - source["sma01"][last]) / source["sma01"][last] * 100
    today_mid = (source["Close"][last] - source["sma02"][last]) / source["sma02"][last] * 100
    today_long = (source["Close"][last] - source["sma03"][last]) / source["sma03"][last] * 100

    short_percent68 = float(info["SMA5_乖離率"][1]) - float(info["SMA5_乖離率"][2]) *1
    short_percent95 = float(info["SMA5_乖離率"][1]) - float(info["SMA5_乖離率"][2]) *2
    short_percent99 = float(info["SMA5_乖離率"][1]) - float(info["SMA5_乖離率"][2]) *3

    mid_percent68 = float(info["SMA25_乖離率"][1]) - float(info["SMA25_乖離率"][2]) *1
    mid_percent95 = float(info["SMA25_乖離率"][1]) - float(info["SMA25_乖離率"][2]) *2
    mid_percent99 = float(info["SMA25_乖離率"][1]) - float(info["SMA25_乖離率"][2]) *3

    long_percent68 = float(info["SMA50_乖離率"][1]) - float(info["SMA50_乖離率"][2]) *1
    long_percent95 = float(info["SMA50_乖離率"][1]) - float(info["SMA50_乖離率"][2]) *2
    long_percent99 = float(info["SMA50_乖離率"][1]) - float(info["SMA50_乖離率"][2]) *3
    col1, col2, col3 = st.columns(3)

    # コンテキストマネージャとして使う
    with col1:
        st.subheader('<短期>')
        st.write('σ:',str(short_percent68))
        st.write('2σ:',str(short_percent95))
        st.write('3σ:',str(short_percent99))
        st.write('現在の乖離率短期',str(today_short))
    with col2:
        st.subheader('<中期>')
        st.write('σ:',str(mid_percent68))
        st.write('2σ:',str(mid_percent95))
        st.write('3σ:',str(mid_percent99))
        st.write('現在の乖離率中期',str(today_mid))

    with col3:
        st.subheader('<長期>')
        st.write('σ:',str(long_percent68))
        st.write('2σ:',str(long_percent95))
        st.write('3σ:',str(long_percent99))
        st.write('現在の乖離率長期',str(today_long))

                     

    st.subheader('<データ一覧>')
    st.table(info)


    df2 = pd.DataFrame(get_kessan(option))
    st.subheader('<決算情報>')
    st.table(df2)

    # 各列に対して、trim_cammaを適用する(決算)
    new_df2 = df2.copy()
    for col in df2.columns:
        new_df2[col] = df2[col].map(lambda v : trim_camma_kessan(v))
    #利益率の
    x = ["3years before", "2years before", "1year before", "latest"]
    x = pd.DataFrame(x)
    sales = [int(new_df2["売上高"][3]), int(new_df2["売上高"][2]), int(new_df2["売上高"][1]), int(new_df2["売上高"][0])]
    sales_data = pd.DataFrame(sales)
    profit = [int(new_df2["営業利益"][3]), int(new_df2["営業利益"][2]), int(new_df2["営業利益"][1]), int(new_df2["営業利益"][0])]
    profit_data = pd.DataFrame(profit)
    profit2 = [int(new_df2["経常利益"][3]), int(new_df2["経常利益"][2]), int(new_df2["経常利益"][1]), int(new_df2["経常利益"][0])]
    profit2_data = pd.DataFrame(profit2)
    
    # 年度データ
    years = ['2020', '2021', '2022', '2023']


    # グラフの作成
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # 売上高のグラフ
    axes[0].plot(years, sales, marker='o', linestyle='-', color='b')
    axes[0].set_title('Revenue')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Revenue')

    # 営業利益のグラフ
    axes[1].plot(years, profit, marker='o', linestyle='-', color='g')
    axes[1].set_title('Operating Income')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Operating Income')

    # 経常利益のグラフ
    axes[2].plot(years, profit2, marker='o', linestyle='-', color='r')
    axes[2].set_title('Ordinary Income')
    axes[2].set_xlabel('Year')
    axes[2].set_ylabel('Ordinary Income')

    # グラフの間のスペース調整
    plt.tight_layout()
    
    
    st.pyplot(fig)
    
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
            
            #移動平均
            span01=5
            span02=25
            span03=50
    
            source['sma01'] = price.rolling(window=span01).mean()
            source['sma02'] = price.rolling(window=span02).mean()
            source['sma03'] = price.rolling(window=span03).mean()
    
            # 移動平均線乖離率
            source["SMA5_乖離率"] = (source["Close"] - source["sma01"]) / source["sma01"] * 100
            source["SMA25_乖離率"] = (source["Close"] - source["sma02"]) / source["sma02"] * 100
            source["SMA50_乖離率"] = (source["Close"] - source["sma03"]) / source["sma03"] * 100
            
            # 今日の乖離率
            last = 999
            today_short = (source["Close"][last] - source["sma01"][last]) / source["sma01"][last] * 100
            today_mid = (source["Close"][last] - source["sma02"][last]) / source["sma02"][last] * 100
            today_long = (source["Close"][last] - source["sma03"][last]) / source["sma03"][last] * 100
            info = source[["SMA5_乖離率", "SMA25_乖離率", "SMA50_乖離率"]].describe().round(2)
            short_percent68 = float(info["SMA5_乖離率"][1]) - float(info["SMA5_乖離率"][2]) 
            short_percent95 = float(info["SMA5_乖離率"][1]) - float(info["SMA5_乖離率"][2]) *2
            short_percent99 = float(info["SMA5_乖離率"][1]) - float(info["SMA5_乖離率"][2]) *3
    
            mid_percent68 = float(info["SMA25_乖離率"][1]) - float(info["SMA25_乖離率"][2]) 
            mid_percent95 = float(info["SMA25_乖離率"][1]) - float(info["SMA25_乖離率"][2]) *2
            mid_percent99 = float(info["SMA25_乖離率"][1]) - float(info["SMA25_乖離率"][2]) *3
    
            long_percent68 = float(info["SMA50_乖離率"][1]) - float(info["SMA50_乖離率"][2]) 
            long_percent95 = float(info["SMA50_乖離率"][1]) - float(info["SMA50_乖離率"][2]) *2
            long_percent99 = float(info["SMA50_乖離率"][1]) - float(info["SMA50_乖離率"][2]) *3
            
            if today_mid<mid_percent68:
                st.write('68%:',code)
                
            if today_mid<mid_percent95:
                st.write('95%:',code)
            
            
        
    
