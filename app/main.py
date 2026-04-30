from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env antes de qualquer importação
# que dependa delas (ex.: llm_service inicializa o cliente OpenAI no import)
load_dotenv()

from fastapi import FastAPI, HTTPException

from app.schemas import ExtractRequest, ExtractResponse, HealthResponse
from app.services.llm_service import extract_entities


app = FastAPI(
    title="akcit-ufg-parser",
    description="API para extração de dados estruturados a partir de texto usando LLM.",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/extract/person", response_model=ExtractResponse)
def extract_person(request: ExtractRequest) -> ExtractResponse:
    """Recebe texto livre e retorna dados estruturados de uma pessoa extraídos por um LLM.

    - **text**: Texto em linguagem natural contendo informações sobre uma pessoa.

    Retorna name, age, email e job quando encontrados no texto.
    """
    try:
        return extract_entities(request.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro interno: {exc}")
