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
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
 
st.title('一目均衡表')
days = st.selectbox(
    '何日間の取引を想定していますか？',
    (1,3,5, 10))
option = st.text_input('銘柄コードを入力してください')
if option:
        ticker = str(option) + '.T'
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

        
 
        # figを定義
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_width=[0.2])
        
        # Candlestick 
        fig.add_trace(
            go.Candlestick(x=source["Date"], open=source["Open"], high=source["High"], low=source["Low"], close=source["Close"], name="OHLC"),
            row=1, col=1
        )
        
        # Volume
        # fig.add_trace(
        #     go.Bar(x=source["Date"], y=source["Volume"], name="Volume"),
        #     row=2, col=1
        # )
        
        # 一目均衡表
        fig.add_trace(go.Scatter(x=source["Date"], y=source["base_line"], name="基準線", mode="lines", line=dict(width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=source["Date"], y=source["conversion_line"], name="転換線", mode="lines", line=dict(width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=source["Date"], y=source["leading_span1"], name="先行スパン1", mode="lines", line=dict(width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=source["Date"], y=source["leading_span2"], name="先行スパン2", mode="lines", line=dict(width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=source["Date"], y=source["lagging_span"], name="遅行スパン", mode="lines", line=dict(width=1)), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=source["Date"], y=source["leading_span1"], name="先行スパン1", mode="lines", fill=None, line=dict(width=0, color="gray"), showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=source["Date"], y=source["leading_span2"], name="先行スパン2", mode="lines", fill='tonexty', line=dict(width=0, color="gray"), showlegend=False), row=1, col=1)
        
        
        # Layout
        fig.update_layout(
            width=700,
            height=500)
        
        # y軸名を定義
        fig.update_yaxes(title_text="株価", row=1, col=1)
        #fig.update_yaxes(title_text="出来高", row=2, col=1)
        

        
        fig.update(layout_xaxis_rangeslider_visible=False)
        st.plotly_chart(fig,use_container_width=True)
        #ローソク足が雲を上抜けする
        
        check1 = []
        for i in range(27,488):
            if source['leading_span1'][i]>source['leading_span2'][i]:
                yesterday = source['Close'][i] - source['leading_span1'][i]
                today = source['Close'][i+1] - source['leading_span1'][i+1]
                if yesterday<0 and today>0:
                    check1.append(i)
            else:
                yesterday = source['Close'][i] - source['leading_span2'][i]
                today = source['Close'][i+1] - source['leading_span2'][i+1]
                if yesterday<0 and today>0:
                    check1.append(i)
    
        
        check2=[]
        dif2 = dict()
        #ゴールデンクロスを検出
        for i in check1:
            for k in range(-10,10):
                yesterday = source['base_line'][i+k]- source['conversion_line'][i+k]
                today = source['base_line'][i+1+k]- source['conversion_line'][i+1+k]
                if yesterday>0 and today<0:
                    check2.append(i)
                    dif2.update({i:k})
                    break

        

        

           
 
        #遅行スパンがローソク足を上抜け
        check3 = []
        dif3 = dict()
        for i in check2:
            for k in range(-10,10):
                yesterday = source['lagging_span'][i+k] - source['Close'][i+k]
                today = source['lagging_span'][i+k+1] - source['Close'][i+k+1]
                if yesterday>0 and today<0:
                    check3.append(i)
                    dif3.update({i:k})
                    break
 
       

        dif4 = []
        day = []
        for key in dif3:
            latest = max(dif2[key],dif3[key])
            day.append(latest)
        
        #設定した日にち後に株価があがっているかの確率算出
        price_up = []
        for i in range(len(check3)):
            late_day = check3[i]+day[i]
            
            if source['Close'][late_day]<source['Close'][late_day+days]:
                    price_up.append(1)

        if len(price_up)>0:
            percent = len(price_up)*100 / len(check3)
 
        st.subheader('三役好転が起きたときに' + str(days) + '日後に上昇する確率は' + str(percent) + '%')
 

       



