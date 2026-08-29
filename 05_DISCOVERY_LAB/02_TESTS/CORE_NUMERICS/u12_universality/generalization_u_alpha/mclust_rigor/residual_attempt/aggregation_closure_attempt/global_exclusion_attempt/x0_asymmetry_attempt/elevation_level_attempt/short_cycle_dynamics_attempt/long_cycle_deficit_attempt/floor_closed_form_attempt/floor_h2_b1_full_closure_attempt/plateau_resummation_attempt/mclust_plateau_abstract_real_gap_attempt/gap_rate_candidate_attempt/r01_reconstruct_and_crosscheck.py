#!/usr/bin/env python3
"""
r01_reconstruct_and_crosscheck.py

Step 1 of this front (MCLUST-GAP-RATE-CANDIDATE-ATTEMPT, wave 25 (d)).
Re-transcribes, VERBATIM, the two bin tables (T1, T2-composite) and the
exact abstract plateau constant Pi(1000) from the parent front's own
ATTEMPT.md (section A.2) and from
`long_cycle_deficit_attempt/floor_closed_form_attempt/ATTEMPT.md` (the
original source of T1/T2, cited by the parent, not re-simulated here).

This script's ONLY job is to recompute gap% := (Pi_abstract - phi_real) /
phi_real * 100 from these transcribed inputs and confirm it reproduces the
parent's own published numbers exactly (to rule out a transcription typo
before any fitting is done downstream). No new simulation, no randomness.

Data provenance (verbatim transcription, not re-derived):
  - Pi(1000) = 0.0377615983402126188243712025905770479904...
    (mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md sec A.1,
    itself cross-validated 3x independently: FLOORH2 solver, PLATRESUM
    series, and this lineage's own g04/ref04 grids -- all agree to
    <1e-38 relative. Reused here as an established constant, not
    recomputed.)
  - T1 (absolute-ell bins): ATTEMPT.md (parent) sec A.2, table T1,
    itself transcribed from floor_closed_form_attempt/ATTEMPT.md sec 2.
  - T2 composite (relative L/n bins, cluster-robust where applicable):
    ATTEMPT.md (parent) sec A.2, table T2 composite, itself transcribed
    from floor_closed_form_attempt/ATTEMPT.md sec 4 (point-level) with
    bins 8,9 replaced by the cluster-robust re-measurement per that
    document's own finding (verbatim numbers, see floor_closed_form_
    attempt/ATTEMPT.md line ~240 cluster table).
  - n = 65536, c = 1000 (the record's fixed target cell throughout this
    whole lineage -- restated identically by every document since
    wave-14).
"""
from decimal import Decimal, getcontext
getcontext().prec = 50

PI_ABSTRACT = Decimal("0.0377615983402126188243712025905770479904")

# T1: absolute-ell bins (floor_closed_form_attempt ATTEMPT.md sec 2,
# transcribed via the parent front's own sec A.2 table)
T1 = [
    # (ell_lo, ell_hi, t0_mid, phi_real, published_gap_pct)
    (500, 1000, 0.011, Decimal("0.0298"), 26.72),
    (2000, 4000, 0.046, Decimal("0.0265"), 42.50),
    (4000, 8000, 0.092, Decimal("0.0253"), 49.26),
    (8000, 16384, 0.186, Decimal("0.0258"), 46.36),
    (16384, 32768, 0.375, Decimal("0.0266"), 41.96),
    (32768, 65536, 0.750, Decimal("0.0273"), 38.32),
]

# T2 composite: relative L/n bins spanning the whole far tail
# (floor_closed_form_attempt ATTEMPT.md sec 4, point-level except bins
# 8,9 which use the cluster-robust re-measurement; transcribed via the
# parent front's own sec A.2 table)
T2 = [
    # (t0_mid, phi_real, published_gap_pct, is_cluster_robust)
    (0.046, Decimal("0.02781"), 35.78, False),
    (0.091, Decimal("0.02716"), 39.03, False),
    (0.186, Decimal("0.02747"), 37.46, False),
    (0.312, Decimal("0.02673"), 41.27, False),
    (0.438, Decimal("0.02722"), 38.73, False),
    (0.562, Decimal("0.02781"), 35.78, False),
    (0.688, Decimal("0.02692"), 40.27, False),
    (0.812, Decimal("0.02637"), 43.20, True),
    (0.938, Decimal("0.02747"), 37.46, True),
]

def gap_pct(phi_real):
    return (PI_ABSTRACT - phi_real) / phi_real * Decimal(100)

def main():
    print(f"Pi_abstract (transcribed) = {PI_ABSTRACT}")
    print()
    print("=== T1 cross-check ===")
    print(f"{'ell bin':<16}{'t0':>8}{'phi_real':>12}{'recomputed gap%':>18}{'published gap%':>16}{'|delta|':>10}")
    t1_max_delta = Decimal(0)
    for lo, hi, t0, phi, pub in T1:
        g = gap_pct(phi)
        d = abs(g - Decimal(str(pub)))
        t1_max_delta = max(t1_max_delta, d)
        print(f"[{lo},{hi})     {t0:>8}{float(phi):>12}{float(g):>18.4f}{pub:>16.2f}{float(d):>10.4f}")
    print(f"T1 max |recomputed - published| = {t1_max_delta} pp")
    print()

    print("=== T2 composite cross-check ===")
    print(f"{'t0':>8}{'phi_real':>12}{'recomputed gap%':>18}{'published gap%':>16}{'|delta|':>10}  cluster?")
    t2_max_delta = Decimal(0)
    gaps = []
    for t0, phi, pub, cluster in T2:
        g = gap_pct(phi)
        d = abs(g - Decimal(str(pub)))
        t2_max_delta = max(t2_max_delta, d)
        gaps.append(float(g))
        print(f"{t0:>8}{float(phi):>12}{float(g):>18.4f}{pub:>16.2f}{float(d):>10.4f}  {cluster}")
    print(f"T2 max |recomputed - published| = {t2_max_delta} pp")
    print()

    mean_g = sum(gaps) / len(gaps)
    rng = (min(gaps), max(gaps))
    spread = rng[1] - rng[0]
    t0s = [t0 for t0, *_ in T2]
    mean_t0 = sum(t0s) / len(t0s)
    cov = sum((t0s[i] - mean_t0) * (gaps[i] - mean_g) for i in range(len(t0s)))
    var_t0 = sum((x - mean_t0) ** 2 for x in t0s)
    var_g = sum((y - mean_g) ** 2 for y in gaps)
    r = cov / (var_t0 ** 0.5 * var_g ** 0.5)
    print(f"T2 composite recomputed: mean={mean_g:.4f}%, range=[{rng[0]:.4f}%,{rng[1]:.4f}%], "
          f"spread={spread:.4f}pp, Pearson r(gap%,t0)={r:.4f}")
    print("Published (parent ATTEMPT.md sec A.2): mean=38.78%, range=[35.78%,43.20%], "
          "spread=7.41pp, r=0.331")
    print()
    print("VERDICT:", "MATCH (transcription confirmed correct)"
          if t1_max_delta < Decimal("0.02") and t2_max_delta < Decimal("0.02")
          else "MISMATCH -- investigate before proceeding")

if __name__ == "__main__":
    main()
