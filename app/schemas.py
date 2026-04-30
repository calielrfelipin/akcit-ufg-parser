from pydantic import BaseModel, EmailStr
from typing import Optional


class ExtractRequest(BaseModel):
    """Corpo da requisição POST /extract."""
    text: str


class ExtractResponse(BaseModel):
    """Estrutura de dados retornada após a extração pelo LLM.

    Campos opcionais retornam None quando o LLM não encontra a informação no texto.
    """
    name: str
    age: Optional[int] = None
    email: Optional[str] = None
    job: Optional[str] = None
