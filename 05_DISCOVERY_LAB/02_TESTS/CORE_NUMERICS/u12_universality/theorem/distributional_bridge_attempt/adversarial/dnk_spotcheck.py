"""
Independent spot-check of D(n,K) := max_k |F_n^{(K)}(k/n) - F_K(k/n)|,
ATTEMPT.md Sec 7.1(d) table, for two cells: (n=6,K=2) and (n=4,K=3).

Same brute-force Definition-4 model as brute_generalK.py, but this script
is self-contained (re-implements the enumeration) and only computes the
full T-pmf, then the sup-CDF-discrepancy against F_K(x)=1-(1-x^2)^K.
Exact Fraction arithmetic throughout.
"""
import sys, os, itertools, math
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cyclic import cyclic_mask


def Tcounts_for(n, K):
    idx = list(range(n))
    Tcounts = {}
    for pi in itertools.permutations(idx):
        for U in itertools.product(range(n), repeat=K):
            f = list(U) + [pi[i] for i in range(K, n)]
            T = sum(cyclic_mask(f))
            Tcounts[T] = Tcounts.get(T, 0) + 1
    return Tcounts


def D_of(n, K):
    Tcounts = Tcounts_for(n, K)
    total = math.factorial(n) * n ** K
    assert sum(Tcounts.values()) == total
    cum = 0
    D = Fraction(0)
    for k in range(0, n + 1):
        cum += Tcounts.get(k, 0)
        Fn = Fraction(cum, total)
        x = Fraction(k, n)
        FK = 1 - (1 - x ** 2) ** K
        diff = abs(Fn - FK)
        if diff > D:
            D = diff
    return D


def main():
    # ATTEMPT.md Sec 7.1(d) table values being spot-checked:
    #   D(6,2) reported as 0.0958
    #   D(4,3) reported as 0.0740
    targets = {(6, 2): 0.0958, (4, 3): 0.0740}
    for (n, K), doc_decimal in targets.items():
        D = D_of(n, K)
        dec = float(D)
        print(f"n={n} K={K}  D(n,K) exact={D}  decimal={dec:.4f}  "
              f"ATTEMPT.md table={doc_decimal:.4f}  "
              f"{'MATCH' if abs(dec - doc_decimal) < 5e-5 else 'MISMATCH <<<<'}")


if __name__ == "__main__":
    main()
