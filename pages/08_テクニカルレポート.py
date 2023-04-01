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
import datetime

st.set_page_config(layout="wide")

app_id = '47d4ff02a160e5f085f1baf6ff2dea46e8110488'
stats_data_id = '0003109785' # 年次別にみた人口動態総覧GDP

# 統計データ取得のURL
url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?'
url += 'appId={0:s}&'.format(app_id) 
url += 'statsDataId={0:s}&'.format(stats_data_id)
url += 'metaGetFlg=N&'          # メタ情報有無
url += 'explanationGetFlg=N&'   # 解説情報有無
url += 'annotationGetFlg=N&'    # 注釈情報有無

# 統計データ取得
json = requests.get(url).json()

# 統計データからデータ部取得
values = json['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# jsonからDataFrameを作成
df = pd.DataFrame(values)


df2 = df.tail(10)
df2 = df2.reset_index(drop=True)
df2['date'] = 1

for i in range(10):
  date = df2['@time'][i] 
  date = date[:4] + date[6:]
  
  date_object = datetime.datetime.strptime(date, "%Y%m%d")
  formatted_date = date_object.strftime("%Y-%m-%d")
  df2['date'][i] = formatted_date


#GDPの値を文字列から数値に変換
df2['$'] = df2['$'].astype('float')
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(8, 8))
X = df2['date']
Y = df2['$']
# グラフ可視化（折れ線グラフ）
ax1.plot(X, Y)
st.pyplot(ax1)
plt.plot_date(X, Y, label='GDP', linestyle='solid')

# 書式設定
plt.legend(loc="best")         # 凡例
plt.gcf().autofmt_xdate()      # X軸値を45度回転
plt.savefig("date_graph3.jpg") # 画像保存
image = Image.open('date_graph3.jpg')
st.image(image, caption='GDP [10億円]',width=400)
df=[]
df2=[]



#景気動向指数
stats_data_id = '0003446461' # CI

# 統計データ取得のURL
url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?'
url += 'appId={0:s}&'.format(app_id) 
url += 'statsDataId={0:s}&'.format(stats_data_id)
url += 'metaGetFlg=N&'          # メタ情報有無
url += 'explanationGetFlg=N&'   # 解説情報有無
url += 'annotationGetFlg=N&'    # 注釈情報有無

# 統計データ取得
json = requests.get(url).json()

# 統計データからデータ部取得
values = json['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# jsonからDataFrameを作成
df = pd.DataFrame(values)
df3=[]

for data in range(5000):
  if df['@tab'][data] == '100' and df['@cat01'][data] =='100':
    df3.append(df['$'][data])
    

df3=pd.DataFrame(df3)
df3['datetime'] = 1
for data in range(5000):
  if df['@tab'][data] == '100' and df['@cat01'][data] =='100':
    df3['datetime'][data] = df['@time'][data]

    
    




df4 = df3.tail(10)
df4 = df4.reset_index(drop=True)
df4['date'] = 1

for i in range(10):
  date = df4['datetime'][i] 
  date = date[:4] + date[6:]
  
  date_object = datetime.datetime.strptime(date, "%Y%m%d")
  formatted_date = date_object.strftime("%Y-%m-%d")
  df4['date'][i] = formatted_date

#GDPの値を文字列から数値に変換
df4[0] = df4[0].astype('float')

X2 = df4['date']
Y2 = df4[0]
# グラフ可視化（折れ線グラフ）
ax2.plot(X2, Y2)
st.pyplot(ax2)
plt.plot_date(X2, Y2, label='CI', linestyle='solid')

# 書式設定
plt.legend(loc="best")         # 凡例
plt.gcf().autofmt_xdate()      # X軸値を45度回転
plt.savefig("date_graph4.jpg") # 画像保存
image = Image.open('date_graph4.jpg')
st.image(image, caption='景気動向指数CI ',width=600)
