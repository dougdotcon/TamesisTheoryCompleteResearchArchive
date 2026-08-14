"""
Generate the deterministic discovery/holdout split and the log(g_N) bin
edges for DISC-COSMOLOGY-MOND-SPARC-003, BEFORE any velocity/outcome data
is touched. Only predictor variables (Mtot_Msun, sepAU) are used here --
never pmRA/pmDE/velocity -- so this step cannot be tuned by the result.

Seed convention matches DISC-COSMOLOGY-MOND-SPARC-002 (lock date as an
integer). Split fraction: 70% discovery / 30% holdout (holdout sealed,
opened only at the Replication Gate, per METHODOLOGY_EXTENSIONS.md Sec.6).
"""
import json
import numpy as np
import pandas as pd

INPUT_PATH = "../data/quality_filtered_sample.parquet"
SPLIT_OUTPUT = "../data/discovery_holdout_split.json"
LOCK_DATE_SEED = 20260814
DISCOVERY_FRACTION = 0.70
N_BINS = 5

G_SI = 6.67430e-11  # m^3 kg^-1 s^-2
MSUN_KG = 1.98892e30
AU_M = 1.495978707e11


def main():
    df = pd.read_parquet(INPUT_PATH)
    n = len(df)
    rng = np.random.default_rng(LOCK_DATE_SEED)
    idx = np.arange(n)
    rng.shuffle(idx)
    n_discovery = int(round(n * DISCOVERY_FRACTION))
    discovery_idx = np.sort(idx[:n_discovery])
    holdout_idx = np.sort(idx[n_discovery:])

    pair_id = df["Source1"].astype(str) + "_" + df["Source2"].astype(str)
    split = {
        "seed": LOCK_DATE_SEED,
        "discovery_fraction": DISCOVERY_FRACTION,
        "n_total": n,
        "n_discovery": len(discovery_idx),
        "n_holdout": len(holdout_idx),
        "discovery_pair_ids": pair_id.iloc[discovery_idx].tolist(),
        "holdout_pair_ids": pair_id.iloc[holdout_idx].tolist(),
    }
    with open(SPLIT_OUTPUT, "w") as f:
        json.dump(split, f)

    disc = df.iloc[discovery_idx]
    g_N = G_SI * (disc["Mtot_Msun"].to_numpy() * MSUN_KG) / (disc["sepAU"].to_numpy() * AU_M) ** 2
    log_gN = np.log10(g_N)

    quantiles = np.linspace(0, 1, N_BINS + 1)
    edges = np.quantile(log_gN, quantiles)

    c = 299792458.0
    H0 = 70.0 * 1000.0 / 3.086e22
    a0_A = c * H0 / (2 * np.pi)
    a0_B = c * H0

    print(f"n_total={n}  n_discovery={len(discovery_idx)}  n_holdout={len(holdout_idx)}")
    print(f"log10(g_N) range in discovery: [{log_gN.min():.3f}, {log_gN.max():.3f}]  (g_N in m/s^2)")
    print(f"a0_A={a0_A:.6e}  a0_B={a0_B:.6e}")
    print(f"log10(a0_A)={np.log10(a0_A):.4f}  log10(a0_B)={np.log10(a0_B):.4f}")
    print(f"{N_BINS}-quantile bin edges (log10 g_N):", [f"{e:.4f}" for e in edges])
    counts, _ = np.histogram(log_gN, bins=edges)
    print("counts per bin:", counts.tolist())


if __name__ == "__main__":
    main()
