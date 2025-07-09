import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import io
import openai
import time
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

st.set_page_config(page_title="STRADE Generator", layout="centered")
st.title("📊 STRADE Architecture Report Generator")

st.markdown("### 🔐 Azure Computer Vision Credentials")
endpoint = st.text_input("Azure Endpoint")
key = st.text_input("Azure Key", type="password")
openai_api_key = st.text_input("OpenAI API Key", type="password")

uploaded_file = st.file_uploader("📁 Upload Architecture Diagram", type=["png", "jpg", "jpeg"])

# Only process if not already done and inputs are valid
if uploaded_file and endpoint and key and openai_api_key:

    if "report_text" not in st.session_state:
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

        st.session_state.extracted_text = extracted_text

        # Prompt Engineering
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

        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a system architecture analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        report_text = response.choices[0].message.content
        st.session_state.report_text = report_text

        # Create PDF
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4
        margin = inch * 0.75
        textobject = c.beginText(margin, height - margin)
        textobject.setFont("Helvetica", 11)

        for line in report_text.split("\n"):
            if line.strip() == "":
                textobject.textLine(" ")
            else:
                # wrap lines longer than page width
                for subline in line.split("\n"):
                    textobject.textLines(subline)

        c.drawText(textobject)
        c.showPage()
        c.save()
        pdf_buffer.seek(0)

        st.session_state.pdf_buffer = pdf_buffer

# If already processed, show results
if "report_text" in st.session_state:
    st.markdown("### 📝 Extracted Text")
    st.text_area("OCR Output", st.session_state.extracted_text, height=200)

    st.markdown("### 🧾 STRADE Report")
    st.markdown(st.session_state.report_text)

    st.download_button(
        label="📄 Download STRADE Report (.pdf)",
        data=st.session_state.pdf_buffer,
        file_name="STRADE_Report.pdf",
        mime="application/pdf"
    )

elif uploaded_file:
    st.info("Processing will begin once all credentials are entered.")
else:
    st.warning("Please enter credentials and upload an image.")
