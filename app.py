import streamlit as st
import sqlite3
import pandas as pd
import json
import hashlib
import io
import uuid
import qrcode

# Imports para geração de PDF com ReportLab
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

st.set_page_config(page_title="Rokfy — Plataforma de Eventos", layout="wide")

# ==========================================
# 1. BANCO DE DADOS & SEGURANÇA (BACK-END)
# ==========================================
DB_FILE = "rokfy.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela de Usuários com novos perfis
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)
    
    # Tabela de Eventos com campos configuráveis de inscrição
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            vagas INTEGER NOT NULL,
            data TEXT NOT NULL,
            local TEXT,
            tipo TEXT NOT NULL,
            preco REAL,
            pagamentos TEXT,
            campos_formulario TEXT,
            perguntas_extra TEXT
        )
    """)
    
    # Tabela de Inscritos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER,
            usuario_id INTEGER,
            dados_inscricao TEXT,
            data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (evento_id) REFERENCES eventos (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)
    
    # Tabela de Certificados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS certificados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_validacao TEXT UNIQUE NOT NULL,
            evento_id INTEGER,
            nome_participante TEXT NOT NULL,
            modalidade TEXT NOT NULL,
            horas INTEGER NOT NULL,
            data_emissao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (evento_id) REFERENCES eventos (id)
        )
    """)
    
    # Usuário Padrão Promotor/Organizador
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (?, ?, ?, ?)
        """, ("Promotor Rokfy", "admin@rokfy.com", hash_senha("123456"), "Promotor de Eventos"))
        
    conn.commit()
    conn.close()

init_db()

# CRUD
def cadastrar_usuario(nome, email, senha, perfil):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, perfil)
            VALUES (?, ?, ?, ?)
        """, (nome, email, hash_senha(senha), perfil))
        conn.commit()
        conn.close()
        return True, "Cadastro realizado com sucesso."
    except sqlite3.IntegrityError:
        return False, "E-mail ja cadastrado."

def autenticar_usuario(email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, hash_senha(senha)))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def salvar_evento_db(nome, categoria, vagas, data, local, tipo, preco, pagamentos, campos_formulario, perguntas_extra):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO eventos (nome, categoria, vagas, data, local, tipo, preco, pagamentos, campos_formulario, perguntas_extra)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, categoria, vagas, str(data), local, tipo, preco, json.dumps(pagamentos), json.dumps(campos_formulario), json.dumps(perguntas_extra)))
    conn.commit()
    conn.close()

def listar_eventos_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    eventos = []
    for r in rows:
        eventos.append({
            "id": r["id"],
            "nome": r["nome"],
            "categoria": r["categoria"],
            "vagas": r["vagas"],
            "data": r["data"],
            "local": r["local"],
            "tipo": r["tipo"],
            "preco": r["preco"],
            "pagamentos": json.loads(r["pagamentos"]) if r["pagamentos"] else [],
            "campos_formulario": json.loads(r["campos_formulario"]) if r["campos_formulario"] else [],
            "perguntas_extra": json.loads(r["perguntas_extra"]) if r["perguntas_extra"] else []
        })
    return eventos

def salvar_inscricao_db(evento_id, usuario_id, dados_inscricao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inscricoes (evento_id, usuario_id, dados_inscricao)
        VALUES (?, ?, ?)
    """, (evento_id, usuario_id, json.dumps(dados_inscricao)))
    conn.commit()
    conn.close()

def salvar_certificado_db(evento_id, nome, modalidade, horas):
    codigo = str(uuid.uuid4()).split('-')[0].upper()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO certificados (codigo_validacao, evento_id, nome_participante, modalidade, horas)
        VALUES (?, ?, ?, ?, ?)
    """, (codigo, evento_id, nome, modalidade, horas))
    conn.commit()
    conn.close()
    return codigo

def listar_certificados_usuario(nome_participante):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.*, e.nome as evento_nome 
        FROM certificados c 
        JOIN eventos e ON c.evento_id = e.id 
        WHERE c.nome_participante = ?
    """, (nome_participante,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==========================================
# 2. MOTOR DE GERAÇÃO DE PDF
# ==========================================
def gerar_pdf_certificado(nome_participante, evento_nome, modalidade, horas, codigo_validacao):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=0.5*inch, leftMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    
    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=30,
        textColor=colors.HexColor('#6C5CE7'),
        alignment=1,
        spaceAfter=20
    )
    
    style_corpo = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=15,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#2D3436')
    )
    
    style_codigo = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#636E72')
    )

    story = []
    story.append(Spacer(1, 0.8*inch))
    story.append(Paragraph("CERTIFICADO DE PARTICIPACAO", style_titulo))
    story.append(Spacer(1, 0.3*inch))
    
    texto_certificado = f"""
    Certificamos que <b>{nome_participante.upper()}</b> participou do evento 
    <b>{evento_nome}</b> na categoria de <b>{modalidade.upper()}</b>, 
    com carga horaria total de <b>{horas} horas</b>.
    """
    story.append(Paragraph(texto_certificado, style_corpo))
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(f"Autenticacao Digital: <b>{codigo_validacao}</b> | Plataforma Rokfy Eventos", style_codigo))
    
    def desenhar_moldura(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#6C5CE7'))
        canvas.setLineWidth(4)
        canvas.rect(20, 20, doc.pagesize[0] - 40, doc.pagesize[1] - 40)
        canvas.setStrokeColor(colors.HexColor('#FD79A8'))
        canvas.setLineWidth(1.5)
        canvas.rect(25, 25, doc.pagesize[0] - 50, doc.pagesize[1] - 50)
        canvas.restoreState()

    doc.build(story, onFirstPage=desenhar_moldura)
    buffer.seek(0)
    return buffer

# ==========================================
# 3. PAGAMENTO PIX
# ==========================================
def gerar_qr_code_pix(chave_payload):
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(chave_payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ==========================================
# 4. DESIGN CSS JOVIAL & ANIMADO (SEM EMOJIS)
# ==========================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%) !important;
    }

    [data-testid="stSidebar"] {
        background-color: #18181B !important;
        border-right: 1px solid #27272A !important;
    }

    .brand-title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #A855F7 0%, #EC4899 50%, #F59E0B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: -1px;
        margin: 0;
    }
    .brand-sub {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        color: #A1A1AA !important;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 25px;
    }

    .hero-banner {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
        border-radius: 20px;
        padding: 35px;
        color: #FFFFFF !important;
        box-shadow: 0 10px 30px rgba(168, 85, 247, 0.3);
        margin-bottom: 30px;
        transition: transform 0.3s ease;
    }
    .hero-banner:hover {
        transform: translateY(-3px);
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        margin: 0;
        font-size: 2.2rem;
    }
    .hero-banner p {
        color: #F1F5F9 !important;
        margin-top: 8px;
        font-size: 1.05rem;
    }

    .rokfy-card {
        background: #18181B;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #27272A;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .rokfy-card:hover {
        border-color: #A855F7;
        box-shadow: 0 6px 25px rgba(168, 85, 247, 0.2);
    }

    .stButton>button {
        background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.7rem 1.8rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4) !important;
    }

    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
        background-color: #27272A !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
        border: 1px solid #3F3F46 !important;
    }

    div[data-baseweb="tab-list"] {
        gap: 10px;
    }
    button[data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 20px !important;
        background-color: #27272A !important;
        color: #A1A1AA !important;
        font-weight: 600 !important;
    }
    button[aria-selected="true"] {
        background: linear-gradient(90deg, #8B5CF6 0%, #EC4899 100%) !important;
        color: #FFFFFF !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

def render_hero(titulo, sub_titulo):
    st.markdown(
        f"""
        <div class="hero-banner">
            <h1>{titulo}</h1>
            <p>{sub_titulo}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 5. SESSÃO E NAVEGAÇÃO
# ==========================================
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if st.session_state["usuario_logado"] is None:
    render_hero("Plataforma Rokfy", "Entre na sua conta ou cadastre-se para participar de eventos.")
    
    tab_login, tab_registro = st.tabs(["Acessar Conta", "Criar Nova Conta"])
    
    with tab_login:
        st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
        email_login = st.text_input("E-mail", key="login_email")
        senha_login = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Entrar no Sistema"):
            user = autenticar_usuario(email_login, senha_login)
            if user:
                st.session_state["usuario_logado"] = user
                st.success(f"Bem-vindo, {user['nome']}")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
        st.info("Conta de teste do Promotor: admin@rokfy.com | Senha: 123456")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_registro:
        st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
        nome_reg = st.text_input("Nome Completo")
        email_reg = st.text_input("E-mail para Cadastro")
        senha_reg = st.text_input("Crie uma Senha", type="password")
        perfil_reg = st.selectbox("Perfil da Conta", [
            "Participante", 
            "Promotor de Eventos", 
            "Organizador", 
            "Avaliador / Comissão"
        ])
        
        if st.button("Finalizar Cadastro"):
            if nome_reg and email_reg and senha_reg:
                sucesso, msg = cadastrar_usuario(nome_reg, email_reg, senha_reg, perfil_reg)
                if sucesso:
                    st.success(msg + " Faça login para continuar.")
                else:
                    st.error(msg)
            else:
                st.error("Preencha todos os campos obrigatorios.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    usuario = st.session_state["usuario_logado"]
    
    st.sidebar.markdown('<div class="brand-title">Rokfy</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="brand-sub">Gestao e Ingressos</div>', unsafe_allow_html=True)
    st.sidebar.write(f"Usuario: **{usuario['nome']}**")
    st.sidebar.write(f"Perfil: **{usuario['perfil']}**")
    st.sidebar.markdown("---")
    
    # Menu baseado nos perfis
    if usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        opcoes_menu = [
            "Painel Geral",
            "Criar e Editar Evento",
            "Eventos Disponiveis",
            "Gestao de Inscritos",
            "Emissao de Certificados",
            "Sobre a Rokfy"
        ]
    else:
        opcoes_menu = [
            "Painel Geral",
            "Eventos Disponiveis",
            "Emissao de Certificados",
            "Sobre a Rokfy"
        ]
        
    opcao = st.sidebar.radio("Navegacao Principal", opcoes_menu)
    st.sidebar.markdown("---")
    if st.sidebar.button("Sair da Conta"):
        st.session_state["usuario_logado"] = None
        st.rerun()

    eventos_db = listar_eventos_db()

    # ------------------------------------------
    # 1. PAINEL GERAL
    # ------------------------------------------
    if opcao == "Painel Geral":
        render_hero(f"Ola, {usuario['nome']}", "Acompanhe seus eventos, inscricoes e certificados em um so lugar.")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="rokfy-card"><h3>Eventos Ativos</h3><p>Explore as oportunidades e inscricoes abertas.</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="rokfy-card"><h3>Inscricao Flexivel</h3><p>Campos customizados definidos pelo promotor do evento.</p></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="rokfy-card"><h3>Certificacao Rapida</h3><p>Emissao por perfil: participante, palestrante e mais.</p></div>', unsafe_allow_html=True)

    # ------------------------------------------
    # 2. CRIAR E EDITAR EVENTO (PROMOTOR / ORGANIZADOR)
    # ------------------------------------------
    elif opcao == "Criar e Editar Evento" and usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        render_hero("Configurador de Evento", "Defina as informacoes basicas e monte o formulario de inscricao perfeito.")
        
        with st.form(key="form_criar_evento"):
            st.subheader("1. Informacoes Gerais do Evento")
            col1, col2 = st.columns([2, 1])
            with col1:
                nome_ev = st.text_input("Nome do Evento")
                desc_ev = st.text_area("Descricao Completa")
            with col2:
                cat_ev = st.selectbox("Categoria", ["Congresso", "Workshop", "Simposio", "Show / Festival", "Curso / Bootcamp", "Encontro Tecnico"])
                vagas_ev = st.number_input("Total de Vagas", min_value=1, value=200)
                data_ev = st.date_input("Data do Evento")
                local_ev = st.text_input("Local ou Link Online")

            st.markdown("---")
            st.subheader("2. Valor e Forma de Pagamento")
            tipo_ev = st.radio("Modalidade de Ingressos:", ["Gratuito", "Pago"])
            preco_ev = 0.0
            meios = []
            if tipo_ev == "Pago":
                cp1, cp2 = st.columns([1, 2])
                with cp1:
                    preco_ev = st.number_input("Preco do Ingresso (R$)", min_value=1.0, value=50.0)
                with cp2:
                    if st.checkbox("Pix Instantaneo", value=True): meios.append("Pix")
                    if st.checkbox("Cartao de Credito"): meios.append("Cartao de Credito")

            st.markdown("---")
            st.subheader("3. Personalizacao do Formulario de Inscricao")
            st.write("Selecione os dados que o participante devera preencher ao se inscrever:")
            
            c_f1, c_f2, c_f3 = st.columns(3)
            with c_f1:
                req_nome = st.checkbox("Nome Completo", value=True, disabled=True)
                req_email = st.checkbox("E-mail", value=True, disabled=True)
            with c_f2:
                req_cpf = st.checkbox("CPF")
                req_tel = st.checkbox("Telefone / WhatsApp")
            with c_f3:
                req_registro = st.checkbox("Registro Profissional (OAB, CRM, CREA, etc.)")
                req_inst = st.checkbox("Empresa ou Instituicao")

            st.write("Adicionar Perguntas Customizadas (separadas por virgula):")
            perguntas_extra_raw = st.text_input("Ex: Tamanho da Camiseta, Como soube do evento?, Restricao Alimentar")

            if st.form_submit_button("Publicar Evento"):
                if nome_ev:
                    campos_selecionados = ["Nome Completo", "E-mail"]
                    if req_cpf: campos_selecionados.append("CPF")
                    if req_tel: campos_selecionados.append("Telefone")
                    if req_registro: campos_selecionados.append("Registro Profissional")
                    if req_inst: campos_selecionados.append("Instituicao")
                    
                    p_extra = [p.strip() for p in perguntas_extra_raw.split(",") if p.strip()]

                    salvar_evento_db(nome_ev, cat_ev, vagas_ev, data_ev, local_ev, tipo_ev, preco_ev, meios, campos_selecionados, p_extra)
                    st.success("Evento criado com sucesso!")
                    st.rerun()
                else:
                    st.error("Informe pelo menos o nome do evento.")

    # ------------------------------------------
    # 3. EVENTOS DISPONÍVEIS & INSCRIÇÃO FLEXÍVEL
    # ------------------------------------------
    elif opcao == "Eventos Disponiveis":
        render_hero("Eventos Abertos", "Inscreva-se nos eventos disponiveis na plataforma.")
        
        if not eventos_db:
            st.info("Nenhum evento cadastrado no momento.")
        else:
            for ev in eventos_db:
                st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
                c_det, c_btn = st.columns([3, 1])
                with c_det:
                    st.subheader(ev['nome'])
                    st.write(f"**Categoria:** {ev['categoria']} | **Data:** {ev['data']} | **Local:** {ev['local']}")
                    st.write(f"**Ingresso:** {'R$ {:.2f}'.format(ev['preco']) if ev['tipo'] == 'Pago' else 'Gratuito'}")
                
                with c_btn:
                    if st.button("Inscrever-se", key=f"btn_inscr_{ev['id']}"):
                        st.session_state[f"inscrevendo_{ev['id']}"] = True

                # Formulario Dinamico de Inscricao
                if st.session_state.get(f"inscrevendo_{ev['id']}", False):
                    st.markdown("---")
                    st.write(f"### Formulario de Inscricao — {ev['nome']}")
                    
                    dados_coletados = {}
                    with st.form(key=f"form_inscri_dinamico_{ev['id']}"):
                        # Campos Fixos
                        dados_coletados["Nome Completo"] = st.text_input("Nome Completo", value=usuario['nome'])
                        dados_coletados["E-mail"] = st.text_input("E-mail", value=usuario['email'])

                        # Campos Escolhidos pelo Promotor
                        campos = ev.get("campos_formulario", [])
                        if "CPF" in campos:
                            dados_coletados["CPF"] = st.text_input("CPF")
                        if "Telefone" in campos:
                            dados_coletados["Telefone"] = st.text_input("Telefone / WhatsApp")
                        if "Registro Profissional" in campos:
                            dados_coletados["Registro Profissional"] = st.text_input("Registro Profissional (OAB, CRM, CREA, etc.)")
                        if "Instituicao" in campos:
                            dados_coletados["Instituicao"] = st.text_input("Empresa / Instituicao")

                        # Perguntas Customizadas
                        perguntas = ev.get("perguntas_extra", [])
                        if perguntas:
                            st.write("**Perguntas Adicionais do Organizador:**")
                            for p in perguntas:
                                dados_coletados[p] = st.text_input(p)

                        # Pagamento se for pago
                        if ev['tipo'] == 'Pago':
                            st.markdown("---")
                            st.write(f"**Pagamento via Pix (Valor: R$ {ev['preco']:.2f})**")
                            payload_pix = f"00020126360014BR.GOV.BCB.PIX0114+5511999999999520400005303986540{ev['preco']:.2f}5802BR5905ROKFY6009SAO PAULO62070503***6304"
                            
                            c_qr, c_txt = st.columns([1, 2])
                            with c_qr:
                                st.image(gerar_qr_code_pix(payload_pix), width=130)
                            with c_txt:
                                st.code(payload_pix, language="text")
                                st.caption("Copie a chave Pix acima ou escaneie o QR Code.")

                        if st.form_submit_button("Confirmar Inscrição"):
                            salvar_inscricao_db(ev['id'], usuario['id'], dados_coletados)
                            st.success("Inscricao confirmada com sucesso!")
                            st.session_state[f"inscrevendo_{ev['id']}"] = False
                            st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------
    # 4. GESTÃO DE INSCRITOS (PROMOTOR / ORGANIZADOR)
    # ------------------------------------------
    elif opcao == "Gestao de Inscritos" and usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        render_hero("Gestao de Inscritos", "Visualize os dados coletados nos formularios de cada evento.")
        
        if not eventos_db:
            st.info("Nenhum evento disponivel.")
        else:
            ev_selecionado = st.selectbox("Selecione o Evento:", [f"#{e['id']} - {e['nome']}" for e in eventos_db])
            ev_id = int(ev_selecionado.split('-')[0].replace('#', '').strip())
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inscricoes WHERE evento_id = ?", (ev_id,))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                st.info("Nenhuma inscricao realizada para este evento ainda.")
            else:
                lista_dados = []
                for r in rows:
                    item = json.loads(r["dados_inscricao"])
                    item["Data Inscricao"] = r["data_inscricao"]
                    lista_dados.append(item)
                
                df = pd.DataFrame(lista_dados)
                st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------
    # 5. EMISSÃO DE CERTIFICADOS
    # ------------------------------------------
    elif opcao == "Emissao de Certificados":
        render_hero("Central de Certificados", "Gere certificados para qualquer categoria de participante ou baixe os seus.")
        
        tab_emitir, tab_meus = st.tabs(["Emitir Certificado", "Meus Certificados Guardados"])
        
        with tab_emitir:
            if not eventos_db:
                st.warning("Nenhum evento disponivel.")
            else:
                st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
                ev_sel = st.selectbox("Evento Vinculado:", [e['nome'] for e in eventos_db])
                ev_obj = next((e for e in eventos_db if e['nome'] == ev_sel), None)
                
                # Categoria / Modalidade Específica
                mod_cert = st.selectbox("Categoria do Certificado:", [
                    "Participante",
                    "Palestrante / Ministrante",
                    "Organizador / Promotor",
                    "Comissao Cientifica",
                    "Avaliador / Parecerista",
                    "Monitor",
                    "Apresentador de Trabalho"
                ])
                
                nome_p = st.text_input("Nome do Beneficiario", value=usuario['nome'])
                horas_p = st.number_input("Carga Horaria (Horas)", value=20, min_value=1)
                
                if st.button("Gerar Certificado Oficial"):
                    if ev_obj and nome_p:
                        cod = salvar_certificado_db(ev_obj['id'], nome_p, mod_cert, horas_p)
                        st.success(f"Certificado gerado com sucesso. Codigo de Validacao: {cod}")
                st.markdown('</div>', unsafe_allow_html=True)

        with tab_meus:
            meus_certs = listar_certificados_usuario(usuario['nome'])
            if not meus_certs:
                st.info("Nenhum certificado registrado para o seu nome ate o momento.")
            else:
                for c in meus_certs:
                    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
                    st.subheader(f"Certificado: {c['evento_nome']}")
                    st.write(f"**Categoria:** {c['modalidade']} | **Carga Horaria:** {c['horas']} horas")
                    st.write(f"**Codigo de Autenticidade:** `{c['codigo_validacao']}`")
                    
                    pdf_bytes = gerar_pdf_certificado(
                        nome_participante=c['nome_participante'],
                        evento_nome=c['evento_nome'],
                        modalidade=c['modalidade'],
                        horas=c['horas'],
                        codigo_validacao=c['codigo_validacao']
                    )
                    
                    st.download_button(
                        label="Baixar Certificado em PDF",
                        data=pdf_bytes,
                        file_name=f"Certificado_Rokfy_{c['codigo_validacao']}.pdf",
                        mime="application/pdf",
                        key=f"down_{c['id']}"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------
    # 6. SOBRE A ROKFY
    # ------------------------------------------
    elif opcao == "Sobre a Rokfy":
        render_hero("Sobre a Rokfy", "Tecnologia de ponta para organizacao de eventos, inscricoes e certificacao.")
        st.markdown(
            '<div class="rokfy-card"><h3>Solucao Completa para Eventos</h3><p>Plataforma dinamica desenvolvida para atender desde workshops locais ate grandes congressos nacionais.</p></div>', 
            unsafe_allow_html=True
        )
