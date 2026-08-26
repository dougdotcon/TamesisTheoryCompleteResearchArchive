#!/usr/bin/env python3
"""
Independent adversarial check (av01) — HOSTILE REFEREE, fresh build.

Re-derives, from Definition 1 of THEOREM.md ALONE (never opens the front's
.py scripts, and never opens the prior stalled referee's ref01_*.py either
-- rebuilt from scratch, from the prose of ATTEMPT.md's Lemma 1 statement
and its own proof, which was hand-checked in this session before any code
was written), a brute-force exact evaluator of

    phi(n, c) = E[ #{cyclic points of f} ] / n ,   q = c/n,

for small n (3,4,5), using EXACT Fraction arithmetic, at several rational
q values, and compares against an independent re-implementation of
Lemma 1's claimed closed form

    A_k(n,q) = sum_{m=0}^k C(k,m) q^m (1-q)^{k-m} * prod_{i=1}^m (n-k+i)/n
    n*phi(n,q*n) = sum_{k=1}^n A_k(n,q)

Two degree-n polynomials in q that agree at >= n+1 rational points are
identical, so exact agreement at n+1 points is a genuine proof (not just
a spot check) that the two formulas define the same polynomial in q.

Brute force construction (exactly Definition 1, THEOREM.md Sec 1):
  - subset S subseteq [n] of "rerouted" indices, weight q^|S| (1-q)^(n-|S|)
  - for i not in S: f(i) = pi(i), pi a uniform permutation of [n]; only the
    *values* pi(i) for i not in S matter, and (by symmetry / marginalizing
    over the n! permutations) these are distributed as a uniformly random
    INJECTIVE map from ([n] \ S) into [n] -- i.e. an ordered selection of
    n-|S| distinct values without replacement, each equally likely
    (matches P(pi(a_1)=b_1,...) = 1/(n)_r for the standard random
    permutation fact, used here only as an enumeration device, not
    assumed as the thing being checked).
  - for i in S: f(i) = U_i, i.i.d. uniform on [n] (WITH repetition, and
    independent of the pi-images).
  - cyclic point count of f computed by direct functional-graph cycle
    detection.
This is a from-scratch enumeration directly against Definition 1; it does
NOT use Lemma 1's derivation as an input, so matching it is a real
independent check of Lemma 1's correctness.
"""
import itertools
from fractions import Fraction as F
import sys

def cyclic_count(f, n):
    """f: list of length n, f[i] in range(n). Returns # of i with i on a
    directed cycle of the functional graph (0-indexed)."""
    color = [0]*n  # 0=white,1=gray(in current path),2=black(done, not cyclic unless flagged)
    is_cyclic = [False]*n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        v = start
        while color[v] == 0:
            color[v] = 1
            path.append(v)
            v = f[v]
        if color[v] == 1:
            # v is in current path -> found a cycle starting at v
            idx = path.index(v)
            for u in path[idx:]:
                is_cyclic[u] = True
        for u in path:
            color[u] = 2
    return sum(is_cyclic)


def brute_force_phi(n, q):
    """Exact E[#cyclic]/n at Definition 1, q rational (Fraction)."""
    total = F(0)
    for m in range(n+1):
        for S in itertools.combinations(range(n), m):
            Sset = set(S)
            nonS = [i for i in range(n) if i not in Sset]
            weight_S = q**m * (1-q)**(n-m)
            if weight_S == 0:
                continue
            # enumerate injective maps nonS -> distinct values in range(n)
            n_nonS = len(nonS)
            n_perm_count = 0
            n_perm_sum = 0
            for images in itertools.permutations(range(n), n_nonS):
                n_perm_count += 1
                pi_map = dict(zip(nonS, images))
                # enumerate U assignments on S (with repetition)
                if m == 0:
                    f = [pi_map[i] for i in range(n)]
                    n_perm_sum += cyclic_count(f, n)
                else:
                    for U in itertools.product(range(n), repeat=m):
                        f = [0]*n
                        for i in nonS:
                            f[i] = pi_map[i]
                        for idx, i in enumerate(S):
                            f[i] = U[idx]
                        n_perm_sum += cyclic_count(f, n)
            n_U_count = n**m
            avg_cyclic_given_S = F(n_perm_sum, n_perm_count * n_U_count)
            total += weight_S * avg_cyclic_given_S
    return total / n


def lemma1_A_k(n, q, k):
    """A_k(n,q) per Lemma 1, exact Fraction arithmetic."""
    total = F(0)
    from math import comb
    for mm in range(k+1):
        term = F(comb(k, mm)) * q**mm * (1-q)**(k-mm)
        prod = F(1)
        for i in range(1, mm+1):
            prod *= F(n - k + i, n)
        total += term * prod
    return total


def lemma1_phi(n, q):
    s = F(0)
    for k in range(1, n+1):
        s += lemma1_A_k(n, q, k)
    return s / n


def main():
    log = []
    def p(*a):
        s = " ".join(str(x) for x in a)
        print(s)
        log.append(s)

    p("=== av01_lemma1_bruteforce: independent Definition-1 brute force vs Lemma 1 ===")
    all_ok = True
    for n in (3, 4, 5):
        # n+1 rational q points needed to pin down a degree-n polynomial
        q_points = [F(k, 10) for k in range(0, n+2)]  # 0/10 .. (n+1)/10, n+2 points (extra for safety)
        p(f"--- n={n} : checking {len(q_points)} rational q points (need >= {n+1}) ---")
        for q in q_points:
            bf = brute_force_phi(n, q)
            l1 = lemma1_phi(n, q)
            ok = (bf == l1)
            all_ok &= ok
            p(f"  n={n} q={q}: brute_force={bf}  lemma1={l1}  match={ok}")
        # also check q=1 endpoint exactly (Remark 1.2 claim: phi(n,n)=Q(n)/n)
        q1 = F(1)
        bf1 = brute_force_phi(n, q1)
        l1_1 = lemma1_phi(n, q1)
        Qn = sum(F(1) for _ in [0])  # placeholder, real Q(n) computed below
        # Q(n) := sum_{k=1}^n (n)_k / n^k  (falling factorial over n^k)
        Qn = F(0)
        fall = F(1)
        for k in range(1, n+1):
            fall *= F(n - k + 1, 1)
            Qn += fall / F(n)**k
        p(f"  n={n} q=1 (gamma=1 endpoint): brute_force={bf1}  lemma1={l1_1}  Q(n)/n={Qn/n}  "
          f"all_equal={bf1==l1_1==Qn/n}")
        all_ok &= (bf1 == l1_1 == Qn/n)
        # q=0 sanity (Remark 1.1: phi(n,0)=1)
        bf0 = brute_force_phi(n, F(0))
        p(f"  n={n} q=0 sanity: brute_force={bf0}  (expect 1)  ok={bf0==1}")
        all_ok &= (bf0 == 1)

    p("")
    p(f"OVERALL: {'ALL CHECKS PASSED' if all_ok else 'MISMATCH FOUND'}")
    with open(__file__.replace('.py', '.log'), 'w') as fh:
        fh.write("\n".join(log) + "\n")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
