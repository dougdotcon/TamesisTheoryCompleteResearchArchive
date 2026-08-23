"""Referee's own T0 re-check: empirical confirmation that b=1 gives
R_mask == seed_mask exactly, and rho_measured ~= c/n. This is a *belt and
braces* empirical check; the primary T0 evidence is the direct code read of
sc_engine.build_R_mask (see REFEREE_REPORT.md sec 1: at b=1 the loop
`for _ in range(1, 1)` is empty, so R = seed_mask.copy() unconditionally,
with no other special-casing anywhere else in the file -- confirmed by
reading the whole file, not just build_R_mask)."""
import sys
import numpy as np

PARENT_DIR = ("/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/"
              "02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/"
              "mclust_rigor/residual_attempt/aggregation_closure_attempt/"
              "global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/"
              "short_cycle_dynamics_attempt")
sys.path.insert(0, PARENT_DIR)
import sc_engine  # noqa: E402

n, b, c = 65536, 1, 1000
N = 30
seed_base = 20260828100
ss = np.random.SeedSequence(seed_base)
children = ss.spawn(N)

violations = 0
rho_vals = []
for ch in children:
    rng = np.random.default_rng(ch)
    pi = sc_engine.build_pi(n, rng)
    seed_mask = sc_engine.build_seeds(n, c, rng)
    R_mask = sc_engine.build_R_mask(n, b, pi, seed_mask)
    if not np.array_equal(R_mask, seed_mask):
        violations += np.count_nonzero(R_mask != seed_mask)
    rho_vals.append(R_mask.mean())

rho_meas = np.mean(rho_vals)
rho_sem = np.std(rho_vals, ddof=1) / np.sqrt(N)
rho_formula = c / n
z = (rho_meas - rho_formula) / rho_sem

print(f"T0 re-check (referee, seed={seed_base}, N={N})")
print(f"  R_mask == seed_mask exactly at b=1: violations={violations}/{N}  "
      f"{'OK' if violations == 0 else 'FAIL'}")
print(f"  rho_formula (=c/n) = {rho_formula:.6f}   "
      f"rho_meas = {rho_meas:.6f}+/-{rho_sem:.6f}  z={z:+.3f}  "
      f"{'OK' if abs(z) < 4 else 'FAIL'}")
