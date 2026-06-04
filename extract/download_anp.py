"""Extração da Série Histórica de Preços de Combustíveis da ANP → DuckDB."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

import duckdb
import requests

LISTING_URL = (
    "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/"
    "serie-historica-de-precos-de-combustiveis"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/csv,*/*",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "extract" / "raw"
DUCKDB_PATH = REPO_ROOT / "dados_publicos.duckdb"

HREF_RE = re.compile(r'href="([^"]+\.csv)"', re.IGNORECASE)
YEAR_RE = re.compile(r"(20\d{2})")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Baixa e carrega os preços de combustíveis da ANP no DuckDB."
    )
    p.add_argument("--ano-inicio", type=int, default=datetime.now().year - 2,
                   help="Primeiro ano a baixar (default: últimos 3 anos).")
    p.add_argument("--full", action="store_true",
                   help="Baixa toda a série mensal disponível (ignora --ano-inicio).")
    p.add_argument("--produtos", default="gasolina-etanol,diesel-gnv,glp",
                   help="Produtos separados por vírgula.")
    p.add_argument("--listar", action="store_true",
                   help="Lista os arquivos selecionados sem baixar (dry-run).")
    p.add_argument("--sem-download", action="store_true",
                   help="Não baixa; apenas carrega os CSVs já em extract/raw/.")
    return p.parse_args()


def produto_de(url: str) -> str:
    nome = url.rsplit("/", 1)[-1].lower()
    if "gasolina" in nome:
        return "gasolina-etanol"
    if "diesel" in nome:
        return "diesel-gnv"
    if "glp" in nome:
        return "glp"
    return "outros"


def ano_de(url: str) -> int | None:
    m = YEAR_RE.search(url)
    return int(m.group(1)) if m else None


def descobrir(session: requests.Session) -> list[str]:
    html = session.get(LISTING_URL, timeout=90).text
    return sorted({u for u in HREF_RE.findall(html) if "/shpc/dsan/" in u})


def filtrar(urls: list[str], args: argparse.Namespace) -> list[str]:
    produtos = {p.strip() for p in args.produtos.split(",") if p.strip()}
    selecionados = []
    for u in urls:
        if produto_de(u) not in produtos:
            continue
        ano = ano_de(u)
        if not args.full and (ano is None or ano < args.ano_inicio):
            continue
        selecionados.append(u)
    return selecionados


def decodificar(blob: bytes) -> str:
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return blob.decode(enc)
        except UnicodeDecodeError:
            continue
    return blob.decode("latin-1", errors="replace")


def baixar(session: requests.Session, url: str) -> Path:
    dest = RAW_DIR / url.rsplit("/", 1)[-1]
    if dest.exists() and ano_de(url) != datetime.now().year:
        return dest
    resp = session.get(url, timeout=180)
    resp.raise_for_status()
    dest.write_text(decodificar(resp.content), encoding="utf-8")
    return dest


def carregar(con: duckdb.DuckDBPyConnection) -> int:
    glob = str(RAW_DIR / "*.csv").replace("\\", "/")
    con.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    con.execute(
        f"""
        CREATE OR REPLACE TABLE raw.precos AS
        SELECT * EXCLUDE (filename),
               parse_filename(filename) AS _arquivo_origem,
               now() AS _loaded_at
        FROM read_csv('{glob}', delim=';', header=true, strict_mode=false,
                      all_varchar=true, union_by_name=true, filename=true)
        """
    )
    return con.execute("SELECT count(*) FROM raw.precos").fetchone()[0]


def main() -> None:
    args = parse_args()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if not args.sem_download:
        with requests.Session() as session:
            session.headers.update(HEADERS)
            urls = filtrar(descobrir(session), args)
            print(f"Selecionados: {len(urls)} arquivos")
            if args.listar:
                for u in urls:
                    print(f"  {ano_de(u)}  {produto_de(u):16}  {u.rsplit('/', 1)[-1]}")
                return
            for i, u in enumerate(urls, 1):
                print(f"[{i}/{len(urls)}] {baixar(session, u).name}")

    if not list(RAW_DIR.glob("*.csv")):
        print("Nenhum CSV em extract/raw/ para carregar.")
        return

    con = duckdb.connect(str(DUCKDB_PATH))
    try:
        total = carregar(con)
    finally:
        con.close()
    print(f"raw.precos: {total} linhas")


if __name__ == "__main__":
    main()
