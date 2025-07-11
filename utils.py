prompts = [
            # Prompt Base
            """
Write a STRIDE report in brazillian portuguese for the following extracted architecture diagram text:
Extracted Text:
{extracted_text}
""",
            # Prompt Especializado
            """
You are a senior system architect. Take all the necessary time to create a quality response and with as much detail as possible. Validate if the answer is not contraditory in any capacity. Bring references to each of the topics. Do not be long-winded. 
Do not generate any observation or follow-up commentary after the STRIDE report. 
Based on the following extracted architecture diagram text, write a STRIDE report in brazillian portuguese, adding the risks, mitigation and references for the following sections:

1. **Spoofing**
2. **Tampering**
3. **Repudiation**
4. **Information Disclosure**
5. **Denial of Service**
6. **Elevation of Privilege**

After the STRIDE Report, generate a table in markdown, with all the stride sections in one column, risks in the second column and mitigation in the third column. Be very concise on the second and third columns.

Extracted Text:
{extracted_text}
""",
            # Prompt Reduzido
            """
Carefully analyze the extracted architecture diagram text and generate a detailed STRIDE report in Brazilian Portuguese. For each STRIDE category, clearly list the risks, mitigation strategies, and provide at least one reference.
Avoid unnecessary commentary or conclusions after the report.
After the report, create a concise markdown table summarizing each STRIDE section, its main risks, and mitigation strategies.
Extracted Text:
{extracted_text}
""",
            # Prompt em Português
            """
Analise cuidadosamente o texto extraído do diagrama de arquitetura e elabore um relatório STRIDE detalhado em português brasileiro. Para cada categoria STRIDE, descreva claramente os riscos, estratégias de mitigação e inclua pelo menos uma referência confiável.
Não inclua comentários adicionais ou conclusões após o relatório.
Ao final, gere uma tabela em markdown resumindo cada seção STRIDE, seus principais riscos e as respectivas mitigações de forma objetiva.

Texto extraído (em inglês):
{extracted_text}
""",
]

prompt_titles = [
    "Prompt Base",
    "Prompt Especializado",
    "Prompt Reduzido",
    "Prompt em Português"
]