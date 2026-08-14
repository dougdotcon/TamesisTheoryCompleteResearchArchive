"""
Apply pre-registered quality cuts to the El-Badry, Rix & Heintz (2021) Gaia
wide-binary catalog and derive component masses via the Pecaut & Mamajek
(2013) mass-luminosity relation (M_G -> Msun, tabulated by Mamajek and
fetched directly from the primary source, not assumed from memory).

This script ONLY filters the sample and derives masses -- it computes NO
test statistic. Cuts are taken from Chae (2023, ApJ 952, 128, arXiv:2305.04613)
and Chae (2023, arXiv:2309.10404), verified by direct fetch of both papers
(see PREREGISTRATION.md Section 3 for citations). Run BEFORE any
discovery/holdout split or fitting -- the resulting filtered sample size is
what the split is generated over.
"""
import numpy as np
import pandas as pd

CATALOG_PATH = "../data/catalog.parquet"
MAMAJEK_PATH = "../data/mamajek_mass_luminosity.tsv"
OUTPUT_PATH = "../data/quality_filtered_sample.parquet"

# --- Quality cuts, fixed a priori, sourced from Chae (2023) papers A & B ---
R_MAX = 0.01                 # chance-alignment probability (El-Badry R_chance_align)
SEP_MIN_AU, SEP_MAX_AU = 200.0, 30000.0
DIST_MAX_PC = 200.0
MG_MIN, MG_MAX = 4.0, 14.0
PM_RELERR_MAX = 0.01         # relative proper-motion error, both components
DIST_CONCORD_NSIGMA = 3.0    # |d_A - d_B| < N * sqrt(sigma_dA^2 + sigma_dB^2)
BINTYPE_REQUIRED = "MSMS"    # both components main-sequence


def load_mamajek_table(path):
    df = pd.read_csv(path, sep="\t")
    df = df.sort_values("M_G").reset_index(drop=True)
    return df["M_G"].to_numpy(), df["Msun"].to_numpy()


def mass_from_MG(M_G, mg_grid, msun_grid):
    """Linear interpolation on the Pecaut & Mamajek (2013) M_G -> Msun
    relation (Mamajek's continuously-updated table, fetched directly).
    Returns NaN outside the tabulated range (B3V..L2V, M_G in [-1.19, 17.3])."""
    M_G = np.asarray(M_G, dtype=float)
    out = np.interp(M_G, mg_grid, msun_grid, left=np.nan, right=np.nan)
    return out


def main():
    mg_grid, msun_grid = load_mamajek_table(MAMAJEK_PATH)

    cols = [
        "Source1", "Source2", "RAdeg", "DEdeg", "RA2deg", "DE2deg",
        "Plx1", "Plx2", "e_Plx1", "e_Plx2",
        "pmRA1", "pmRA2", "e_pmRA1", "e_pmRA2",
        "pmDE1", "pmDE2", "e_pmDE1", "e_pmDE2",
        "RUWE1", "RUWE2",
        "Gmag1", "Gmag2",
        "theta", "sepAU", "BinType", "R",
    ]
    df = pd.read_parquet(CATALOG_PATH, columns=cols)
    n0 = len(df)

    numeric_cols = [c for c in cols if c not in ("Source1", "Source2", "BinType")]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df.loc[df[c].abs() >= 1e19, c] = np.nan  # 1e20 sentinel

    mask = pd.Series(True, index=df.index)
    mask &= df["BinType"].astype(str).str.strip() == BINTYPE_REQUIRED
    mask &= df["R"] < R_MAX
    mask &= (df["sepAU"] >= SEP_MIN_AU) & (df["sepAU"] <= SEP_MAX_AU)

    d1_pc = 1000.0 / df["Plx1"]
    d2_pc = 1000.0 / df["Plx2"]
    sigma_d1 = d1_pc * (df["e_Plx1"] / df["Plx1"])
    sigma_d2 = d2_pc * (df["e_Plx2"] / df["Plx2"])
    d_mean_pc = (d1_pc + d2_pc) / 2.0
    mask &= (df["Plx1"] > 0) & (df["Plx2"] > 0)
    mask &= d_mean_pc < DIST_MAX_PC
    mask &= (d1_pc - d2_pc).abs() < DIST_CONCORD_NSIGMA * np.sqrt(sigma_d1**2 + sigma_d2**2)

    pm1_relerr = np.sqrt(df["e_pmRA1"]**2 + df["e_pmDE1"]**2) / df["pmRA1"].abs().clip(lower=1e-9)
    pm2_relerr = np.sqrt(df["e_pmRA2"]**2 + df["e_pmDE2"]**2) / df["pmRA2"].abs().clip(lower=1e-9)
    mask &= (pm1_relerr < PM_RELERR_MAX) & (pm2_relerr < PM_RELERR_MAX)

    M_G1 = df["Gmag1"] - 5 * np.log10(d1_pc) + 5
    M_G2 = df["Gmag2"] - 5 * np.log10(d2_pc) + 5
    mask &= (M_G1 >= MG_MIN) & (M_G1 <= MG_MAX)
    mask &= (M_G2 >= MG_MIN) & (M_G2 <= MG_MAX)

    mask &= mask.notna() if hasattr(mask, "notna") else True
    mask = mask.fillna(False)

    sel = df[mask].copy()
    sel["d1_pc"] = d1_pc[mask]
    sel["d2_pc"] = d2_pc[mask]
    sel["d_mean_pc"] = d_mean_pc[mask]
    sel["M_G1"] = M_G1[mask]
    sel["M_G2"] = M_G2[mask]
    sel["M1_Msun"] = mass_from_MG(sel["M_G1"], mg_grid, msun_grid)
    sel["M2_Msun"] = mass_from_MG(sel["M_G2"], mg_grid, msun_grid)
    sel = sel[sel["M1_Msun"].notna() & sel["M2_Msun"].notna()]
    sel["Mtot_Msun"] = sel["M1_Msun"] + sel["M2_Msun"]

    sel.to_parquet(OUTPUT_PATH, index=False)

    print(f"n0 (raw catalog)               = {n0}")
    print(f"n after BinType==MSMS+R+sepAU  = {int((mask).sum())} (pre-mass-interp final)")
    print(f"n final (mass interpolated ok) = {len(sel)}")
    print(f"Mtot_Msun range: {sel['Mtot_Msun'].min():.3f} - {sel['Mtot_Msun'].max():.3f}")
    print(f"sepAU range: {sel['sepAU'].min():.1f} - {sel['sepAU'].max():.1f}")
    print(f"d_mean_pc range: {sel['d_mean_pc'].min():.1f} - {sel['d_mean_pc'].max():.1f}")


if __name__ == "__main__":
    main()
