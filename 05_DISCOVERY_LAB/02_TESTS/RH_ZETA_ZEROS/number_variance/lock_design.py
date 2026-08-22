"""
Gera DESIGN.json -- a especificacao COMPLETA e TRAVADA do desenho
(grade de L, contagem de blocos B(L), pontos decisivos primarios,
limiares da regra de decisao). Usa SOMENTE metadados deterministicos
(design_metadata.json: T, logT, x_range de cada dataset) -- nenhum
V(L) real e tocado aqui. Rodado uma unica vez, ANTES de
run_primary.py, e nao alterado depois.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
meta = json.load(open(HERE / "design_metadata.json"))

MULT = [1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256]
FACTOR = 4.0
MIN_B = 10
MIN_BLOCK_WIDTH_FACTOR = 3.0  # dentro de block_number_variance

# Modelo B: P_cutoff por dataset (zeros1 exato, T inteiro; zeros3 limitado por crivo)
MODEL_B_P_CUTOFF = {"zeros1": None, "zeros3": 200_000_000}  # None = exato ate T

DECISION_THRESHOLDS = {"reject_z": 3.0, "accept_z": 2.0}

design = {
    "mult_grid": MULT, "factor_block_width": FACTOR, "min_blocks": MIN_B,
    "min_block_width_factor": MIN_BLOCK_WIDTH_FACTOR,
    "block_edge_scheme": "np.linspace(x_min, x_max, B+1) -- blocos de largura uniforme, deterministico, sem seed",
    "model_B_P_cutoff": MODEL_B_P_CUTOFF,
    "decision_thresholds": DECISION_THRESHOLDS,
    "datasets": {},
}

for name in ["zeros1", "zeros3"]:
    m = meta[name]
    logT, xr, log43T = m["logT"], m["x_range"], m["log43T"]
    rows = []
    for mult in MULT:
        L = mult * logT
        B = int(np.floor(xr / (FACTOR * L)))
        usable = B >= MIN_B
        proven = L <= log43T
        rows.append({"mult": mult, "L": L, "B": B, "usable": usable, "proven_corollary_1_4_3": proven})
    usable_rows = [r for r in rows if r["usable"]]
    primary = usable_rows[-1]  # maior L usavel -- ponto decisivo primario
    secondary = usable_rows[-2] if len(usable_rows) >= 2 else None
    design["datasets"][name] = {
        "T": m["T"], "logT": logT, "log43T": log43T, "x_range": xr,
        "grid": rows,
        "primary_L": primary["L"], "primary_mult": primary["mult"], "primary_B": primary["B"],
        "secondary_L": secondary["L"] if secondary else None,
        "secondary_mult": secondary["mult"] if secondary else None,
        "secondary_B": secondary["B"] if secondary else None,
    }

print(json.dumps(design, indent=2))
json.dump(design, open(HERE / "DESIGN.json", "w"), indent=2)
