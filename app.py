import streamlit as st
import pandas as pd
import io
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from PIL import Image

# Dependências para PPTX e DOCX
from pptx import Presentation
from docx import Document
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

st.set_page_config(page_title="Rokfy — Gerador de Certificados", layout="wide")

# ==========================================
# 1. ESTILO VISUAL ORIGINAL (PRESERVADO)
# ==========================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #FAF6EE !important; color: #1A1A1A !important;
    }
    .stApp { background-color: #FAF6EE !important; }

    [data-testid="stSidebar"] { background-color: #F3ECE0 !important; border-right: 1px solid #E5DBD0 !important; }
    .brand-logo-text { font-family: serif !important; font-size: 3.2rem !important; color: #E05A47 !important; text-align: center; margin: 0; line-height: 0.9; font-weight: bold; }
    .brand-tag { font-size: 0.65rem !important; font-weight: 800 !important; letter-spacing: 3px !important; color: #1A1A1A !important; text-transform: uppercase; text-align: center; margin-top: 10px; margin-bottom: 20px; }

    .shape-container-top { width: 100%; background-color: #FA8072; border-radius: 24px 24px 0 0; padding: 30px; color: #FFFFFF !important; }
    .shape-container-top h1, .shape-container-top p { color: #FFFFFF !important; }
    .wave-divider { width: 100%; height: 50px; margin-bottom: 20px; }
    .wave-divider path { fill: #FA8072; }
    .rokfy-card { background: #FFFFFF; border-radius: 16px; padding: 26px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); border: 1px solid #EAE0D5; margin-bottom: 20px; }
    
    .stButton>button { background-color: #E05A47 !important; color: #ffffff !important; border: none !important; border-radius: 10px !important; font-weight: 700 !important; padding: 0.65rem 1.6rem !important; }
    .step-indicator { font-weight: 800; color: #E05A47; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; margin-bottom: 5px; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Estado de Sessão para Gerenciar o Passo a Passo (Wizard)
if "etapa" not in st.session_state:
    st.session_state.etapa = 1

def proxima_etapa():
    st.session_state.etapa += 1

def etapa_anterior():
    st.session_state.etapa -= 1

def render_header(titulo, sub_titulo):
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

# Sidebar apenas com Logo Visual
st.sidebar.markdown('<div class="brand-logo-text">Rokfy</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-tag">Certificados em Massa</div>', unsafe_allow_html=True)
st.sidebar.info(f"📍 **Etapa Atual: {st.session_state.etapa} de 4**")

# ==========================================
# FUNÇÕES DE PROCESSAMENTO DE ARQUIVOS
# ==========================================
def substituir_tags_texto(texto, mapa):
    """Substitui <tag> no texto por valores do mapa."""
    if not texto:
        return ""
    for k, v in mapa.items():
        v_str = str(v) if v is not None else ""
        texto = texto.replace(f"<{k}>", v_str).replace(f"<{k.lower()}>", v_str).replace(f"{{{k}}}", v_str)
    return texto

def processar_pptx(pptx_bytes, mapa):
    prs = Presentation(io.BytesIO(pptx_bytes))
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    paragraph.text = substituir_tags_texto(paragraph.text, mapa)
    out = io.BytesIO()
    prs.save(out)
    out.seek(0)
    return out

def processar_docx(docx_bytes, mapa):
    doc = Document(io.BytesIO(docx_bytes))
    for p in doc.paragraphs:
        p.text = substituir_tags_texto(p.text, mapa)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                cell.text = substituir_tags_texto(cell.text, mapa)
    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    return out

# ==========================================
# FLUXO PRINCIPAL DE ETAPAS
# ==========================================

# ------------------------------------------
# ETAPA 1: CONFIGURAÇÃO DE E-MAIL (SMTP)
# ------------------------------------------
if st.session_state.etapa == 1:
    render_header("Etapa I: Configuração do Servidor de E-mail", "Insira suas credenciais para que o sistema possa disparar as mensagens.")
    
    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
    st.text_input("Servidor SMTP", value="smtp.gmail.com", key="smtp_server")
    st.number_input("Porta SMTP", value=587, key="smtp_port")
    st.text_input("Seu E-mail de Envio (Remetente)", key="smtp_user")
    st.text_input("Senha / Senha de Aplicativo", type="password", key="smtp_pass")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col2:
        st.button("Próximo: Modelo de Arquivo >", on_click=proxima_etapa, use_container_width=True)

# ------------------------------------------
# ETAPA 2: MODELO VISUAL / ARQUIVO
# ------------------------------------------
elif st.session_state.etapa == 2:
    render_header("Etapa II: Modelo do Certificado", "Suba o arquivo base do certificado contendo as tags marcadas com < >.")
    
    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
    st.write("**Instruções de Tags no Modelo:**")
    st.info("Coloque no seu arquivo tags como `<nome>`, `<cpf>`, `<curso>`, `<data>`, `<registro>`, `<livro>`, `<folha>`. O sistema irá substituir cada tag automaticamente pelos dados de cada participante.")
    
    tipo_arquivo = st.radio("Selecione o formato do modelo:", ["PowerPoint (.PPTX)", "Word (.DOCX)", "Imagem (PNG / JPG)"], key="tipo_modelo")
    
    ext = ["pptx"] if "PowerPoint" in tipo_arquivo else (["docx"] if "Word" in tipo_arquivo else ["png", "jpg", "jpeg"])
    st.file_uploader("Upload do Modelo Base", type=ext, key="arquivo_modelo_uploaded")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.button("< Voltar: Servidor E-mail", on_click=etapa_anterior, use_container_width=True)
    with c2:
        st.button("Próximo: Dados dos Participantes >", on_click=proxima_etapa, use_container_width=True)

# ------------------------------------------
# ETAPA 3: DADOS DOS PARTICIPANTES
# ------------------------------------------
elif st.session_state.etapa == 3:
    render_header("Etapa III: Dados dos Participantes", "Escolha como deseja inserir as informações que preencherão o certificado e os e-mails.")

    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
    opcao_dados = st.radio("Origem dos Dados:", ["Fazer Upload de Planilha Pronta (Excel / CSV)", "Preencher / Editar Tabela Direto no App"], key="opcao_dados")
    
    if opcao_dados == "Fazer Upload de Planilha Pronta (Excel / CSV)":
        arquivo_p = st.file_uploader("Upload da Planilha", type=["xlsx", "xls", "csv"], key="arquivo_planilha_uploaded")
        if arquivo_p:
            try:
                df = pd.read_csv(arquivo_p) if arquivo_p.name.endswith('.csv') else pd.read_excel(arquivo_p)
                st.session_state['df_participantes'] = df
            except Exception as e:
                st.error(f"Erro ao ler planilha: {e}")
    else:
        st.write("Edite a tabela diretamente abaixo. Adicione linhas ou colunas conforme necessário:")
        df_padrao = pd.DataFrame({
            "nome": ["Maria Silva", "João Santos"],
            "email": ["maria@exemplo.com", "joao@exemplo.com"],
            "cpf": ["123.456.789-00", "987.654.321-11"],
            "curso": ["Treinamento Avançado", "Treinamento Avançado"],
            "registro": ["REG-001", "REG-002"],
            "livro": ["Livro 1", "Livro 1"],
            "folha": ["10", "11"]
        })
        st.session_state['df_participantes'] = st.data_editor(df_padrao, num_rows="dynamic", use_container_width=True)

    if 'df_participantes' in st.session_state and st.session_state['df_participantes'] is not None:
        st.write("### Dados Carregados:")
        st.dataframe(st.session_state['df_participantes'], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.button("< Voltar: Modelo Base", on_click=etapa_anterior, use_container_width=True)
    with c2:
        st.button("Próximo: E-mail e Disparo >", on_click=proxima_etapa, use_container_width=True)

# ------------------------------------------
# ETAPA 4: E-MAIL PADRÃO, TAGS E GERADOR
# ------------------------------------------
elif st.session_state.etapa == 4:
    render_header("Etapa IV: Mensagem de E-mail e Disparo", "Configure o modelo de e-mail com tags e efetue o envio privado em massa ou download.")

    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
    st.subheader("1. Modelo Padrão de E-mail")
    st.info("Você pode incluir qualquer tag no assunto e corpo da mensagem (ex: `<nome>`, `<curso>`). Cada pessoa receberá sua mensagem personalizada de forma estritamente privada.")

    assunto_template = st.text_input("Assunto do E-mail", value="Seu Certificado do curso de <curso> está disponível!", key="assunto_template")
    corpo_template = st.text_area("Corpo do E-mail", value="Olá <nome>,\n\nSegue em anexo o seu certificado do curso de <curso>.\nDados de Registro: Número <registro>, Livro <livro>, Folha <folha>.\n\nParabéns!", height=150, key="corpo_template")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="rokfy-card">', unsafe_allow_html=True)
    st.subheader("2. Finalizar e Disparar")

    df_final = st.session_state.get('df_participantes', None)
    modelo_file = st.session_state.get('arquivo_modelo_uploaded', None)
    tipo_m = st.session_state.get('tipo_modelo', "PowerPoint (.PPTX)")

    tab_disparo, tab_zip = st.tabs(["🚀 Disparar E-mails Privados em Massa", "📦 Baixar Todos os Certificados (ZIP)"])

    with tab_disparo:
        if st.button("Iniciar Envio em Massa"):
            if not df_final or 'email' not in [str(c).lower() for c in df_final.columns]:
                st.error("Garante que a tabela possui uma coluna de e-mail válida na Etapa III.")
            elif not st.session_state.get('smtp_user') or not st.session_state.get('smtp_pass'):
                st.error("Preencha as credenciais SMTP na Etapa I.")
            else:
                sucesso, erro = 0, 0
                progresso = st.progress(0)
                total = len(df_final)

                col_email = [c for c in df_final.columns if str(c).lower() == 'email'][0]

                for idx, row in df_final.iterrows():
                    mapa = row.to_dict()
                    destinatario = str(row[col_email]).strip()

                    assunto_personalizado = substituir_tags_texto(assunto_template, mapa)
                    corpo_personalizado = substituir_tags_texto(corpo_template, mapa)

                    try:
                        # Processa Arquivo de Anexo
                        if modelo_file:
                            bytes_m = modelo_file.getvalue()
                            if "PowerPoint" in tipo_m:
                                file_out = processar_pptx(bytes_m, mapa)
                                filename = f"Certificado_{row.get('nome', idx)}.pptx"
                                subtype = "vnd.openxmlformats-officedocument.presentationml.presentation"
                            elif "Word" in tipo_m:
                                file_out = processar_docx(bytes_m, mapa)
                                filename = f"Certificado_{row.get('nome', idx)}.docx"
                                subtype = "vnd.openxmlformats-officedocument.wordprocessingml.document"
                            else:
                                file_out = io.BytesIO(bytes_m)
                                filename = f"Certificado_{row.get('nome', idx)}.png"
                                subtype = "png"
                        else:
                            file_out = None

                        # Montagem de e-mail PRIVADO e INDIVIDUAL
                        msg = MIMEMultipart()
                        msg['From'] = st.session_state['smtp_user']
                        msg['To'] = destinatario
                        msg['Subject'] = assunto_personalizado
                        msg.attach(MIMEText(corpo_personalizado, 'plain'))

                        if file_out:
                            anexo = MIMEApplication(file_out.getvalue(), _subtype=subtype)
                            anexo.add_header('Content-Disposition', 'attachment', filename=filename)
                            msg.attach(anexo)

                        # Envio único isolado
                        s = smtplib.SMTP(st.session_state['smtp_server'], int(st.session_state['smtp_port']))
                        s.starttls()
                        s.login(st.session_state['smtp_user'], st.session_state['smtp_pass'])
                        s.send_message(msg)
                        s.quit()

                        sucesso += 1
                    except Exception as e:
                        erro += 1

                    progresso.progress((idx + 1) / total)

                st.success(f"Disparo concluído! {sucesso} e-mails enviados com sucesso. ({erro} falhas)")

    with tab_zip:
        if st.button("Gerar Arquivo ZIP com Todos os Certificados"):
            if modelo_file and df_final is not None:
                zip_b = io.BytesIO()
                with zipfile.ZipFile(zip_b, "a", zipfile.ZIP_DEFLATED, False) as zf:
                    for idx, row in df_final.iterrows():
                        mapa = row.to_dict()
                        nome_p = str(row.get('nome', f'participante_{idx+1}'))
                        bytes_m = modelo_file.getvalue()

                        if "PowerPoint" in tipo_m:
                            f_out = processar_pptx(bytes_m, mapa)
                            zf.writestr(f"Certificado_{nome_p}.pptx", f_out.getvalue())
                        elif "Word" in tipo_m:
                            f_out = processar_docx(bytes_m, mapa)
                            zf.writestr(f"Certificado_{nome_p}.docx", f_out.getvalue())

                zip_b.seek(0)
                st.download_button("Baixar Arquivo ZIP", data=zip_b, file_name="Certificados.zip", mime="application/zip")
            else:
                st.error("Verifique se o modelo e a planilha/tabela foram inseridos.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.button("< Voltar: Tabela de Participantes", on_click=etapa_anterior, use_container_width=False)
