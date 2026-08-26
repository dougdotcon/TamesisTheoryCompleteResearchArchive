"""
k04_uniformity_grid.py -- MCLUST-H1-VALIDITY-ATTEMPT, main experiment.

Direct numerical test of H1 (uniform validity of the outer/inner
matched-asymptotics decomposition), extended in the x-direction: computes
F(x;c) := lim_{g->inf} Phi(s,g) [x = s*sqrt(c)] at a grid of c values
(covering both smaller and larger c than the 2-value, 5-x-value spot
check in plateau_resummation_attempt/ATTEMPT.md Section 6) and a WIDER
x-range (0 to 8, vs. the record's 0 to 3), then measures, at each order
N=1,2:

    rho_N(x,c) := [F(x;c) - sum_{n=1}^{N} eps^n psi_n(x)] / eps^{N+1}

which the matched-asymptotics derivation predicts converges to psi_{N+1}(x)
as eps->0 (c->inf), AT EACH FIXED x. H1's claim of UNIFORM validity is
the stronger statement that this convergence (and the size of the
remainder, in eps^{N+1} units) does not degrade as x grows over the
tested range -- i.e. that the same asymptotic order holds with an
x-INDEPENDENT (or at least x-bounded) implied constant, not just
pointwise at x=0.

Per-c (K, dps) sizing was determined by direct convergence probing
(k01/k02 exploration, disclosed in ATTEMPT.md Section 3) -- each choice
verified to give >=15 stable digits at t0=45/c vs t0=60/c, for x up to 8,
BEFORE being used here.
"""
import json
import time
import mpmath as mp
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k01_family_series as fam
import k03_profiles as prof

GRID_C = [
    # (c, K, dps)
    (200, 300, 60),
    (500, 400, 60),
    (1000, 250, 60),
    (2000, 500, 70),
    (4000, 700, 90),
    (8000, 1000, 110),
]
GRID_X = [0, 0.5, 1, 2, 4, 6, 8]

results = []

t_start = time.time()
for c, K, DPS in GRID_C:
    t0 = time.time()
    a, b = fam.build_family(c, K, DPS)
    build_t = time.time() - t0
    mp.mp.dps = DPS
    sqc = mp.sqrt(mp.mpf(c))
    eps = 1 / sqc
    t0_plateau = mp.mpf(50) / c   # c*t0 = 50 -> e^{-50} ~ 2e-22, negligible
    t0_check = mp.mpf(60) / c

    for x in GRID_X:
        s0 = mp.mpf(x) / sqc
        F = fam.phi_series_sum(a, s0, t0_plateau, K, c)
        Fchk = fam.phi_series_sum(a, s0, t0_check, K, c)
        approach_reldiff = abs((F - Fchk) / Fchk) if Fchk != 0 else abs(F - Fchk)

        p1 = prof.psi1(x)
        p2 = prof.psi2(x)
        p3 = prof.psi3(x)

        rho1 = (F - eps * p1) / eps**2          # should -> psi2(x)
        rho2 = (F - eps * p1 - eps**2 * p2) / eps**3   # should -> psi3(x)
        rho3 = (F - eps * p1 - eps**2 * p2 - eps**3 * p3) / eps**4  # 4th-order residual, no target

        gap1 = rho1 - p2   # should -> 0 as eps->0 at fixed x
        gap2 = rho2 - p3   # should -> 0 as eps->0 at fixed x

        row = dict(
            c=c, x=x, eps=str(eps), F=str(F),
            approach_reldiff=str(approach_reldiff),
            psi1=str(p1), psi2=str(p2), psi3=str(p3),
            rho1=str(rho1), rho2=str(rho2), rho3=str(rho3),
            gap1=str(gap1), gap2=str(gap2),
            gap1_over_eps=str(gap1 / eps), gap2_over_eps=str(gap2 / eps),
        )
        results.append(row)

    print(f"c={c:6d} K={K:5d} dps={DPS:4d} build={build_t:6.2f}s  "
          f"max approach_reldiff over x-grid = "
          f"{max(float(abs(mp.mpf(r['approach_reldiff']))) for r in results if r['c']==c):.2e}")

print(f"\nTotal wall time: {time.time()-t_start:.1f}s")

with open("k04_uniformity_grid_results.json", "w") as f:
    json.dump(results, f, indent=1)

# ---------------------------------------------------------------------
# Human-readable summary tables
# ---------------------------------------------------------------------
print("\n=== rho1(x,c) vs predicted psi2(x)  (order-1 residual, should -> psi2) ===")
print(f"{'c':>6} {'x':>5} {'rho1':>16} {'psi2(pred)':>16} {'gap1':>12} {'gap1/eps':>12}")
for r in results:
    print(f"{r['c']:>6} {r['x']:>5} {mp.nstr(mp.mpf(r['rho1']),8):>16} "
          f"{mp.nstr(mp.mpf(r['psi2']),8):>16} {mp.nstr(mp.mpf(r['gap1']),4):>12} "
          f"{mp.nstr(mp.mpf(r['gap1_over_eps']),4):>12}")

print("\n=== rho2(x,c) vs predicted psi3(x)  (order-2 residual, should -> psi3) ===")
print(f"{'c':>6} {'x':>5} {'rho2':>16} {'psi3(pred)':>16} {'gap2':>12} {'gap2/eps':>12}")
for r in results:
    print(f"{r['c']:>6} {r['x']:>5} {mp.nstr(mp.mpf(r['rho2']),8):>16} "
          f"{mp.nstr(mp.mpf(r['psi3']),8):>16} {mp.nstr(mp.mpf(r['gap2']),4):>12} "
          f"{mp.nstr(mp.mpf(r['gap2_over_eps']),4):>12}")
