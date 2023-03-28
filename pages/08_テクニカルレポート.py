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
st.write(df)

df2 = df.tail(10)
df2 = df2.reset_index(drop=True)
st.write(df2)
df2['date'] = 1

for i in range(10):
  date = df2['@time'][i] 
  date = date[:4] + date[6:]
  
  date_object = datetime.datetime.strptime(date, "%Y%m%d")
  formatted_date = date_object.strftime("%Y-%m-%d")
  df2['date'][i] = formatted_date
st.write(df2)

# 出生率と死亡率を取得する
#gdp = df2['$']


# 図と座標軸を取得
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

# 折れ線グラフをセット
ax.plot(df2['date'], df2['$'], label='GDP')


# Y軸の範囲設定
#ymax = max([ df2['$'].max(), mortality_rate['$'].max() ])
#ax.set_ylim([0, ymax])

# 凡例表示
ax.legend()

# 折れ線グラフを表示
st.pyplot(fig)
