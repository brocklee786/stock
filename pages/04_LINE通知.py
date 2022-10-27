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
import time
from math import nan
 
 

#データフレームを画像に変換
def TablePlot(df,outputPath,w,h):
    fig, ax = plt.subplots(figsize=(w,h))
    ax.axis('off')
    ax.table(cellText=df.values,
            colLabels=df.columns,
            loc='center')
    plt.rcParams['font.family'] = 'MS Gothic'
    plt.savefig(outputPath)
 
#画像とメッセージをLINEに送信
def main_gazo1():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = '逆張り'
    payload = {"message" :  message}
    files = {"imageFile":open('./table1.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
 
def main_gazo2():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = '順張り'
    payload = {"message" :  message}
    files = {"imageFile":open('./table2.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
 
def main_gazo3():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = 'DMI'
    payload = {"message" :  message}
    files = {"imageFile":open('./table3.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
 
def main_gazo4():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = 'MACD'
    payload = {"message" :  message}
    files = {"imageFile":open('./table4.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)

def main_gazo5():
    url = "https://notify-api.line.me/api/notify"
    token = "Y7qIXR6HxmIoOG2Tpx2X6uAZEfa1RcTIKKkK9tVn0LL"
    headers = {"Authorization" : "Bearer "+ token}
 
    message = '一目均衡表'
    payload = {"message" :  message}
    files = {"imageFile":open('./table5.png','rb')}
 
    requests.post(url ,headers = headers ,params=payload,files=files)
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
 

    
def trim_camma_cashflow(x):
    y = x.replace(',','')
    return y
   
st.set_page_config(layout="wide")
 
st.title('LINEに通知')
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (1,3, 5, 10))
codes = ['5901','6810','6807','6804','6779','6770','6754','6753','6752','6750','6724','6723','5727','5802','5805','5929','5943','6013','6047','6055','6058','6062','6083','6070','6088','6101','6113','6136','6141','6208','6238','6250','6269','6287','6298','6338','6395','6407','6412','6463','6503','6513','6544','6556','6630','6641','6666','6871','6925','6937','6941','6952','6962','6995','6997','6999','7072','7078','7187','7198','7202','7240','7261','7270','7278','7296','7313','7254','7414','7421','7453','7483','7532','7545','7575','7606','7613','7616','7718','7730','7732','7731','7752','7803','7760','7864','7867','7906','7915','7965','7970','7981','7984','7994','8012','8020','8086','8129','8130','8133','8174','8233','8253','8282','8341','8370','8411','8570','8595','8699','8795','8802','8804','8876','8905','8909','8920','8923','8929','8934','9005','9006','9024','9007','9076','9099','9308','9401','9409','9416','9434','9502','9503','9511','9513','9517','9519','9625','9692','9832','1518','1712','1808','1812','1826','1944','1963','1969','2001','2002','2127','2154','2158','2160','2212','2301','2309','2389','2395','2427','2432','2433','2438','2471','2503','2531','2579','2607','2613','2678','2681','2685','2730','2784','2792','2910','2929','2975','3003','3031','3048','3076','3086','3099','3101','3103','3105','3107','3134','3167','3161','3197','3222','3254','3319','3360','3377','3405','3407','3433','3436','3479','3482','3491','3591','3604','3632','3657','3661','3675','3681','3683','3691','3694','3902','3926','3962','3966','3990','3997','4028','4042','4043','4045','4053','4054','4056','4057','4080','4088','4095','4204','4272','4331','4394','4395','4423']
 
useful_code = []
percent_50 = []
RSI_gyakucode = []
RSI_juncode = []
st.subheader('RSIによる分析')
#リストに入っているすべてのコードでRSIが一番高い際の値とそのRSIの日数を計算
if st.button('LINEに通知する1'):
    st.write('calculating...')
     
    for code in codes:
           
            ticker = str(code) + '.T'
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
            #移動平均
            span01=5
            span02=25
            span03=50
   
            source['sma01'] = price.rolling(window=span01).mean()
            source['sma02'] = price.rolling(window=span02).mean()
            source['sma03'] = price.rolling(window=span03).mean()
   
            change3_probability = []
            probability_50  = []
            #フィッティングした際にRSIが一番高くなるものを算出
            for i in range(1,20):
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
                    df_up_sma_random = df_up.rolling(window=i, center=False).mean()
                    df_down_sma_random = df_down.rolling(window=i, center=False).mean()
                    source["RSI"] = 100.0 * (df_up_sma_random / (df_up_sma_random + df_down_sma_random))
               
                    change3 =  []
                    no_change3 = []
               
                    for k in range(20,490):
                            #下降トレンドから上昇トレンドのとき
                           
                            sub1 = source['RSI'][500-k] - source['RSI'][500-k-1]
                            sub2 = source['RSI'][500-k-1] - source['RSI'][500-k-2]
                            #sub3 = source['RSI'][500-k-1+14]
                           
                            if sub1>0 and sub2<0 and source['RSI'][500-k-3] < 40:
                                    for a in range(1,5):
                                            trend_change = source['sma01'][500-k+a] - source['sma01'][500-k-1+a]
                                            if trend_change > 0:
                                                    change3.append(1)
                                                    break
                                            else:
                                                    no_change3.append(1)
   
                    probability3 = len(change3) * 100 / (len(change3) + len(no_change3))
                    probability3 = int(probability3)
                    change3_probability.append(probability3)
   
                    percent50_raise = []
                    percent50_unraise = []
                    #50%を超えたときに上昇が続いているか(順張り)
                    for j in range(20,500):
                            raise_continue = source['sma01'][500-j+days] - source['sma01'][500-j-1]
                            if source['RSI'][500-j-1] > 50 and source['RSI'][500-j-2] < 50:
                                    if raise_continue > 0:
                                            percent50_raise.append(1)
                                    else:
                                            percent50_unraise.append(1)
   
                    percent50_probability = len(percent50_raise) * 100 / (len(percent50_raise) + len(percent50_unraise))
                    percent50_probability = int(percent50_probability)
                    probability_50.append(percent50_probability)
   
            max_num = max(change3_probability)
            max_day = change3_probability.index(max_num) + 1
            max_num2 = max(probability_50)
            max_day2 = probability_50.index(max_num2) + 1
       
   
       
            if max_num > 50 and source['RSI'][499] < 40:
                    company_info = get_company_info(code)
                    useful_code.append({
                    '社名':company_info['社名'],
                    '銘柄コード':code,
                    '最大正解確率':max_num,
                    'RSI日数':max_day,
                    'RSI現在':source['RSI'][499],
                    '株価':source['Close'][499]})
                    RSI_gyakucode.append(code)
                    
   
            if max_num2 > 70 and 45 < source['RSI'][499] < 50 and source['sma01'][499] - source['sma01'][498] > 0:
                    company_info = get_company_info(code)
                    percent_50.append({'社名':company_info['社名'],'銘柄コード':code,'最大正解確率':max_num2,'RSI日数':max_day2,'RSI現在':source['RSI'][499],'株価':source['Close'][499]})
                    RSI_juncode.append(code)
    RSI_theoretical_price = []
    if len(RSI_gyakucode)>0:
        for code in RSI_gyakucode:
                option = code

                ticker_dict = get_basic_info(option)
                
                df = pd.DataFrame.from_dict([ticker_dict])
                df2 = pd.DataFrame(get_kessan(option))
                df3 = pd.DataFrame(get_zaimu(option))
                
            
            
            
                
            
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
            


                
            
            
                #stock_value = st.text_input('現在の株価を入力してください')
            
                #データを数値に変換
                if new_df['PER(調整後)'][0] == '---':
                    break

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
                

                RSI_theoretical_price.append(int_theoretical_stock_price)

    for i in range(len(RSI_theoretical_price)):
        useful_code[i]['理論株価'] = RSI_theoretical_price[i]


    RSI_theoretical_price2 = []
    if len(RSI_juncode)>0:
        for code in RSI_juncode:
                option = code

                ticker_dict = get_basic_info(option)
                
                df = pd.DataFrame.from_dict([ticker_dict])
                df2 = pd.DataFrame(get_kessan(option))
                df3 = pd.DataFrame(get_zaimu(option))
                
            
            
            
                
            
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
                if new_df['PER(調整後)'][0] == '---':
                    break

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
                

                RSI_theoretical_price.append(int_theoretical_stock_price)

    for i in range(len(RSI_theoretical_price2)):
        percent_50[i]['理論株価'] = RSI_theoretical_price2[i]
 
    
    useful_code = pd.DataFrame(useful_code)
    if len(useful_code)>0:
        TablePlot(useful_code,'table1.png',10,6)
        main_gazo1()
        st.subheader('逆張り')
        st.table(useful_code)
    percent_50 = pd.DataFrame(percent_50)
    if len(percent_50)>0:
        TablePlot(percent_50,'table2.png',10,6)
        main_gazo2()
        st.subheader('順張り')
        st.table(percent_50)

    st.balloons()
    st.balloons()
expander1 = st.sidebar.expander('逆張り')
expander1.write('RSIが30%以下で反転した際に 5日以内に移動平均線が転換している確率が50%より大きい&現在のRSIが30%未満')
expander1 = st.sidebar.expander('順張り')
expander1.write('現在のRSIが45%~50%&その確率が80%よりも大きい')

MACD_code = []
MACD_buy2 = []
DMI_code = []
DMI_buy2 = []
#MACDとDMIによる通知
st.subheader('DMIとMACDによる分析')
if st.button('LINEに通知する2'):
    for code in codes:
        ticker = str(code) + '.T'
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
 
        # MACD計算
 
        exp12 = source['Close'].ewm(span=12, adjust=False).mean()
        exp26 = source['Close'].ewm(span=26, adjust=False).mean()
        source['MACD'] = exp12 - exp26
 
        # シグナル計算
 
        source['Signal'] = source['MACD'].rolling(window=9).mean()
 
        # ヒストグラム(MACD - シグナル)
 
        source['Hist'] = source['MACD'] - source['Signal']
 
        #DMIの計算
        # DMIの計算
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
 
        DMI_buy = []
        DMI_Nobuy = []
        for i in range(20,489):
                #pDIとmDIがクロスしているかどうかを確認する。
                yesterday = source['pDI'][i-1] - source['mDI'][i-1]
                today = source['pDI'][i] - source['mDI'][i]
                sub = source['Close'][i+days] - source['Close'][i]
                adx_check = source['ADX'][i] - source['ADX'][i-1]
                if yesterday<0 and today>0 and sub > 0 and adx_check>0:
                        DMI_buy.append(i)
                elif yesterday<0 and today>0 and sub<0 and adx_check>0:
                        DMI_Nobuy.append(i)
 
       
       
        DMI_buy = pd.DataFrame(DMI_buy)
        correct_DMI = []
       
        MACD_buy = []
        MACD_Nobuy = []
        for i in range(20,489):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
                sub1 = source['Close'][i+days] - source['Close'][i]
                if yesterday1<0 and today1>0 and sub1>0:
                        MACD_buy.append(i)
                if yesterday1<0 and today1>0 and sub1<0:
                        MACD_Nobuy.append(i)
       
       
 
        MACD_buy_check = []
        for i in range(20,489):
                #MACDとシグナルがクロスしているかどうかを確認する。
                yesterday1 = source['MACD'][i-1] - source['Signal'][i-1]
                today1 = source['MACD'][i] - source['Signal'][i]
               
                if yesterday1<0 and today1>0:
                        MACD_buy_check.append(i)
               
        #st.table(MACD_buy)
 
        MACD_DMI_check = []
        for num in MACD_buy_check:
                for k in range(-3,3):
                       
                        yesterday2 = source['pDI'][(num)+k-1] - source['mDI'][(num)+k-1]
                        today2 = source['pDI'][(num)+k] - source['mDI'][(num)+k]
                        adx_check2 = source['ADX'][num+k] - source['ADX'][num+k-1]
                        if yesterday2<0 and today2>0 and adx_check2>0:
                                MACD_DMI_check.append(num)
                                break
 
        buy = []
        for num in MACD_DMI_check:
                sub2 = source['Close'][num+days] - source['Close'][num]
                if sub2 > 0:
                        buy.append({'Number':num,'Date':source['Date'][num],'Price':source['Close'][num]})
 
        #st.table(buy)
       
        #st.table(correct)
 
        #それぞれの正答率を求める
        if len(DMI_buy)>0:
            DMI_possibility = int(len(DMI_buy) * 100 / (len(DMI_buy) + len(DMI_Nobuy)))
        if len(MACD_buy)>0:
            MACD_possibility = int(len(MACD_buy) * 100 / (len(MACD_buy) + len(MACD_Nobuy)))
        #colab_possibility = int(len(buy) * 100 / len(MACD_DMI_check))
 
       
        MACD_today = source['MACD'][499] - source['Signal'][499]
        MACD_yesterday = source['MACD'][498] - source['MACD'][498]
        dif = MACD_today - MACD_yesterday
        if -5<MACD_today<0 and dif<0 and MACD_possibility>60:
                    company_info = get_company_info(code)
                    MACD_code.append(code)
                    MACD_buy2.append({'社名':company_info['社名'],'銘柄コード':code,'正解確率':MACD_possibility,'株価':source['Close'][499]})
       
        DMI_today = source['pDI'][499] - source['mDI'][499]
        DMI_yesterday = source['pDI'][498] - source['mDI'][498]
        adx_trend = source['ADX'][499] - source['ADX'][498]
        dif2 = DMI_today - DMI_yesterday
        if -5<DMI_today<0 and dif2<0 and adx_trend>0 and DMI_possibility>60:
                    company_info = get_company_info(code)
                    DMI_code.append(code)
                    DMI_buy2.append({'社名':company_info['社名'],'銘柄コード':code,'正解確率':DMI_possibility,'株価':source['Close'][499]})



    #ファンダメンタル(理論株価の計算)
    pd.DataFrame(MACD_buy2)
    pd.DataFrame(DMI_buy2)
    
    MACD_theoretical_price = []
    if len(MACD_code)>0:
        for code in MACD_code:
                option = code

                ticker_dict = get_basic_info(option)
                
                df = pd.DataFrame.from_dict([ticker_dict])
                df2 = pd.DataFrame(get_kessan(option))
                df3 = pd.DataFrame(get_zaimu(option))
                
            
            
            
                
            
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
            


                
            
            
                #stock_value = st.text_input('現在の株価を入力してください')
            
                #データを数値に変換
                if new_df['PER(調整後)'][0] == '---':
                    break
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
                

                MACD_theoretical_price.append(int_theoretical_stock_price)
        

    DMI_theoretical_price = []
    if len(DMI_code)>0:
        for code in DMI_code:
                option = code

                ticker_dict = get_basic_info(option)
                
                df = pd.DataFrame.from_dict([ticker_dict])
                df2 = pd.DataFrame(get_kessan(option))
                df3 = pd.DataFrame(get_zaimu(option))

            
            
            
                
            
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
            


                
            
            
                #stock_value = st.text_input('現在の株価を入力してください')
            
                #データを数値に変換
                if new_df['PER(調整後)'][0] == '---':
                    break
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
                

                DMI_theoretical_price.append(int_theoretical_stock_price)

    for i in range(len(MACD_theoretical_price)):
        MACD_buy2[i]['理論株価'] = MACD_theoretical_price[i]

    for i in range(len(DMI_theoretical_price)):
        DMI_buy2[i]['理論株価'] = DMI_theoretical_price[i]


    if len(DMI_buy2)>0:
        DMI_buy2 = pd.DataFrame(DMI_buy2)
        TablePlot(DMI_buy2,'table3.png',10,10)
        main_gazo3()
        st.subheader('DMI')
        st.table(DMI_buy2)
        
    if len(MACD_buy2)>0:
        MACD_buy2 = pd.DataFrame(MACD_buy2)
        TablePlot(MACD_buy2,'table4.png',10,10)
        main_gazo4()
        st.subheader('MACD')
        st.table(MACD_buy2)
        
    st.balloons()
    st.balloons()
ichimoku=[]
ichimoku_code=[]
st.subheader('一目均衡表よる分析')
if st.button('LINEに通知する3'):
    for code in codes:
        ticker = str(code) + '.T'
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

        #ローソク足が雲を上抜けする
        check1 = []
        for i in range(489,498):
            if source['leading_span1'][i]>source['leading_span2'][i]:
                yesterday = source['Close'][i] - source['leading_span1'][i]
                today = source['Close'][i+1] - source['leading_span1'][i+1]
                if yesterday<0 and today>0:
                    check1.append(1)
            else:
                yesterday = source['Close'][i] - source['leading_span2'][i]
                today = source['Close'][i+1] - source['leading_span2'][i+1]
                if yesterday<0 and today>0:
                    check1.append(1)
    

        #ゴールデンクロスを検出
        for i in range(489,498):
                yesterday = source['base_line'][i]- source['conversion_line'][i]
                today = source['base_line'][i+1]- source['conversion_line'][i+1]
                if yesterday>0 and today<0:
                    check1.append(1)
                    break

    
        #遅行スパンがローソク足を上抜け
        for i in range(489,498):
                yesterday = source['lagging_span'][i] - source['Close'][i]
                today = source['lagging_span'][i+1] - source['Close'][i+1]
                if yesterday>0 and today<0:
                    check1.append(1)
                    break

        if len(check1)>2:
            company_info = get_company_info(code)
            ichimoku.append({'社名':company_info['社名'],'銘柄コード':code,'株価':source['Close'][499]})
            ichimoku_code.append(code)
            
    ichimoku_theoretical_price = []
    if len(ichimoku_code)>0:
        for code in ichimoku_code:
                option = code

                ticker_dict = get_basic_info(option)
                
                df = pd.DataFrame.from_dict([ticker_dict])
                df2 = pd.DataFrame(get_kessan(option))
                df3 = pd.DataFrame(get_zaimu(option))
                
            
            
            
                
            
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
            


                
            
            
                #stock_value = st.text_input('現在の株価を入力してください')
            
                #データを数値に変換
                if new_df['PER(調整後)'][0] == '---':
                    break

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
                

                ichimoku_theoretical_price.append(int_theoretical_stock_price)

    for i in range(len(ichimoku_theoretical_price)):
        ichimoku[i]['理論株価'] = ichimoku_theoretical_price[i]

    if len(ichimoku)>0:
        ichimoku = pd.DataFrame(ichimoku)
        TablePlot(ichimoku,'table5.png',10,10)
        main_gazo5()
        st.subheader('一目均衡表')
        st.table(ichimoku)
 
