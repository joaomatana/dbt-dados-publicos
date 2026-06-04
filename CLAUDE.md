# dbt-dados-publicos
Projeto de analytics engineering: ELT de dados públicos da ANP com dbt + DuckDB.
## Regras
- Modelagem em camadas: staging → intermediate → marts. Nunca pular camada.
- staging: 1 modelo por fonte, só limpeza/cast/rename. Sem regra de negócio.
- Todo modelo em marts precisa de descrição e ao menos 1 teste no schema.yml.
- SQL em snake_case. Nomes: stg_<fonte>__<entidade>, int_<...>, mart_<...>.
- Nunca commitar os CSVs crus nem o arquivo .duckdb (estão no .gitignore).
## Comandos
- Build: `dbt build` (models + tests)
- Docs: `dbt docs generate && dbt docs serve`
