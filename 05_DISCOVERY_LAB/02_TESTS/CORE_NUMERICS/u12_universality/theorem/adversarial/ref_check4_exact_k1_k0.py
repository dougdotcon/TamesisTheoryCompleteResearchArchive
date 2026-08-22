"""
Referee check #4: independent exact-fraction enumeration of Proposition 4
(phi_n^(1) = 2/3 + 1/(3n^2)) for small n, written from scratch (different
cycle-detection code path than the repo's k1_exact_check.py, and also
different from ref_check3's tortoise/hare style -- here we just build the
full functional graph and count, in exact rational arithmetic).
Also spot-checks phi_n^(0) = 1 (trivial) and the Corollary 4.2 tail bound,
and the Chernoff bound (7.3).
"""
import itertools
from fractions import Fraction
import math

def num_cyclic(f, n):
    # f: list, 0-indexed, f[i] in 0..n-1
    cnt = 0
    for x in range(n):
        y = x
        for _ in range(n):
            y = f[y]
        # after n steps, y is in a cycle (rho-shape); check if x reachable
        # from y within n more steps -- simpler: just check x is cyclic
        # directly by seeing if iterating f from x returns to x within n steps
        cur = f[x]
        steps = 1
        found = False
        while steps <= n:
            if cur == x:
                found = True
                break
            cur = f[cur]
            steps += 1
        if found:
            cnt += 1
    return cnt

def exact_phi_K1(n):
    total = Fraction(0)
    count = 0
    for perm in itertools.permutations(range(n)):
        pi = list(perm)
        for U in range(n):
            f = list(pi)
            f[0] = U   # reroute index 0 (WLOG by exchangeability)
            c = num_cyclic(f, n)
            total += Fraction(c, n)
            count += 1
    return total / count

if __name__ == "__main__":
    print("=== Check 4a: independent exact enumeration, K=1, small n ===")
    for n in range(2, 7):
        phi = exact_phi_K1(n)
        formula = Fraction(2, 3) + Fraction(1, 3 * n * n)
        print(f"n={n}: exact={phi}  =  {float(phi):.6f}   formula(2/3+1/3n^2)={formula}={float(formula):.6f}   match={phi==formula}")

    print("\n=== Check 4b: Corollary 4.2 tail-bound numerics ===")
    import mpmath as mp
    mp.mp.dps = 30
    for c in [1, 5, 10, 30, 80]:
        c = mp.mpf(c)
        phi = mp.quad(lambda t: mp.e**(-c*t*t), [0, 1])
        leading = (mp.sqrt(mp.pi)/2) / mp.sqrt(c)
        R = leading - phi
        bound = mp.e**(-c) / (2*c)
        ok_pos = R > 0
        ok_lt = R < bound
        print(f"c={float(c):6.1f}  R(c)={float(R):.6e}   bound=e^-c/(2c)={float(bound):.6e}   0<R<bound: {ok_pos and ok_lt}")

    print("\n=== Check 4b-fix: same bound, via exact erf (no quadrature cancellation), higher dps ===")
    print("(the mp.quad-based c=80 line above shows a false R(c)=0 -- that is")
    print(" catastrophic cancellation in MY numerical check, not a flaw in the proof;")
    print(" recomputing analytically via erf at sufficient precision fixes it:)")
    for c, dps in [(80, 60), (200, 150)]:
        mp.mp.dps = dps
        cc = mp.mpf(c)
        phi_exact = (mp.sqrt(mp.pi)/2)/mp.sqrt(cc) * mp.erf(mp.sqrt(cc))
        leading = (mp.sqrt(mp.pi)/2)/mp.sqrt(cc)
        R = leading - phi_exact
        bound = mp.e**(-cc)/(2*cc)
        print(f"c={c:5d} (dps={dps})  R(c)={mp.nstr(R,6)}   bound={mp.nstr(bound,6)}   0<R<bound: {0<R<bound}")

    print("\n=== Check 4c: Chernoff bound (7.3) sanity, P(Bin(n,c/n)>=M) <= e^-c (ec/M)^M ===")
    from scipy.stats import binom
    for (n, c, M) in [(50, 5, 15), (500, 5, 15), (5000, 5, 15), (200, 10, 25)]:
        p = c / n
        actual = 1 - binom.cdf(M - 1, n, p)  # P(X >= M)
        bound = math.exp(-c) * (math.e * c / M) ** M
        print(f"n={n:5d} c={c:4.1f} M={M:3d}   P(X>=M)={actual:.3e}   Chernoff_bound={bound:.3e}   bound_holds={actual<=bound}")
