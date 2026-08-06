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
    
    # Tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)
    
    # Tabela de Eventos com campos customizáveis do formulário de inscrição
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
    
    # Admin / Promotor Padrão
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
        return True, "Usuario cadastrado com sucesso!"
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
        fontSize=32,
        textColor=colors.HexColor('#E05A47'),
        alignment=1,
        spaceAfter=20
    )
    
    style_corpo = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=16,
        leading=24,
        alignment=1,
        textColor=colors.HexColor('#1A1A1A')
    )
    
    style_codigo = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        alignment=1,
        textColor=colors.HexColor('#666666')
    )

    story = []
    story.append(Spacer(1, 0.8*inch))
    story.append(Paragraph("CERTIFICADO DE PARTICIPACAO", style_titulo))
    story.append(Spacer(1, 0.3*inch))
    
    texto_certificado = f"""
    Certificamos que <b>{nome_participante.upper()}</b> participou do evento 
    <b>{evento_nome}</b> na categoria de <b>{modalidade.upper()}</b>, 
    cumprindo uma carga horaria total de <b>{horas} horas</b>.
    """
    story.append(Paragraph(texto_certificado, style_corpo))
    story.append(Spacer(1, 0.6*inch))
    story.append(Paragraph(f"Chancela de Autenticidade Digital: <b>{codigo_validacao}</b> | Emitido pela Plataforma Rokfy", style_codigo))
    
    def desenhar_moldura(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#FA8072'))
        canvas.setLineWidth(4)
        canvas.rect(20, 20, doc.pagesize[0] - 40, doc.pagesize[1] - 40)
        canvas.setStrokeColor(colors.HexColor('#E05A47'))
        canvas.setLineWidth(1)
        canvas.rect(25, 25, doc.pagesize[0] - 50, doc.pagesize[1] - 50)
        canvas.restoreState()

    doc.build(story, onFirstPage=desenhar_moldura)
    buffer.seek(0)
    return buffer

# ==========================================
# 3. MOTOR DE PAGAMENTO PIX
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
# 4. DESIGN CSS (LAYOUT ORIGINAL BEGE)
# ==========================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    @font-face {
        font-family: 'Chomsky';
        src: local('Chomsky'), local('Chomsky Regular'), local('Chomsky-Regular');
        font-weight: normal; font-style: normal;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #FAF6EE !important; color: #1A1A1A !important;
    }
    .stApp { background-color: #FAF6EE !important; }

    [data-testid="stSidebar"] { background-color: #F3ECE0 !important; border-right: 1px solid #E5DBD0 !important; }
    .brand-logo-text { font-family: 'Chomsky', 'UnifrakturMaguntia', serif !important; font-size: 3.8rem !important; color: #E05A47 !important; text-align: center; margin: 0; line-height: 0.9; }
    .brand-tag { font-size: 0.65rem !important; font-weight: 800 !important; letter-spacing: 3px !important; color: #1A1A1A !important; text-transform: uppercase; text-align: center; margin-top: 10px; margin-bottom: 20px; }

    .top-navbar { display: flex; justify-content: space-between; align-items: center; background: #FFFFFF; padding: 14px 28px; border-radius: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 25px; }
    .shape-container-top { width: 100%; background-color: #FA8072; border-radius: 24px 24px 0 0; padding: 35px 35px 15px 35px; color: #FFFFFF !important; position: relative; }
    .shape-container-top h1, .shape-container-top p { color: #FFFFFF !important; }
    .wave-divider { width: 100%; height: 60px; margin-bottom: 25px; }
    .wave-divider path { fill: #FA8072; }
    .rokfy-card { background: #FFFFFF; border-radius: 16px; padding: 26px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); border: 1px solid #EAE0D5; margin-bottom: 20px; }
    .stButton>button { background-color: #E05A47 !important; color: #ffffff !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; padding: 0.65rem 1.6rem !important; }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

def render_header_shape(titulo, sub_titulo):
    st.markdown(
        f"""
        <div class="shape-container-top">
            <h1 style="margin:0;">{titulo}</h1>
            <p style="margin-top:5px; opacity: 0.9;">{sub_titulo}</p>
        </div>
        <svg class="wave-divider" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,133.3C672,139,768,181,864,186.7C960,192,1056,160,1152,138.7C1248,117,1344,107,1392,101.3L1440,96L1440,0L1392,0C1344,0,1248,0,1152,0C1056,0,960,0,864,0C768,0,672,0,576,0C480,0,384,0,288,0C192,0,96,0,48,0L0,0Z"></path>
        </svg>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 5. CONTROLE DE SESSÃO & TELAS
# ==========================================
if "usuario_logado" not in st.session_state:
    st.session_state["usuario_logado"] = None

if st.session_state["usuario_logado"] is None:
    render_header_shape("Acesse o Rokfy", "Faca login ou crie sua conta para acessar o sistema.")
    
    tab_login, tab_registro = st.tabs(["Entrar no Sistema", "Criar Nova Conta"])
    
    with tab_login:
        st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
        email_login = st.text_input("E-mail", key="login_email")
        senha_login = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Acessar Conta"):
            user = autenticar_usuario(email_login, senha_login)
            if user:
                st.session_state["usuario_logado"] = user
                st.success(f"Bem-vindo(a), {user['nome']}!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
        st.info("Dica de Teste Promotor: admin@rokfy.com | Senha: 123456")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_registro:
        st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
        nome_reg = st.text_input("Nome Completo")
        email_reg = st.text_input("E-mail")
        senha_reg = st.text_input("Crie uma Senha", type="password")
        perfil_reg = st.selectbox("Tipo de Conta", ["Participante", "Promotor de Eventos", "Organizador", "Avaliador / Comissao"])
        
        if st.button("Cadastrar Usuário"):
            if nome_reg and email_reg and senha_reg:
                sucesso, msg = cadastrar_usuario(nome_reg, email_reg, senha_reg, perfil_reg)
                if sucesso:
                    st.success(msg + " Agora faca login.")
                else:
                    st.error(msg)
            else:
                st.error("Preencha todos os campos.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    usuario = st.session_state["usuario_logado"]
    
    st.markdown(
        f"""
        <div class="top-navbar">
            <div style="font-weight: 800; font-size: 1.1rem; color: #E05A47;">ROKFY PLATFORM</div>
            <div style="display:flex; align-items:center; gap:15px; font-weight:600; font-size:0.9rem;">
                <span>Ola, <b>{usuario['nome']}</b> ({usuario['perfil']})</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown('<div class="brand-logo-text">Rokfy</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="brand-tag">Gestão Integrada de Eventos</div>', unsafe_allow_html=True)
    
    if usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        opcoes_menu = [
            "Home / Apresentacao",
            "Criar e Configurar Evento",
            "Eventos Cadastrados",
            "Gestao de Inscritos",
            "Anais de Eventos",
            "Emissao de Certificados",
            "Sobre Nos / Contato"
        ]
    else:
        opcoes_menu = [
            "Home / Apresentacao",
            "Eventos Cadastrados",
            "Emissao de Certificados",
            "Sobre Nos / Contato"
        ]
        
    opcao = st.sidebar.radio("Navegacao", opcoes_menu)
    st.sidebar.markdown("---")
    if st.sidebar.button("Sair do Sistema"):
        st.session_state["usuario_logado"] = None
        st.rerun()

    eventos_db = listar_eventos_db()

    # 1. HOME
    if opcao == "Home / Apresentacao":
        render_header_shape("Plataforma Completa de Eventos", f"Painel de Controle de {usuario['nome']}.")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.markdown('<div class="rokfy-card"><h3>Gestao de Ingressos</h3><p style="color:#666;">Inscricoes personalizadas pelo promotor.</p></div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="rokfy-card"><h3>Certificados por Categoria</h3><p style="color:#666;">Emissao especifica para palestrante, participante e mais.</p></div>', unsafe_allow_html=True)
        with col_c:
            st.markdown('<div class="rokfy-card"><h3>Anais e Repositorio</h3><p style="color:#666;">Publicacao oficial de conteudos do evento.</p></div>', unsafe_allow_html=True)

    # 2. CRIAR E CONFIGURAR EVENTO (PROMOTOR / ORGANIZADOR)
    elif opcao == "Criar e Configurar Evento" and usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        render_header_shape("Configurador do Evento", "Defina dados do evento e monte o formulario de inscricao.")
        with st.form(key="form_criar_evento"):
            st.subheader("1. Dados Principais")
            c1, c2 = st.columns([2, 1])
            with c1:
                nome_ev = st.text_input("Nome do Evento")
                desc_ev = st.text_area("Descricao")
            with c2:
                cat_ev = st.selectbox("Categoria", ["Congresso", "Festival / Show", "Simposio", "Workshop", "Curso / Bootcamp"])
                vagas_ev = st.number_input("Limite de Vagas", min_value=10, value=500)
                data_ev = st.date_input("Data")
                local_ev = st.text_input("Localizacao / Link")
                
            st.markdown("---")
            st.subheader("2. Valor e Pagamento")
            tipo_ev = st.radio("Modelo de Evento:", ["Gratuito", "Pago"])
            preco_ev = 0.0
            meios = []
            if tipo_ev == "Pago":
                cp1, cp2 = st.columns([1, 2])
                with cp1:
                    preco_ev = st.number_input("Preco do Ingresso (R$)", min_value=1.0, value=100.0)
                with cp2:
                    if st.checkbox("PIX", value=True): meios.append("PIX")
                    if st.checkbox("Cartao de Credito"): meios.append("Cartao de Credito")

            st.markdown("---")
            st.subheader("3. Configurar Formulário de Inscrição")
            st.write("Marque quais informacoes o promotor precisa coletar do inscrito:")
            
            f1, f2, f3 = st.columns(3)
            with f1:
                req_nome = st.checkbox("Nome Completo", value=True, disabled=True)
                req_email = st.checkbox("E-mail", value=True, disabled=True)
            with f2:
                req_cpf = st.checkbox("CPF")
                req_tel = st.checkbox("Telefone / WhatsApp")
            with f3:
                req_registro = st.checkbox("Codigo de Registro Profissional (OAB, CRM, CREA, etc.)")
                req_inst = st.checkbox("Empresa ou Instituicao")

            st.write("Perguntas personalizadas extras (separe por virgula):")
            perguntas_extra_raw = st.text_input("Exemplo: Area de Atuacao, Tamanho da Camiseta, Restricao Alimentar")

            if st.form_submit_button("Salvar e Publicar Evento"):
                if nome_ev:
                    campos_selecionados = ["Nome Completo", "E-mail"]
                    if req_cpf: campos_selecionados.append("CPF")
                    if req_tel: campos_selecionados.append("Telefone")
                    if req_registro: campos_selecionados.append("Registro Profissional")
                    if req_inst: campos_selecionados.append("Instituicao")
                    
                    p_extra = [p.strip() for p in perguntas_extra_raw.split(",") if p.strip()]

                    salvar_evento_db(nome_ev, cat_ev, vagas_ev, data_ev, local_ev, tipo_ev, preco_ev, meios, campos_selecionados, p_extra)
                    st.success("Evento configurado e publicado com sucesso!")
                    st.rerun()

    # 3. EVENTOS CADASTRADOS & INSCRIÇÃO RESPONSIVA
    elif opcao == "Eventos Cadastrados":
        render_header_shape("Eventos Cadastrados", "Escolha um evento e preencha o formulario configurado pelo promotor.")
        if not eventos_db:
            st.info("Nenhum evento disponivel no momento.")
        else:
            for ev in eventos_db:
                st.markdown(f'<div class="rokfy-card">', unsafe_allow_html=True)
                col_info, col_acao = st.columns([3, 2])
                with col_info:
                    st.markdown(f"### {ev['nome']}")
                    st.write(f"**Categoria:** {ev['categoria']} | **Data:** {ev['data']} | **Local:** {ev['local']}")
                    st.write(f"**Valor:** {'R$ {:.2f}'.format(ev['preco']) if ev['tipo'] == 'Pago' else 'Gratuito'}")
                
                with col_acao:
                    if st.button("Abrir Formulario de Inscricao", key=f"btn_form_{ev['id']}"):
                        st.session_state[f"insc_aberta_{ev['id']}"] = True

                # Formulario dinamico definido pelo promotor do evento
                if st.session_state.get(f"insc_aberta_{ev['id']}", False):
                    st.markdown("---")
                    st.subheader("Formulario de Inscrição")
                    
                    dados_coletados = {}
                    with st.form(key=f"form_dinamico_{ev['id']}"):
                        dados_coletados["Nome Completo"] = st.text_input("Nome Completo", value=usuario['nome'])
                        dados_coletados["E-mail"] = st.text_input("E-mail", value=usuario['email'])

                        campos = ev.get("campos_formulario", [])
                        if "CPF" in campos:
                            dados_coletados["CPF"] = st.text_input("CPF")
                        if "Telefone" in campos:
                            dados_coletados["Telefone"] = st.text_input("Telefone / WhatsApp")
                        if "Registro Profissional" in campos:
                            dados_coletados["Registro Profissional"] = st.text_input("Codigo Profissional (OAB/CRM/CREA/etc.)")
                        if "Instituicao" in campos:
                            dados_coletados["Instituicao"] = st.text_input("Instituicao / Empresa")

                        perguntas = ev.get("perguntas_extra", [])
                        if perguntas:
                            st.write("**Perguntas Adicionais:**")
                            for p in perguntas:
                                dados_coletados[p] = st.text_input(p)

                        if ev['tipo'] == 'Pago':
                            st.markdown("---")
                            st.write(f"**Pagamento via PIX (Valor: R$ {ev['preco']:.2f})**")
                            payload_pix = f"00020126360014BR.GOV.BCB.PIX0114+5511999999999520400005303986540{ev['preco']:.2f}5802BR5905ROKFY6009SAO PAULO62070503***6304"
                            
                            c_qr, c_txt = st.columns([1, 2])
                            with c_qr:
                                st.image(gerar_qr_code_pix(payload_pix), width=140)
                            with c_txt:
                                st.write("Escaneie o QR Code ou copie a chave Pix abaixo:")
                                st.code(payload_pix, language="text")

                        if st.form_submit_button("Confirmar Inscricao"):
                            salvar_inscricao_db(ev['id'], usuario['id'], dados_coletados)
                            st.success("Inscricao realizada e dados salvos com sucesso!")
                            st.session_state[f"insc_aberta_{ev['id']}"] = False
                            st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    # 4. GESTÃO DE INSCRITOS (PROMOTOR / ORGANIZADOR)
    elif opcao == "Gestao de Inscritos" and usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        render_header_shape("Gestao de Inscritos", "Acesse a lista de participantes e os dados coletados nos formularios.")
        if not eventos_db:
            st.info("Nenhum evento disponível.")
        else:
            ev_sel = st.selectbox("Selecione o Evento:", [f"#{e['id']} - {e['nome']}" for e in eventos_db])
            ev_id = int(ev_sel.split('-')[0].replace('#', '').strip())
            
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inscricoes WHERE evento_id = ?", (ev_id,))
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                st.info("Nenhuma inscricao registrada para este evento ainda.")
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

    # 5. ANAIS DE EVENTOS
    elif opcao == "Anais de Eventos" and usuario["perfil"] in ["Promotor de Eventos", "Organizador"]:
        render_header_shape("Anais de Eventos", "Publicacao e indexacao academica.")
        if not eventos_db:
            st.warning("Cadastre um evento primeiro.")
        else:
            st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
            st.selectbox("Selecione o Evento:", [f"#{e['id']} - {e['nome']}" for e in eventos_db])
            st.text_input("ISSN / ISBN", placeholder="Ex: 2447-8821")
            st.file_uploader("Upload do Arquivo PDF dos Anais", type=["pdf"])
            if st.button("Publicar Anais"):
                st.success("Anais salvos!")
            st.markdown('</div>', unsafe_allow_html=True)

    # 6. EMISSÃO DE CERTIFICADOS POR CATEGORIA
    elif opcao == "Emissao de Certificados":
        render_header_shape("Emissão de Certificados", "Gere e baixe o certificado especifico para sua modalidade.")
        
        tab_gerar, tab_meus = st.tabs(["Emitir Certificado", "Meus Certificados Guardados"])
        
        with tab_gerar:
            if not eventos_db:
                st.warning("Nenhum evento disponivel.")
            else:
                st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
                ev_sel = st.selectbox("Evento Vinculado:", [e['nome'] for e in eventos_db])
                ev_obj = next((e for e in eventos_db if e['nome'] == ev_sel), None)
                
                # Categorias Especiais Solicitadas
                mod_cert = st.selectbox("Categoria / Modalidade do Certificado:", [
                    "Participante", 
                    "Palestrante / Ministrante", 
                    "Organizador / Promotor", 
                    "Comissao Cientifica",
                    "Avaliador / Parecerista",
                    "Monitor",
                    "Apresentador de Trabalho"
                ])
                nome_p = st.text_input("Nome do Contemplado", value=usuario['nome'])
                horas_p = st.number_input("Carga Horaria", value=20)
                
                if st.button("Gerar e Registrar Certificado"):
                    if ev_obj and nome_p:
                        cod = salvar_certificado_db(ev_obj['id'], nome_p, mod_cert, horas_p)
                        st.success(f"Certificado gerado com sucesso! Codigo de Validacao: {cod}")
                st.markdown('</div>', unsafe_allow_html=True)
                
        with tab_meus:
            meus_certs = listar_certificados_usuario(usuario['nome'])
            if not meus_certs:
                st.info("Nenhum certificado emitido para o seu nome ainda.")
            else:
                for c in meus_certs:
                    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
                    st.subheader(f"Certificado: {c['evento_nome']}")
                    st.write(f"**Categoria:** {c['modalidade']} | **Carga Horaria:** {c['horas']} horas")
                    st.write(f"**Autenticacao:** `{c['codigo_validacao']}`")
                    
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

    # 7. SOBRE NÓS
    elif opcao == "Sobre Nos / Contato":
        render_header_shape("Sobre a Rokfy", "Plataforma completa de eventos.")
        st.markdown('<div class="rokfy-card"><h3>Quem Somos</h3><p>Sua solucao completa para gestao de eventos e certificacao.</p></div>', unsafe_allow_html=True)
