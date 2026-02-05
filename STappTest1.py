import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Time series data analysis")
#st.text("")


uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=False, type=["txt", "csv"]) #https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader
if uploaded_file is not None:
    df_datos_eolicos = pd.read_csv(uploaded_file, sep='\t', decimal=",", header=0,encoding='ISO-8859-1')
    st.text("File loaded.")

    # Convertir la columna de fecha a formato datetime para luego hacer grupby y calcular valores para agrupo de anos, mes etc..
    df_datos_eolicos["Date/Time"]=pd.to_datetime(df_datos_eolicos["Date/Time"])

    #A table to dispaly the dataframe
    st.text("Table ")
    st.write(df_datos_eolicos.head(2))
    #st.write(df_datos_eolicos.loc["2017-01-01"])  #https://www.geeksforgeeks.org/python/python-pandas-dataframe-loc/

    #convertir la columna Date/time en indice Dataframe para facilitar analisi temporal
    df_datos_eolicos.set_index("Date/Time", inplace=True)

    #Create dropdowns menu____________________________
    variable = st.selectbox("Select a variable:", df_datos_eolicos.columns.to_list() )

    frecuencia1 = st.selectbox("Select a frequency:", ['H (Hourly)', 'D (Daily)', 'W (Weekly)','M (Monthly)','Y (Yearly)'],index=1) #indiex to pre select a particular item in the list
    #frecuencia: "H" hora, "D, diaria, W (Semanal), M (mensual), A (anual)
    
    frecuencia="D"
    if frecuencia1=="H (Hourly)": frecuencia="H"
    if frecuencia1=="D (Daily": frecuencia="D"
    if frecuencia1=="W (Weekly)": frecuencia="W"
    if frecuencia1=="M (Monthly)": frecuencia="ME"
    if frecuencia1=="Y (Yearly)": frecuencia="YE"
    #st.write(frecuencia)

    #funcion grafico______________________________-
    #variable="Velocidad a 100m [m/s]"
    #frecuencia="D"
    #Agrupar segun la frequencia especificada
    df_agrupado=df_datos_eolicos[variable].resample(frecuencia).mean().reset_index() #DF di una sola variable

    #crear figura interactiva con Ploty
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df_agrupado["Date/Time"],y=df_agrupado[variable], mode="lines",name=variable))

    #configurar el titulo y etiquetas
    fig.update_layout(
        title=f"Time series of {variable} with frequency ({frecuencia})",
        xaxis_title="Date",
        yaxis_title=variable,
        template="plotly_white",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                dict(count=7, label="Last week",step="day", stepmode="backward"),
                dict(count=1, label="Last month",step="month", stepmode="backward"),
                dict(count=6, label="Lasts 6 months",step="month", stepmode="backward"),
                dict(count=1, label="Last year",step="year", stepmode="backward"),
                dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True), #deslizador de fechas
            type="date"
        )
    )

    #mostrar la figura
    st.plotly_chart(fig, config = {'scrollZoom': False})

# A button that displays text when clicked
#if st.button("About"):
#    st.text("Welcome to GeeksForGeeks!")


