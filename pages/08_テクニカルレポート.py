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

for i in range(10):
  datetime = df2['@time'][i] 
  datetime = datetime[:4] + datetime[6:]
  df2['datetime'] = 1
  df2['datetime'][i] = datetime
  
  
st.write(df2)
