import numpy as np 
from PIL import Image, ImageDraw
import easyocr
import streamlit as st

reader = easyocr.Reader(['ja','en'])
selected_image = st.file_uploader('upload image', type='jpg')

original_image = st.empty()
result_image = st.empty()

if (selected_image != None):
    original_image.image(selected_image)
    pil = Image.open(selected_image)
    result = reader.readtext(np.array(pil))
    draw = ImageDraw.Draw(pil)
    for each_result in result:
        draw.rectangle(tuple(each_result[0][0] + each_result[0][2]), outline=(0, 0, 255), width=3)
        st.write(each_result[1])
    result_image.image(pil)
