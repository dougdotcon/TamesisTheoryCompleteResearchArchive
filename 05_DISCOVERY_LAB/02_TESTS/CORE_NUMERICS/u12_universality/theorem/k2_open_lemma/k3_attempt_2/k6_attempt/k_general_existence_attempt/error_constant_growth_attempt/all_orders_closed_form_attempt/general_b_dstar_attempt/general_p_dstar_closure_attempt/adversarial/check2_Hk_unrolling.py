"""
Independent check of the H(power,depth) unrolling machine from ATTEMPT.md
Section 2.3, against the target T(power,depth) := P_b * S_power(N-depth, r-depth),
computed by BRUTE FORCE (no recursion at all) using exact Fraction arithmetic,
for concrete numeric (r,b), k up to 10 (power up to 19).

This is built entirely from scratch (not reading odd_part.py). It also serves
as a numeric check of the inductive proof (done by hand, see referee report)
that H(power,d) == P_b*S_power(N-d,r-d) for every power,d, which follows from
(E2) plus the cited S-recursion.
"""
from fractions import Fraction
from math import comb, factorial

def P_b_val(r, b, N):
    return Fraction(factorial(r) * factorial(r+b), factorial(N))

def S_bruteforce(power, N, m):
    if m < 0:
        return 0
    total = 0
    for i in range(0, m+1):
        total += (N - 2*i)**power * comb(N, i)
    return total

def falling(x, d):
    # x*(x-1)*...*(x-d+1), d factors; x can be an int here
    result = 1
    for t in range(d):
        result *= (x - t)
    return result

def H(power, d, r, b, N, beta):
    beta_local = beta + d
    N_d = N - d
    rd = r - d
    Nd_ff = falling(N, d)  # [N]_d
    rd_ff = falling(r, d)  # [r]_d
    term1 = Fraction(beta_local, 1) ** (power - 1) * Fraction(rd_ff, Nd_ff)
    if power == 1:
        return term1
    tail = Fraction(0)
    for s in range(1, power - 2 + 1, 2):
        tail += comb(power - 1, s) * H(s, d + 1, r, b, N, beta)
    return term1 + 2 * N_d * tail

def T(power, d, r, b, N):
    Pb = P_b_val(r, b, N)
    m = r - d
    Nd = N - d
    return Pb * S_bruteforce(power, Nd, m)

def run():
    checks = 0
    mismatches = 0
    test_points = []
    for r in [9, 10, 12, 15, 20, 25]:
        for b in [0, 1, 2, 3, 5, 8]:
            test_points.append((r, b))

    for (r, b) in test_points:
        N = 2*r + b + 1
        beta = b + 1
        for k in range(1, 11):  # power 1..19, k up to 10
            power = 2*k - 1
            if power > r:
                # H_k(r,b) definition requires S_{2k-1}(N,r); if power exceeds
                # available depth for recursion (d can go up to power-1 potentially
                # exceeding r), skip degenerate deep recursion beyond r to avoid
                # falling factorial hitting negative/zero r-d in a way not covered;
                # but structurally r-d can go negative -- falling factorial and
                # C(N-d, r-d+1) etc are still well-defined (falling factorial can
                # be 0). Let's NOT skip; just compute.
                pass
            hval = H(power, 0, r, b, N, beta)
            tval = T(power, 0, r, b, N)
            checks += 1
            if hval != tval:
                mismatches += 1
                print(f"MISMATCH r={r} b={b} k={k} power={power}: H={hval} T={tval}")
    print(f"H(power,0) vs brute-force P_b*S_power(N,r): {checks} checks, {mismatches} mismatches")

if __name__ == "__main__":
    run()
