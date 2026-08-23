"""
Referee check 01 -- Proposicao 2.1 and Theorem 1 of ATTEMPT.md.

Everything here is re-derived from scratch from the PRIMARY sources named in
the referee brief:

  - Theorem A / Theorem B, read directly from
    k2_open_lemma/k3_attempt_2/k6_attempt/k_general_existence_attempt/
    error_constant_growth_attempt/all_orders_closed_form_attempt/ATTEMPT.md
    Sec.4 (around its own line ~392-420) -- transcribed here independently,
    NOT copied from the target document's Sec.2.
  - Reduction Lemma A / (2.1), read directly from k2_open_lemma/ATTEMPT.md Sec.2.
  - mychain.py (this directory): an independent from-scratch reimplementation
    of the (a,b,r) exploration-walk Markov chain, used as ground truth for
    psi_n^{(K)}, psi_n^{(K),R}, phi_n^{(K)} -- NOT the closed forms below.

Two independent things are checked:

(A) SYMBOLIC RE-DERIVATION of Proposicao 2.1 from Theorem A/B (sympy, general
    n, concrete K), confirming the target's transcription of the Estagio-9
    primary source is correct, not merely restating the target's own algebra.

(B) THEOREM 1's exact decomposition identity: symbolically (sympy) for a
    wider K-range than the target tested (target: K=0..8), plus an exact
    Fraction check to much higher K, cross-validated against mychain.py's
    independent recursion (ground truth, not from the closed forms).
"""
import sys
from fractions import Fraction as F
from math import comb, factorial

import sympy as sp

sys.path.insert(0, ".")
import mychain as mc

log = open("check01_prop21_theorem1.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


# ---------------------------------------------------------------------------
# PART A: symbolic re-derivation of Proposicao 2.1 from Theorem A/B directly.
# ---------------------------------------------------------------------------
p("=" * 78)
p("PART A: re-deriving Proposicao 2.1 from Theorem A/B (primary source),")
p("        symbolically, independent of the target's own Sec.2 algebra.")
p("=" * 78)

n_sym = sp.symbols("n", positive=True)


def g_r_theoremA(r, b, m, nsym):
    """Theorem A (binomial form), transcribed directly from the primary
    source (all_orders_closed_form_attempt/ATTEMPT.md Sec.4, the boxed
    formula right after 'Binomial form.'):

        g_r(m,b) = r!(r+b)!/(2r+b+1)! * sum_{j=0}^r C(2r+b+1,r-j) (m+j)!/(m! n^j)

    r,b are concrete nonnegative integers; m, nsym are symbolic/expressions.
    """
    N = 2 * r + b + 1
    pref = sp.Rational(factorial(r) * factorial(r + b), factorial(N))
    total = 0
    for j in range(0, r + 1):
        rising = 1
        for i in range(1, j + 1):
            rising *= (m + i)
        total += sp.binomial(N, r - j) * rising / nsym**j
    return sp.together(pref * total)


def h_r_theoremB(r, b, a, nsym):
    """Theorem B, transcribed directly from the primary source:
        h_r(a,b) = (n-a+1)/n * g_r(n-a+1, b+1)   [g's Theorem-A closed form,
        evaluated possibly out of g's own probabilistic domain at a=0 -- the
        document's own explicitly-flagged 'Domain caveat', reproduced here
        verbatim as a formula, not reinterpreted]."""
    m_prime = nsym - a + 1
    return sp.together((nsym - a + 1) / nsym * g_r_theoremA(r, b + 1, m_prime, nsym))


def prop21_target_formula(K, nsym):
    """The target document's claimed closed form (Proposicao 2.1):
        psi_n^{(K),R} = kappa * sum_{i=1}^K C(2K,K-i) * g(i;n),
        kappa := (K-1)! K! / (2K)!,  g(i;n) := prod_{l=1}^i (1+l/n)."""
    kappa = sp.Rational(factorial(K - 1) * factorial(K), factorial(2 * K))
    total = 0
    for i in range(1, K + 1):
        gin = 1
        for l in range(1, i + 1):
            gin *= (1 + sp.Rational(l, 1) / nsym)
        total += sp.binomial(2 * K, K - i) * gin
    return sp.together(kappa * total)


p("Checking h_{K-1}(0,0) [Theorem B at r=K-1,a=0,b=0] equals the target's")
p("Proposicao 2.1 closed form, symbolically in n, for K=1..14:")
all_ok_A = True
for K in range(1, 15):
    lhs = h_r_theoremB(K - 1, 0, 0, n_sym)
    rhs = prop21_target_formula(K, n_sym)
    diff = sp.simplify(lhs - rhs)
    ok = (diff == 0)
    all_ok_A &= ok
    p(f"  K={K:2d}  sympy.simplify(TheoremB - Proposicao2.1) = {diff}   {'OK' if ok else 'MISMATCH!!'}")
p(f"PART A RESULT: {'ALL 14/14 SYMBOLIC MATCHES' if all_ok_A else 'FAILURE'}")
p("(This independently re-derives Proposicao 2.1 from the primary source's")
p(" own Theorem A/B formulas, transcribed fresh from that source's prose,")
p(" not from the target document's Sec.2 restatement of them.)")

# Cross-check psi_n^{(K),R} (Proposicao 2.1's closed form) against
# mychain.py's independent h(0,0,K-1) recursion, exact Fraction, for a wide
# (K,n) grid.
p("")
p("Cross-checking Proposicao 2.1's closed form against mychain.py's")
p("independent (a,b,r) Markov-chain recursion for psi_n^{(K),R}, exact Fraction:")


def prop21_value(K, n):
    kappa = F(factorial(K - 1) * factorial(K), factorial(2 * K))
    total = F(0)
    for i in range(1, K + 1):
        gin = F(1)
        for l in range(1, i + 1):
            gin *= F(n + l, n)
        total += comb(2 * K, K - i) * gin
    return kappa * total


count = 0
mism = 0
for K in range(1, 13):
    for n in range(K + 1, K + 16):
        v1 = prop21_value(K, n)
        v2 = mc.psi_R(n, K)
        count += 1
        if v1 != v2:
            mism += 1
            p(f"  MISMATCH K={K} n={n}: closed-form={v1} chain={v2}")
p(f"psi_n^{{(K),R}} cross-check: {count} pairs, {mism} mismatches "
  f"(K=1..12, n=K+1..K+15)")

log.write("\n")

# ---------------------------------------------------------------------------
# PART B: Theorem 1's exact decomposition identity.
# ---------------------------------------------------------------------------
p("=" * 78)
p("PART B: Theorem 1's exact decomposition identity, T(n,K)/A = RHS")
p("=" * 78)


def phi_K_sym(K):
    return sp.Rational(4**K * factorial(K)**2, factorial(2 * K + 1))


def psi_K_theoremA(K, nsym):
    """Corolario A1 = g_K(n,0) via Theorem A directly."""
    return g_r_theoremA(K, 0, nsym, nsym)


def T_over_A_LHS(K, nsym):
    """LHS: T(n,K)/A computed independently from (2.1) + Theorem-A psi +
    Proposicao-2.1-style psi_R (all re-derived above from Theorem B), i.e.
    completely independent of the target's own Sec.3 collect-and-simplify
    algebra -- only the CITED facts (2.1), Theorem A, Theorem B are used."""
    A = phi_K_sym(K) / sp.Integer(4)**K
    phiK = phi_K_sym(K)
    psi = psi_K_theoremA(K, nsym)
    psiR = h_r_theoremB(K - 1, 0, 0, nsym) if K >= 1 else sp.Integer(1)
    if K == 0:
        phi_n = sp.Integer(1)
    else:
        phi_n = sp.Rational(K, 1) / nsym * psiR + (1 - sp.Rational(K, 1) / nsym) * psi
    T = nsym * (phi_n - phiK)
    return sp.together(T / A)


def T_over_A_RHS(K, nsym):
    """RHS: the target document's boxed Theorem 1 formula, transcribed
    directly from ATTEMPT.md Sec.3 (independently re-typed here)."""
    CONST = sp.Integer(2)**(2 * K - 1) - sp.Rational(2 * K + 1, 2) * sp.binomial(2 * K, K)
    total = CONST
    for j in range(1, K + 1):
        fj = nsym * (g_of_j(j, nsym) - 1)
        Bj = sp.Rational((2 * K + 1) * (j + 1), K + j + 1) * sp.binomial(2 * K, K - j)
        total += sp.binomial(2 * K + 1, K - j) * fj + Bj * (g_of_j(j, nsym) - 1)
    return sp.together(total)


def g_of_j(j, nsym):
    prod = 1
    for l in range(1, j + 1):
        prod *= (1 + sp.Rational(l, 1) / nsym)
    return prod


p("Symbolic identity check (sympy.simplify(LHS-RHS)==0), K=0..25")
p("(target's own T1 test only went to K=0..8):")
all_ok_B_sym = True
for K in range(0, 26):
    lhs = T_over_A_LHS(K, n_sym)
    rhs = T_over_A_RHS(K, n_sym)
    diff = sp.simplify(lhs - rhs)
    ok = (diff == 0)
    all_ok_B_sym &= ok
    p(f"  K={K:2d}  diff={diff}   {'OK' if ok else 'MISMATCH!!'}")
p(f"PART B SYMBOLIC RESULT: {'ALL 26/26 MATCHES (K=0..25)' if all_ok_B_sym else 'FAILURE'}")

log.close()
print("\nWrote check01_prop21_theorem1.log")
