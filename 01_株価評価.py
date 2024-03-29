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



st.set_page_config(layout="wide")

st.title('株価評価')


option = st.text_input('銘柄コードを入力してください')
 

def get_basic_info(option):
    ticker = str(option)
    url = "https://minkabu.jp/stock/" + ticker
    html = requests.get(url)
 
    soup = BeautifulSoup(html.content, "html.parser")
 
    basic_info = {}
    tr_all = soup.find_all('tr')
    for tr in tr_all:
        th = tr.find('th')
        if th is None:
            continue
       
        td = tr.find('td')
   
        key = th.text
        value = td.text
   
        basic_info[key] = value
    print(basic_info)
    return(basic_info)
   
def get_company_info(option):

    ticker = str(option)
    url = "https://minkabu.jp/stock/" + ticker + "/fundamental"
    html = requests.get(url)
    soup = BeautifulSoup(html.content,"html.parser")

    basic_info2 = {}
    dl_all = soup.find_all("dl",{"class":"md_dataList"})

    for i in range(len(dl_all)):
        dt = dl_all[i].find_all("dt")  
        dd = dl_all[i].find_all("dd")
        for i,j in zip(dt,dd):
            soup1 = BeautifulSoup(str(i),"lxml")
            soup2 = BeautifulSoup(str(j),"lxml")
            text1 = soup1.get_text()
            text2 = soup2.get_text()
            basic_info2[text1] = text2

    return(basic_info2)
   
 # 単位を削除する関数
def trim_unit(x):
   
    # 単位=円を削除
    yen_re = re.search(r"([+-]?\d{1,3}(,\d{3})*\.\d+)円", x)
    if yen_re:
        value = yen_re.group(1)
        value = value.replace(',', '')
 
        return value
   
    # 単位=%を削除
    perc_re = re.search(r"(\d+\.\d+)%", x)
    if perc_re:
        value = perc_re.group(1)
        return np.float64(value)
   
    # 単位=株を削除
    stock_re = re.search(r"(\d{1,3}(,\d{3})*)株", x)
    if stock_re:
        value = stock_re.group(1)
        value = value.replace(',', '')
        return np.int64(value)
   
    # 単位=倍を削除
    times_re = re.search(r"(\d+\.\d+)倍", x)
    if times_re:
        value = times_re.group(1)
        return np.float64(value)
   
    # 単位=百万円を削除
    million_yen_re = re.search(r"(\d{1,3}(,\d{3})*)百万円", x)
    if million_yen_re:
        value = million_yen_re.group(1)
        value = value.replace(',', '')
        value = np.int64(value) * 1000000
        return value
   
    # 単位=千株を削除
    thousand_stock_re = re.search(r"(\d{1,3}(,\d{3})*)千株", x)
    if thousand_stock_re:
        value = thousand_stock_re.group(1)
        value = value.replace(',', '')
        value = np.int64(value) * 1000
        return value
   
    return x
 
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
 
#財務情報を取得
def get_zaimu(option):
    # 指定URLのHTMLデータを取得
    code = int(option)
    url = "https://minkabu.jp/stock/{0:d}/settlement".format(code)
    html = requests.get(url)
    # BeautifulSoupのHTMLパーサーを生成
    soup = BeautifulSoup(html.content, "html.parser")
 
    # 全<table>要素を抽出
    table_all = soup.find_all('table')
 
    # 財務情報の<table>要素を検索する。
    fin_table1 = None
    for table in table_all:
   
        # <caption>要素を取得
        caption = table.find('caption')
        if caption is None:
            continue
   
        # <caption>要素の文字列が目的のものと一致したら終了
        if caption.text == '財務情報':
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
    df3 = pd.DataFrame(rows, columns=headers)
 
    # 先頭の列(決算期)をインデックスに指定する
    df3 = df3.set_index(headers[0])
    return(df3)

def get_cashflow(option):
    # 指定URLのHTMLデータを取得
    code = int(option)
    url = "https://minkabu.jp/stock/{0:d}/settlement".format(code)
    html = requests.get(url)
    # BeautifulSoupのHTMLパーサーを生成
    soup = BeautifulSoup(html.content, "html.parser")
 
    # 全<table>要素を抽出
    table_all = soup.find_all('table')
 
    # キャッシュフロー情報の<table>要素を検索する。
    fin_table1 = table_all[4]
 
    # <table>要素内のヘッダ情報を取得する。
    headers = []
    thead_th = fin_table1.find('thead').find_all('th')
    for th in thead_th:
        headers.append(th.text)
 
    # <table>要素内のデータを取得する。
    rows = []
    tbody_tr = fin_table1.find('tbody').find_all('tr')
 
    for tr in tbody_tr:
 
 
        # <tr>要素内の<th>要素を取得する。
        th = tr.find('th')
 
        # 1行内のデータを格納するためのリスト
        row = []
 
        row.append(th.text)
 
        # <tr>要素内の<td>要素を取得する。
        td_all = tr.find_all('td')
        for td in td_all:
            row.append(td.text)
 
        # 1行のデータを格納したリストを、リストに格納
        rows.append(row)
 
    rows.pop(0)
 
 
    # DataFrameを生成する
    df4 = pd.DataFrame(rows, columns=headers)
 
    # 先頭の列(決算期)をインデックスに指定する
    df4 = df4.set_index(headers[0])
    
   
    return(df4)

# 数値のカンマを削除する関数
def trim_camma_kessan(x):
    # 2,946,639.3のようなカンマ区切り、小数点有りの数値か否か確認する
    comma_re = re.search(r"(\d{1,3}(,\d{3})*(\.\d+){0,1})", x)
    if comma_re:
        value = comma_re.group(1)
        value = value.replace(',', '') # カンマを削除
        return value
   
    return x
 
def plot_polar(labels, values, imgname):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # 軸ラベル
    ax.set_rlim(0 ,10)
    fig.savefig(imgname)
    plt.close(fig)
    
def trim_camma_cashflow(x):
    y = x.replace(',','')
    return y

 
 
if option:
    ticker_dict = get_basic_info(option)
    company_info = get_company_info(option)
    df = pd.DataFrame.from_dict([ticker_dict])
    df2 = pd.DataFrame(get_kessan(option))
    df3 = pd.DataFrame(get_zaimu(option))
    df4 = pd.DataFrame(get_cashflow(option))
   
 
 
    st.write('<span style="color:red">基本情報</span>',
              unsafe_allow_html=True)
    st.table(df)
    st.write('<span style="color:red">決算情報</span>',
              unsafe_allow_html=True)
    st.table(df2)
    st.write('<span style="color:red">財務情報</span>',
              unsafe_allow_html=True)
    st.table(df3)
    st.write('<span style="color:red">キャッシュフロー</span>',
              unsafe_allow_html=True)
    st.table(df4)
    
 
    # 各列に対して、trim_unitを適用する
    new_df = df.copy()
    for col in new_df.columns:
        new_df[col] = new_df[col].map(lambda v : trim_unit(v))
 
   
    #st.table(new_df)
 
    #データフレームから辞書型にして使えるように変更
    dict = new_df.to_dict()
   
    # 各列に対して、trim_cammaを適用する(決算)
    new_df2 = df2.copy()
    for col in df2.columns:
        new_df2[col] = df2[col].map(lambda v : trim_camma_kessan(v))
 
    #st.table(new_df2)
 
    # 各列に対して、trim_cammaを適用する(財務)
    new_df3 = df3.copy()
    for col in df3.columns:
        new_df3[col] = df3[col].map(lambda v : trim_camma_kessan(v))
 
    #st.table(new_df3)
    # 各列に対して、trim_cammaを適用する(キャッシュフロー)
    new_df4 = df4.copy()
    for col in df4.columns:
        new_df4[col] = df4[col].map(lambda v : trim_camma_cashflow(v))

    
 
 
    #stock_value = st.text_input('現在の株価を入力してください')
   
    #データを数値に変換
    num_PER = float(new_df['PER(調整後)'][0])
    num_PSR = float(new_df['PSR'][0])
    num_PBR = float(new_df['PBR'][0])
    num_profit = float(new_df2['純利益'][0]) * 1000000
    num_asset = float(new_df3['総資産'][0]) * 1000000
    num_capital_ratio_percent = float(new_df3['自己資本率'][0])
    num_capital_ratio = float(new_df3['自己資本率'][0]) / 100
    num_BPS = float(new_df3['1株純資産'][0])
    num_EPS = (float(new_df2['純利益'][0]) / float(new_df['発行済株数'][0])) * 1000000
    #それぞれのデータ
    #if stock_value:
        #num_stock_value = int(stock_value)
        #データの整理
    EPS = num_EPS
    PSR = num_PSR
    PBR = num_PBR
    BPS = num_BPS
    ROA = (num_profit / num_asset)
    if ROA >= 0.3:
        ROA = 0.3
    PER = num_PER
 
 
    #割引率の計算
    if num_capital_ratio_percent >= 80:
        discount = 0.8
    elif 80 > num_capital_ratio_percent >=67:
        discount = 0.75
    elif 67> num_capital_ratio_percent >= 50:
        discount = 0.7
    elif 50 > num_capital_ratio_percent >= 33:
        discount = 0.65
    elif 33 > num_capital_ratio_percent >= 10:
        discount = 0.6
    else:
        discount = 0.5
 
    #財務レバレッジ補正
    financial_leverage_correction = 1 / (num_capital_ratio + 0.33)
 
    #リスク評価率
    if PBR >= 0.5:
        risk = 1
    elif 0.5 > PBR >=0.41:
        risk = 0.8
    elif 0.41 > PBR >= 0.34:
        risk = 0.66
    elif 0.34 > PBR >= 0.25:
        risk = 0.5
    elif 0.25 > PBR >= 0.21:
        risk = 0.33
    elif 0.2 > PBR >= 0.04:
        risk = (PBR / 5 * 50) + 50
    else:
        risk = (PBR-1) * 10 +5
 
   
    #資産価値
    asset_value = BPS * discount
    int_asset_value = int(asset_value)
    #事業価値
    business_value = EPS * ROA * 150 * financial_leverage_correction
    int_business_value = int(business_value)
    #理論株価
    theoretical_stock_price = (asset_value + business_value) * risk
    int_theoretical_stock_price = int(theoretical_stock_price)
    #上限株価
    max_stock_price = asset_value + (business_value * 2)
    int_max_stock_price = int(max_stock_price)
    
    stock_value = new_df['時価総額'][0] / new_df['発行済株数'][0]
    
    st.sidebar.write('<span style="color:red">社名</span>',
              unsafe_allow_html=True)
    st.sidebar.write(company_info["社名"])
    st.sidebar.write('<span style="color:red">業種</span>',
              unsafe_allow_html=True)
    st.sidebar.write(company_info["業種"])
    st.sidebar.write('<span style="color:red">現在株価</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(stock_value) + '円')
    st.sidebar.write('<span style="color:red">資産価値</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(int_asset_value) + '円')
    st.sidebar.write('<span style="color:red">事業価値</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(int_business_value) + '円')
    st.sidebar.write('<span style="color:red">理論株価1</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(int_theoretical_stock_price) + '円')
    st.sidebar.write('<span style="color:red">理論株価2</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(EPS*PER) + '円')
    st.sidebar.write('<span style="color:red">理論株価3</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(EPS*10 + BPS) + '円')
    st.sidebar.write('<span style="color:red">上限株価</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(int_max_stock_price) + '円')
    st.sidebar.write('<span style="color:red">EPS</span>',
              unsafe_allow_html=True)
    st.sidebar.write(EPS)
    st.sidebar.write('<span style="color:red">PSR</span>',
              unsafe_allow_html=True)
    st.sidebar.write(PSR)
    st.sidebar.write('<span style="color:red">BPS</span>',
              unsafe_allow_html=True)
    st.sidebar.write(BPS)
    st.sidebar.write('<span style="color:red">PBR</span>',
              unsafe_allow_html=True)
    st.sidebar.write(PBR)
    sales = int(new_df4['営業CF'][0])
    investment = int(new_df4['投資CF'][0])
    finance = int(new_df4['財務CF'][0])
    company = 0
    
    #営業CFがプラスかマイナスかを判断する。
    if sales >= 0:
        if investment >= 0:
            if finance >= 0:
                company = 1
 
            else:
                company = 2
        else:
            if finance >= 0:
                company = 3
            else:
                company = 7
    else:
        if investment >= 0:
            if finance >= 0:
                company = 4
            else:
                company = 4
        else:
            if finance >= 0:
                company = 5
            else:
                company = 6
 
    if company == 1:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('事業転換中の企業？')  
    if company == 2:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('事業縮小中の企業？')   
    if company == 3:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('成長企業？')   
    if company == 4:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('やや要注意な企業？')   
    if company == 5:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('再建中の企業？')   
    if company == 6:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('事業見直しの企業？')   
    if company == 7:
        st.sidebar.write('<span style="color:red">キャッシュフローによる健全性評価</span>',
              unsafe_allow_html=True)
        st.sidebar.write('優良企業？') 
        
    #理論株価と株価の関係性のグラフ

    tkr = yf.Ticker(str(option) + '.T')
    hist = tkr.history(period='max')
    

    #BPS
    BPS_now = float(new_df3['1株純資産'][0])
    BPS2 = float(new_df3['1株純資産'][1])
    BPS3 = float(new_df3['1株純資産'][2])
    BPS4 = float(new_df3['1株純資産'][3])

    #st.write(BPS2)

    #発行株式数
    number_of_stock = float(new_df3['純資産'][0]) / float(new_df3['1株純資産'][0]) * 1000000
    number_of_stock2 = float(new_df3['純資産'][1]) / float(new_df3['1株純資産'][1]) * 1000000
    number_of_stock3 = float(new_df3['純資産'][2]) / float(new_df3['1株純資産'][2]) * 1000000
    number_of_stock4 = float(new_df3['純資産'][3]) / float(new_df3['1株純資産'][3]) * 1000000

    #st.write(number_of_stock)

    #EPS
    EPS_now = float(new_df2['純利益'][0]) / number_of_stock * 1000000
    EPS2 = float(new_df2['純利益'][1]) / number_of_stock * 1000000
    EPS3 = float(new_df2['純利益'][2]) / number_of_stock * 1000000
    EPS4 = float(new_df2['純利益'][3]) / number_of_stock * 1000000

    #st.write(EPS_now)
    
    #ROA
    ROA_now = float(new_df2['純利益'][0]) / float(new_df3['純資産'][0]) * 100
    ROA2 = float(new_df2['純利益'][1]) / float(new_df3['純資産'][1]) 
    if ROA2 >= 0.3:
        ROA2 = 0.3
    ROA3 = float(new_df2['純利益'][2]) / float(new_df3['純資産'][2])
    if ROA3 >= 0.3:
        ROA3 = 0.3
    ROA4 = float(new_df2['純利益'][3]) / float(new_df3['純資産'][3]) 
    if ROA4 >= 0.3:
        ROA4 = 0.3
 
    #st.write(ROA_now)

    #株価
    stockprice = hist['Close']['2022-05-12T00:00:00']
    stockprice2 = hist['Close']['2021-05-12T00:00:00']
    stockprice3 = hist['Close']['2020-05-12T00:00:00']
    stockprice4 = hist['Close']['2019-05-15T00:00:00']

    #st.write(stockprice2)

    #自己資本比率
    zikoshihon_now = float(new_df3['自己資本率'][0])
    zikoshihon2 = float(new_df3['自己資本率'][1])
    zikoshihon3 = float(new_df3['自己資本率'][2])
    zikoshihon4 = float(new_df3['自己資本率'][3])

    #st.write(zikoshihon4)

    #PBR
    PBR_now = stockprice / BPS_now
    PBR2 = stockprice / BPS2
    PBR3 = stockprice / BPS3
    PBR4 = stockprice / BPS4

    #st.write(PBR_now)
    
    #割引率の計算
    if zikoshihon2 >= 80:
        discount2 = 0.8
    elif 80 > zikoshihon2 >=67:
        discount2 = 0.75
    elif 67> zikoshihon2 >= 50:
        discount2 = 0.7
    elif 50 > zikoshihon2 >= 33:
        discount2 = 0.65
    elif 33 > zikoshihon2 >= 10:
        discount2 = 0.6
    else:
        discount2 = 0.5

    if zikoshihon3 >= 80:
        discount3 = 0.8
    elif 80 > zikoshihon3 >=67:
        discount3 = 0.75
    elif 67> zikoshihon3 >= 50:
        discount3 = 0.7
    elif 50 > zikoshihon3 >= 33:
        discount3 = 0.65
    elif 33 > zikoshihon3 >= 10:
        discount3 = 0.6
    else:
        discount3 = 0.5

    if zikoshihon4 >= 80:
        discount4 = 0.8
    elif 80 > zikoshihon4 >=67:
        discount4 = 0.75
    elif 67> zikoshihon4 >= 50:
        discount4 = 0.7
    elif 50 > zikoshihon4 >= 33:
        discount4 = 0.65
    elif 33 > zikoshihon4 >= 10:
        discount4 = 0.6
    else:
        discount4 = 0.5
 
    #財務レバレッジ補正
    financial_leverage_correction2 = 1 / ((zikoshihon2 / 100) + 0.33)
    financial_leverage_correction3 = 1 / ((zikoshihon3 / 100) + 0.33)
    financial_leverage_correction4 = 1 / ((zikoshihon4 / 100) + 0.33)
 
    #リスク評価率
    if PBR2 >= 0.5:
        risk2 = 1
    elif 0.5 > PBR2 >=0.41:
        risk2 = 0.8
    elif 0.41 > PBR2 >= 0.34:
        risk2 = 0.66
    elif 0.34 > PBR2 >= 0.25:
        risk2 = 0.5
    elif 0.25 > PBR2 >= 0.21:
        risk2 = 0.33
    elif 0.2 > PBR2 >= 0.04:
        risk2 = (PBR2 / 5 * 50) + 50
    else:
        risk2 = (PBR2 - 1) * 10 + 5
 
    if PBR3 >= 0.5:
        risk3 = 1
    elif 0.5 > PBR3 >=0.41:
        risk3 = 0.8
    elif 0.41 > PBR3 >= 0.34:
        risk3 = 0.66
    elif 0.34 > PBR3 >= 0.25:
        risk3 = 0.5
    elif 0.25 > PBR3 >= 0.21:
        risk3 = 0.33
    elif 0.2 > PBR3 >= 0.04:
        risk3 = (PBR3 / 5 * 50) + 50
    else:
        risk3 = (PBR3 - 1) * 10 + 5

    if PBR4 >= 0.5:
        risk4 = 1
    elif 0.5 > PBR4 >=0.41:
        risk4 = 0.8
    elif 0.41 > PBR4 >= 0.34:
        risk4 = 0.66
    elif 0.34 > PBR4 >= 0.25:
        risk4 = 0.5
    elif 0.25 > PBR4 >= 0.21:
        risk4 = 0.33
    elif 0.2 > PBR4 >= 0.04:
        risk4 = (PBR4 / 5 * 50) + 50
    else:
        risk4 = (PBR4 - 1) * 10 + 5
   
    #資産価値
    asset_value2 = BPS2 * discount2
    asset_value3 = BPS3 * discount3
    asset_value4 = BPS4 * discount4
    int_asset_value2 = int(asset_value2)
    int_asset_value3 = int(asset_value3)
    int_asset_value4 = int(asset_value4)

    #事業価値
    business_value2 = EPS2 * ROA2 * 150 * financial_leverage_correction2
    business_value3 = EPS3 * ROA3 * 150 * financial_leverage_correction3
    business_value4 = EPS4 * ROA4 * 150 * financial_leverage_correction4
    int_business_value2 = int(business_value2)
    int_business_value3 = int(business_value3)
    int_business_value4 = int(business_value4)

    #理論株価
    theoretical_stock_price2 = (asset_value2 + business_value2) * risk2
    theoretical_stock_price3 = (asset_value3 + business_value3) * risk3
    theoretical_stock_price4 = (asset_value4 + business_value4) * risk4
    int_theoretical_stock_price2 = int(theoretical_stock_price2)
    int_theoretical_stock_price3 = int(theoretical_stock_price3)
    int_theoretical_stock_price4 = int(theoretical_stock_price4)
    #上限株価
    max_stock_price2 = asset_value2 + (business_value2 * 2)
    max_stock_price3 = asset_value3 + (business_value3 * 2)
    max_stock_price4 = asset_value4 + (business_value4 * 2)
    int_max_stock_price2 = int(max_stock_price2)
    int_max_stock_price3 = int(max_stock_price3)
    int_max_stock_price4 = int(max_stock_price4)

    stockvalue = [{'2022': int(stock_value), '2021': int(stockprice2), '2020': int(stockprice3), '2019': int(stockprice4)}]
    stockvalue_data = pd.DataFrame(stockvalue)
    st.write('<span style="color:red">株価推移</span>',
              unsafe_allow_html=True)
    st.table(stockvalue_data)
    
    theoretical = [{'2022':int_theoretical_stock_price, '2021': int_theoretical_stock_price2, '2020': int_theoretical_stock_price3, '2019': int_theoretical_stock_price4}]
    theoretical_data = pd.DataFrame(theoretical)
    st.write('<span style="color:red">理論株価推移</span>',
              unsafe_allow_html=True)
    st.table(theoretical_data)
    
    max_theoretical = [{'2022':int_max_stock_price, '2021': int_max_stock_price2, '2020': int_max_stock_price3, '2019': int_max_stock_price4}]
    max_theoretical_data = pd.DataFrame(max_theoretical)
    st.write('<span style="color:red">上限株価推移</span>',
              unsafe_allow_html=True)
    st.table(max_theoretical_data)
    
    st.sidebar.write('表示日数を指定して下さい')
    days = st.sidebar.slider('日数', 1, 1460, 300)
    
    tkr = yf.Ticker(str(option) + '.T')
    hist = tkr.history(period=f'{days}d')
    hist = hist.reset_index()
    hist = hist.set_index(['Date'])
    hist = hist.rename_axis('Date').reset_index()
    hist = hist.T
    a = hist.to_dict()
    # a
    # pd.DataFrame(a)


    for items in a.values():
        time = items['Date']
        items['Date'] = time.strftime("%Y/%m/%d")

    b = [x for x in a.values()]

    source = pd.DataFrame(b)

    price = source['Close']
    

    #移動平均
    #移動平均
    span01=5
    span02=25
    span03=50

    source['sma01'] = price.rolling(window=span01).mean()
    source['sma02'] = price.rolling(window=span02).mean()
    source['sma03'] = price.rolling(window=span03).mean()

   
    
    
    
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
    
    open_close_color = alt.condition("datum.Open <= datum.Close",
                                     alt.value("#06982d"),
                                     alt.value("#ae1325"))

    ave1_color = alt.value("#1f77b4")
    ave2_color = alt.value("#d62728")
    ave3_color = alt.value("#7f7f7f")

    base = alt.Chart(source).encode(
         alt.X('Date:T',
              axis=alt.Axis(
                  format='%y/%m/%d',
                  labelAngle=-45,
                  title='Date'
              )
        ),
        color=open_close_color
    ).properties(height=600)

    rule = base.mark_rule().encode(
        alt.Y(
            'Low:Q',
            title='Price',
            scale=alt.Scale(zero=False),
        ),
        alt.Y2('High:Q')
    ).interactive().properties(height=600)

    bar = base.mark_bar().encode(
        alt.Y('Open:Q'),
        alt.Y2('Close:Q')
    ).interactive().properties(height=600)

    average1 = base.mark_line(opacity=0.8, clip=True).encode(
            alt.Y("sma01:Q", stack=None, scale=alt.Scale(zero=False)),
            color=ave1_color
    ).interactive().properties(height=600)

    average2 = base.mark_line(opacity=0.8, clip=True).encode(
            alt.Y("sma02:Q", stack=None, scale=alt.Scale(zero=False)),
            color=ave2_color
    ).interactive().properties(height=600)

    average3 = base.mark_line(opacity=0.8, clip=True).encode(
            alt.Y("sma03:Q", stack=None, scale=alt.Scale(zero=False)),
            color=ave3_color
    ).interactive().properties(height=600)

    

    st.altair_chart(rule + bar + average1 + average2 + average3 , use_container_width=True)

    

    
    
    base3 = alt.Chart(source).mark_line().encode(
         alt.X('Date:T',
              axis=alt.Axis(
                  format='%y/%m/%d',
                  labelAngle=-45,
                  title='Date'
              )
        ),
        alt.Y('RSI:Q',
             axis=alt.Axis(
                  title='RSI'
              ))
        
    ).interactive()
    
    st.altair_chart(base3, use_container_width=True)
    days = st.selectbox(
        '何日間表示しますか？',
        (50,100,150,200,300))

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


    ## チャートを単回帰分析し、得られる単回帰直線よりも上（下）の値だけで再度単回帰分析...
    ## これを繰り返し、高値（安値）を2～3点に絞り込む

    # 高値の始点/支点を取得
    def get_highpoint(start, end):
        chart = source[start:end+1]
        while len(chart)>3:
            regression = linregress(
                x = chart['time_id'],
                y = chart['High'],
            )
            chart = chart.loc[chart['High'] > regression[0] * chart['time_id'] + regression[1]]
        return chart

    # 安値の始点/支点を取得
    def get_lowpoint(start, end):
        chart = source[start:end+1]
        while len(chart)>3:
            regression = linregress(
                x = chart['time_id'],
                y = chart['Low'],
            )
            chart = chart.loc[chart['Low'] < regression[0] * chart['time_id'] + regression[1]]
        return chart

    def g_trendlines(span=20, min_interval=3):
        trendlines = []

        # 高値の下降トレンドラインを生成
        for i in source.index[::10]:
            highpoint = get_highpoint(i, i + span)
            # ポイントが2箇所未満だとエラーになるので回避する
            if len(highpoint) < 2:
                continue
            # 始点と支点が近過ぎたらトレンドラインとして引かない
            if abs(highpoint.index[0] - highpoint.index[1]) < min_interval:
                continue
            regression = linregress(
                x = highpoint['time_id'],
                y = highpoint['High'],
            )
            print(regression[0] < 0.0, 'reg_high: ', regression[0], ', ', regression[1], )

            # 下降してるときだけ
            if regression[0] < 0.0:
                trendlines.append(regression[0] * source['time_id'][i:i+span*2] + regression[1])

        # 安値の上昇トレンドラインを生成
        for i in source.index[::10]:
            lowpoint   = get_lowpoint(i, i + span)
            # ポイントが2箇所未満だとエラーになるので回避する
            if len(lowpoint) < 2:
                continue
            # 始点と支点が近過ぎたらトレンドラインとして引かない
            if abs(lowpoint.index[0] - lowpoint.index[1]) < min_interval:
                continue
            regression = linregress(
                x = lowpoint['time_id'],
                y = lowpoint['Low'],
            )
            print(regression[0] > 0.0, 'reg_low: ', regression[0], ', ', regression[1], )

            # 上昇してるときだけ
            if regression[0] > 0.0:
                trendlines.append(regression[0] * source['time_id'][i:i+span*2] + regression[1])

        return trendlines


    figure, axis1 = plt.subplots(figsize=(15,7))

    # ローソク足
    mpf.candlestick2_ohlc(
        axis1,
        opens  = source.Open.values,
        highs  = source.High.values,
        lows   = source.Low.values,
        closes = source.Close.values,
        width=0.6, colorup='#77d879', colordown='#db3f3f'
    )

    # トレンドラインたちを引く
    for i, line in enumerate(g_trendlines()):
        axis1.plot(line, label=i)

    # X軸の見た目を整える
    xticks_number  = 12 # 12本刻みに目盛りを書く
    xticks_index   = range(0, len(source), xticks_number)


    # axis1を装飾 ( plt.sca(axis): set current axis )
    plt.sca(axis1)

    plt.legend()
    st.pyplot(figure,use_container_width=True)
   
   
 
    stock_value = new_df['時価総額'][0] / new_df['発行済株数'][0]
 
 
    #target_per = st.text_input('実績PER高値平均を入力してください')
    target_per2 = 0
    ave_profit = 0
    #num_target_profit = float(target_per)
    past_profit = new_df2["営業利益"][0]
    if past_profit:
        num_past_profit = int(past_profit)
        now_profit = st.text_input('今期の営業利益を入力してください')
        future_profit = st.text_input('来期の予想営業利益を入力してください')
        profit_stock_now = st.text_input('今期の1株益を入力してください')
        profit_stock_future = st.text_input('来期の1株益を入力してください')
        sales_amount = st.text_input('今期の売上高予想を入力してください')
        if now_profit:
            num_now_profit = int(now_profit)
            
            if future_profit:
                num_future_profit = int(future_profit)
                ave_growth = ((num_now_profit - num_past_profit)/num_past_profit + (num_future_profit - num_now_profit)/num_now_profit) / 2
                ave_growth_percent = ave_growth * 100
                sale_growth_rule = ((num_now_profit - num_past_profit)/num_past_profit) * 100
                profit_rate = float(new_df2['営業利益'][0]) / float(new_df2['売上高'][0]) * 100
                if 0 < ave_growth <= 0.075:
                    target_per2 = 15.75
                elif 0.075 < ave_growth <= 0.125:
                    target_per2 = 16.5
                elif 0.125 < ave_growth <= 0.175:
                    target_per2 = 17.3
                elif 0.175 < ave_growth <= 0.225:
                    target_per2 = 18
                elif 0.225 < ave_growth <= 0.275:
                    target_per2 = 18.8
                elif 0.275 < ave_growth <= 0.325:
                    target_per2 = 19.5
                elif 0.325 < ave_growth <= 0.375:
                    target_per2 = 20.3
                elif 0.375 < ave_growth <= 0.45:
                    target_per2 = 21
                elif 0.45 < ave_growth <= 0.55:
                    target_per2 = 22.5
                elif 0.55 < ave_growth <= 0.65:
                    target_per2 = 24
                else:
                    target_per2 = 25.5


                
                if profit_stock_now:
                    num_profit_stock_now = float(profit_stock_now)
                    
                    if profit_stock_future:
                        num_profit_stock_future = float(profit_stock_future)
                        ave_profit = (num_profit_stock_now + num_profit_stock_future) / 2













                        #st.sidebar.write('<span style="color:red">目標PER1</span>',
                                            #unsafe_allow_html=True)
                        #st.sidebar.write(str(target_per))


                        #st.sidebar.write('<span style="color:red">目標PER2</span>',
                                            #unsafe_allow_html=True)
                        #st.sidebar.write(str(target_per2))


                        st.sidebar.write('<span style="color:red">1年後の目標株価</span>',
                                        unsafe_allow_html=True)
                        st.sidebar.write(str(target_per2 * ave_profit) + '円')

                        company_value = new_df['時価総額'][0]
                        #PSR = int(company_value) / int(new_df2['売上高'][0])

                        
                        if sales_amount:
                            profit_increase_rate = float(sales_amount) / float(new_df2['売上高'][0])
                            rule = int(sale_growth_rule) + int(profit_rate)
                            sales_growth = ((int(sales_amount) - int(new_df2['売上高'][0])) / int(new_df2['売上高'][0])) * 100
                            stock_profit_growth = ((float(profit_stock_future) - float(profit_stock_now)) / float(profit_stock_now)) * 100

                            sales_point = 0
                            share_point = 0
                            profit_point = 0
                            growth_point = 0

                            if  ave_growth_percent <= -30:
                                share_point = 1
                            elif  -30 < ave_growth_percent <= -20:
                                share_point = 2
                            elif  -20 < ave_growth_percent <= -10:
                                share_point = 3
                            elif -10 < ave_growth_percent <= -5:
                                share_point = 4
                            elif  -5 < ave_growth_percent <= 0:
                                share_point = 5
                            elif  0 < ave_growth_percent <= 5:
                                share_point = 6
                            elif  5 < ave_growth_percent <= 10:
                                share_point = 7
                            elif 10 < ave_growth_percent <= 20:
                                share_point = 8
                            elif 20 < ave_growth_percent <= 30:
                                share_point = 9
                            else:
                                share_point = 10

                            if   sales_growth <= -30:
                                sales_point = 1
                            elif  -30 < sales_growth <= -20:
                                sales_point = 2
                            elif  -20 < sales_growth <= -10:
                                sales_point = 3
                            elif -10 < sales_growth <= -5:
                                sales_point = 4
                            elif -5 < sales_growth <= 0:
                                sales_point = 5
                            elif   0 < sales_growth <= 5:
                                sales_point = 6
                            elif  5 < sales_growth <= 10:
                                sales_point = 7
                            elif  10 < sales_growth <= 20:
                                sales_point = 8
                            elif 20 < sales_growth <= 30:
                                sales_point = 9
                            else:
                                sales_point = 10


                            if   stock_profit_growth <= -30:
                                profit_point = 1
                            elif  -30 < stock_profit_growth <= -20:
                                profit_point = 2
                            elif  -20 < stock_profit_growth <= -10:
                                profit_point = 3
                            elif -10 < stock_profit_growth <= -5:
                                profit_point = 4
                            elif -5 < stock_profit_growth <= 0:
                                profit_point = 5
                            elif   0 < stock_profit_growth <= 5:
                                profit_point = 6
                            elif  5 < stock_profit_growth <= 10:
                                profit_point = 7
                            elif  10 < stock_profit_growth <= 20:
                                profit_point = 8
                            elif 20 < stock_profit_growth <= 30:
                                profit_point = 9
                            else:
                                profit_point = 10


                            growth_point = (share_point + sales_point + profit_point) / 3

                            

                            if   profit_rate <= 0:
                                profit_rate_point = 1
                            elif  0 < profit_rate <= 1.5:
                                profit_rate_point = 2
                            elif  1.5 < profit_rate <= 3:
                                profit_rate_point = 3
                            elif 3 < profit_rate <= 5:
                                profit_rate_point = 4
                            elif 5 < profit_rate <= 7.5:
                                profit_rate_point = 5
                            elif 7.5 < profit_rate <= 10:
                                profit_rate_point = 6
                            elif 10 < profit_rate <= 15:
                                profit_rate_point = 7
                            elif 15 < profit_rate <= 20:
                                profit_rate_point = 8
                            elif 20 < profit_rate <= 30:
                                profit_rate_point = 9
                            else:
                                profit_rate_point = 10

                            num_jyunrieki= float(new_df2['純利益'][0])
                            num_soushisan = float(new_df3['総資産'][0])
                            num_zikoshihon = float(new_df3['自己資本率'][0])

                            ROE = num_jyunrieki / (num_soushisan * num_zikoshihon * 0.01) * 100
                            ROE_point = 0
                            if   ROE <= 0:
                                ROE_point = 1
                            elif  0 < ROE <= 1.5:
                                ROE_point = 2
                            elif  1.5 < ROE <= 3:
                                ROE_point = 3
                            elif 3 < ROE <= 5:
                                ROE_point = 4
                            elif 5 < ROE <= 7.5:
                                ROE_point = 5
                            elif 7.5 < ROE <= 10:
                                ROE_point = 6
                            elif  10 < ROE <= 15:
                                ROE_point = 7
                            elif  15 < ROE <= 20:
                                ROE_point = 8
                            elif 20 < ROE <= 30:
                                ROE_point = 9
                            else:
                                ROE_point = 10


                            profitness_point = (profit_rate_point + ROE_point) / 2

                            PER_point = 0
                            if   50 < PER :
                                PER_point = 1
                            elif  40 < PER <= 50:
                                PER_point = 2
                            elif  35 < PER <= 40:
                                PER_point = 3
                            elif 25 < PER <= 35:
                                PER_point = 4
                            elif 20 < PER <= 25:
                                PER_point = 5
                            elif   15 < PER <= 20:
                                PER_point = 6
                            elif   PER == 15:
                                PER_point = 7
                            elif  10 < PER < 15:
                                PER_point = 8
                            elif 7.5 < PER <= 10:
                                PER_point = 9
                            else:
                                PER_point = 10

                            PSR_point = 0
                            if   10 < PSR :
                                PSR_point = 1
                            elif  8 < PSR <= 10:
                                PSR_point = 2
                            elif  6 < PSR <= 8:
                                PSR_point = 3
                            elif 5 < PSR <= 6:
                                PSR_point = 4
                            elif 4 < PSR <= 5:
                                PSR_point = 5
                            elif   3 < PSR <= 4 :
                                PSR_point = 6
                            elif  2 < PSR <= 3:
                                PSR_point = 7
                            elif  1 < PSR <= 2:
                                PSR_point = 8
                            elif 0.5 < PSR <= 1:
                                PSR_point = 9
                            else:
                                PSR_point = 10

                            PBR_point = 0
                            if   20 < PBR :
                                PBR_point = 1
                            elif  10 < PBR <= 20:
                                PBR_point = 2
                            elif  7.5 < PBR <= 10:
                                PBR_point = 3
                            elif 5 < PBR <= 7.5:
                                PBR_point = 4
                            elif 3 < PBR < 5:
                                PBR_point = 5
                            elif   2.5 < PBR < 3 :
                                PBR_point = 6
                            elif  2 < PBR <= 2.5:
                                PBR_point = 7
                            elif  1 < PBR <= 2:
                                PBR_point = 8
                            elif 0.5 < PBR <= 1:
                                PBR_point = 9
                            else:
                                PBR_point = 10

                            cheap_point = (PER_point + PSR_point + PBR_point) / 3

                            self_asset_rate = float(new_df3['自己資本率'][0])
                            safety_point = 0
                            if    self_asset_rate <= 10 :
                                safety_point = 1
                            elif  10 < self_asset_rate <= 20:
                                safety_point = 2
                            elif  20 < self_asset_rate <= 25:
                                safety_point = 3
                            elif 25 < self_asset_rate <= 30:
                                safety_point = 4
                            elif 30 < self_asset_rate <= 40:
                                safety_point = 5
                            elif 40 < self_asset_rate <= 50 :
                                safety_point = 6
                            elif  50 < self_asset_rate <= 60:
                                safety_point = 7
                            elif  60 < self_asset_rate <= 70:
                                safety_point = 8
                            elif 70 < self_asset_rate <= 80:
                                safety_point = 9
                            else:
                                safety_point = 10

                            value_difference_rate = (target_per2 * ave_profit) / stock_value
                            value_difference_point = 0

                            if    value_difference_rate <= 1 :
                                value_difference_point = 1
                            elif  1 < value_difference_rate <= 1.05:
                                value_difference_point = 2
                            elif  1.05 < value_difference_rate <= 1.1:
                                value_difference_point = 3
                            elif 1.1 < value_difference_rate <= 1.3:
                                value_difference_point = 4
                            elif 1.3 < value_difference_rate <= 1.4:
                                value_difference_point = 5
                            elif    1.4 < value_difference_rate <= 1.5 :
                                value_difference_point = 6
                            elif  1.5 < value_difference_rate <= 1.6:
                                value_difference_point = 7
                            elif  1.6 < value_difference_rate <= 2:
                                value_difference_point = 8
                            elif 2 < value_difference_rate <= 3:
                                value_difference_point = 9
                            else:
                                value_difference_point = 10

                            rule_point = 0

                            if    rule <= 5 :
                                rule_point = 1
                            elif  5 < rule <= 10:
                                rule_point = 2
                            elif  10 < rule <= 15:
                                rule_point = 3
                            elif 15 < rule <= 20:
                                rule_point = 4
                            elif 20 < rule <= 25:
                                rule_point = 5
                            elif 25 < rule <= 30:
                                rule_point = 6
                            elif  30 < rule <= 35:
                                rule_point = 7
                            elif  35 < rule <= 40:
                                rule_point = 8
                            elif 40 < rule <= 50:
                                rule_point = 9
                            else:
                                rule_point = 10

                            surprise_point = (rule_point + value_difference_point) / 2



                            labels = ['Growth', 'Earning', 'Cheapness', 'Safety', 'Possibility']
                            values = [growth_point, profitness_point, cheap_point, safety_point, surprise_point]
                            plot_polar(labels, values, "radar.png") 
                            image = Image.open('radar.png')
                            st.sidebar.image(image, caption='分析結果',use_column_width=True)
                            
                            st.write('<span style="color:red">成長性</span>',
                            unsafe_allow_html=True)
                            left_column, right_column = st.columns(2)
                            left_column.write('売上げ:' + str(share_point) + '点　3期平均増加率(' + str(int(ave_growth_percent)) +')')
                            right_column.write('利益：' + str(sales_point) + '点　増加率(' + str(int(sales_growth)) +')')
                            left_column.write('1株益:' + str(profit_point) + '点　増加率(' + str(int(stock_profit_growth)) +')')
                            st.write('<span style="color:red">収益性</span>',
                            unsafe_allow_html=True)
                            left_column2, right_column2 = st.columns(2)
                            left_column2.write('利益率:' + str(profit_rate_point) + '点　(' + str(int(profit_rate)) +'%)')
                            right_column2.write('ROE:' + str(ROE_point) + '点　増加率(' + str(int(ROE)) +'%)')
                            st.write('<span style="color:red">割安性</span>',
                            unsafe_allow_html=True)
                            left_column3, right_column3 = st.columns(2)
                            left_column3.write('PER:' + str(PER_point) + '点　(' + str(int(PER)) +'倍)')
                            right_column3.write('PSR:' + str(PSR_point) + '点　(' + str(int(PSR)) +'倍)')
                            left_column3.write('PBR:' + str(PBR_point) + '点　(' + str(int(PBR)) +'倍)')
                            st.write('<span style="color:red">安全性</span>',
                            unsafe_allow_html=True)
                            left_column4, right_column4 = st.columns(2)
                            left_column4.write('自己資本比率:' + str(safety_point) + '点　(' + str(int(self_asset_rate)) +'%)')
                            st.write('<span style="color:red">大化け性</span>',
                            unsafe_allow_html=True)
                            left_column5, right_column5 = st.columns(2)
                            left_column5.write('現株価と目標株価との差:' + str(value_difference_point) + '点　(' + str(int(value_difference_rate)) +'%)')
                            right_column5.write('40%ルール:' + str(rule_point) + '点　(' + str(int(rule)) +'%)')
                            st.write('<span style="color:red">合計点数</span>',
                            unsafe_allow_html=True)
                            
                            add_point1 = float(share_point) + float(sales_point) + float(profit_point) + float(profit_rate_point)
                            add_point2 = float(ROE_point) + float(PER_point) + float(PSR_point) + float(PBR_point)
                            add_point3 = float(safety_point) + float(value_difference_point) + float(rule_point)
                            add_point4 = add_point1 + add_point2 + add_point3
                            total_point = 10/11 * add_point4
                            st.subheader(str(int(total_point)) + '点')
                            





 
 
 
 
 
 
 
 
 
expander1 = st.sidebar.expander('資産価値算出方法')
expander1.write('BPS x 割引率')
expander2 = st.sidebar.expander('事業価値算出方法')
expander2.write('EPS x ROA x 150 x 財務レバレッジ補正')
expander3 = st.sidebar.expander('理論株価1算出方法')
expander3.write('(資産価値 + 事業価値) x リスク評価率')
expander4 = st.sidebar.expander('理論株価2算出方法')
expander4.write('EPS×PER')
expander5 = st.sidebar.expander('理論株価3算出方法')
expander5.write('EPS×10 + BPS')
expander6 = st.expander('PER 株価収益率')
expander6.write('PER(倍) = 株価　÷　1株あたりの純利益(EPS)　PERが低ければ低いほど会社が稼ぐ利益に対して株価が割安であることがわかる。')
expander7 = st.expander('EPS:一株あたりの当期純利益(Earning per Share)')
expander7.write('EPS = 純利益 ÷ 発行済みの株式数  株価が収益の何倍まで買われているかを示す指標で、業界平均や過去の水準と比較して割高・割安を判断する')
expander8 = st.expander('配当性向')
expander8.write('企業が得た利益の一部が配当として分配されるため、その金額をEPSで割ると、利益のどれくらいが配当されるのかが把握できる。30~40%が平均とされており、これを超えると買いサインの目安となる。配当性向 = 1株あたりの配当 ÷ EPS × 100')
expander9 = st.expander('PSR:株価売上高倍率(Price to Sales Ratio)')
expander9.write('PSR = 時価総額 ÷ 売上高.新興企業同士の株価水準を判断する場合に使用されることなどがあり、PSRが低いほど、株価が割安と判断することができる。.PSRが0.5倍以下だと割安な状態、20倍以上だと割高な状態といえる')
expander10 = st.expander('PBR:株価純資産倍率(Price book-value Ratio)')
expander10.write('PBR = 株価 ÷ BPS.株価が1株当たり純資産(BPS：Book-value Per Share）の何倍まで買われているか、すなわち1株当たり純資産の何倍の値段が付けられているかを見る投資尺度。現在の株価が企業の資産価値（解散価値）に対して割高か割安かを判断する目安として利用される。PBRの数値は、低いほうが割安と判断される。')
expander11 = st.expander('BPS:1株あたりの純資産(Book value per share)')
expander11.write('BPS = 純資産 ÷ 発行済株式数.1株当たりの純資産額を表した金額で、株価が純資産の何倍まで買われているかを示す指標である。BPSが上昇していれば投資先としての安全性、安定性が高いと判断できるため買いサイン。')
expander12 = st.expander('ROA:総資産利益率(Return on Asset)')
expander12.write('4%前後が多く5%を超える日本株は優良企業とされる。インフラ関連や工場をもつ産業や企業などはROAが低くなり、設備投資が少ないIT関連企業などはROAが高くなる傾向がある.ROA = 当期純利益 ÷ 純資産 × １００')
expander13 = st.expander('ROE:自己資本利益率(Return On Equity)')
expander13.write('その株を買うことによってどれだけ効率よく利益を狙えるかを示す指標。８％前後の企業が多く10%を超えると優良企業。ROE=当期純利益÷自己資本×１００.')
expander14 = st.expander('PEGレシオ(price earning growth)')
expander14.write('1倍以下は割安、2倍以上は割高と判断できる。PERが高くなりがちな中小型株を分析できる。PEGレシオ = PER ÷ EPS成長率。')





