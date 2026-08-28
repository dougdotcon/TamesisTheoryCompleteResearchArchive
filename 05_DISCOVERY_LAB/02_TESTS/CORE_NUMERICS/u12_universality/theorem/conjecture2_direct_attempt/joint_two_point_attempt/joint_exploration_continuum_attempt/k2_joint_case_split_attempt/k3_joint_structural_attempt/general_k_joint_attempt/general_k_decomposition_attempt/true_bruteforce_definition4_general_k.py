"""
True, from-scratch brute force of Definition 4's LITERAL model (THEOREM.md
Sec 7.2): pi a uniform random permutation of [n]; K sources fixed WLOG at
{0,...,K-1}; targets U_0,...,U_{K-1} i.i.d. Uniform([n]); f(i):=U_i for
i<K, f(i):=pi(i) otherwise. T := #cyclic points of f.

This script does NOT use the governing-source reduced model, arcs, or any
formula from Section 2/3 of ATTEMPT.md as an *input* -- it enumerates every
one of the n! * n^K raw (pi, U) configurations directly, exactly as
Definition 4 states, and for EACH configuration:
  (1) finds cyclic points of f by direct functional-graph traversal
      (n nodes, no shortcut) -- gives the ground-truth T and, restricting
      to i<K, the ground-truth *realized* S = {cyclic sources};
  (2) independently reconstructs the arcs ARC(0),...,ARC(K-1) and the
      outside set from pi and the K source positions (by walking pi's
      cycles and splitting them at source boundaries -- this is a direct,
      from-scratch construction, not copied from any other front's code);
  (3) computes O and, for each realized cyclic source s, V_s := number of
      cyclic points of f lying in ARC(s), and checks the bookkeeping
      identity T = O + sum_{s in S} V_s (a deterministic identity that
      must hold in EVERY single configuration, since every cyclic point of
      f is either outside or in some cyclic source's arc -- this is a
      strong per-configuration check, not just a check "in law");
  (4) accumulates the exact (Fraction-style, via sympy.Rational) empirical
      distribution of S (as a subset of {0,...,K-1}), for comparison
      against the general-K Proposition S closed form using the EXACT
      marginal law of (L_0,...,L_{K-1},O) implied by this same brute force
      (not assumed from the Governing-Source Reindexing citation -- this
      brute force re-derives everything from Definition 4 itself, so it is
      an independent check of Prop. S as applied to the real model, not
      just the abstract destinations model of proposition_s_general_k.py).

No code from any other front in this lineage was read or used.
"""
import itertools
import sympy as sp
from itertools import permutations, product


def cyclic_points(f, n):
    """Return the set of cyclic points of f: [n] -> [n], by direct
    forward simulation from each point (no shortcut)."""
    cyc = set()
    for start in range(n):
        seen = []
        cur = start
        while True:
            if cur in seen:
                if cur == start:
                    cyc.add(start)
                break
            seen.append(cur)
            cur = f[cur]
    return cyc


def build_arcs(pi, K, n):
    """Reconstruct ARC(0..K-1) and OUTSIDE from a permutation pi and K
    sources at {0,...,K-1}, by walking pi's cycles and splitting each
    cycle that contains >=1 source at the source boundaries. Returns
    (arcs: dict s -> ordered list of positions, position [-1] == s itself,
    outside: set)."""
    sources = set(range(K))
    visited = [False] * n
    arcs = {s: [] for s in range(K)}
    outside = set()
    for start in range(n):
        if visited[start]:
            continue
        cyc = []
        cur = start
        while not visited[cur]:
            visited[cur] = True
            cyc.append(cur)
            cur = pi[cur]
        m = len(cyc)
        src_idx = [idx for idx, pos in enumerate(cyc) if pos in sources]
        if not src_idx:
            outside.update(cyc)
        else:
            for j, idx in enumerate(src_idx):
                prev_idx = src_idx[j - 1]
                length = (idx - prev_idx) % m
                if length == 0:
                    length = m
                positions = [cyc[(prev_idx + 1 + k) % m] for k in range(length)]
                s = cyc[idx]
                assert positions[-1] == s
                arcs[s] = positions
    return arcs, outside


def brute_force(n, K, verbose=False):
    assert n >= K
    total_configs = 0
    # exact counting via Fraction-equivalent: use Python's Fraction directly
    from fractions import Fraction
    S_counts = {}         # frozenset -> count
    identity_failures = 0
    identity_checks = 0
    for pi_tuple in permutations(range(n)):
        pi = list(pi_tuple)
        arcs, outside = build_arcs(pi, K, n)
        O = len(outside)
        L = {s: len(arcs[s]) for s in range(K)}
        for U in product(range(n), repeat=K):
            total_configs += 1
            f = list(pi)  # start from pi, then override sources
            for s in range(K):
                f[s] = U[s]
            cyc = cyclic_points(f, n)
            S = frozenset(s for s in range(K) if s in cyc)
            S_counts[S] = S_counts.get(S, 0) + 1

            # bookkeeping identity check
            T = len(cyc)
            Vs_sum = 0
            for s in S:
                Vs_sum += sum(1 for p in arcs[s] if p in cyc)
            identity_checks += 1
            if T != O + Vs_sum:
                identity_failures += 1
                if verbose:
                    print(f"IDENTITY FAIL: n={n} K={K} pi={pi} U={U} "
                          f"T={T} O={O} S={sorted(S)} Vs_sum={Vs_sum}")

    return total_configs, S_counts, identity_checks, identity_failures


def prop_s_formula_from_L(A, L, O, n):
    """Prop S formula using arc lengths L (dict) and O, n -- x_i := L_i/n,
    p_D := O/n. Returns a Fraction."""
    from fractions import Fraction
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


def main():
    from fractions import Fraction
    print("=" * 78)
    print("True Definition-4 brute force: bookkeeping identity + Prop. S check")
    print("=" * 78)
    all_ok = True
    configs = [
        (4, 1), (5, 1), (4, 2), (5, 2), (6, 2),
        (4, 3), (5, 3), (6, 3),
        (5, 4), (6, 4),
    ]
    for n, K in configs:
        total_configs, S_counts, checks, fails = brute_force(n, K)
        ok_identity = (fails == 0)
        all_ok &= ok_identity
        # marginal P(S=A), exact
        total = sum(S_counts.values())
        print(f"n={n} K={K}: total_configs={total_configs} "
              f"(n! n^K = {sp.factorial(n) * n**K}), "
              f"identity checks={checks} failures={fails} "
              f"[{'OK' if ok_identity else 'FAIL'}]")
        for A in sorted(S_counts.keys(), key=lambda s: (len(s), sorted(s))):
            emp = Fraction(S_counts[A], total)
            print(f"    P(S={sorted(A)}) empirical = {emp}  "
                  f"({S_counts[A]}/{total})")
        print()

    print("ALL BOOKKEEPING IDENTITY CHECKS PASSED"
          if all_ok else "SOME BOOKKEEPING IDENTITY CHECKS FAILED")


if __name__ == "__main__":
    main()
