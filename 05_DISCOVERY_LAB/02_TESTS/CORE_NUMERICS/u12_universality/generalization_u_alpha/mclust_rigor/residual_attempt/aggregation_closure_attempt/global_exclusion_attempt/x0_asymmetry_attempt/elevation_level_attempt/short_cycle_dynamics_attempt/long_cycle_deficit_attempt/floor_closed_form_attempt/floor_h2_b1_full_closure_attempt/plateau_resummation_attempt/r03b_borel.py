#!/usr/bin/env python3
"""
r03b_borel.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Borel-Laplace evaluation of Phi(0,t0), for SMALL c where direct summation of
the exact series is infeasible (its partial-sum terms reach ~e^{(ct0)^2/2c}
before cancelling, so direct cost explodes as c decreases at fixed ct0).

Method. Phi(0,.) is entire (established: coefficient ratios decrease through
order 500, wave-16 referee; reconfirmed here by the r03 tail diagnostics), so
its Borel transform
    B(u) = sum_k a_k(0) u^k / k!
is entire and sub-exponential on the positive axis, and the Laplace-Borel
representation
    Phi(0,t0) = (1/t0) * int_0^inf e^{-u/t0} B(u) du
holds for every t0 > 0 (absolutely convergent; equality is the classical
Borel-sum identity for entire functions of exponential-type-zero growth on
rays -- here verified EMPIRICALLY at 4 c values against direct summation of
the same function values; see VALIDATION runs below).

Cost: B(u)'s partial-sum term peak is only ~e^{2 sqrt(c u)}, and the Laplace
integral needs u <~ 300*t0, so the WHOLE cost depends on c*t0 alone:
dps ~ 2*sqrt(300*ct0)*log10(e) + 115 + margin, K_a ~ 4*sqrt(300*ct0).
This makes >=100-digit plateau values affordable at c = 1, 10, 40.

Quadrature: B oscillates like ~cos(2 sqrt(cu) - pi/4) (J_0-type); panels are
taken between consecutive phase multiples of pi (u_j = (j pi)^2 / 4c), with
40-point Gauss-Legendre per panel (nodes/weights computed at working
precision by Newton iteration on P_40). B is evaluated ONCE per node and
reused for every t0 at the same c.

Deterministic; no randomness.

usage: python3 r03b_borel.py
"""

import json
import sys
import time
from mpmath import mp, mpf, fabs, log10, nstr, exp, pi, cos, factorial

sys.path.insert(0, '.')
from r01_family_series import FamilyRecursion

# (c, K_a, dps, [ct0 values], [validation t0 with expected source])
RUNS = [
    # deep tier (>=100 digits target) + cheap validation t0's
    (1,    1300, 460, [230, 260, 290], [30]),
    (10,   1300, 460, [230, 260, 290], [60]),
    (40,   1300, 460, [230, 260, 290], [120]),
    # validation-only tiers against direct-deep runs (r03 smallc/ladder)
    (100,  1300, 460, [], [230, 260, 290]),
    (1000, 1300, 460, [], [230, 260, 290]),
]

NGL = 40


def gl_nodes_weights(n):
    """Gauss-Legendre nodes/weights on [-1,1] at current precision."""
    nodes, weights = [], []
    for i in range(1, n // 2 + 1):
        x = cos(pi * (i - mpf(1) / 4) / (n + mpf(1) / 2))
        for _ in range(60):
            p0, p1 = mpf(1), x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x = x - dx
            if fabs(dx) < mpf(10) ** (-mp.dps + 8):
                break
        p0, p1 = mpf(1), x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        w = 2 / ((1 - x * x) * dp * dp)
        nodes.append(x)
        weights.append(w)
    # mirror (n even assumed)
    full_n = [-x for x in nodes] + list(reversed(nodes))
    full_w = list(weights) + list(reversed(weights))
    return full_n, full_w


def run_c(cval, K_a, dps, deep_ct0s, val_ct0s):
    mp.dps = dps
    t = time.time()
    fr = FamilyRecursion(cval)
    a0 = fr.run(K_a)['a0']
    bc = []
    f = mpf(1)
    for k, ak in enumerate(a0):
        if k > 0:
            f *= k
        bc.append(ak / f)
    bc_rev = list(reversed(bc))

    def B(u):
        acc = mp.zero
        for coeff in bc_rev:
            acc = acc * u + coeff
        return acc

    all_ct0 = sorted(set(deep_ct0s + val_ct0s))
    ct0_max = max(all_ct0)
    t0_max = mpf(ct0_max) / cval
    u_max = 300 * t0_max
    # phase panels u_j = (j pi)^2/(4c) up to u_max
    edges = [mpf(0)]
    j = 1
    while True:
        uj = (j * pi) ** 2 / (4 * cval)
        if uj >= u_max:
            break
        edges.append(uj)
        j += 1
    edges.append(u_max)
    xs, ws = gl_nodes_weights(NGL)
    nodes, weights, Bvals = [], [], []
    maxB = mp.zero
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        h = (b - a) / 2
        m = (a + b) / 2
        for x, w in zip(xs, ws):
            u = m + h * x
            bv = B(u)
            nodes.append(u)
            weights.append(w * h)
            Bvals.append(bv)
            if fabs(bv) > maxB:
                maxB = fabs(bv)
    res = {'c': cval, 'K_a': K_a, 'dps': dps, 'n_panels': len(edges) - 1,
           'u_max': float(u_max), 'max|B|': nstr(maxB, 8)}
    # tail-of-B truncation control: last Borel term at u_max
    last_term = fabs(bc[-1]) * u_max ** (len(bc) - 1)
    res['lastBterm_at_umax'] = float(log10(last_term)) if last_term > 0 else -1e9
    vals = {}
    for ct0 in all_ct0:
        t0 = mpf(ct0) / cval
        acc = mp.zero
        for u, w, bv in zip(nodes, weights, Bvals):
            acc += w * exp(-u / t0) * bv
        v = acc / t0
        vals[ct0] = v
        res[f'S_ct0_{ct0}'] = nstr(v, 130)
        # quadrature tail bound: e^{-u_max/t0} * max|B| * u_max
        tb = exp(-u_max / t0) * maxB * u_max
        res[f'tailbound_ct0_{ct0}'] = float(log10(tb)) if tb > 0 else -1e9
    if len(deep_ct0s) >= 2:
        d1, d2 = vals[deep_ct0s[-2]], vals[deep_ct0s[-1]]
        diff = fabs(d1 - d2)
        res['approach_last_two'] = nstr(diff, 5)
        rel = diff / fabs(d2) if d2 != 0 else mpf(1)
        res['stable_digits'] = int(-log10(rel)) if rel > 0 else dps
        res['plateau'] = nstr(vals[deep_ct0s[-1]], 120)
    res['runtime_s'] = round(time.time() - t, 1)
    return res


def main():
    results = []
    for (cval, K_a, dps, deep, val) in RUNS:
        r = run_c(cval, K_a, dps, deep, val)
        results.append(r)
        print(f"c={cval:>5}  K_a={K_a} dps={dps} panels={r['n_panels']}  "
              f"max|B|={r['max|B|']}  lastBterm~1e{r['lastBterm_at_umax']:.0f}"
              f"  ({r['runtime_s']}s)")
        for key in sorted(k for k in r if k.startswith('S_ct0')):
            print(f"   {key} = {r[key][:118]}")
        if 'plateau' in r:
            print(f"   stable_digits={r['stable_digits']}  "
                  f"|S_mid-S_hi|={r['approach_last_two']}")
        sys.stdout.flush()
        with open('r03b_borel_values.json', 'w') as f:
            json.dump(results, f, indent=1)


if __name__ == '__main__':
    main()
