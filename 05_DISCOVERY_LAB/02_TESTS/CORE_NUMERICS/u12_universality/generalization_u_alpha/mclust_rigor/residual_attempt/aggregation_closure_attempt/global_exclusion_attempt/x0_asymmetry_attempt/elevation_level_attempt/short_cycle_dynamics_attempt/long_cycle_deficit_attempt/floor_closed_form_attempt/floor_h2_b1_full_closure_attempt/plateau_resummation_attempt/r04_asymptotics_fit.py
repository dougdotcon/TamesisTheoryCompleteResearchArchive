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
HOLDOUT = [1, 10]          # lower-precision values: used as prediction tests


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
                    if 'plateau' in r and sd >= min_digits and \
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

    avail = [c for c in LADDER if c in vals]
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
        spread = max(fabs(dmain[j] - fits[n][j])
                     for n in fits if n != 'all' and j < len(fits[n]))
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
    d1_pred = -2 * sqrt(2 / pi)
    print(f"  d1 - (-2*sqrt(2/pi)) = {nstr(dmain[1] - d1_pred, 8)}"
          f"   [derived prediction: d1 = -2 sqrt(2/pi) = {nstr(d1_pred, 20)}]")
    d2_pred = mpf(7) / 2
    print(f"  d2 - 7/2             = {nstr(dmain[2] - d2_pred, 8)}"
          f"   [derived prediction: d2 = 7/2]")
    print(f"  next (undetermined) coefficient: d3 = {nstr(dmain[3], 20)}")
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
        'd1_minus_pred': nstr(dmain[1] - d1_pred, 10),
    }
    with open('r04_fit_results.json', 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
