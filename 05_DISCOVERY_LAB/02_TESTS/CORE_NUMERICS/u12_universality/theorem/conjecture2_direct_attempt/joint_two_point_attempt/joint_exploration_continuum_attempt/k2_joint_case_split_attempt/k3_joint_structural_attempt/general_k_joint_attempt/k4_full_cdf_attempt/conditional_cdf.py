"""
K4-FULL-CDF-ATTEMPT: the exact closed-form conditional CDF given
(L0,L1,L2,L3) (Section 3 of ATTEMPT.md), plus a slow-but-exact O(n^4)
reference engine (full_cdf_exact) built ENTIRELY from Proposicao S (cited,
Estagio 41) + the Full Cycle-Count Decomposition Theorem (cited) via
direct nested composition-simplex enumeration with an INCLUSION-EXCLUSION
lattice-count formula -- a route genuinely independent of the "shift
trick" swap-of-summation-order method used in symbolic_derivation_full_cdf.py
/ assemble_regimes.py, used here purely as a cross-check, not as an input
to that derivation.
"""
from fractions import Fraction
from math import comb
import itertools

K = 4


def count_le(bounds, t):
    """#{(v_1,...,v_d): 1<=v_i<=bounds[i], sum v_i <= t}, via inclusion-
    exclusion (independently re-derived and verified in this front's own
    scratch testing; a standard combinatorial fact, not cited from any
    other front's code)."""
    d = len(bounds)
    total = 0
    for mask in range(1 << d):
        bits = bin(mask).count('1')
        sub = sum(bounds[i] for i in range(d) if mask & (1 << i))
        N = t - d - sub
        if N >= 0:
            val = comb(N + d, d)
        else:
            val = 0
        total += (-1) ** bits * val
    return total


def clip(t, L):
    return max(0, min(t, L))


def cond_cdf(n, k, L):
    """P(T<=k | L0,L1,L2,L3) exactly, via the 16-subset sum of Proposicao
    S (general K, CITED) times the elementary |A|-fold lattice count
    (Section 3 of ATTEMPT.md)."""
    O = n - sum(L)
    assert O >= 0
    t = k - O
    total = Fraction(0)
    for r in range(K + 1):
        for A in itertools.combinations(range(K), r):
            m = len(A)
            fact = 1
            for j in range(1, m + 1):
                fact *= j
            prod = 1
            for a in A:
                prod *= Fraction(L[a], n)
            ssum = sum(Fraction(L[a], n) for a in A)
            pD = Fraction(O, n)
            PA = fact * prod * (pD + ssum)
            if PA == 0:
                continue
            if m == 0:
                indicator = 1 if O <= k else 0
                total += PA * indicator
            else:
                bounds = [L[a] for a in A]
                cnt = count_le(bounds, t)
                denom = 1
                for b in bounds:
                    denom *= b
                total += PA * Fraction(cnt, denom)
    return total


def full_cdf_exact(n, k):
    """Slow-but-exact O(n^4)-ish reference engine: average cond_cdf(n,k,L)
    over the ENTIRE composition simplex (L0,L1,L2,L3 each >=1, sum<=n),
    each composition equally likely (1/C(n,4)).  Built from Sections 2-3's
    proved machinery ONLY -- never uses Proposicao D4's own closed form
    at any point."""
    total = Fraction(0)
    n_comps = 0
    for L0 in range(1, n - 2):
        for L1 in range(1, n - L0 - 1):
            for L2 in range(1, n - L0 - L1):
                L3max = n - L0 - L1 - L2
                for L3 in range(1, L3max + 1):
                    L = (L0, L1, L2, L3)
                    n_comps += 1
                    total += cond_cdf(n, k, L)
    return total / n_comps, n_comps


if __name__ == "__main__":
    # Part A: cond_cdf vs the position-level reduced model of
    # decomposition_theorem.py, at every k=0..n, several (n,L).
    from decomposition_theorem import reduced_model_pmf

    print("=" * 78)
    print("PART A: conditional CDF closed form vs position-level reduced model")
    print("=" * 78)
    configs = [
        (7, (1, 1, 1, 1)),
        (8, (2, 1, 1, 1)),
        (8, (1, 2, 1, 2)),
        (9, (2, 2, 1, 1)),
    ]
    all_ok = True
    for n, L in configs:
        reduced = reduced_model_pmf(n, L)
        O = n - sum(L)
        # build cdf of T from reduced pmf (over (S,V) -> T=O+sum(V))
        Tpmf = {}
        for (S, V), pr in reduced.items():
            Tval = O + sum(V)
            Tpmf[Tval] = Tpmf.get(Tval, Fraction(0)) + pr
        mism = 0
        for k in range(0, n + 1):
            expected = sum(pr for Tval, pr in Tpmf.items() if Tval <= k)
            got = cond_cdf(n, k, L)
            if expected != got:
                mism += 1
                print(f"    MISMATCH n={n} L={L} k={k}: reduced={expected} formula={got}")
        ok = (mism == 0)
        all_ok &= ok
        print(f"  n={n} L={L}: k=0..{n}, mismatches={mism}  {'OK' if ok else 'FAIL'}")
    print("Conditional CDF CONFIRMED." if all_ok else "FAILED.")

    print()
    print("=" * 78)
    print("PART B: full_cdf_exact (O(n^4) reference engine) self-sanity")
    print("=" * 78)
    for n in (6, 7):
        vals = [full_cdf_exact(n, k)[0] for k in range(n + 1)]
        print(f"  n={n}: F(0..{n}) = {vals}")
        assert vals[-1] == 1, "F(n) must equal 1"
        assert vals[0] == 0 or n < 4, "F(0) must be 0 for n>=4"
        for i in range(len(vals) - 1):
            assert vals[i] <= vals[i + 1], "F must be nondecreasing"
    print("full_cdf_exact sanity checks passed (F(0)=0, F(n)=1, nondecreasing).")
