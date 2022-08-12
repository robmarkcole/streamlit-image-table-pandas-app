import streamlit as st
import pandas as pd
import glob
import base64
from PIL import Image
from io import BytesIO
import os

def get_thumbnail(path: str) -> Image:
    img = Image.open(path)
    img.thumbnail((200, 200))
    return img

def image_to_base64(img_path: str) -> str:
    img = get_thumbnail(img_path)
    with BytesIO() as buffer:
        img.save(buffer, 'png') # or 'jpeg'
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(img_path: str) -> str:
    return f'<img src="data:image/png;base64,{image_to_base64(img_path)}">'

@st.cache
def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(thumbnail=image_formatter))

st.title('London Skyline Image Table')

images = glob.glob('images/*.png')
df = pd.DataFrame({'image_path': images, 'thumbnail': images})
html = convert_df(df)

st.markdown(
    html,
    unsafe_allow_html=True
)

st.download_button(
     label="Download data as HTML",
     data=html,
     file_name='output.html',
     mime='text/html',
 )