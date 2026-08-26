"""
g04_compute_grid.py -- compute Pi(c) at a fresh grid of c values, fully
independently (own (P,Q)-family implementation, g01, validated against
6 published anchors in g02) of both ancestor fronts' own computations.

Precision target here is deliberately much lower than the ancestor fronts'
(>=110 digits): ~28-32 stable digits is already 20+ orders of magnitude
more than needed to resolve the eps^4/eps^5 asymptotic terms at every c
used (see g05_residual_isolation.py), and is far cheaper -- this lets this
front reach c=100, a c-value neither ancestor front could complete (their
own disclosed cost wall stopped at c=250, expensively, at reduced 46-digit
precision).

Three-way error control per c (matching the record's own convention,
recalibrated): S(ct0=60), S(ct0=80), S(ct0=100); reported value is
S(ct0=100), with |S(80)-S(100)| as the approach-error diagnostic.
"""
import json
import time
import mpmath as mp
from g01_family_series import build_a_b


def S(a, t0, K):
    t0 = mp.mpf(t0)
    s = mp.mpf(0)
    p = mp.mpf(1)
    for k in range(K + 1):
        s += a[k].at0() * p
        p *= t0
    return s


def compute_pi(c, K, dps, ct0s=(60, 80, 100)):
    mp.mp.dps = dps
    t0s = time.time()
    a, b = build_a_b(c, K, dps)
    vals = {ct0: S(a, ct0 / mp.mpf(c), K) for ct0 in ct0s}
    approach_err = abs(vals[ct0s[-2]] - vals[ct0s[-1]])
    elapsed = time.time() - t0s
    return vals[ct0s[-1]], approach_err, elapsed


# (c, K, dps) -- K,dps chosen from g03's timing probes; the smaller c
# values need larger K/dps (order-2-entire cost wall, as diagnosed
# identically by both ancestor fronts).
JOBS = [
    (100, 1800, 300),
    (250, 800, 150),
    (640, 500, 100),
    (1000, 500, 100),
    (2560, 500, 100),
    (6400, 500, 100),
    (16000, 500, 100),
    (40960, 500, 100),
    (100000, 500, 100),
    (250000, 500, 100),
    (655360, 500, 100),
]

REFERENCE = {
    # from the record (already-vetted, referee-confirmed, leading digits
    # only -- used here ONLY as a sanity cross-check on my own fresh
    # numbers, not as an input to anything computed downstream)
    640: "0.0466626652057907264316848615295666243978",
    1000: "0.0377615983402126188243712025905770479904",
    2560: "0.0240217755876659764091477607960026096265",
    40960: "0.0061443932785551918066159319216308650218",
    655360: "0.0015451312096662308759993857963513008680",
    250: "0.0722226317815141619643797100974506988118877722234201774",
}


def main():
    results = {}
    for c, K, dps in JOBS:
        val, err, elapsed = compute_pi(c, K, dps)
        results[c] = {
            "Pi": mp.nstr(val, 40),
            "approach_err": mp.nstr(err, 4),
            "K": K,
            "dps": dps,
            "elapsed_s": round(elapsed, 1),
        }
        ref = REFERENCE.get(c)
        match = ""
        if ref is not None:
            refv = mp.mpf(ref)
            reldiff = abs(val - refv) / abs(refv)
            match = f"  [vs record: reldiff={mp.nstr(reldiff,4)}]"
        print(f"c={c:>8d}  Pi(c)={mp.nstr(val,32):40s} approach_err={mp.nstr(err,4):>10s} "
              f"K={K} dps={dps} t={elapsed:.1f}s{match}")

    with open("g04_grid_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved g04_grid_results.json")


if __name__ == "__main__":
    main()
