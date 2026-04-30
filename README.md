# akcit-ufg-parser

API backend para extração de dados estruturados a partir de texto livre, utilizando LLM (Large Language Model). Desenvolvido como MVP para projeto de pós-graduação em Engenharia de Software com foco em IA generativa — UFG.

## Visão Geral

Recebe um texto em linguagem natural e retorna um JSON estruturado com informações extraídas, sem nenhuma lógica de parsing manual — toda a extração é feita pelo LLM.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Verifica se a API está no ar |
| `POST` | `/extract/person` | Extrai dados de uma pessoa a partir de texto livre |

### GET /health

```json
{ "status": "ok" }
```

### POST /extract/person

**Entrada:**
```json
{ "text": "Me chamo Ana Lima, tenho 32 anos, sou engenheira de software e meu e-mail é ana@example.com" }
```

**Saída:**
```json
{
  "name": "Ana Lima",
  "age": 32,
  "email": "ana@example.com",
  "job": "engenheira de software"
}
```

Campos opcionais (`age`, `email`, `job`) retornam `null` quando não encontrados no texto.

## Stack

- **Python 3.10+**
- **FastAPI** — framework web
- **Pydantic v2** — validação de dados de entrada e saída
- **OpenAI SDK** — integração com LLM (compatível com qualquer provedor OpenAI-compatible)
- **python-dotenv** — gerenciamento de variáveis de ambiente
- **slowapi** — rate limiting por IP

## Estrutura do Projeto

```
akcit-ufg-parser/
├── app/
│   ├── main.py                      # Ponto de entrada da API
│   ├── schemas.py                   # Modelos Pydantic (request e response)
│   ├── services/
│   │   └── llm_service.py           # Integração com o LLM
│   └── prompts/
│       └── extractor_person.txt     # Template de prompt para extração de pessoas
├── tests/
│   └── test_api.py                  # Suite de testes pytest
├── docs/
│   ├── escopo-do-projeto.md         # Escopo, requisitos e stack
│   └── backlog.md                   # Itens implementados e planejados
├── .env.example                     # Modelo de variáveis de ambiente
├── requirements.txt
├── prompts-claude.md                # Registro dos prompts usados com IA generativa
└── README.md
```

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/calielrfelipin/akcit-ufg-parser.git
cd akcit-ufg-parser

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
copy .env.example .env
# Edite .env com sua chave de API
```

## Configuração

Edite o arquivo `.env` criado no passo anterior:

```env
OPENAI_API_KEY=sk-...          # Chave da OpenAI (ou do provedor escolhido)
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
ENVIRONMENT=development        # Use "production" para desabilitar /docs e /redoc
```

### Usando Groq (alternativa gratuita)

O projeto suporta qualquer provedor compatível com a API OpenAI. Para usar o [Groq](https://console.groq.com):

```env
OPENAI_API_KEY=gsk_...
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=llama-3.1-8b-instant
```

## Execução

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

## Documentação Interativa

Acesse `http://localhost:8000/docs` para a interface Swagger UI gerada automaticamente pelo FastAPI.

> Disponível apenas quando `ENVIRONMENT` não estiver definido como `production`.

## Exemplos de Uso

```bash
# Healthcheck
curl http://localhost:8000/health
```

```bash
# Extração de dados de pessoa
curl -X POST http://localhost:8000/extract/person \
  -H "Content-Type: application/json" \
  -d '{"text": "Carlos Souza, 28 anos, analista de dados. Contato: carlos@email.com"}'
```

```json
{
  "name": "Carlos Souza",
  "age": 28,
  "email": "carlos@email.com",
  "job": "analista de dados"
}
```

## Segurança

| Medida | Detalhe |
|--------|---------|
| Validação de entrada | `text` limitado entre 1 e 5000 caracteres via `Field` do Pydantic — rejeita vazio e textos gigantes com 422 automático |
| Rate limiting | 10 requisições por minuto por IP no `POST /extract/person` via `slowapi` — retorna 429 se exceder |
| Log estruturado | Erros internos registrados com `logging` no servidor; o cliente recebe apenas `"Erro interno do servidor."` sem detalhes de implementação |
| Docs condicionais | `/docs` e `/redoc` desabilitados quando `ENVIRONMENT=production` |

## Decisões de Arquitetura

| Decisão | Motivo |
|---|---|
| `temperature=0` | Respostas determinísticas e consistentes |
| Retry automático | O LLM pode ocasionalmente retornar JSON malformado; uma segunda tentativa resolve a maioria dos casos |
| Prompt em arquivo `.txt` separado | Facilita ajustes no comportamento do LLM sem tocar no código Python |
| `OPENAI_BASE_URL` configurável | Permite trocar de provedor (OpenAI, Groq, Ollama, etc.) sem alteração de código |
| Rota `/extract/{tipo}` | Prefixo compartilhado prepara a API para novos tipos de extração sem quebrar a estrutura existente |
| Nome de prompt `extractor_{tipo}.txt` | Convenção de nomenclatura espelha as rotas, facilitando rastrear qual prompt serve qual endpoint |

## Documentação

| Arquivo | Conteúdo |
|---------|----------|
| [docs/escopo-do-projeto.md](docs/escopo-do-projeto.md) | Objetivo, funcionalidades, requisitos não-funcionais e o que está fora do escopo |
| [docs/backlog.md](docs/backlog.md) | Itens implementados por categoria e próximos passos planejados |
| [prompts-claude.md](prompts-claude.md) | Registro dos prompts usados com IA generativa para gerar os artefatos do projeto |

## Licença

MIT
