"""Extração da Série Histórica de Preços de Combustíveis da ANP.

Baixa os CSVs públicos da ANP, salva os arquivos crus em ``extract/raw/`` e os carrega
como tabelas *raw* no DuckDB, de onde o dbt os consome via ``source()``.

Características (implementação na ETAPA 2):
- Janela recente (~2-3 anos) por padrão; ``--full`` baixa a série completa (desde 2004).
- Resiliente a encoding (utf-8 com fallback latin-1), separador ``;``, vírgula decimal
  e datas no formato BR.
- Idempotente: rodar de novo não duplica dados.

TODO(ETAPA 2): implementar download, parsing e carga no DuckDB.
"""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Baixa e carrega os preços de combustíveis da ANP no DuckDB.",
    )
    parser.add_argument(
        "--ano-inicio",
        type=int,
        default=None,
        help="Primeiro ano a baixar (default: janela recente de ~3 anos).",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Baixa a série histórica completa (desde 2004).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(
        "download_anp.py será implementado na ETAPA 2. "
        f"Args recebidos: ano_inicio={args.ano_inicio}, full={args.full}."
    )


if __name__ == "__main__":
    main()
