"""
Compares Proposition S's UNCONDITIONAL P(S=A) -- i.e. averaged over the
random governing-source arc-length composition (L_0,...,L_{K-1},O), using
the Governing-Source Reindexing fact (Estagio 38, general-K, PROVED, cited)
that the GAP vector (g_0,...,g_{K-1},O) -- not L directly -- is uniform
over compositions of n-K into K+1 nonnegative parts, with L_s := g_s + 1 --
against the true Definition-4 brute-force empirical values produced by
true_bruteforce_definition4_general_k.py.

The empirical target values below are transcribed directly from that
script's own log (true_bruteforce_definition4_general_k.log), which was
produced independently (own arc-reconstruction code, no formula assumed).

No code from any other front in this lineage was read or used.
"""
from fractions import Fraction
import itertools


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for i in range(total + 1):
        for rest in compositions(total - i, parts - 1):
            yield (i,) + rest


def prop_s(A, L, O, n):
    m = len(A)
    fact = 1
    for i in range(1, m + 1):
        fact *= i
    prod = Fraction(1)
    for a in A:
        prod *= Fraction(L[a], n)
    PA = sum(Fraction(L[a], n) for a in A)
    pD = Fraction(O, n)
    return fact * prod * (pD + PA)


def predicted_unconditional(K, n):
    """(g_0,...,g_{K-1}, O) uniform over compositions of n-K into K+1
    nonnegative parts (Governing-Source Reindexing, Estagio 38, cited);
    L_s := g_s + 1."""
    comps = list(compositions(n - K, K + 1))
    w = Fraction(1, len(comps))
    out = {}
    for A in itertools.chain.from_iterable(
        itertools.combinations(range(K), r) for r in range(K + 1)
    ):
        A = frozenset(A)
        total = Fraction(0)
        for comp in comps:
            g = comp[:K]
            O = comp[K]
            L = tuple(gi + 1 for gi in g)
            total += prop_s(A, L, O, n)
        out[A] = total * w
    return out


# Empirical P(S=A), transcribed exactly from
# true_bruteforce_definition4_general_k.log (own, from-scratch true
# Definition-4 brute force -- arcs reconstructed from pi, cyclicity from
# direct functional-graph traversal of f, NOT from any formula).
EMPIRICAL = {
    (4, 1): {(): Fraction(3, 8), (0,): Fraction(5, 8)},
    (5, 2): {(): Fraction(1, 5), (0,): Fraction(13, 50), (1,): Fraction(13, 50),
             (0, 1): Fraction(7, 25)},
    (6, 3): {(): Fraction(1, 8), (0,): Fraction(49, 360), (1,): Fraction(49, 360),
             (2,): Fraction(49, 360), (0, 1): Fraction(7, 60), (0, 2): Fraction(7, 60),
             (1, 2): Fraction(7, 60), (0, 1, 2): Fraction(7, 60)},
    (6, 4): {(): Fraction(1, 15), (0,): Fraction(7, 90), (1,): Fraction(7, 90),
             (2,): Fraction(7, 90), (3,): Fraction(7, 90),
             (0, 1): Fraction(8, 135), (0, 2): Fraction(8, 135), (0, 3): Fraction(8, 135),
             (1, 2): Fraction(8, 135), (1, 3): Fraction(8, 135), (2, 3): Fraction(8, 135),
             (0, 1, 2): Fraction(19, 360), (0, 1, 3): Fraction(19, 360),
             (0, 2, 3): Fraction(19, 360), (1, 2, 3): Fraction(19, 360),
             (0, 1, 2, 3): Fraction(1, 18)},
}


def main():
    print("=" * 78)
    print("Unconditional Proposition S vs. true Definition-4 brute force")
    print("=" * 78)
    all_ok = True
    for (n, K), emp in EMPIRICAL.items():
        pred = predicted_unconditional(K, n)
        for Atuple, empval in emp.items():
            A = frozenset(Atuple)
            predval = pred[A]
            ok = (predval == empval)
            all_ok &= ok
            print(f"n={n} K={K} A={sorted(A)}: predicted={predval} "
                  f"empirical={empval}  [{'OK' if ok else 'MISMATCH'}]")
    print()
    print("ALL MATCH" if all_ok else "MISMATCH FOUND")


if __name__ == "__main__":
    main()
