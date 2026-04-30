from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env antes de qualquer importação
# que dependa delas (ex.: llm_service inicializa o cliente OpenAI no import)
load_dotenv()

from fastapi import FastAPI, HTTPException

from app.schemas import ExtractRequest, ExtractResponse
from app.services.llm_service import extract_entities


app = FastAPI(
    title="akcit-ufg-parser",
    description="API para extração de dados estruturados a partir de texto usando LLM.",
    version="1.0.0",
)


@app.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest) -> ExtractResponse:
    """Recebe texto livre e retorna dados estruturados extraídos por um LLM.

    - **text**: Texto em linguagem natural contendo informações sobre uma pessoa.

    Retorna name, age, email e job quando encontrados no texto.
    """
    try:
        return extract_entities(request.text)
    except ValueError as exc:
        # Erro de validação do JSON retornado pelo LLM
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        # Erros inesperados (rede, autenticação, etc.)
        raise HTTPException(status_code=500, detail=f"Erro interno: {exc}")
