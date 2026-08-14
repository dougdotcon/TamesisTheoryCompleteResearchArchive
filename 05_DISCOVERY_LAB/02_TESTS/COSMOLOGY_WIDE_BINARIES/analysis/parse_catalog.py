#!/usr/bin/env python3
"""
DISC-COSMOLOGY-MOND-SPARC-003 — parsing do catalogo bruto de binarias
largas do Gaia (El-Badry, Rix & Heintz 2021, MNRAS 506, 2269).

Le data/catalog.dat.gz (baixado diretamente de
https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/catalog.dat.gz, NUNCA
gerado sinteticamente) em streaming (sem jamais materializar o .dat
descomprimido inteiro em disco), e escreve data/catalog.parquet.

Nao aplica nenhum corte de qualidade nem deriva nenhuma estatistica --
apenas conversao de tipos (string bruta -> int/float/string) coluna a
coluna, preservando os valores tal como aparecem no arquivo bruto
(incluindo a sentinela numerica 1.0E20 do CDS para "sem valor", que e
mantida literal, nao convertida para NaN -- essa decisao de tratamento
fica para a etapa de pre-registro).

Uso:
    python3 parse_catalog.py
"""
import gzip
import hashlib
import io
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
GZ_PATH = DATA_DIR / "catalog.dat.gz"
README_PATH = DATA_DIR / "ReadMe"
PARQUET_PATH = DATA_DIR / "catalog.parquet"
COLDEFS_PATH = HERE.parent / "data" / "column_definitions.json"

EXPECTED_URL = "https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/catalog.dat.gz"
EXPECTED_GZ_BYTES = 1937351290  # Content-Length confirmado por HEAD em 2026-08-14
EXPECTED_ROWS = 1817594  # abstract do paper, El-Badry+2021


def parse_readme_columns(readme_path: Path):
    """Extrai as 217 definicoes de coluna do bloco byte-by-byte de
    catalog.dat no ReadMe oficial (nao hardcoded -- lido do arquivo real)."""
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    start = end = None
    for i, l in enumerate(lines):
        if "Byte-by-byte Description of file: catalog.dat" in l:
            start = i
        if start is not None and l.strip().startswith("Note (1)"):
            end = i
            break
    assert start is not None and end is not None, "nao achei o bloco byte-by-byte de catalog.dat no ReadMe"
    block = lines[start:end]

    pat = re.compile(r"^\s*(\d+)(?:-\s*(\d+))?\s+(\S+)\s+(\S+)\s+(\S+)\s*(.*)$")
    entries = []
    cur = None
    for ln in block:
        if set(ln.strip()) == {"-"}:
            continue
        m = pat.match(ln)
        if m:
            b1, b2, fmt, units, label, rest = m.groups()
            cur = {
                "start": int(b1),
                "end": int(b2 or b1),
                "format": fmt,
                "units": units,
                "label": label,
                "explain": rest.strip(),
            }
            entries.append(cur)
        elif cur is not None and ln.strip():
            cur["explain"] += " " + ln.strip()

    for e in entries:
        groups = re.findall(r"\(([^()]*)\)", e["explain"])
        cds = ""
        for g in reversed(groups):
            if not re.fullmatch(r"\d+", g.strip()):
                cds = g.strip()
                break
        e["cds_name"] = cds
        desc = re.sub(r"\s*\(\d+\)\s*$", "", e["explain"])
        if cds:
            desc = re.sub(r"\s*\(" + re.escape(cds) + r"\)\s*$", "", desc)
        e["description"] = desc.strip()
        e["nullable"] = e["explain"].strip().startswith("?")
        e["null_sentinel"] = e["explain"].strip().startswith("?=1e+20")

    return entries


def dtype_for(fmt: str) -> str:
    if fmt.startswith("I"):
        return "Int64"       # pandas nullable integer
    if fmt.startswith(("F", "E")):
        return "float64"
    if fmt.startswith("A"):
        return "string"
    raise ValueError(f"formato desconhecido: {fmt}")


def sha256_of(path: Path, bufsize=1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    t0 = time.time()

    print(f"[1/5] Verificando {GZ_PATH} ...")
    if not GZ_PATH.exists():
        sys.exit(f"ERRO: {GZ_PATH} nao existe. Baixe antes de rodar este script.")
    actual_bytes = GZ_PATH.stat().st_size
    print(f"      bytes no disco: {actual_bytes}")
    if actual_bytes != EXPECTED_GZ_BYTES:
        print(f"      AVISO: bytes no disco ({actual_bytes}) != Content-Length esperado "
              f"({EXPECTED_GZ_BYTES}). Download pode estar incompleto -- "
              f"prosseguindo mesmo assim e documentando a diferenca.")

    print("[2/5] sha256 do catalog.dat.gz (pode demorar alguns minutos)...")
    sha256 = sha256_of(GZ_PATH)
    print(f"      sha256 = {sha256}")

    print("[3/5] Extraindo definicao de colunas do ReadMe oficial...")
    entries = parse_readme_columns(README_PATH)
    assert len(entries) == 217, f"esperava 217 colunas, achei {len(entries)}"
    names = [e["label"] for e in entries]
    dtypes = {e["label"]: dtype_for(e["format"]) for e in entries}
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    COLDEFS_PATH.write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"      {len(names)} colunas confirmadas, salvas em {COLDEFS_PATH}")

    print("[4/5] Parsing em streaming (gzip -> pipe-split -> parquet, sem materializar .dat completo)...")
    string_cols = [e["label"] for e in entries if e["format"].startswith("A")]
    int_cols = [e["label"] for e in entries if e["format"].startswith("I")]
    float_cols = [e["label"] for e in entries if e["format"].startswith(("F", "E"))]

    CHUNK_ROWS = 200_000
    writer = None
    total_rows = 0
    malformed_lines = 0

    with gzip.open(GZ_PATH, "rt", encoding="utf-8", newline="\n") as fh:
        reader = pd.read_csv(
            fh,
            sep="|",
            header=None,
            names=names,
            dtype=str,
            chunksize=CHUNK_ROWS,
            engine="c",
            na_filter=True,
            keep_default_na=False,
            na_values=[""],
        )
        for chunk_i, chunk in enumerate(reader):
            n_before = len(chunk)
            # strip whitespace padding left over from the fixed-width origin
            for c in chunk.columns:
                chunk[c] = chunk[c].str.strip()

            for c in string_cols:
                chunk[c] = chunk[c].astype("string")
            for c in int_cols:
                chunk[c] = pd.to_numeric(chunk[c], errors="coerce").astype("Int64")
            for c in float_cols:
                chunk[c] = pd.to_numeric(chunk[c], errors="coerce").astype("float64")

            table = pa.Table.from_pandas(chunk, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(str(PARQUET_PATH), table.schema, compression="zstd")
            writer.write_table(table)
            total_rows += n_before
            if chunk_i % 5 == 0:
                elapsed = time.time() - t0
                print(f"      chunk {chunk_i}: +{n_before} linhas (total {total_rows}), "
                      f"{elapsed:.0f}s decorridos")

    if writer is not None:
        writer.close()

    print(f"[5/5] Concluido. Linhas totais escritas: {total_rows}")
    print(f"      Esperado (abstract El-Badry+2021): {EXPECTED_ROWS}")
    print(f"      Diferenca: {total_rows - EXPECTED_ROWS}")

    manifest = {
        "source_url": EXPECTED_URL,
        "gz_sha256": sha256,
        "gz_bytes_on_disk": actual_bytes,
        "gz_bytes_expected_content_length": EXPECTED_GZ_BYTES,
        "gz_complete": actual_bytes == EXPECTED_GZ_BYTES,
        "rows_parsed": total_rows,
        "rows_expected_paper_abstract": EXPECTED_ROWS,
        "n_columns": len(names),
        "parquet_path": str(PARQUET_PATH.relative_to(DATA_DIR.parent.parent.parent)),
        "elapsed_seconds": time.time() - t0,
    }
    (DATA_DIR / "parse_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
