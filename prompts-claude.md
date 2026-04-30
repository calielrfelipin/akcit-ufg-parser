# Prompts utilizados no projeto

Registro dos prompts utilizados para gerar os artefatos deste projeto com auxílio de IA generativa.

---

## Prompt 1 - `.gitignore`

```text
Contexto: Estou iniciando uma API Python com FastAPI em um repositório de estudo para pós-graduação.
Objetivo: Gere um arquivo .gitignore para Python cobrindo ambiente virtual, cache do interpretador, arquivos de distribuição, configurações de IDEs comuns e variáveis de ambiente (.env).
Estilo: Organize por seções com comentários descritivos.
Resposta: Forneça apenas o conteúdo do arquivo .gitignore.
```

---

## Prompt 2 - `requirements.txt`

```text
Contexto: API Python com FastAPI que usa LLM via OpenAI SDK para extrair dados estruturados de texto livre.
Objetivo: Liste as dependências mínimas necessárias: framework web, validação de dados, cliente OpenAI e gerenciamento de variáveis de ambiente.
Estilo: Apenas o arquivo requirements.txt com versões mínimas fixadas (>=).
Resposta: Forneça apenas o conteúdo do requirements.txt.
```

---

## Prompt 3 - `.env.example`

```text
Contexto: API Python que se conecta a um provedor LLM compatível com a API OpenAI (OpenAI, Groq, Ollama, etc.).
Objetivo: Crie um arquivo .env.example com as variáveis de ambiente necessárias: chave de API, URL base do provedor e nome do modelo.
Estilo: Inclua comentários explicativos em cada variável e um exemplo preenchido para o provedor Groq como alternativa gratuita.
Resposta: Forneça apenas o conteúdo do .env.example.
```

---

## Prompt 4 - `app/schemas.py`

```text
Contexto: API FastAPI em Python com Pydantic v2 para extração de dados de pessoas a partir de texto livre.
Objetivo: Crie os schemas de request e response. O request recebe um campo "text". O response retorna name (obrigatório), age, email e job (todos opcionais).
Estilo: Tipagem estrita com Pydantic BaseModel, campos opcionais com Optional e valor padrão None.
Resposta: Forneça apenas o arquivo app/schemas.py.
```

---

## Prompt 5 - `app/prompts/extractor_person.txt`

```text
Contexto: Sistema de extração de entidades de pessoas a partir de texto em português utilizando LLM.
Objetivo: Escreva um prompt de sistema que instrua o LLM a extrair nome, idade, e-mail e cargo de um texto livre, retornando exclusivamente um JSON válido com os campos name, age, email e job.
Estilo: Regras claras e explícitas: campo obrigatório com fallback, campos opcionais com null, sem markdown na resposta, sem inventar dados. Inclua um placeholder {text} para injeção do texto do usuário.
Resposta: Forneça apenas o conteúdo do arquivo de prompt.
```

---

## Prompt 6 - `app/services/llm_service.py`

```text
Contexto: API FastAPI que chama um LLM via OpenAI SDK para extrair dados estruturados. O prompt fica em um arquivo .txt separado com placeholder {text}.
Objetivo: Implemente o serviço de integração com o LLM com: leitura do template de prompt, chamada à API com temperature=0, parse e validação da resposta JSON via Pydantic, e retry automático em caso de resposta malformada.
Estilo: Funções privadas separadas por responsabilidade (_load_prompt, _call_llm, _parse_response), tipagem completa, sem frameworks além do OpenAI SDK.
Resposta: Forneça apenas o arquivo app/services/llm_service.py.
```

---

## Prompt 7 - `app/main.py`

```text
Contexto: API FastAPI em Python com endpoint de extração de dados de pessoa via LLM e suporte a futuros tipos de extração.
Objetivo: Crie o arquivo main.py com dois endpoints: GET /health retornando {"status": "ok"} e POST /extract/person que recebe ExtractRequest e retorna ExtractResponse via serviço LLM. Trate ValueError com 422 e exceções genéricas com 500.
Estilo: Código limpo, tipagem explícita, sem lógica de negócio no controller.
Resposta: Forneça apenas o arquivo app/main.py.
```

---

## Prompt 8 - `README.md`

```text
Contexto: MVP de micro-API para extração de dados estruturados de texto livre usando LLM, desenvolvido como projeto de estudo para pós-graduação em Engenharia de Software com foco em IA generativa na UFG.
Objetivo: Escreva o README completo com: visão geral, tabela de endpoints, stack, estrutura de projeto, instruções de instalação, configuração (incluindo exemplo com Groq), execução, exemplos de uso via curl e tabela de decisões de arquitetura.
Estilo: Markdown direto e profissional, sem seções desnecessárias.
Resposta: Forneça o arquivo README.md completo.
```

---

## Prompt 9 - Revisão de segurança

```text
Contexto: API FastAPI em Python com um endpoint POST /extract/person que recebe texto livre, injeta em um prompt e chama um LLM via OpenAI SDK. Sem autenticação, exposta publicamente.
Objetivo: Identifique os principais riscos de segurança do projeto e o que pode ser adicionado para mitigá-los.
Estilo: Análise direta agrupada por risco, com exemplos de código onde aplicável.
Resposta: Liste os riscos encontrados e sugestões de melhoria em formato de checklist.
```

---

## Prompt 10 - Melhorias de segurança

```text
Contexto: API FastAPI com endpoint POST /extract/person. Foram identificados os seguintes riscos: sem limite de tamanho no texto de entrada, erro interno exposto no HTTP 500, sem rate limiting e /docs habilitado em produção.
Objetivo: Implemente as quatro melhorias: (1) Field(min_length=1, max_length=5000) no schema de request; (2) rate limiting de 10 req/min por IP com slowapi; (3) log estruturado com o módulo logging — erros internos logados no servidor, cliente recebe mensagem genérica no 500; (4) /docs e /redoc desabilitados quando ENVIRONMENT=production.
Estilo: Código limpo, sem abstrações desnecessárias. Altere apenas os arquivos necessários.
Resposta: Forneça os arquivos alterados: app/schemas.py, app/main.py, app/services/llm_service.py, requirements.txt e .env.example.
```
