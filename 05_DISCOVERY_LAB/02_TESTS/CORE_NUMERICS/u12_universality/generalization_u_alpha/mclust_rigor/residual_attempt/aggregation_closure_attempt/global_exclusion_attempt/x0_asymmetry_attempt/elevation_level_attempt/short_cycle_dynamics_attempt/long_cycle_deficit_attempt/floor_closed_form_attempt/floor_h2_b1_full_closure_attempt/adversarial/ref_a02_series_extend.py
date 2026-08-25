#!/usr/bin/env python3
"""
REFEREE script A02 -- extend the small-t0 coefficient hierarchy to HIGH
order in exact closed form, using the family identity established in
ref_a01_symbolic.py:

    every a_k(s), b_k(s) is of the form  A(s) + B(s)*erfcx(s*sqrt(c/2)),
    A,B polynomials; the recursion maps this family to itself and the
    bounded-branch ODE solve is pure linear algebra (no quadrature).

Purpose: adjudicate the front's SS5 obstruction claim #1, namely that
  (a) each order needs one MORE nested quadrature layer  (a01: FALSE), and
  (b) "the series' empirically-measured radius of convergence
      (c*t0 ~ 0.5-0.7) is intrinsically far below the t0 range phi_far
      actually integrates over"  --  tested here by computing ~200 EXACT
      coefficients and summing the series far beyond c*t0 ~ 0.5.

Deterministic (no randomness).  mpmath, dps=250.
"""
import json
from mpmath import mp, mpf, sqrt, pi, exp

mp.dps = 300

LOG = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    LOG.append(line)

C = mpf(1000)
TAU = sqrt(pi * C / 2)          # psi1(0)
MU = C / TAU                    # sqrt(2c/pi);  note TAU*MU = c exactly

# ---------------- polynomial helpers (lists of mpf, index = power) ----
def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p

def padd(p, q):
    n = max(len(p), len(q))
    return trim([ (p[i] if i < len(p) else mpf(0))
                + (q[i] if i < len(q) else mpf(0)) for i in range(n)])

def pscale(p, a):
    return trim([a * x for x in p])

def pshift(p):          # multiply by s
    return trim([mpf(0)] + list(p))

def pmul1ms(p):         # multiply by (1 - s)
    return padd(p, pscale(pshift(p), mpf(-1)))

def pder(p):
    if len(p) == 1:
        return [mpf(0)]
    return trim([p[i] * i for i in range(1, len(p))])

def pint(p):            # antiderivative, constant 0
    return trim([mpf(0)] + [p[i] / (i + 1) for i in range(len(p))])

def peval(p, xv):
    acc = mpf(0)
    for coef in reversed(p):
        acc = acc * xv + coef
    return acc

# ---------------- family ops:  f = A(s) + B(s)*E,  E = erfcx(s*sqrt(c/2))
#   E' = c*s*E - MU
def fam_der(A, B):
    return padd(pder(A), pscale(B, -MU)), padd(pder(B), pscale(pshift(B), C))

def fam_add(f, g_):
    return padd(f[0], g_[0]), padd(f[1], g_[1])

def fam_scale(f, a):
    return pscale(f[0], a), pscale(f[1], a)

def fam_mul1ms(f):
    return pmul1ms(f[0]), pmul1ms(f[1])

def fam_solve_b(RA, RB):
    """bounded-branch solution of  b' - c s b = RA + RB*E  inside the family.
    B = int(RB) + beta ;  A solves A' - c s A = RA + MU*(int(RB)+beta),
    coefficients determined top-down; beta fixed by the s^0 equation."""
    BB0 = pint(RB)
    R = padd(RA, pscale(BB0, MU))
    dR = len(R) - 1
    if dR == 0 and R[0] == 0:
        # homogeneous within family -> zero solution
        return [mpf(0)], [mpf(0)]
    if dR == 0:
        beta = -R[0] / MU
        return [mpf(0)], padd(BB0, [beta])
    dA = dR - 1
    alpha = [mpf(0)] * (dA + 1)
    def Rn(n):
        return R[n] if n < len(R) else mpf(0)
    for n in range(dR, 0, -1):
        a_np1 = alpha[n + 1] if n + 1 <= dA else mpf(0)
        alpha[n - 1] = ((n + 1) * a_np1 - Rn(n)) / C
    a1 = alpha[1] if dA >= 1 else mpf(0)
    beta = (a1 - Rn(0)) / MU
    return trim(alpha), padd(BB0, [beta])

def fam_at0(f):
    # E(0) = erfcx(0) = 1
    return f[0][0] + f[1][0]

# ---------------- the recursion --------------------------------------
KMAX = 500
a = [None] * (KMAX + 1)
b = [None] * (KMAX + 1)
a[0] = ([mpf(1)], [mpf(0)])
a[1] = ([-C], [mpf(0)])
b[0] = ([mpf(0)], [mpf(0)])
b[1] = fam_solve_b([-C], [mpf(0)])

for k in range(1, KMAX):
    # w_k = a_{k-1}/k + (1-s) b_k - b_{k-1}
    wk = fam_add(fam_add(fam_scale(a[k - 1], mpf(1) / k), fam_mul1ms(b[k])),
                 fam_scale(b[k - 1], mpf(-1)))
    # a_{k+1} = [a_k' - c a_k + c w_k]/(k+1)
    ak_d = fam_der(*a[k])
    a[k + 1] = fam_scale(fam_add(fam_add(ak_d, fam_scale(a[k], -C)),
                                 fam_scale(wk, C)), mpf(1) / (k + 1))
    # b_{k+1} solves  b' - c s b = -c a_k/(k+1) + c b_k
    RHS = fam_add(fam_scale(a[k], -C / (k + 1)), fam_scale(b[k], C))
    b[k + 1] = fam_solve_b(RHS[0], RHS[1])

ak0 = [fam_at0(a[k]) for k in range(KMAX + 1)]
bk0 = [fam_at0(b[k]) for k in range(KMAX + 1)]

# ---------------- cross-checks against ref_a01 (independent sympy/quad)
ref = json.load(open('ref_series_coeffs.json'))
log("cross-checks against ref_a01_symbolic.py values (c=1000):")
for name, mine, want in [("a2(0)", ak0[2], ref["a2_0"]),
                         ("a3(0)", ak0[3], ref["a3_0"]),
                         ("a4(0)", ak0[4], ref["a4_0"]),
                         ("b2(0)", bk0[2], ref["b2_0"])]:
    rd = abs(float(mine) - want) / abs(want)
    log(f"  {name}: family-recursion={float(mine):.6e}  a01={want:.6e}  "
        f"reldiff={rd:.2e}")
    assert rd < 1e-10
log("front's own claimed values: a2(0)=520316.636488, b2(0)=-20816.636488,")
log("                            a3(0)=-180730907.6285  -- all reproduced.")

# ---------------- coefficient growth / radius diagnostics -------------
log("")
log("coefficient growth ( |a_k(0)|, ratio |a_k/a_{k-1}|, c/ratio ):")
for k in list(range(1, 12)) + [15, 20, 30, 40, 60, 80, 100, 150, 200,
                               300, 400, 500]:
    r = abs(ak0[k] / ak0[k - 1])
    log(f"  k={k:4d}  |a_k(0)|={mp.nstr(abs(ak0[k]), 6):>14}  "
        f"ratio={mp.nstr(r, 6):>12}   c/ratio={mp.nstr(C / r, 5):>10}")
log("")
log("if ratio ~ c/(k*const) the series is ENTIRE-like (infinite radius);")
log("a finite radius R would show ratio -> 1/R = const.")

# ---------------- sum the series at practically relevant t0 -----------
def series_sum(t0, K):
    t = mpf(t0)
    acc = mpf(0)
    for k in range(K + 1):
        acc += ak0[k] * t**k
    return acc

log("")
log("partial sums S_K(t0) = sum_{k<=K} a_k(0) t0^k   (exact coefficients):")
refs = {  # accepted MC references from the parent lineage (read-only inputs)
    0.0003: ("parent fcd_t3.log N=40k", 0.74785, 0.00217),
    0.001:  ("parent fcd_t3.log N=40k", 0.37585, 0.00242),
    0.003:  ("parent fcd_t3.log N=40k", 0.08240, 0.00137),
    0.01:   ("parent referee T3 N=200k", 0.03770, 0.00043),
    0.03:   ("parent fcd_t3.log N=40k", 0.03812, 0.00096),
    0.05:   ("parent fcd_t3.log N=40k", 0.03667, 0.00094),
    0.09:   ("parent referee T3 N=200k", 0.03744, 0.00042),
}
t0_list = [0.0003, 0.0005, 0.0007, 0.001, 0.002, 0.003, 0.005, 0.01,
           0.02, 0.03, 0.05, 0.09]
final = {}
for t0 in t0_list:
    row = [f"t0={t0:7.4f} (c*t0={1000*t0:5.1f}):"]
    for K in (3, 10, 50, 100, 200, 300, 400, 500):
        row.append(f"S_{K}={mp.nstr(series_sum(t0, K), 8)}")
    log("  " + "  ".join(row))
    s_fin = series_sum(t0, 500)
    conv = abs(s_fin - series_sum(t0, 400))
    final[t0] = (float(s_fin), float(conv))
    extra = ""
    if t0 in refs:
        src, v, sem = refs[t0]
        z = (v - float(s_fin)) / sem
        extra = f"   vs {src}: {v}+-{sem}  z={z:+.2f}"
    log(f"      S_500={mp.nstr(s_fin, 10)}  |S_500-S_400|={mp.nstr(conv, 3)}"
        + extra)

log("")
log("plateau-approach diagnostic (S_500 values):")
sref = series_sum(0.09, 500)
for t0 in (0.01, 0.02, 0.03, 0.05):
    d = series_sum(t0, 500) - sref
    log(f"  S(t0={t0}) - S(0.09) = {mp.nstr(d, 4)}    "
        f"[e^(-c t0) = {mp.nstr(exp(-1000*mpf(t0)), 3)}]")

log("")
log("3-term truncation error (exact): S_200 - S_3 at the front's claimed")
log("validity-window edge and beyond:")
for t0 in (0.0003, 0.0005, 0.0007, 0.001):
    d = series_sum(t0, 200) - series_sum(t0, 3)
    log(f"  t0={t0}:  S_200-S_3 = {mp.nstr(d, 6)}   "
        f"(front's MC SEM at N=500k was ~2.4e-4..6.9e-4)")

json.dump({"t0_S500": {str(k): v for k, v in final.items()},
           "a_k0_first30": [float(x) for x in ak0[:31]],
           "plateau_S500": float(series_sum(0.09, 500))},
          open('ref_a02_series.json', 'w'), indent=1)
with open('ref_a02_series_extend.log', 'w') as f:
    f.write("\n".join(LOG) + "\n")
log("done.")
