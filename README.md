# Gerador de Relatório STRIDE

Este projeto é um aplicativo Streamlit que utiliza a API de Computer Vision da Azure para extrair texto de diagramas de arquitetura e a API da OpenAI para gerar um relatório de ameaças STRIDE com base no texto extraído.

## Funcionalidades

Upload de diagramas de arquitetura (PNG, JPG, JPEG).

Extração de texto do diagrama utilizando Azure Computer Vision OCR.

Geração automática de um relatório de ameaças STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) usando a API da OpenAI.

Inclusão de riscos, mitigações e referências para cada seção STRIDE no relatório.

Geração de uma tabela resumo com os riscos e mitigações.

Opção de download do relatório gerado em formato .pdf.

## Pré-requisitos

Para executar este projeto localmente, você precisará ter instalado:

Python 3.7 ou superior

pip (gerenciador de pacotes do Python)

## Você também precisará de credenciais válidas!

Gere um arquivo `.env` no repositório e adicione as credenciais abaixo:
- AZURE_ENDPOINT (endpoint para o serviço de Computer Vision da Azure)
- AZURE_API_KEY (chave de API para o serviço de Computer Vision da Azure)
- OPENAI_API_KEY (chave de API para o uso do modelo da OpenAI)

## Instalação

Clone este repositório (ou copie o código do notebook para um arquivo .py) e rode os seguintes comandos:

python -m venv .venv

source .venv/bin/activate  # No Windows use `.venv\Scripts\activate`
  
pip install -r requirements.txt

streamlit run streamlitapp.py
