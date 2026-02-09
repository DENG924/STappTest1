import streamlit as st
import pandas as pd

st.set_page_config(page_title="Upload file")#, page_icon=":material/waving_hand:")
st.title("Upload a file")

st.write(
    """
    About the file format, the column headers must contain the following strings to allow the variables to be correctly recognized.
    1. **Date and time**: "Date/Time"
    2. **Speed**: "Speed", "Velocidad"
    3. **Direction**: "Dir", "Veleta"
    4. **Standard deviation**: "Std", "Dev"
    5. **Temperature**: "temp"
    """
)


uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=False, type=["txt", "csv"]) #https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
if uploaded_file is not None:
    df_datos_eolicos = pd.read_csv(uploaded_file, sep='\t', decimal=",", header=0,encoding='ISO-8859-1')
    st.text("File loaded.")

    # Convertir la columna de fecha a formato datetime para luego hacer grupby y calcular valores para agrupo de anos, mes etc..
    df_datos_eolicos["Date/Time"]=pd.to_datetime(df_datos_eolicos["Date/Time"])

    #Crear las columnas "Año" y "Mes"
    df_datos_eolicos["Año"]=df_datos_eolicos["Date/Time"].dt.year
    df_datos_eolicos["Mes"]=df_datos_eolicos["Date/Time"].dt.to_period("M")
    df_datos_eolicos["Dia"]=df_datos_eolicos["Date/Time"].dt.to_period("D")
    df_datos_eolicos["Hora"]=df_datos_eolicos["Date/Time"].dt.to_period("h")

    #convertir la columna Date/time en indice Dataframe para facilitar analisi temporal
    df_datos_eolicos.set_index("Date/Time", inplace=True)

    #A table to dispaly the dataframe
    st.text("Table of preview of the first 3 rows of the file")
    st.write(df_datos_eolicos.head(3))
    #st.write(df_datos_eolicos.loc["2017-01-01"])  #https://www.geeksforgeeks.org/python/python-pandas-dataframe-loc/
    #st.write(df_datos_eolicos)
    st.session_state["df_datos_eolicos"] = df_datos_eolicos # initiated session state to access the data in other page