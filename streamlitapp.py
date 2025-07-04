import streamlit as st
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import io

# ==== CONFIGURATION ====
AZURE_ENDPOINT = "https://<your-region>.api.cognitive.microsoft.com/"
AZURE_KEY = "<your-azure-computer-vision-key>"

# ==== STREAMLIT UI ====
st.title("System Architecture Image Analyzer")
st.subheader("Upload an architecture diagram and get an AI-powered analysis")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Diagram", use_column_width=True)

    if st.button("Analyze Image"):
        st.info("Analyzing with Azure Computer Vision...")

        # Connect to Azure
        client = ComputerVisionClient(
            AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY)
        )

        # Read image content
        image_data = uploaded_file.read()
        image_stream = io.BytesIO(image_data)

        # Call Azure API
        analysis = client.analyze_image_in_stream(
            image=image_stream,
            visual_features=["Description", "Tags", "Objects"]
        )

        # Extract components
        description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
        tags = [tag.name for tag in analysis.tags]
        objects = [obj.object_property for obj in analysis.objects]

        # ==== Prompt-Engineered Summary ====
        st.markdown("### 🧠 AI Summary")
        st.write(f"**Azure Vision Description:** {description}")
        
        prompt_summary = f"""
        The uploaded diagram likely contains the following architecture elements based on AI analysis:
        
        - **Detected Tags:** {', '.join(tags)}
        - **Detected Components:** {', '.join(objects) if objects else 'None'}
        
        Based on these features, the diagram may include services like load balancers, databases, cloud services, or application servers.
        """

        st.code(prompt_summary, language="markdown")
