import os

# Define a chave antes de qualquer import do app, pois llm_service
# inicializa o cliente OpenAI no nível do módulo via os.environ[]
os.environ.setdefault("OPENAI_API_KEY", "test-key")

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import ExtractResponse

client = TestClient(app)

FULL_RESPONSE = ExtractResponse(
    name="Ana Lima",
    age=32,
    email="ana@example.com",
    job="engenheira de software",
)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Limpa o storage do rate limiter entre testes para evitar interferência."""
    yield
    try:
        app.state.limiter._storage.reset()
    except Exception:
        pass


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------

class TestHealth:
    def test_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_returns_status_ok(self):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# POST /extract/person — casos de sucesso
# ---------------------------------------------------------------------------

class TestExtractPersonSuccess:
    def test_full_extraction_returns_all_fields(self):
        with patch("app.main.extract_entities", return_value=FULL_RESPONSE):
            response = client.post("/extract/person", json={
                "text": "Me chamo Ana Lima, tenho 32 anos, sou engenheira de software e meu e-mail é ana@example.com"
            })

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Ana Lima"
        assert data["age"] == 32
        assert data["email"] == "ana@example.com"
        assert data["job"] == "engenheira de software"

    def test_partial_extraction_returns_null_for_missing_fields(self):
        with patch("app.main.extract_entities", return_value=ExtractResponse(name="João")):
            response = client.post("/extract/person", json={"text": "Meu nome é João"})

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "João"
        assert data["age"] is None
        assert data["email"] is None
        assert data["job"] is None


# ---------------------------------------------------------------------------
# POST /extract/person — validação de entrada
# ---------------------------------------------------------------------------

class TestExtractPersonValidation:
    def test_empty_text_returns_422(self):
        response = client.post("/extract/person", json={"text": ""})
        assert response.status_code == 422

    def test_text_above_5000_chars_returns_422(self):
        response = client.post("/extract/person", json={"text": "a" * 5001})
        assert response.status_code == 422

    def test_text_at_5000_chars_is_accepted(self):
        with patch("app.main.extract_entities", return_value=FULL_RESPONSE):
            response = client.post("/extract/person", json={"text": "a" * 5000})
        assert response.status_code == 200

    def test_missing_text_field_returns_422(self):
        response = client.post("/extract/person", json={})
        assert response.status_code == 422

    def test_missing_body_returns_422(self):
        response = client.post("/extract/person")
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /extract/person — tratamento de erros do LLM
# ---------------------------------------------------------------------------

class TestExtractPersonErrors:
    def test_llm_value_error_returns_422(self):
        with patch("app.main.extract_entities", side_effect=ValueError("JSON inválido")):
            response = client.post("/extract/person", json={"text": "texto qualquer"})
        assert response.status_code == 422

    def test_llm_unexpected_error_returns_500(self):
        with patch("app.main.extract_entities", side_effect=Exception("falha de rede")):
            response = client.post("/extract/person", json={"text": "texto qualquer"})
        assert response.status_code == 500

    def test_llm_unexpected_error_does_not_expose_internals(self):
        with patch("app.main.extract_entities", side_effect=Exception("senha=abc123")):
            response = client.post("/extract/person", json={"text": "texto qualquer"})
        assert "senha" not in response.text
        assert "abc123" not in response.text


# ---------------------------------------------------------------------------
# POST /extract/person — rate limiting
# ---------------------------------------------------------------------------

class TestExtractPersonRateLimit:
    def test_returns_429_after_10_requests_per_minute(self):
        with patch("app.main.extract_entities", return_value=FULL_RESPONSE):
            for _ in range(10):
                r = client.post("/extract/person", json={"text": "texto"})
                assert r.status_code == 200

            r = client.post("/extract/person", json={"text": "texto"})
            assert r.status_code == 429
