"""
ADVERSARIAL REFEREE: the b>=1 question in detail.

The target's Sec.6.3 item 3 / scorecard row 13 asserts the NEGATIVE claim that
fitting a {r^q phi_r} u {r^q} basis to D*^(p)_r(b) at b = 1, 2, 3 FAILS out of
sample ("54-56 failures out of 61 tested r", "at p=2 as well as p=3").

My PART K found 0/61 failures at b=1.  This script pins that down.
"""
from fractions import Fraction as F
from math import factorial
import sympy as sp
from ref_sim import A
from ref_ladder import c1

r_s = sp.Symbol('r')


def phi(r):
    return F(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


def Dstar(p, r, b=0):
    return sum(A(r, j, b) * F(c1(j + 1, j + 1 - p)) for j in range(p, r + 1))


def fit_and_test(p, b, deg_phi, deg_pol, rmax_test=200, verbose=True):
    """fit c = sum_{q<=deg_phi} A_q r^q phi_r + sum_{q<=deg_pol} B_q r^q"""
    nb1, nb2 = deg_phi + 1, deg_pol + 1
    Ac = sp.symbols(f'a0:{nb1}')
    Bc = sp.symbols(f'b0:{nb2}') if nb2 > 0 else ()
    npts = nb1 + nb2
    fitpts = list(range(0, npts))
    eqs = []
    for rr in fitpts:
        pr = sp.Rational(phi(rr).numerator, phi(rr).denominator)
        d = Dstar(p, rr, b)
        eqs.append(sp.Eq(sum(Ac[q] * rr ** q * pr for q in range(nb1)) +
                         sum(Bc[q] * rr ** q for q in range(nb2)),
                         sp.Rational(d.numerator, d.denominator)))
    sol = sp.solve(eqs, list(Ac) + list(Bc), dict=True)
    if not sol:
        return None, None, None, None
    sol = sol[0]
    fp = sp.expand(sum(sol[Ac[q]] * r_s ** q for q in range(nb1)))
    fq = sp.expand(sum(sol[Bc[q]] * r_s ** q for q in range(nb2))) if nb2 else sp.Integer(0)
    bad = tested = 0
    for rr in range(npts, rmax_test + 1):
        v1 = sp.Rational(fp.subs(r_s, rr))
        v2 = sp.Rational(fq.subs(r_s, rr))
        pred = F(v1.p, v1.q) * phi(rr) + F(v2.p, v2.q)
        tested += 1
        if pred != Dstar(p, rr, b):
            bad += 1
    return fp, fq, bad, tested


print("=" * 78)
print("The b>=1 fit, done carefully.  Basis sizes chosen to MATCH the b=0 shape:")
print("  at b=0, D*^(p) = (degree-p poly in r)*phi_r + (degree-(p-1) poly in r)")
print("=" * 78)
for p in [0, 1, 2, 3, 4]:
    for b in [0, 1, 2, 3, 4]:
        fp, fq, bad, tested = fit_and_test(p, b, p, p - 1)
        if fp is None:
            print(f"  p={p} b={b}: singular fit")
            continue
        verdict = "EXACT (basis WORKS)" if bad == 0 else f"{bad}/{tested} out-of-sample FAILURES"
        print(f"  p={p} b={b}: {verdict}")
        if bad == 0:
            print(f"        D*^({p})_r({b}) = [{sp.factor(fp)}] phi_r + [{sp.factor(fq)}]")

print()
print("=" * 78)
print("Does a LARGER basis rescue b>=2?  (allow the phi-part degree to grow)")
print("=" * 78)
for p in [2, 3]:
    for b in [2, 3]:
        found = False
        for dphi in range(p, p + 7):
            for dpol in range(p - 1, p + 6):
                fp, fq, bad, tested = fit_and_test(p, b, dphi, dpol, rmax_test=120)
                if fp is not None and bad == 0:
                    print(f"  p={p} b={b}: SUCCEEDS with deg_phi={dphi}, deg_pol={dpol}")
                    print(f"        D* = [{sp.factor(sp.nsimplify(fp))}] phi_r + [{sp.factor(fq)}]")
                    found = True
                    break
            if found:
                break
        if not found:
            print(f"  p={p} b={b}: NO fit in this basis up to deg_phi<={p+6}, deg_pol<={p+5}"
                  f"   -> the target's negative claim HOLDS here")

print()
print("=" * 78)
print("Structural explanation attempt: is D*^(0)_r(b) itself in the basis?")
print("=" * 78)
for b in range(0, 6):
    vals = [Dstar(0, rr, b) for rr in range(0, 12)]
    ratios = [sp.nsimplify(sp.Rational(v.numerator, v.denominator) /
                           sp.Rational(phi(rr).numerator, phi(rr).denominator))
              for rr, v in enumerate(vals)]
    print(f"  b={b}: D*^(0)_r(b)/phi_r for r=0..11 = {[str(x) for x in ratios[:8]]}")
