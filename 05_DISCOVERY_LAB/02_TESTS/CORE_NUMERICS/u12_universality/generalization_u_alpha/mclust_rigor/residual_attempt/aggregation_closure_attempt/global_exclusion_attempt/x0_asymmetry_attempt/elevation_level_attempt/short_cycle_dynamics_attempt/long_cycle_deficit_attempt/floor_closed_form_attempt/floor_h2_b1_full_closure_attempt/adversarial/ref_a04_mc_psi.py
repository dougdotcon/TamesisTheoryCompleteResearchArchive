#!/usr/bin/env python3
"""
REFEREE test R-B: fresh Monte Carlo of Psi(s0,g0) (mode-E start) against
the closed-form small-g coefficients:
   linear:     g0 * psi1(s0),      psi1(s) = sqrt(pi c/2) erfcx(s sqrt(c/2))
   +quadratic: + g0^2 * b2(s0),    b2(s) = -c - (c/2) sqrt(pi c/2) (1-2s) erfcx(.)
   +cubic:     + g0^3 * b3(s0)     (referee's closed form, ref_a01 PART D)
Replicates the front's T-A design (5 values of s0, 2 small g0) with a fresh
seed and checks the claimed pattern: linear-only biased at g0=3e-4
(|z| ~ 6-9), linear+quadratic |z| < ~2.

Fresh referee seed: SeedSequence(20260857001)   N = 300,000 per point.
"""
import json
import numpy as np
from scipy.special import erfcx
from ref_mc_lib import simulate

SEED = 20260857001
N = 300_000
C = 1000.0

def psi1(s):
    return np.sqrt(np.pi * C / 2) * erfcx(s * np.sqrt(C / 2))

def b2(s):
    return -C - (C / 2) * np.sqrt(np.pi * C / 2) * (1 - 2 * s) \
        * erfcx(s * np.sqrt(C / 2))

def b3(s):
    # ref_a01 PART D closed form:
    #   b3(s) = c^2 (8-7s)/12 + sqrt(2 pi) c^{3/2} (7cs^2-8cs+2c+7)/24 * erfcx
    return C**2 * (8 - 7 * s) / 12 + np.sqrt(2 * np.pi) * C**1.5 \
        * (7 * C * s**2 - 8 * C * s + 2 * C + 7) / 24 \
        * erfcx(s * np.sqrt(C / 2))

s0_list = [0.0, 0.01, 0.03, 0.05, 0.08]
g0_list = [0.0001, 0.0003]

ss = np.random.SeedSequence(SEED)
children = ss.spawn(len(s0_list) * len(g0_list))

LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    LOG.append(line)

log(f"REFEREE R-B: fresh MC of Psi(s0,g0) (mode-E start), seed "
    f"SeedSequence({SEED}), N={N} per point, c={C:.0f}")
log("")
log(f"{'s0':>5} {'g0':>7} {'phat':>10} {'sem':>9} "
    f"{'z_lin':>7} {'z_quad':>7} {'z_cub':>7}")
rows = []
ci = 0
for g0 in g0_list:
    for s0 in s0_list:
        rng = np.random.default_rng(children[ci]); ci += 1
        _, phat, sem = simulate(rng, N, g0, c=C, start_in_G=False, s0=s0)
        p1 = g0 * psi1(s0)
        p2 = p1 + g0**2 * b2(s0)
        p3 = p2 + g0**3 * b3(s0)
        z = lambda p: (phat - p) / sem
        log(f"{s0:5.2f} {g0:7.4f} {phat:10.6f} {sem:9.6f} "
            f"{z(p1):+7.2f} {z(p2):+7.2f} {z(p3):+7.2f}")
        rows.append(dict(s0=s0, g0=g0, phat=phat, sem=sem,
                         p_lin=p1, p_quad=p2, p_cub=p3,
                         z_lin=z(p1), z_quad=z(p2), z_cub=z(p3)))

log("")
log("front's claimed pattern (T-A): linear-only z from -6.2 to -9.2 at")
log("g0=3e-4; linear+quadratic |z|<2.0 at all 10 points.")
json.dump(rows, open('ref_a04_results.json', 'w'), indent=1)
with open('ref_a04_mc_psi.log', 'w') as f:
    f.write("\n".join(LOG) + "\n")
