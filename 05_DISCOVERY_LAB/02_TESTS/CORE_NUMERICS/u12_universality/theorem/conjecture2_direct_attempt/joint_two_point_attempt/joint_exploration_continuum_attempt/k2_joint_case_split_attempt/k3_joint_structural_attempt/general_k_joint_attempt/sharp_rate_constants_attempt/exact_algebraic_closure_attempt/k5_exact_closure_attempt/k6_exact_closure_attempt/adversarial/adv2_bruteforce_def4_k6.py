"""
Hostile referee, K6-EXACT-CLOSURE-ATTEMPT.

Independent, fully exhaustive brute-force implementation of THEOREM.md
Definition 4 (lines 859-872) at K=6, written directly from that prose --
NOT imported from, or structurally copied from, the target's own
bruteforce_definition4_k6.py (that file was read only to confirm the
target's own reported counts/timings match what a correct implementation
should give, per this review's task instructions).

Deliberately different implementation strategy from the target's own
script: instead of the "colour nodes IN_PROGRESS/DONE, walk until a
repeat" rho-detection algorithm, this script uses the mathematically
equivalent but algorithmically different "iterate every point n_max=2n
steps forward and check for a return to itself" method (functional
graphs stabilize into rho-shape within at most n steps, so an explicit
compute-successor-fn iterated map trajectory, without a proper visited
frontier, is a genuine second, independent cyclic-point detector) -- if
BOTH detectors agree, plus BOTH agree with the closed-form D6, that is
much stronger evidence than either check alone.

Model (exactly Definition 4's prose): K=6 reroute sources fixed WLOG at
{0,...,5}; f(i)=U_i for i<6, f(i)=pi(i) otherwise; T = #cyclic points.
Enumerates ALL n! permutations and ALL n^6 target tuples, no shortcut.

Run at n=6 (full run, as instructed) -- 33,592,320 configurations, the
K=5 predecessor's own referee's analogous scale.
"""
import sys
import time
from fractions import Fraction
from itertools import permutations, product
from math import factorial

K = 6


def is_cyclic_point(f, n, start):
    """A second, structurally different cyclic-point test: walk forward
    from `start` for up to n steps, recording visited nodes and their
    order; `start` is cyclic iff the walk returns to `start` at some
    step <= n (a point on a rho-graph is cyclic iff its own forward
    orbit revisits itself, which -- since f has out-degree exactly 1 on
    n nodes -- must happen within at most n steps if it happens at all).
    """
    v = f[start]
    for _ in range(n):
        if v == start:
            return True
        v = f[v]
    return False


def count_cyclic_points_v2(f, n):
    return sum(1 for i in range(n) if is_cyclic_point(f, n, i))


def exact_T_distribution(n):
    assert 0 <= K <= n
    counts = [0] * (n + 1)
    total = 0
    t0 = time.time()
    for pi in permutations(range(n)):
        pi = list(pi)
        for U in product(range(n), repeat=K):
            f = pi[:]
            for i in range(K):
                f[i] = U[i]
            T = count_cyclic_points_v2(f, n)
            counts[T] += 1
        total += n ** K
    return counts, total, time.time() - t0


def d6_predicted(n, k):
    """Proposicao D6's Bracket6, transcribed by hand from ATTEMPT.md
    Section 3.3 (NOT from the target's own .py files)."""
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
    ns = [int(x) for x in sys.argv[1:]] or [6]
    for n in ns:
        print(f"=== REFEREE independent brute force: n={n} K={K} ===", flush=True)
        counts, total, elapsed = exact_T_distribution(n)
        expected_total = factorial(n) * n ** K
        assert total == expected_total, (total, expected_total)
        print(f"n={n} K={K}  total configs={total}  elapsed={elapsed:.1f}s  "
              f"rate={total/elapsed:.0f} cfg/s")
        print(f"  counts (T=0..{n}): {counts}")
        cum = 0
        all_match = True
        for kk in range(0, n):
            cum += counts[kk]
            val = Fraction(cum, total)
            pred = d6_predicted(n, kk)
            ok = (val == pred)
            all_match = all_match and ok
            print(f"    k={kk}: brute={val} ({float(val):.12f})  "
                  f"D6={pred} ({float(pred):.12f})  match={ok}")
        cum += counts[n]
        assert cum == total
        print(f"  ALL k in [0,n-1] MATCH D6 (referee's independently-coded "
              f"cyclic-point detector): {all_match}")
        assert all_match, f"MISMATCH at n={n}"
        pt_eq_n = Fraction(counts[n], total)
        expected_pt_eq_n = Fraction(720, n ** 6)
        assert pt_eq_n == expected_pt_eq_n, (pt_eq_n, expected_pt_eq_n)
        print(f"  P(T=n) = {pt_eq_n} matches 720/n^6 = {expected_pt_eq_n}.  PASSED.")
        sys.stdout.flush()
    print("DONE.")
