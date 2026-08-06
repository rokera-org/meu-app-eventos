import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Rokfy — The Sound & Events", layout="wide")

# Estilização Editorial NYT + Rock Elegante (Fundo Bege, Salmão, Fonte Gótica no Logo)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Fundo Bege Claro Editorial estilo NYT */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-color: #FBF9F5 !important;
        color: #121212 !important;
    }

    .stApp {
        background-color: #FBF9F5 !important;
    }

    /* Barra Superior */
    header[data-testid="stHeader"] {
        background-color: #FBF9F5 !important;
        border-bottom: 1px solid #E2DED4;
    }

    /* Sidebar - Estilo Peraminho/Editorial com Borda Dupla */
    [data-testid="stSidebar"] {
        background-color: #F4F1EA !important;
        border-right: 2px solid #E2DED4 !important;
    }

    [data-testid="stSidebar"] * {
        color: #121212 !important;
    }

    /* Nome ROKFY com Fonte Gótica tipo Chomsky/NYT e cor Salmão */
    .brand-logo {
        font-family: 'UnifrakturMaguntia', 'Chomsky', serif !important;
        font-size: 3.2rem !important;
        color: #E05A47 !important; /* Cor Salmão */
        text-align: center;
        margin: 0;
        padding: 10px 0 0 0;
        line-height: 1;
        text-shadow: 1px 1px 0px rgba(0,0,0,0.1);
    }

    .brand-tag {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        color: #121212 !important;
        text-transform: uppercase;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    /* Divisória Estilo Jornal NYT (Linhas Duplas) */
    .nyt-divider {
        border-top: 3px double #121212;
        margin: 15px 0 25px 0;
    }

    /* Banner Principal */
    .hero-editorial {
        background-color: #F4F1EA;
        border: 1px solid #E2DED4;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }

    .hero-editorial h1 {
        font-family: 'UnifrakturMaguntia', serif !important;
        color: #121212 !important;
        font-size: 2.4rem !important;
        margin: 0 0 8px 0 !important;
    }

    .hero-editorial p {
        color: #555555 !important;
        font-size: 1rem !important;
        margin: 0 !important;
    }

    /* Cards Interativos e Orgânicos (Sem visual quadrado duro) */
    .interactive-card {
        background-color: #ffffff;
        border: 1px solid #E2DED4;
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        margin-bottom: 20px;
        position: relative;
    }

    .interactive-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 24px rgba(224, 90, 71, 0.12);
        border-color: #E05A47;
    }

    .badge-rock {
        display: inline-block;
        background-color: #FDF0ED;
        color: #E05A47;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 20px;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    /* Botões Interativos em Salmão */
    .stButton>button {
        background-color: #E05A47 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 30px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1.6rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(224, 90, 71, 0.25) !important;
    }

    .stButton>button:hover {
        background-color: #C84B39 !important;
        transform: scale(1.03) !important;
        box-shadow: 0 6px 18px rgba(224, 90, 71, 0.35) !important;
    }

    /* Métricas Interativas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #E2DED4;
        border-radius: 14px;
        padding: 18px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    [data-testid="stMetricValue"] {
        color: #E05A47 !important;
        font-weight: 700 !important;
    }

    /* Inputs Limpos e Arredondados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #121212 !important;
        border: 1px solid #E2DED4 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
    }

    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #E05A47 !important;
        box-shadow: 0 0 0 3px rgba(224, 90, 71, 0.15) !important;
    }

    /* Certificado Estilo Relíquia/Editorial */
    .cert-frame {
        background-color: #ffffff;
        border: 2px solid #121212;
        border-radius: 12px;
        padding: 36px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        position: relative;
    }

    .cert-frame::after {
        content: "🎸";
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 1.5rem;
        opacity: 0.2;
    }

    .cert-title {
        font-family: 'UnifrakturMaguntia', serif;
        font-size: 2rem;
        color: #121212;
        margin-bottom: 5px;
    }

    .cert-sub {
        color: #E05A47;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Logo na Barra Lateral
st.sidebar.markdown('<div class="brand-logo">Rokfy</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-tag">Events & Experiences</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)

# Navegação
opcao = st.sidebar.radio(
    "Navegação",
    ["⚡ Lineup & Eventos", "📊 Painel de Controle", "📜 Certificados & Passaporte", "🎵 Submeter Trabalhos"]
)

# Banner Principal
st.markdown(
    """
    <div class="hero-editorial">
        <h1>The Rokfy Journal</h1>
        <p>A experiência definitiva em curadoria de eventos, festivais e congressos de atitude.</p>
    </div>
    """,
    unsafe_allow_html=True
)

if opcao == "⚡ Lineup & Eventos":
    st.markdown("<h3>Próximos Festivais e Encontros</h3>", unsafe_allow_html=True)
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="interactive-card">
                <span class="badge-rock">🎸 Rock & Tech</span>
                <h3 style="font-size: 1.2rem; margin: 6px 0;">Rock In Tech Summit 2026</h3>
                <p style="font-size: 0.85rem; color: #666; margin-bottom: 15px;">
                    📍 Arena Hall • 22 de Outubro<br>
                    Inovação, música e tecnologia em uma só imersão.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Garantir Ingressos", key="ev1"):
            st.toast("🔥 Inscrição iniciada para o Rock In Tech Summit!", icon="🎟️")

    with col2:
        st.markdown(
            """
            <div class="interactive-card">
                <span class="badge-rock">🎷 Jazz & Academics</span>
                <h3 style="font-size: 1.2rem; margin: 6px 0;">Congresso de Acústica</h3>
                <p style="font-size: 0.85rem; color: #666; margin-bottom: 15px;">
                    📍 Teatro Universitário • 14 de Novembro<br>
                    Engenharia de som e produção musical moderna.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Garantir Ingressos", key="ev2"):
            st.toast("🎷 Inscrição iniciada para o Congresso de Acústica!", icon="🎟️")

    with col3:
        st.markdown(
            """
            <div class="interactive-card">
                <span class="badge-rock">⚡ Indie & Design</span>
                <h3 style="font-size: 1.2rem; margin: 6px 0;">Design & Distortion</h3>
                <p style="font-size: 0.85rem; color: #666; margin-bottom: 15px;">
                    📍 Espaço Cultural • 02 de Dezembro<br>
                    Identidade visual e cultura underground.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Garantir Ingressos", key="ev3"):
            st.toast("⚡ Inscrição iniciada para Design & Distortion!", icon="🎟️")

elif opcao == "📊 Painel de Controle":
    st.markdown("<h3>Gestão do Evento & Credenciamento</h3>", unsafe_allow_html=True)
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Público Confirmado", "1.420", "+12% esta semana")
    col_m2.metric("Credenciamentos VIP", "380", "100% esgotado")
    col_m3.metric("Taxa de Engajamento", "94%", "Alta adesão")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="interactive-card">
            <h4>📁 Carregar Lista de Participantes</h4>
            <p style="font-size: 0.85rem; color: #666;">Faça o upload do arquivo CSV para processar as credenciais instantaneamente com animação de leitura.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    arquivo_csv = st.file_uploader("", type=["csv"])
    
    if arquivo_csv is not None:
        progress_bar = st.progress(0, text="⚡ Sincronizando credenciais no sistema Rokfy...")

        for percent in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent + 1, text="⚡ Sincronizando credenciais no sistema Rokfy...")
        
        time.sleep(0.1)
        progress_bar.empty()
        st.success("🎉 Base de inscritos atualizada com sucesso!")
        
        df = pd.read_csv(arquivo_csv)
        st.dataframe(df, use_container_width=True)

elif opcao == "📜 Certificados & Passaporte":
    st.markdown("<h3>Emissão de Certificado de Presença</h3>", unsafe_allow_html=True)
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    col_form, col_preview = st.columns([1, 1.1])
    
    with col_form:
        st.markdown("<div class='interactive-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Dados do Participante</h4>", unsafe_allow_html=True)
        nome = st.text_input("Nome Completo", "Lucas 'Hendrix' Oliveira")
        evento = st.text_input("Nome do Evento", "Rock In Tech Summit 2026")
        horas = st.number_input("Carga Horária (Horas)", min_value=1, value=30)
        codigo = st.text_input("Código de Autenticidade", "RKF-NYT-8821")
        
        if st.button("Assinar & Emitir Documento"):
            bar_cert = st.progress(0, text="🖋️ Gerando chancela digital com estilo editorial...")
            for i in range(100):
                time.sleep(0.006)
                bar_cert.progress(i + 1, text="🖋️ Gerando chancela digital com estilo editorial...")
            bar_cert.empty()
            st.toast("Documento assinado com sucesso!", icon="📜")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown(
            f"""
            <div class="cert-frame">
                <div class="cert-title">Certificate of Attendance</div>
                <div class="cert-sub">ROKFY OFFICIAL EDITION</div>
                <div style="font-size: 0.95rem; color: #333; margin: 25px 0; line-height: 1.7;">
                    Atestamos para os devidos fins que <b>{nome}</b> participou com distinção do evento 
                    <b>"{evento}"</b>, totalizando uma carga de <b>{horas} horas</b>.
                </div>
                <div style="border-top: 1px double #121212; padding-top: 15px; display: flex; justify-content: space-between; font-size: 0.78rem; color: #555;">
                    <div><b>Hash:</b> {codigo}</div>
                    <div><b>Autenticação:</b> Rokfy Verified ⚡</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

elif opcao == "🎵 Submeter Trabalhos":
    st.markdown("<h3>Submissão de Artigos & Projetos</h3>", unsafe_allow_html=True)
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("<div class='interactive-card'>", unsafe_allow_html=True)
    titulo = st.text_input("Título do Trabalho / Artigo")
    autores = st.text_input("Autores Principais")
    pdf_file = st.file_uploader("Upload do Arquivo (.PDF)", type=["pdf"])
    
    if st.button("Enviar Submissão"):
        if pdf_file is not None:
            prog_pdf = st.progress(0, text="🎵 Enviando arquivo para a banca curadora...")
            for p in range(100):
                time.sleep(0.008)
                prog_pdf.progress(p + 1, text="🎵 Enviando arquivo para a banca curadora...")
            prog_pdf.empty()
            st.balloons()
            st.success("🚀 Trabalho enviado com sucesso para a curadoria do Rokfy!")
        else:
            st.warning("Anexe o PDF do seu trabalho antes de prosseguir.")
            
    st.markdown("</div>", unsafe_allow_html=True)
