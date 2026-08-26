"""K=2, "overlap-allowed" convention (Prop K1's own convention, generalized):
query points fixed at {0,1}; the K=2 reroute sources R are a uniform random
2-SUBSET of ALL of [n] (can include 0 and/or 1). Computes
P_n^{(2)}(both) := P(0,1 both cyclic), for comparison against this front's
P_nn(n,2) (disjoint-by-construction convention) -- both should converge to
the same continuum limit 1/3, by the same style of argument as Reduction
Lemma A (THEOREM.md Estagio 3) / Lemma P2 (distributional_bridge_attempt),
even though they are different finite-n quantities. Exact, Fraction-free
integer counting (kept as plain ints/Fraction only at the end)."""
from fractions import Fraction
from itertools import permutations, combinations
import sys


def cyclic_points(f, n):
    cyclic = set()
    color = [0] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:
            idx = path.index(x)
            for y in path[idx:]:
                cyclic.add(y)
        for y in path:
            color[y] = 2
    return cyclic


def run(n):
    q1, q2 = 0, 1
    total = 0
    both = 0
    for pi in permutations(range(n)):
        for R in combinations(range(n), 2):
            for u1 in range(n):
                for u2 in range(n):
                    f = list(pi)
                    f[R[0]] = u1
                    f[R[1]] = u2
                    cyc = cyclic_points(f, n)
                    total += 1
                    if q1 in cyc and q2 in cyc:
                        both += 1
    return Fraction(both, total), total


if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [4, 5]
    for n in ns:
        p, total = run(n)
        print(f"n={n}: total_configs={total} P_n^(2)(both) [overlap-allowed] = {p} ({float(p):.6f})  "
              f"vs this front's P_nn(n,2) [disjoint] = {Fraction(10*n*n+7*n+2,30*n*n)} "
              f"({float(Fraction(10*n*n+7*n+2,30*n*n)):.6f})")
