# STRIDE Analyzer Streamlit App

This app allows you to upload software architecture diagrams and receive a STRIDE threat modeling report using ChatGPT with vision capabilities.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   streamlit run streamlit_stride_app.py
   ```

3. Enter your OpenAI API key in the app UI.

4. Upload an architecture diagram image (PNG, JPG, JPEG).

The app will analyze the diagram and generate a STRIDE report, identifying components, relationships, vulnerabilities, and suggested fixes.