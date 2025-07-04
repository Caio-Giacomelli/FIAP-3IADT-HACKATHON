import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import requests

st.set_page_config(page_title="STRIDE Analyzer", layout="centered")
st.title("STRIDE Threat Modeling from Architecture Diagrams")
st.write("""
Enter the URL of a software architecture diagram. The app will analyze the image using ChatGPT, identify all components and relationships, and generate a STRIDE report with vulnerabilities and suggested fixes.
""")

api_key = st.text_input("Enter your OpenAI API Key", type="password")

image_url = st.text_input("Enter the URL of the architecture diagram image (PNG, JPG, JPEG)")

if image_url and api_key:
    try:
        response_img = requests.get(image_url)
        response_img.raise_for_status()
        image = Image.open(io.BytesIO(response_img.content))
        st.image(image, caption="Diagram from URL", use_column_width=True)
        st.info("Processing the image with ChatGPT. This may take a moment...")

        # Convert image to base64 for API
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()

        prompt = (
            "You are a security expert. Analyze the following software architecture diagram. "
            "Identify all components and relationships shown in the diagram. "
            "For each component and relationship, perform a STRIDE threat modeling analysis: "
            "list vulnerabilities and suggest potential fixes for each. "
            "Return the result as a structured report with sections for Components, Relationships, Vulnerabilities, and Fixes. "
            "If the image is unclear, state what information is missing."
        )

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a security expert skilled in STRIDE threat modeling."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            max_tokens=1500
        )
        report = response.choices[0].message.content
        st.success("STRIDE Report Generated:")
        st.markdown(report)
    except Exception as e:
        st.error(f"Error: {e}")

elif not api_key:
    st.warning("Please enter your OpenAI API key.") 