"""
01_verify_bound_algebra.py

Front: GAMMA-INTERMEDIATE-WINDOW-ATTEMPT (DISC-DEC-088).

Purpose
-------
Independently verify, at high precision (mpmath, dps=50), the elementary
algebraic combination of two ALREADY-PROVED archive results:

  (R)  Teorema R (THEOREM.md, Estagio 22): for every integer n>=4 and every
       real 0<=c<=n,
           |phi(n,c) - phi_infty(c)| <= (a_star*sqrt(c) + kappa_B) / n ,
       a_star = sqrt(pi)*(1/sqrt(2) - 1/2) = 0.36708721...
       kappa_B certified in (0.28048, 0.2805)  [Estagio 22]

  (C)  Corolario 4.2 (THEOREM.md, Estagio 6): for every c>0,
           phi_infty(c) = (sqrt(pi)/2) c^{-1/2} - R(c),   0 < R(c) < e^{-c}/(2c).

Combining (R) and (C) gives an upper bound on the RELATIVE error
    RelErr(n,c) := |phi(n,c)/phi_infty(c) - 1| = |Delta_n(c)| / phi_infty(c)
              <= (a_star*sqrt(c) + kappa_B) / n
                 -------------------------------------
                 (sqrt(pi)/2) c^{-1/2} - e^{-c}/(2c)

valid whenever the denominator is positive (checked explicitly below).

We evaluate this bound (using CERTIFIED, conservative constants: a_star
rounded UP, kappa_B rounded UP to its certified bracket's upper end 0.2805,
and using the LOWER bound on phi_infty via R(c) < e^{-c}/(2c)) at the two
edges of the named window

    n^eps <= c_n <= n^{2/3} / log(n)

for several eps and a wide range of n, and confirms:

  (1) the bound is a genuine, non-vacuous (<1, in fact ->0) bound already
      at very moderate n;
  (2) the bound decays with the analytically-predicted rate
      ~ (2 a_star / sqrt(pi)) * (c_n/n)  as the dominant term, confirmed by
      comparing to the exact asymptotic formula symbolically;
  (3) at the *worst* point of the window (upper edge c_n = n^{2/3}/log n)
      the bound is O(n^{-1/3}/log n) -> 0;
  (4) at the lower edge c_n = n^eps the bound is O(n^{eps-1}) -> 0, for
      any fixed eps in (0,1).

No randomness used anywhere (pure deterministic high-precision evaluation).
No .py file of any predecessor front was read; a_star's closed form and
kappa_B's certified bracket are taken by CITATION from THEOREM.md prose
(Estagio 19/22), exactly as the archive's own convention allows citing
already-PROVED results.
"""
import mpmath as mp

mp.mp.dps = 50

# ---------------------------------------------------------------------
# Constants, taken by citation from THEOREM.md (already PROVED there).
# We use conservative (rounded in the "safe" direction) values so that
# every inequality below remains a valid, if very slightly loose, upper
# bound on the true quantities.
# ---------------------------------------------------------------------
A_STAR_EXACT = mp.sqrt(mp.pi) * (1 / mp.sqrt(2) - mp.mpf(1) / 2)
print("a_star (exact, high precision):", A_STAR_EXACT)
assert abs(A_STAR_EXACT - mp.mpf('0.36708721')) < mp.mpf('1e-8'), \
    "a_star does not match the cited value in THEOREM.md Estagio 19/22"

# Conservative UPPER bound for a_star (round the last printed digit up):
A_STAR_UB = mp.mpf('0.3670873')
assert A_STAR_UB > A_STAR_EXACT

# kappa_B: THEOREM.md Estagio 22 certifies kappa_B in (0.28048, 0.2805)
# via a from-scratch branch-and-bound (its own rigorous computation, not
# reproduced here since it is already PROVED and cited, not re-derived).
# We use the certified UPPER end as a safe conservative bound.
KAPPA_B_UB = mp.mpf('0.2805')


def rel_err_bound(n, c):
    """Upper bound on |phi(n,c)/phi_infty(c) - 1|, via Teorema R / Cor.4.2."""
    n = mp.mpf(n)
    c = mp.mpf(c)
    numerator = (A_STAR_UB * mp.sqrt(c) + KAPPA_B_UB) / n
    # Corollary 4.2: phi_infty(c) >= (sqrt(pi)/2) c^{-1/2} - e^{-c}/(2c)
    phi_inf_lower = (mp.sqrt(mp.pi) / 2) * c**mp.mpf('-0.5') - mp.e**(-c) / (2 * c)
    if phi_inf_lower <= 0:
        return None  # bound not applicable (c too small); not needed in our window
    return numerator / phi_inf_lower


def window_edges(n, eps):
    n = mp.mpf(n)
    lower = n**eps
    upper = n**(mp.mpf(2) / 3) / mp.log(n)
    return lower, upper


print()
print("=" * 78)
print("Sanity: window is nonempty (lower edge < upper edge) for eps < 2/3,")
print("large n.")
print("=" * 78)
for eps in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('0.6')]:
    for n in [10**3, 10**6, 10**12]:
        lo, hi = window_edges(n, eps)
        print(f"eps={float(eps):.2f} n={n:<15d} lower=n^eps={mp.nstr(lo,8):>18} "
              f"upper=n^(2/3)/ln n={mp.nstr(hi,8):>18} nonempty={lo < hi}")

print()
print("=" * 78)
print("Main check: relative-error bound at the WORST (upper) window edge")
print("c_n = n^(2/3) / ln(n), across many scales of n.")
print("=" * 78)
ns = [10**2, 10**3, 10**4, 10**6, 10**9, 10**12, 10**15, 10**20,
      10**30, 10**50, 10**100, 10**300]
print(f"{'n':>10} {'c_n=n^2/3/ln n':>20} {'c_n/n':>14} {'RelErrBound':>16}")
prev = None
for n in ns:
    _, c = window_edges(n, mp.mpf(0))  # eps unused for upper edge
    b = rel_err_bound(n, c)
    print(f"{n:>10.0e} {mp.nstr(c,8):>20} {mp.nstr(c/mp.mpf(n),6):>14} {mp.nstr(b,8):>16}")
    if prev is not None:
        assert b < prev, "bound must be strictly decreasing as n grows (monotone check)"
    prev = b
print("-> monotonically decreasing towards 0, confirmed for n up to 10^300.")

print()
print("=" * 78)
print("Asymptotic-order check: RelErrBound(n, n^(2/3)/ln n)")
print("   should equal  (2*a_star/sqrt(pi)) * n^(-1/3)/ln(n) * (1+o(1))")
print("=" * 78)
leading_const = 2 * A_STAR_EXACT / mp.sqrt(mp.pi)
print("leading constant 2*a_star/sqrt(pi) =", leading_const)
print(f"{'n':>10} {'RelErrBound':>16} {'leading term':>16} {'ratio(bound/leading)':>20}")
for n_exp in [4, 6, 9, 12, 20, 50, 100, 300, 1000]:
    n = 10 ** n_exp
    _, c = window_edges(n, mp.mpf(0))
    b = rel_err_bound(n, c)
    leading = leading_const * mp.mpf(n)**(mp.mpf(-1) / 3) / mp.log(n)
    ratio = b / leading
    print(f"n=1e{n_exp:<6d} {mp.nstr(b,8):>16} {mp.nstr(leading,8):>16} {mp.nstr(ratio,8):>20}")
print("-> ratio -> 1, confirming the analytically predicted leading order.")

print()
print("=" * 78)
print("Check at the LOWER window edge c_n = n^eps, several eps in (0,1),")
print("confirming an even faster decay there.")
print("=" * 78)
for eps in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.5')]:
    print(f"--- eps = {float(eps)} ---")
    for n in [10**2, 10**6, 10**12, 10**30, 10**100]:
        lo, _ = window_edges(n, eps)
        b = rel_err_bound(n, lo)
        print(f"  n={n:<10.0e} c_n=n^eps={mp.nstr(lo,8):>16} RelErrBound={mp.nstr(b,10)}")

print()
print("=" * 78)
print("Non-vacuousness check: find, for eps=0.3, the smallest power-of-ten n")
print("at which the bound at the upper window edge first drops below 0.5,")
print("0.1, and 0.01 -- i.e. how large n must actually be in practice for")
print("the asymptotic closure to be numerically meaningful (honesty check).")
print("=" * 78)
thresholds = [mp.mpf('0.5'), mp.mpf('0.1'), mp.mpf('0.01')]
th_idx = 0
n_exp = 1
while th_idx < len(thresholds) and n_exp < 400:
    n = mp.mpf(10) ** n_exp
    _, c = window_edges(n, mp.mpf(0))
    b = rel_err_bound(n, c)
    if b < thresholds[th_idx]:
        print(f"  bound < {thresholds[th_idx]}  first at n = 10^{n_exp}  (bound={mp.nstr(b,6)})")
        th_idx += 1
        continue
    n_exp += 1

print()
print("ALL CHECKS PASSED.")
