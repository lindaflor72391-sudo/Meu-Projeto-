import streamlit as st
from abas.home import exibir_home
from abas.dashboard import exibir_dashboard

# Menu de navegação lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.selectbox("Ir para:", ["Home", "Gráficos"])

if pagina == "Home":
    exibir_home()
elif pagina == "Gráficos":
    exibir_dashboard()
