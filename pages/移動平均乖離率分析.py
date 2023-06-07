import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")

st.title("移動平均乖離率分析")

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
    
    #利益率の
    x = ["3years before", "2years before", "1year before", "latest"]
    sales = [df2["売上高"][0], df2["売上高"][1], df2["売上高"][2], df2["売上高"][3]]
    profit = [df2["営業利益"][0], df2["営業利益"][1], df2["営業利益"][2], df2["営業利益"][3]]
    profit2 = [df2["経常利益"][0], df2["経常利益"][1], df2["経常利益"][2], df2["経常利益"][3]]
#     fig2, ax = plt.subplots()

#     ax.bar(x, profit)
#     st.pyplot(fig2)
    
#     fig3, ax2 = plt.subplots()

#     ax2.bar(x, profit2)
#     st.pyplot(fig3)

    fig2, ax = plt.subplots(1, 3, figsize=(15, 5))

    sns.barplot(df2["売上高"], ax=ax[0])
    sns.barplot(df2["営業利益"], ax=ax[1])
    sns.barplot(df2["経常利益"], ax=ax[2])
    st.pyplot(fig2)
    
