import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Rokfy — Plataforma de Eventos", layout="wide")

# CSS: Identidade Visual Rokfy (SaaS Claro + Elementos Rock/Gótico Elegante)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Fundo Geral */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }

    .stApp {
        background-color: #f1f5f9 !important;
    }

    /* Topo e Header */
    header[data-testid="stHeader"] {
        background-color: #0d131a !important;
    }

    /* Sidebar - Gótico Limpo */
    [data-testid="stSidebar"] {
        background-color: #0d131a !important;
        border-right: 2px solid #0f4c5c !important;
    }

    [data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* Logotipo ROKFY */
    .brand-title {
        font-family: 'Cinzel', serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: 4px !important;
        color: #ffffff !important;
        text-transform: uppercase;
        margin: 0;
        padding-bottom: 2px;
    }

    .brand-subtitle {
        font-size: 0.72rem !important;
        letter-spacing: 2px !important;
        color: #38bdf8 !important;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Tipografia de Títulos */
    h1, h2, h3, h4 {
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        letter-spacing: 1px;
    }

    h2 {
        font-size: 1.4rem !important;
        border-bottom: 2px solid #0f4c5c;
        padding-bottom: 8px;
        margin-bottom: 20px !important;
    }

    /* Hero Banner Principal */
    .hero-rokfy {
        background: linear-gradient(135deg, #0d131a 0%, #0f4c5c 100%);
        border-left: 5px solid #38bdf8;
        padding: 28px 36px;
        border-radius: 6px;
        color: #ffffff;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(15, 76, 92, 0.3);
    }

    .hero-rokfy h1 {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        margin: 0 0 6px 0 !important;
        letter-spacing: 2px !important;
    }

    .hero-rokfy p {
        color: #94a3b8 !important;
        margin: 0 !important;
        font-size: 0.95rem !important;
    }

    /* Cards e Containers com Sombra e Borda Sutil */
    .rokfy-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 3px solid #0f4c5c;
        border-radius: 6px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    .event-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 20px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    .event-card:hover {
        transform: translateY(-3px);
        border-color: #0f4c5c;
        box-shadow: 0 8px 20px rgba(15, 76, 92, 0.15);
    }

    /* Botões Padrão Rokfy */
    .stButton>button {
        background-color: #0f4c5c !important;
        color: #ffffff !important;
        border: 1px solid #135f73 !important;
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.25s ease !important;
    }

    .stButton>button:hover {
        background-color: #0d131a !important;
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        box-shadow: 0 4px 14px rgba(13, 19, 26, 0.3) !important;
    }

    /* Inputs e Caixas */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 4px !important;
    }

    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #0f4c5c !important;
        box-shadow: 0 0 0 3px rgba(15, 76, 92, 0.15) !important;
    }

    /* Métricas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0f4c5c;
        border-radius: 4px;
        padding: 16px;
    }

    [data-testid="stMetricValue"] {
        color: #0f4c5c !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
    }

    /* Certificado Gótico Elegante */
    .certificate-container {
        background-color: #ffffff;
        border: 2px solid #0d131a;
        border-radius: 4px;
        padding: 36px;
        text-align: center;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
        position: relative;
    }

    .certificate-container::before {
        content: "";
        position: absolute;
        top: 8px; left: 8px; right: 8px; bottom: 8px;
        border: 1px solid #0f4c5c;
        pointer-events: none;
    }

    .cert-title {
        font-family: 'Cinzel', serif;
        color: #0d131a;
        font-weight: 700;
        font-size: 1.4rem;
        letter-spacing: 3px;
    }

    .cert-sub {
        color: #0f4c5c;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        font-weight: 600;
    }

    .cert-body {
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.7;
        margin: 25px 0;
    }

    .cert-footer {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        border-top: 1px solid #cbd5e1;
        padding-top: 20px;
        margin-top: 28px;
        font-size: 0.78rem;
        color: #64748b;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Logo na Barra Lateral
st.sidebar.markdown('<div class="brand-title">ROKFY</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-subtitle">Plataforma Acadêmica & Eventos</div>', unsafe_allow_html=True)

# Navegação
opcao = st.sidebar.radio(
    "",
    ["Início & Eventos", "Painel do Organizador", "Emitir Certificados", "Anais do Evento"]
)

# Header Fixo
st.markdown(
    """
    <div class="hero-rokfy">
        <h1>ROKFY — EVENT MANAGEMENT</h1>
        <p>Gestão completa para simpósios, congressos e encontros acadêmicos.</p>
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
            <div class="event-card">
                <span style="font-size: 0.7rem; color: #0f4c5c; font-weight: 700; letter-spacing: 1px;">TECNOLOGIA & IA</span>
                <h3 style="font-size: 1.1rem; margin: 8px 0;">XVI Simpósio de IA</h3>
                <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 12px;">19 a 21 de Novembro • Auditório Central</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Inscrever-se", key="ev1"):
            st.success("Inscrição iniciada para o XVI Simpósio de IA!")

    with col2:
        st.markdown(
            """
            <div class="event-card">
                <span style="font-size: 0.7rem; color: #0f4c5c; font-weight: 700; letter-spacing: 1px;">SAÚDE & MEDICINA</span>
                <h3 style="font-size: 1.1rem; margin: 8px 0;">Jornada de Inovação Médica</h3>
                <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 12px;">05 a 08 de Dezembro • Centro de Convenções</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Inscrever-se", key="ev2"):
            st.success("Inscrição iniciada para a Jornada de Inovação Médica!")

    with col3:
        st.markdown(
            """
            <div class="event-card">
                <span style="font-size: 0.7rem; color: #0f4c5c; font-weight: 700; letter-spacing: 1px;">DIREITO & SOCIEDADE</span>
                <h3 style="font-size: 1.1rem; margin: 8px 0;">Congresso Jurídico 2026</h3>
                <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 12px;">12 a 15 de Outubro • Bloco Acadêmico</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Inscrever-se", key="ev3"):
            st.success("Inscrição iniciada para o Congresso Jurídico!")

elif opcao == "Painel do Organizador":
    st.markdown("<h2>Gestão e Credenciamento</h2>", unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Inscritos Totais", "284")
    col_m2.metric("Credenciados", "190")
    col_m3.metric("Taxa de Presença", "67%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Importar Lista de Participantes</h3>", unsafe_allow_html=True)
    
    arquivo_csv = st.file_uploader("Selecione o arquivo da planilha (.CSV)", type=["csv"])
    
    if arquivo_csv is not None:
        progress_text = "Processando e validando registros da planilha..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        time.sleep(0.2)
        my_bar.empty()
        st.success("Planilha importada com sucesso!")
        
        df = pd.read_csv(arquivo_csv)
        st.dataframe(df, use_container_width=True)

elif opcao == "Emitir Certificados":
    st.markdown("<h2>Emissão de Certificados Rokfy</h2>", unsafe_allow_html=True)
    
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.markdown("<div class='rokfy-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Dados do Documento</h3>", unsafe_allow_html=True)
        nome = st.text_input("Nome Completo", "Maria Eduarda Silva")
        evento = st.text_input("Nome do Evento", "XVI Simpósio de Inteligência Artificial")
        horas = st.number_input("Carga Horária (Horas)", min_value=1, value=20)
        codigo = st.text_input("Autenticação Digital", "RKF-2026-9908-X")
        
        if st.button("Gerar Documento"):
            prog_cert = st.progress(0, text="Gerando assinatura digital...")
            for p in range(100):
                time.sleep(0.008)
                prog_cert.progress(p + 1, text="Gerando assinatura digital...")
            prog_cert.empty()
            st.success("Certificado validado!")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown(
            f"""
            <div class="certificate-container">
                <div class="cert-title">CERTIFICADO DE PARTICIPAÇÃO</div>
                <div class="cert-sub">PLATAFORMA ACADÊMICA ROKFY</div>
                <div class="cert-body">
                    Certificamos que <b>{nome}</b> participou com êxito da atividade 
                    <b>"{evento}"</b>, cumprindo carga horária total de <b>{horas} horas</b>.
                </div>
                <div class="cert-footer">
                    <div style="text-align: left;">
                        <b>Autenticação:</b> {codigo}<br>
                        <span>Validação Rokfy Digital</span>
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
    
    st.markdown("<div class='rokfy-card'>", unsafe_allow_html=True)
    titulo = st.text_input("Título do Artigo / Resumo Expandido")
    autores = st.text_input("Autores e Instituição de Origem")
    pdf_file = st.file_uploader("Upload do Trabalho Completo (.PDF)", type=["pdf"])
    
    if st.button("Submeter Trabalho"):
        if pdf_file is not None:
            bar_pdf = st.progress(0, text="Enviando e indexando documento nos Anais...")
            for i in range(100):
                time.sleep(0.01)
                bar_pdf.progress(i + 1, text="Enviando e indexando documento nos Anais...")
            bar_pdf.empty()
            st.success("Trabalho enviado para a comissão científica com sucesso!")
        else:
            st.warning("Selecione um arquivo PDF antes de submeter.")
            
    st.markdown("</div>", unsafe_allow_html=True)
