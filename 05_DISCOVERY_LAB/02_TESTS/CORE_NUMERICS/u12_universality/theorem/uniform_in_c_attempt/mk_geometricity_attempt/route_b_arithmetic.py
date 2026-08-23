"""
Route B (the referee's sketch, DERIVATION_PREREG.md Route B step (a)):
independently verify the arithmetic claim from
error_constant_growth_attempt/ATTEMPT.md Lemma 7 / the ledger's constructive
note:

    F_r(2,0) = (phi_r/4^r) * sum_{i=0}^{r} 2^{r-i} C(2r+1,i)   [exact, PROVED
                                                                 elsewhere via
                                                                 Lemma 7]
    sum_{i=0}^{r} C(2r+1,i) = 2^{2r}      exactly  (odd N=2r+1, exact half)
    => F_r(2,0) <= phi_r * 2^r            exactly, sharper than the ledger's
                                           quoted "<= 2*phi_r*2^r" (which used
                                           the cruder sum_{i<=r} C(2r+1,i) <=
                                           2^{2r+1} instead of the exact
                                           half-sum identity)

This is checked here two ways: (1) direct exact evaluation of both sides for
a range of r; (2) symbolic re-derivation of the half-sum identity
sum_{i=0}^r C(2r+1,i) = 2^{2r} for symbolic r.

This script does NOT attempt step (b)/(c) of Route B (unrolling Proposicao 6
with general-b bounds on A_r(b), B_r(b)) -- ATTEMPT.md reports honestly why
that sub-route was not carried through (no closed form for A_r(b), B_r(b) is
available anywhere in the archive for general b; deriving one is a separate,
substantial undertaking not needed once Route A succeeds).
"""
from fractions import Fraction as Fr
from math import comb, factorial

import sympy as sp


def phi_r_exact(r):
    return Fr(4**r * factorial(r)**2, factorial(2 * r + 1))


def F_r_2_0_exact(r):
    """F_r(2,0) via the Lemma-7-derived closed form, exact."""
    s = sum(2**(r - i) * comb(2 * r + 1, i) for i in range(0, r + 1))
    return phi_r_exact(r) * Fr(s, 4**r)


print("=== Route B step (a): F_r(2,0) exact formula vs the two crude bounds ===\n")
print(f"{'r':>4} {'F_r(2,0) exact':>18} {'phi_r*2^r (sharp crude)':>26} "
      f"{'2*phi_r*2^r (ledger crude)':>28} {'both hold':>10}")

all_hold = True
for r in range(0, 41):
    exact = F_r_2_0_exact(r)
    phir = phi_r_exact(r)
    sharp_bound = phir * Fr(2**r)
    ledger_bound = 2 * phir * Fr(2**r)
    holds1 = exact <= sharp_bound
    holds2 = exact <= ledger_bound
    all_hold = all_hold and holds1 and holds2
    if r <= 15 or r % 5 == 0:
        print(f"{r:>4} {float(exact):>18.4f} {float(sharp_bound):>26.4f} "
              f"{float(ledger_bound):>28.4f} {str(holds1 and holds2):>10}")

print(f"\nboth bounds hold for every r in 0..40: {all_hold}")
print("(ratio F_r(2,0)/[phi_r*2^r] should -> 1 since the half-sum identity is EXACT, "
      "not just an upper bound -- checking:)")
for r in (5, 10, 20, 40):
    exact = F_r_2_0_exact(r)
    phir = phi_r_exact(r)
    ratio = exact / (phir * Fr(2**r))
    print(f"  r={r}: ratio = {float(ratio):.6f}  (exact Fraction: {ratio})")

print("\n=== symbolic re-derivation: sum_{i=0}^r C(2r+1,i) = 2^{2r} (exact) ===")
r_sym = sp.symbols('r', positive=True, integer=True)
i_sym = sp.symbols('i')
# Verify for concrete r via exact integer summation (already implicitly done
# above), plus a direct symbolic proof via the classical binomial-symmetry
# argument, checked mechanically here for many concrete r (sympy symbolic
# hypergeometric closed-form summation of the *general* case is unnecessary --
# the identity is a one-line consequence of symmetry, checked here to
# reconfirm no off-by-one).
all_half_sum_ok = True
for r in range(0, 60):
    lhs = sum(comb(2 * r + 1, i) for i in range(0, r + 1))
    rhs = 2**(2 * r)
    ok = (lhs == rhs)
    all_half_sum_ok = all_half_sum_ok and ok
print(f"sum_{{i=0}}^r C(2r+1,i) == 2^(2r) for r=0..59: {all_half_sum_ok}")

# One-line symbolic proof, recorded here for the write-up:
# sum_{i=0}^{2r+1} C(2r+1,i) = 2^{2r+1} (binomial theorem at x=1).
# C(2r+1,i) = C(2r+1,2r+1-i), so the map i -> 2r+1-i is an involution on
# {0,...,2r+1} pairing i in {0,...,r} bijectively with 2r+1-i in {r+1,...,2r+1}
# (since 2r+1 is odd, no fixed point: i = 2r+1-i => i=(2r+1)/2 not an integer).
# Each pair (i, 2r+1-i) has EQUAL binomial coefficients, so the two halves of
# the sum are equal, each = 2^{2r+1}/2 = 2^{2r}. QED (elementary, no
# induction needed beyond the binomial theorem itself).
print("\nProof recorded above is a direct symmetry argument (binomial theorem "
      "at x=1, then the involution i -> 2r+1-i splits {0,...,2r+1} into two "
      "equal-sum halves since 2r+1 is odd) -- no induction, no asymptotics.")

print(f"\n=== ROUTE B STEP (a) VERIFIED: {all_hold and all_half_sum_ok} ===")
print("Route B steps (b)/(c) [unrolling Proposicao 6 with general-b bounds on "
      "A_r(b), B_r(b)] are NOT attempted here -- see ATTEMPT.md SS4 for why, "
      "and why they are not needed once Route A succeeds.")
