"""
K3-FULL-CDF-ATTEMPT -- Step 2: the exact conditional CDF of T given the
governing-source arc-length composition (L0,L1,L2), in closed form.

Built on decomposition_theorem.py's Full Cycle-Count Decomposition
Theorem: T = O + sum_{s in S} V_s, S the random cyclic-source subset with
proven P(S=A) formulas, and (V_s)_{s in S} conditionally independent,
V_s ~ Uniform{1,...,L_s}.

This gives, for each of the 8 possible cyclic-source subsets A, an EXACT,
closed-form (piecewise via clip/min) contribution to P(T<=k | L0,L1,L2):

  A = empty       : T = O deterministically.           P(T<=k|A) = [O<=k]
  A = {s}         : T = O + V_s, V_s ~ Unif(1..L_s).    P(T<=k|A) = clip(k-O,0,L_s)/L_s
  A = {s,t}       : T = O + V_s + V_t, independent.     P(T<=k|A) = paircount(L_s,L_t,k-O)/(L_s L_t)
  A = {0,1,2}     : T = O + V_0+V_1+V_2, independent.   P(T<=k|A) = triplecount(L0,L1,L2,k-O)/(L0 L1 L2)

where paircount/triplecount are the elementary (standard, provable by
direct counting -- see docstrings below) lattice-point counts of the
number of ways to write a given sum as v+w (resp. v+w+u) with each
variable ranging over its own {1,...,L} range.

Combined with the (already-proven) P(S=A|L) formulas, this gives the
FULL closed-form conditional CDF

  P(T<=k | L0,L1,L2) = P(empty|L)*[O<=k]
                       + sum_s P({s}|L) * clip(k-O,0,L_s)/L_s
                       + sum_{s<t} P({s,t}|L) * paircount(L_s,L_t,k-O)/(L_s L_t)
                       + P({0,1,2}|L) * triplecount(L0,L1,L2,k-O)/(L0 L1 L2)

-- a genuine, PROVED closed form (no fitting anywhere in this file),
conditional on the arc-length composition. This is the K=3 analogue of
Proposition D1's Lemma D1.0 (K=1's "conditional CDF given the mark's arc
length L").

Note the L_s in the denominators of each term cancel exactly against the
L_s numerator in the corresponding P(A|L) formula -- see
symbolic_derivation_full_cdf.py, which exploits this cancellation to sum
this conditional formula in closed form over the entire composition
simplex (proving the fully unconditional Proposicao D3).
"""
from fractions import Fraction


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def pair_count_le(L0, L1, m):
    """#{(v,w) : 1<=v<=L0, 1<=w<=L1, v+w<=m}, exact elementary count.
    (Standard lattice-point count under a line in a rectangle; proved
    directly by summing, for each v, the number of admissible w.)"""
    if m < 2:
        return 0
    vmax = min(L0, m - 1)
    if vmax < 1:
        return 0
    v0 = min(m - L1, vmax)  # for v<=v0: full L1 available; else m-v
    total = 0
    if v0 >= 1:
        total += v0 * L1
    for v in range(max(1, v0 + 1), vmax + 1):
        total += (m - v)
    return total


def triple_count_le(L0, L1, L2, m):
    """#{(v,w,u): 1<=v<=L0,1<=w<=L1,1<=u<=L2, v+w+u<=m}, exact elementary
    count (reduces to a sum of pair_count_le, by fixing v)."""
    total = 0
    vmax = min(L0, m - 2)
    for v in range(1, vmax + 1):
        total += pair_count_le(L1, L2, m - v)
    return total


def P_T_le_k_given_L(L0, L1, L2, n, k):
    """The exact, PROVED closed-form conditional CDF P(T<=k | L0,L1,L2),
    built directly from the Decomposition Theorem (decomposition_theorem.py)
    -- no enumeration over U_0,U_1,U_2 here at all, just the closed-form
    per-pattern contributions."""
    O = n - L0 - L1 - L2
    Ls = [L0, L1, L2]
    total = Fraction(0)

    if O <= k:
        total += Fraction(O, n)

    for s in range(3):
        Ls_s = Ls[s]
        c = clip(k - O, 0, Ls_s)
        total += Fraction(Ls_s + O, n ** 2) * c

    for s, t, u in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        Lu = Ls[u]
        cnt = pair_count_le(Ls[s], Ls[t], k - O)
        total += Fraction(2 * (n - Lu), n ** 3) * cnt

    cnt3 = triple_count_le(L0, L1, L2, k - O)
    total += Fraction(6, n ** 3) * cnt3

    return total


def full_cdf_exact(n, k):
    """Unconditional P(T<=k), by exact averaging of P_T_le_k_given_L over
    the uniform composition simplex (L0,L1,L2>=1, L0+L1+L2<=n) -- an
    O(n^3)-time, exact-Fraction computation (no floating point, no
    sampling). This is the reference "slow but exact and provably
    correct" engine used to discover and to cross-check the closed form
    in symbolic_derivation_full_cdf.py / find_and_verify_closed_form.py."""
    from math import comb
    total = Fraction(0)
    ncomp = 0
    for L0 in range(1, n - 1):
        for L1 in range(1, n - L0):
            for L2 in range(1, n - L0 - L1 + 1):
                ncomp += 1
                total += P_T_le_k_given_L(L0, L1, L2, n, k)
    assert ncomp == comb(n, 3)
    return total / ncomp


if __name__ == "__main__":
    # Cross-check this conditional-CDF engine against the position-level
    # reduced model of decomposition_theorem.py, at several (L,n).
    from decomposition_theorem import reduced_model_pmf_given_L

    print("Verifying conditional CDF closed form against position-level model:")
    tests = [(2, 3, 4, 12), (1, 1, 1, 6), (5, 2, 3, 15), (7, 1, 2, 25)]
    all_ok = True
    for L0, L1, L2, n in tests:
        pmf = reduced_model_pmf_given_L(L0, L1, L2, n)
        cum = Fraction(0)
        ok = True
        for k in range(0, n + 1):
            cum += pmf.get(k, Fraction(0))
            cf = P_T_le_k_given_L(L0, L1, L2, n, k)
            if cf != cum:
                ok = False
                print(f"    MISMATCH L=({L0},{L1},{L2}) n={n} k={k}: {cf} vs {cum}")
        all_ok &= ok
        print(f"  L=({L0},{L1},{L2}) n={n}: {'MATCH (all k)' if ok else 'MISMATCH FOUND'}")
    assert all_ok
    print("  Conditional CDF closed form CONFIRMED.\n")

    print("Sample of the unconditional exact CDF (slow O(n^3) reference engine):")
    for n in (6, 10):
        print(f"  n={n}:", [str(full_cdf_exact(n, k)) for k in range(0, n + 1)])
