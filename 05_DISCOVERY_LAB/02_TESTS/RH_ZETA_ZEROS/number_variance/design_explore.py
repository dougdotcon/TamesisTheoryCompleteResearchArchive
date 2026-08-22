"""
DESENHO -- so METADADOS deterministicos (T, logT, faixa de x
renormalizado, densidade local), NUNCA a estatistica de saida V(L).
Mesma disciplina do phase0_timing.py do FHK: usado para dimensionar a
grade de L e o numero de blocos ANTES do lock, sem espiar o resultado
substantivo.
"""
import json
from pathlib import Path

import numpy as np

from estimator import N_absolute, local_density

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"


def load_zeros1():
    vals = np.array([float(x) for x in open(DATA_DIR / "zeros1.txt").read().split()])
    assert len(vals) == 100000
    return vals


def load_offset_file(path, base, expected_n=10000):
    offsets = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            offsets.append(float(line))
        except ValueError:
            continue
    offsets = np.array(offsets)
    assert len(offsets) == expected_n, f"{path}: esperado {expected_n}, achado {len(offsets)}"
    assert np.all(np.diff(offsets) > 0)
    return offsets


def main():
    out = {}

    g1 = load_zeros1()
    x1 = N_absolute(g1)
    T1 = float(g1[-1])
    out["zeros1"] = {
        "n_zeros": len(g1), "T": T1, "logT": float(np.log(T1)),
        "log43T": float(np.log(T1) ** (4 / 3)),
        "x_min": float(x1.min()), "x_max": float(x1.max()),
        "x_range": float(x1.max() - x1.min()),
        "mean_spacing_check": float((x1.max() - x1.min()) / (len(x1) - 1)),
    }

    base3 = 267653395647.0
    off3 = load_offset_file(DATA_DIR / "zeros3.txt", base3, 10000)
    dens3 = local_density(base3)
    x3 = off3 * dens3
    out["zeros3"] = {
        "n_zeros": len(off3), "T": base3, "logT": float(np.log(base3)),
        "log43T": float(np.log(base3) ** (4 / 3)),
        "local_density": float(dens3),
        "offset_min": float(off3.min()), "offset_max": float(off3.max()),
        "x_min": float(x3.min()), "x_max": float(x3.max()),
        "x_range": float(x3.max() - x3.min()),
        "mean_spacing_check": float((x3.max() - x3.min()) / (len(x3) - 1)),
        "err2_bound_at_max_offset": float((off3.max() - off3.min()) ** 2 / (4 * np.pi * base3)),
    }

    base4 = 144176897509546973000.0
    off4 = load_offset_file(DATA_DIR / "zeros4.txt", base4, 10000)
    dens4 = local_density(base4)
    x4 = off4 * dens4
    out["zeros4_SEALED_HOLDOUT"] = {
        "n_zeros": len(off4), "T": base4, "logT": float(np.log(base4)),
        "log43T": float(np.log(base4) ** (4 / 3)),
        "local_density": float(dens4),
        "offset_min": float(off4.min()), "offset_max": float(off4.max()),
        "x_min": float(x4.min()), "x_max": float(x4.max()),
        "x_range": float(x4.max() - x4.min()),
        "mean_spacing_check": float((x4.max() - x4.min()) / (len(x4) - 1)),
        "err2_bound_at_max_offset": float((off4.max() - off4.min()) ** 2 / (4 * np.pi * base4)),
        "note": "metadados apenas -- NENHUM V(L) sera computado para este dataset nesta frente",
    }

    print(json.dumps(out, indent=2))
    json.dump(out, open(HERE / "design_metadata.json", "w"), indent=2)


if __name__ == "__main__":
    main()
