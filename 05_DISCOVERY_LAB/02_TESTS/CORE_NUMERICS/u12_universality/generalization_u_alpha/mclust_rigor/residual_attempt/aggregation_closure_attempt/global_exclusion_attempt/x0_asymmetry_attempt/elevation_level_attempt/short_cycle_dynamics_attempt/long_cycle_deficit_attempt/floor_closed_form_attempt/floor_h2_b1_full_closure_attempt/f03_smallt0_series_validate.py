"""
f03_smallt0_series_validate.py -- high-powered, fresh-seed Monte Carlo test
of the small-t0 series for Phi(0,t0) = phi_abstract(t0) derived in f01:

  Phi(0,t0) = 1 - c*t0 + a2(0)*t0^2 + a3(0)*t0^3 + O(t0^4)

against (a) the naive pure-race prediction e^{-c t0} (0-th/1st order),
(b) the 2-term series (through t0^2), (c) the 3-term series (through t0^3).

Motivation for doing this at high N specifically: the archived T3 run
(fcd_t3.py, N=40000/t0) has SE ~0.002-0.003 at the smallest t0 values, and a
first look at its own logged numbers (fcd_t3.log) showed the 3-term series
prediction landing ~2.7 sigma from the logged t0=0.0003 point -- WORSE than
the 2-term prediction, despite a3(0) passing two independent numerical
cross-checks in f01 (finite-difference derivative check + ODE-shooting check
for the ingredients that feed it) and an exact sympy re-derivation of the
recursion itself. Before concluding anything about the series' radius of
convergence, get a properly-powered, independently-seeded measurement of our
own, per this archive's own standing discipline (a single N=40000 log value
is not enough evidence to conclude a well-checked formula is wrong).

Seeds: SeedSequence(20260856001) (this front's reserved range).
"""
import numpy as np
import json
import time
import sys

sys.path.insert(0, ".")
from abstract_proc import phi_hat

with open("series_coeffs.json") as fh:
    coeffs = json.load(fh)

C = coeffs["c"]
a0, a1, a2_0, a3_0 = coeffs["a0"], coeffs["a1"], coeffs["a2_0"], coeffs["a3_0"]

t0_values = [0.00003, 0.00005, 0.0001, 0.0002, 0.0003, 0.0005, 0.0007, 0.001]
N = 500000

ss = np.random.SeedSequence(20260856001)
children = ss.spawn(len(t0_values))

print(f"c={C}, a1={a1}, a2(0)={a2_0:.4f}, a3(0)={a3_0:.4f}\n")
print(f"{'t0':>9} {'c*t0':>7} {'N':>7} {'phi_hat':>10} {'SE':>9} "
      f"{'e^-ct0':>10} {'z(exp)':>8} {'2-term':>10} {'z(2t)':>8} "
      f"{'3-term':>10} {'z(3t)':>8}")

rows = []
t_start = time.time()
for t0, child in zip(t0_values, children):
    rng = np.random.default_rng(child)
    p, se = phi_hat(t0, C, N, rng)
    exp_pred = np.exp(-C * t0)
    two_term = a0 + a1 * t0 + a2_0 * t0 ** 2
    three_term = two_term + a3_0 * t0 ** 3
    z_exp = (p - exp_pred) / se
    z_2t = (p - two_term) / se
    z_3t = (p - three_term) / se
    rows.append(dict(t0=t0, ct0=C * t0, N=N, phi_hat=p, se=se,
                      exp_pred=exp_pred, z_exp=z_exp,
                      two_term=two_term, z_2t=z_2t,
                      three_term=three_term, z_3t=z_3t))
    print(f"{t0:9.5f} {C*t0:7.3f} {N:7d} {p:10.6f} {se:9.6f} "
          f"{exp_pred:10.6f} {z_exp:8.2f} {two_term:10.6f} {z_2t:8.2f} "
          f"{three_term:10.6f} {z_3t:8.2f}")

print(f"\nelapsed: {time.time()-t_start:.1f}s")

with open("f03_results.json", "w") as fh:
    json.dump(rows, fh, indent=2)
