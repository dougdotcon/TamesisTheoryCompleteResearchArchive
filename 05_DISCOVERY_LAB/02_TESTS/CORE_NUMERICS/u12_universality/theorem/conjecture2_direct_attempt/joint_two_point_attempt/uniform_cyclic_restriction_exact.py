"""wave 17 front (c) JOINT-TWO-POINT-EXPLORATION-ATTEMPT (DISC-DEC-072).
Written FRESH this session (not reusing the stalled attempt's scripts, per
mandate discipline). Deterministic exact enumeration -- no randomness, no
seed needed.

Model (Definition 4 of THEOREM.md: the finite conditional-K model): pi a
uniform permutation of [n]; R a uniform K-subset of [n], independent of pi;
f(i) = U_i i.i.d. Uniform([n]) for i in R; f(i) = pi(i) for i not in R.

Purpose: exhaustively verify, for every (n,K) in a feasible range, the new
structural claim discovered this session:

  THEOREM (Uniform Cyclic Restriction). Conditional on the realized final
  cyclic point set C(f) = c (any fixed subset with |c| = m >= 2, positive
  probability), the restriction f|_c is distributed EXACTLY uniformly over
  Sym(c) -- all m! bijections of c equally likely.

  COROLLARY (exact 50/50 split, every finite n and K, not just n -> oo):
  for two fixed distinct points i != j, P(i,j both cyclic AND same final
  cycle) = P(i,j both cyclic AND different final cycles), exactly.

Both are checked here by full exhaustive enumeration (exact integer counts,
zero floating point until the final display step, where Fraction is used).
A companion classical-fact check verifies "P(two fixed elements of a
uniform permutation of m elements lie in the same cycle) = 1/2 for every
m>=2" directly (needed as the second half of the corollary's proof).
"""
from fractions import Fraction
from itertools import permutations, combinations, product
from collections import defaultdict
import sys
import time


def cyclic_set_and_restriction(f, n):
    """Return (frozenset of cyclic points, sorted tuple of (i,f(i)) pairs
    restricted to the cyclic set) for a mapping f given as a list, 0-indexed."""
    color = [0] * n          # 0 unvisited, 1 on current path, 2 fully done
    on_cycle = [False] * n
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
            idx = path.index(v)
            for w in path[idx:]:
                on_cycle[w] = True
        for w in path:
            if color[w] == 1:
                color[w] = 2
    C = frozenset(i for i in range(n) if on_cycle[i])
    restr = tuple(sorted((i, f[i]) for i in C))
    return C, restr


def enumerate_full(n, K):
    """Single exhaustive pass over all (pi, R, dests) configurations.
    Returns:
      total            -- number of configurations enumerated
      by_C             -- dict: C (frozenset) -> dict(restriction tuple -> count)
      both_01          -- count with points 0,1 both cyclic
      same_01          -- count with points 0,1 both cyclic AND same final cycle
      cyc_sum          -- sum over configs of |C(f)| (for an E[C/n] sanity readout)
    """
    pts = list(range(n))
    by_C = defaultdict(lambda: defaultdict(int))
    total = 0
    both_01 = 0
    same_01 = 0
    cyc_sum = 0
    for pi in permutations(pts):
        for R in combinations(pts, K):
            for dests in product(pts, repeat=K):
                f = list(pi)
                for r, d in zip(R, dests):
                    f[r] = d
                C, restr = cyclic_set_and_restriction(f, n)
                by_C[C][restr] += 1
                total += 1
                cyc_sum += len(C)
                if 0 in C and 1 in C:
                    both_01 += 1
                    # same final cycle iff restr, viewed as a permutation of
                    # C, maps 0 into the same cycle as 1 -- walk it directly.
                    d_ = dict(restr)
                    v = d_[0]
                    same = False
                    steps = 0
                    while v != 0 and steps <= len(C) + 2:
                        if v == 1:
                            same = True
                            break
                        v = d_[v]
                        steps += 1
                    if 0 == 1:
                        same = True  # unreachable, n>=2 always
                    same_01 += int(same)
    return total, by_C, both_01, same_01, cyc_sum


def check_uniform_restriction(n, K, by_C):
    """Check exact uniformity of f|_c over Sym(c) for every realized c with
    |c| >= 2. Returns list of violations (empty if none)."""
    bad = []
    for C, d in by_C.items():
        m = len(C)
        if m < 2:
            continue
        nfact = 1
        for i in range(1, m + 1):
            nfact *= i
        if len(d) != nfact:
            bad.append((C, "missing bijections", len(d), nfact))
            continue
        counts = set(d.values())
        if len(counts) != 1:
            bad.append((C, "nonuniform counts", sorted(counts)))
    return bad


def classical_same_cycle_half(m):
    """Exact P(1,2 same cycle) for a uniform permutation of m elements,
    m>=2, by direct exhaustive enumeration. Independent re-derivation of
    the textbook fact (used as the second ingredient of the corollary's
    proof: Uniform Cyclic Restriction + this classical fact => 50/50)."""
    pts = list(range(m))
    same = 0
    total = 0
    for pi in permutations(pts):
        total += 1
        v = pi[0]
        is_same = False
        steps = 0
        while v != 0 and steps <= m + 2:
            if v == 1:
                is_same = True
                break
            v = pi[v]
            steps += 1
        same += int(is_same)
    return Fraction(same, total)


def main():
    print("=== Classical fact check: P(1,2 same cycle | uniform perm of m) ===")
    for m in range(2, 8):
        val = classical_same_cycle_half(m)
        print(f"  m={m}: P = {val} = {float(val):.6f}  "
              f"{'OK (=1/2)' if val == Fraction(1, 2) else 'MISMATCH'}")
    print()

    print("=== Uniform Cyclic Restriction theorem: exhaustive check ===")
    plan = [
        (1, [3, 4, 5, 6, 7]),
        (2, [3, 4, 5, 6, 7]),
        (3, [3, 4, 5, 6]),
        (4, [4, 5, 6]),
        (5, [5, 6]),
    ]
    all_ok = True
    for K, ns in plan:
        for n in ns:
            if K > n:
                continue
            t0 = time.time()
            total, by_C, both_01, same_01, cyc_sum = enumerate_full(n, K)
            bad = check_uniform_restriction(n, K, by_C)
            dt = time.time() - t0
            diff_01 = both_01 - same_01
            Pboth = Fraction(both_01, total)
            Psame = Fraction(same_01, total)
            Pdiff = Fraction(diff_01, total)
            ratio = Psame / Pboth if Pboth else None
            Ecyc = Fraction(cyc_sum, total * n)
            ok = (not bad) and (Psame == Pdiff)
            all_ok = all_ok and ok
            sizes = sorted(len(C) for C in by_C if len(C) >= 2)
            max_size = max(sizes) if sizes else 0
            print(f"n={n:2d} K={K}  configs={total:>10d}  time={dt:5.1f}s  "
                  f"sizes|c|>=2 up to {max_size}  "
                  f"P_both={str(Pboth):>9s}={float(Pboth):.5f}  "
                  f"P_same={str(Psame):>9s}  P_diff={str(Pdiff):>9s}  "
                  f"ratio={str(ratio):>7s}  E[C/n]={str(Ecyc):>9s}={float(Ecyc):.5f}  "
                  f"restriction={'UNIFORM' if not bad else 'VIOLATION'}  "
                  f"same=diff:{'YES' if Psame==Pdiff else 'NO'}")
            sys.stdout.flush()
            if bad:
                for b in bad[:5]:
                    print("    VIOLATION:", b)
    print()
    print("ALL CHECKS PASS (zero violations across all (n,K) tested)"
          if all_ok else "SOME CHECKS FAILED -- see VIOLATION lines above")


if __name__ == "__main__":
    main()
