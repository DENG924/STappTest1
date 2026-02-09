import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Tables")#, page_icon=":material/table:")
st.title("Tables")
st.text(
    """
    Calculate the following values
    - HOURLY: average value over hourly based grouped data
    - MONTHLY: average value over hourly based grouped data
    - YEARLY: average value over hourly based grouped data
    - TOTAL: average value over entire period of data

    The wind direction is calculate by average of the x and y projecton of direction vector.
    """
)

if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    if st.button("Submit"):
        df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

        columnas_direcciones = [col for col in df_datos_eolicos.columns if "Veleta" in col]
        ColFiltered=df_datos_eolicos.columns.to_list()
        ColFiltered.remove("Año")
        ColFiltered.remove("Mes")
        ColFiltered.remove("Dia")
        ColFiltered.remove("Hora")
        for dir in columnas_direcciones:
            ColFiltered.remove(dir)

        df_valores_anuales=df_datos_eolicos.groupby("Año")[ColFiltered].mean()

        df_valores_mensuales=df_datos_eolicos.groupby("Mes")[ColFiltered].mean()

        #df_valores_mensuales=df_datos_eolicos.groupby("Hora")[ColFiltered].mean()

        resultados_totales={}
        for col in ColFiltered:
            resultados_totales[col] = {
                "Valor promedio total": df_datos_eolicos[col].mean(),
                "Valor promedio anual": df_valores_anuales[col].mean(),  #promedio de los promedios anuales
                "Valor promedio mensual": df_valores_mensuales[col].mean() #promedio de los promedios mensuales
            }
        # convertir resultados en dataframe transposto
        df_resultados_totales = pd.DataFrame(resultados_totales).T

        #_______________DIRECCION____________________________________________
        def f_calculo_direccion_promedio(direcciones):
            direcciones_rad= np.deg2rad(direcciones) #pasa grados a radiantes
            u =np.mean(np.cos(direcciones_rad)) #componente u (este-oeste)
            v =np.mean(np.sin(direcciones_rad)) #componente v (norte-sur)
            direcciones_prom=np.rad2deg(np.arctan2(v,u)) #calcolo direcion promedia y conversion a grados
            return direcciones_prom % 360 #asegurar que sea en 0-360

        #aplicar la funcion en el eje X del dataframe, o sea una columna por vez
        df_direcciones_anuales = df_datos_eolicos.groupby("Año")[columnas_direcciones].apply(lambda x: x.apply(f_calculo_direccion_promedio))

        df_direcciones_mensuales = df_datos_eolicos.groupby("Mes")[columnas_direcciones].apply(lambda x: x.apply(f_calculo_direccion_promedio))

        resultados_direcciones={}
        for col in columnas_direcciones:
            resultados_direcciones[col] = {
                "Valor promedio total": f_calculo_direccion_promedio(df_datos_eolicos[col]),
                "Valor promedio anual": df_datos_eolicos.groupby("Año")[col].apply(f_calculo_direccion_promedio).mean(),  #obtenemos un valor por cada Año. aplicando nuevamente mean se obtiene un unico valor. O sea el promedio de los promedios anuales
                "Valor promedio mensual": df_datos_eolicos.groupby("Mes")[col].apply(f_calculo_direccion_promedio).mean() #como ante, el promedio de los promedios mensuales
            }

        # convertir resultados en dataframe transposto
        df_resultados_direcciones = pd.DataFrame(resultados_direcciones).T

        #_UNISCE RISULTI VALORI E DIREZIONI______________________________
        for dir in columnas_direcciones:
            df_valores_anuales[dir]=df_direcciones_anuales[dir]
            df_valores_mensuales[dir]=df_direcciones_mensuales[dir]
        #df_resultados_totales=pd.concat(df_resultados_totales,df_resultados_direcciones)
        
        #RESULTADO________________________________________________________
        st.write("Table of values on total period")
        st.write(df_resultados_totales)

        st.write("Table of direction on total period")
        st.write(df_resultados_direcciones)

        st.write("Table of Yearly values")
        st.write(df_valores_anuales)
        #st.session_state["df_valores_anuales"] = df_anuales # initiated session state to access the data in other page

        st.write("Table of Monthly values")
        st.write(df_valores_mensuales)

        #st.write("Table of Hourly values")