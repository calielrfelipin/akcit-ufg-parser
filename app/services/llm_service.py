import json
import os
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError

from app.schemas import ExtractResponse


# Localiza o arquivo de prompt relativo a este módulo
_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "extractor_person.txt"

# Inicializa o cliente OpenAI com suporte a provedores compatíveis via OPENAI_BASE_URL
_client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)

_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _load_prompt(text: str) -> str:
    """Lê o template de prompt e injeta o texto do usuário.

    Usa replace() em vez de format() para não conflitar com as chaves
    literais do exemplo JSON que existe no template.
    """
    template = _PROMPT_PATH.read_text(encoding="utf-8")
    return template.replace("{text}", text)


def _call_llm(prompt: str) -> str:
    """Faz a chamada à API do LLM e retorna o conteúdo bruto da resposta."""
    response = _client.chat.completions.create(
        model=_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,  # temperatura 0 = resposta determinística e consistente
    )
    return response.choices[0].message.content.strip()


def _parse_response(raw: str) -> ExtractResponse:
    """Converte a string JSON bruta em um ExtractResponse validado pelo Pydantic.

    Levanta ValueError se o JSON for inválido ou não corresponder ao schema.
    """
    # Remove blocos de código markdown caso o LLM os inclua (ex: ```json ... ```)
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    data = json.loads(raw)  # pode levantar json.JSONDecodeError
    return ExtractResponse(**data)  # pode levantar pydantic.ValidationError


def extract_entities(text: str) -> ExtractResponse:
    """Ponto de entrada principal do serviço.

    Envia o texto ao LLM, valida a resposta e tenta novamente uma vez em caso de falha.

    Args:
        text: Texto livre do qual se deseja extrair entidades.

    Returns:
        ExtractResponse com os campos extraídos.

    Raises:
        ValueError: Se o LLM retornar JSON inválido mesmo após a segunda tentativa.
    """
    prompt = _load_prompt(text)

    raw = _call_llm(prompt)

    try:
        return _parse_response(raw)
    except (json.JSONDecodeError, ValidationError, KeyError):
        # Primeira tentativa falhou — tenta novamente antes de desistir
        raw = _call_llm(prompt)
        try:
            return _parse_response(raw)
        except (json.JSONDecodeError, ValidationError, KeyError) as exc:
            raise ValueError(
                f"O LLM retornou uma resposta inválida após duas tentativas: {exc}"
            ) from exc
