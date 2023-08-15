import yfinance as yf
import streamlit as st

# 銘柄コードリスト
used_codes = [3181, 2780, 2681, 2674, 3093, 3179, 9278]

st.title('類似銘柄戦略')

def backtest(data):
    for code in used_codes:
        stock_data = yf.download(str(code), start="2017-01-01", end="2023-08-01")
        stock_data["PrevClose"] = stock_data["Close"].shift(1)  # 前日の終値
        stock_data["PriceChange"] = (stock_data["Close"] - stock_data["PrevClose"]) / stock_data["PrevClose"]
        
        for index, row in stock_data.iterrows():
            if row["PriceChange"] > 0.05:
                st.write(f"銘柄コード {code} が前日から5%以上上昇しました。")
                for other_code in used_codes:
                    if other_code != code:
                        other_stock_data = yf.download(str(other_code), start=index, end=index)
                        if len(other_stock_data) > 0:
                            other_next_day_close = other_stock_data["Close"].values[0]
                            if other_next_day_close > row["Close"]:
                                st.write(f"  銘柄コード {other_code} も翌日に上昇しています。")

# バックテストを実行
if st.button('計算を行う'):
  backtest(used_codes)
