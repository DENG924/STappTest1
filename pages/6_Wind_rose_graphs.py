import streamlit as st
import pandas as pd
import numpy as np
#import plotly.graph_objects as go
import matplotlib.pyplot as plt  #per rosa di viento

st.set_page_config(page_title="Wind rose analysis")#, page_icon=":material/table:")
st.title("Wind rose analysis")
#st.text("")

if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    opziones_dir = [col for col in df_datos_eolicos.columns if "Veleta" in col]
    columna_direccion= st.selectbox("Select reference direction:", opziones_dir, index=0)

    opziones_velocidades = [col for col in df_datos_eolicos.columns if "Velocidad" in col]
    columna_velocidad = st.selectbox("Select a wind speed:", opziones_velocidades, index=0)

    opziones_std = [col for col in df_datos_eolicos.columns if "Std" in col]
    columna_std= st.selectbox("Select a std:", opziones_std, index=0)
  
    bins = st.slider("Choose number of sectors", min_value=8, max_value=32)

    #fecha_inicio1=widgets.DatePicker(description="Fecha inicio:", value=df_datos_eolicos.index[0].date())  #value=datetime.date(2019, 7, 9)
    #fecha_fin1=widgets.DatePicker(description="Fecha fin:", value=df_datos_eolicos.last_valid_index().date())

    if st.button("Run"):
        #columna_direccion=selector_direciones.value
        #columna_velocidad=selector_velocidad.value
        #columna_std=selector_std.value
        #fecha_inicio
        #fecha_fin
        #bins=selector_sector.value

        #filtrar por fechas si especificada
        #if fecha_inicio and fecha_fin:
        #    df=df.loc[fecha_inicio:fecha_fin]
        
        #eiminar filas con valores nan
        df_limpio=df_datos_eolicos[[columna_direccion,columna_velocidad,columna_std]].dropna()
        direcciones=df_limpio[columna_direccion]
        velocidades=df_limpio[columna_velocidad]
        stds=df_limpio[columna_std]

        #definir intervalos pra la rosa de los vientos
        sectores=np.linspace(0,360,bins+1)  

        #calculo valores de interes por sector
        y_avg=np.zeros(len(sectores)-1)
        y_min=np.zeros(len(sectores)-1)
        y_max=np.zeros(len(sectores)-1)
        dev=np.zeros(len(sectores)-1)
        turbolencia=np.zeros(len(sectores)-1)
        for i in range(len(sectores)-1):
            #print(i,sectores[i],sectores[i+1])
            if(np.any((direcciones>=sectores[i]) & (direcciones<sectores[i+1]))): 
                y_avg[i]=velocidades[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])].mean()
                y_min[i]=velocidades[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])].min()
                y_max[i]=velocidades[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])].max()
                dev[i]=velocidades[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])].std()  #prof
                #dev[i]=stds[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])].mean()
                turbolencia[i]=(stds[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])] / velocidades[(direcciones>=sectores[i]) & (direcciones<sectores[i+1])]).mean()
            #else:
            #    y_avg[i]=0    #o igual if(np.isnan(y_avg[i])): y_avg[i]=0
        #st.write("sectores", sectores)
        #st.write("Velocidad promedias:",y_avg)
        #st.write("Velocidad min:",y_min)
        #st.write("Velocidad max:",y_max)
        #st.write("Velocidad dev:",dev)
        #st.write("turbolencia:",turbolencia)
        
        #st.writ(velocidades[(direcciones>=sectores_rad[4]) & (direcciones<sectores_rad[5])].min())
        #st.writ(np.any((direcciones>=sectores_rad[4]) & (direcciones<sectores_rad[5])))

        
        #Rosa de Frequencia Absoluta
        fig, ax = plt.subplots(subplot_kw=dict(polar=True)) #plt.subplots(1,2 oppure 2,2,...per 4 grafici
        #axs[0] #se ho 2 grafici
        #axs[0,0] #se ho 4 grafici
        ax.bar(np.deg2rad(sectores[:-1]), np.histogram(direcciones,bins=sectores)[0],width=np.deg2rad(360/bins),alpha=0.7, color="blue")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Frequencia Absoluta")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()

        #Rosa de Frequencia Relativa [%]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.bar(np.deg2rad(sectores[:-1]), np.histogram(direcciones,bins=sectores)[0] /len(direcciones)*100,width=np.deg2rad(360/bins),alpha=0.7, color="green")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Frequencia Relativa [%]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()


        #Rosa de Velocidad promedia [m/s]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.bar(np.deg2rad(sectores[:-1]), y_avg,width=np.deg2rad(360/bins),alpha=0.7, color="red")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Velocidad promedia [m/s]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()

        #Rosa de Velocidad minima [m/s]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.bar(np.deg2rad(sectores[:-1]), y_min,width=np.deg2rad(360/bins),alpha=0.7, color="purple")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Velocidad minima [m/s]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()

        #Rosa de Velocidad maxima [m/s]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.bar(np.deg2rad(sectores[:-1]), y_max,width=np.deg2rad(360/bins),alpha=0.7, color="orange")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Velocidad maxima [m/s]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()

        #Rosa de desviación estándar [m/s]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.bar(np.deg2rad(sectores[:-1]), dev,width=np.deg2rad(360/bins),alpha=0.7, color="cyan")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Desviación estándar de Velocidad [m/s]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()

        #Rosa de turbolencia [1]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.bar(np.deg2rad(sectores[:-1]), turbolencia,width=np.deg2rad(360/bins),alpha=0.7, color="magenta")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Rosa de Turbolencia [1]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        st.pyplot(fig) #plt.show()

        #Datos de viento [1]
        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.scatter(np.deg2rad(direcciones), velocidades,alpha=0.5, color="blue")  #se black attiva cambio colore asse
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.set_title("Scatter plot Velocidad de viento [m/s]")
        plt.xticks(np.arange(0, 6.28, 6.28/bins, dtype=float))
        #ax.yaxis.label.set_color('blue')          #setting up Y-axis label color to blue
        #ax.tick_params(axis='y', colors='blue')  #setting up Y-axis tick color to 
        st.pyplot(fig) #plt.show()

        st.write("sectores", sectores)
        st.write("Velocidad promedias:",y_avg)
        st.write("Velocidad min:",y_min)
        st.write("Velocidad max:",y_max)
        st.write("Velocidad dev:",dev)
        st.write("turbolencia:",turbolencia)
