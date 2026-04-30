import logging
import os

from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env antes de qualquer importação
# que dependa delas (ex.: llm_service inicializa o cliente OpenAI no import)
load_dotenv()

from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.schemas import ExtractRequest, ExtractResponse, HealthResponse
from app.services.llm_service import extract_entities

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

_ENV = os.getenv("ENVIRONMENT", "development")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="akcit-ufg-parser",
    description="API para extração de dados estruturados a partir de texto usando LLM.",
    version="1.0.0",
    docs_url="/docs" if _ENV != "production" else None,
    redoc_url="/redoc" if _ENV != "production" else None,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/extract/person", response_model=ExtractResponse)
@limiter.limit("10/minute")
def extract_person(request: Request, body: ExtractRequest) -> ExtractResponse:
    """Recebe texto livre e retorna dados estruturados de uma pessoa extraídos por um LLM.

    - **text**: Texto em linguagem natural contendo informações sobre uma pessoa.

    Retorna name, age, email e job quando encontrados no texto.
    """
    try:
        return extract_entities(body.text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception:
        logger.exception("Unexpected error in POST /extract/person")
        raise HTTPException(status_code=500, detail="Erro interno do servidor.")
