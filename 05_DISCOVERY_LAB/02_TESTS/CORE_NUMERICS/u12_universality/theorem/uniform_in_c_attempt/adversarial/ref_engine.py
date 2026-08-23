"""
Adversarial referee, independent engine.

Written from scratch from THEOREM.md Definition 1 and from the PROSE of
ATTEMPT.md 2.1 only.  No script in the parent directory was read before this
file was written and run.

Contents
--------
raw_phi(n, q)      : brute-force enumeration of the RAW Definition-1 model.
chain_phi(n, q)    : the (j,R) orbit-chain recursion of ATTEMPT.md (2.1).
chain_phiK(n, K)   : the conditional-K version (Definition 4).
Everything is exact (fractions.Fraction).
"""

from fractions import Fraction as F
from itertools import permutations, product
from functools import lru_cache


# ----------------------------------------------------------------------
# 1. RAW model, brute force, exact.
# ----------------------------------------------------------------------
def raw_phi(n, q):
    """P(1 is cyclic under f) computed by exhaustive enumeration of
    Definition 1: pi uniform on S_n, xi_i iid Bern(q), f(x)=U_x (uniform on
    [n]) if xi_x=1 else pi(x).

    Sum over pi (n! terms), over the mark-subset S (2^n terms) weighted
    q^|S| (1-q)^(n-|S|), and over the reroute targets (n^|S| terms) each
    weighted 1/n^|S|.  Points are labelled 0..n-1; point 0 plays the role
    of '1'.
    """
    q = F(q)
    nf = 1
    for i in range(1, n + 1):
        nf *= i
    total = F(0)
    pts = list(range(n))
    for pi in permutations(pts):
        for mask in range(1 << n):
            S = [i for i in pts if (mask >> i) & 1]
            k = len(S)
            w_mask = q**k * (1 - q) ** (n - k)
            if w_mask == 0:
                continue
            cyc_count = 0
            for targets in product(pts, repeat=k):
                f = list(pi)
                for idx, i in enumerate(S):
                    f[i] = targets[idx]
                # is 0 on a cycle?  follow the orbit of 0 for n steps.
                x = 0
                for _ in range(n):
                    x = f[x]
                    if x == 0:
                        cyc_count += 1
                        break
            total += w_mask * F(cyc_count, n**k)
    return total / nf


# ----------------------------------------------------------------------
# 2. The (j,R) orbit chain of ATTEMPT.md 2.1, re-derived and coded here.
# ----------------------------------------------------------------------
def chain_phi(n, q):
    """phi(n,c) with q = c/n, via the backward pass on (j,R)."""
    q = F(q)
    if n == 1:
        # single point: f(1)=U_1=1 always (reroute) or pi(1)=1: cyclic w.p. 1
        return F(1)
    # terminal layer j = n-1
    P = {R: q * F(1, n) + (1 - q) * F(1, R + 1) for R in range(n)}
    for j in range(n - 2, -1, -1):
        newP = {}
        for R in range(j + 1):
            av = n - j + R                       # available pi-targets
            term = q * (F(1, n) + F(n - j - 1, n) * P[R + 1])
            term += (1 - q) * (F(1, av) + F(n - j - 1, av) * P[R])
            newP[R] = term
        P = newP
    return P[0]


def chain_phiK(n, K):
    """phi_n^{(K)}: exactly K of the n points are rerouted, the rerouted set
    being a uniform K-subset.  Same exploration; the branch weight at step j
    with R reroutes already seen is (K-R)/(n-j) (sampling without
    replacement among the n-j points whose mark is not yet revealed).

    Careful bookkeeping: at state (j,R) we have revealed the marks of
    x_0,...,x_{j-1} (the j points we have already STEPPED FROM), of which R
    were reroutes.  We are about to reveal the mark of x_j.  The number of
    points with unrevealed marks is n-j, and K-R of them are rerouted.
    """
    if K > n:
        raise ValueError
    if n == 1:
        return F(1)
    P = {}
    for R in range(n):
        # j = n-1: reveal mark of x_{n-1}; n-(n-1) = 1 unrevealed point
        # so it is a reroute iff K-R == 1.
        qq = F(K - R, 1) if (K - R) in (0, 1) else None
        if K - R < 0 or K - R > 1:
            P[R] = None
            continue
        qq = F(K - R)          # 0 or 1
        P[R] = qq * F(1, n) + (1 - qq) * F(1, R + 1)
    for j in range(n - 2, -1, -1):
        newP = {}
        for R in range(j + 1):
            rem = K - R
            if rem < 0 or rem > n - j:
                newP[R] = None
                continue
            qq = F(rem, n - j)
            a = P[R + 1] if R + 1 in P and P[R + 1] is not None else F(0)
            b = P[R] if P[R] is not None else F(0)
            av = n - j + R
            term = qq * (F(1, n) + F(n - j - 1, n) * a)
            term += (1 - qq) * (F(1, av) + F(n - j - 1, av) * b)
            newP[R] = term
        P = newP
    return P[0]


# ----------------------------------------------------------------------
# 3. float version of chain_phi for large n (audited separately)
# ----------------------------------------------------------------------
def chain_phi_float(n, q):
    import numpy as np
    q = float(q)
    if n == 1:
        return 1.0
    R = np.arange(n, dtype=np.float64)
    P = q / n + (1.0 - q) / (R + 1.0)
    for j in range(n - 2, -1, -1):
        Rv = np.arange(j + 1, dtype=np.float64)
        av = n - j + Rv
        P = q * (1.0 / n + (n - j - 1) / n * P[1:j + 2]) \
            + (1.0 - q) * (1.0 / av + (n - j - 1) / av * P[0:j + 1])
    return float(P[0])


if __name__ == "__main__":
    print("=" * 72)
    print("A. RAW Definition-1 enumeration  vs  (j,R) chain   [exact]")
    print("=" * 72)
    ok = True
    for n in (2, 3, 4):
        for q in (F(0), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(1)):
            a = raw_phi(n, q)
            b = chain_phi(n, q)
            flag = "OK " if a == b else "MISMATCH"
            if a != b:
                ok = False
            print(f"  n={n} q={str(q):>5}  raw={str(a):>28}  chain={str(b):>28}  {flag}")
    print("  ALL MATCH" if ok else "  *** FAILURE ***")

    print()
    print("=" * 72)
    print("B. phi_n^{(K)} engine vs archive-published values (cited in ATTEMPT 2.3)")
    print("=" * 72)
    print("  phi_n^{(0)} = 1 ?", all(chain_phiK(n, 0) == 1 for n in range(1, 10)))
    print("  phi_n^{(1)} = 2/3 + 1/(3n^2) ?",
          all(chain_phiK(n, 1) == F(2, 3) + F(1, 3 * n * n) for n in range(1, 11)))
    tab = {2: F(3, 4), 3: F(17, 27), 4: F(113, 192), 5: F(356, 625),
           6: F(151, 270), 7: F(569, 1029), 8: F(281, 512)}
    print("  phi_n^{(2)} table n=2..8 ?",
          all(chain_phiK(n, 2) == v for n, v in tab.items()))
    print("  phi_7^{(6)} = 355081/823543 ?", chain_phiK(7, 6) == F(355081, 823543),
          "  got", chain_phiK(7, 6))

    print()
    print("=" * 72)
    print("C. mixture identity phi(n,c) = E_{K~Bin(n,c/n)}[phi_n^{(K)}]  [exact]")
    print("=" * 72)
    from math import comb
    ok = True
    for n in range(2, 8):
        for q in (F(1, 5), F(1, 3), F(1, 2), F(3, 4)):
            mix = sum(F(comb(n, K)) * q**K * (1 - q)**(n - K) * chain_phiK(n, K)
                      for K in range(n + 1))
            direct = chain_phi(n, q)
            if mix != direct:
                ok = False
                print("  MISMATCH", n, q, mix, direct)
    print("  mixture identity exact for n=2..7, 4 values of q each:", ok)

    print()
    print("=" * 72)
    print("D. phi(n,n) = Q(n)/n exactly  (Prop 7.1), n=1..11")
    print("=" * 72)
    ok = True
    for n in range(1, 12):
        Q = F(0)
        prod = F(1)
        j = 0
        while True:
            Q += prod
            j += 1
            if j > n:
                break
            prod *= (1 - F(j, n))
            if prod == 0:
                break
        lhs = chain_phi(n, F(1))
        rhs = Q / n
        if lhs != rhs:
            ok = False
        print(f"  n={n:2d}  phi(n,n)={str(lhs):>26}   Q(n)/n={str(rhs):>26}  "
              f"{'OK' if lhs == rhs else 'MISMATCH'}")
    print("  ALL MATCH" if ok else "  *** FAILURE ***")
