import streamlit as st 
import pandas as pd 
import os 
 
# 1. Configuração inicial 
st.set_page_config(page_title="Dashboard Pro", layout="wide") 
 
# 2. CSS - Degradê grafite/prata na barra lateral 
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
 
# 3. Menu lateral
with st.sidebar: 
    st.title("🚀 Navegação") 
    tela = st.radio("Escolha a página:", ["Cadastro", "Gráficos", "Upload Customizado"]) 
 
# 4. Página de Cadastro 
if tela == "Cadastro": 
    st.markdown('<div class="caixa-topo"><h1> 👋 Bem-vindo!</h1></div>', 
unsafe_allow_html=True) 
    st.subheader("Preencha os dados do novo visitante") 
     
    with st.form(key="form_limpo", clear_on_submit=True): 
        c1, c2 = st.columns(2) 
        with c1: 
            nome = st.text_input("Nome", key="nome") # Removi o key para capturar a variável 
            idade = st.number_input("Idade", min_value=0, key="idade") 
            ocupacao = st.text_input("Ocupação", key="ocup") 
        with c2: 
            telefone = st.text_input("Telefone", key="tel") 
            email = st.text_input("E-mail", key="email")
            cidade = st.text_input("Cidade", key="cidade") 
         
        if st.form_submit_button("Finalizar Cadastro"): 
            #Salvando os dados 
            arquivo_destino = "cadastros.csv" 
             
            #Dicionário com os novos dados a serem salvos
            novos_dados = { 
                "Nome": [nome], 
                "Idade": [idade], 
                "Ocupação": [ocupacao], 
                "Telefone": [telefone], 
                "E-mail": [email],
                "Cidade": [cidade],
            } 
            df_novo = pd.DataFrame(novos_dados) 
             
            # Salva no CSV: mode='a' (anexa), header=so se o arquivo nao existir 
            df_novo.to_csv(arquivo_destino, mode='a', index=False,  
                           header=not os.path.exists(arquivo_destino), encoding='utf-8-sig') 
            
 
            st.success("✅ Cadastro realizado com sucesso!")
            st.balloons() 
 
# 5.GRÁFICOS (arquivo base fixa) --- 
elif tela == "Gráficos": 
    st.title("📊 Análise: Chocolate.csv") 
    nome_arquivo = "chocolate.csv" 
 
    if os.path.exists(nome_arquivo): 
        try: 
            df = pd.read_csv(nome_arquivo, sep=None, engine='python', encoding='utf-8-sig') 
            df.columns = [str(c).strip() for c in df.columns] 
            col1, col2 = st.columns(2) 
            colunas_totais = df.columns.tolist() 
            with col1: 
                sel_x = st.selectbox("Selecione a Legenda (Eixo X)", colunas_totais, 
key="x_choc") 
            with col2: 
                sel_y = st.selectbox("Selecione o Valor (Eixo Y)", colunas_totais, index=min(1, 
len(colunas_totais)-1), key="y_choc") 
            df_temp = df.copy() 
            df_temp[sel_y] = pd.to_numeric(df_temp[sel_y], errors='coerce') 
            df_temp = df_temp.dropna(subset=[sel_y]) 
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
 
# 6. UPLOAD CUSTOMIZADO (arquivo novo)
else: 
    st.title("   Upload de Novo Arquivo") 
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
            df[sel_y] = pd.to_numeric(df[sel_y], errors='coerce') 
            df_plot = df.groupby(sel_x)[sel_y].sum() 
            st.bar_chart(df_plot) 
            with st.expander("Ver dados brutos do arquivo"): 
                st.dataframe(df, use_container_width=True) 
        except Exception as e: 
            st.error("Erro ao processar o arquivo. Verifique o formato.") 
    else: 
        st.info("Aguardando upload do CSV...")