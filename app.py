import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plataforma de Eventos", layout="wide")

# Estilização CSS customizada: Azul Petróleo (#0f4c5c), Tons de Cinza Médio/Escuro,
# Estética Moderna/Gótica Leve, Fontes Sem Serifas (Sans-Serif) e Sem Emojis.
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@300;400;600&display=swap');

    /* Configurações Globais */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #12181b;
        color: #e2e8f0;
    }

    .stApp {
        background-color: #12181b;
    }

    /* Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0d1214;
        border-right: 1px solid #1f292d;
    }

    /* Títulos - Tipografia com inspiração gótica moderna (sem serifa pesada) */
    h1, h2, h3, h4 {
        font-family: 'Cinzel', 'Inter', sans-serif !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #f1f5f9 !important;
        font-weight: 600;
    }

    h1 {
        border-bottom: 2px solid #0f4c5c;
        padding-bottom: 10px;
        margin-bottom: 24px;
        font-size: 1.8rem !important;
    }

    h2 {
        font-size: 1.3rem !important;
        color: #cbd5e1 !important;
        margin-top: 15px;
    }

    h3 {
        font-size: 1.0rem !important;
        color: #94a3b8 !important;
    }

    /* Botões em Azul Petróleo */
    .stButton>button {
        background-color: #0f4c5c !important;
        color: #ffffff !important;
        border: 1px solid #1d6a7d !important;
        border-radius: 2px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        background-color: #135f73 !important;
        border-color: #258197 !important;
        box-shadow: 0 0 12px rgba(15, 76, 92, 0.4) !important;
    }

    /* Inputs e Caixas de Texto */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1a2226 !important;
        color: #e2e8f0 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 2px !important;
    }

    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #0f4c5c !important;
        box-shadow: 0 0 5px rgba(15, 76, 92, 0.5) !important;
    }

    /* Componentes de Métricas */
    [data-testid="stMetric"] {
        background-color: #1a2226;
        border: 1px solid #2a3439;
        border-left: 3px solid #0f4c5c;
        padding: 12px;
        border-radius: 2px;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 600;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 1px;
    }

    /* Avisos e Caixas de Informação */
    .stAlert {
        background-color: #161e22 !important;
        color: #cbd5e1 !important;
        border: 1px solid #2a3439 !important;
        border-left: 4px solid #0f4c5c !important;
    }

    /* Card do Certificado */
    .certificate-card {
        border: 1px solid #2a3439;
        border-top: 3px solid #0f4c5c;
        background-color: #161e22;
        padding: 30px;
        border-radius: 2px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }

    .certificate-title {
        font-family: 'Cinzel', 'Inter', sans-serif;
        color: #f1f5f9;
        font-size: 1.3rem;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }

    .certificate-sub {
        color: #64748b;
        font-size: 0.7rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    .certificate-body {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 25px 0;
    }

    .certificate-footer {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid #243036;
        font-size: 0.75rem;
        color: #94a3b8;
    }

    .svg-icon {
        display: inline-block;
        vertical-align: middle;
        fill: #0f4c5c;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown("<h1>PLATAFORMA DE GESTÃO DE EVENTOS ACADÊMICOS</h1>", unsafe_allow_html=True)
st.caption("Módulo de Controle Integrado e Emissão de Documentos")

# Sidebar de Navegação
st.sidebar.markdown("<h3 style='margin-bottom: 15px;'>NAVEGAÇÃO</h3>", unsafe_allow_html=True)
opcao = st.sidebar.radio(
    "",
    ["Painel Geral", "Emissão de Certificados", "Anais e Publicações"]
)

if opcao == "Painel Geral":
    st.markdown("<h2>Painel de Inscrições e Métricas</h2>", unsafe_allow_html=True)
    arquivo_csv = st.file_uploader("Upload da lista de participantes (.CSV)", type=["csv"])
    
    if arquivo_csv is not None:
        df = pd.read_csv(arquivo_csv)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Inscritos", len(df))
        col2.metric("Status da Plataforma", "Ativo")
        col3.metric("Certificados Gerados", len(df))
        
        st.markdown("<h3 style='margin-top:25px;'>Registro de Participantes</h3>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aguardando carregamento de arquivo de dados em formato CSV.")

elif opcao == "Emissão de Certificados":
    st.markdown("<h2>Geração e Validação de Certificados</h2>", unsafe_allow_html=True)
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("<h3>Parâmetros do Documento</h3>", unsafe_allow_html=True)
        nome = st.text_input("Nome Completo", "Maria Eduarda Silva")
        evento = st.text_input("Nome do Evento", "I Simpósio Acadêmico")
        horas = st.number_input("Carga Horária", min_value=1, value=20)
        codigo = st.text_input("Código de Verificação", "AUT-2026-889A-X")
        st.button("Gerar Documento")

    with col_preview:
        st.markdown("<h3>Visualização Prévia</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="certificate-card">
                <div class="certificate-title">CERTIFICADO DE PARTICIPAÇÃO</div>
                <div class="certificate-sub">SISTEMA INTEGRADO DE AUTENTICAÇÃO ACADÊMICA</div>
                <div class="certificate-body">
                    Certificamos que <b>{nome}</b> participou da atividade <b>"{evento}"</b>, 
                    cumprindo carga horária total de <b>{horas} horas</b>.
                </div>
                <div class="certificate-footer">
                    <div style="text-align: left;">
                        <b>Autenticação:</b> {codigo}<br>
                        <svg class="svg-icon" width="12" height="12" viewBox="0 0 24 24">
                            <path d="M3 3h8v8H3zm2 2v4h4V5zm8-2h8v8h-8zm2 2v4h4V5zM3 13h8v8H3zm2 2v4h4v-4zm13-2h3v2h-3zm-3 2h2v3h-2zm3 3h3v3h-3zm-3 1h2v2h-2z"/>
                        </svg> Validação Digital
                    </div>
                    <div style="text-align: right;">
                        _______________________<br>
                        Comissão Organizadora
                    </div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

elif opcao == "Anais e Publicações":
    st.markdown("<h2>Repositório de Publicações</h2>", unsafe_allow_html=True)
    st.text_input("Título da Submissão")
    st.text_input("Autores e Filiação")
    st.file_uploader("Upload do Trabalho (.PDF)", type=["pdf"])
    st.button("Submeter para os Anais")
