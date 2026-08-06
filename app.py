import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plataforma de Eventos", layout="wide")

# CSS para visual de Web App SaaS (Estilo Even3: Fundo claro, cabeçalho limpo e cards modernos)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Fundo geral claro de Web App moderno */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f8fafc !important;
        color: #1e293b !important;
    }

    .stApp {
        background-color: #f8fafc !important;
    }

    /* Esconde barra nativa do Streamlit para parecer App nativo */
    header[data-testid="stHeader"] {
        background-color: #1e3a8a !important;
    }

    /* Barra Lateral estilo Dashboard SaaS */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    [data-testid="stSidebar"] * {
        color: #475569 !important;
    }

    /* Títulos e Cabeçalhos */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #0f172a !important;
    }

    h1 {
        font-size: 1.6rem !important;
        letter-spacing: -0.5px !important;
        margin-bottom: 20px !important;
    }

    h2 {
        font-size: 1.25rem !important;
        margin-top: 10px !important;
    }

    /* Cartões e Encartes estilo SaaS */
    .app-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Banner Superior Estilo Even3 */
    .top-hero {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: #ffffff;
        padding: 28px 32px;
        border-radius: 8px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .top-hero h2 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        margin: 0 0 6px 0 !important;
    }

    .top-hero p {
        color: #e0f2fe !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
    }

    /* Botões Modernos e Arredondados em Azul Petróleo/Vibrante */
    .stButton>button {
        background-color: #0284c7 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1.25rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        background-color: #0369a1 !important;
        box-shadow: 0 4px 12px rgba(3, 105, 161, 0.25) !important;
    }

    /* Inputs Limpos */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }

    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #0284c7 !important;
        box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15) !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    [data-testid="stMetricValue"] {
        color: #0284c7 !important;
        font-weight: 700 !important;
    }

    /* Estilo do Certificado Limpo */
    .certificate-container {
        background-color: #ffffff;
        border: 2px solid #0369a1;
        border-radius: 8px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }

    .cert-title {
        color: #0369a1;
        font-weight: 700;
        font-size: 1.3rem;
        letter-spacing: 1px;
    }

    .cert-sub {
        color: #64748b;
        font-size: 0.8rem;
        margin-bottom: 20px;
    }

    .cert-body {
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 20px 0;
    }

    .cert-footer {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        border-top: 1px solid #e2e8f0;
        padding-top: 16px;
        margin-top: 24px;
        font-size: 0.8rem;
        color: #64748b;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Banner Principal Superior estilo Web App
st.markdown(
    """
    <div class="top-hero">
        <h2>Plataforma de Gestão de Eventos</h2>
        <p>Gerencie inscrições, emita certificados com validação digital e publique trabalhos.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Menu Lateral (Sidebar)
st.sidebar.markdown("### Menu Principal")
opcao = st.sidebar.radio(
    "",
    ["Início / Painel", "Inscrições & Participantes", "Emitir Certificados", "Anais do Evento"]
)

if opcao == "Início / Painel":
    col1, col2, col3 = st.columns(3)
    col1.metric("Eventos Ativos", "1")
    col2.metric("Inscrições Confirmadas", "128")
    col3.metric("Certificados Emitidos", "128")

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="app-card">
            <h3>Visão Geral do Evento</h3>
            <p style="color: #64748b; font-size: 0.9rem;">
                Selecione uma das opções no menu lateral para gerenciar as inscrições, 
                configurar a emissão de certificados ou acessar as submissões acadêmicas.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif opcao == "Inscrições & Participantes":
    st.markdown("<h2>Gestão de Inscritos</h2>", unsafe_allow_html=True)
    
    arquivo_csv = st.file_uploader("Importar lista de credenciamento (.CSV)", type=["csv"])
    
    if arquivo_csv is not None:
        df = pd.read_csv(arquivo_csv)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Envie um arquivo CSV com a lista de participantes para carregar a tabela.")

elif opcao == "Emitir Certificados":
    st.markdown("<h2>Emissão e Validação de Certificados</h2>", unsafe_allow_html=True)
    
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.markdown("### Dados do Participante")
        nome = st.text_input("Nome Completo", "Maria Eduarda Silva")
        evento = st.text_input("Nome do Evento", "Congresso Internacional de Tecnologia")
        horas = st.number_input("Carga Horária (Horas)", min_value=1, value=20)
        codigo = st.text_input("Código de Autenticidade", "EV3-2026-9981-X")
        st.button("Gerar Certificado")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown(
            f"""
            <div class="certificate-container">
                <div class="cert-title">CERTIFICADO DE PARTICIPAÇÃO</div>
                <div class="cert-sub">SISTEMA INTEGRADO DE EVENTOS ACADÊMICOS</div>
                <div class="cert-body">
                    Certificamos que <b>{nome}</b> participou do evento <b>"{evento}"</b>, 
                    com carga horária total de <b>{horas} horas</b>.
                </div>
                <div class="cert-footer">
                    <div style="text-align: left;">
                        <b>Código:</b> {codigo}<br>
                        <span>Validação via QR Code</span>
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

elif opcao == "Anais do Evento":
    st.markdown("<h2>Submissão de Trabalhos</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.text_input("Título do Artigo / Resumo")
    st.text_input("Autores")
    st.file_uploader("Arquivo do Trabalho (.PDF)", type=["pdf"])
    st.button("Enviar Submissão")
    st.markdown("</div>", unsafe_allow_html=True)
