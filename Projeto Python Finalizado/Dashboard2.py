import streamlit as st
import pandas as pd
import os

# 1. Configuração inicial
st.set_page_config(page_title="Dashboard Pro", layout="wide")

# 2. CSS - DEGRADÊ GRAFITE/PRATA E ESTILO LATERAL
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .caixa-topo {
        background: linear-gradient(90deg, #2c2c2c 0%, #bdc3c7 100%) !important;
        padding: 40px !important;
        border-radius: 15px !important;
        margin-bottom: 30px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .caixa-topo h1 {
        color: white !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🚀 Navegação")
    tela = st.radio("Escolha a página:", ["Cadastro", "Gráficos"])

# --- PÁGINA: CADASTRO ---
if tela == "Cadastro":
    st.markdown('<div class="caixa-topo"><h1>👋 Bem-vindo!</h1></div>', unsafe_allow_html=True)
    st.subheader("Preencha os dados do novo visitante")
    
    with st.form(key="form_limpo", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Nome", key="nome")
            st.number_input("Idade", min_value=0, key="idade")
            st.text_input("Ocupação", key="ocup")
        with c2:
            st.text_input("Telefone", key="tel")
            st.text_input("E-mail", key="email")
        
        if st.form_submit_button("Finalizar Cadastro"):
            st.success("✅ Cadastro realizado com sucesso!")
            st.balloons()

# --- PÁGINA: GRÁFICOS (LEITURA AUTOMÁTICA CHOCOLATE.CSV) ---
else:
    st.title("📊 Análise de Chocolates")
    
    nome_arquivo = "chocolate.csv"

    if os.path.exists(nome_arquivo):
        try:
            # Lê o arquivo tratando separadores e acentos
            df = pd.read_csv(nome_arquivo, sep=None, engine='python', encoding='utf-8-sig')
            
            # Limpa espaços em branco nos nomes das colunas
            df.columns = [str(c).strip() for c in df.columns]

            if not df.empty:
                # Pega as duas primeiras colunas (Nomes e Valores)
                col_nomes = df.columns[0]
                col_valores = df.columns[1]

                # Força a segunda coluna a ser número (ignora erros de texto)
                df[col_valores] = pd.to_numeric(df[col_valores], errors='coerce')
                
                # Remove linhas onde o valor não é um número
                df_limpo = df.dropna(subset=[col_valores])

                st.success(f"Dados carregados: {col_nomes} vs {col_valores}")

                # --- EXIBIÇÃO DO GRÁFICO ---
                # Definimos o índice para o Streamlit saber o que colocar na legenda
                st.bar_chart(df_limpo.set_index(col_nomes)[col_valores])
                
                # Exibe a tabela para conferência
                with st.expander("Visualizar dados brutos"):
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("O arquivo chocolate.csv está vazio.")

        except Exception as e:
            st.error(f"Erro ao processar o gráfico: {e}")
    else:
        st.error(f"Arquivo '{nome_arquivo}' não encontrado.")
        st.info("Coloque o arquivo na mesma pasta do código.")
