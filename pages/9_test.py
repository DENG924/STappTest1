import streamlit as st
import pandas as pd
import os
from pathlib import Path

dir_path = Path(__file__).parent

st.set_page_config(page_title="test")#, page_icon=":material/waving_hand:")
st.title("test path")


if st.button("Example Dataset"):
    files = os.listdir("./")
    st.write(files)

    files = os.listdir(dir_path)
    st.write(dir_path)
    st.write(files)
    #df_datos_eolicos = pd.read_csv(file_url, sep='\t', decimal=",", header=0,encoding='ISO-8859-1')
    st.text("File loaded.")


    #A table to dispaly the dataframe
    st.text("Table of preview of the first 3 rows of the file")
    st.write(df_datos_eolicos.head(3))
    #st.write(df_datos_eolicos.loc["2017-01-01"])  #https://www.geeksforgeeks.org/python/python-pandas-dataframe-loc/
    #st.write(df_datos_eolicos)
    st.session_state["df_datos_eolicos"] = df_datos_eolicos # initiated session state to access the data in other page
