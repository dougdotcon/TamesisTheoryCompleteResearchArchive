#!/usr/bin/env python3
"""
r02_power_law_fit.py

Core fitting/testing script for MCLUST-GAP-RATE-CANDIDATE-ATTEMPT.

Tests the candidate rate law (c/n)^{1/4} (referee-flagged, DISC-DEC-085
N1, never previously tested against the bin data) plus neighboring
exponents (c/n)^{1/3}, (c/n)^{1/5}, plus the three previously-tried rates
from the parent front's own Sec A.4 (1/n, 1/sqrt(n), sqrt(c/n) = (c/n)^{1/2}),
against the T1 and T2-composite bin tables (transcribed and cross-checked
in r01_reconstruct_and_crosscheck.py).

KEY STRUCTURAL FACT this script establishes numerically (not previously
stated this way in the record): c and n are FIXED at c=1000, n=65536
across every bin in T1/T2 -- only t0=L/n varies bin-to-bin. Therefore
ANY function of (c/n) alone, including every candidate in this family, is
a SINGLE CONSTANT NUMBER across all bins. This has two consequences,
verified numerically below:
  (1) Fitting a prefactor A to minimize sum((gap_i - A*rate)^2) over bins
      reduces exactly to A* = mean(gap_i)/rate (i.e. to fitting the
      sample mean) -- IDENTICAL residual pattern for every exponent p.
      "Goodness of shape fit" is therefore not a meaningful discriminator
      between candidates using this dataset alone.
  (2) Because g(p) := (c/n)^p is continuous, strictly monotonic in p, and
      ranges over (0,1) for p in (0,inf), there EXISTS some real p* with
      g(p*) = mean(gap)/1 exactly (a "natural", unfitted, prefactor-1
      match) -- solved for explicitly below. Whether the record's
      candidate p=1/4 is close to a NATURAL exponent from independent
      theory (it is not motivated by one anywhere in the record) or
      merely close to this unremarkable real number p* by accident is
      exactly the question this script's numbers are used to answer,
      honestly, in ATTEMPT.md.
"""
import math
import json

C = 1000
N = 65536

# Transcribed bin tables (verbatim from r01, itself cross-checked against
# the parent front's published numbers to <0.005pp everywhere).
T1_GAP = [26.72, 42.50, 49.26, 46.36, 41.96, 38.32]
T1_T0 = [0.011, 0.046, 0.092, 0.186, 0.375, 0.750]

T2_GAP = [35.78, 39.03, 37.46, 41.27, 38.73, 35.78, 40.27, 43.20, 37.46]
T2_T0 = [0.046, 0.091, 0.186, 0.312, 0.438, 0.562, 0.688, 0.812, 0.938]


def rate(p):
    return (C / N) ** p


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    return cov / math.sqrt(vx * vy)


def fit_report(name, gaps, t0s):
    mean_g = sum(gaps) / len(gaps)
    print(f"\n--- {name} (n_bins={len(gaps)}, mean gap={mean_g:.4f}%) ---")
    rows = []
    for label, p in [("1/n (p_equiv n/a)", None),
                      ("1/sqrt(n) (p_equiv n/a)", None),
                      ("(c/n)^(1/2)  [sqrt(c/n)]", 1/2),
                      ("(c/n)^(1/3)  [NEW, neighbor]", 1/3),
                      ("(c/n)^(1/4)  [NEW, referee N1 target]", 1/4),
                      ("(c/n)^(1/5)  [NEW, neighbor]", 1/5)]:
        if p is None:
            r = (1 / N) if "1/n" in label else (1 / math.sqrt(N))
        else:
            r = rate(p)
        A_fit = mean_g / (100 * r)  # prefactor fitting the MEAN in fraction units
        # residuals using the FITTED prefactor (degenerate: identical for all p)
        pred_fit = [100 * A_fit * r] * len(gaps)
        resid_fit = [gaps[i] - pred_fit[i] for i in range(len(gaps))]
        rms_fit = math.sqrt(sum(x**2 for x in resid_fit) / len(resid_fit))
        maxabs_fit = max(abs(x) for x in resid_fit)
        # residuals using an UN-FITTED, "natural" prefactor of exactly 1
        pred_nat = 100 * r
        resid_nat = [g - pred_nat for g in gaps]
        rms_nat = math.sqrt(sum(x**2 for x in resid_nat) / len(resid_nat))
        r_resid_t0 = pearson(t0s, resid_fit)
        rows.append(dict(label=label, rate_pct=100*r, A_fit=A_fit,
                          rms_fit_pp=rms_fit, maxabs_fit_pp=maxabs_fit,
                          pred_natural_pct=pred_nat, rms_natural_pp=rms_nat,
                          r_resid_vs_t0=r_resid_t0))
        print(f"{label:<40} rate={100*r:8.4f}%  A_fit={A_fit:7.4f}  "
              f"RMS(fit,pp)={rms_fit:6.3f}  max|resid_fit|(pp)={maxabs_fit:6.3f}  "
              f"pred@A=1:{pred_nat:8.4f}%  RMS(A=1,pp)={rms_nat:7.3f}  "
              f"r(resid_fit,t0)={r_resid_t0:+.4f}")
    return rows


def solve_p_star(mean_gap_frac):
    """Solve (c/n)^p = mean_gap_frac exactly for p (natural-log ratio)."""
    return math.log(mean_gap_frac) / math.log(C / N)


def main():
    print(f"c={C}, n={N}, c/n={C/N:.10f}")
    print(f"Nearest 'nice' fractions bracketing candidate exponents: "
          f"1/2={0.5}, 1/3={1/3:.4f}, 1/4={0.25}, 1/5={0.2}")

    out = {}
    out["T1"] = fit_report("T1 (absolute-ell bins, NOT cluster-corrected)", T1_GAP, T1_T0)
    out["T2_composite"] = fit_report("T2 composite (relative L/n bins, cluster-robust where applicable)", T2_GAP, T2_T0)

    print("\n=== Exact-unit-prefactor exponent p* (solves (c/n)^p = mean_gap) ===")
    for name, gaps in [("T1", T1_GAP), ("T2_composite", T2_GAP)]:
        mean_g = sum(gaps) / len(gaps) / 100.0
        p_star = solve_p_star(mean_g)
        print(f"{name}: mean_gap={mean_g*100:.4f}%  p* (unit-prefactor exponent) = {p_star:.6f}  "
              f"(1/p* = {1/p_star:.4f})")
        out[name + "_p_star"] = p_star

    # Demonstrate the degeneracy claim explicitly: residuals (fitted-A) for
    # p=1/3,1/4,1/5 are numerically identical to (gap_i - mean(gap)).
    print("\n=== Degeneracy check: residual_i (fitted-A model) vs (gap_i - mean(gap)) ===")
    for name, gaps in [("T1", T1_GAP), ("T2_composite", T2_GAP)]:
        mean_g = sum(gaps) / len(gaps)
        naive_resid = [g - mean_g for g in gaps]
        for p in (1/3, 1/4, 1/5):
            r = rate(p)
            A_fit = mean_g / 100 / r
            model_resid = [g - 100 * A_fit * r for g in gaps]
            max_diff = max(abs(model_resid[i] - naive_resid[i]) for i in range(len(gaps)))
            print(f"{name} p={p:.4f}: max|model_resid - (gap-mean)| = {max_diff:.2e} pp "
                  f"({'IDENTICAL (as predicted)' if max_diff < 1e-9 else 'DIFFERS -- investigate'})")

    with open("r02_fit_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved r02_fit_results.json")


if __name__ == "__main__":
    main()
