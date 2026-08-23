"""probe_uniform.py -- sup_{c in [0,C]} |phi(n,c) - phi_infty(c)|.

Question 1 of the brief: is the finite-n error bounded by a function of n
alone, uniformly over a fixed compact [0,C]?  And how does that bound grow
with C?

Predicted (ATTEMPT.md SS5):  n * sup_{[0,C]} |Delta_n| -> sup_{[0,C]} |e(c)|,
with e(c) = -c^2/12 + O(c^3) near 0 and e(c) ~ sqrt(pi c)/8 - 1/2 for large c.
So the answer should be: YES uniform on every [0,C], with the constant growing
like sqrt(C).

Grid note: Delta_n(c) ~ e(c)/n with e smooth and |e'| <= 1/8 everywhere on the
range scanned, so a grid of spacing dc misplaces n*sup by at most |e'| dc / 2;
the refinement pass below reduces that further.  (The a-priori Lipschitz-1
bound of SS3 is far more pessimistic than the actual O(1/n) variation.)
"""

import time
import numpy as np
import mpmath as mp
from chain_multi import phi_mixed_multi, default_rmax
from ecoef import e_of_c, phi_inf

mp.mp.dps = 30

_PICACHE = {}


def phi_inf_grid(cs):
    out = np.empty(len(cs))
    for i, c in enumerate(cs):
        k = round(float(c), 12)
        if k not in _PICACHE:
            _PICACHE[k] = float(phi_inf(c))
        out[i] = _PICACHE[k]
    return out


def sup_on(n, C, npts=161):
    cs = np.linspace(0.0, C, npts)
    r = default_rmax(C, n)
    v = phi_mixed_multi(n, cs, rmax=r)
    d = v - phi_inf_grid(cs)
    i = int(np.argmax(np.abs(d)))
    lo = cs[max(i - 1, 0)]
    hi = cs[min(i + 1, npts - 1)]
    if hi > lo:
        cs2 = np.linspace(lo, hi, 25)
        v2 = phi_mixed_multi(n, cs2, rmax=r)
        d2 = v2 - phi_inf_grid(cs2)
        j = int(np.argmax(np.abs(d2)))
        if abs(d2[j]) > abs(d[i]):
            return abs(d2[j]), cs2[j], d2[j]
    return abs(d[i]), cs[i], d[i]


def sup_e(C, npts=2001):
    cs = np.linspace(1e-9, C, npts)
    vals = [abs(float(e_of_c(c))) for c in cs]
    i = int(np.argmax(vals))
    return vals[i], cs[i]


BUDGET = 1.2e9          # n * npts * rmax element-ops per (n,C) cell


if __name__ == "__main__":
    print("=== probe_uniform.py : sup over compacts [0,C] ===")
    Cs = [1.0, 2.0, 5.0, 10.0, 25.0, 100.0, 400.0]
    ns = [200, 800, 3200, 12800, 51200]
    print()
    print("n * sup_{[0,C]} |phi(n,.) - phi_inf|      [argmax c in brackets]")
    print("  (cells left blank when n*npts*rmax exceeded the compute budget)")
    print()
    hdr = "     C   " + "".join("     n=%-15d" % n for n in ns) + "  sup|e| on [0,C]"
    print(hdr)
    rows = {}
    for C in Cs:
        row = "  %6.1f " % C
        for n in ns:
            if C > n or n * 161 * default_rmax(C, n) > BUDGET:
                row += "  %-21s" % ""
                continue
            t0 = time.time()
            s, cstar, signed = sup_on(n, C)
            rows[(C, n)] = (s, cstar, signed)
            row += "  %-9.6f [%7.3f]  " % (n * s, cstar)
        se, ce = sup_e(C)
        row += " %.6f [%7.3f]" % (se, ce)
        print(row, flush=True)

    print()
    print("--- signed sup: where is the max attained, and with what sign? ---")
    for C in Cs:
        cand = [n for n in ns if (C, n) in rows]
        if not cand:
            continue
        n = max(cand)
        s, cstar, signed = rows[(C, n)]
        se, ce = sup_e(C)
        print("  C=%-7.1f n=%-6d n*Delta = %+.6f at c=%.4f | e-pred %+.6f at c=%.4f"
              % (C, n, n * signed, cstar, float(e_of_c(ce)), ce))

    print()
    print("--- grid-resolution control (C=25, n=3200): npts 41/161/641 ---")
    for npts in (41, 161, 641):
        s, cstar, _ = sup_on(3200, 25.0, npts=npts)
        print("    npts=%-5d n*sup = %.8f at c=%.4f" % (npts, 3200 * s, cstar))

    print()
    print("--- explicit-bound sanity: |Delta_n(c)| <= (sqrt(c)+kappa_B)/n ? ---")
    f = lambda c: -(c ** 2) * mp.quad(lambda t: t ** 4 * mp.e ** (-c * t * t), [0, 1])
    cm = mp.findroot(lambda c: mp.diff(f, c), 5.0)
    kB = -f(cm)
    print("  kappa_B := sup_c c^2 I_2(c) = %s  attained at c = %s"
          % (mp.nstr(kB, 10), mp.nstr(cm, 8)))
    worst, where = 0.0, None
    for (C, n), (s, cstar, _) in rows.items():
        bound = (np.sqrt(cstar) + float(kB)) / n
        if s / bound > worst:
            worst, where = s / bound, (C, n, cstar)
    print("  max over the scan of |Delta_n(c*)| / [(sqrt(c*)+kappa_B)/n] = %.4f  at %s"
          % (worst, where))
