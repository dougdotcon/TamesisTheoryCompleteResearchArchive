"""
cross_checks.py -- confront the closed form of Theorem A with EVERY exact fact
this lineage has published, each derived by a completely different method.

Nothing here is fitted; every target was transcribed from a predecessor
document as a CROSS-CHECK TARGET only.
"""

from fractions import Fraction
import math
from core import Chain, _ff, _denom, phi_wallis

_C = {}


def stirling1u(N, M):
    if N < 0 or M < 0:
        return 0
    if N == 0:
        return 1 if M == 0 else 0
    if M == 0:
        return 0
    key = (N, M)
    v = _C.get(key)
    if v is None:
        v = (N - 1) * stirling1u(N - 1, M) + stirling1u(N - 1, M - 1)
        _C[key] = v
    return v


def A_j(r, j, b):
    if j < 0 or j > r:
        return Fraction(0)
    return Fraction(_ff(r, j, 0), _denom(j, 0, r, b))


def g_closed(m, b, r, n):
    tot = Fraction(0)
    P = 1
    for j in range(0, r + 1):
        tot += A_j(r, j, b) * Fraction(P, n ** j)
        P *= (m + j + 1)
    return tot


def h_closed(a, b, r, n):
    return Fraction(n - a + 1, n) * g_closed(n - a + 1, b + 1, r, n)


def psi(K, n):
    return g_closed(n, 0, K, n)


def coeff_closed(k, p, r, b):
    if k < 0 or k + p > r:
        return Fraction(0)
    return Fraction(stirling1u(k + p + 1, k + 1) * _ff(r, k, p),
                    _denom(k, p, r, b))


def Dstar(p, r, b):
    """Phi[p]_r(1,b) -- the sharp order-p residual constant."""
    return sum(coeff_closed(k, p, r, b) for k in range(0, r + 1))


ok = 0
fail = 0


def check(name, cond):
    global ok, fail
    if cond:
        ok += 1
        print("   [PASS] %s" % name)
    else:
        fail += 1
        print("   [FAIL] %s" % name)


print("=" * 78)
print("X1 -- the five PROVED exact psi_n^(K) closed forms (waves 5 / k3 / k6)")
print("=" * 78)


def poly(cs, n):
    """cs = [c_d,...,c_0] as a list high->low ; returns value"""
    v = 0
    for c in cs:
        v = v * n + c
    return v


targets = {
    1: (lambda n: Fraction(4 * n + 1, 6 * n), 2),
    2: (lambda n: Fraction(8 * n ** 2 + 4 * n + 1, 15 * n ** 2), 3),
    3: (lambda n: Fraction(poly([64, 48, 25, 6], n), 140 * n ** 3), 4),
    4: (lambda n: Fraction(poly([128, 128, 103, 52, 12], n), 315 * n ** 4), 5),
    5: (lambda n: Fraction(poly([1024, 1280, 1405, 1105, 538, 120], n),
                           2772 * n ** 5), 6),
}
for K, (f, n0) in targets.items():
    bad = sum(1 for n in range(n0, 40) if psi(K, n) != f(n))
    check("psi_n^(%d) for n=%d..39 (%d values)" % (K, n0, 40 - n0), bad == 0)

print()
print("=" * 78)
print("X2 -- psi_n^(3),R = h_2(0,0) (PROVED, k3_attempt_2 Sec.5)")
print("=" * 78)
bad = 0
for n in range(4, 40):
    want = (Fraction(11, 30) + Fraction(13, 20 * n) + Fraction(23, 60 * n ** 2)
            + Fraction(1, 10 * n ** 3))
    if h_closed(0, 0, 2, n) != want:
        bad += 1
check("h_2(0,0) = 11/30 + 13/(20n) + 23/(60n^2) + 1/(10n^3), n=4..39", bad == 0)

print()
print("=" * 78)
print("X3 -- the brute-force-confirmed value g_6(7,0) = 355081/823543")
print("      (wave-7 referee: exhaustive over 592,950,960 (pi,U) combinations)")
print("=" * 78)
check("g_closed(7,0,6,7) == 355081/823543",
      g_closed(7, 0, 6, 7) == Fraction(355081, 823543))
check("simulator agrees too", Chain(7).g_r(7, 0, 6) == Fraction(355081, 823543))

print()
print("=" * 78)
print("X4 -- the leading order: F_K(1,0) = varphi_K = 4^K (K!)^2/(2K+1)!")
print("      i.e. sum_{j=0}^{K} (K!)^2/((K-j)!(K+j+1)!) = varphi_K")
print("=" * 78)
bad = sum(1 for K in range(0, 40) if Dstar(0, K, 0) != phi_wallis(K))
check("K=0..39", bad == 0)

print()
print("=" * 78)
print("X5 -- Estagio 5/6 PROVED rate: lim n(psi_n^(K)-varphi_K) = K varphi_K/4")
print("      i.e. G_K(1,0) = K varphi_K / 4")
print("=" * 78)
bad = sum(1 for K in range(0, 40)
          if Dstar(1, K, 0) != Fraction(K, 4) * phi_wallis(K))
check("K=0..39", bad == 0)

print()
print("=" * 78)
print("X6 -- Estagio 8 PROVED Theorem 3: H_K(1,0) = K(3K+1)/32 varphi_K - K/12")
print("=" * 78)
bad = 0
for K in range(0, 90):
    want = Fraction(K * (3 * K + 1), 32) * phi_wallis(K) - Fraction(K, 12)
    if Dstar(2, K, 0) != want:
        bad += 1
check("K=0..89", bad == 0)
check("Estagio 8 tabulated D*_r(0): 0,0,1/15,5/28,103/315,1405/2772,"
      "1431/2002,2219/2340",
      [Dstar(2, r, 0) for r in range(0, 8)] ==
      [Fraction(0), Fraction(0), Fraction(1, 15), Fraction(5, 28),
       Fraction(103, 315), Fraction(1405, 2772), Fraction(1431, 2002),
       Fraction(2219, 2340)])

print()
print("=" * 78)
print("X7 -- Estagio 7 PROVED rate coefficient c_K = ((K+2)varphi_K - 2)/4")
print("      via the PROVED Reduction Lemma A relation")
print("      lim n(psi_n^(K)-varphi_K) uses F_{K-1}(1,1):")
print("      c_K = K[varphi_K/4 + F_{K-1}(1,1) - varphi_K]")
print("=" * 78)
bad = 0
for K in range(1, 30):
    FK1 = sum(A_j(K - 1, j, 1) for j in range(0, K))     # F_{K-1}(1,1)
    lhs = K * (Fraction(1, 4) * phi_wallis(K) + FK1 - phi_wallis(K))
    rhs = Fraction((K + 2) * phi_wallis(K) - 2, 4)
    if lhs != rhs:
        bad += 1
check("K=1..29 : K[varphi_K/4 + F_{K-1}(1,1) - varphi_K] == ((K+2)phi_K-2)/4",
      bad == 0)
check("c_1 = 0 and c_2 = 1/30 and c_3 = 1/14 exactly",
      Fraction(3 * phi_wallis(1) - 2, 4) == 0
      and Fraction(4 * phi_wallis(2) - 2, 4) == Fraction(1, 30)
      and Fraction(5 * phi_wallis(3) - 2, 4) == Fraction(1, 14))
check("c_6 = 1093/6006 (confirmed by 5 independent methods in this archive)",
      Fraction(8 * phi_wallis(6) - 2, 4) == Fraction(1093, 6006))

print()
print("=" * 78)
print("X8 -- Estagio 8 Theorem 3': the referee's exact general-b constant,")
print("      re-derived independently here as Phi[2]_r(1,b), spot values")
print("      (target document Sec.5.2 table, mpmath dps 60)")
print("=" * 78)
tab = {(10, 0): 1.78481, (10, 1): 1.19694, (10, 2): 0.83037, (10, 3): 0.59313,
       (100, 0): 74.7164, (100, 1): 64.7476, (100, 2): 56.2739,
       (100, 3): 49.0490}
bad = 0
for (r, b), want in sorted(tab.items()):
    got = float(Dstar(2, r, b))
    if abs(got - want) > 6e-5 * max(1.0, abs(want)):
        bad += 1
        print("      r=%d b=%d : got %.6f want %.6f" % (r, b, got, want))
check("8 tabulated D*_r(b) values reproduced to the printed precision",
      bad == 0)

print()
print("=" * 78)
print("X9 -- exhaustive agreement with the from-scratch exact simulator")
print("      (the transition rules implemented verbatim), LARGE sweep")
print("=" * 78)
checks = 0
bad = 0
for n in range(2, 34):
    ch = Chain(n)
    for r in range(0, min(n, 11)):
        for b in range(0, min(n - r, 9)):
            for m in range(b + r + 1, n + 1):
                if (n - m) + b + r >= n:
                    continue
                checks += 1
                if ch.g_r(m, b, r) != g_closed(m, b, r, n):
                    bad += 1
            for a in range(0, n - b - r):
                checks += 1
                if ch.h_r(a, b, r) != h_closed(a, b, r, n):
                    bad += 1
check("%d exact (g and h) checks, n<=33, r<=10, b<=8" % checks, bad == 0)

print()
print("=" * 78)
print("SUMMARY:  %d passed, %d failed" % (ok, fail))
print("=" * 78)
