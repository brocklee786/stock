import streamlit as st
import pytesseract
from PIL import Image


my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if my_upload:
    img = fix_image("./ocr.jpg")
    
# OCRエンジンのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 画像から文字を読み取る
text = pytesseract.image_to_string(img, lang='eng')

# 結果の表示
st.write(text)
