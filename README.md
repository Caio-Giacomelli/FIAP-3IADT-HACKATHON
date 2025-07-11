# FIAP Hackathon: Gerador de Relatório STRIDE com base em imagens de diagramas de arquitetura

Este projeto é um aplicativo Streamlit que utiliza a API da OpenAI para analisar imagens de diagramas de arquitetura e gerar um relatório de ameaças STRIDE com base na análise feita.

## Desenvolvedores

- Caio Henrique Giacomelli (RM 358131)
- Rafael Pereira Alonso (RM 358127)
- Wagner Dominike Eugênio de Mello (RM 358565)

## Funcionalidades

Upload de diagramas de arquitetura em formatos PNG, JPG ou JPEG.

Análise da imagem enviada do diagrama utilizando a API da OpenAI.

Geração automática de um relatório de ameaças STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) usando a API da OpenAI.

Inclusão de riscos, mitigações e referências para cada seção STRIDE no relatório.

Geração de uma tabela resumo com os riscos e mitigações.

Opção de download do relatório gerado em formato .pdf.

## Pré-requisitos

Para executar este projeto localmente, você precisará ter instalado:

Python 3.7 ou superior

pip (gerenciador de pacotes do Python)

## Você também precisará de credenciais válidas!

Gere um arquivo `.env` no repositório e adicione a credencial abaixo:
- OPENAI_API_KEY (chave de API para o uso do modelo da OpenAI)

## Instalação

Clone este repositório (ou copie o código do notebook para um arquivo .py) e rode os seguintes comandos:

python -m venv .venv

source .venv/bin/activate  # No Windows use `.venv\Scripts\activate`
  
pip install -r requirements.txt

streamlit run streamlitapp.py
