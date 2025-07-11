import streamlit as st
import os
from dotenv import load_dotenv
from diagram_analyzer import analyze_diagram, generate_stride_report
from pdf_generator import generate_stride_pdf, add_pdf_download_button
from utils import prompts, prompt_titles

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Gerador de Relatório STRIDE", layout="centered")
st.title("📊 Gerador de Relatório STRIDE")

def clear_session_state():
    if "stride_reports" in st.session_state:
        del st.session_state.stride_reports
    if "stride_prompts" in st.session_state:
        del st.session_state.stride_prompts
    if "pdf_buffers" in st.session_state:
        del st.session_state.pdf_buffers
    if "extracted_text" in st.session_state:
        del st.session_state.extracted_text

def display_results():
    stride_reports = st.session_state.stride_reports
    pdf_buffers = st.session_state.pdf_buffers

    tabs = st.tabs(prompt_titles)
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown(f"### 🧾 Relatório Stride - {prompt_titles[i]}")
            st.markdown(stride_reports[i])
            add_pdf_download_button(
                pdf_buffers[i],
                label=f"📄 Download Relatório Stride ({prompt_titles[i]}).pdf",
                file_name=f"Relatorio_Stride_{i+1}.pdf"
            )

def process_image(uploaded_file, prompts):
    with st.spinner("Processando a imagem..."):
        try:
            image_bytes = uploaded_file.read()
            st.session_state.extracted_text = analyze_diagram(image_bytes, openai_api_key)
        except Exception as e:
            st.error(f"Erro ao processar a imagem ou gerar o relatório: {e}")
            st.stop()

    st.markdown(f"### 🧾 Componentes identificados")
    st.markdown(st.session_state.extracted_text)
    with st.spinner("Gerando relatórios..."):
        try:
            responses = generate_stride_report(st.session_state.extracted_text, prompts, openai_api_key)
            stride_reports = [resp['report'] for resp in responses]
            stride_prompts = [resp['prompt'] for resp in responses]
            pdf_buffers = [generate_stride_pdf(stride_prompts[i], stride_reports[i]) for i in range(len(stride_reports))]

            st.session_state.stride_reports = stride_reports
            st.session_state.stride_prompts = stride_prompts
            st.session_state.pdf_buffers = pdf_buffers
        except Exception as e:
            st.error(f"Erro ao gerar relatórios: {e}")
            st.stop()


uploaded_file = st.file_uploader("📁 Upload do Diagrama de Arquitetura", type=["png", "jpg", "jpeg"], on_change=clear_session_state)

if not openai_api_key:
    st.error("Por favor, configure as credenciais no arquivo .env")
    st.stop()

if uploaded_file and openai_api_key:
    st.image(uploaded_file, caption="Diagrama de Arquitetura enviado", use_container_width=True)
    if "stride_reports" not in st.session_state:
        process_image(uploaded_file, prompts)
        display_results()
    else:
        display_results()
else:
    st.warning("Por favor, carregue a imagem do diagrama")
