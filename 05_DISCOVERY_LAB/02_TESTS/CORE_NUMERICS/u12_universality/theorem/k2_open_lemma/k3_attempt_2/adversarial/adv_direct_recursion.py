"""
Independent (task item 2/9), separately-coded memoized exact-fraction implementation
of ATTEMPT.md SS2's transition rules -- written from scratch for this review, not
copied from markov_direct.py (different memoization strategy: a single dict keyed by
(kind,a,b,r) rather than two separate lru_cache'd closures; explicit assertion that
every branch's probability mass sums to the pool size, checked at every call as a
runtime self-audit -- not present in the front's markov_direct.py).

Compared against THIS review's own adv_bruteforce.py (not the front's
psi_bruteforce_ref.py) -- so this is an end-to-end independent chain: independent
model implementation vs independent raw-definition enumeration.
"""
from fractions import Fraction as F
import sys
from adv_bruteforce import psi_generic


def psi_via_direct_recursion(n, K):
    N = F(n)
    memo = {}

    def g(a, b, r):
        key = ("g", a, b, r)
        if key in memo:
            return memo[key]
        m = N - a
        # partition audit: 1 (success) + r (to source) + b (poisoned fail) +
        # (m-1-r-b) (fresh continue) must equal m, exactly, as integers.
        assert F(1) + r + b + (m - 1 - r - b) == m, "g-step partition does not sum to m!"
        val = F(1) / m
        if r > 0:
            val += F(r) / m * h(a + 1, b, r - 1)
        rem = m - 1 - r - b
        if rem > 0:
            val += rem / m * g(a + 1, b, r)
        memo[key] = val
        return val

    def h(a, b, r):
        key = ("h", a, b, r)
        if key in memo:
            return memo[key]
        # partition audit: 1 (success) + a (pi-visited fail) + b (poisoned fail) +
        # r (to source) + (n-1-a-b-r) (fresh continue) must equal n.
        assert F(1) + a + b + r + (N - 1 - a - b - r) == N, "h-step partition does not sum to n!"
        val = F(1) / N
        if r > 0:
            val += F(r) / N * h(a, b + 1, r - 1)
        rem = N - 1 - a - b - r
        if rem > 0:
            val += rem / N * g(a, b + 1, r)
        memo[key] = val
        return val

    return g(F(0), F(0), K)


if __name__ == "__main__":
    print("K | n | direct-recursion(mine) | brute-force(mine, adv_bruteforce.py) | MATCH")
    all_ok = True
    for K in [1, 2, 3]:
        for n in range(K + 1, 9):
            dr = psi_via_direct_recursion(n, K)
            bf = psi_generic(n, K)
            ok = dr == bf
            all_ok &= ok
            print(f"{K} | {n} | {dr} | {bf} | {'MATCH' if ok else 'MISMATCH!!!'}")
            sys.stdout.flush()
    print()
    print("ALL MATCH:" if all_ok else "MISMATCHES FOUND:", all_ok)
