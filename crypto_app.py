import pandas as pd
import streamlit as st
import yfinance as yf
import base64
import matplotlib.pyplot as plt
import numpy as np
import json
from PIL import Image
from datetime import datetime


image = Image.open("pexels-worldspectrum-844124.jpg")
image = image.resize((800, 300))
st.image(image)

st.title("CryptoCurrency")

st.markdown(
    """
This App retrieves list of cryptocurrencies coins and give use 
the ability to View, Visualize and Download the data

***
"""
)

st.sidebar.header("Select Crypto")


# @st.cache
def load_crypto_json():
    file = open("crypto.json", "r")
    loaded = json.load(file)
    return loaded


crypto_dict = load_crypto_json()
crypto_name = list(crypto_dict.keys())
crypto_sym = list(crypto_dict.values())


selected_crypto = st.sidebar.selectbox("Cypto", crypto_name)
start_time = st.sidebar.date_input("Start Date", value=datetime(2022, 1, 1))
end_time = st.sidebar.date_input("End Date")


@st.cache
def get_data(symbol, start, end):
    df = yf.download(symbol, start=start_time, end=end_time)
    return df


st.markdown(
    f"""
    ####  DataFrame of  {selected_crypto} from  {start_time} to {end_time}
    """
)
my_dataframe = get_data(crypto_dict[selected_crypto], start_time, end_time)
st.dataframe(my_dataframe)

# ----------------------------------------------------------------------------------------------------#
########## Download Dataframe
@st.cache
def convert_df(df):
    return df.to_csv().encode("utf-8")


csv = convert_df(my_dataframe)

st.download_button(
    "Download CSV",
    csv,
    f"{selected_crypto}_{start_time}_{end_time}.csv",
    "text/csv",
    key="download-csv",
)

# ----------------------------------------------------------------------------------------------------#


# ----------------------------------------------------------------------------------------------------#
########## Charts
selected_column = st.sidebar.selectbox(
    "Select Column to display/change charts", list(my_dataframe.columns)
)

st.markdown(
    f"""
    ***
            Line Chart of the {selected_crypto} from  {start_time} to {end_time}
    """
)


st.line_chart(my_dataframe[selected_column])

st.markdown(
    f"""
    ***
            Line Chart Percentage Change of the {selected_crypto} from  {start_time} to {end_time}
    """
)


st.line_chart(my_dataframe[selected_column].pct_change())

st.markdown(
    f"""
    ***
            Moving Average of the {selected_crypto} from  {start_time} to {end_time}
    """
)

windows = my_dataframe[selected_column].rolling(20)
moving_averages = windows.mean()

moving_averages_list = moving_averages.tolist()[20 - 1 :]
st.line_chart(moving_averages_list)

# ----------------------------------------------------------------------------------------------------#
