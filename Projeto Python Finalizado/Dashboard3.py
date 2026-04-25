import streamlit as st
import pandas as pd
import os

# 1. Configuração inicial
st.set_page_config(page_title="Dashboard Pro", layout="wide")

# 2. CSS - ESTILIZAÇÃO
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0e1117 !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    .caixa-topo {
        background: linear-gradient(90deg, #2c2c2c 0%, #bdc3c7 100%) !important;
        padding: 40px !important;
        border-radius: 15px !important;
        margin-bottom: 30px !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .caixa-topo h1 { color: white !important; margin: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL ---
with st.sidebar:
    st.title("🚀 Navegação")
    tela = st.radio("Escolha a página:", ["Cadastro", "Gráficos"])

# --- PÁGINA: CADASTRO ---
if tela == "Cadastro":
    st.markdown('<div class="caixa-topo"><h1>👋 Bem-vindo!</h1></div>', unsafe_allow_html=True)
    with st.form(key="form_cadastro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Nome", key="nome")
            st.number_input("Idade", min_value=0, key="idade")
        with c2:
            st.text_input("Telefone", key="tel")
            st.text_input("E-mail", key="email")
        if st.form_submit_button("Finalizar"):
            st.success("✅ Cadastro realizado!")

# --- PÁGINA: GRÁFICOS ---
else:
    st.title("📊 Análise de Dados")
    nome_arquivo = "chocolate.csv"

    if os.path.exists(nome_arquivo):
        try:
            # Lê o arquivo tratando possíveis erros de separador
            df = pd.read_csv(nome_arquivo, sep=None, engine='python', encoding='utf-8-sig')
            df.columns = [str(c).strip() for c in df.columns] 

            if not df.empty:
                st.subheader("Configuração do Gráfico")
                col1, col2 = st.columns(2)
                todas_colunas = df.columns.tolist()
                
                with col1:
                    eixo_x = st.selectbox("Legenda (Eixo X):", todas_colunas, index=0)
                with col2:
                    eixo_y = st.selectbox("Valores Numéricos (Eixo Y):", todas_colunas, index=min(1, len(todas_colunas)-1))

                # --- TRATAMENTO DOS DADOS ---
                df_temp = df.copy()
                
                # Converte o Eixo Y para número e remove o que não for numérico
                df_temp[eixo_y] = pd.to_numeric(df_temp[eixo_y], errors='coerce')
                df_temp = df_temp.dropna(subset=[eixo_y])

                # --- AGRUPAMENTO (Essencial para o gráfico aparecer) ---
                # Isso soma os valores do Eixo Y para cada item do Eixo X
                df_para_grafico = df_temp.groupby(eixo_x)[eixo_y].sum()

                # --- EXIBIÇÃO DO GRÁFICO ---
                if not df_para_grafico.empty:
                    st.write(f"### Total de {eixo_y} por {eixo_x}")
                    st.bar_chart(df_para_grafico)
                else:
                    st.warning("Selecione uma coluna com números para o Eixo Y.")
                
                # --- TABELA ---
                with st.expander("Ver dados brutos"):
                    st.dataframe(df, use_container_width=True)
            else:
                st.warning("O arquivo chocolate.csv está vazio.")
                
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
    else:
        st.error(f"Arquivo '{nome_arquivo}' não encontrado na pasta do projeto.")

