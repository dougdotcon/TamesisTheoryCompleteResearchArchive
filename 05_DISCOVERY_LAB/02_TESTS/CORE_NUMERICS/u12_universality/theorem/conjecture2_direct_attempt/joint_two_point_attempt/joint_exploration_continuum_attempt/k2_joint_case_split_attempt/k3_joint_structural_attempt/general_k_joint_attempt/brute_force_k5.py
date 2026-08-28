"""
True ground-truth exhaustive enumeration of Definition 4's full K=5 model,
analogous to brute_force_k4.py, generalized to K=5.
"""
import sys
from itertools import permutations, product
from fractions import Fraction
import time


def both_cyclic_count(n):
    K = 5
    q1, q2 = n - 2, n - 1
    count = 0
    total = 0
    for perm in permutations(range(n)):
        for U in product(range(n), repeat=K):
            f = list(perm)
            for t in range(K):
                f[t] = U[t]
            total += 1

            def is_cyc(p):
                cur = p
                for _ in range(n + 1):
                    cur = f[cur]
                    if cur == p:
                        return True
                return False
            if is_cyc(q1) and is_cyc(q2):
                count += 1
    return count, total


if __name__ == '__main__':
    n_values = [int(x) for x in sys.argv[1:]] or [6, 7]
    for n in n_values:
        t0 = time.time()
        count, total = both_cyclic_count(n)
        elapsed = time.time() - t0
        frac = Fraction(count, total)
        print(f"n={n}: configs={total}, both_cyclic={count}, "
              f"P_nn({n},5)={frac} = {float(frac):.10f}, elapsed={elapsed:.1f}s")
