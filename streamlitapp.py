import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import io

st.title("🧠 System Architecture Image Analyzer")
st.subheader("Upload a system architecture diagram and let Azure Vision help describe it!")


st.markdown("#### 🔐 Enter your Azure Computer Vision credentials:")
azure_endpoint = st.text_input("Azure Endpoint", type="default")
azure_key = st.text_input("Azure Key", type="password")

uploaded_file = st.file_uploader("📤 Upload an architecture image", type=["png", "jpg", "jpeg"])

if azure_endpoint and azure_key and uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Diagram", use_column_width=True)

    if st.button("🔍 Analyze Image"):
        st.info("Connecting to Azure Computer Vision and analyzing the image...")

        try:
            client = ComputerVisionClient(
                azure_endpoint, CognitiveServicesCredentials(azure_key)
            )

            uploaded_file.seek(0)
            image_stream = uploaded_file

            analysis = client.analyze_image_in_stream(
                image=image_stream,
                visual_features=["Description", "Tags", "Objects"]
            )

            description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
            tags = [tag.name for tag in analysis.tags]
            objects = [obj.object_property for obj in analysis.objects]

            st.markdown("### ✅ Azure Vision Result")
            st.write(f"**Description:** {description}")
            st.write(f"**Tags:** {', '.join(tags)}")
            st.write(f"**Detected Objects:** {', '.join(objects) if objects else 'None'}")

            st.markdown("### 🧠 AI-Powered Summary")
            st.markdown(f"""
            Based on Azure's vision analysis, this diagram likely includes:

            - Common components: **{', '.join(objects) or 'Not detected'}**
            - Tags suggesting architectural elements: **{', '.join(tags)}**
            - General context: *"{description}"*
            """)

        except Exception as e:
            st.error(f"❌ Error during analysis: {e}")
else:
    st.warning("Please provide your Azure endpoint, key, and upload an image.")
