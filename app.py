import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão de Eventos Acadêmicos", page_icon="🎓", layout="wide")

st.title("🎓 Plataforma Acadêmica de Eventos")
st.caption("Acesso gratuito para estudantes, Ligas Acadêmicas e professores.")

st.sidebar.header("📌 Menu do Evento")
opcao = st.sidebar.radio("Navegar para:", ["Dashboard do Evento", "Emitir Certificados", "Publicações & Anais"])

if opcao == "Dashboard do Evento":
    st.header("📊 Painel de Controle e Inscrições")
    arquivo_csv = st.file_uploader("Suba a planilha CSV de inscritos do evento", type=["csv"])
    
    if arquivo_csv is not None:
        df = pd.read_csv(arquivo_csv)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Inscritos", len(df))
        col2.metric("Custo para a Faculdade", "R$ 0,00 (Grátis)")
        col3.metric("Certificados Prontos", f"{len(df)} disponíveis")
        st.subheader("📋 Lista de Participantes")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Envie uma planilha CSV para visualizar os dados do seu evento.")

elif opcao == "Emitir Certificados":
    st.header("📜 Gerador de Certificados com QR Code")
    col_form, col_preview = st.columns([1, 1])
    
    with col_form:
        st.subheader("Preencha os dados do certificado")
        nome = st.text_input("Nome do Estudante / Professor", "Maria Eduarda Silva")
        evento = st.text_input("Nome do Evento", "I Simpósio Universitário de IA")
        horas = st.number_input("Carga Horária (Horas)", min_value=1, value=20)
        codigo = st.text_input("Código de Autenticidade", "UF-2026-889A-X")
        st.button("✨ Emitir Certificado")

    with col_preview:
        st.subheader("👁️ Pré-visualização na Tela")
        st.markdown(
            f"""
            <div style="border: 3px solid #1A365D; padding: 20px; border-radius: 8px; background-color: #ffffff; text-align: center;">
                <h3 style="color: #1A365D; margin-bottom: 5px;">CERTIFICADO DE PARTICIPAÇÃO</h3>
                <p style="color: #718096; font-size: 12px;">PLATAFORMA ACADÊMICA LIVRE</p>
                <hr>
                <p style="font-size: 16px; color: #2D3748;">
                    Certificamos que <b>{nome}</b> participou do evento <b>"{evento}"</b> com carga horária de <b>{horas} horas</b>.
                </p>
                <br>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
                    <div style="text-align: left; font-size: 10px; color: #718096;">
                        <b>Autenticidade:</b> {codigo}<br>
                        <span>[ QR Code de Validação ]</span>
                    </div>
                    <div style="text-align: center; font-size: 10px; color: #718096;">
                        _______________________<br>
                        Comissão Organizadora
                    </div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

elif opcao == "Publicações & Anais":
    st.header("📚 Repositório de Trabalhos e Anais")
    st.text_input("Título do Trabalho / Resumo")
    st.text_input("Autores (Alunos e Orientador)")
    st.file_uploader("Upload do Trabalho em PDF", type=["pdf"])
    st.button("📤 Publicar nos Anais do Evento")
