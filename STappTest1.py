#cd C:\Users\admin\Desktop\my_venv\venvTK\Scripts
#Activate
#streamlit run "C:\Users\Public\DAN\Danilo2\MasterRE\Modulo6 - Wind\PY_M6_wind\Resource_analysis_ST\welcome.py"

import streamlit as st

st.set_page_config(page_title="Welcome")#, page_icon=":material/waving_hand:")
st.title("Welcome to Wind Resource Analisys 👋")
st.sidebar.success("To start go to Upload file page!")
st.write(
    """
    To start please use the **Upload file** page at left bar 👈

    ### What can this tool do?
    - Calculate the Wind Speed average, maximum, minimum values on a Hourly, Monthly, Annual basis
    - Calculate the Air Density take in to account the air pression and temperature decrease with the height
    - Calculate parameters of interest at the specified height, such as wind speed, air density, turbulence index, etc.
    - Calculate Weibull parameters
    - Time series data analisys
    - Wind rose analisys
    - Weibull analisys
    - Turbolence analisys

    ### The following formulas will be use
     """
)
st.write("")
st.write("1. Temperature variation with altitude [link](https://en.wikipedia.org/wiki/Lapse_rate)")
st.latex(r'''T(h)=T(z_0​)-L \cdot (h−z_0​) ''')
st.write("2. Pressure variation with altitude [link](https://es.wikipedia.org/wiki/F%C3%B3rmula_barom%C3%A9trica)")
st.latex(r'''P(h)=P0 \cdot \left(1-\frac{L\cdot (h-h0)}{T_0}\right)^{(\frac{-g M}{RL})} ''')
st.write("3. Air density variation with altitude")
st.latex(r'''\rho(h)=\frac{P(h)M}{RT(h)}''')
st.write("4. Power density density variation with altitude")
st.latex(r'''P=\frac{1}{2} \cdot \rho \cdot V^3''')


# Preload Python modules that take a while to compile in a new venv.
# Otherwise, when users switch to another page, it seems that Streamlit
# is slow, when in reality this is just an artifact of loading/compiling
# large modules from zero.
with st.spinner("Preloading Python modules for other pages..."):
    import numpy  # noqa: ICN001 F401
    import pandas  # noqa: ICN001 F401
    import plotly
