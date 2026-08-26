#!/usr/bin/env python3
"""
Compute Pi(c) = lim_{t0->inf} Phi(0,t0) via direct summation of the
independently-derived (P,Q)-family series, with 3-way error control
(approach error via multiple c*t0 targets; truncation via last-term size;
roundoff via a higher-dps rerun at one c value, done separately).
"""
import time
import sys
import json
import mpmath as mp
from ref01_family_series import build_family, eval_family

def stable_digits(x, y):
    if x == y:
        return mp.mp.dps
    diff = abs(x - y)
    scale = max(abs(x), abs(y))
    if scale == 0:
        return mp.mp.dps
    reldiff = diff / scale
    if reldiff == 0:
        return mp.mp.dps
    return int(-mp.log10(reldiff))

def compute_pi(c_val, K, dps, ct0_targets):
    mp.mp.dps = dps
    t0s = time.time()
    a, b = build_family(c_val, K, dps)
    build_time = time.time() - t0s
    c = mp.mpf(c_val)

    # precompute a_k(0) once
    a0 = [eval_family(a[k], mp.mpf(0), c) for k in range(K + 1)]

    results = {}
    last_term_rel = {}
    for ct0 in ct0_targets:
        t0v = mp.mpf(ct0) / c
        S = mp.mpf(0)
        last_term = None
        for k in range(K + 1):
            term = a0[k] * t0v ** k
            S += term
            last_term = term
        results[ct0] = S
        last_term_rel[ct0] = abs(last_term) / abs(S) if S != 0 else None

    ks = sorted(ct0_targets)
    sd = stable_digits(results[ks[-1]], results[ks[-2]]) if len(ks) >= 2 else None

    return {
        "c": c_val, "K": K, "dps": dps,
        "build_time": build_time,
        "results": {str(k): mp.nstr(v, dps) for k, v in results.items()},
        "last_term_rel": {str(k): (mp.nstr(v, 5) if v is not None else None) for k, v in last_term_rel.items()},
        "stable_digits_estimate": sd,
        "Pi_c": mp.nstr(results[ks[-1]], min(dps, 45)),
    }

if __name__ == "__main__":
    c_val = float(sys.argv[1]) if len(sys.argv) > 1 else 1000
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    dps = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    ct0_targets = [60, 80, 100]
    res = compute_pi(c_val, K, dps, ct0_targets)
    print(json.dumps(res, indent=2))
