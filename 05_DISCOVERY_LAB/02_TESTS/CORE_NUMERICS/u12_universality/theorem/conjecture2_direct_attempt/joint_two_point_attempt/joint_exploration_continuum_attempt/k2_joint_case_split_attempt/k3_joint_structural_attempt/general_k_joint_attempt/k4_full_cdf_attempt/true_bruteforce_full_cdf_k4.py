"""
K4-FULL-CDF-ATTEMPT: fresh, from-scratch, fully-exhaustive true brute
force of Definition 4's literal K=4 model.  No shortcut of any kind:
genuine permutations pi of [n], genuine i.i.d. targets U0,U1,U2,U3 in
[0,n), f(i)=U_i for i<4 else f(i)=pi(i), T = #cyclic points of f (found
by direct functional-graph traversal, O(n) amortized per configuration
via iterative pointer-chasing with a 3-state visited marker -- not the
naive O(n^2) restart-from-scratch-per-point method).

Usage: python3 true_bruteforce_full_cdf_k4.py N   (single n, writes a
pmf dict to bf_pmf_N.pkl and prints a summary; also verifies against
Proposicao D4 if F_generic.pkl is present).
"""
import sys
import time
import pickle
from itertools import permutations, product
from fractions import Fraction

K = 4


def cyclic_count(f, n):
    """f: list of length n, f[i] in [0,n).  Returns #cyclic points, via
    O(n) amortized iterative pointer-chasing (3-state: 0=unvisited,
    1=in current chain, 2=done)."""
    state = [0] * n
    cyclic = [False] * n
    for start in range(n):
        if state[start] != 0:
            continue
        path = []
        pos = {}
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            pos[cur] = len(path)
            path.append(cur)
            cur = f[cur]
        if state[cur] == 1:
            idx = pos[cur]
            for node in path[idx:]:
                cyclic[node] = True
        for node in path:
            state[node] = 2
    return sum(cyclic)


def run(n):
    counts = {}
    total = 0
    f = [0] * n
    for pi in permutations(range(n)):
        for i in range(n):
            f[i] = pi[i]
        for U in product(range(n), repeat=K):
            for s in range(K):
                f[s] = U[s]
            T = cyclic_count(f, n)
            counts[T] = counts.get(T, 0) + 1
            total += 1
            # restore f[s] for next pi-consistent baseline not needed:
            # next U iteration overwrites f[0..3] again; f[4:] untouched
            # by U loop and gets reset at top of pi loop.
    return counts, total


def to_cdf(counts, total, n):
    pmf = {t: Fraction(c, total) for t, c in counts.items()}
    cdf = {}
    running = Fraction(0)
    for k in range(0, n + 1):
        running += pmf.get(k, Fraction(0))
        cdf[k] = running
    return pmf, cdf


if __name__ == "__main__":
    n = int(sys.argv[1])
    t0 = time.time()
    counts, total = run(n)
    elapsed = time.time() - t0
    pmf, cdf = to_cdf(counts, total, n)
    print(f"n={n}: total configs = {total} (= {n}! * {n}^{K}), elapsed = {elapsed:.1f}s")
    print(f"  pmf (T -> count): {sorted(counts.items())}")
    print(f"  cdf: {[(k, str(cdf[k])) for k in range(n+1)]}")

    with open(f'bf_pmf_{n}.pkl', 'wb') as fh:
        pickle.dump(dict(n=n, counts=counts, total=total, cdf=cdf, elapsed=elapsed), fh)

    # cross-check against Proposicao D4 if available
    try:
        import sympy as sp
        with open('F_generic.pkl', 'rb') as fh:
            F = pickle.load(fh)
        nn, kk = sp.symbols('n k')
        mismatches = 0
        for k in range(0, n):
            got = sp.Rational(F.subs({nn: sp.Integer(n), kk: sp.Integer(k)}))
            gotf = Fraction(got.p, got.q)
            exp = cdf[k]
            if gotf != exp:
                mismatches += 1
                print(f"  MISMATCH k={k}: bruteforce={exp} D4={gotf}")
        print(f"  Proposicao D4 cross-check: {n} k-values, mismatches={mismatches}")
    except FileNotFoundError:
        print("  (F_generic.pkl not found -- skipping D4 cross-check)")
