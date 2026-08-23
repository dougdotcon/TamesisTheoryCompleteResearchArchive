"""
REFEREE independent check 1 — Corolario A1's closed form for psi_n^{(K)}.

Written entirely from scratch, from the PRIMARY sources (not the target
document's transcription of them):

  psi_n^{(1)} = 2/3 + 1/(6n)
      -- k2_open_lemma/ATTEMPT.md  Section 3, line ~226
  psi_n^{(2)} = 8/15 + 4/(15n) + 1/(15n^2)
      -- k2_open_lemma/ATTEMPT.md  Section 4.4, line ~359
  psi_n^{(3)} = 16/35 + 12/(35n) + 5/(28n^2) + 3/(70n^3)
      -- k2_open_lemma/k3_attempt_2/ATTEMPT.md  Section 5, line ~305
  psi_n^{(4)} = 128/315 + 128/(315n) + 103/(315n^2) + 52/(315n^3) + 4/(105n^4)
      -- k2_open_lemma/k3_attempt_2/ATTEMPT.md  Section 7.1, line ~409

Corolario A1 (THEOREM.md, Estagio 9, PROVED unconditionally):

  psi_n^{(K)} = (phi_K/4^K) * sum_{j=0}^{K} C(2K+1, K-j) * (n+j)!/(n! n^j)

phi_K = 4^K (K!)^2 / (2K+1)!   (Wallis mean, THEOREM.md Lemma 2 sec 5.2)

We check: (a) Corolario A1's formula, expanded symbolically in n, equals
each of the four primary-source closed forms exactly, for K=1,2,3,4;
(b) the n -> infinity limit of Corolario A1's formula equals phi_K exactly,
for K=0..12; (c) psi_n^{(0)} = 1 identically.
"""
import sympy as sp

n = sp.symbols('n', positive=True)


def phi(K):
    return sp.Rational(4**K) * sp.factorial(K)**2 / sp.factorial(2 * K + 1)


def corollary_a1(K):
    """Corolario A1's closed form, built fresh from the stated formula."""
    total = 0
    for j in range(0, K + 1):
        term = sp.binomial(2 * K + 1, K - j) * sp.factorial(n + j) / (
            sp.factorial(n) * n**j
        )
        total += term
    return sp.together(sp.simplify(phi(K) / sp.Integer(4)**K * total))


# Primary-source closed forms, transcribed independently from the primary
# documents (NOT from the target document's own transcription).
primary_sources = {
    1: sp.Rational(2, 3) + sp.Rational(1, 6) / n,
    2: sp.Rational(8, 15) + sp.Rational(4, 15) / n + sp.Rational(1, 15) / n**2,
    3: sp.Rational(16, 35) + sp.Rational(12, 35) / n + sp.Rational(5, 28) / n**2
    + sp.Rational(3, 70) / n**3,
    4: sp.Rational(128, 315) + sp.Rational(128, 315) / n + sp.Rational(103, 315) / n**2
    + sp.Rational(52, 315) / n**3 + sp.Rational(4, 105) / n**4,
}

print("=== (a) Corolario A1 vs primary-source closed forms, K=1..4 ===")
all_match_a = True
for K, target_expr in primary_sources.items():
    lhs = corollary_a1(K)
    diff = sp.simplify(sp.together(lhs - target_expr))
    ok = diff == 0
    all_match_a &= ok
    print(f"K={K}: Corolario A1 - primary_source = {diff}  ->  {'MATCH' if ok else 'MISMATCH'}")

print()
print("=== (b) n -> infinity limit of Corolario A1 vs phi_K, K=0..12 ===")
all_match_b = True
for K in range(0, 13):
    expr = corollary_a1(K)
    lim = sp.limit(expr, n, sp.oo)
    target = sp.nsimplify(phi(K))
    ok = sp.simplify(lim - target) == 0
    all_match_b &= ok
    print(f"K={K}: lim = {lim}, phi_K = {target}  ->  {'MATCH' if ok else 'MISMATCH'}")

print()
print("=== (c) psi_n^{(0)} identically 1 ===")
expr0 = corollary_a1(0)
ok0 = sp.simplify(expr0 - 1) == 0
print(f"Corolario A1 at K=0: {expr0}  ->  {'IDENTICALLY 1' if ok0 else 'NOT IDENTICALLY 1'}")

print()
overall = all_match_a and all_match_b and ok0
print(f"OVERALL: {'ALL CHECKS PASS' if overall else 'FAILURE DETECTED'}")
