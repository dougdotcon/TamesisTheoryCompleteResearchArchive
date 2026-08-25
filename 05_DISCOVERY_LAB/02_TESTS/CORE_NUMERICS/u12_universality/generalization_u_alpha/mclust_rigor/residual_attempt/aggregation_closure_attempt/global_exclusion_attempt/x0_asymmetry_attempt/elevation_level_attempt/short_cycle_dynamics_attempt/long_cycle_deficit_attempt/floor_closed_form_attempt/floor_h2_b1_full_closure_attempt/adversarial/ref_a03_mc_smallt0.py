#!/usr/bin/env python3
"""
REFEREE test R-A: fresh Monte Carlo of Phi(0,t0) at small t0, against
  (i)   the naive e^{-c t0},
  (ii)  the front's 2-term series  1 - c t0 + a2(0) t0^2,
  (iii) the front's 3-term series  ... + a3(0) t0^3,
  (iv)  the referee's full closed-form-coefficient series (S_500, ref_a02).
Tests BOTH the claimed validity window (3-term |z|<~1 for c*t0 <~ 0.3) and
the claimed clean breakdown beyond (c*t0 >~ 0.5-0.7).

Fresh referee seed: SeedSequence(20260857000)   N = 500,000 per t0.
"""
import json
import numpy as np
from ref_mc_lib import simulate

SEED = 20260857000
N = 500_000
C = 1000.0

coeff = json.load(open('ref_series_coeffs.json'))
a2, a3 = coeff['a2_0'], coeff['a3_0']
ak = json.load(open('ref_a02_series.json'))['a_k0_first30']

def series_full(t0, K=25):
    return float(sum(ak[k] * t0**k for k in range(K + 1)))

t0_list = [0.00003, 0.00005, 0.0001, 0.0002, 0.0003, 0.0005, 0.0007, 0.001]
ss = np.random.SeedSequence(SEED)
children = ss.spawn(len(t0_list))

LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    LOG.append(line)

log(f"REFEREE R-A: fresh MC of Phi(0,t0), seed SeedSequence({SEED}), "
    f"N={N} per point, c={C:.0f}")
log("")
log(f"{'t0':>9} {'c*t0':>6} {'phat':>10} {'sem':>9} "
    f"{'z_exp':>7} {'z_2term':>8} {'z_3term':>8} {'z_full':>7}")
rows = []
for t0, ch in zip(t0_list, children):
    rng = np.random.default_rng(ch)
    _, phat, sem = simulate(rng, N, t0, c=C, start_in_G=True, s0=0.0)
    p_exp = np.exp(-C * t0)
    p2 = 1 - C * t0 + a2 * t0**2
    p3 = p2 + a3 * t0**3
    pf = series_full(t0)
    z = lambda p: (phat - p) / sem
    log(f"{t0:9.5f} {C*t0:6.2f} {phat:10.6f} {sem:9.6f} "
        f"{z(p_exp):+7.2f} {z(p2):+8.2f} {z(p3):+8.2f} {z(pf):+7.2f}")
    rows.append(dict(t0=t0, phat=phat, sem=sem, p_exp=p_exp, p2=p2, p3=p3,
                     p_full=pf, z_exp=z(p_exp), z2=z(p2), z3=z(p3),
                     z_full=z(pf)))

log("")
log("front's claimed window: 3-term |z|<1 for c*t0 <~ 0.3, clean breakdown")
log("by c*t0 ~ 0.5-0.7.  Referee's full-series column tests whether any")
log("residual misfit is MC noise (|z_full| small everywhere) or model error.")
json.dump(rows, open('ref_a03_results.json', 'w'), indent=1)
with open('ref_a03_mc_smallt0.log', 'w') as f:
    f.write("\n".join(LOG) + "\n")
