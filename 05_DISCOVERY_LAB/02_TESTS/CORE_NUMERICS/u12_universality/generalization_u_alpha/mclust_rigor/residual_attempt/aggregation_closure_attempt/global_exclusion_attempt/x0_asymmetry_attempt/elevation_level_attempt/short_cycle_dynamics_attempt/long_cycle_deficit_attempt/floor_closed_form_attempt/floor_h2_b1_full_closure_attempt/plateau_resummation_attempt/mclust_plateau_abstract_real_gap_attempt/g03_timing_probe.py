"""
g03_timing_probe.py -- find an efficient (K, dps) working point for
computing Pi(c) to ~25-35 stable digits (far more than needed to resolve
the eps^4/eps^5 residual terms at every c in the accessible c=640..655360
range, but cheap relative to the ancestor fronts' 110-121-digit target).

Method mirrors the record's own three-way error control (SS2.1 of both
ancestor documents), just recalibrated to a much smaller target precision:
approach error measured as |S(ct0=hi) - S(ct0=lo)| for two c*t0 values.
"""
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


def probe(c, K, dps, ct0_list):
    t0s = time.time()
    mp.mp.dps = dps
    a, b = build_a_b(c, K, dps)
    t_build = time.time() - t0s
    vals = {}
    for ct0 in ct0_list:
        t0 = mp.mpf(ct0) / c
        vals[ct0] = S(a, t0, K)
    t_total = time.time() - t0s
    return vals, t_build, t_total


if __name__ == "__main__":
    c = 1000
    for K, dps in [(300, 80), (500, 100), (700, 120)]:
        vals, t_build, t_total = probe(c, K, dps, [60, 80, 100])
        diffs = {f"{a}-{b}": abs(vals[a] - vals[b]) for a, b in [(80, 100), (60, 100)]}
        print(f"K={K} dps={dps}  t_build={t_build:.1f}s t_total={t_total:.1f}s")
        for ct0, v in vals.items():
            print(f"   S(ct0={ct0}) = {mp.nstr(v, 30)}")
        for k, dv in diffs.items():
            print(f"   |S({k})| diff = {mp.nstr(dv, 6)}")
        print(f"   reference (record, 121 digits): 0.0377615983402126188243712025905770479904")
        print()
