import streamlit as st
import pandas as pd

def exibir_dashboard():
    st.title("📊 Análise de Dados")
    # Carregando o CSV
    df = pd.read_csv(chocolate.csv)
    st.write("Dados brutos:", df.head())
    
    # Criando um gráfico simples
    st.line_chart(df)

    

