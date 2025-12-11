# README — Execução do experimento

Este projeto roda o `main.py` localmente ou via Docker Compose, gerando resultados para k = 5, 10 e 20 com avaliação por igualdade exata ou por NLI (RoBERTa-Large-MNLI).

## Pré-requisitos
- Python 3.11+ (recomendado virtualenv)
- Docker (opcional, se preferir Compose)
- Endpoint de LLM acessível em `http://localhost:11434/api/generate` com o modelo `ministral-3:14b`
- Variável de ambiente `AI_API_KEY` com o token do provedor

## Variáveis de ambiente
- `AI_API_KEY` (obrigatória) — chave usada no header Authorization.
- `EVAL_MODE` (opcional) — `nli` (default) usa RoBERTa-Large-MNLI para marcar equivalências lógicas; `exact` usa igualdade literal.
- Opcionalmente use um `.env` na raiz:
  ```
  AI_API_KEY=seu_token
  EVAL_MODE=nli
  ```

## Instalação (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução (local)
```bash
export AI_API_KEY=seu_token
export EVAL_MODE=nli   # ou exact
python main.py
```

O script lê todos os JSON em `goal/` e roda para k em `[5, 10, 20]`. Para cada k, os arquivos ficam em `outputs/k{k}/`:
- `results.json`
- `param_success_logs.json`, `param_error_logs.json`, `return_success_logs.json`, `return_error_logs.json`, `throws_success_logs.json`, `throws_error_logs.json`
- Versões `.txt` dos logs e `results_summary.txt`

## Execução com Docker Compose
```bash
AI_API_KEY=seu_token EVAL_MODE=nli docker compose up --build
```
Compose usa `docker-compose.yml` da raiz, monta `.` em `/app` e expõe `network_mode: host` (espera o endpoint LLM em `localhost:11434`).

## Notas
- Se quiser rodar só uma vez e sair: `docker compose run --rm app`.
- Ajuste `EVAL_MODE` para controlar quando predições logicamente equivalentes são marcadas como corretas (NLI usa threshold 0.80).
- Dependências estão em `requirements.txt`; se mudar, reinstale ou rebuild o container. 

