"""
GAMMA-C-GAMMA-JOINT-SADDLE-ATTEMPT, script 01.

Purpose: independently re-derive and re-verify, from scratch (own code,
no ancestor .py imported or transcribed), the exact facts this front's
own analysis will be built on:

  (A) Lemma 1 (wave-17, PROVED): A_k(n,gamma) and S_n = sum_k A_k,
      from the primary combinatorial definition.
  (B) The double-sum-swap identity (Estagio 52 / route2_bypass Estagio
      54, PROVED):
        S_n'  := 1 + S_n(gamma) = sum_{m=0}^n (gamma^m/n^m) m! T(n,m)
        T(n,m):= sum_{j=0}^{n-m} C(j+m,m) C(n-j,m) (1-gamma)^j
  (C) The Beta-integral closed form for T(n,m), which the hostile
      referee of route2_bypass_attempt derived (Pfaff transform DLMF
      15.8.7 + Euler's integral) and verified to <5e-51 relative error:
        T(n,m) = C(n+m+1, 2m+1) * E_{t~Beta(m+1,m+1)}[ (1-gamma*t)^(n-m) ]
      This is THIS FRONT's recommended starting point per the mandate.
      Re-verified here independently, fresh code, before building
      anything further on it.

All exact arithmetic (Fraction / sympy Rational) or high-precision
mpmath (dps=50). No randomness anywhere in this script.
"""
import sympy as sp
import mpmath as mp
from fractions import Fraction as F
from math import comb, factorial

mp.mp.dps = 50

print("=" * 78)
print("(A) Lemma 1 from the primary definition: A_k, S_n, direct re-derivation")
print("=" * 78)

def A_k_direct(n, k, gamma):
    """A_k(n,gamma) = sum_{m=0}^k C(k,m) gamma^m (1-gamma)^(k-m) P_{k,m},
    P_{k,m} = prod_{i=1}^m (1 - (k-i)/n).  Exact Fraction arithmetic."""
    total = F(0)
    for m in range(0, k + 1):
        P = F(1)
        for i in range(1, m + 1):
            P *= (1 - F(k - i, n))
        total += comb(k, m) * (gamma ** m) * ((1 - gamma) ** (k - m)) * P
    return total

def S_n_direct(n, gamma):
    return sum(A_k_direct(n, k, gamma) for k in range(1, n + 1))

# spot check against brute force enumeration is out of scope here (already
# done by the wave-17 ultimate ancestor and re-derived by route2_bypass's
# own script 01); this front instead re-derives A_k from its OWN
# closed-form product formula and cross-checks against a second,
# independent evaluator using the explicit polynomial P_{k,m}=(n-k+1)_m/n^m.

def A_k_pochhammer(n, k, gamma):
    total = F(0)
    for m in range(0, k + 1):
        # (n-k+1)_m / n^m as a rising factorial ratio
        num = F(1)
        for i in range(m):
            num *= (n - k + 1 + i)
        P = num / (n ** m) if m > 0 else F(1)
        total += comb(k, m) * (gamma ** m) * ((1 - gamma) ** (k - m)) * P
    return total

mism = 0
checks = 0
for n in [3, 5, 8, 12]:
    for k in range(1, n + 1):
        for gnum, gden in [(1, 3), (2, 5), (1, 2), (3, 4)]:
            g = F(gnum, gden)
            a1 = A_k_direct(n, k, g)
            a2 = A_k_pochhammer(n, k, g)
            checks += 1
            if a1 != a2:
                mism += 1
                print(f"  MISMATCH A_k n={n} k={k} g={g}: {a1} vs {a2}")
print(f"A_k: two independent evaluators, {checks} checks, {mism} mismatches")
assert mism == 0

print()
print("=" * 78)
print("(B) The double-sum-swap identity S_n' = sum_m (g^m/n^m) m! T(n,m)")
print("=" * 78)

def T_nm_direct(n, m, gamma):
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - gamma) ** j)
    return total

def Sn_prime_via_swap(n, gamma):
    total = F(0)
    for m in range(0, n + 1):
        total += (gamma ** m) * factorial(m) * T_nm_direct(n, m, gamma) / (n ** m)
    return total

mism = 0
checks = 0
for n in [3, 5, 8, 12, 15]:
    for gnum, gden in [(1, 3), (2, 5), (1, 2), (3, 4)]:
        g = F(gnum, gden)
        lhs = 1 + S_n_direct(n, g)
        rhs = Sn_prime_via_swap(n, g)
        checks += 1
        if lhs != rhs:
            mism += 1
            print(f"  MISMATCH swap n={n} g={g}: {lhs} vs {rhs}")
print(f"Double-sum-swap identity: {checks} checks (fresh code), {mism} mismatches")
assert mism == 0

print()
print("=" * 78)
print("(C) The Beta-integral closed form for T(n,m), independently re-verified")
print("    T(n,m) = C(n+m+1,2m+1) * (1/B(m+1,m+1)) * Int_0^1 t^m(1-t)^m(1-g t)^(n-m) dt")
print("=" * 78)

def T_beta_integral(n, m, gamma_mp):
    Cnorm = mp.binomial(n + m + 1, 2 * m + 1)
    beta_pref = mp.factorial(2 * m + 1) / (mp.factorial(m) ** 2)  # = 1/B(m+1,m+1)
    integrand = lambda t: t ** m * (1 - t) ** m * (1 - gamma_mp * t) ** (n - m)
    integral_val = mp.quad(integrand, [0, 1])
    return Cnorm * beta_pref * integral_val

max_rel_err = mp.mpf(0)
n_checks = 0
test_grid = [(5, 0), (5, 2), (9, 3), (17, 4), (30, 6), (12, 5), (40, 8), (60, 10)]
for n_val, m_val in test_grid:
    if m_val > n_val:
        continue
    for gnum, gden in [(1, 4), (2, 7), (1, 2), (5, 6)]:
        g_frac = F(gnum, gden)
        exact = T_nm_direct(n_val, m_val, g_frac)
        exact_mp = mp.mpf(exact.numerator) / mp.mpf(exact.denominator)
        g_mp = mp.mpf(gnum) / mp.mpf(gden)
        predicted = T_beta_integral(n_val, m_val, g_mp)
        rel_err = abs(predicted - exact_mp) / abs(exact_mp)
        max_rel_err = max(max_rel_err, rel_err)
        n_checks += 1

print(f"Checked {n_checks} (n,m,gamma) triples, disjoint grid from ancestor scripts.")
print(f"Max relative error: {mp.nstr(max_rel_err, 8)}")
assert max_rel_err < mp.mpf('1e-40'), "Beta-integral closed form FAILED independent re-verification"
print("CONFIRMED (independently, fresh code): Beta-integral closed form for T(n,m) holds.")

print()
print("=" * 78)
print("(D) Consistency: term_m(n,gamma) := (g^m/n^m) m! T(n,m) via BOTH exact-sum")
print("    and Beta-integral routes, agreeing, and term_0 -> 1/gamma as n->inf")
print("=" * 78)

def term_m_exact(n, m, gamma_frac):
    return (gamma_frac ** m) * factorial(m) * T_nm_direct(n, m, gamma_frac) / (n ** m)

def term_m_beta(n, m, gamma_mp):
    return (gamma_mp ** m) * mp.factorial(m) * T_beta_integral(n, m, gamma_mp) / (mp.mpf(n) ** m)

mism = 0
checks = 0
for n_val, m_val in [(20, 0), (20, 3), (50, 5), (80, 8)]:
    for gnum, gden in [(1, 3), (1, 2), (7, 10)]:
        g_frac = F(gnum, gden)
        g_mp = mp.mpf(gnum) / mp.mpf(gden)
        t1 = term_m_exact(n_val, m_val, g_frac)
        t1_mp = mp.mpf(t1.numerator) / mp.mpf(t1.denominator)
        t2 = term_m_beta(n_val, m_val, g_mp)
        rel = abs(t1_mp - t2) / abs(t1_mp)
        checks += 1
        if rel > mp.mpf('1e-35'):
            mism += 1
            print(f"  MISMATCH term_m n={n_val} m={m_val} g={g_frac}: {t1_mp} vs {t2}")
print(f"term_m cross-check (exact sum vs Beta integral): {checks} checks, {mism} mismatches")
assert mism == 0

# term_0(n,gamma) = (1-(1-gamma)^{n+1})/gamma -> 1/gamma as n -> infty
for gnum, gden in [(1, 3), (1, 2), (7, 10)]:
    g_mp = mp.mpf(gnum) / mp.mpf(gden)
    t0_500 = term_m_beta(500, 0, g_mp)
    predicted_limit = 1 / g_mp
    print(f"  gamma={gnum}/{gden}: term_0(n=500) = {mp.nstr(t0_500,15)}, "
          f"1/gamma = {mp.nstr(predicted_limit,15)}, "
          f"diff = {mp.nstr(abs(t0_500-predicted_limit),6)}")
    assert abs(t0_500 - predicted_limit) < mp.mpf('1e-70')

print()
print("All baseline facts independently re-derived and re-verified. No mismatches.")
print("No randomness used in this script (exact Fraction / sympy / deterministic mpmath only).")
