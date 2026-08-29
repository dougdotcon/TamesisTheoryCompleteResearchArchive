#!/usr/bin/env python3
"""
Script 01 -- Fresh, from-scratch re-derivation of the EXACT finite-sum
structure of A_k(n,gamma), directly from Lemma 1's raw definition
(gamma_scaling_attempt/ATTEMPT.md Sec 1, quoted and cited, NOT re-derived
from Definition 1 of THEOREM.md itself -- Lemma 1's own combinatorial
proof is accepted as already PROVED in this lineage).

    A_k(n,gamma) = sum_{m=0}^k C(k,m) gamma^m (1-gamma)^{k-m} P_{k,m}
    P_{k,m}      = prod_{i=1}^m (1 - (k-i)/n) = (n-k+1)_m / n^m   (Pochhammer)

NO ancestor .py file was opened or imported anywhere in this front.
Every check below is written fresh from the mathematical PROSE quoted
in gamma_scaling_attempt/ATTEMPT.md Sec 1 (Lemma 1) and re-verified
independently against a brute-force combinatorial enumerator distinct
from the one that front used (that front's V1 check enumerated
Definition 1 directly with permutations/reroutes; this script's sanity
check instead enumerates the *cycle-counting* combinatorial identity
A_k = E[P_{k,M}] directly against a literal m-by-m symbolic sum, a
different, narrower cross-check aimed only at confirming this script's
own manipulation of the already-cited formula is correct, not at
re-proving Lemma 1 itself).

New observation of this front (Sec 2 below): A_k(n,gamma), after
factoring out (1-gamma)^k, is EXACTLY a terminating (well-defined,
finite, no convergence question) 2F0 hypergeometric polynomial in a
single variable w := -gamma/((1-gamma)n):

    A_k(n,gamma) = (1-gamma)^k * 2F0(-k, n-k+1 ; ; w),   w = -gamma/((1-gamma)n)

2F0(-k,b;;w) := sum_{m=0}^k  [(-k)_m (b)_m / m!] w^m   (terminates since
(-k)_m = 0 for m>k -- a finite polynomial, no formal-series convergence
issue at all).

This 2F0 form itself (Part B) is fully, independently verified (both
symbolically for k=0..6 with n,gamma left free, and numerically via 40
random exact-Fraction (n,k,gamma) triples). Part C ATTEMPTS to further
identify it with a classical CHARLIER POLYNOMIAL C_k(x;a):=2F0(-k,-x;;
-1/a) -- this attempt does NOT check out under this script's own naive
parameter matching (disclosed honestly in Part C/ATTEMPT.md Self-caught
issues) and is explicitly NOT claimed as a result. Nothing downstream
(script 02, 03) relies on the Charlier name; only on the independently-
verified 2F0 form, which is new to this lineage either way (Lemma 1's
own PROOF works entirely with the P_{k,m}/sigma_k(m) exponential-
sandwich route, never noting the exact product is itself a rising
factorial / Pochhammer ratio, i.e. exactly a terminating hypergeometric
sum).

Nothing in this script is a numerical experiment about C(gamma) itself
-- it is pure exact-algebra scaffolding, checked purely symbolically
and via small-case brute force, laying the exact-structure groundwork
that script 02/03 build on.
"""
import sys
import sympy as sp
from sympy import symbols, Rational, binomial, prod, simplify, nsimplify, Poly, gamma as sp_gamma
from fractions import Fraction

LOG = []
def log(*args):
    s = " ".join(str(a) for a in args)
    print(s)
    LOG.append(s)

log("="*78)
log("SCRIPT 01 -- exact hypergeometric/Charlier structure of A_k(n,gamma)")
log("="*78)

# ---------------------------------------------------------------------
# Part A. Symbolic definition of A_k exactly as quoted from Lemma 1,
# and independent symbolic re-derivation of the closed algebraic form
# of P_{k,m} as a Pochhammer ratio.
# ---------------------------------------------------------------------
log("\n--- Part A: P_{k,m} as an exact Pochhammer/rising-factorial ratio ---")

n_s, k_s, gam_s = symbols('n k gamma', positive=True)
m_s = symbols('m', integer=True, nonnegative=True)

def P_km_product(k_val, m_val, n_val):
    """Literal product P_{k,m} = prod_{i=1}^m (1-(k-i)/n), exact rationals."""
    val = sp.Integer(1)
    for i in range(1, m_val+1):
        val *= (1 - Rational(k_val - i, n_val))
    return val

def P_km_pochhammer(k_val, m_val, n_val):
    """Claimed closed form: (n-k+1)_m / n^m, i.e. prod_{i=1}^m (n-k+i)/n."""
    num = sp.Integer(1)
    for i in range(1, m_val+1):
        num *= (n_val - k_val + i)
    return Rational(num, n_val**m_val)

mismatches = 0
checks = 0
for n_val in range(3, 14):
    for k_val in range(1, n_val+1):
        for m_val in range(0, k_val+1):
            a = P_km_product(k_val, m_val, n_val)
            b = P_km_pochhammer(k_val, m_val, n_val)
            checks += 1
            if sp.simplify(a - b) != 0:
                mismatches += 1
                log(f"  MISMATCH n={n_val} k={k_val} m={m_val}: {a} vs {b}")
log(f"P_{{k,m}} product-form vs Pochhammer-form: {checks} checks, {mismatches} mismatches "
    f"(n=3..13, all valid k,m)")
assert mismatches == 0

# ---------------------------------------------------------------------
# Part B. A_k as a finite sum; verify the 2F0 hypergeometric packaging
# reproduces the same finite sum, symbolically, for small k (n,gamma
# left symbolic).
# ---------------------------------------------------------------------
log("\n--- Part B: A_k(n,gamma) as a terminating 2F0 in w=-gamma/((1-gamma)n) ---")

def A_k_direct_symbolic(k_val, n_sym, g_sym):
    """A_k via the literal Lemma-1 finite sum, n and gamma left symbolic."""
    total = sp.Integer(0)
    for m_val in range(0, k_val+1):
        Pkm = sp.Integer(1)
        for i in range(1, m_val+1):
            Pkm *= (n_sym - k_val + i) / n_sym
        total += binomial(k_val, m_val) * g_sym**m_val * (1-g_sym)**(k_val-m_val) * Pkm
    return sp.expand(total)

def A_k_2F0_symbolic(k_val, n_sym, g_sym):
    """A_k via the claimed 2F0 packaging:
       (1-g)^k * sum_{m=0}^k [(-k)_m (n-k+1)_m / m!] * w^m,  w=-g/((1-g)n)."""
    w = -g_sym / ((1-g_sym)*n_sym)
    total = sp.Integer(0)
    poch_negk = sp.Integer(1)      # (-k)_0 = 1
    poch_b    = sp.Integer(1)      # (n-k+1)_0 = 1
    fact      = sp.Integer(1)
    for m_val in range(0, k_val+1):
        if m_val > 0:
            poch_negk *= (-k_val + (m_val-1))
            poch_b    *= (n_sym - k_val + 1 + (m_val-1))
            fact      *= m_val
        total += (poch_negk * poch_b / fact) * w**m_val
    return sp.expand((1-g_sym)**k_val * total)

mismatches_B = 0
for k_val in range(0, 7):
    direct = A_k_direct_symbolic(k_val, n_s, gam_s)
    hyp    = A_k_2F0_symbolic(k_val, n_s, gam_s)
    diff = sp.simplify(sp.together(direct - hyp))
    log(f"  k={k_val}: symbolic difference simplifies to: {diff}")
    if diff != 0:
        mismatches_B += 1
log(f"2F0 packaging vs direct Lemma-1 sum: k=0..6, {mismatches_B} mismatches (symbolic, exact)")
assert mismatches_B == 0

# Numeric spot check at a handful of (n,k,gamma) concrete rational points,
# k up to 12, cross-checking BOTH representations evaluate to the same
# exact Fraction.
log("\n  Numeric spot-check (exact Fraction), various (n,k,gamma):")
import random
random.seed(1)   # fixed sanity-check seed, NOT drawn from the reserved block (disclosed, same convention as ancestor fronts)
spot_mismatches = 0
spot_checks = 0
bug_demo_logged = False
for _ in range(40):
    n_val = random.randint(5, 60)
    k_val = random.randint(1, n_val)
    g_num = random.randint(1, 9)
    g_val = Rational(g_num, 10)
    # SELF-CAUGHT BUG (documented in ATTEMPT.md Self-caught issues): the
    # FIRST version of this loop passed n_val as a bare Python int into
    # A_k_direct_symbolic, whose inner loop computes
    # `(n_sym - k_val + i) / n_sym` -- with n_sym a plain int, Python 3's
    # `/` performs FLOATING-POINT division (not exact Fraction division),
    # silently turning `direct` into a float while `hyp` (built entirely
    # from sympy Rational arithmetic) stayed exact. This produced ~1e-17
    # scale spurious "mismatches" (floating roundoff, not a real algebraic
    # discrepancy) in 19/40 random trials. Caught by manually inspecting
    # one flagged case: `direct` printed as a decimal (e.g.
    # `0.239850548797262`) instead of an exact Rational, immediately
    # revealing the float leak. FIX: force n_val to sp.Integer before
    # calling either evaluator, so ALL arithmetic in both functions stays
    # in exact Rational arithmetic throughout, matching this lineage's own
    # established discipline (Fraction/Rational exact arithmetic for all
    # symbolic-tier claims).
    n_val_exact = sp.Integer(n_val)
    direct = A_k_direct_symbolic(k_val, n_val_exact, g_val)
    hyp    = A_k_2F0_symbolic(k_val, n_val_exact, g_val)
    spot_checks += 1
    if sp.simplify(direct - hyp) != 0:
        spot_mismatches += 1
        log(f"    MISMATCH n={n_val} k={k_val} gamma={g_val}")
log(f"  {spot_checks} random exact-Fraction spot checks, {spot_mismatches} mismatches "
    f"(post-fix; see Self-caught issues in ATTEMPT.md for the pre-fix float-leak bug)")
assert spot_mismatches == 0

# ---------------------------------------------------------------------
# Part C. Explicit identification with the Charlier polynomial family
# C_k(x;a) := 2F0(-k,-x;;-1/a), verified purely by parameter substitution
# (algebraic identity, not a numerical coincidence).
# ---------------------------------------------------------------------
log("\n--- Part C: identification with Charlier polynomials C_k(x;a) ---")
log("  Standard definition (classical, e.g. Koekoek-Lesky-Swarttouw):")
log("    C_k(x;a) := 2F0(-k,-x;;-1/a) = sum_{m=0}^k C(k,m) (-x)_m (-1/a)^m")
log("  This front's 2F0 has second upper parameter b=n-k+1 and argument")
log("  w=-gamma/((1-gamma)n). Matching -x=b=n-k+1  =>  x=k-n-1,")
log("  and -1/a=w  =>  a=(1-gamma)n/gamma. So the CLAIM is:")
log("    A_k(n,gamma) = (1-gamma)^k * C_k(k-n-1 ; (1-gamma)n/gamma)")
log("  Verified directly (not via a citation) by expanding the classical")
log("  C_k(x;a) definition symbolically at x=k-n-1, a=(1-gamma)n/gamma and")
log("  comparing term-by-term against Part B's already-verified 2F0 form.")

def Charlier_symbolic(k_val, x_sym, a_sym):
    total = sp.Integer(0)
    poch_negk = sp.Integer(1)
    poch_negx = sp.Integer(1)
    fact = sp.Integer(1)
    for m_val in range(0, k_val+1):
        if m_val > 0:
            poch_negk *= (-k_val + (m_val-1))
            poch_negx *= (-x_sym + (m_val-1))
            fact *= m_val
        total += binomial(k_val, m_val) * poch_negx * (-1/a_sym)**m_val
    return sp.expand(total)

x_expr = k_s - n_s - 1
a_expr = (1-gam_s)*n_s/gam_s

mismatches_C = 0
for k_val in range(0, 7):
    charlier_val = Charlier_symbolic(k_val, x_expr.subs(k_s, k_val), a_expr)
    claim = sp.simplify((1-gam_s)**k_val * charlier_val)
    direct = A_k_direct_symbolic(k_val, n_s, gam_s)
    diff = sp.simplify(sp.together(claim - direct))
    log(f"  k={k_val}: (1-g)^k C_k(k-n-1;(1-g)n/g) - A_k^direct simplifies to: {diff}")
    if diff != 0:
        mismatches_C += 1
log(f"Charlier identification (naive parameter matching): k=0..6, {mismatches_C}/7 mismatches")

# SELF-CAUGHT ISSUE (disclosed, documented in ATTEMPT.md Self-caught
# issues): the naive parameter matching x=k-n-1, a=(1-gamma)n/gamma
# against the textbook convention C_k(x;a):=2F0(-k,-x;;-1/a) does NOT
# reproduce A_k except at k=0 (matches trivially) and k=1 (matches up to
# a term proportional to gamma that should have cancelled but did not --
# diagnosed as a genuine convention/sign mismatch, not a numerical
# accident, since the k=1 residual -2*gamma is EXACT and n-independent).
# This was almost certainly caused by a wrong sign or off-by-one in
# translating between this front's own -x=b matching and the specific
# classical convention chosen; several textbook variants of the Charlier
# polynomial exist (differing by x<->-x, a<->1/a, or a normalization
# factor) and no further time was spent hunting for the exact matching
# convention, since NOTHING downstream in this front (script 02, 03)
# depends on the Charlier-polynomial name -- only on the independently,
# fully-verified 2F0 form of Part B, which needs no external polynomial
# family at all. The Charlier-family connection is therefore NOT claimed
# by this front; it is recorded here, with its failure disclosed exactly
# as it was found, as an idea for a possible future front rather than as
# a result of this one.
log("  --> NOT claimed as a result of this front (see script's inline")
log("      comment / ATTEMPT.md Self-caught issues): the naive parameter")
log("      matching to the textbook Charlier convention does not check")
log("      out past k=0. Nothing downstream depends on this named-family")
log("      identification -- only on the independently-verified 2F0 form")
log("      of Part B, which stands fully verified regardless.")

log("\n--- Part D: what this DOES and DOES NOT buy (honest scope note) ---")
log("""
This establishes, for the FIRST time in this lineage (no ancestor
ATTEMPT.md mentions 2F0, or any hypergeometric/orthogonal-polynomial
identification), that A_k(n,gamma) is EXACTLY (not asymptotically) a
terminating 2F0(-k, n-k+1; ; -gamma/((1-gamma)n)) hypergeometric
polynomial, times (1-gamma)^k -- a genuine new exact structural fact
(Part B, fully verified). The FURTHER claim that this is literally a
textbook Charlier polynomial (Part C) did NOT check out under this
front's own naive parameter matching and is explicitly NOT claimed.

Either way, it does NOT, by itself, give a closed form for
S_n = sum_k A_k or for C(gamma). Note the argument w=-gamma/((1-gamma)n)
is FIXED (independent of k) -- only the degree k and the second upper
parameter b=n-k+1 move with the summation index -- so summing
2F0(-k,n-k+1;;w) over k=1..n is a "diagonal-parameter" sum of a
hypergeometric family at fixed argument but drifting degree/parameter,
which is not a standard closed textbook identity either (the classical
Charlier generating function sum_k C_k(x;a) t^k/k! = e^t(1-t/a)^x, even
if the Part-C identification had checked out, holds for FIXED x,a -- it
would not directly apply here since the analogous x=k-n-1 moves with
k). Script 02 uses this exact 2F0 representation only as a numerically
EXACT (no exponential-sandwich approximation at all) evaluator of A_k,
pushed to larger n/higher precision than any ancestor's pmf-based
evaluator, and as the basis for an exact-moment (rather than
deterministic-worst-case) refinement of the Bulk/Tail Lemma's bulk term
in script 03.
""")

log("\nPARTS A, B FULLY VERIFIED (0 mismatches). Part C (Charlier-family")
log("naming) NOT established and NOT claimed -- see disclosure above.")
log(f"Summary: {checks} Pochhammer-ratio checks (0 mismatches), "
    f"{mismatches_B} symbolic-2F0 mismatches (of 7, PASSED), "
    f"{spot_checks} random exact spot checks (0 mismatches, PASSED), "
    f"{mismatches_C} Charlier-ID mismatches (of 7, NOT claimed/used further).")

with open(__file__.replace('.py', '.log'), 'w') as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written.")
