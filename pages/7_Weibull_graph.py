import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats

st.set_page_config(page_title="Weibull analysis")#, page_icon=":material/table:")

st.title("Overview")
st.text("The following calculations and graphs can be performed")
st.text("1. Weibull and Wind speed graph")
st.text("2. Weibull calculations ")



st.title("Weibull and Wind histogram graph")
st.text("Graph of wind speed histogram and Weibull probability density")

if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    opziones_velocidades = [col for col in df_datos_eolicos.columns if "Velocidad" in col]
    variable = st.selectbox("Select a wind speed:", opziones_velocidades, index=0)

    if st.button("Submit"):
        df_filtrado=df_datos_eolicos.copy()
        #if fecha_inicio and fecha_fin:
        #    df_filtrado=df_filtrado.loc[str(fecha_inicio):str(fecha_inicio)]

        #reducir dataframe a solo dato de velocidad
        df_datos_velocidad=df_filtrado[variable].dropna()  #si puo fare prima al posto di copy

        #Calcular los parámetros de Weibull
        shape,loc,scale=stats.weibull_min.fit(df_datos_velocidad, floc=0)# Return estimates of shape (if applicable), location, and scale parameters from data. The default estimation method is Maximum Likelihood Estimation (MLE), but Method of Moments (MM) is also available
        #generar valores para graficar la curva de Weibull
        x_vals=np.linspace(0,df_datos_velocidad.max(),100)
        weibull_pdf=stats.weibull_min.pdf(x_vals,shape,loc,scale) #weibull_pdf calcola la curva di weibull con i valori dati, #pdf=probabiliy density function (weibull), contra a cdf=cumulative distribute functiuon
        
        #crear histograma interactivo con Plotly
        fig=go.Figure()

        #crear el histograma de frequencia
        hist_data=np.histogram(df_datos_velocidad, bins=25, density=True)
        bin_edges=hist_data[1]
        bin_centers=(bin_edges[:-1]+bin_edges[1:])/2
        bin_values=hist_data[0]

        #Agregar histogramma
        fig.add_trace(go.Bar(x=bin_centers,y=bin_values,name="Wind speed frequency", opacity=0.6, marker=dict(color="blue")))

        #Agregar etiquedas de frecuencia en la base de cada barra #si puo eliminare
        for x,y in zip(bin_centers,bin_values):
            fig.add_annotation(
                x=x,y=y/2, text=f"{y:.3f}",showarrow=False, 
                font=dict(size=10),align="center",bgcolor="lightgray", opacity=0.8
            )
        
        #Agregar curva de Weibull
        fig.add_trace(go.Scatter(x=x_vals,y=weibull_pdf, mode="lines",name="Weibull", line=dict(color="red")))
        
        #agragar texto con los parametros de Weibull
        fig.add_annotation(
            x=0.95, y=0.95, xref="paper", yref="paper",
            text=f"Shape factor(k):{shape:.3f}<br>Scale factor (l):{scale:.3f}",
            showarrow=False,
            align="left",
            bordercolor="black",
            borderwidth=1,
            bgcolor="lightgray",
            font=dict(size=12)
        )

        fig.update_layout(legend_title_text = "Legend")

        fig.update_layout(legend=dict(  #legenda in alto a destra
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        fig.update_layout(
            title=f"Histogram of {variable} with Weibull",
            xaxis_title="Wind speed [m/s]",
            yaxis_title="frequency data/probability density",
            barmode="overlay",
            template="plotly_white"
        )

        #mostrar la figura
        st.plotly_chart(fig, config = {'scrollZoom': False}) #fig.show()










st.title("Weibull calculations")
st.text("Calculations of Weibull probabiliy density and comulative distribute functions")
if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    opziones_velocidades = [col for col in df_datos_eolicos.columns if "Velocidad" in col]
    variable = st.selectbox("Choose a wind speed:", opziones_velocidades, index=0)
    st.write("Probabiliy density function (pdf) parameters")
    velocidad = st.slider("Choose wind speed for PDF", min_value=0, max_value=25)
    st.write("Cumulative distribute function (cdf) parameters ")
    velocidad_min = st.slider("Choose minimum wind speed for CDF", min_value=0, max_value=25)
    velocidad_max = st.slider("Choose maximum wind speed for CDF", min_value=0, max_value=25)

    if st.button("Run"):
        #variable=selector_variable.value
        #velocidad=input_velocidad.value
        #velocidad_min=input_velocidad_min.value
        #velocidad_max=input_velocidad_max.value

        #obtener datos de velocidad y ajustar weibull
        df_datos_velocidad=df_datos_eolicos[variable].dropna()
        shape,loc,scale=stats.weibull_min.fit(df_datos_velocidad, floc=0)

        #1 probabilidad que se de una velocidad especificada
        prob_v = stats.weibull_min.pdf(velocidad,shape,loc,scale) #pdf=probabiliy density function (weibull), contra a cdf=cumulative distribute functiuon

        #2probabilidad acumuladade velocidades menores a a una velocidad especificada
        prob_cumulada_v = stats.weibull_min.cdf(velocidad,shape,loc,scale) #cdf=cumulative distribute functiuon

        #3probabilidad que se de una velocidad especificada
        #prob_cumulada_rango = prob_cumulada_v - stats.weibull_min.cdf(velocidad_min,shape,loc,scale)  #prof
        prob_cumulada_rango = stats.weibull_min.cdf(velocidad_max,shape,loc,scale) - stats.weibull_min.cdf(velocidad_min,shape,loc,scale) 

        #emprimir resultatos
        st.write(f"\n **Results for {variable}**")
        st.write(f"Probability that the speed is exactly {velocidad:.2f} m/s: {prob_v:5f}    (Weibull probability function)")
        st.write(f"Probability that the speed will be less than {velocidad:.2f} m/s: {prob_cumulada_v:5f}        (Weibull cumulative function)")
        st.write(f"Probability that the speed is in the range ({velocidad_min:.2f} - {velocidad_max:.2f}) m/s: {prob_cumulada_rango:5f}   (Weibull cumulative function)")
