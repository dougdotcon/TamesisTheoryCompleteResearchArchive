#!/usr/bin/env python3
"""
r03_perbin_and_exploratory.py

Two additional pieces, both directly responsive to the mandate's own
wording:

PART A (mandate-literal): "whether the prefactor is consistent across all
bins/t0 values or drifts" -- computed here as the PER-BIN implied
prefactor A_i := gap_i / (100 * rate), for rate = (c/n)^{1/4} fixed
(c=1000, n=65536 do not vary bin-to-bin, so this is mathematically
guaranteed to have the same RELATIVE spread as gap_i itself -- shown
explicitly, not asserted).

PART B (exploratory extension, clearly beyond the literal mandate, added
because it is cheap and because the mandate explicitly invites checking
"whether the shape ... is actually well-matched ... or just coincidentally
close in magnitude"): a t0-DEPENDENT generalization motivated by the
parent front's own Sec A.3 "mode-E / s+g<=1 boundary" discussion --
replace the fixed pool n by an effective REMAINING pool n_eff(t0) :=
n*(1-t0) (the room left before the physical s+g<=1 ceiling). This makes
rate_eff(t0) = (c/n_eff(t0))^p actually vary across bins, so a real
(non-degenerate) least-squares fit of a single prefactor A across all
bins is possible, and its R^2 against the mean-only null model is a
meaningful number (unlike Part A / r02, where it is not). This is NOT the
literally-mandated candidate -- it is reported separately and labeled
speculative.
"""
import math
import json

C = 1000
N = 65536

T1_GAP = [26.72, 42.50, 49.26, 46.36, 41.96, 38.32]
T1_T0 = [0.011, 0.046, 0.092, 0.186, 0.375, 0.750]

T2_GAP = [35.78, 39.03, 37.46, 41.27, 38.73, 35.78, 40.27, 43.20, 37.46]
T2_T0 = [0.046, 0.091, 0.186, 0.312, 0.438, 0.562, 0.688, 0.812, 0.938]


def rate_fixed(p):
    return (C / N) ** p


def r2_vs_mean(observed, predicted):
    mean_o = sum(observed) / len(observed)
    ss_res = sum((observed[i] - predicted[i]) ** 2 for i in range(len(observed)))
    ss_tot = sum((o - mean_o) ** 2 for o in observed)
    return 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')


def part_a(name, gaps, t0s):
    print(f"\n=== PART A: per-bin implied prefactor, {name}, rate=(c/n)^(1/4) ===")
    r14 = rate_fixed(1/4) * 100  # in percent
    print(f"(c/n)^(1/4) = {r14:.4f}%  (constant, same for every bin)")
    print(f"{'t0':>8}{'gap% obs':>10}{'A_i=gap_i/rate':>16}")
    A_list = []
    for t0, g in zip(t0s, gaps):
        A_i = g / r14
        A_list.append(A_i)
        print(f"{t0:>8}{g:>10.2f}{A_i:>16.4f}")
    meanA = sum(A_list) / len(A_list)
    spreadA = (max(A_list) - min(A_list))
    rel_spread = spreadA / meanA * 100
    print(f"mean A_i={meanA:.4f}  range=[{min(A_list):.4f},{max(A_list):.4f}]  "
          f"relative spread={rel_spread:.2f}%  (identical, by construction, to "
          f"the relative spread of gap_i itself, since rate_i is a bin-independent "
          f"constant)")
    return dict(mean_A=meanA, range_A=[min(A_list), max(A_list)], rel_spread_pct=rel_spread)


def part_b(name, gaps, t0s, p):
    print(f"\n=== PART B (exploratory, non-mandate): n_eff(t0)=n*(1-t0), "
          f"rate_eff(t0)=(c/n_eff)^{p:.4f}, {name} ===")
    xs = []
    for t0 in t0s:
        n_eff = N * (1 - t0)
        xs.append((C / n_eff) ** p * 100)  # percent
    # Real (non-degenerate) least-squares fit of y = A*x (single free param A)
    sx2 = sum(x**2 for x in xs)
    sxy = sum(xs[i] * gaps[i] for i in range(len(xs)))
    A = sxy / sx2
    pred = [A * x for x in xs]
    resid = [gaps[i] - pred[i] for i in range(len(gaps))]
    rms = math.sqrt(sum(r**2 for r in resid) / len(resid))
    maxabs = max(abs(r) for r in resid)
    r2 = r2_vs_mean(gaps, pred)
    print(f"fitted A={A:.4f}  RMS resid={rms:.3f}pp  max|resid|={maxabs:.3f}pp  "
          f"R^2 (vs mean-only null)={r2:.4f}")
    print(f"{'t0':>8}{'rate_eff%':>12}{'pred%':>10}{'obs%':>10}{'delta(pp)':>12}")
    for i in range(len(t0s)):
        print(f"{t0s[i]:>8}{xs[i]:>12.4f}{pred[i]:>10.4f}{gaps[i]:>10.2f}{resid[i]:>12.4f}")
    return dict(A=A, rms_pp=rms, maxabs_pp=maxabs, r2_vs_mean=r2)


def main():
    out = {}
    out["T1_partA"] = part_a("T1", T1_GAP, T1_T0)
    out["T2_partA"] = part_a("T2 composite", T2_GAP, T2_T0)

    for p, label in [(1/4, "p=1/4"), (1/3, "p=1/3"), (1/5, "p=1/5")]:
        out[f"T1_partB_{label}"] = part_b("T1", T1_GAP, T1_T0, p)
        out[f"T2_partB_{label}"] = part_b("T2 composite", T2_GAP, T2_T0, p)

    with open("r03_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved r03_results.json")


if __name__ == "__main__":
    main()
