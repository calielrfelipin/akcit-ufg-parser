# Escopo do Projeto — akcit-ufg-parser

## Contexto

Projeto de estudo desenvolvido como parte de pós-graduação em Engenharia de Software com foco em IA generativa na UFG. O objetivo é explorar na prática o uso de LLMs para extração de dados estruturados a partir de texto livre, sem lógica de parsing manual.

---

## Objetivo

Construir uma micro-API em Python capaz de receber um texto em linguagem natural e retornar um JSON estruturado com as informações extraídas, delegando toda a inteligência de extração a um LLM via prompt engineering.

---

## Funcionalidades no Escopo

### Extração de dados de pessoas — `POST /extract/person`
- Recebe texto livre em português
- Extrai: nome completo, idade, e-mail e cargo/profissão
- Campos opcionais retornam `null` quando ausentes no texto
- Nome retorna `"Desconhecido"` se não encontrado

### Healthcheck — `GET /health`
- Verifica disponibilidade da API
- Retorna `{"status": "ok"}`

### Segurança e resiliência
- Validação de entrada: texto entre 1 e 5 000 caracteres
- Rate limiting: 10 requisições por minuto por IP
- Log estruturado no servidor, sem vazamento de detalhes internos ao cliente
- Documentação Swagger desabilitada em ambiente de produção
- Retry automático em caso de resposta malformada do LLM

---

## Fora do Escopo (nesta versão)

- Autenticação e autorização de usuários
- Persistência de dados (banco de dados)
- Outros tipos de extração além de pessoas (planejados para versões futuras)
- Deploy em nuvem
- Pipeline de CI/CD
- Interface frontend

---

## Requisitos Não-Funcionais

| Requisito | Decisão |
|-----------|---------|
| Compatibilidade de provedor | API OpenAI-compatible — funciona com OpenAI, Groq, Ollama e similares via `OPENAI_BASE_URL` |
| Determinismo | `temperature=0` garante respostas consistentes |
| Extensibilidade | Rota `/extract/{tipo}` e arquivos de prompt nomeados por convenção (`extractor_{tipo}.txt`) permitem adicionar novos tipos sem refatoração |
| Observabilidade | Log estruturado com timestamp, nível e módulo |
| Testabilidade | Suite pytest com mocks, sem dependência de chave de API real |

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.10+ |
| Framework web | FastAPI |
| Validação | Pydantic v2 |
| Integração LLM | OpenAI SDK |
| Rate limiting | slowapi |
| Configuração | python-dotenv |
| Testes | pytest + httpx |

---

## Estrutura de Arquivos

```
akcit-ufg-parser/
├── app/
│   ├── main.py                      # Endpoints e configuração FastAPI
│   ├── schemas.py                   # Contratos de request/response
│   ├── services/
│   │   └── llm_service.py           # Integração com LLM
│   └── prompts/
│       └── extractor_person.txt     # Prompt de extração de pessoas
├── tests/
│   └── test_api.py                  # Suite de testes
├── docs/
│   ├── escopo-do-projeto.md         # Este arquivo
│   └── backlog.md                   # Histórico e itens planejados
├── .env.example
├── requirements.txt
├── prompts-claude.md                # Registro dos prompts usados com IA
└── README.md
```
