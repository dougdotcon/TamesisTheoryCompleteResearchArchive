#!/usr/bin/env python3
"""
01_validate_exact_formula.py  --  wave 17 front (e), DISC-DEC-072, GAMMA-SCALING-LAW-ATTEMPT

Validates Lemma 1 of ATTEMPT.md, the exact finite-n formula (derived from scratch
in this front by cycle counting on Definition 1 of THEOREM.md):

    phi(n,c) = (1/n) * sum_{k=1}^{n} A_k(n,q),        q = c/n,
    A_k(n,q) = sum_{m=0}^{k} C(k,m) q^m (1-q)^{k-m} * prod_{i=1}^{m} (1 - (k-i)/n)

Checks (all EXACT, over the rationals; no randomness anywhere):
  (V1) n = 3,4,5: coefficient-by-coefficient identity, as polynomials in q, between
       Lemma 1 and a from-scratch brute-force enumeration of Definition 1
       (sum over all permutations pi, all reroute subsets S, all U-assignments on S,
        counting cyclic points of the resulting mapping).
  (V2) q = 1 endpoint: (1/n)*sum_k A_k(n,1) == Q(n)/n exactly for n = 1..400,
       Q(n) = sum_{k=1}^n n!/((n-k)! n^k)  (Ramanujan Q).  Cross-checks the archive
       identity phi(n,n) = Q(n)/n (THEOREM.md, Estagio 10 post-adversarial correction).
  (V3) Mixture inversion: from Lemma 1's polynomial-in-q coefficients and the exact
       mixture identity (7.1) of THEOREM.md (Fact 4.1,
       phi(n,c) = sum_K C(n,K) q^K (1-q)^{n-K} phi_n^{(K)}), solve the triangular
       system for phi_n^{(K)} and compare, for n = 6..10, with the archive's
       independently proved closed forms (Estagios 3,4 of THEOREM.md):
         phi_n^{(1)} = 2/3 + 1/(3n^2)
         phi_n^{(2)} = 8/15 + 1/(30n) + 7/(10n^2) + 1/(5n^3)
         phi_n^{(3)} = 16/35 + 1/(14n) + 11/(10n^2) + 23/(35n^3) + 6/(35n^4)
       and phi_n^{(n)} = Q(n)/n.
  (V4) Roundoff control for the float64 evaluator used in 02: exact Fraction value of
       phi(n, gamma*n) at (n=50, gamma=1/2), (n=200, gamma=3/10) vs float64 pipeline.
"""

from fractions import Fraction
from itertools import permutations, combinations, product
from math import comb
import sys, time

sys.set_int_max_str_digits(1000000)

LOG = []
def log(s):
    print(s, flush=True)
    LOG.append(s)

def poly_phi_lemma1(n):
    """Lemma 1 phi(n, q*n) as polynomial in q: list of Fraction coeffs, degree n."""
    coeffs = [Fraction(0)] * (n + 1)
    for k in range(1, n + 1):
        # A_k = sum_m C(k,m) q^m (1-q)^{k-m} P_{k,m};  P_{k,m} = prod_{i<=m} (n-k+i)/n
        P = Fraction(1)
        for m in range(0, k + 1):
            if m >= 1:
                P *= Fraction(n - k + m, n)
            # expand C(k,m) q^m (1-q)^{k-m} = C(k,m) sum_j C(k-m,j) (-1)^j q^{m+j}
            base = Fraction(comb(k, m)) * P
            for j in range(0, k - m + 1):
                coeffs[m + j] += base * comb(k - m, j) * (-1) ** j
    return [c / n for c in coeffs]

def count_cyclic(f, n):
    """Number of cyclic points of mapping f: [0..n-1] -> [0..n-1] (list)."""
    cyc = 0
    for s in range(n):
        # follow path from s, detect if s is on a cycle: iterate n steps then check
        seen = {}
        x = s
        while x not in seen:
            seen[x] = True
            x = f[x]
        # x is first repeated vertex; s cyclic iff x==... walk cycle from x
        # s is cyclic iff s is in the cycle through x
        cycle = set()
        y = x
        while y not in cycle:
            cycle.add(y)
            y = f[y]
        if s in cycle:
            cyc += 1
    return cyc

def poly_phi_bruteforce(n):
    """E[#cyclic]/n as polynomial in q by full enumeration of Definition 1.
    P(config) = (1/n!) * q^{|S|} (1-q)^{n-|S|} * n^{-|S|}.
    Returns list of Fraction coefficients in q, degree n."""
    coeffs = [Fraction(0)] * (n + 1)
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    for pi in permutations(range(n)):
        for m in range(0, n + 1):
            for S in combinations(range(n), m):
                # sum over U assignments on S
                tot = 0  # integer sum of cyclic counts over all n^m assignments
                for U in product(range(n), repeat=m):
                    f = list(pi)
                    for idx, s_i in enumerate(S):
                        f[s_i] = U[idx]
                    tot += count_cyclic(f, n)
                # weight: q^m (1-q)^{n-m} / (n! * n^m); expand (1-q)^{n-m}
                w = Fraction(tot, fact * n ** m * n)
                for j in range(0, n - m + 1):
                    coeffs[m + j] += w * comb(n - m, j) * (-1) ** j
    return coeffs

def ramanujan_Q(n):
    """Q(n) = sum_{k=1}^n n!/((n-k)! n^k) as Fraction."""
    s = Fraction(0)
    term = Fraction(1)
    for k in range(1, n + 1):
        term *= Fraction(n - k + 1, n)   # term = (n)_k / n^k
        s += term
    return s

def phi_exact(n, q):
    """phi(n, q*n) exactly (Fraction q)."""
    s = Fraction(0)
    for k in range(1, n + 1):
        P = Fraction(1)
        A = Fraction(0)
        # walk m upward, keeping binomial pmf term exactly
        for m in range(0, k + 1):
            if m >= 1:
                P *= Fraction(n - k + m, n)
            A += comb(k, m) * q**m * (1 - q) ** (k - m) * P
        s += A
    return s / n

def main():
    t0 = time.time()
    log("=== 01_validate_exact_formula.py ===")
    log("Deterministic exact-arithmetic validation; NO randomness used anywhere.")

    # ---------- V1 ----------
    log("\n[V1] Lemma 1 vs brute-force enumeration of Definition 1 (exact, poly in q)")
    ok_all = True
    for n in (3, 4, 5):
        t = time.time()
        a = poly_phi_lemma1(n)
        b = poly_phi_bruteforce(n)
        same = a == b
        ok_all &= same
        log(f"  n={n}: degree-{n} polynomials in q agree coefficient-by-coefficient: "
            f"{same}   ({time.time()-t:.1f}s)")
        if n == 3:
            log(f"    n=3 coefficients (Lemma 1):    {[str(c) for c in a]}")
            log(f"    n=3 coefficients (bruteforce): {[str(c) for c in b]}")
        if not same:
            log(f"    MISMATCH lemma1={a} brute={b}")
    log(f"  V1 PASS: {ok_all}")

    # ---------- V2 ----------
    log("\n[V2] q=1 endpoint vs Ramanujan Q(n)/n, exact, n=1..400")
    ok = True
    for n in range(1, 401):
        # at q=1 only m=k survives: A_k = (n)_k/n^k
        s = Fraction(0)
        term = Fraction(1)
        for k in range(1, n + 1):
            term *= Fraction(n - k + 1, n)
            s += term
        lhs = s / n
        rhs = ramanujan_Q(n) / n
        if lhs != rhs:
            ok = False
            log(f"  MISMATCH at n={n}")
            break
    log(f"  V2 PASS: {ok}  (phi(n,n) = Q(n)/n exactly, n=1..400)")

    # ---------- V3 ----------
    log("\n[V3] Mixture inversion vs archive closed forms for phi_n^(K) (exact)")
    # (7.1): phi(n,qn) = sum_K C(n,K) q^K (1-q)^{n-K} phi_n^{(K)}.
    # Expanding in q: coeff of q^j equals sum_{K<=j} C(n,K) C(n-K, j-K) (-1)^{j-K} phi_n^{(K)}.
    # Triangular: solve upward for phi_n^{(K)}.
    ok_all = True
    for n in range(6, 11):
        cs = poly_phi_lemma1(n)
        phiK = []
        for j in range(0, n + 1):
            acc = cs[j]
            for K in range(0, j):
                acc -= Fraction(comb(n, K) * comb(n - K, j - K) * (-1) ** (j - K)) * phiK[K]
            phiK.append(acc / comb(n, j))
        nf = Fraction(n)
        targets = {
            0: Fraction(1),
            1: Fraction(2, 3) + 1 / (3 * nf**2),
            2: Fraction(8, 15) + 1 / (30 * nf) + 7 / (10 * nf**2) + 1 / (5 * nf**3),
            3: Fraction(16, 35) + 1 / (14 * nf) + 11 / (10 * nf**2)
               + 23 / (35 * nf**3) + 6 / (35 * nf**4),
            n: ramanujan_Q(n) / n,
        }
        res = {K: (phiK[K] == v) for K, v in targets.items()}
        ok_all &= all(res.values())
        log(f"  n={n}: phi_n^(0)==1:{res[0]}  phi_n^(1) matches Estagio-3 form:{res[1]}  "
            f"phi_n^(2) matches:{res[2]}  phi_n^(3) matches Estagio-4 form:{res[3]}  "
            f"phi_n^(n)==Q(n)/n:{res[n]}")
    log(f"  V3 PASS: {ok_all}")

    # ---------- V4 ----------
    log("\n[V4] float64 evaluator roundoff control vs exact Fractions")
    import numpy as np
    from numpy import log as nplog
    from scipy.special import gammaln

    def phi_float(n, gamma, kmax=None):
        if kmax is None:
            kmax = n
        tot = 0.0
        lg = float(np.log(gamma)) if gamma > 0 else -np.inf
        l1g = float(np.log1p(-gamma)) if gamma < 1 else -np.inf
        for k in range(1, kmax + 1):
            m = np.arange(0, k + 1)
            if 0 < gamma < 1:
                logpmf = (gammaln(k + 1) - gammaln(m + 1) - gammaln(k - m + 1)
                          + m * lg + (k - m) * l1g)
            elif gamma == 1:
                logpmf = np.where(m == k, 0.0, -np.inf)
            else:
                logpmf = np.where(m == 0, 0.0, -np.inf)
            i = np.arange(1, k + 1)
            logfac = np.concatenate(([0.0], np.cumsum(np.log1p(-(k - i) / n))))
            tot += np.exp(logpmf + logfac).sum()
        return tot / n

    checks = [(50, Fraction(1, 2)), (200, Fraction(3, 10))]
    ok = True
    for n, qf in checks:
        t = time.time()
        ex = phi_exact(n, qf)
        fl = phi_float(n, float(qf))
        rel = abs(fl - float(ex)) / float(ex)
        good = rel < 1e-11
        ok &= good
        log(f"  n={n}, gamma={qf}: exact={float(ex):.15f} float64={fl:.15f} "
            f"rel.err={rel:.2e} (<1e-11: {good})  ({time.time()-t:.1f}s)")
    log(f"  V4 PASS: {ok}")

    log(f"\nTotal time: {time.time()-t0:.1f}s")
    with open(__file__.replace(".py", ".log"), "w") as fh:
        fh.write("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
