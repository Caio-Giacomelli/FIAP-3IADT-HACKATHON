import base64
import openai

def analyze_diagram(image_bytes, openai_api_key):
    # OpenAI Vision API (image analysis)
    client = openai.OpenAI(api_key=openai_api_key)
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": "You are a system architecture analyst."},
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Describe the architecture diagram, focusing on the components, their relationships, and the overall system. Do not include any other text than the description of the diagram. Do not describe the components, just identify them and their relationships. Keep it short and concise."},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{image_base64}"}
                ]
            }
        ]
    )
    extracted_text = response.output_text
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