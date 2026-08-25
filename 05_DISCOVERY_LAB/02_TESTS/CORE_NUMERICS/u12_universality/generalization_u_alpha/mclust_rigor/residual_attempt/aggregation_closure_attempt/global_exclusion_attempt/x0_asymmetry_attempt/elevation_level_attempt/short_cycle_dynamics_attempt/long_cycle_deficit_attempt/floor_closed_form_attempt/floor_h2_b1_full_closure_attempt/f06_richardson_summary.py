"""
f06_richardson_summary.py -- reproducible grid-refinement sequence for the
corrected f04 solver (small domain, chosen just large enough to reach the
plateau at t0=0.03, so refinement is affordable), a Richardson extrapolation
to h->0, an S_MAX-truncation sensitivity check, and a final comparison table
against (a) this front's own already-archived T3 Monte Carlo
(fcd_t3.log, CITED not re-derived) and (b) the adversarial referee's
independent T3 replication (adversarial/REFEREE_REPORT.md SS3, CITED). No
new randomness is used in this script (the PDE solver is fully
deterministic); no seed is consumed.
"""
import numpy as np
import json
import time
import sys

sys.path.insert(0, ".")
from f04_corrected_2d_solver import solve

print("=" * 70)
print("Grid-refinement sequence (small domain G_MAX=0.05, S_MAX=0.10, target t0=0.03)")
print("=" * 70)

h_values = [0.001, 0.0005, 0.00025, 0.000125, 0.0000625, 0.00003125]
t0_target = 0.03
seq = []
for h in h_values:
    t_start = time.time()
    g_grid, Phi, Psi, hist = solve(0.05, 0.10, h, n_iter=600, verbose=False)
    j = int(round(t0_target / h))
    val = float(Phi[0, j])
    dt = time.time() - t_start
    seq.append(dict(h=h, phi=val, n_iter=len(hist), last_change=hist[-1][1], elapsed_s=dt))
    print(f"  h={h:.8f}  Phi(0,{t0_target})={val:.6f}  iters={len(hist)}  "
          f"last_change={hist[-1][1]:.2e}  elapsed={dt:.1f}s")

diffs = [seq[i + 1]["phi"] - seq[i]["phi"] for i in range(len(seq) - 1)]
ratios = [diffs[i + 1] / diffs[i] for i in range(len(diffs) - 1)]
print("\nSuccessive differences:", [f"{d:.5f}" for d in diffs])
print("Successive ratios (->0.5 expected for clean 1st-order h-convergence "
      "once past the ~1/c boundary-layer scale):", [f"{r:.3f}" for r in ratios])

# Richardson extrapolation using the finest two points, two ways:
v1, v2 = seq[-2]["phi"], seq[-1]["phi"]
last_ratio = ratios[-1]
L_assume_half = 2 * v2 - v1
L_observed_ratio = v2 + diffs[-1] * (last_ratio / (1 - last_ratio))
print(f"\nRichardson extrapolation (finest two points, h={seq[-2]['h']:.2e},{seq[-1]['h']:.2e}):")
print(f"  assuming exact ratio 0.5 (pure 1st order):        L = {L_assume_half:.5f}")
print(f"  using the OBSERVED ratio {last_ratio:.3f}:                    L = {L_observed_ratio:.5f}")
L_best = 0.5 * (L_assume_half + L_observed_ratio)
L_spread = abs(L_assume_half - L_observed_ratio)
print(f"  reported estimate (midpoint of the two): L ~= {L_best:.5f}  "
      f"(spread between methods: {L_spread:.5f} -- treated as an INFORMAL "
      f"uncertainty band, not a rigorous error bound)")

print()
print("=" * 70)
print("S_MAX truncation sensitivity (fixed h=0.001, original big domain)")
print("=" * 70)
sens = []
for S_MAX in [0.5, 0.7, 0.9]:
    g_grid, Phi, Psi, hist = solve(0.40, S_MAX, 0.001, n_iter=200, verbose=False)
    j = int(round(0.09 / 0.001))
    val = float(Phi[0, j])
    sens.append(dict(S_MAX=S_MAX, phi_at_009=val))
    print(f"  S_MAX={S_MAX}  Phi(0,0.09)={val:.6f}")

print()
print("=" * 70)
print("Comparison against CITED (not re-derived) Monte Carlo references")
print("=" * 70)
# fcd_t3.log (this front's own already-archived T3, already read in full in
# this dispatch -- CITED here, not re-run):
t3_front = {0.09: (0.03832, 0.00096), 0.37: (0.03885, 0.00097), 0.03: (0.03812, 0.00096)}
# adversarial/REFEREE_REPORT.md SS3 (independent T3 replication, N=200000/t0,
# CITED here, not re-run):
t3_referee = {0.09: (0.03744, 0.00042), 0.37: (0.03701, 0.00042), 0.01: (0.03770, 0.00043)}

comparisons = []
for label, table in [("this front's own T3 (fcd_t3.log)", t3_front),
                      ("referee's independent T3 replication", t3_referee)]:
    print(f"\n vs. {label}:")
    for t0, (val_mc, se_mc) in table.items():
        z = (val_mc - L_best) / se_mc
        comparisons.append(dict(source=label, t0=t0, mc_value=val_mc, mc_se=se_mc,
                                 pde_richardson_estimate=L_best, z=z))
        print(f"    t0={t0:.2f}  MC={val_mc:.5f}+-{se_mc:.5f}   "
              f"PDE-Richardson estimate={L_best:.5f}   z=(MC-PDE)/SE={z:+.2f}")

with open("f06_richardson_summary.json", "w") as fh:
    json.dump({
        "grid_sequence": seq, "diffs": diffs, "ratios": ratios,
        "richardson_assume_half": L_assume_half,
        "richardson_observed_ratio": L_observed_ratio,
        "richardson_best_estimate": L_best,
        "richardson_spread": L_spread,
        "s_max_sensitivity": sens,
        "mc_comparisons": comparisons,
    }, fh, indent=2)
