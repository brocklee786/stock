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
    st.write(source["Close"][last])
    st.write(source["sma02"][last])
    st.write(source["sma02"])
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
    for code in codes1_3:
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
        
        
        
    
