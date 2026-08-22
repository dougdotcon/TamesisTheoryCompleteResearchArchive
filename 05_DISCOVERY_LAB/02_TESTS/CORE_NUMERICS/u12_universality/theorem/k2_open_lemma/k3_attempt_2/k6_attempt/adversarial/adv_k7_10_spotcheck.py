"""
PART A, item 3 (adversarial referee, k6_attempt).

Spot-check K=7..10's claimed closed forms.

(A) K=7: FULL independent re-derivation via markov_transfer.build_levels(7),
    plus substitution of every level's closed form (g_0..g_7, h_0..h_7) into
    the exact defining recursion (typed fresh, as in adv_k6_recursion_check.py),
    plus a match against the document's claimed psi_n^(7) closed form.

(B) K=7,8,9,10: verify, DIRECTLY from the document's own claimed closed forms
    (taken as given text, not re-derived, for B alone), that:
      - the n->infinity limit equals phi_K = 4^K(K!)^2/(2K+1)! exactly
      - the 1/n coefficient equals K*phi_K/4 exactly (the rate conjecture,
        unconditionally, since these are EXACT finite closed forms, no
        continuum argument needed)
    extending verify_via_exact_k9_k10.py's check (which only covered K=9,10)
    to all four of K=7,8,9,10.
"""
import sys
sys.path.insert(0, '/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/k3_attempt_2')
import sympy as sp
import markov_transfer as mt
import time

n_sym = mt.n
b_sym = mt.b

print("=" * 70)
print("PART (A): full independent re-derivation + recursion check at K=7")
print("=" * 70)
t0 = time.time()
levels7 = mt.build_levels(7)
print(f"build_levels(7) took {time.time()-t0:.1f}s")

psi7_mine = sp.simplify(levels7[7][0](n_sym, 0))
psi7_claimed = sp.together(
    16384 * n_sym**7 + 28672 * n_sym**6 + 48818 * n_sym**5 + 67550 * n_sym**4
    + 70819 * n_sym**3 + 52192 * n_sym**2 + 23868 * n_sym + 5040
) / (51480 * n_sym**7)
diff = sp.simplify(psi7_mine - psi7_claimed)
print("psi_n^(7) mine     =", psi7_mine)
print("psi_n^(7) claimed  =", psi7_claimed)
print("difference (should be 0):", diff)
assert diff == 0

print()
print("Substituting all 16 levels (g_0..g_7, h_0..h_7) into the exact recursion:")


def check_g_recursion(r, g_r_func, h_prev_func):
    m = sp.Symbol('m', positive=True)
    lhs = g_r_func(m, b_sym)
    term_h = 0
    if r >= 1:
        term_h = sp.Rational(r, 1) / m * h_prev_func(n_sym - m + 1, b_sym)
    term_g = (m - 1 - r - b_sym) / m * g_r_func(m - 1, b_sym)
    rhs = sp.Rational(1, 1) / m + term_h + term_g
    return sp.simplify(lhs - rhs) == 0


def check_h_recursion(r, h_r_func, h_prev_func, g_r_func):
    a = sp.Symbol('a', positive=True)
    lhs = h_r_func(a, b_sym)
    term_h = 0
    if r >= 1:
        term_h = sp.Rational(r, 1) / n_sym * h_prev_func(a, b_sym + 1)
    term_g = (n_sym - 1 - a - b_sym - r) / n_sym * g_r_func(n_sym - a, b_sym + 1)
    rhs = sp.Rational(1, 1) / n_sym + term_h + term_g
    return sp.simplify(lhs - rhs) == 0


all_ok = True
h_prev = None
for r in range(0, 8):
    g_r, h_r = levels7[r]
    ok_g = check_g_recursion(r, g_r, h_prev)
    ok_h = check_h_recursion(r, h_r, h_prev, g_r)
    print(f"  r={r}: g_{r} OK={ok_g}   h_{r} OK={ok_h}")
    all_ok = all_ok and ok_g and ok_h
    h_prev = h_r
print("ALL 16 LEVELS SATISFY THE EXACT RECURSION:", all_ok)
assert all_ok

print()
print("=" * 70)
print("PART (B): internal-consistency check of K=7,8,9,10's claimed closed")
print("          forms (limit = phi_K, 1/n coefficient = K*phi_K/4), taken")
print("          directly from ATTEMPT.md Sec.1.1's stated formulas")
print("=" * 70)

claimed = {
    7: (16384 * n_sym**7 + 28672 * n_sym**6 + 48818 * n_sym**5 + 67550 * n_sym**4
        + 70819 * n_sym**3 + 52192 * n_sym**2 + 23868 * n_sym + 5040) / (51480 * n_sym**7),
    8: (32768 * n_sym**8 + 65536 * n_sym**7 + 131870 * n_sym**6 + 223472 * n_sym**5
        + 300913 * n_sym**4 + 306016 * n_sym**3 + 219100 * n_sym**2 + 97632 * n_sym + 20160) / (109395 * n_sym**8),
    9: (262144 * n_sym**9 + 589824 * n_sym**8 + 1371549 * n_sym**7 + 2759301 * n_sym**6
        + 4562055 * n_sym**5 + 5967729 * n_sym**4 + 5900344 * n_sym**3 + 4116636 * n_sym**2
        + 1792656 * n_sym + 362880) / (923780 * n_sym**9),
    10: (524288 * n_sym**10 + 1310720 * n_sym**9 + 3462425 * n_sym**8 + 8082170 * n_sym**7
         + 15900584 * n_sym**6 + 25576250 * n_sym**5 + 32554945 * n_sym**4 + 31376020 * n_sym**3
         + 21389436 * n_sym**2 + 9124560 * n_sym + 1814400) / (1939938 * n_sym**10),
}


def phiK(K):
    return sp.Rational(4**K * sp.factorial(K)**2, sp.factorial(2 * K + 1))


all_ok2 = True
for K in [7, 8, 9, 10]:
    psi = claimed[K]
    lim = sp.limit(psi, n_sym, sp.oo)
    rate = sp.limit((psi - lim) * n_sym, n_sym, sp.oo)
    target_lim = phiK(K)
    target_rate = sp.simplify(sp.Rational(K, 4) * target_lim)
    ok_lim = (lim == target_lim)
    ok_rate = (rate == target_rate)
    all_ok2 = all_ok2 and ok_lim and ok_rate
    print(f"K={K}: limit={lim} (phi_{K}={target_lim}, match={ok_lim})   "
          f"1/n coeff={rate} (K*phi_K/4={target_rate}, match={ok_rate})")
print("ALL LIMIT + RATE CHECKS PASS:", all_ok2)
assert all_ok2

print()
print("ALL PART-A-ITEM-3 CHECKS PASSED.")
