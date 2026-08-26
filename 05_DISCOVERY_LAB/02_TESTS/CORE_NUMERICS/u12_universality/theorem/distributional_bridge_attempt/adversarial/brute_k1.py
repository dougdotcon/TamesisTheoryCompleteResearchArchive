"""
Independent, from-scratch brute-force check of Proposition D1 (K=1 exact
finite-n CDF) against the ATTEMPT.md-claimed closed form
    P(M_n^{(1)} <= k/n) = k(k+1)/n^2 ,  k=0,...,n-1.

Model (Definition 4, K=1): rerouted index fixed WLOG at index 0 (0-indexed
here; index "1" in the document's 1-indexing). pi ranges over all n!
permutations of {0,...,n-1} (uniform), U ranges over all n choices in
{0,...,n-1} (uniform, independent of pi). Every (pi, U) pair equally likely,
n!*n total configurations. f(0) = U, f(i) = pi(i) for i = 1,...,n-1.

Exact rational (Fraction) arithmetic throughout -- no floating point.
"""
import sys, os, itertools
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cyclic import count_cyclic

def brute_k1_cdf_counts(n):
    """Return dict k -> exact integer count of configurations with T=k,
    over all n!*n configurations (pi in S_n, U in [n])."""
    counts = {}
    idx = list(range(n))
    for pi in itertools.permutations(idx):
        for U in range(n):
            f = [U] + [pi[i] for i in range(1, n)]
            T = count_cyclic(f)
            counts[T] = counts.get(T, 0) + 1
    return counts

def main():
    import math
    print("n | k | brute P(T<=k) | claimed k(k+1)/n^2 | match")
    all_ok = True
    for n in range(2, 10):  # n=2..9 (task asked for n=2..8 at least; pushed one further)
        counts = brute_k1_cdf_counts(n)
        total = n * math.factorial(n)
        assert sum(counts.values()) == total
        cum = 0
        for k in range(0, n + 1):
            cum += counts.get(k, 0)
            brute_p = Fraction(cum, total)
            if k <= n - 1:
                claimed = Fraction(k * (k + 1), n * n)
            else:
                claimed = Fraction(1, 1)
            ok = (brute_p == claimed)
            all_ok = all_ok and ok
            print(f"n={n} k={k:2d}  brute={brute_p!s:>12}  claimed={claimed!s:>12}  {'OK' if ok else 'MISMATCH <<<<<'}")

        # Corollary D1.2 (second moment) and E[T] (THEOREM.md Prop 4) cross-check,
        # both from the same brute pmf, independent of Proposition D1's own proof.
        ET = sum(Fraction(c, total) * k for k, c in counts.items())
        ET2 = sum(Fraction(c, total) * k * k for k, c in counts.items())
        claimed_ET = Fraction(2 * n, 3) + Fraction(1, 3 * n)
        claimed_ET2 = Fraction((n - 1) ** 2, 2) + n
        ok_ET = (ET == claimed_ET)
        ok_ET2 = (ET2 == claimed_ET2)
        all_ok = all_ok and ok_ET and ok_ET2
        print(f"      E[T] brute={ET} claimed(THEOREM.md Prop4, x n)={claimed_ET}  {'OK' if ok_ET else 'MISMATCH <<<<'}")
        print(f"      E[T^2] brute={ET2} claimed(Cor D1.2, x n^2)={claimed_ET2}  {'OK' if ok_ET2 else 'MISMATCH <<<<'}")
    print()
    print("ALL MATCH" if all_ok else "MISMATCH FOUND")

if __name__ == "__main__":
    main()
