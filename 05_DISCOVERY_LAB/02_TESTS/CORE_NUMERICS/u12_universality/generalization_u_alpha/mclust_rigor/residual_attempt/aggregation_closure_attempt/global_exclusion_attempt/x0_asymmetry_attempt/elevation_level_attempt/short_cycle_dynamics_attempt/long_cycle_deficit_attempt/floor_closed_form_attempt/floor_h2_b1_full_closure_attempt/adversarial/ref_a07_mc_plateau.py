#!/usr/bin/env python3
"""
REFEREE test R-C: fresh, high-power Monte Carlo of Phi(0,t0) in the
practically relevant plateau range, to test:
  (i)  the front's Richardson-extrapolated claim  Phi(0, t0>~0.01) ~= 0.0377
  (ii) the referee's exact-series values (ref_a02): Phi(0,0.01)=0.0377932,
       plateau constant 0.03776160 for t0 >= 0.02.

Fresh referee seed: SeedSequence(20260857002)   N = 1,000,000 per t0.
"""
import json
import numpy as np
from ref_mc_lib import simulate

SEED = 20260857002
N = 1_000_000
C = 1000.0

series = json.load(open('ref_a02_series.json'))
S500 = {float(k): v[0] for k, v in series['t0_S500'].items()}
plateau = series['plateau_S500']

t0_list = [0.01, 0.03, 0.09, 0.37]
ss = np.random.SeedSequence(SEED)
children = ss.spawn(len(t0_list))

LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    LOG.append(line)

log(f"REFEREE R-C: fresh MC of Phi(0,t0) in the plateau range, seed "
    f"SeedSequence({SEED}), N={N} per point, c={C:.0f}")
log("")
log(f"{'t0':>6} {'phat':>10} {'sem':>9} {'z_vs_0.0377':>12} "
    f"{'series':>10} {'z_vs_series':>12}")
rows = []
for t0, ch in zip(t0_list, children):
    rng = np.random.default_rng(ch)
    _, phat, sem = simulate(rng, N, t0, c=C, start_in_G=True, s0=0.0)
    zr = (phat - 0.0377) / sem
    sv = S500.get(t0, plateau)
    zs = (phat - sv) / sem
    log(f"{t0:6.2f} {phat:10.6f} {sem:9.6f} {zr:+12.2f} {sv:10.6f} {zs:+12.2f}")
    rows.append(dict(t0=t0, phat=phat, sem=sem, z_richardson=zr,
                     series=sv, z_series=zs))

log("")
log("(t0=0.37 compared against the t0>=0.02 plateau constant 0.03776160;")
log(" the exact series was summed only to t0=0.09 in ref_a02, but its")
log(" plateau approach is ~e^{-c t0}, i.e. already <1e-50 beyond t0=0.09.)")
json.dump(rows, open('ref_a07_results.json', 'w'), indent=1)
with open('ref_a07_mc_plateau.log', 'w') as f:
    f.write("\n".join(LOG) + "\n")
