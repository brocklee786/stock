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
stats_data_id = '0003109785' # 年次別にみた人口動態総覧

# メタ情報取得のURL
url = 'https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo?'
url += 'appId={0:s}&'.format(app_id) 
url += 'statsDataId={0:s}&'.format(stats_data_id)
url += 'explanationGetFlg=N&'   # 解説情報有無：無し

# メタ情報取得
meta_info = requests.get(url).json()

# 統計データのカテゴリ要素をID(数字の羅列)から、意味がわかる名称に変更する
for class_obj in meta_info:

    # メタ情報の「@id」の先頭に'@'を付与'した文字列が、
    # 統計データの列名と対応している
    column_name = '@' + class_obj['@id']
    
    # 統計データの列名を「@code」から「@name」に置換するディクショナリを作成
    id_to_name_dict = {}
    for obj in class_obj['CLASS']:
        id_to_name_dict[obj['@code']] = obj['@name']
    
    # ディクショナリを用いて、指定した列の要素を置換 
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 統計データの列名を変換するためのディクショナリを作成
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

# ディクショナリに従って、列名を置換する
new_columns = []
for col in stats_data:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)
        
df.columns = new_columns

st.write(df)



