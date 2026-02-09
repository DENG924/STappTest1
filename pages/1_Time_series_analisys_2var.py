import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Time series data analysis 2var")#, page_icon=":material/table:")
st.title("Time series data analysis with 2 variables")
#st.text("")

if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    ColFiltered=df_datos_eolicos.columns.to_list()
    ColFiltered.remove("Año")
    ColFiltered.remove("Mes")
    ColFiltered.remove("Dia")
    ColFiltered.remove("Hora")
    
    variable1 = st.selectbox("Select variable 1:", ColFiltered, index=0)
    variable2 = st.selectbox("Select variable 2:", ColFiltered, index=1)

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
    df_agrupado=df_datos_eolicos[[variable1, variable2]]                #dataframe di solo 2 colonne
    df_agrupado=df_agrupado.resample(frecuencia).mean().reset_index()  #ricampionato

    #crear figura interactiva con Ploty
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=df_agrupado["Date/Time"],y=df_agrupado[variable1], mode="lines",name=variable1))
    fig.add_trace(go.Scatter(x=df_agrupado["Date/Time"],y=df_agrupado[variable2], mode="lines",name=variable2))

    #configurar el titulo y etiquetas
    fig.update_layout(
        title=f"Time serires of {variable1} and {variable2} with frequency ({frecuencia})",
        xaxis_title="Date",
        yaxis_title=variable1 + " vs " +  variable2,
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



