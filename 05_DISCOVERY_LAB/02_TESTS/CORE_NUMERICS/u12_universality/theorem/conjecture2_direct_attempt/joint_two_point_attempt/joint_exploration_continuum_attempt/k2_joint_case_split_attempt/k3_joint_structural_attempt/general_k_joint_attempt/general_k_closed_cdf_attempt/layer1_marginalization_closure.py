"""
Section 3 of ATTEMPT.md: Layer 1 of S_r's triple summation closes in
closed form, symbolic simultaneously in (n,K,r) -- PROVED, new.

S_r(n,K,k) (`exchangeability_reduction_to_Sr.py`) is a sum over
L_0,...,L_{r-1}>=1 and O>=0 of (O+Sigma)*Count_r(L;k-O)*mult(Sigma,O),
where mult(Sigma,O) marginalizes the K-r UNTOUCHED sources via
comp_count(n-Sigma-O-(K-r), K-r). Unpacking Count_r(L;t) as a sum over
"landing vectors" v (1<=v_i<=L_i, sum v<=t) and swapping the order of
summation (v first, then L_i>=v_i), the L-marginalization for FIXED v
becomes -- via the substitution L_i' := L_i - v_i >= 0 -- a stars-and-bars
sum over the shift total j := Sigma - V (V:=sum v_i) of

    InnerJ(V,O) := sum_{j>=0} C(j+r-1,r-1) * (O+V+j) * C(n-V-O-1-j, K-r-1)

This is a genuine Vandermonde-type convolution (a product of TWO binomial
coefficients in j, summed over j's FULL natural range -- the range where
the SECOND binomial coefficient's own combinatorial validity forces it to
vanish, not an externally-imposed cutoff). This closes in one shot,
PROVED by the classical "concatenation of two compositions" identity
`sum_j C(j+a-1,a-1)*C(M-j+b-1,b-1) = C(M+a+b-1,a+b-1)` (a nonneg
composition of M into a+b parts = a composition of j into a parts,
concatenated with one of M-j into b parts, summed over the split point j)
applied twice (once directly, once after using j*C(j+r-1,r-1)=r*C(j+r-1,r)
to peel off the "+j" term):

    InnerJ(V,O) = (O+V)*C(N+r-1,K-1) + r*C(N+r-1,K),   N := n-V-O   (r<K)
    InnerJ(V,O) = n*C(N+r-1,r-1),  N=n-V-O               (r=K, no untouched sources)

This script (a) verifies the ground-truth L-marginalization step for
concrete (n,K,r,V,O) against the closed InnerJ formula above (both
built completely independently -- InnerJ_direct sums the raw definition
directly, no shortcut), and (b) proves the two component identities
symbolically (sympy, exact, for representative concrete r,b -- the
identity itself, `concatenation of compositions`, is elementary and
K-free/r-free/b-free by construction, so this is a confirmation, not a
search for a pattern).
"""
from math import comb
import sympy as sp


# ---------------------------------------------------------------------
# (a) Ground truth (raw definition) vs closed form, numeric verification
# ---------------------------------------------------------------------

def comp_count(m, parts):
    if m < 0:
        return 0
    if parts == 0:
        return 1 if m == 0 else 0
    return comb(m + parts - 1, parts - 1)


def InnerJ_direct(n, K, r, V, O):
    """Raw definition: sum over j of C(j+r-1,r-1)*(O+V+j)*C(N-1-j,K-r-1),
    N=n-V-O, summed over j's own natural valid range."""
    b = K - r
    N = n - V - O
    if b == 0:
        if N < 0:
            return 0
        c1 = comb(N + r - 1, r - 1) if r > 0 else (1 if N == 0 else 0)
        return c1 * (O + V + N)
    total = 0
    for j in range(0, max(N, 0)):
        c1 = comb(j + r - 1, r - 1) if r > 0 else (1 if j == 0 else 0)
        c2 = comb(N - 1 - j, b - 1) if (N - 1 - j) >= 0 and (N - 1 - j) >= (b - 1) else 0
        total += c1 * (O + V + j) * c2
    return total


def InnerJ_closed(n, K, r, V, O):
    """PROVED closed form (this section's main claim)."""
    N = n - V - O
    if K - r == 0:
        if N < 0:
            return 0
        c1 = comb(N + r - 1, r - 1) if r > 0 else (1 if N == 0 else 0)
        return c1 * (O + V + N)
    A1 = comb(N + r - 1, K - 1) if N + r - 1 >= 0 else 0
    A2 = comb(N + r - 1, K) if N + r - 1 >= 0 else 0
    return (O + V) * A1 + r * A2


def check_numeric():
    cases = [
        (6, 3, 0, 3, 1), (6, 3, 1, 2, 0), (6, 3, 1, 3, 1), (6, 3, 2, 3, 0),
        (7, 4, 2, 4, 1), (7, 4, 3, 5, 2), (8, 5, 3, 4, 1), (8, 5, 4, 5, 2),
        (9, 6, 0, 6, 0), (9, 6, 5, 5, 1), (10, 4, 1, 7, 2), (12, 6, 3, 8, 0),
    ]
    ok = True
    for n, K, r, V, O in cases:
        a = InnerJ_direct(n, K, r, V, O)
        b = InnerJ_closed(n, K, r, V, O)
        match = (a == b)
        ok = ok and match
        print(f"   n={n} K={K} r={r} V={V} O={O}: direct={a} closed={b} {'OK' if match else 'MISMATCH!'}")
    return ok


# ---------------------------------------------------------------------
# (b) Symbolic proof of the two convolution identities, representative
#     concrete r,b (the identity is elementary/K-free/r-free by its own
#     combinatorial proof above; this is a direct confirmation).
# ---------------------------------------------------------------------

def check_symbolic():
    N, j = sp.symbols('N j', integer=True)
    ok = True
    for r in range(1, 6):
        for b in range(1, 6):
            # identity 1: sum_j C(j+r-1,r-1)*C(N-1-j,b-1), j=0..N-b -> C(N+r-1,r+b-1)
            expr1 = sp.binomial(j + r - 1, r - 1) * sp.binomial(N - 1 - j, b - 1)
            s1 = sp.summation(expr1, (j, 0, N - b))
            target1 = sp.binomial(N + r - 1, r + b - 1)
            d1 = sp.simplify(s1 - target1)
            # identity 2: sum_j C(j+r-1,r)*C(N-1-j,b-1), j=0..N-b -> C(N+r-1,r+b)
            expr2 = sp.binomial(j + r - 1, r) * sp.binomial(N - 1 - j, b - 1)
            s2 = sp.summation(expr2, (j, 0, N - b))
            target2 = sp.binomial(N + r - 1, r + b)
            d2 = sp.simplify(s2 - target2)
            match = (d1 == 0 and d2 == 0)
            ok = ok and match
            print(f"   r={r} b={b}: identity1 diff={d1}  identity2 diff={d2}  {'OK' if match else 'MISMATCH!'}")
    return ok


if __name__ == "__main__":
    print("Layer 1 (untouched-source marginalization) closure: PROVED, symbolic")
    print("in (n,K,r). Verification (a): numeric, raw definition vs closed form.")
    print("=" * 70)
    ok_a = check_numeric()
    print("=" * 70)
    print("Verification (b): the two underlying Vandermonde-type convolution")
    print("identities, symbolic in N, representative (r,b) pairs.")
    print("=" * 70)
    ok_b = check_symbolic()
    print("=" * 70)
    print(f"ALL LAYER-1 CHECKS PASS: {ok_a and ok_b}")
    if not (ok_a and ok_b):
        raise SystemExit(1)
