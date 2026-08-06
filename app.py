import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Rokfy — Plataforma de Eventos", layout="wide")

# Inicialização de Estado Global
if "eventos" not in st.session_state:
    st.session_state["eventos"] = [
        {
            "nome": "Rokfy Metal & Innovation Fest 2026",
            "categoria": "Festival / Show",
            "vagas": 1500,
            "data": "18/10/2026",
            "local": "Expo Arena Hall",
            "tipo": "Pago",
            "preco": 180.0,
            "pagamentos": ["PIX", "Cartão de Crédito", "Boleto Bancário"]
        }
    ]

# Estilização CSS Avançada: Fonte Chomsky Real, Menu Hambúrguer (3 Traços) e UI Modernizada
custom_css = """
<style>
    /* Importação de Fontes Modernas */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Importação Direta da Fonte Chomsky Oficial */
    @font-face {
        font-family: 'Chomsky';
        src: url('https://cdn.jsdelivr.net/gh/mcdry/chomsky-font@master/Chomsky.otf') format('opentype'),
             url('https://db.onlinewebfonts.com/t/7a165b4526b7d2f9b20e06bd30cbcf82.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }

    /* Reset Global com Design Moderno Arredondado */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #FAF9F6 !important;
        color: #1A1A1A !important;
    }

    .stApp {
        background-color: #FAF9F6 !important;
    }

    /* Subtituição Visual do Botão da Sidebar (Flechas >> por 3 Traços ☰) */
    button[data-testid="stSidebarCollapseButton"] svg,
    button[aria-label="Close sidebar"] svg,
    button[aria-label="Open sidebar"] svg {
        display: none !important;
    }

    button[data-testid="stSidebarCollapseButton"]::after,
    button[aria-label="Close sidebar"]::after,
    button[aria-label="Open sidebar"]::after {
        content: "☰" !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        color: #1A1A1A !important;
        display: block !important;
        text-align: center;
    }

    /* Top Navigation Bar */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        padding: 14px 28px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #EAE6DF;
        margin-bottom: 25px;
    }

    .nav-links {
        display: flex;
        gap: 24px;
    }

    .nav-link-item {
        color: #555555;
        font-weight: 600;
        font-size: 0.92rem;
        text-decoration: none;
        transition: color 0.2s;
        cursor: pointer;
    }

    .nav-link-item:hover {
        color: #E05A47;
    }

    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {
        background-color: #F4F1EA !important;
        border-right: 1px solid #E5E0D8 !important;
    }

    /* Logo Rokfy em Fonte Chomsky Legítima */
    .brand-logo {
        font-family: 'Chomsky', 'UnifrakturMaguntia', serif !important;
        font-size: 3.6rem !important;
        color: #E05A47 !important;
        text-align: center;
        margin: 0;
        padding: 0;
        line-height: 0.9;
        letter-spacing: -1px;
    }

    .brand-tag {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        letter-spacing: 3px !important;
        color: #1A1A1A !important;
        text-transform: uppercase;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 20px;
    }

    .divider-line {
        height: 1px;
        background: linear-gradient(90deg, rgba(224,90,71,0) 0%, rgba(224,90,71,0.3) 50%, rgba(224,90,71,0) 100%);
        margin: 15px 0 25px 0;
    }

    /* Hero Banner Fluido e Moderno */
    .hero-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F1E8 100%);
        border-radius: 20px;
        padding: 36px;
        border: 1px solid #EAE6DF;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 30px;
    }

    .hero-card h1 {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
        margin-bottom: 8px !important;
    }

    .hero-card p {
        font-size: 1rem !important;
        color: #666666 !important;
        margin: 0 !important;
    }

    /* Cards com Cantos Soft Arredondados */
    .rokfy-card-modern {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 28px;
        border: 1px solid #EAE6DF;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 20px;
    }

    .rokfy-card-modern:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    }

    /* Botões Modernos e Arredondados */
    .stButton>button {
        background-color: #E05A47 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        padding: 0.65rem 1.6rem !important;
        box-shadow: 0 4px 12px rgba(224, 90, 71, 0.2) !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        background-color: #C84B39 !important;
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(224, 90, 71, 0.35) !important;
    }

    /* Certificados Elegantes */
    .cert-container {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 35px;
        border: 2px solid #1A1A1A;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    .cert-title-chomsky {
        font-family: 'Chomsky', serif;
        font-size: 2.8rem;
        color: #1A1A1A;
        margin-bottom: 5px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Barra de Navegação Superior (Home, Sobre Nós, Quem Somos, Contato)
st.markdown(
    """
    <div class="top-navbar">
        <div style="font-weight: 800; font-size: 1.1rem; color: #E05A47;">ROKFY PLATFORM</div>
        <div class="nav-links">
            <span class="nav-link-item">Home</span>
            <span class="nav-link-item">Sobre Nós</span>
            <span class="nav-link-item">Quem Somos</span>
            <span class="nav-link-item">Contato</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar com Logo em Fonte Chomsky e Menu
st.sidebar.markdown('<div class="brand-logo">Rokfy</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-tag">Gestão Integrada de Eventos</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

opcao = st.sidebar.radio(
    "Navegação do Sistema",
    [
        "Home / Apresentação",
        "Criar e Configurar Evento",
        "Eventos Cadastrados",
        "Anais de Eventos",
        "Emissão de Certificados",
        "Sobre Nós / Contato"
    ]
)

# JANELA 1: HOME
if opcao == "Home / Apresentação":
    st.markdown(
        """
        <div class="hero-card">
            <h1>Plataforma Completa para Gestão de Eventos e Festivais</h1>
            <p>Gerencie inscrições, bilhetagem com pagamento via PIX e Cartão, emissão em lote de certificados e anais acadêmicos em uma única experiência.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown(
            """
            <div class="rokfy-card-modern">
                <h3 style="color: #E05A47; margin-bottom: 8px;">Gestão Simplicada</h3>
                <p style="font-size: 0.9rem; color: #666;">Crie eventos pagos ou gratuitos com controle exato de vagas, upload de banners e múltiplos meios de pagamento.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_f2:
        st.markdown(
            """
            <div class="rokfy-card-modern">
                <h3 style="color: #E05A47; margin-bottom: 8px;">Certificação em Lote</h3>
                <p style="font-size: 0.9rem; color: #666;">Anexe planilhas CSV e gerencie chancela digital para participantes, organizadores, palestrantes e comissão.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_f3:
        st.markdown(
            """
            <div class="rokfy-card-modern">
                <h3 style="color: #E05A47; margin-bottom: 8px;">Anais & Repositório</h3>
                <p style="font-size: 0.9rem; color: #666;">Publique os anais dos seus eventos com código ISSN/ISBN e repositório de artigos integrado.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# JANELA 2: CRIAR EVENTO
elif opcao == "Criar e Configurar Evento":
    st.markdown(
        """
        <div class="hero-card">
            <h1>Criar Novo Evento</h1>
            <p>Preencha os dados básicos, limites de vagas e meios de recebimento.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.form(key="form_criar_evento"):
        c1, c2 = st.columns([2, 1])
        with c1:
            nome_ev = st.text_input("Nome do Evento", placeholder="Ex: Rokfy Innovation Summit 2026")
            desc_ev = st.text_area("Descrição do Evento", placeholder="Apresentação do evento e programação...")
        with c2:
            cat_ev = st.selectbox("Categoria", ["Congresso", "Festival / Show", "Simpósio", "Workshop"])
            vagas_ev = st.number_input("Limite de Vagas", min_value=10, max_value=50000, value=500)
            data_ev = st.date_input("Data de Realização")
            local_ev = st.text_input("Localização / Link", placeholder="Ex: Centro de Convenções")

        banner_file = st.file_uploader("Upload de Banner / Imagem Principal", type=["png", "jpg", "jpeg"])
        
        tipo_ev = st.radio("Modelo de Evento:", ["Gratuito", "Pago"])
        preco_ev = 0.0
        meios = []
        
        if tipo_ev == "Pago":
            cp1, cp2 = st.columns([1, 2])
            with cp1:
                preco_ev = st.number_input("Preço do Ingresso (R$)", min_value=1.0, value=150.0)
            with cp2:
                st.write("Opções de Pagamento:")
                if st.checkbox("PIX", value=True): meios.append("PIX")
                if st.checkbox("Cartão de Crédito", value=True): meios.append("Cartão de Crédito")
                if st.checkbox("Boleto Bancário"): meios.append("Boleto Bancário")
                if st.checkbox("Transferência Bancária"): meios.append("Transferência Bancária")

        if st.form_submit_button("Publicar Evento"):
            if nome_ev:
                st.session_state["eventos"].append({
                    "nome": nome_ev,
                    "categoria": cat_ev,
                    "vagas": vagas_ev,
                    "data": str(data_ev),
                    "local": local_ev,
                    "tipo": tipo_ev,
                    "preco": preco_ev,
                    "pagamentos": meios
                })
                st.success(f"Evento '{nome_ev}' cadastrado com sucesso!")
            else:
                st.error("Informe o nome do evento.")

# JANELA 3: EVENTOS CADASTRADOS
elif opcao == "Eventos Cadastrados":
    st.markdown("<h2>Eventos Ativos</h2>", unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, ev in enumerate(st.session_state["eventos"]):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="rokfy-card-modern">
                    <span style="background: #FDF0ED; color: #E05A47; font-size: 0.75rem; font-weight: 800; padding: 4px 10px; border-radius: 6px;">{ev['categoria']}</span>
                    <h3 style="margin-top: 10px;">{ev['nome']}</h3>
                    <p style="font-size: 0.9rem; color: #555;">
                        <b>Data:</b> {ev['data']} | <b>Vagas:</b> {ev['vagas']}<br>
                        <b>Local:</b> {ev['local']}<br>
                        <b>Valor:</b> {f'R$ {ev["preco"]:.2f}' if ev['tipo'] == 'Pago' else 'Gratuito'}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

# JANELA 4: ANAIS DE EVENTOS (CONDICIONADO)
elif opcao == "Anais de Eventos":
    st.markdown("<h2>Anais de Eventos</h2>", unsafe_allow_html=True)
    if not st.session_state["eventos"]:
        st.warning("É necessário cadastrar um evento antes de criar os Anais.")
    else:
        st.markdown("<div class='rokfy-card-modern'>", unsafe_allow_html=True)
        ev_sel = st.selectbox("Selecione o Evento:", [e["nome"] for e in st.session_state["eventos"]])
        titulo_anais = st.text_input("Título dos Anais", value=f"Anais Oficiais - {ev_sel}")
        issn = st.text_input("ISSN / ISBN", placeholder="Ex: 2447-8821")
        file_anais = st.file_uploader("Arquivo PDF dos Anais", type=["pdf"])
        if st.button("Publicar Anais"):
            st.success("Anais vinculados e publicados com sucesso!")
        st.markdown("</div>", unsafe_allow_html=True)

# JANELA 5: EMISSÃO DE CERTIFICADOS
elif opcao == "Emissão de Certificados":
    st.markdown("<h2>Emissão e Validação de Certificados</h2>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.markdown("<div class='rokfy-card-modern'>", unsafe_allow_html=True)
        mod_cert = st.selectbox("Modalidade", ["Participante", "Organizador", "Comissão Científica", "Palestrante", "Ministrante de Curso"])
        nome_p = st.text_input("Nome do Contemplado", "Carlos Eduardo Lima")
        ev_cert = st.selectbox("Evento Vinculado", [e["nome"] for e in st.session_state["eventos"]])
        horas = st.number_input("Carga Horária", value=20)
        st.file_uploader("Anexar Planilha para Emissão em Lote (.CSV)", type=["csv"])
        if st.button("Gerar Certificado"):
            st.success("Certificado gerado com sucesso!")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_c2:
        st.markdown(
            f"""
            <div class="cert-container">
                <div class="cert-title-chomsky">Certificado Oficial</div>
                <div style="color: #E05A47; font-weight: 800; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 20px;">
                    ROKFY PLATFORM • {mod_cert.upper()}
                </div>
                <p style="font-size: 0.95rem; color: #333; line-height: 1.6;">
                    Certificamos que <b>{nome_p}</b> participou na condição de <b>{mod_cert}</b> do evento 
                    <b>"{ev_cert}"</b>, totalizando a carga horária de <b>{horas} horas</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

# JANELA 6: SOBRE NÓS / QUEM SOMOS / CONTATO
elif opcao == "Sobre Nós / Contato":
    st.markdown(
        """
        <div class="hero-card">
            <h1>Sobre a Rokfy</h1>
            <p>A Rokfy é uma plataforma de tecnologia voltada para a curadoria, gestão e publicação de eventos com atitude.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(
            """
            <div class="rokfy-card-modern">
                <h3>Quem Somos</h3>
                <p style="color: #555; font-size: 0.95rem;">
                    Nossa missão é simplificar a gestão de festivais, simpósios e congressos acadêmicos, oferecendo ferramentas robustas para organizadores e uma experiência fluida para os participantes.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_info2:
        st.markdown(
            """
            <div class="rokfy-card-modern">
                <h3>Entre em Contato</h3>
                <p style="color: #555; font-size: 0.95rem;">
                    <b>Atendimento:</b> contato@rokfy.com.br<br>
                    <b>Suporte ao Organizador:</b> +55 (11) 99999-8888<br>
                    <b>Atendimento Comercial:</b> Segunda a Sexta, das 09h às 18h.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
