import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Rokfy — Gestão de Eventos", layout="wide")

# Inicialização de Estado Global (Persistência de Eventos Criados)
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

# Estilização Editorial NYT + Rock Elegante (Bege, Salmão, Fonte Gótica no Logo)
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Fundo Bege Claro Editorial */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-color: #FBF9F5 !important;
        color: #121212 !important;
    }

    .stApp {
        background-color: #FBF9F5 !important;
    }

    header[data-testid="stHeader"] {
        background-color: #FBF9F5 !important;
        border-bottom: 1px solid #E2DED4;
    }

    [data-testid="stSidebar"] {
        background-color: #F4F1EA !important;
        border-right: 2px solid #E2DED4 !important;
    }

    [data-testid="stSidebar"] * {
        color: #121212 !important;
    }

    /* Logo Rokfy em Fonte Gótica tipo Chomsky */
    .brand-logo {
        font-family: 'UnifrakturMaguntia', 'Chomsky', serif !important;
        font-size: 3.4rem !important;
        color: #E05A47 !important;
        text-align: center;
        margin: 0;
        padding: 5px 0 0 0;
        line-height: 1;
    }

    .brand-tag {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        letter-spacing: 3px !important;
        color: #121212 !important;
        text-transform: uppercase;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 20px;
    }

    .nyt-divider {
        border-top: 3px double #121212;
        margin: 15px 0 25px 0;
    }

    .hero-editorial {
        background-color: #F4F1EA;
        border: 1px solid #E2DED4;
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }

    .hero-editorial h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #121212 !important;
        font-size: 1.6rem !important;
        margin: 0 0 6px 0 !important;
    }

    .hero-editorial p {
        color: #555555 !important;
        font-size: 0.95rem !important;
        margin: 0 !important;
    }

    .rokfy-card {
        background-color: #ffffff;
        border: 1px solid #E2DED4;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }

    .badge-tag {
        display: inline-block;
        background-color: #FDF0ED;
        color: #E05A47;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .stButton>button {
        background-color: #E05A47 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.4rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton>button:hover {
        background-color: #C84B39 !important;
        box-shadow: 0 4px 12px rgba(224, 90, 71, 0.25) !important;
    }

    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div {
        background-color: #ffffff !important;
        color: #121212 !important;
        border: 1px solid #E2DED4 !important;
        border-radius: 6px !important;
    }

    /* Molduras para Modelos de Certificado */
    .cert-frame-classic {
        background-color: #ffffff;
        border: 2px solid #121212;
        border-radius: 8px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0,0,0,0.04);
    }

    .cert-frame-modern {
        background-color: #ffffff;
        border-left: 6px solid #E05A47;
        border-top: 1px solid #E2DED4;
        border-right: 1px solid #E2DED4;
        border-bottom: 1px solid #E2DED4;
        border-radius: 8px;
        padding: 28px;
        text-align: center;
    }

    .cert-title {
        font-family: 'UnifrakturMaguntia', serif;
        font-size: 2rem;
        color: #121212;
        margin-bottom: 2px;
    }

    .cert-sub {
        color: #E05A47;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 18px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Logo na Barra Lateral
st.sidebar.markdown('<div class="brand-logo">Rokfy</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-tag">Gestão Integrada de Eventos</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)

# Navegação
opcao = st.sidebar.radio(
    "Menu do Sistema",
    [
        "Criar e Configurar Evento",
        "Eventos Cadastrados",
        "Anais de Eventos",
        "Emissão de Certificados",
        "Painel do Organizador"
    ]
)

# 1. JANELA: CRIAR E CONFIGURAR EVENTO
if opcao == "Criar e Configurar Evento":
    st.markdown(
        """
        <div class="hero-editorial">
            <h1>Cadastro e Publicação de Evento</h1>
            <p>Configure o evento, defina limite de participantes, imagens e parâmetros de bilhetagem.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    with st.form(key="form_criar_evento"):
        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            nome_ev = st.text_input("Nome do Evento", placeholder="Ex: II Simpósio de Biotecnologia & Rock")
            desc_ev = st.text_area("Descrição Detalhada", placeholder="Informações do evento...")
        
        with col_b:
            cat_ev = st.selectbox("Categoria", ["Congresso", "Festival / Show", "Simpósio", "Workshop", "Encontro Acadêmico"])
            vagas_ev = st.number_input("Limite de Participantes", min_value=10, max_value=100000, value=300)
            data_ev = st.date_input("Data do Evento")
            local_ev = st.text_input("Local ou Plataforma Virtual", placeholder="Ex: Auditório Principal")

        st.markdown("<br>", unsafe_allow_html=True)
        banner_file = st.file_uploader("Upload do Banner / Imagem de Divulgação", type=["png", "jpg", "jpeg"])
        if banner_file:
            st.image(banner_file, caption="Pré-visualização do Banner", use_column_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        tipo_ev = st.radio("Modelo de Cobrança:", ["Gratuito", "Pago"])
        preco_ev = 0.0
        meios = []
        
        if tipo_ev == "Pago":
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                preco_ev = st.number_input("Valor da Inscrição (R$)", min_value=1.0, value=120.0)
            with col_p2:
                st.write("Formas de Pagamento Aceitas:")
                if st.checkbox("PIX", value=True): meios.append("PIX")
                if st.checkbox("Cartão de Crédito", value=True): meios.append("Cartão de Crédito")
                if st.checkbox("Boleto Bancário"): meios.append("Boleto Bancário")
                if st.checkbox("Transferência Bancária"): meios.append("Transferência Bancária")

        if st.form_submit_button("Salvar e Publicar Evento"):
            if not nome_ev:
                st.error("Preencha o nome do evento.")
            else:
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

# 2. JANELA: EVENTOS CADASTRADOS
elif opcao == "Eventos Cadastrados":
    st.markdown(
        """
        <div class="hero-editorial">
            <h1>Eventos Cadastrados no Sistema</h1>
            <p>Lista de eventos ativos disponíveis para gerenciamento e inscrições.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    if not st.session_state["eventos"]:
        st.info("Nenhum evento cadastrado no momento.")
    else:
        cols = st.columns(2)
        for idx, ev in enumerate(st.session_state["eventos"]):
            with cols[idx % 2]:
                st.markdown(
                    f"""
                    <div class="rokfy-card">
                        <span class="badge-tag">{ev['categoria']}</span>
                        <h3>{ev['nome']}</h3>
                        <p style="font-size: 0.88rem; color: #555;">
                            <b>Data:</b> {ev['data']}<br>
                            <b>Local:</b> {ev['local']}<br>
                            <b>Limite de Participantes:</b> {ev['vagas']} vagas<br>
                            <b>Modalidade:</b> {ev['tipo']} {f'- R$ {ev["preco"]:.2f}' if ev['tipo'] == 'Pago' else ''}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# 3. JANELA: ANAIS DE EVENTOS (CONDICIONADA À EXISTÊNCIA DE EVENTOS)
elif opcao == "Anais de Eventos":
    st.markdown(
        """
        <div class="hero-editorial">
            <h1>Publicação de Anais e Trabalhos Acadêmicos</h1>
            <p>Criação de anais e repositórios vinculados a eventos ativos na plataforma.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    if not st.session_state["eventos"]:
        st.warning("Atenção: É necessário cadastrar pelo menos um evento antes de criar e publicar os Anais do Evento.")
    else:
        st.markdown("<h3>Criar Edição dos Anais</h3>", unsafe_allow_html=True)
        
        lista_nomes_eventos = [e["nome"] for e in st.session_state["eventos"]]
        evento_selecionado = st.selectbox("Selecione o Evento Vinculado:", lista_nomes_eventos)
        
        st.markdown("<div class='rokfy-card'>", unsafe_allow_html=True)
        titulo_anais = st.text_input("Título dos Anais", value=f"Anais do {evento_selecionado}")
        issn_isbn = st.text_input("Código ISSN / ISBN", placeholder="Ex: 2358-8810")
        arquivo_anais = st.file_uploader("Upload do Volume Completo (.PDF)", type=["pdf"])
        
        if st.button("Publicar Anais do Evento"):
            if arquivo_anais:
                bar_a = st.progress(0, text="Processando e indexando arquivo nos anais...")
                for p in range(100):
                    time.sleep(0.005)
                    bar_a.progress(p + 1, text="Processando e indexando arquivo nos anais...")
                bar_a.empty()
                st.success(f"Anais vinculados com sucesso ao evento '{evento_selecionado}'!")
            else:
                st.error("Anexe o arquivo em PDF para efetuar a publicação.")
        st.markdown("</div>", unsafe_allow_html=True)

# 4. JANELA: EMISSÃO DE CERTIFICADOS (MOLDURAS, PLANILHAS E MODALIDADES)
elif opcao == "Emissão de Certificados":
    st.markdown(
        """
        <div class="hero-editorial">
            <h1>Gerador e Emissor de Certificados</h1>
            <p>Configure modelos, escolha a modalidade de atuação e emita em lote via planilha de presenças.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    col_config, col_preview = st.columns([1, 1])
    
    with col_config:
        st.markdown("<div class='rokfy-card'>", unsafe_allow_html=True)
        st.markdown("<h4>1. Parâmetros do Certificado</h4>", unsafe_allow_html=True)
        
        modelo_layout = st.selectbox("Modelo Visual do Certificado", ["Modelo Clássico Editorial", "Modelo Moderno Rokfy"])
        
        modalidade = st.selectbox(
            "Modalidade / Categoria Especial",
            [
                "Participante",
                "Organizador",
                "Comissão Científica",
                "Palestrante",
                "Ministrante de Curso"
            ]
        )
        
        st.markdown("<h4>2. Emissão Individual</h4>", unsafe_allow_html=True)
        nome_cert = st.text_input("Nome do Contemplado", "Dr. Roberto Silva")
        evento_cert = st.selectbox("Evento", [e["nome"] for e in st.session_state["eventos"]])
        horas_cert = st.number_input("Carga Horária (Horas)", min_value=1, value=20)
        
        st.markdown("<h4>3. Emissão em Lote (Importar Planilha)</h4>", unsafe_allow_html=True)
        planilha_cert = st.file_uploader("Anexar Planilha de Presença (.CSV)", type=["csv"])
        
        if planilha_cert is not None:
            df_cert = pd.read_csv(planilha_cert)
            st.write("Lista de presenciais detectada:")
            st.dataframe(df_cert.head(3), use_container_width=True)
        
        if st.button("Emitir Certificado(s)"):
            b_cert = st.progress(0, text="Processando chancela e assinaturas digitais...")
            for i in range(100):
                time.sleep(0.005)
                b_cert.progress(i + 1, text="Processando chancela e assinaturas digitais...")
            b_cert.empty()
            st.success("Certificados emitidos e autenticados com sucesso!")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with col_preview:
        st.markdown("<h4>Pré-visualização do Documento</h4>", unsafe_allow_html=True)
        
        texto_atribuicao = {
            "Participante": f"participou na qualidade de <b>Participante</b> do evento",
            "Organizador": f"atuou na qualidade de <b>Membro da Comissão Organizadora</b> do evento",
            "Comissão Científica": f"atuou na qualidade de <b>Membro da Comissão Científica</b> do evento",
            "Palestrante": f"ministrou a palestra principal na qualidade de <b>Palestrante</b> no evento",
            "Ministrante de Curso": f"atuou na qualidade de <b>Ministrante de Curso/Minicurso</b> no evento"
        }
        
        frame_class = "cert-frame-classic" if modelo_layout == "Modelo Clássico Editorial" else "cert-frame-modern"
        
        st.markdown(
            f"""
            <div class="{frame_class}">
                <div class="cert-title">Certificado Oficial</div>
                <div class="cert-sub">PLATAFORMA ROKFY • MODALIDADE {modalidade.upper()}</div>
                <div style="font-size: 0.92rem; color: #333; margin: 22px 0; line-height: 1.6;">
                    Certificamos para os devidos fins que <b>{nome_cert}</b> {texto_atribuicao[modalidade]} 
                    <b>"{evento_cert}"</b>, cumprindo carga horária total de <b>{horas_cert} horas</b>.
                </div>
                <div style="border-top: 1px double #121212; padding-top: 12px; font-size: 0.75rem; color: #555; text-align: left;">
                    <b>Código de Autenticidade:</b> RKF-AUT-2026-X8<br>
                    <b>Validação Digital:</b> Documento Assinado Eletronicamente
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 5. JANELA: PAINEL DO ORGANIZADOR
elif opcao == "Painel do Organizador":
    st.markdown(
        """
        <div class="hero-editorial">
            <h1>Painel de Controle e Métricas</h1>
            <p>Acompanhamento de inscritos, controle financeiro e lista geral de participantes.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="nyt-divider"></div>', unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total de Eventos", len(st.session_state["eventos"]))
    col_m2.metric("Inscrições Validadas", "1.840")
    col_m3.metric("Certificados Emitidos", "520")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3>Importar / Atualizar Base Geral de Participantes</h3>", unsafe_allow_html=True)
    csv_geral = st.file_uploader("Upload de Planilha (.CSV)", type=["csv"], key="planilha_geral")
    
    if csv_geral is not None:
        df_g = pd.read_csv(csv_geral)
        st.dataframe(df_g, use_container_width=True)
