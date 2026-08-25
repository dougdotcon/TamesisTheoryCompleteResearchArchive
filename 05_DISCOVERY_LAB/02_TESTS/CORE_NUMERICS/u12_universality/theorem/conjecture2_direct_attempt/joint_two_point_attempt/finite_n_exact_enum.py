"""T2 — exact enumeration (fractions.Fraction, zero floating point) of the
finite-n conditional-K model: uniform permutation pi of [n]; a uniform
K-subset R of [n] rerouted; each i in R gets f(i) = U_i i.i.d. uniform on
[n]; f(i) = pi(i) otherwise. Exact quantities, for two FIXED points 1,2
(valid for any pair by exchangeability):

  P_both(n,K)  = P(1 and 2 both cyclic)          -> continuum 1/(K+1)
  P_same(n,K)  = P(both cyclic AND on the same cycle of f)
  P_diff(n,K)  = P(both cyclic AND on different cycles)
                 -> continuum prediction: each -> 1/(2(K+1)) (50/50 split)

Also E[C/n] as a harness sanity (must match the archive's psi-type means
in trend). Enumeration is over all pi (n!), all K-subsets, all n^K
destination tuples — fully exact. No random seed (deterministic).
"""
from fractions import Fraction
from itertools import permutations, combinations, product
import sys

def cyclic_info(f, n):
    """Return (cyclic_set, cycle_id) for mapping f (0-indexed list)."""
    color = [0]*n   # 0 unvisited, 1 in progress stack, 2 done
    on_cycle = [False]*n
    cyc_id = [-1]*n
    next_id = 0
    for s in range(n):
        if color[s]:
            continue
        path = []
        v = s
        while color[v] == 0:
            color[v] = 1
            path.append(v)
            v = f[v]
        if color[v] == 1:
            # found a new cycle: nodes from v to end of path
            idx = path.index(v)
            for w in path[idx:]:
                on_cycle[w] = True
                cyc_id[w] = next_id
            next_id += 1
        for w in path:
            if color[w] == 1:
                color[w] = 2
    return on_cycle, cyc_id

def enumerate_exact(n, K):
    tot_both = 0
    tot_same = 0
    tot_cyc = 0
    count = 0
    pts = list(range(n))
    for pi in permutations(pts):
        for R in combinations(pts, K):
            for dests in product(pts, repeat=K):
                f = list(pi)
                for r, d in zip(R, dests):
                    f[r] = d
                on_cycle, cyc_id = cyclic_info(f, n)
                count += 1
                tot_cyc += sum(on_cycle)
                if on_cycle[0] and on_cycle[1]:
                    tot_both += 1
                    if cyc_id[0] == cyc_id[1]:
                        tot_same += 1
    P_both = Fraction(tot_both, count)
    P_same = Fraction(tot_same, count)
    P_diff = P_both - P_same
    E_frac = Fraction(tot_cyc, count*n)
    return P_both, P_same, P_diff, E_frac, count

def main():
    plan = [(1, [3,4,5,6,7]), (2, [3,4,5,6])]
    for K, ns in plan:
        print(f"=== K = {K} ===   continuum predictions: "
              f"P_both -> 1/{K+1}, P_same & P_diff -> 1/{2*(K+1)} each")
        print(f"{'n':>2} | {'P_both':>12} = {'float':>8} | {'P_same':>12} = "
              f"{'float':>8} | {'P_diff':>12} = {'float':>8} | ratio same/both | E[C/n]")
        for n in ns:
            Pb, Ps, Pd, Ef, cnt = enumerate_exact(n, K)
            ratio = Ps/Pb if Pb else Fraction(0)
            print(f"{n:>2} | {str(Pb):>12} = {float(Pb):8.5f} | "
                  f"{str(Ps):>12} = {float(Ps):8.5f} | "
                  f"{str(Pd):>12} = {float(Pd):8.5f} | "
                  f"{str(ratio):>9} = {float(ratio):6.4f} | "
                  f"{str(Ef):>10} = {float(Ef):7.5f}   [{cnt} exact configs]")
            sys.stdout.flush()
        print(f"    continuum: P_both = {1/(K+1):.5f}, "
              f"P_same = P_diff = {1/(2*(K+1)):.5f}, ratio = 0.5000")
        print()

if __name__ == "__main__":
    main()
