import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential
from PIL import Image
import io
import time
from docx import Document

st.set_page_config(page_title="STRADE Analyzer", layout="centered")
st.title("🧠 STRADE Report from Architecture Diagram")

st.markdown("### 📌 Azure Computer Vision Credentials")
cv_endpoint = st.text_input("Computer Vision Endpoint")
cv_key = st.text_input("Computer Vision Key", type="password")

st.markdown("### 🤖 Azure OpenAI Credentials")
aoai_endpoint = st.text_input("Azure OpenAI Endpoint (e.g., https://YOUR-RESOURCE.openai.azure.com/)")
aoai_key = st.text_input("Azure OpenAI Key", type="password")
aoai_deployment = st.text_input("Deployment Name (e.g., gpt-4 or gpt-35-turbo)")

uploaded_file = st.file_uploader("📁 Upload your architecture diagram image", type=["png", "jpg", "jpeg"])

if uploaded_file and all([cv_endpoint, cv_key, aoai_endpoint, aoai_key, aoai_deployment]):
    st.success("Processing your image and generating the report...")

    computervision_client = ComputerVisionClient(
        cv_endpoint, CognitiveServicesCredentials(cv_key)
    )

    image_bytes = uploaded_file.read()
    image_stream = io.BytesIO(image_bytes)

    ocr_response = computervision_client.read_in_stream(image_stream, raw=True)
    operation_id = ocr_response.headers["Operation-Location"].split("/")[-1]

    while True:
        result = computervision_client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    extracted_text = ""
    if result.status == 'succeeded':
        for page in result.analyze_result.read_results:
            for line in page.lines:
                extracted_text += line.text + "\n"
    else:
        st.error("❌ Failed to extract text from image.")
        st.stop()

    st.markdown("### 📝 Extracted Text from Image")
    st.text_area("OCR Result", extracted_text, height=200)

    prompt = f"""
You are a system architecture analyst. Based on the following OCR-extracted text from a system architecture diagram, generate a STRADE report with these sections:

1. **Structure** – Describe the overall architecture and how components are organized.
2. **Technology Stack** – Mention languages, cloud services, APIs, databases, etc.
3. **Risks** – Identify technical or operational risks.
4. **Assumptions** – List assumptions based on the diagram.
5. **Decisions** – Note architectural decisions visible.
6. **Evolution** – Suggest how this system could evolve over time.

OCR Text:
{extracted_text}
"""

    aoai_client = OpenAIClient(aoai_endpoint, AzureKeyCredential(aoai_key))

    completion = aoai_client.chat_completions.create(
        deployment_id=aoai_deployment,
        messages=[
            {"role": "system", "content": "You are a software architecture analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    report_text = completion.choices[0].message.content


    st.markdown("### 📄 STRADE Report")
    st.markdown(report_text)

    doc = Document()
    doc.add_heading("STRADE Report", 0)
    for line in report_text.split("\n"):
        if line.startswith("**") and line.endswith("**"):
            doc.add_heading(line.replace("**", ""), level=1)
        else:
            doc.add_paragraph(line)

    doc_buffer = io.BytesIO()
    doc.save(doc_buffer)
    doc_buffer.seek(0)

    st.download_button(
        label="📥 Download STRADE Report (.docx)",
        data=doc_buffer,
        file_name="STRADE_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
else:
    st.info("Enter credentials and upload an image to start.")
