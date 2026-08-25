#!/usr/bin/env python3
"""HOSTILE REFEREE check 1 (wave 17 front (e), DISC-DEC-072).

Independent, from-scratch validation of Lemma 1 of ATTEMPT.md:

    phi(n, qn) = (1/n) sum_{k=1}^n A_k(n,q),
    A_k = sum_{m=0}^k C(k,m) q^m (1-q)^{k-m} * prod_{i=1}^m (n-k+i)/n .

Written WITHOUT reading any of the front's .py scripts (mandate).

Checks:
  R1  Brute-force enumeration of Definition 1 (THEOREM.md par.1) at n=2,3,4,5:
      enumerate ALL permutations pi, ALL reroute subsets S, ALL U-assignments
      on S; per-mapping cyclic-point count; accumulate E[#cyclic] as an EXACT
      polynomial in q (Fraction coefficients).  Compare coefficient-by-
      coefficient with the Lemma-1 polynomial.
  R2  q=1 endpoint: Lemma 1 vs independently computed Q(n)/n (Ramanujan Q,
      Q(n)=sum_k (n)_k/n^k), exact Fractions, n=1..400.
  R3  Mixture inversion: solve the exact Bernstein-basis system
      phi(n,qn) = sum_K C(n,K) q^K (1-q)^{n-K} phi_n^{(K)}
      for phi_n^{(K)} from the Lemma-1 polynomial (exact Gaussian elimination
      over Fractions), n=6..10; compare with the archive's independently
      proved closed forms:
        phi_n^{(0)} = 1
        phi_n^{(1)} = 2/3 + 1/(3n^2)                       (Estagio 2/3)
        phi_n^{(2)} = 8/15 + 1/(30n) + 7/(10n^2) + 1/(5n^3) (Estagio 3)
        phi_n^{(3)} = 16/35 + 1/(14n) + 11/(10n^2) + 23/(35n^3) + 6/(35n^4)
                                                            (Estagio 4, n>=4)
        phi_n^{(n)} = Q(n)/n                                (Estagio 10)
No randomness anywhere (deterministic object); referee seed block
20260869000+ reserved but UNUSED.
"""
from fractions import Fraction
from itertools import permutations, combinations, product
from math import comb
import sys, time

def cyclic_count(f, n):
    """Number of cyclic points of mapping f: tuple of length n, 0-based."""
    cnt = 0
    for i in range(n):
        # iterate n steps to land in the cycle part, then check recurrence
        x = i
        for _ in range(n):
            x = f[x]
        # x is now on a cycle; i is cyclic iff i is reachable from x on cycle
        # simpler: i cyclic iff f^t(i)=i for some 1<=t<=n
        x = i
        ok = False
        for _ in range(n):
            x = f[x]
            if x == i:
                ok = True
                break
        if ok:
            cnt += 1
    return cnt

def bruteforce_poly(n):
    """E[#cyclic] as polynomial in q (list of Fraction coefs, degree n).
    E = sum_m q^m (1-q)^(n-m) * T_m / (n! * n^m), where
    T_m = sum over |S|=m, pi, U of #cyclic(f)."""
    T = [0]*(n+1)
    fact = 1
    for j in range(2, n+1):
        fact *= j
    for pi in permutations(range(n)):
        for m in range(n+1):
            for S in combinations(range(n), m):
                base = list(pi)
                if m == 0:
                    T[0] += cyclic_count(base, n)
                    continue
                for U in product(range(n), repeat=m):
                    f = list(pi)
                    for idx, s in enumerate(S):
                        f[s] = U[idx]
                    T[m] += cyclic_count(f, n)
    # assemble polynomial in monomial basis
    coeffs = [Fraction(0)]*(n+1)
    for m in range(n+1):
        w = Fraction(T[m], fact * n**m)
        # q^m (1-q)^(n-m) = sum_j C(n-m,j) (-1)^j q^(m+j)
        for j in range(n-m+1):
            coeffs[m+j] += w * comb(n-m, j) * (-1)**j
    return coeffs

def lemma1_poly(n):
    """n*phi(n,qn) = sum_k A_k as exact polynomial in q (monomial basis)."""
    coeffs = [Fraction(0)]*(n+1)
    for k in range(1, n+1):
        # P_{k,m} = prod_{i=1}^m (n-k+i)/n
        P = Fraction(1)
        for m in range(0, k+1):
            if m > 0:
                P *= Fraction(n-k+m, n)
            w = comb(k, m) * P
            # q^m (1-q)^(k-m)
            for j in range(k-m+1):
                coeffs[m+j] += w * comb(k-m, j) * (-1)**j
    return coeffs

def Qn_exact(n):
    Q = Fraction(0)
    t = Fraction(1)
    for k in range(1, n+1):
        t *= Fraction(n-k+1, n)
        Q += t
    return Q

def bernstein_invert(n, poly):
    """Solve sum_K C(n,K) q^K(1-q)^{n-K} x_K = poly(q) exactly."""
    # build matrix M[j][K] = coefficient of q^j in C(n,K) q^K (1-q)^(n-K)
    M = [[Fraction(0)]*(n+1) for _ in range(n+1)]
    for K in range(n+1):
        for j in range(n-K+1):
            M[K+j][K] += comb(n, K) * comb(n-K, j) * (-1)**j
    # Gaussian elimination solve M x = poly
    A = [row[:] + [poly[i]] for i, row in enumerate(M)]
    N = n+1
    for col in range(N):
        piv = next(r for r in range(col, N) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v/pv for v in A[col]]
        for r in range(N):
            if r != col and A[r][col] != 0:
                fac = A[r][col]
                A[r] = [a - fac*b for a, b in zip(A[r], A[col])]
    return [A[r][N] for r in range(N)]

def main():
    out = []
    def log(s):
        print(s); out.append(s)

    log("=== ref01: Lemma 1 independent validation (hostile referee) ===")
    # R1: brute force n=2..5
    ok_all = True
    for n in (2, 3, 4, 5):
        t0 = time.time()
        bf = bruteforce_poly(n)              # E[#cyclic](q)
        lm = lemma1_poly(n)                  # n*phi = sum A_k
        same = (bf == lm)
        ok_all &= same
        log(f"[R1] n={n}: brute-force poly deg {n} vs Lemma-1 poly: "
            f"{'IDENTICAL' if same else 'MISMATCH'}  ({time.time()-t0:.1f}s)")
        if not same:
            log(f"      bf = {bf}")
            log(f"      lm = {lm}")
    # R2: q=1 endpoint vs Q(n)/n, n=1..400
    bad = 0
    for n in range(1, 401):
        # Lemma 1 at q=1: (1/n) sum_k prod_{i=1}^k (n-k+i)/n  == Q(n)/n
        s = Fraction(0)
        for k in range(1, n+1):
            P = Fraction(1)
            for i in range(1, k+1):
                P *= Fraction(n-k+i, n)
            s += P
        if s != Qn_exact(n):
            bad += 1
    log(f"[R2] q=1 endpoint vs exact Ramanujan Q(n)/n, n=1..400: "
        f"{'0 mismatches' if bad==0 else f'{bad} MISMATCHES'}")
    ok_all &= (bad == 0)
    # NOTE (referee): R2 is algebraically near-tautological (Lemma 1 at q=1
    # IS the Q(n) sum); the load-bearing test is R1.
    # R3: mixture inversion n=6..10
    for n in range(6, 11):
        lm = lemma1_poly(n)
        phi_poly = [c / n for c in lm]      # phi(n,qn) polynomial
        phiK = bernstein_invert(n, phi_poly)
        ref = {
            0: Fraction(1),
            1: Fraction(2,3) + Fraction(1, 3*n*n),
            2: Fraction(8,15) + Fraction(1,30*n) + Fraction(7,10*n*n)
               + Fraction(1,5*n**3),
            3: Fraction(16,35) + Fraction(1,14*n) + Fraction(11,10*n*n)
               + Fraction(23,35*n**3) + Fraction(6,35*n**4),
            n: Qn_exact(n)/n,
        }
        res = []
        for K, v in sorted(ref.items()):
            match = (phiK[K] == v)
            ok_all &= match
            res.append(f"K={K}:{'OK' if match else 'FAIL'}")
        log(f"[R3] n={n}: Bernstein inversion of Lemma-1 poly vs archive "
            f"closed forms -> {' '.join(res)}")
    log(f"=== ref01 VERDICT: {'ALL CHECKS PASS' if ok_all else 'FAILURES FOUND'} ===")
    with open(__file__.replace('.py', '.log'), 'w') as fh:
        fh.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
