import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="calculations")#, page_icon=":material/table:")
st.title("Overview")
st.text(
    """
    The following calculations can be performed:
    1. Calculation data at the selected altitude
    2. Extrapolating data to a new altitude
    """)
@st.dialog("File format")
def file_format_popup():
    st.write("""
    About the file format, the column headers must contain the following strings to allow the variables to be correctly recognized.
    1. **Date and time**: Date/Time
    1. **Speed**: "Speed", "Velocidad"
    2. **Direction**: "Dir", "Veleta"
    3. **Standard deviation**: "Std", "Dev"
    4. **Temperature**: "temp"
    """)
if st.button("File format"):
    file_format_popup()





st.title("Calculation data at the selected altitude")
st.text("""
    Calculates parameters of interest at a specified measured altitude. These parameters include, air density, turbulence, etc.
    Submit multiple time to calculate at different altitudes.
    """)
if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    opziones_velocidades = [col for col in df_datos_eolicos.columns if "Velocidad" in col]
    colV = st.selectbox("Select a wind speed:", opziones_velocidades, index=0)
    
    opziones_std = [col for col in df_datos_eolicos.columns if "Std" in col]
    colDev= st.selectbox("Select a std:", opziones_std, index=0)
    
    # Create a text input box with a default placeholder
    h_text = st.text_input("Enter the altitude [m] corresponding to wind speed", "100")

    opziones_temp= [col for col in df_datos_eolicos.columns if "temp" in col]
    colTemp= st.selectbox("Select a temperature:", opziones_temp, index=0)

    try:
        h = int(h_text)
    except ValueError:
        h=None

    if (h is None) or (colV is None) or (colDev is None):
        st.error("Please define all the variable above")
    else:
        # Display the name after clicking the Submit button
        if st.button("Submit"):
            # Paso 5: Extrapolar la temperatura, presion, densidad de aire, y densidad de potencia a las altitudes deseadas
            L= 0.0065 #K/m en aire libre #ley temperatura
            P0=101325      #a nivel del mar [Pa] #Ley pression
            T0=288.15      #a nivel del mar [K]
            R=8.3144598    #costante gas universale [J/(mol·K)]
            g=9.80665      #[m/s^2]
            M=0.0289644    #[kg/mol]
            #R_aire=287.05 #[J/kg*K]
            my_expo=(g*M)/(R*L)
            #for h in altura_extrapoladas:
            df_datos_eolicos[f"Temperatura a {h}m [°C]"]=df_datos_eolicos[colTemp] - L*(h-5)
            df_datos_eolicos[f"Presión a {h}m [Pa]"]= P0*(1-L*(h-0)/T0)**my_expo
            df_datos_eolicos[f"Densidad aire a {h}m [Kg/m3]"]= (df_datos_eolicos[f"Presión a {h}m [Pa]"]*M) / (R*(df_datos_eolicos[f"Temperatura a {h}m [°C]"]+273.15))
            df_datos_eolicos["Densidad de potencia a "+ str(h)+ "m [W/m2]"]= 0.5*df_datos_eolicos[f"Densidad aire a {h}m [Kg/m3]"]*df_datos_eolicos[colV]**3
            df_datos_eolicos["Indice de Turbolencia a "+ str(h)+ "m"]= df_datos_eolicos[colDev] / df_datos_eolicos[colV]

            st.write("Previw of first 3 line of results")
            st.write(df_datos_eolicos.head(3))
            st.session_state["df_datos_eolicos"] = df_datos_eolicos # initiated session state to access the data in other page








st.title("Extrapolating data to a new altitude")
st.text("""
    Calculates parameters of interest at a specified altitude from at least two measurements. These parameters include velocity, air density, turbulence, etc.
    - Measurement 1: Set of altitude, velocity, direction, and reference standard deviation.
    - Measurement 2: Altitude, velocity 2
    - Altitude 1 > Altitude 2
    Run multiple time to extrapolate different altitudes
    """)
if 'df_datos_eolicos' not in st.session_state:
    st.error('Please go back to <Upload file> page and upload a file.')
else:
    df_datos_eolicos = st.session_state["df_datos_eolicos"] #take the data from the page upload data

    #Create dropdowns menu____________________________
    opziones_velocidades = [col for col in df_datos_eolicos.columns if "Velocidad" in col]
    colV1 = st.selectbox("Select wind speed 1:", opziones_velocidades, index=0)
    colV2 = st.selectbox("Select wind speed 2:", opziones_velocidades, index=1)
    
    opziones_std = [col for col in df_datos_eolicos.columns if "Std" in col]
    colDev1= st.selectbox("Select reference std:", opziones_std, index=0)
    
    opziones_dir = [col for col in df_datos_eolicos.columns if "Veleta" in col]
    colDir1= st.selectbox("Select reference direction:", opziones_dir, index=0)

    opziones_temp= [col for col in df_datos_eolicos.columns if "temp" in col]
    colTemp1= st.selectbox("Select reference temperature:", opziones_temp, index=0)

    # Create a text input box with a default placeholder
    h1_text = st.text_input("Enter the altitude [m] corresponding to wind speed 1", "100")
    h2_text = st.text_input("Enter the altitude [m] corresponding to wind speed 2", "80")
    he_text = st.text_input("Enter the altitude [m] to calculate the parameters of interest ", "120")

    try:
        h1 = int(h1_text)
    except ValueError:
        h1=None

    try:
        h2 = int(h2_text)
    except ValueError:
        h2=None

    try:
        h = int(he_text)
    except ValueError:
        h=None

    if (h1 is None) or (h2 is None) or (colV1 is None) or (colV2 is None) or (colDev1 is None) or (h is None) or (colDir1 is None) or (colTemp1 is None):
        st.error("Please define all the variable above")
    else:
        # Display the name after clicking the Submit button
        if st.button("Run"):
            #NB: desde aqui en adelante vamos a estimar todo con V1=V100, o sea tendremo esa como Vref, href, Std_ref, direcion_ref

            # Paso 1: Obtener la velocidad media durante el período a la altitud de referencia (medida), o bien, reduzco los datos a un único valor. Seria igual a lo que ocurre al usar una base de datos web donde solo tengo un valor para el año típico (actividad A4).
            V1=df_datos_eolicos[colV1].mean()  #a 100m
            V2=df_datos_eolicos[colV2].mean()  #a 80m

            # Paso 2: Calcular el exponente de cizalladura del viento (α) y la longitud de rugosidad (Z0).
            alpha=np.log(V1/V2)/ (h1/h2)  #log(V100/V80)/(100/80)
            st.write("alpha:       ", alpha)

            kappa=0.41
            #Z0=np.exp(  (V1/V2 -1)*(h1-h2) /kappa)  #prof
            #print("Z0:          ", Z0)

            #DD
            Z01=np.exp( (V2*np.log(h1) - V1*np.log(h2))/ (V2-V1) )  #calcolo mio da v2/v1=ln(z1/z0)/ln(z2/z0)
            st.write("Z0", Z01)
            ustar=kappa*(V1-V2)/np.log(h1/h2)
            st.write("u*:          ", ustar)
            Z0_1=h1/np.exp(V1*kappa/ustar)
            st.write("Z0_",h1,":      ", Z0_1)
            Z0_2=h2/np.exp(V2*kappa/ustar)
            st.write("Z0_",h2,":      ", Z0_2)

            # Paso 3: Extrapolar la velocidad del viento a las altitudes deseadas utilizando las leyes exponencial y logarítmica.            
            #for h in altura_extrapoladas:
            df_datos_eolicos[f"Velocidad (potencial) a {h}m [m/s]"]= df_datos_eolicos[colV1] * (h/h1)**alpha                        #DD
            df_datos_eolicos[f"Velocidad (logaritmica) a {h}m [m/s]"]= df_datos_eolicos[colV1] * (np.log(h/Z01)/np.log(h1/Z01))     #DD


            # Paso 4: Extrapolar la dirección del viento a las altitudes deseadas
            #for h in altura_extrapoladas:
            #direccion_promedio=df_datos_eolicos["Veleta a 100  [°]"].mean()  #df_datos_eolicos.columns[5]
            df_datos_eolicos[f"Dirección a {h}m [°]"]=df_datos_eolicos[colDir1]

            # Paso 5: Extrapolar la temperatura, presion, densidad de aire, y densidad de potencia a las altitudes deseadas
            L= 0.0065 #K/m en aire libre #ley temperatura
            P0=101325      #a nivel del mar [Pa] #Ley pression
            T0=288.15      #a nivel del mar [K]
            R=8.3144598    #costante gas universale [J/(mol·K)]
            g=9.80665      #[m/s^2]
            M=0.0289644    #[kg/mol]
            #R_aire=287.05 #[J/kg*K]
            my_expo=(g*M)/(R*L)
            #for h in altura_extrapoladas:
            df_datos_eolicos[f"Temperatura a {h}m [°C]"]=df_datos_eolicos[colTemp1] - L*(h-5)
            df_datos_eolicos[f"Presión a {h}m [Pa]"]= P0*(1-L*(h-0)/T0)**my_expo
            df_datos_eolicos[f"Densidad aire a {h}m [Kg/m3]"]= (df_datos_eolicos[f"Presión a {h}m [Pa]"]*M) / (R*(df_datos_eolicos[f"Temperatura a {h}m [°C]"]+273.15))
            df_datos_eolicos["Densidad de potencia a "+ str(h)+ "m [W/m2]"]= 0.5*df_datos_eolicos[f"Densidad aire a {h}m [Kg/m3]"]*df_datos_eolicos[f"Velocidad (potencial) a {h}m [m/s]"]**3     

            # Paso 6: Extrapolar la densidad de potencia y turbolencia a las altitudes deseadas
            #for h in altura_extrapoladas:
            df_datos_eolicos["Indice de Turbolencia a "+ str(h)+ "m"]= df_datos_eolicos[colDev1] / df_datos_eolicos[f"Velocidad (potencial) a {h}m [m/s]"]

            st.write("Previw of first 3 line of results")
            st.write(df_datos_eolicos.head(3))
            st.session_state["df_datos_eolicos"] = df_datos_eolicos # initiated session state to access the data in other page

