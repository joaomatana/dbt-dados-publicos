# dbt-dados-publicos

ELT dos preços de combustíveis da ANP (dados públicos brasileiros) com **dbt + DuckDB**.

> 🚧 **Em construção.** Fundação do projeto pronta (ETAPA 1). Extração, modelos dbt,
> CI/CD e docs publicados chegam nas próximas etapas.

## Stack
- **dbt-core + dbt-duckdb** — transformação ELT em camadas, zero infra (roda local e no CI).
- **DuckDB** — warehouse analítico local (arquivo `.duckdb`, fora do versionamento).
- **Python** (requests/pandas) — extração dos CSVs da ANP.
- **GitHub Actions** — build + testes a cada push; refresh semanal dos dados.

## Como rodar (local)
```bash
# 1. Dependências
python -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. dbt (a partir da pasta do projeto dbt)
cd dbt
dbt debug      # valida a conexão com o DuckDB
dbt build      # roda models + testes
```

## Estrutura
```
extract/   # download e carga dos CSVs da ANP (raw)
dbt/       # projeto dbt: models/staging -> intermediate -> marts
.github/   # CI/CD (build, testes, docs)
```

_README completo (arquitetura, diagrama Mermaid, porquês da stack, badges de CI e link do
dbt docs) na ETAPA 5._
