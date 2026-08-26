#!/usr/bin/env python3
"""
r04_asymptotics_fit.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Tests the derived asymptotic law  Pi(c) = sqrt(pi/(2c)) * [1 + O(1/sqrt(c))]
against the >=100-digit plateau values (r03/r03b), and extracts the
coefficients of the conjectured expansion

    y(eps) := Pi(c) * sqrt(2c/pi) = d0 + d1*eps + d2*eps^2 + ...,
    eps := c^{-1/2},

from the geometric ladder c = 10*4^j (eps halving), by exact polynomial
interpolation (Vandermonde solve, mpmath) on nested subsets. Coefficient
uncertainty is estimated from the spread across subsets; d0 is CHECKED
against the derived value 1 (it is not imposed).

Deterministic; no randomness.
"""

import json
import sys
from mpmath import mp, mpf, mpmathify, sqrt, pi, fabs, log10, nstr, matrix, lu_solve

mp.dps = 130

LADDER = [40, 100, 160, 250, 640, 1000, 2560, 10240, 40960, 163840, 655360]
HOLDOUT = [250]          # lower-precision values: used as prediction tests only
# NOTE (honest, self-checked by this front on 2026-08-26): c=40,100,160,10,1
# direct-summation attempts by the predecessor instance never completed
# (empty logs / no result json) -- confirmed by this front to be a genuine
# cost wall, not a stray crash: the required K scales like the recursion's
# O(K^2) descending-solve cost times an O(dps) mpf-arithmetic cost, and K
# itself barely shrinks with a lower target-digit count (the "+1" term in
# the alpha-sizing formula dominates over the digit term at these c), so
# c=40 (K=16000,dps=1200) is estimated (by direct scaling off the c=1000
# ladder point's measured 163.5s at K=2000,dps=360) at roughly
# (16000/2000)^2 * (1200/360) ~= 64*3.3 ~= 213x -> ~9.7 HOURS wall time --
# correctly out of budget per the mandate's anti-stall instruction. c=250
# (46 stable digits, 736s) is the practical floor for this method; it is
# used below ONLY as a holdout consistency check, never as a fit input.
LOW_DIGIT_FLOOR = {250: 40}   # allow c=250 in even at only 40 stable digits


def load_values(min_digits=95):
    """best (highest stable_digits) entry per c across all result files"""
    best = {}
    for fn in ('r03_plateau_values_ladder.json',
               'r03_plateau_values_fixmid.json',
               'r03_plateau_values_c100deep.json',
               'r03_plateau_values_c40deep.json',
               'r03_plateau_values_c10mid.json',
               'r03_plateau_values_c1small.json',
               'r03_plateau_values_control.json'):
        try:
            with open(fn) as f:
                for r in json.load(f):
                    sd = r.get('stable_digits', 0)
                    c = r['c']
                    if not isinstance(c, int):
                        continue
                    thresh = LOW_DIGIT_FLOOR.get(c, min_digits)
                    if 'plateau' in r and sd >= thresh and \
                            sd > best.get(c, (None, None, -1))[2]:
                        best[c] = (mpmathify(r['plateau']), fn, sd)
        except FileNotFoundError:
            pass
    vals = {c: v[0] for c, v in best.items()}
    meta = {c: (v[1], v[2]) for c, v in best.items()}
    return vals, meta


def poly_fit(eps_list, y_list):
    n = len(eps_list)
    A = matrix(n, n)
    b = matrix(n, 1)
    for i in range(n):
        for j in range(n):
            A[i, j] = eps_list[i] ** j
        b[i] = y_list[i]
    return lu_solve(A, b)


def main():
    vals, meta = load_values()
    print("loaded plateau values:")
    for c in sorted(vals):
        print(f"  c={c:>7}  {nstr(vals[c], 30)}  from {meta[c][0]}"
              f" (stable_digits={meta[c][1]})")
    print()
    print("Pi(c)*sqrt(2c/pi)  [derived limit: 1]:")
    for c in sorted(vals):
        y = vals[c] * sqrt(2 * mpf(c) / pi)
        print(f"  c={c:>7}  y = {nstr(y, 25)}   y-1 = {nstr(y - 1, 8)}"
              f"   (y-1)*sqrt(c) = {nstr((y - 1) * sqrt(mpf(c)), 12)}")
    print()

    avail = [c for c in LADDER if c in vals and c not in HOLDOUT]
    if len(avail) < 5:
        print("not enough ladder points yet")
        return
    eps = [1 / sqrt(mpf(c)) for c in avail]
    ys = [vals[c] * sqrt(2 * mpf(c) / pi) for c in avail]

    # full fit and nested-subset fits for stability
    subsets = {
        'all': list(range(len(avail))),
        'drop_largest_eps': list(range(1, len(avail))),
        'drop_smallest_eps': list(range(len(avail) - 1)),
        'drop_both_ends': list(range(1, len(avail) - 1)),
    }
    fits = {}
    for name, idx in subsets.items():
        d = poly_fit([eps[i] for i in idx], [ys[i] for i in idx])
        fits[name] = d
        print(f"fit[{name}] over c={[avail[i] for i in idx]}:")
        for j in range(min(6, len(d))):
            print(f"    d{j} = {nstr(d[j], 30)}")
    print()
    # stable digits per coefficient = agreement between 'all' and the
    # most-different subset fit
    print("coefficient stability (agreement across subset fits):")
    dmain = fits['all']
    trusted = []
    for j in range(len(dmain)):
        others = [fabs(dmain[j] - fits[n][j])
                  for n in fits if n != 'all' and j < len(fits[n])]
        if not others:
            trusted.append(0)
            if j < 7:
                print(f"  d{j} = {nstr(dmain[j], 32)}   stable to ~0 digits"
                      f" (no cross-subset comparator at this order)")
            continue
        spread = max(others)
        digs = int(-log10(spread / max(fabs(dmain[j]), mpf('1e-30')))) \
            if spread > 0 else 99
        trusted.append(digs)
        if j < 7:
            print(f"  d{j} = {nstr(dmain[j], 32)}   stable to ~{digs} digits")
    print()

    # --- checks of the DERIVED asymptotic coefficients ---
    print("derived-coefficient checks:")
    print(f"  d0 - 1              = {nstr(dmain[0] - 1, 8)}"
          f"   [derived: 0]")
    u = sqrt(2 / pi)
    preds = [
        ('d0', mpf(1), 'derived'),
        ('d1', -2 * u, 'derived  [-2 sqrt(2/pi)]'),
        ('d2', mpf(7) / 2, 'derived  [7/2]'),
        ('d3', -mpf(34) / 3 * u, 'derived  [-(34/3) sqrt(2/pi)]'),
        ('d4', mpf(209) / 8, 'CONJECTURED (gamma-pattern) [209/8]'),
        ('d5', -mpf(1546) / 15 * u, 'CONJECTURED [-(1546/15) sqrt(2/pi)]'),
    ]
    for j, (name, pred, tag) in enumerate(preds):
        if j < len(dmain):
            print(f"  {name} - pred = {nstr(dmain[j] - pred, 8):>14}"
                  f"   pred = {nstr(pred, 22):>26}   {tag}")
    print()

    # --- holdout prediction tests at lower-precision c values ---
    for c in HOLDOUT:
        if c in vals:
            epsh = 1 / sqrt(mpf(c))
            yh = vals[c] * sqrt(2 * mpf(c) / pi)
            pred = sum(dmain[j] * epsh ** j for j in range(len(dmain)))
            print(f"  holdout c={c}: y_measured = {nstr(yh, 15)}  "
                  f"y_fit_extrapolated = {nstr(pred, 15)}  "
                  f"rel.diff = {nstr(fabs(pred - yh) / yh, 4)}")
    out = {
        'ladder_c': avail,
        'd_coeffs': [nstr(dmain[j], 40) for j in range(len(dmain))],
        'trusted_digits': trusted,
        'd0_minus_1': nstr(dmain[0] - 1, 10),
        'd1_minus_pred': nstr(dmain[1] - preds[1][1], 10) if len(dmain) > 1 else None,
        'd2_minus_pred': nstr(dmain[2] - preds[2][1], 10) if len(dmain) > 2 else None,
        'd3_minus_pred': nstr(dmain[3] - preds[3][1], 10) if len(dmain) > 3 else None,
    }
    with open('r04_fit_results.json', 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
