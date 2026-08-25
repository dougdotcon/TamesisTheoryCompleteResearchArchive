#!/usr/bin/env python3
"""
r05_identify.py -- wave 17 front (d) PLATEAU-RESUMMATION-ATTEMPT

Inverse-symbolic HYPOTHESIS GENERATION (mpmath.identify / PSLQ) on
  (i)  the plateau constants Pi(c) at the >=100-digit c values, and
  (ii) the eps-expansion coefficients d1, d2, ... extracted by r04,
plus cross-c EXCLUSION tests of simple closed-form families.

DISCIPLINE (per mandate): nothing found here is a result. Every hit is a
candidate that must then be proved or reported as "unproven candidate
matching to N digits"; every miss is an exclusion "to the stated precision
over the stated basis/coefficient bounds".

Deterministic; no randomness.
"""

import json
from mpmath import (mp, mpf, mpmathify, sqrt, pi, e, log, exp, erfc, fabs,
                    log10, nstr, identify, pslq)

mp.dps = 120


def load_values(min_digits=95):
    best = {}
    for fn in ('r03_plateau_values_ladder.json',
               'r03_plateau_values_fixmid.json',
               'r03_plateau_values_c100deep.json',
               'r03_plateau_values_c40deep.json',
               'r03_plateau_values_c10mid.json',
               'r03_plateau_values_control.json'):
        try:
            with open(fn) as f:
                for r in json.load(f):
                    sd = r.get('stable_digits', 0)
                    c = r['c']
                    if not isinstance(c, int):
                        continue
                    if 'plateau' in r and sd >= min_digits and \
                            sd > best.get(c, (None, -1))[1]:
                        best[c] = (mpmathify(r['plateau']), sd)
        except FileNotFoundError:
            pass
    return {c: v[0] for c, v in best.items()}


def erfcx(x):
    return exp(x * x) * erfc(x)


def try_identify(x, digits, label, bases):
    """identify at a precision matched to the trusted digits"""
    old = mp.dps
    mp.dps = max(15, digits - 2)
    try:
        xx = +x
        hit = identify(xx, bases)
    finally:
        mp.dps = old
    print(f"  identify[{label}] (at {digits} digits, bases={bases}):"
          f" {hit if hit else 'NO MATCH'}")
    return hit


def try_pslq(vec, names, label, digits, maxcoeff=10**6):
    old = mp.dps
    mp.dps = max(15, digits - 2)
    try:
        v = [+x for x in vec]
        rel = pslq(v, maxcoeff=maxcoeff, maxsteps=100000)
    finally:
        mp.dps = old
    if rel:
        expr = " + ".join(f"{r}*{n}" for r, n in zip(rel, names) if r)
        resid = sum(r * x for r, x in zip(rel, vec))
        print(f"  pslq[{label}]: {expr} = 0   (residual {nstr(resid, 3)},"
              f" maxcoeff<={maxcoeff})")
    else:
        print(f"  pslq[{label}]: NO RELATION (maxcoeff<={maxcoeff},"
              f" {digits} digits)")
    return rel


def main():
    vals = load_values()
    print("=" * 72)
    print("(i) full-constant identification attempts (hypothesis generation)")
    print("=" * 72)
    for c in sorted(vals):
        if c not in (10, 100, 250, 1000):
            continue
        P = vals[c]
        cc = mpf(c)
        digs = 100
        print(f"c={c}:  Pi = {nstr(P, 30)}...")
        try_identify(P, digs, f"Pi({c})",
                     ['sqrt(2)', 'sqrt(pi)', 'pi', 'log(2)', 'exp(1)'])
        try_identify(P * sqrt(2 * cc / pi), digs, f"Pi({c})*sqrt(2c/pi)",
                     ['sqrt(2)', 'sqrt(pi)', 'pi', 'log(2)', 'exp(1)'])
        # erfcx-family bases at the natural special points of this problem
        E1 = erfcx(sqrt(cc / 2))          # E(s=1)
        Ehalf = erfcx(sqrt(cc / 8))       # E(s=1/2)
        rtc = sqrt(pi * cc / 2)
        try_pslq([P, mpf(1), E1, rtc * E1, 1 / rtc, mpf(1) / cc, Ehalf],
                 ['Pi', '1', 'E(1)', 'rt*E(1)', '1/rt', '1/c', 'E(1/2)'],
                 f"Pi({c}) vs erfcx family", digs, maxcoeff=10**4)
        # log-space: Pi = A * c^p * e^{qc} test -> ln Pi vs {1, ln c, c}
        try_pslq([log(P), mpf(1), log(cc), cc, log(pi)],
                 ['ln Pi', '1', 'ln c', 'c', 'ln pi'],
                 f"ln Pi({c})", digs, maxcoeff=10**3)
        print()

    print("=" * 72)
    print("(ii) eps-expansion coefficients d1, d2, ... (from r04)")
    print("=" * 72)
    try:
        with open('r04_fit_results.json') as f:
            fit = json.load(f)
    except FileNotFoundError:
        print("r04 results not present yet")
        return
    dco = [mpmathify(s) for s in fit['d_coeffs']]
    # trusted digits per coefficient, conservative (from r04 stability print)
    trusted = fit.get('trusted_digits', [40, 25, 18, 14, 10, 8])
    for j in range(1, min(6, len(dco))):
        dj = dco[j]
        digs = trusted[j] if j < len(trusted) else 8
        print(f"d{j} = {nstr(dj, min(30, digs + 2))}   (~{digs} digits)")
        if digs < 6:
            print("   too few digits; skipping identification")
            continue
        try_identify(dj, digs, f"d{j}",
                     ['sqrt(2)', 'sqrt(pi)', 'pi', 'log(2)'])
        # linear combos over a small named basis
        base = [mpf(1), sqrt(2 / pi), log(mpf(2)), sqrt(pi / 2), pi,
                1 / pi, sqrt(mpf(2)), log(pi)]
        names = ['1', 'sqrt(2/pi)', 'ln2', 'sqrt(pi/2)', 'pi', '1/pi',
                 'sqrt(2)', 'ln(pi)']
        try_pslq([dj] + base, [f'd{j}'] + names, f"d{j} linear", digs,
                 maxcoeff=200)
        print()

    print("=" * 72)
    print("(iii) cross-c EXCLUSION tests of simple closed-form families")
    print("=" * 72)
    # family A: Pi = alpha/sqrt(c) + beta/c  (solve on 2 c's, test on others)
    need = [1000, 40960, 655360, 10]
    if all(c in vals for c in need):
        c1, c2 = mpf(1000), mpf(40960)
        # solve
        a11, a12 = 1 / sqrt(c1), 1 / c1
        a21, a22 = 1 / sqrt(c2), 1 / c2
        det = a11 * a22 - a12 * a21
        al = (vals[1000] * a22 - vals[40960] * a12) / det
        be = (a11 * vals[40960] - a21 * vals[1000]) / det
        for ctest in (655360, 10):
            pred = al / sqrt(mpf(ctest)) + be / mpf(ctest)
            got = vals[ctest]
            print(f"  family Pi=a/sqrt(c)+b/c (fit@1000,40960):"
                  f" test c={ctest}: rel.mismatch = "
                  f"{nstr(fabs(pred - got) / got, 4)}  -> "
                  f"{'EXCLUDED' if fabs(pred-got)/got > mpf('1e-90') else 'consistent'}")
    # family B: 3-term expansion exactly terminating
    need = [1000, 40960, 655360, 2560]
    if all(c in vals for c in need):
        import itertools
        cs = [mpf(1000), mpf(40960), mpf(655360)]
        from mpmath import matrix, lu_solve
        A = matrix(3, 3)
        b = matrix(3, 1)
        for i, cc in enumerate(cs):
            A[i, 0], A[i, 1], A[i, 2] = 1 / sqrt(cc), 1 / cc, cc ** mpf('-1.5')
            b[i] = vals[int(cc)]
        sol = lu_solve(A, b)
        cc = mpf(2560)
        pred = sol[0] / sqrt(cc) + sol[1] / cc + sol[2] * cc ** mpf('-1.5')
        got = vals[2560]
        print(f"  family Pi=a/sqrt(c)+b/c+g/c^1.5 (fit@1000,40960,655360):"
              f" test c=2560: rel.mismatch = {nstr(fabs(pred-got)/got, 4)}"
              f"  -> {'EXCLUDED' if fabs(pred-got)/got > mpf('1e-80') else 'consistent'}")
    # family C: any function whose eps-expansion is even in eps
    # (e.g. rational in 1/c, or A*erfcx(l*sqrt(c)) up to 1/c-series): excluded
    # iff d1 != 0 -- report d1 with its stable digits (from r04).
    if 'd_coeffs' in fit:
        d1 = mpmathify(fit['d_coeffs'][1])
        print(f"  family 'even in eps' (rational in 1/c; A*erfcx(l sqrt(c));"
              f" ...): d1 = {nstr(d1, 12)} != 0 -> EXCLUDED")


if __name__ == '__main__':
    main()
