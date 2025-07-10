import io
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import openai

def analyze_diagram(image_bytes, azure_endpoint, azure_key):
    # Azure OCR
    computervision_client = ComputerVisionClient(
        azure_endpoint, CognitiveServicesCredentials(azure_key)
    )
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
        raise RuntimeError("OCR failed.")
    
    return extracted_text

def generate_stride_report(extracted_text, prompts, openai_api_key):
    # OpenAI API
    client = openai.OpenAI(api_key=openai_api_key)
    responses = []
    for prompt in prompts:
        # Fill prompt with extracted text if needed
        if "{extracted_text}" in prompt:
            prompt_filled = prompt.format(extracted_text=extracted_text)
        else:
            prompt_filled = prompt + f"\n\nExtracted Text:\n{extracted_text}"
        
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are a system architecture analyst."},
                {"role": "user", "content": prompt_filled}
            ],
            temperature=0.4,
        )
        responses.append({
            'prompt': prompt_filled,
            'report': response.choices[0].message.content
        })
    
    return responses 