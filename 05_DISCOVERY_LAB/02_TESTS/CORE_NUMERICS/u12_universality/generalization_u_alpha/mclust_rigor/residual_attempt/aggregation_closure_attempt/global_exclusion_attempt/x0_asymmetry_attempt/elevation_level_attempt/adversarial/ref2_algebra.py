"""ref2_algebra.py -- independent symbolic/exact re-derivation of the algebra of
`elevation_level_attempt/ATTEMPT.md` sections 2, 3, 4, 5, 6.3.

Written from scratch by the adversarial referee (wave 10 front (a) review).
Nothing imported from the target's scripts.  sympy / mpmath / fractions only.

Run:  python3 ref2_algebra.py
"""
import sys
from fractions import Fraction

import sympy as sp
import mpmath as mp

mp.mp.dps = 50

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)


# ----------------------------------------------------------------------------
# 0.  symbols
# ----------------------------------------------------------------------------
t, s, u, c, n, b, rho, A, P, delta, eps = sp.symbols(
    "t s u c n b rho A P delta eps", positive=True)

say("=" * 78)
say("ref2_algebra.py  --  adversarial re-derivation of ATTEMPT.md algebra")
say("=" * 78)

# ----------------------------------------------------------------------------
# 1.  Section 2 -- the exposure densities (2.1) and (2.2), symbolically
#     P(y in U_rem) = (1-c/n)^(b-1)   ;   P(y in R cap U_rem) = (c/n)(1-c/n)^(b-1)
#     and the identity (1-c/n)^(b-1) = (1-rho)/(1-c/n) with rho = 1-(1-c/n)^b.
# ----------------------------------------------------------------------------
say("")
say("## 1. Section 2 densities -- symbolic identity check")
p = sp.Symbol("p", positive=True)          # p = c/n
rho_expr = 1 - (1 - p) ** b
lhs = (1 - p) ** (b - 1)
rhs = (1 - rho_expr) / (1 - p)
say("   (1-c/n)^(b-1) - (1-rho)/(1-c/n)  simplifies to:",
    sp.simplify(sp.expand(lhs - rhs)))

# ----------------------------------------------------------------------------
# 2.  Section 4 -- the direct algebraic check.
#     hazard 1/(A-t), q_CLUST(s)=s/A, master H_q(t) = t - (1-t) INT_0^t (1-q)/(1-s) ds
#     BUT with the elevated pool the (1-s) in the denominator is replaced by (A-s).
# ----------------------------------------------------------------------------
say("")
say("## 2. Section 4 direct algebraic check  H(t) = t^2/A")
q = s / A
integrand = (1 - q) / (A - s)
say("   (1-q(s))/(A-s) simplifies to:", sp.simplify(integrand))
I = sp.integrate(sp.simplify(integrand), (s, 0, t))
H = sp.simplify(t - (A - t) * I)
say("   H(t) = t - (A-t)*Int  =", sp.simplify(H), "   (expect t**2/A)")
say("   difference from t^2/A:", sp.simplify(H - t**2 / A))

# the surviving-mass / phi_cond substitution
integrand2 = sp.Rational(1, 1) / (A - t) * ((A - t) / A) * sp.exp(-c * t**2 / A)
say("   integrand of phi_cond:", sp.simplify(integrand2))
phi_cond = sp.integrate(integrand2, (t, 0, A))
sub = sp.integrate(sp.exp(-c * A * u**2), (u, 0, 1))
say("   Int_0^A ... dt  - Int_0^1 exp(-cA u^2) du  =",
    sp.simplify(sp.expand(phi_cond - sub)))

# ----------------------------------------------------------------------------
# 3.  Section 6.3 -- the O(c/n) chain-mass correction.
#     q(u) = u(1 + delta(1-u)) ; check (1-q)/(1-u) = 1 - delta*u ;
#     check H_delta(u) = u^2 + (delta/2) u^2 (1-u).
# ----------------------------------------------------------------------------
say("")
say("## 3. Section 6.3  --  delta correction")
qd = u * (1 + delta * (1 - u))
say("   (1-q_delta(u))/(1-u) =", sp.simplify((1 - qd) / (1 - u)),
    "   (expect 1 - delta*u)")
Id = sp.integrate(sp.simplify((1 - qd) / (1 - u)), (u, 0, t))
Hd = sp.simplify(t - (1 - t) * Id)
say("   H_delta(t) =", sp.expand(Hd))
say("   H_delta - [t^2 + (delta/2) t^2 (1-t)] =",
    sp.simplify(sp.expand(Hd - (t**2 + delta / 2 * t**2 * (1 - t)))))

# ----------------------------------------------------------------------------
# 4.  Closed forms used by phi_RED:  phi_U and T_U
# ----------------------------------------------------------------------------
say("")
say("## 4. closed forms phi_U(c) and T_U(c)")
cc = sp.Symbol("cp", positive=True)
phiU_sym = sp.integrate(sp.exp(-cc * u**2), (u, 0, 1))
say("   phi_U(c') =", sp.simplify(phiU_sym))
TU_sym = sp.integrate((1 - u) * sp.exp(-cc * u**2), (u, 0, 1))
say("   T_U(c')   =", sp.simplify(TU_sym))
say("   T_U - [phi_U - (1-exp(-c'))/(2c')] =",
    sp.simplify(sp.expand(TU_sym - (phiU_sym - (1 - sp.exp(-cc)) / (2 * cc)))))


# ----------------------------------------------------------------------------
# 5.  high-precision numerical implementations (mpmath), independent of target
# ----------------------------------------------------------------------------
def phiU(cp):
    cp = mp.mpf(cp)
    if cp == 0:
        return mp.mpf(1)
    return mp.sqrt(mp.pi) / (2 * mp.sqrt(cp)) * mp.erf(mp.sqrt(cp))


def TU(cp):
    cp = mp.mpf(cp)
    return phiU(cp) - (1 - mp.e**(-cp)) / (2 * cp)


def phiU_quad(cp):
    return mp.quad(lambda x: mp.e**(-mp.mpf(cp) * x * x), [0, 1])


def TU_quad(cp):
    return mp.quad(lambda x: (1 - x) * mp.e**(-mp.mpf(cp) * x * x), [0, 1])


say("")
say("## 5. closed form vs quadrature (mpmath, 50 dps)")
for cp in [0.5, 5.0, 29.47, 216.84, 1000.0]:
    say("   c'=%10.4f  |phiU_cf-quad|=%.3e  |TU_cf-quad|=%.3e"
        % (cp, abs(phiU(cp) - phiU_quad(cp)), abs(TU(cp) - TU_quad(cp))))


# ----------------------------------------------------------------------------
# 6.  phi_RED as stated in (5.1) -- rebuilt by me from the decomposition
# ----------------------------------------------------------------------------
def rho_of(bb, cv, nv):
    return 1 - (1 - mp.mpf(cv) / nv) ** bb


def phi_RED(bb, cv, nv):
    """(5.1) exactly as stated: c' = c(1-rho)."""
    r = rho_of(bb, cv, nv)
    cp = mp.mpf(cv) * (1 - r)
    rs = (mp.mpf(cv) / nv) * (1 - r)              # rho_start
    epsR = (rs / r) * TU(cp) + (1 + cp * TU(cp)) / ((1 - r) * nv)
    return (1 - r) * phiU(cp) + r * epsR


def phi_RED_expand(bb, cv, nv):
    """the second, 'expanded' form printed in (5.1)."""
    r = rho_of(bb, cv, nv)
    cp = mp.mpf(cv) * (1 - r)
    return ((1 - r) * (phiU(cp) + (mp.mpf(cv) / nv) * TU(cp))
            + r * (1 + cp * TU(cp)) / ((1 - r) * nv))


say("")
say("## 6. phi_RED: the two printed forms of (5.1) agree?")
for (bb, cv, nv) in [(8, 10, 32768), (100, 400, 65536), (100, 600, 65536),
                     (800, 100, 65536), (100, 1000, 65536)]:
    a1, a2 = phi_RED(bb, cv, nv), phi_RED_expand(bb, cv, nv)
    say("   b=%4d c=%5d n=%6d  phi_RED=%.10f  |form1-form2|=%.3e"
        % (bb, cv, nv, a1, abs(a1 - a2)))

# ----------------------------------------------------------------------------
# 7.  rho -> 0 limit at fixed (b,c):  phi_RED -> phi_U(c)
# ----------------------------------------------------------------------------
say("")
say("## 7. n -> infinity at fixed (b,c):  phi_RED -> phi_U(c) ?")
for nv in [2**16, 2**20, 2**24, 2**28, 2**32]:
    v = phi_RED(100, 400, nv)
    say("   n=2^%2d  phi_RED=%.12f   phi_U(c)=%.12f   diff=%.3e"
        % (nv.bit_length() - 1, v, phiU(400), v - phiU(400)))

# ----------------------------------------------------------------------------
# 8.  THE REFEREE'S OWN MATCHING ANALYSIS OF THE REDUCTION (4.1)
#     Compare the three candidate conventions for (c', n') on exact
#     expected-count grounds:
#        world  |R^c|   = n(1-c/n)^b               = (1-rho) n
#        pool   |U_rem| = n(1-c/n)^(b-1)           = (1-rho)n/(1-c/n)
#        per-step reroute rate = c/n
#     M-U at (C, N):  world = N - C, pool = N, rate = C/N.
# ----------------------------------------------------------------------------
say("")
say("## 8. referee's matching analysis of the reduction (4.1)")
say("   M-CLUST(b) at (c,n) conditioned on x0 notin R:")
say("     world  |R^c|   = n(1-c/n)^b      pool |U_rem| = n(1-c/n)^(b-1)")
say("     reroute rate per normal step = |R cap U_rem|/|U_rem| = c/n  (exact)")
say("   M-U at (C,N): world = N-C, pool = N, rate = C/N")
say("")
hdr = ("   %-28s %14s %14s %14s" % ("convention", "world err", "pool err", "rate err"))
say(hdr)
for (bb, cv, nv) in [(50, 400, 65536), (100, 400, 65536), (100, 600, 65536),
                     (200, 150, 65536), (300, 150, 65536), (400, 100, 65536),
                     (100, 1000, 65536), (800, 100, 65536)]:
    pfrac = mp.mpf(cv) / nv
    r = rho_of(bb, cv, nv)
    world = nv * (1 - pfrac) ** bb
    pool = nv * (1 - pfrac) ** (bb - 1)
    say("   b=%d c=%d n=%d  rho=%.4f  world=%.2f pool=%.2f rate=%.6g"
        % (bb, cv, nv, r, world, pool, pfrac))
    conventions = {
        "(4.1) N=(1-rho)n,C=c(1-rho)": (mp.mpf(cv) * (1 - r), nv * (1 - r)),
        "alt  N=(1-rho)(n+c)":         (mp.mpf(cv) * (1 - r) * (1 + pfrac),
                                        nv * (1 - r) * (1 + pfrac)),
        "REF  N=n(1-c/n)^(b-1)":       (mp.mpf(cv) * (1 - pfrac) ** (bb - 1),
                                        nv * (1 - pfrac) ** (bb - 1)),
    }
    for name, (C, N) in conventions.items():
        say("      %-28s world %+10.4f  pool %+10.4f  rate %+.3e"
            % (name, (N - C) - world, N - pool, C / N - pfrac))

# ----------------------------------------------------------------------------
# 9.  size of the effect of the c' choice on phi
# ----------------------------------------------------------------------------
say("")
say("## 9. effect of c' -> c'' = c(1-c/n)^(b-1) on phi_U (relative)")
for (bb, cv, nv) in [(8, 40, 32768), (50, 400, 65536), (100, 400, 65536),
                     (100, 600, 65536), (300, 150, 65536), (400, 100, 65536),
                     (200, 600, 65536), (800, 100, 65536), (100, 1000, 65536),
                     (400, 300, 65536), (200, 800, 131072), (400, 400, 131072)]:
    pfrac = mp.mpf(cv) / nv
    r = rho_of(bb, cv, nv)
    cp = mp.mpf(cv) * (1 - r)
    cpp = mp.mpf(cv) * (1 - pfrac) ** (bb - 1)
    say("   b=%4d c=%5d n=%6d  c/n=%.5f  c'=%9.4f c''=%9.4f  "
        "dphi/phi=%+.4f%%"
        % (bb, cv, nv, pfrac, cp, cpp, 100 * (phiU(cpp) / phiU(cp) - 1)))

# ----------------------------------------------------------------------------
# 10. lambda(t): the derived elevation, and its P_lead / P_exact anchors
# ----------------------------------------------------------------------------
say("")
say("## 10. lambda(t) anchors")
for (bb, cv, nv) in [(100, 600, 65536), (400, 100, 65536), (8, 160, 65536)]:
    pfrac = mp.mpf(cv) / nv
    r = rho_of(bb, cv, nv)
    Apool = (1 - r) / (1 - pfrac)
    lam0 = 1 / Apool
    Pexact = (1 - pfrac) ** (-(bb - 1))
    Plead = 1 / (1 - r)
    say("   b=%4d c=%5d  lambda(0)=%.10f  P_exact=%.10f  diff=%.2e   "
        "P_lead=%.10f" % (bb, cv, lam0, Pexact, lam0 - Pexact, Plead))

# ----------------------------------------------------------------------------
# 11. d ln lambda / dt at 0
# ----------------------------------------------------------------------------
say("")
say("## 11. growth rate  d ln lambda/dt |_0")
lam = (1 - t) / (A - t)
dln = sp.simplify(sp.diff(sp.log(lam), t).subs(t, 0))
say("   d ln lambda/dt|0 =", sp.simplify(dln), " with A=1-rho ->",
    sp.simplify(dln.subs(A, 1 - rho)))

with open(__file__.replace(".py", ".log"), "w") as fh:
    fh.write("\n".join(OUT) + "\n")
print("\n[written]", __file__.replace(".py", ".log"))
