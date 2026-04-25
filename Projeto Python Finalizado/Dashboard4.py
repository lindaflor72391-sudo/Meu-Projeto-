import streamlit as st
import pandas as pd
import os

# 1. Configuração inicial
st.set_page_config(page_title="Dashboard Pro", layout="wide")

# 2. CSS - DEGRADÊ GRAFITE/PRATA E BARRA LATERAL
st.markdown("""
    <style>
    /* BARRA LATERAL AZUL ESCURO */
    [data-testid="stSidebar"] {
        background-color: #0e1117 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* CAIXA DE BEM-VINDO: DEGRADÊ GRAFITE PARA PRATA (FORÇADO) */
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
    # Menu atualizado com a opção de Gráficos separada
    tela = st.radio("Escolha a página:", ["Cadastro", "Gráficos", "Upload Customizado"])

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

# --- PÁGINA: GRÁFICOS (ARQUIVO FIXO CHOCOLATE.CSV) ---
elif tela == "Gráficos":
    st.title("📊 Análise: Chocolate.csv")
    nome_arquivo = "chocolate.csv"

    if os.path.exists(nome_arquivo):
        try:
            # Leitura do arquivo local
            df = pd.read_csv(nome_arquivo, sep=None, engine='python', encoding='utf-8-sig')
            df.columns = [str(c).strip() for c in df.columns]

            # Seleção de Colunas
            col1, col2 = st.columns(2)
            colunas_totais = df.columns.tolist()
            
            with col1:
                sel_x = st.selectbox("Selecione a Legenda (Eixo X)", colunas_totais, key="x_choc")
            with col2:
                sel_y = st.selectbox("Selecione o Valor (Eixo Y)", colunas_totais, index=min(1, len(colunas_totais)-1), key="y_choc")

            # Tratamento e Agrupamento (Garante que o gráfico apareça)
            df_temp = df.copy()
            df_temp[sel_y] = pd.to_numeric(df_temp[sel_y], errors='coerce')
            df_temp = df_temp.dropna(subset=[sel_y])
            
            # Agrupa para evitar erros de nomes repetidos
            df_agrupado = df_temp.groupby(sel_x)[sel_y].sum()

            if not df_agrupado.empty:
                st.bar_chart(df_agrupado)
                with st.expander("Ver tabela de dados"):
                    st.write(df)
            else:
                st.warning("Selecione uma coluna numérica para o Eixo Y.")

        except Exception as e:
            st.error(f"Erro ao ler chocolate.csv: {e}")
    else:
        st.error(f"Arquivo '{nome_arquivo}' não encontrado na pasta do script.")

# --- PÁGINA: UPLOAD CUSTOMIZADO ---
else:
    st.title("📂 Upload de Novo Arquivo")
    arquivo = st.file_uploader("Suba seu CSV aqui", type="csv")

    if arquivo:
        try:
            df = pd.read_csv(arquivo, sep=None, engine='python').dropna(how='all')
            st.success("Arquivo carregado com sucesso!")
            
            c_x, c_y = st.columns(2)
            colunas = df.columns.tolist()
            
            with c_x:
                sel_x = st.selectbox("Selecione o Eixo X", colunas)
            with c_y:
                sel_y = st.selectbox("Selecione o Eixo Y", colunas)

            # Preparação do gráfico
            df[sel_y] = pd.to_numeric(df[sel_y], errors='coerce')
            df_plot = df.groupby(sel_x)[sel_y].sum()
            
            st.bar_chart(df_plot)
                
        except Exception as e:
            st.error("Erro ao processar o arquivo. Verifique o formato.")
    else:
        st.info("Aguardando upload do CSV...")
