import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="ROKFY — Gestão de Eventos", layout="wide")

# Estilização CSS: Sobriedade, Elegância SaaS (Estilo Even3), Fontes Sans-Serif (Sem Serifas)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Reset Global - Apenas Fontes Sem Serifas */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #f3f5f8 !important;
        color: #1e293b !important;
    }

    .stApp {
        background-color: #f3f5f8 !important;
    }

    /* Barra Superior Nativa */
    header[data-testid="stHeader"] {
        background-color: #0f2a36 !important;
    }

    /* Barra Lateral - Cinza Escuro Sobrio */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1f2937 !important;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    /* Identidade ROKFY na Sidebar */
    .brand-container {
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #1f2937;
        margin-bottom: 20px;
    }

    .brand-logo {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        letter-spacing: 3px !important;
        color: #ffffff !important;
        text-transform: uppercase;
        margin: 0;
    }

    .brand-tag {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 1.5px !important;
        color: #0d9488 !important;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Títulos - Totalmente Sem Serifa / Linhas Limpas */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        letter-spacing: -0.3px !important;
    }

    h2 {
        font-size: 1.25rem !important;
        margin-bottom: 16px !important;
        color: #0f2a36 !important;
    }

    /* Top Banner / Header em Azul Petróleo Escuro Sobrio */
    .hero-banner {
        background-color: #0f2a36;
        border-left: 4px solid #0d9488;
        border-radius: 6px;
        padding: 24px 30px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .hero-banner h1 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin: 0 0 6px 0 !important;
    }

    .hero-banner p {
        color: #94a3b8 !important;
        margin: 0 !important;
        font-size: 0.9rem !important;
    }

    /* Cards Brancos Limpos Estilo Even3 */
    .app-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 20px;
    }

    /* Botões em Azul Petróleo com Hover Sobrio */
    .stButton>button {
        background-color: #0f2a36 !important;
        color: #ffffff !important;
        border: 1px solid #0f2a36 !important;
        border-radius: 5px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.55rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        background-color: #134e4a !important;
        border-color: #134e4a !important;
        color: #ffffff !important;
        box-shadow: 0 4px 10px rgba(19, 78, 74, 0.2) !important;
    }

    /* Inputs Limpos */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 5px !important;
    }

    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #0f2a36 !important;
        box-shadow: 0 0 0 3px rgba(15, 42, 54, 0.1) !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    [data-testid="stMetricValue"] {
        color: #0f2a36 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 500 !important;
    }

    /* Certificado Estilo Documento Oficial */
    .cert-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-top: 4px solid #0f2a36;
        border-radius: 6px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .cert-title {
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: 1px;
        color: #0f2a36;
        margin-bottom: 4px;
    }

    .cert-sub {
        font-size: 0.75rem;
        color: #64748b;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 20px;
        font-weight: 600;
    }

    .cert-body {
        font-size: 0.9rem;
        color: #334155;
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
        font-size: 0.78rem;
        color: #64748b;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Logo na Barra Lateral
st.sidebar.markdown(
    """
    <div class="brand-container">
        <div class="brand-logo">ROKFY</div>
        <div class="brand-tag">Gestão de Eventos</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Navegação
opcao = st.sidebar.radio(
    "",
    ["Início & Eventos", "Painel do Organizador", "Emitir Certificados", "Anais do Evento"]
)

# Banner do Topo
st.markdown(
    """
    <div class="hero-banner">
        <h1>ROKFY — Event Management Platform</h1>
        <p>Infraestrutura tecnológica para congressos, simpósios e encontros acadêmicos.</p>
    </div>
    """,
    unsafe_allow_html=True
)

if opcao == "Início & Eventos":
    st.markdown("<h2>Eventos em Destaque</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="app-card">
                <span style="font-size: 0.75rem; color: #134e4a; font-weight: 700; text-transform: uppercase;">Tecnologia</span>
                <h3 style="font-size: 1.05rem; margin: 8px 0 4px 0;">XVI Simpósio de Inteligência Artificial</h3>
                <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 16px;">19 a 21 de Novembro • Curitiba, PR</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Inscrever-se", key="ev1"):
            st.success("Redirecionando para formulário de inscrição...")

    with col2:
        st.markdown(
            """
            <div class="app-card">
                <span style="font-size: 0.75rem; color: #134e4a; font-weight: 700; text-transform: uppercase;">Saúde</span>
                <h3 style="font-size: 1.05rem; margin: 8px 0 4px 0;">Jornada Acadêmica de Inovação Médica</h3>
                <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 16px;">05 a 08 de Dezembro • São Paulo, SP</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Inscrever-se", key="ev2"):
            st.success("Redirecionando para formulário de inscrição...")

    with col3:
        st.markdown(
            """
            <div class="app-card">
                <span style="font-size: 0.75rem; color: #134e4a; font-weight: 700; text-transform: uppercase;">Direito</span>
                <h3 style="font-size: 1.05rem; margin: 8px 0 4px 0;">Congresso Nacional de Direito 2026</h3>
                <p style="font-size: 0.8rem; color: #64748b; margin-bottom: 16px;">12 a 15 de Outubro • Brasília, DF</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Inscrever-se", key="ev3"):
            st.success("Redirecionando para formulário de inscrição...")

elif opcao == "Painel do Organizador":
    st.markdown("<h2>Gestão e Credenciamento</h2>", unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Inscritos Totais", "284")
    col_m2.metric("Credenciados", "190")
    col_m3.metric("Taxa de Presença", "67%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Importar Lista de Inscritos</h3>", unsafe_allow_html=True)
    
    arquivo_csv = st.file_uploader("Selecione o arquivo da planilha (.CSV)", type=["csv"])
    
    if arquivo_csv is not None:
        progress_text = "Processando e validando registros da planilha..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.008)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        time.sleep(0.1)
        my_bar.empty()
        st.success("Planilha importada com sucesso!")
        
        df = pd.read_csv(arquivo_csv)
        st.dataframe(df, use_container_width=True)

elif opcao == "Emitir Certificados":
    st.markdown("<h2>Emissão de Certificados ROKFY</h2>", unsafe_allow_html=True)
    
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Dados do Participante</h3>", unsafe_allow_html=True)
        nome = st.text_input("Nome Completo", "Maria Eduarda Silva")
        evento = st.text_input("Nome do Evento", "XVI Simpósio de Inteligência Artificial")
        horas = st.number_input("Carga Horária (Horas)", min_value=1, value=20)
        codigo = st.text_input("Autenticação Digital", "RKF-2026-9908-X")
        
        if st.button("Gerar Documento"):
            prog_cert = st.progress(0, text="Gerando assinatura digital...")
            for p in range(100):
                time.sleep(0.006)
                prog_cert.progress(p + 1, text="Gerando assinatura digital...")
            prog_cert.empty()
            st.success("Certificado validado!")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown(
            f"""
            <div class="cert-box">
                <div class="cert-title">CERTIFICADO DE PARTICIPAÇÃO</div>
                <div class="cert-sub">SISTEMA INTEGRADO ROKFY</div>
                <div class="cert-body">
                    Certificamos que <b>{nome}</b> participou da atividade 
                    <b>"{evento}"</b>, cumprindo carga horária total de <b>{horas} horas</b>.
                </div>
                <div class="cert-footer">
                    <div style="text-align: left;">
                        <b>Autenticação:</b> {codigo}<br>
                        <span>Validação Digital ROKFY</span>
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
    st.markdown("<h2>Submissão de Trabalhos Acadêmicos</h2>", unsafe_allow_html=True)
    
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    titulo = st.text_input("Título do Artigo / Resumo Expandido")
    autores = st.text_input("Autores e Instituição de Origem")
    pdf_file = st.file_uploader("Upload do Trabalho Completo (.PDF)", type=["pdf"])
    
    if st.button("Submeter Trabalho"):
        if pdf_file is not None:
            bar_pdf = st.progress(0, text="Enviando e indexando documento nos Anais...")
            for i in range(100):
                time.sleep(0.008)
                bar_pdf.progress(i + 1, text="Enviando e indexando documento nos Anais...")
            bar_pdf.empty()
            st.success("Trabalho submetido com sucesso!")
        else:
            st.warning("Selecione um arquivo PDF antes de submeter.")
            
    st.markdown("</div>", unsafe_allow_html=True)
