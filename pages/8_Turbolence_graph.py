import streamlit as st
import pandas as pd
import numpy as np
#import plotly.graph_objects as go
import matplotlib.pyplot as plt  #per rosa di viento

st.set_page_config(page_title="Turbolence analisys")#, page_icon=":material/table:")
st.title("Turbolence analysis")
#st.text("")

if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    opziones_velocidades = [col for col in df_datos_eolicos.columns if "Velocidad" in col]
    col_vel_text = st.multiselect("Select the wind speeds:", opziones_velocidades)


    opziones_std = [col for col in df_datos_eolicos.columns if "Std" in col]
    col_std_text= st.multiselect("Select the stds:", opziones_std)

    # Create a text input box with a default placeholder
    h_text = st.text_input("Enter the altitudes [m] corresponding to wind speeds (comma to separate)", "100,80")
    h=""
    h=h_text.split(",")
    #try:
    #    h = int(h_text)
    #except ValueError:
    #    h=None

    #fecha_inicio1=widgets.DatePicker(description="Fecha inicio:", value=df_datos_eolicos.index[0].date())  #value=datetime.date(2019, 7, 9)
    #fecha_fin1=widgets.DatePicker(description="Fecha fin:", value=df_datos_eolicos.last_valid_index().date())

    if (h is None) or (col_vel_text is None) or (col_std_text is None):
        st.error("Please define all the variable above")
    else:
        # Display the name after clicking the Submit button
        if st.button("Submit"):
            bins_velocidad=np.arange(0,25,1) #intervalo de 1m/s

            #crear el grafico
            fig, ax = plt.subplots()

            for i in range(0,len(h)):
                col_vel=col_vel_text[i]
                col_std=col_std_text[i]
                altura=h[i]
                #extraer columna y filtrar valores nan
                df_filtrado=df_datos_eolicos[[col_vel,col_std]].dropna()

                #Calcular indice de turbolencia 
                df_filtrado["Indice de Turbolencia" + str(altura)]= df_filtrado[col_std] /df_filtrado[col_vel]

                #Calcular indice de turbolencia por bin
                df_agrupado= df_filtrado.groupby(pd.cut(df_filtrado[col_vel],bins=bins_velocidad)).mean()

                velocidades_centrales= bins_velocidad[:-1] + np.diff(bins_velocidad)/2

                ax.plot(velocidades_centrales[:len(df_agrupado)], df_agrupado["Indice de Turbolencia" + str(altura)], label=f"Altura{altura}")

                #graficar curva de referencia de la IEC 61400-1 para cada categoria
                #for categoria, df_categoria in categorias_iec.items():
                #    ax.plot(df_categoria.iloc[:0], df_datos_categoria.iloc[:1], linestype="--", color=categorias_colores[categorias], label=f"IEC {categoria}")

            #configuracion del grafico
            ax.set_xlabel("Velocidad del viento [m/s]")
            ax.set_ylabel("Indice de turbolecia Medio")
            ax.set_title("Indice de turbolencia rapresentativo medio")
            ax.legend()
            ax.grid()
            st.pyplot(fig) #plt.show()
