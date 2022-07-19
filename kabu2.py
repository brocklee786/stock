import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import matplotlib
import matplotlib.pyplot as plt

st.title('株価評価')
# st.image('./sample.jpg')

option = st.text_input('株価番号を入力してください')
 
def get_basic_info(option):
    ticker = str(option)
    url = "https://minkabu.jp/stock/" + ticker
    html = requests.get(url)
 
    soup = BeautifulSoup(html.content, "html.parser")
 
    basic_info = {}
    li_all = soup.find_all('li')
    for li in li_all:
        dt = li.find('dt')
        if dt is None:
            continue
       
        dd = li.find('dd')
   
        key = dt.text
        value = dd.text
   
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
    ax.set_rlim(0 ,5)
    fig.savefig(imgname)
    plt.close(fig)

 
 
if option:
    ticker_dict = get_basic_info(option)
    company_info = get_company_info(option)
    df = pd.DataFrame.from_dict([ticker_dict])
    df2 = pd.DataFrame(get_kessan(option))
    df3 = pd.DataFrame(get_zaimu(option))
   
 
 
    st.write('<span style="color:red">基本情報</span>',
              unsafe_allow_html=True)
    st.table(df)
    st.write('<span style="color:red">決算情報</span>',
              unsafe_allow_html=True)
    st.table(df2)
    st.write('<span style="color:red">財務情報</span>',
              unsafe_allow_html=True)
    st.table(df3)
 
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
 
 
    #stock_value = st.text_input('現在の株価を入力してください')
   
    #データを数値に変換
    num_PER = float(new_df['PER(調整後)'][0])
    num_PSR = float(new_df['PSR'][0])
    num_PBR = float(new_df['PBR'][0])
    num_profit = float(new_df2['純利益'][0])
    num_asset = float(new_df3['総資産'][0])
    num_capital_ratio_percent = float(new_df3['自己資本率'][0])
    num_capital_ratio = float(new_df3['自己資本率'][0]) / 100
    num_BPS = float(new_df3['1株純資産'][0])
    num_EPS = float(new_df2['1株益'][0])
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
    st.sidebar.write('<span style="color:red">理論株価</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(int_theoretical_stock_price) + '円')
    st.sidebar.write('<span style="color:red">上限株価</span>',
              unsafe_allow_html=True)
    st.sidebar.write(str(int_max_stock_price) + '円')

    
   
   
 
    stock_value = new_df['時価総額'][0] / new_df['発行済株数'][0]
 
 
    target_per = st.text_input('実績PER高値平均を入力してください')
    target_per2 = 0
    ave_profit = 0
    if target_per:
        num_target_profit = float(target_per)
        past_profit = st.text_input('前期の営業利益を入力してください')
        if past_profit:
            num_past_profit = int(past_profit)
            now_profit = st.text_input('今期の営業利益を入力してください')
            if now_profit:
                num_now_profit = int(now_profit)
                future_profit = st.text_input('来期の予想営業利益を入力してください')
                if future_profit:
                    num_future_profit = int(future_profit)
                    ave_growth = ((num_now_profit - num_past_profit)/num_past_profit + (num_future_profit - num_now_profit)/num_now_profit) / 2
                    ave_growth_percent = ave_growth * 100
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
 
 
                    profit_stock_now = st.text_input('今期の1株益を入力してください')
                    if profit_stock_now:
                        num_profit_stock_now = float(profit_stock_now)
                        profit_stock_future = st.text_input('来期の1株益を入力してください')
                        if profit_stock_future:
                            num_profit_stock_future = float(profit_stock_future)
                            ave_profit = (num_profit_stock_now + num_profit_stock_future) / 2
 
       
 
                   
 
 
 
 
 
   
 
 
                            
                            st.sidebar.write('<span style="color:red">目標PER1</span>',
                                                unsafe_allow_html=True)
                            st.sidebar.write(str(target_per))
 
                            
                            st.sidebar.write('<span style="color:red">目標PER2</span>',
                                                unsafe_allow_html=True)
                            st.sidebar.write(str(target_per2))
 
                            
                            st.sidebar.write('<span style="color:red">1年後の目標株価</span>',
                                            unsafe_allow_html=True)
                            st.sidebar.write(str(target_per2 * ave_profit) + '円')
 
                            company_value = new_df['時価総額'][0]
                            PSR = int(company_value) / int(new_df2['売上高'][0])
 
                            sales_amount = st.text_input('今期の売上高予想を入力してください')
                            if sales_amount:
                                profit_increase_rate = float(sales_amount) / float(new_df2['売上高'][0])
                                rule = profit_increase_rate + ave_growth_percent
                                sales_growth = ((int(sales_amount) - int(new_df2['売上高'][0])) / int(new_df2['売上高'][0])) * 100
                                stock_profit_growth = ((float(profit_stock_future) + float(profit_stock_now)) / float(profit_stock_now)) * 100
                                   
                                sales_point = 0
                                share_point = 0
                                profit_point = 0
                                growth_point = 0
 
                                if  ave_growth_percent <= -20:
                                    share_point = 1
                                elif  -20 < ave_growth_percent <= -5:
                                        share_point = 2
                                elif  -5 < ave_growth_percent <= 5:
                                        share_point = 3
                                elif 5 < ave_growth_percent <= 20:
                                        share_point = 4
                                else:
                                        share_point = 5
 
                                if   sales_growth <= -20:
                                    sales_point = 1
                                elif  -20 < sales_growth <= -5:
                                        sales_point = 2
                                elif  -5 < sales_growth <= 5:
                                        sales_point = 3
                                elif 5 < sales_growth <= 20:
                                        sales_point = 4
                                else:
                                        sales_point = 5
 
 
                                if   stock_profit_growth <= -20:
                                    profit_point = 1
                                elif  -20 < stock_profit_growth <= -5:
                                        profit_point = 2
                                elif  -5 < stock_profit_growth <= 5:
                                        profit_point = 3
                                elif 5 < stock_profit_growth <= 20:
                                        profit_point = 4
                                else:
                                        profit_point = 5
 
                                   
                                growth_point = (share_point + sales_point + profit_point) / 3
 
                                profit_rate = float(new_df2['営業利益'][0]) / float(new_df2['売上高'][0]) * 100

                                if   profit_rate <= 1.5:
                                    profit_rate_point = 1
                                elif  1.5 < profit_rate <= 5:
                                        profit_rate_point = 2
                                elif  5 < profit_rate <= 10:
                                        profit_rate_point = 3
                                elif 10 < profit_rate <= 20:
                                        profit_rate_point = 4
                                else:
                                        profit_rate_point = 5

                                num_jyunrieki= float(new_df2['純利益'][0])
                                num_soushisan = float(new_df3['総資産'][0])
                                num_zikoshihon = float(new_df3['自己資本率'][0])

                                ROE = num_jyunrieki / (num_soushisan * num_zikoshihon * 0.01) * 100
                                ROE_point = 0
                                if   ROE <= 1.5:
                                    ROE_point = 1
                                elif  1.5 < ROE <= 5:
                                        ROE_point = 2
                                elif  5 < ROE <= 10:
                                        ROE_point = 3
                                elif 10 < ROE <= 20:
                                        ROE_point = 4
                                else:
                                        ROE_point = 5


                                profitness_point = (profit_rate_point + ROE_point) / 2

                                PER_point = 0
                                if   40 < PER :
                                    PER_point = 1
                                elif  25 < PER <= 40:
                                        PER_point = 2
                                elif  15 < PER <= 25:
                                        PER_point = 3
                                elif 10 < PER <= 15:
                                        PER_point = 4
                                else:
                                        PER_point = 5

                                PSR_point = 0
                                if   8 < PSR :
                                    PSR_point = 1
                                elif  5 < PSR <= 8:
                                        PSR_point = 2
                                elif  3 < PSR <= 5:
                                        PSR_point = 3
                                elif 1 < PSR <= 3:
                                        PSR_point = 4
                                else:
                                        PSR_point = 5

                                PBR_point = 0
                                if   10 < PBR :
                                    PBR_point = 1
                                elif  5 < PBR <= 10:
                                        PBR_point = 2
                                elif  2.5 < PBR <= 5:
                                        PBR_point = 3
                                elif 1 < PBR <= 2.5:
                                        PBR_point = 4
                                else:
                                        PBR_point = 5

                                cheap_point = (PER_point + PSR_point + PBR_point) / 3

                                self_asset_rate = float(new_df3['自己資本率'][0])
                                safety_point = 0
                                if    self_asset_rate <= 10 :
                                    safety_point = 1
                                elif  20 < self_asset_rate <= 30:
                                        safety_point = 2
                                elif  30 < self_asset_rate <= 50:
                                        safety_point = 3
                                elif 50 < self_asset_rate <= 70:
                                        safety_point = 4
                                else:
                                        safety_point = 5

                                value_difference_rate = (target_per2 * ave_profit) / stock_value
                                value_difference_point = 0

                                if    value_difference_rate <= 10 :
                                    value_difference_point = 1
                                elif  20 < value_difference_rate <= 30:
                                        value_difference_point = 2
                                elif  30 < value_difference_rate <= 50:
                                        value_difference_point = 3
                                elif 50 < value_difference_rate <= 70:
                                        value_difference_point = 4
                                else:
                                        value_difference_point = 5

                                rule_point = 0

                                if    rule <= 10 :
                                    rule_point = 1
                                elif  10 < rule <= 20:
                                        rule_point = 2
                                elif  20 < rule <= 30:
                                        rule_point = 3
                                elif 30 < rule <= 40:
                                        rule_point = 4
                                else:
                                        rule_point = 5

                                surprise_point = (rule_point + value_difference_point) / 2

                                
                                
                                labels = ['Growth', 'Earning', 'Cheapness', 'Safety', 'Possibility']
                                values = [growth_point, profitness_point, cheap_point, safety_point, surprise_point]
                                plot_polar(labels, values, "radar.png") 
                                image = Image.open('radar.png')
                                st.image(image, caption='分析結果',use_column_width=True)
                                


                                

 
 
 
 
 
 
 
 
 
expander1 = st.sidebar.expander('資産価値算出方法')
expander1.write('BPS x 割引率')
expander2 = st.sidebar.expander('事業価値算出方法')
expander2.write('EPS x ROA x 150 x 財務レバレッジ補正')
expander3 = st.sidebar.expander('理論株価算出方法')
expander3.write('(資産価値 + 事業価値) x リスク評価率')
 
