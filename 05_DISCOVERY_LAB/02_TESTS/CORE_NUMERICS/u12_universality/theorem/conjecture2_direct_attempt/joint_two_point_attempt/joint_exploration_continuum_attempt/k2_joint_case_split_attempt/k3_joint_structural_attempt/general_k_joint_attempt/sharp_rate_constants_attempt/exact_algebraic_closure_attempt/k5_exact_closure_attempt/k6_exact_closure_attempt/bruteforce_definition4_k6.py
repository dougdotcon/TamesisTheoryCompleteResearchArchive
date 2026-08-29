"""
K6-EXACT-CLOSURE-ATTEMPT.

Fresh, independent, fully-exhaustive brute-force implementation of
THEOREM.md Definition 4 (the u12 permutation-with-reroutes ensemble,
lines 859-872), instantiated at K=6. Written directly from Definition 4's
own prose -- no code imported from any ancestor front (the K=5
predecessor's own `bruteforce_definition4_k5.py` was read, per the
mandate, only as prose/structure reference for what "fully exhaustive"
means in this lineage; every line of code below is typed fresh).

Model: n points labelled 0..n-1. K=6 reroute sources fixed WLOG at
{0,...,5} (exchangeability is standard and unquestioned in this lineage;
we still enumerate ALL n! permutations pi and ALL n^6 target tuples U,
never a reduced/decomposition-model shortcut, so this remains a genuine,
independent ground truth against Proposicao D6).

    f(i) := U_i    if i < 6  (i is a reroute source)
    f(i) := pi(i)  otherwise

    T := #{cyclic points of f} := #{i : iterating f from i returns to i}.

Cyclic-point counting on a general functional graph (out-degree exactly
1 everywhere, not necessarily a bijection since U_i can collide): the
standard O(n) "rho-shaped graph" walk -- colour nodes IN_PROGRESS while
on the current walk, DONE once resolved; a walk that lands on an
IN_PROGRESS node has just closed a genuine cycle, consisting of exactly
the tail of the current walk from that node onward.

Outputs, per n tested: exact P(T<=k) (Python Fraction, exact integer
counts under the hood) for every k=0,...,n, from a full enumeration of
all n! * n^6 (pi, U) pairs -- cross-checked against Proposicao D6.
"""
import sys
import time
from fractions import Fraction
from itertools import permutations, product
from math import factorial

K = 6


def count_cyclic_points(f, n):
    color = [0] * n  # 0 unvisited, 1 in-progress, 2 done
    depth = [0] * n
    cyclic = 0
    for start in range(n):
        if color[start]:
            continue
        walk = []
        v = start
        while color[v] == 0:
            color[v] = 1
            depth[v] = len(walk)
            walk.append(v)
            v = f[v]
        if color[v] == 1:
            cyclic += len(walk) - depth[v]
        for u in walk:
            color[u] = 2
    return cyclic


def exact_T_distribution(n, verbose_every=None):
    assert 0 <= K <= n
    counts = [0] * (n + 1)
    total = 0
    t0 = time.time()
    pcount = 0
    for pi in permutations(range(n)):
        pcount += 1
        pi = list(pi)
        for U in product(range(n), repeat=K):
            f = pi[:]
            for i in range(K):
                f[i] = U[i]
            T = count_cyclic_points(f, n)
            counts[T] += 1
        total += n ** K
        if verbose_every and pcount % verbose_every == 0:
            el = time.time() - t0
            rate = total / el if el > 0 else 0.0
            print(f"    ...{pcount}/{factorial(n)} permutations done, "
                  f"{total} configs, {el:.1f}s, {rate:.0f} cfg/s", flush=True)
    return counts, total


def cdf_from_counts(counts, total):
    cum = 0
    out = []
    for c in counts:
        cum += c
        out.append(Fraction(cum, total))
    return out


def d6_predicted(n, k):
    """Proposicao D6, transcribed by hand from d6_derivation.py/.log
    (this front's own derivation, Section 3 of ATTEMPT.md) -- exact
    rational evaluation via Fraction-safe integer arithmetic."""
    num = (
        -k**12 + 24*k**11 + 6*k**10*n**2 - 45*k**10*n - 245*k**10
        - 90*k**9*n**2 + 715*k**9*n + 1380*k**9
        - 15*k**8*n**4 + 195*k**8*n**3 - 105*k**8*n**2 - 4620*k**8*n - 4623*k**8
        + 120*k**7*n**4 - 1680*k**7*n**3 + 4350*k**7*n**2 + 15354*k**7*n + 9072*k**7
        + 20*k**6*n**6 - 330*k**6*n**5 + 1510*k**6*n**4 + 1725*k**6*n**3
        - 18082*k**6*n**2 - 26481*k**6*n - 8735*k**6
        - 60*k**5*n**6 + 1110*k**5*n**5 - 6600*k**5*n**4 + 8241*k**5*n**3
        + 28380*k**5*n**2 + 17115*k**5*n - 780*k**5
        - 15*k**4*n**8 + 270*k**4*n**7 - 1810*k**4*n**6 + 4875*k**4*n**5
        - 365*k**4*n**4 - 15750*k**4*n**3 - 8095*k**4*n**2 + 14010*k**4*n + 10724*k**4
        - 40*k**3*n**7 + 630*k**3*n**6 - 3620*k**3*n**5 + 8340*k**3*n**4
        + 135*k**3*n**3 - 25200*k**3*n**2 - 30304*k**3*n - 9696*k**3
        + 6*k**2*n**10 - 105*k**2*n**9 + 735*k**2*n**8 - 2685*k**2*n**7
        + 5744*k**2*n**6 - 7065*k**2*n**5 - 1130*k**2*n**4 + 13830*k**2*n**3
        + 26276*k**2*n**2 + 17136*k**2*n + 2880*k**2
        + 6*k*n**10 - 105*k*n**9 + 720*k*n**8 - 2375*k*n**7 + 3384*k*n**6
        - 10*k*n**5 - 1860*k*n**4 - 6696*k*n**3 - 7440*k*n**2 - 2880*k*n
    )
    den = 720 * n**6 * factorial(n) // (factorial(6) * factorial(n - 6))
    return Fraction(num, den)


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [5, 6, 7]
    for n in ns:
        print(f"=== n={n} K={K} ===", flush=True)
        t0 = time.time()
        counts, total = exact_T_distribution(n, verbose_every=(5000 if n >= 7 else None))
        elapsed = time.time() - t0
        expected_total = factorial(n) * n ** K
        assert total == expected_total, (total, expected_total)
        cdf = cdf_from_counts(counts, total)
        print(f"n={n} K={K}  total configs={total}  elapsed={elapsed:.1f}s  "
              f"rate={total/elapsed:.0f} cfg/s")
        print(f"  counts (T=0..{n}): {counts}")
        # Proposicao D6's stated domain of validity is 0<=k<=n-1 (matching
        # D1-D5's own stated domains); P(T<=n)=1 trivially (T<=n always)
        # and is NOT expected to come from evaluating the same rational
        # formula at k=n (see Self-caught issues in ATTEMPT.md -- the K=5
        # predecessor front hit and documented the identical point).
        all_match = True
        for k in range(0, n):
            val = cdf[k]
            pred = d6_predicted(n, k)
            ok = (val == pred)
            all_match = all_match and ok
            print(f"    k={k}: brute={val} ({float(val):.12f})  "
                  f"D6={pred} ({float(pred):.12f})  match={ok}")
        print(f"  ALL k in [0,n-1] MATCH D6: {all_match}")
        assert all_match, f"MISMATCH at n={n}"
        assert cdf[n] == 1, "P(T<=n) must be 1 trivially"
        pt_eq_n = 1 - cdf[n - 1]
        expected_pt_eq_n = Fraction(720, n ** 6)
        assert pt_eq_n == expected_pt_eq_n, (pt_eq_n, expected_pt_eq_n)
        print(f"  P(T=n) = 1-D6(n,n-1) = {pt_eq_n} matches 720/n^6 "
              f"= {expected_pt_eq_n}.  PASSED (k=n boundary, separately).")
        sys.stdout.flush()
    print("DONE.")
