# 必要なライブラリのインポート
import streamlit as st
import pytesseract
from PIL import Image

# OCRエンジンのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlitアプリケーションを定義する
def app():
    # サイドバーの設定
    st.sidebar.title('OCRアプリ')
    st.sidebar.subheader('画像から文字を読み取る')

    # メイン画面の設定
    st.title('OCRアプリ')
    st.write('画像から文字を読み取ります')

    # 画像のアップロード
    uploaded_file = st.file_uploader('画像をアップロードしてください', type=['jpeg', 'png'])

    # 画像がアップロードされた場合
    if uploaded_file is not None:
        # 画像の表示
        img = Image.open(uploaded_file)
        st.image(img, caption='アップロードされた画像', use_column_width=True)

        # 画像から文字を読み取る
        text = pytesseract.image_to_string(img, lang='eng')

        # 読み取った文字の表示
        st.subheader('読み取った文字')
        st.write(text)

app()
