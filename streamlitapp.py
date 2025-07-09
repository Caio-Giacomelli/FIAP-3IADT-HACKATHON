import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import io
import openai
import os


st.set_page_config(page_title="STRADE Generator", layout="centered")
st.title("📊 STRADE Architecture Report Generator")


st.markdown("### 🔐 Azure Computer Vision Credentials")
endpoint = st.text_input("Azure Endpoint")
key = st.text_input("Azure Key", type="password")


openai_api_key = st.text_input("OpenAI API Key", type="password")

uploaded_file = st.file_uploader("📁 Upload Architecture Diagram", type=["png", "jpg", "jpeg"])

if uploaded_file and endpoint and key and openai_api_key:
    st.success("Processing image...")


    computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(key)
    )

    # Read image
    image_bytes = uploaded_file.read()
    image_stream = io.BytesIO(image_bytes)


    ocr_result = computervision_client.read_in_stream(image_stream, raw=True)
    operation_location = ocr_result.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    import time
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
        st.error("❌ OCR failed.")
        st.stop()

    st.markdown("### 📝 Extracted Text")
    st.text_area("OCR Output", extracted_text, height=200)


    prompt = f"""
You are a system architect assistant. Based on the following extracted architecture diagram text, write a STRADE report with the following sections:

1. **Structure** – Describe the overall architecture and how components are organized.
2. **Technology Stack** – Mention programming languages, cloud services, APIs, databases, etc.
3. **Risks** – Identify potential technical or operational risks.
4. **Assumptions** – List key assumptions based on the diagram.
5. **Decisions** – Note any architectural decisions visible.
6. **Evolution** – Suggest how the architecture could evolve.

Extracted Text:
{extracted_text}
"""



    client = openai.OpenAI(api_key="your_openai_api_key")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a system architecture analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )

    report_text = response.choices[0].message.content

    strade_report = response['choices'][0]['message']['content']
    st.markdown("### 🧾 STRADE Report")
    st.markdown(strade_report)

    from docx import Document
    doc = Document()
    doc.add_heading('STRADE Report', 0)
    for line in strade_report.split('\n'):
        if line.startswith("**") and line.endswith("**"):
            doc.add_heading(line.replace("**", ""), level=1)
        else:
            doc.add_paragraph(line)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📄 Download STRADE Report (.docx)",
        data=buffer,
        file_name="STRADE_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

else:
    st.warning("Please enter credentials and upload an image.")
