#!/usr/bin/env python3
"""
r03_plateau_multi_c.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Computes the abstract b=1 floor plateau constant

    Pi(c) := lim_{t0->inf} Phi(0,t0)

to high precision at a ladder of c values, by summing the exact (P,Q)-family
series Phi(0,t0) = sum_k a_k(0) t0^k at several c*t0 values.

COST STRUCTURE (found the hard way -- see self-caught issue in ATTEMPT.md):
the series has entire-order-2-like content: partial-sum terms reach
~e^{c t0^2/2} before cancelling (in addition to the ~e^{c t0} race content),
so at fixed target c*t0 the required K scales like ~c t0^2 = (ct0)^2/c and
the required dps like ~ (ct0)^2/(2 ln10 c). Small c is therefore EXPENSIVE:
each c gets its own (K, dps, ct0 list). A first attempt at uniform
K=1500/dps=320 produced pure cancellation garbage at c=1 (partial sums
~1e+1866), caught immediately by the max|term|/agreement diagnostics.

Error control, per c:
  * approach error |Pi(c) - S(t0)|: measured empirically as the pairwise
    differences of the three S(ct0/c) sums; digits reported = stable common
    prefix of the two largest-ct0 sums.
  * truncation: last |term| of the K-term sum reported (must be << 1e-target).
  * roundoff: c=1000 rerun at dps=400 vs dps=320 (job 'control').

Deterministic; no randomness.

usage: python3 r03_plateau_multi_c.py JOBNAME
"""

import json
import sys
import time
from mpmath import mp, mpf, fabs, log10, nstr

sys.path.insert(0, '.')
from r01_family_series import FamilyRecursion, sum_series

# job -> list of (c, K, dps, [ct0 values])
# K sizing: K >= max( ~2*alpha*X2 with X2=(ct0max)^2/2c and alpha from
# alpha(1-ln alpha) = -(1 + (digits+margin)*ln10/X2)  [Gaussian content],
#                     ~1.7*4.25*ct0max                [race content] )
# dps sizing: log10(max term) + 115 target digits + >=60 margin.
JOBS = {
    # large-c ladder (direct summation feasible; Borel job covers c<=40)
    'ladder': [
        (160,    2600, 380, [230, 260, 290]),
        (250,    2100, 380, [230, 260, 290]),
        (640,    2000, 360, [230, 260, 290]),
        (1000,   2000, 360, [230, 260, 290]),
        (2560,   2000, 360, [230, 260, 290]),
        (10240,  2000, 360, [230, 260, 290]),
        (40960,  2000, 360, [230, 260, 290]),
        (163840, 2000, 360, [230, 260, 290]),
        (655360, 2000, 360, [230, 260, 290]),
    ],
    # roundoff control
    'control': [
        (1000, 2000, 440, [230, 260, 290]),
    ],
    # ---- corrected-sizing jobs (empirical rule measured from the c=1000
    # and c=160 first-pass runs: log(max|term|) ~= ct0 + 0.92*(ct0)^2/c,
    # i.e. the cancellation content is ~e^{c t0^2} not ~e^{c t0^2/2};
    # K from 2*alpha*X2' (X2'=0.92*(ct0max)^2/c) with 10-20% safety) ----
    'fixmid': [
        (640, 2400, 420, [230, 260, 290]),
        (250, 3300, 480, [230, 260, 290]),
        (160, 4700, 560, [230, 260, 290]),
    ],
    'c100deep': [
        (100, 7400, 690, [230, 260, 290]),
    ],
    'c40deep': [
        (40, 16000, 1200, [230, 260, 290]),
    ],
    'c10mid': [
        (10, 11400, 800, [100, 110, 120]),
    ],
    'c1small': [
        (1, 7200, 480, [25, 30]),
    ],
}


def run_one(cval, K, dps, ct0s):
    mp.dps = dps
    t = time.time()
    fr = FamilyRecursion(cval)
    out = fr.run(K)
    a0 = out['a0']
    res = {'c': cval, 'K': K, 'dps': dps, 'ct0s': ct0s}
    vals = []
    for ct0 in ct0s:
        t0 = mpf(ct0) / cval
        v, mx, last = sum_series(a0, t0)
        vals.append(v)
        res[f'S_ct0_{ct0}'] = nstr(v, 130)
        res[f'maxterm_ct0_{ct0}'] = float(log10(mx)) if mx > 0 else None
        res[f'lastterm_ct0_{ct0}'] = float(log10(last)) if last > 0 else -1e9
    d1, d2 = vals[-2], vals[-1]
    diff = fabs(d1 - d2)
    res['approach_last_two'] = nstr(diff, 5)
    res['approach_first_last'] = nstr(fabs(vals[0] - d2), 5)
    rel = diff / fabs(d2) if d2 != 0 else mpf(1)
    res['stable_digits'] = int(-log10(rel)) if rel > 0 else dps
    res['plateau'] = nstr(d2, 120)
    res['runtime_s'] = round(time.time() - t, 1)
    return res


def main():
    job = sys.argv[1]
    results = []
    outfile = f'r03_plateau_values_{job}.json'
    for (cval, K, dps, ct0s) in JOBS[job]:
        r = run_one(cval, K, dps, ct0s)
        results.append(r)
        print(f"c={cval:>7}  K={K} dps={dps}  stable_digits={r['stable_digits']}"
              f"  last|term|~1e{r[f'lastterm_ct0_{ct0s[-1]}']:.0f}"
              f"  max|term|~1e{r[f'maxterm_ct0_{ct0s[-1]}']:.0f}"
              f"  ({r['runtime_s']}s)")
        print(f"   Pi({cval}) = {r['plateau']}")
        print(f"   |S_mid-S_hi| = {r['approach_last_two']}   "
              f"|S_lo-S_hi| = {r['approach_first_last']}")
        sys.stdout.flush()
        with open(outfile, 'w') as f:
            json.dump(results, f, indent=1)


if __name__ == '__main__':
    main()
