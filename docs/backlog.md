# Backlog — akcit-ufg-parser

---

## Implementado

### Setup e configuração

| # | Item | Artefato |
|---|------|----------|
| 1 | Configurar `.gitignore` para Python, venv e variáveis de ambiente | `.gitignore` |
| 2 | Definir dependências do projeto | `requirements.txt` |
| 3 | Criar template de variáveis de ambiente | `.env.example` |

### Modelagem e contratos

| # | Item | Artefato |
|---|------|----------|
| 4 | Definir schemas de request e response com Pydantic v2 | `app/schemas.py` |
| 5 | Criar prompt de extração de dados de pessoa em português | `app/prompts/extractor_person.txt` |

### Serviço LLM

| # | Item | Artefato |
|---|------|----------|
| 6 | Implementar cliente OpenAI SDK com suporte a provedores alternativos | `app/services/llm_service.py` |
| 7 | Implementar parse e validação da resposta JSON via Pydantic | `app/services/llm_service.py` |
| 8 | Implementar retry automático em caso de resposta malformada | `app/services/llm_service.py` |

### API

| # | Item | Artefato |
|---|------|----------|
| 9 | Criar endpoint `GET /health` | `app/main.py` |
| 10 | Criar endpoint `POST /extract/person` | `app/main.py` |
| 11 | Estruturar rota com prefixo `/extract/{tipo}` para suportar futuras extrações | `app/main.py` |

### Segurança

| # | Item | Artefato |
|---|------|----------|
| 12 | Validação de tamanho do texto de entrada (1–5 000 caracteres) | `app/schemas.py` |
| 13 | Rate limiting de 10 req/min por IP com `slowapi` | `app/main.py` |
| 14 | Log estruturado no servidor sem vazamento de detalhes internos ao cliente | `app/main.py`, `app/services/llm_service.py` |
| 15 | Documentação Swagger desabilitada em `ENVIRONMENT=production` | `app/main.py` |

### Testes

| # | Item | Artefato |
|---|------|----------|
| 16 | Teste `GET /health` — 200 e body correto | `tests/test_api.py` |
| 17 | Teste `POST /extract/person` — extração completa | `tests/test_api.py` |
| 18 | Teste `POST /extract/person` — extração parcial (campos opcionais `null`) | `tests/test_api.py` |
| 19 | Teste de validação — texto vazio, acima do limite, body ausente | `tests/test_api.py` |
| 20 | Teste de erro LLM — `ValueError` → 422 e exceção genérica → 500 | `tests/test_api.py` |
| 21 | Teste de não-vazamento de internos no 500 | `tests/test_api.py` |
| 22 | Teste de rate limiting — 429 na 11ª requisição | `tests/test_api.py` |

### Documentação

| # | Item | Artefato |
|---|------|----------|
| 23 | README com visão geral, endpoints, setup, exemplos e decisões de arquitetura | `README.md` |
| 24 | Registro dos prompts usados com IA generativa | `prompts-claude.md` |
| 25 | Escopo do projeto | `docs/escopo-do-projeto.md` |

---

## Planejado / Próximos Passos

### Novas extrações

| # | Item | Rota prevista |
|---|------|---------------|
| 26 | Extração de dados de reunião (participantes, data/hora, pauta, plataforma) | `POST /extract/meeting` |
| 27 | Prompt correspondente | `app/prompts/extractor_meeting.txt` |

### Segurança e resiliência

| # | Item |
|---|------|
| 28 | Separar instruções do sistema e texto do usuário em `role: system` / `role: user` para reduzir superfície de prompt injection |
| 29 | Adicionar autenticação por API key no header |
| 30 | Timeout configurável na chamada ao LLM |

### Qualidade

| # | Item |
|---|------|
| 31 | Testes para novos endpoints à medida que forem criados |
| 32 | Cobertura de código com `pytest-cov` |

### Operação

| # | Item |
|---|------|
| 33 | `Dockerfile` para containerização |
| 34 | Pipeline CI/CD com GitHub Actions (lint + testes) |
