import streamlit as st
import pandas as pd

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
    tela = st.radio("Escolha a página:", ["Cadastro", "Gráficos & Upload"])

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

# --- PÁGINA: GRÁFICOS ---
else:
    st.title("📊 Análise de Dados")
    arquivo = st.file_uploader("Suba seu CSV aqui", type="csv")

    if arquivo:
        try:
            # Leitura robusta (detecta vírgula ou ponto e vírgula)
            df = pd.read_csv(arquivo, sep=None, engine='python').dropna(how='all')
            
            # TRADUÇÃO DAS OPÇÕES DA LISTA (PT-BR)
            dicionario = {
                'name': 'Nome', 'age': 'Idade', 'sales': 'Vendas', 
                'value': 'Valor', 'city': 'Cidade', 'date': 'Data'
            }
            df = df.rename(columns=dicionario)
            
            st.success("Arquivo carregado!")

            # --- EIXOS X E Y ---
            colunas_totais = df.columns.tolist()
            # Tenta pegar apenas números para o Y, se não houver, pega tudo
            colunas_num = df.select_dtypes(include=['number']).columns.tolist()
            if not colunas_num: colunas_num = colunas_totais

            c_x, c_y = st.columns(2)
            
            with c_x:
                # Título em PT-BR e seleção do X
                sel_x = st.selectbox("Selecione o Eixo X", colunas_totais)
            
            with c_y:
                # Título em PT-BR e seleção do Y
                sel_y = st.selectbox("Selecione o Eixo Y", colunas_num)

            # GRÁFICO AUTOMÁTICO
            if sel_x and sel_y:
                # Limpeza final para não dar erro no gráfico
                dados_grafico = df[[sel_x, sel_y]].copy()
                dados_grafico[sel_y] = pd.to_numeric(dados_grafico[sel_y], errors='coerce')
                dados_grafico = dados_grafico.dropna()
                
                st.bar_chart(dados_grafico.set_index(sel_x))
                
        except Exception as e:
            st.error(f"Erro ao processar o arquivo. Verifique se as colunas estão corretas.")
    else:
        st.info("Aguardando upload do CSV...")
