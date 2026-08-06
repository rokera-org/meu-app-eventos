import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rokfy — Plataforma de Eventos", layout="wide")

# Estado Global
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

# Estilização CSS: Fundo Bege + Shapes Orgânicos Salmão (Ondas Fluidas)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Tentar fonte Chomsky local do computador */
    @font-face {
        font-family: 'Chomsky';
        src: local('Chomsky'), local('Chomsky Regular'), local('Chomsky-Regular');
        font-weight: normal;
        font-style: normal;
    }

    /* Fundo Global em Bege Editorial Conforme Combinado */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #FAF6EE !important; /* Bege Claro Editorial */
        color: #1A1A1A !important;
    }

    .stApp {
        background-color: #FAF6EE !important;
    }

    /* Ícone do Menu Hambúrguer (Substitui as setas << >>) */
    button[data-testid="stSidebarCollapseButton"] svg,
    button[aria-label="Close sidebar"] svg,
    button[aria-label="Open sidebar"] svg {
        display: none !important;
    }

    button[data-testid="stSidebarCollapseButton"]::after,
    button[aria-label="Close sidebar"]::after,
    button[aria-label="Open sidebar"]::after {
        content: "☰" !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
        display: block !important;
        line-height: 1 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F3ECE0 !important;
        border-right: 1px solid #E5DBD0 !important;
    }

    .brand-logo-text {
        font-family: 'Chomsky', 'UnifrakturMaguntia', 'Old English Text MT', serif !important;
        font-size: 3.8rem !important;
        color: #E05A47 !important;
        text-align: center;
        margin: 0;
        padding: 0;
        line-height: 0.9;
    }

    .brand-tag {
        font-size: 0.65rem !important;
        font-weight: 800 !important;
        letter-spacing: 3px !important;
        color: #1A1A1A !important;
        text-transform: uppercase;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    /* Navbar Superior */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        padding: 14px 28px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        margin-bottom: 25px;
    }

    /* Shape Orgânico Salmão Flutuante (Onda Fluida de Ponta a Ponta) */
    .shape-container-top {
        width: 100%;
        background-color: #FA8072;
        border-radius: 24px 24px 0 0;
        padding: 35px 35px 15px 35px;
        color: #FFFFFF !important;
        position: relative;
    }

    .shape-container-top h1, .shape-container-top p {
        color: #FFFFFF !important;
    }

    /* Wave SVG que conecta o Shape Salmão ao Fundo Bege */
    .wave-divider {
        width: 100%;
        height: 60px;
        margin-bottom: 25px;
    }

    .wave-divider path {
        fill: #FA8072;
    }

    /* Cards e Containers Brancos */
    .rokfy-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 26px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid #EAE0D5;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #E05A47 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.6rem !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Top Bar
st.markdown(
    """
    <div class="top-navbar">
        <div style="font-weight: 800; font-size: 1.1rem; color: #E05A47;">ROKFY PLATFORM</div>
        <div style="display:flex; gap:20px; font-weight:600; font-size:0.9rem;">
            <span>Home</span>
            <span>Sobre Nós</span>
            <span>Quem Somos</span>
            <span>Contato</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar com Logo
st.sidebar.markdown('<div class="brand-logo-text">Rokfy</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-tag">Gestão Integrada de Eventos</div>', unsafe_allow_html=True)

opcao = st.sidebar.radio(
    "Navegação",
    [
        "Home / Apresentação",
        "Criar e Configurar Evento",
        "Eventos Cadastrados",
        "Anais de Eventos",
        "Emissão de Certificados",
        "Sobre Nós / Contato"
    ]
)

# Renderização do Shape Irregular Salmão (Topo Curvado que se funde ao bege)
def render_header_shape(titulo, sub-titulo):
    st.markdown(
        f"""
        <div class="shape-container-top">
            <h1 style="margin:0;">{titulo}</h1>
            <p style="margin-top:5px; opacity: 0.9;">{sub-titulo}</p>
        </div>
        <svg class="wave-divider" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,133.3C672,139,768,181,864,186.7C960,192,1056,160,1152,138.7C1248,117,1344,107,1392,101.3L1440,96L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
        </svg>
        """,
        unsafe_allow_html=True
    )

# 1. HOME
if opcao == "Home / Apresentação":
    render_header_shape("Plataforma Completa de Eventos", "Gestão de inscrições, emissão de certificados e publicação de anais.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="rokfy-card"><h3>Gestão de Eventos</h3><p style="color:#666;">Crie e gerencie eventos com ingressos pagos via PIX e cartão.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="rokfy-card"><h3>Certificação</h3><p style="color:#666;">Emissão em lote para palestrantes, organizadores e inscritos.</p></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="rokfy-card"><h3>Anais & ISSN</h3><p style="color:#666;">Repositório completo para artigos e volumes acadêmicos.</p></div>', unsafe_allow_html=True)

# 2. CRIAR EVENTO
elif opcao == "Criar e Configurar Evento":
    render_header_shape("Novo Evento", "Preencha as configurações e meios de pagamento.")
    
    with st.form(key="form_criar_evento"):
        c1, c2 = st.columns([2, 1])
        with c1:
            nome_ev = st.text_input("Nome do Evento")
            desc_ev = st.text_area("Descrição")
        with c2:
            cat_ev = st.selectbox("Categoria", ["Congresso", "Festival / Show", "Simpósio"])
            vagas_ev = st.number_input("Limite de Vagas", value=300)
            data_ev = st.date_input("Data")
            
        if st.form_submit_button("Salvar Evento"):
            if nome_ev:
                st.session_state["eventos"].append({"nome": nome_ev, "categoria": cat_ev, "vagas": vagas_ev, "data": str(data_ev), "local": "Auditório", "tipo": "Gratuito", "preco": 0.0, "pagamentos": []})
                st.success("Evento salvo!")

# 3. EVENTOS CADASTRADOS
elif opcao == "Eventos Cadastrados":
    render_header_shape("Eventos Cadastrados", "Lista de eventos cadastrados no sistema.")
    cols = st.columns(2)
    for idx, ev in enumerate(st.session_state["eventos"]):
        with cols[idx % 2]:
            st.markdown(f'<div class="rokfy-card"><h3>{ev["nome"]}</h3><p>{ev["categoria"]} • {ev["vagas"]} vagas</p></div>', unsafe_allow_html=True)

# 4. ANAIS DE EVENTOS
elif opcao == "Anais de Eventos":
    render_header_shape("Anais de Eventos", "Publicação e indexação de volumes acadêmicos.")
    if not st.session_state["eventos"]:
        st.warning("Cadastre um evento primeiro para poder publicar anais.")
    else:
        st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
        st.selectbox("Evento Vinculado", [e["nome"] for e in st.session_state["eventos"]])
        st.text_input("ISSN / ISBN")
        st.file_uploader("Upload PDF dos Anais", type=["pdf"])
        if st.button("Publicar Anais"):
            st.success("Anais publicados!")
        st.markdown('</div>', unsafe_allow_html=True)

# 5. CERTIFICADOS
elif opcao == "Emissão de Certificados":
    render_header_shape("Emissão de Certificados", "Gere certificados individuais ou via planilha CSV.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
        st.selectbox("Modalidade", ["Participante", "Organizador", "Comissão Científica", "Palestrante", "Ministrante de Curso"])
        st.text_input("Nome", "Carlos Silva")
        st.file_uploader("Importar Planilha CSV (Lote)", type=["csv"])
        if st.button("Gerar Certificados"):
            st.success("Certificados gerados com sucesso!")
        st.markdown('</div>', unsafe_allow_html=True)

# 6. SOBRE NÓS
elif opcao == "Sobre Nós / Contato":
    render_header_shape("Sobre a Rokfy", "Conheça mais sobre nossa solução.")
    st.markdown('<div class="rokfy-card"><h3>Quem Somos</h3><p>Plataforma para gestão de eventos acadêmicos e culturais.</p></div>', unsafe_allow_html=True)
    
