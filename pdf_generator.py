import io
from markdown_pdf import MarkdownPdf, Section
import streamlit as st

def generate_stride_pdf(prompt, report):
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    pdf.add_section(Section(f"# Relatório Stride\n"))
    pdf.add_section(Section(f"## Prompt Utilizado\n\n{prompt}\n"))
    pdf.add_section(Section(report))
    pdf.meta["title"] = "Relatório Stride"
    buffer = io.BytesIO()
    pdf.save(buffer)
    buffer.seek(0)
    return buffer

def add_pdf_download_button(buffer, label, file_name):
    st.download_button(
        label=label,
        data=buffer,
        file_name=file_name,
        mime="application/pdf"
    ) 