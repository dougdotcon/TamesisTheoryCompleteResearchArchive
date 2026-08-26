"""
The H_{2k-1}(r,b) machine, at CONCRETE integer (r,b).

Ingredient chain (all cited/PROVED input, per the task mandate's step 6
and step 10 -- reproduced here from the mathematical description in
THEOREM.md "Estagio 21" / the wave-16 predecessor's referee report,
which the target document itself cites verbatim and uses directly):

  H_{2k-1}(r,b) := P_b * S_{2k-1}(N,r),  N = 2r+b+1,  P_b = r!(r+b)!/N!

  S_1(N,m) = (m+1) C(N,m+1)
  S_{2k-1}(N,m) = (N-2m)^{2k-2}(m+1)C(N,m+1)
                  + 2N * sum_{s odd, 1<=s<=2k-3} C(2k-2,s) S_s(N-1,m-1)

Using the wave-16 referee's cited closed factorization
S_{2k-1}(N,m) = A_k(N,m) * C(N,m+1), A_1(N,m):=m+1, and the elementary
identity C(N-1,m) = (m+1)/N * C(N,m+1), one gets (cited, used directly,
NOT re-derived from first principles here -- this is exactly the
"already-PROVED input" the task mandate names):

  A_k(N,m) = (m+1) [ (N-2m)^{2k-2}
                      + 2 sum_{s odd,1<=s<=2k-3} C(2k-2,s) A_{(s+1)/2}(N-1,m-1) ]

  a_k^{(d)}(r) := A_k(N-d, r-d)   (depth-d partial unrolling, N=2r+b+1)

  a_k^{(d)}(r) = (r-d+1) [ (beta+d)^{2k-2}
                    + 2 sum_{s odd,1<=s<=2k-3} C(2k-2,s) a_{(s+1)/2}^{(d+1)}(r) ]
  a_1^{(d)}(r) = r-d+1,   beta := b+1

  H_{2k-1}(r,b) = a_k^{(0)}(r) / (r+1)

This module implements the a_k^{(d)} recursion (memoized per (r,beta)
call), AND a completely independent brute-force cross-check that
evaluates S_{2k-1}(N,m) directly from its ORIGINAL recursive
definition above (no A_k factorization at all), so that a bug in the
A_k-based fast route cannot be masked by a shared implementation error.

Written fresh by the referee. No predecessor .py file was read or used.
"""
from fractions import Fraction
from math import comb


def a_k_table(r, beta, k_max):
    """Returns dict {(k,d): a_k^{(d)}(r)} for k=1..k_max, computed via
    the recursion above, memoized for this (r,beta) call."""
    cache = {}

    def a(k, d):
        key = (k, d)
        if key in cache:
            return cache[key]
        if k == 1:
            val = r - d + 1
        else:
            bracket = (beta + d) ** (2 * k - 2)
            s = 1
            while s <= 2 * k - 3:
                bracket += 2 * comb(2 * k - 2, s) * a((s + 1) // 2, d + 1)
                s += 2
            val = (r - d + 1) * bracket
        cache[key] = val
        return val

    for k in range(1, k_max + 1):
        a(k, 0)
    return cache


def H_odd_fast(k_max, r, b):
    """Returns dict {k: H_{2k-1}(r,b)} for k=1..k_max, exact Fraction,
    via the a_k^{(0)} recursion divided by (r+1)."""
    beta = b + 1
    table = a_k_table(r, beta, k_max)
    out = {}
    for k in range(1, k_max + 1):
        out[k] = Fraction(table[(k, 0)], r + 1)
    return out


# ---------------------------------------------------------------------
# Brute-force, from the ORIGINAL cited S_{2k-1}(N,m) recursion, with NO
# A_k factorization anywhere -- an independent cross-check route.
# ---------------------------------------------------------------------

def S_odd_direct(k, N, m):
    """S_{2k-1}(N,m) via direct recursive unrolling of the ORIGINAL
    cited recursion (no A_k factorization)."""
    if k == 1:
        return (m + 1) * comb(N, m + 1)
    if m < 0:
        return 0
    total = (N - 2 * m) ** (2 * k - 2) * (m + 1) * comb(N, m + 1)
    s = 1
    while s <= 2 * k - 3:
        total += 2 * N * comb(2 * k - 2, s) * S_odd_direct((s + 1) // 2, N - 1, m - 1)
        s += 2
    return total


def H_odd_bruteforce(k, r, b):
    N = 2 * r + b + 1
    Pb = Fraction(1)
    # P_b = r!(r+b)!/N!  -- compute directly, exact
    import math
    Pb = Fraction(math.factorial(r) * math.factorial(r + b), math.factorial(N))
    return Pb * S_odd_direct(k, N, r)


# Second, independent brute force: sum_{i=0}^{m} (N-2i)^{2k-1} C(N,i),
# the closed (non-recursive) definition the wave-16 referee's own
# brute-force cross-check used, verbatim.
def S_odd_sum_form(k, N, m):
    total = 0
    for i in range(0, m + 1):
        total += (N - 2 * i) ** (2 * k - 1) * comb(N, i)
    return total


def H_odd_sumform(k, r, b):
    import math
    N = 2 * r + b + 1
    Pb = Fraction(math.factorial(r) * math.factorial(r + b), math.factorial(N))
    return Pb * S_odd_sum_form(k, N, r)


# ---------------------------------------------------------------------
# Self tests
# ---------------------------------------------------------------------

def self_test():
    checks = 0
    fails = 0

    # (a) fast route vs brute-force recursive S_odd_direct
    for r in range(0, 10):
        for b in [0, 1, 2, 5, 8]:
            table = H_odd_fast(9, r, b)
            for k in range(1, 10):
                got = table[k]
                want = H_odd_bruteforce(k, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    print("FAIL fast vs brute (recursive) r,b,k=", r, b, k, got, want)

    # (b) fast route vs the closed sum-form brute-force (independent of
    # the recursion entirely)
    for r in range(0, 10):
        for b in [0, 1, 3, 7]:
            table = H_odd_fast(8, r, b)
            for k in range(1, 9):
                got = table[k]
                want = H_odd_sumform(k, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    print("FAIL fast vs brute (sum-form) r,b,k=", r, b, k, got, want)

    # (c) reproduce the two concrete base cases quoted in THEOREM.md /
    # the target document's own citation: H_1=1, H_3=(b+1)^2+4r
    for r in range(0, 15):
        for b in range(0, 6):
            table = H_odd_fast(2, r, b)
            checks += 1
            if table[1] != 1:
                fails += 1
                print("FAIL H_1 != 1 at r,b=", r, b, table[1])
            checks += 1
            want_H3 = (b + 1) ** 2 + 4 * r
            if table[2] != want_H3:
                fails += 1
                print("FAIL H_3 mismatch r,b=", r, b, table[2], want_H3)

    # (d) degree bound: deg_r H_{2k-1}(r,b) = k-1, leading coeff
    # 4^{k-1}(k-1)!, independent of b -- checked via (k)-th finite
    # difference vanishing and (k-1)-th finite difference matching.
    def finite_diff(vals, order):
        v = list(vals)
        for _ in range(order):
            v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
        return v

    import math as _m
    for k in range(1, 25):
        for b in [0, 1, 3, 7, 30]:
            npts = k + 3
            r0 = 5
            vals = []
            for r in range(r0, r0 + npts):
                table = H_odd_fast(k, r, b)
                vals.append(table[k])
            # (k)-th finite difference should vanish (degree <= k-1)
            fd_k = finite_diff(vals, k)
            checks += 1
            if any(x != 0 for x in fd_k):
                fails += 1
                print("FAIL degree bound (too high) k,b=", k, b, fd_k)
            # (k-1)-th finite difference should be constant = lead*(k-1)!
            fd_km1 = finite_diff(vals, k - 1) if k >= 1 else vals
            lead = Fraction(4 ** (k - 1) * _m.factorial(k - 1))
            fact_km1 = _m.factorial(k - 1)
            want_const = lead * fact_km1
            checks += 1
            if any(x != want_const for x in fd_km1):
                fails += 1
                print("FAIL leading coeff k,b=", k, b, fd_km1, want_const)

    print(f"odd_part.py self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = self_test()
    print("odd_part.py:", "OK" if ok else "FAILED")
