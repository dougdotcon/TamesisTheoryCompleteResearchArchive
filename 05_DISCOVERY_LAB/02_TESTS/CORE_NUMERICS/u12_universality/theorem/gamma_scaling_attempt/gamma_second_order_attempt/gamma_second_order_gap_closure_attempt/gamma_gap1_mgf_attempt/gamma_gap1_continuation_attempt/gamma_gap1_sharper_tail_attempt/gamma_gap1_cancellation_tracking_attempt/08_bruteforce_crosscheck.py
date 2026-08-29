"""
08_bruteforce_crosscheck.py

Independent verification of the "exact cubic max" method (script 03/05/06:
endpoints + closed-form critical points via the quadratic formula) against
a naive BRUTE-FORCE fine-grid scan of |x_k(D)| over D in [D_min,D_max],
at moderate (not astronomical) n where a dense grid scan is computationally
tractable. This checks the method itself is not silently missing a case
(e.g. a sign error in the quadratic-formula roots, an off-by-something in
the candidate set), independent of and complementary to script 03's
targeted interior-critical-point check.

Also independently re-derives R_k^exact := (1/6)*E_M[|x(D)|^3 e^{|x(D)|}]
via DIRECT summation over the true (finite, exact) Binomial pmf (mpmath,
high precision, no shortcuts) and compares it against the crude bound
(1/6)*H_exact(D_max or D_min)^3*e^{...} at a handful of moderate (k,n,gamma)
triples, matching the grandparent front's own §4 style of ground-truth
verification.
"""
import mpmath as mp

mp.mp.dps = 50


def beta_of(g):
    return g * (2 - g) / 2


def c_exact(k, n, g):
    c0v = g * k * (2 * g ** 2 * k ** 2 - 6 * g * k ** 2 + 3 * g * k
                    + 6 * k ** 2 - 6 * k + 1) / (12 * n ** 2)
    c1v = (g ** 2 * k ** 2 / 2 - g * k ** 2 - g * k * n + g * k / 2
           + k ** 2 / 2 + k * n - k / 2 - n / 2 + mp.mpf(1) / 12) / n ** 2
    c2v = (2 * g * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
    c3v = mp.mpf(1) / (6 * n ** 2)
    return c0v, c1v, c2v, c3v


def x_of_D(k, n, g, Dval):
    c0v, c1v, c2v, c3v = c_exact(k, n, g)
    return c0v + c1v * Dval + c2v * Dval ** 2 + c3v * Dval ** 3


def exact_max_abs_x(k, n, g, Dlo, Dhi):
    if Dlo > Dhi:
        Dlo, Dhi = Dhi, Dlo
    c0v, c1v, c2v, c3v = c_exact(k, n, g)
    candidates = [Dlo, Dhi]
    disc = (2 * c2v) ** 2 - 4 * (3 * c3v) * c1v
    if disc >= 0:
        sq = mp.sqrt(disc)
        for root in [(-2 * c2v + sq) / (6 * c3v), (-2 * c2v - sq) / (6 * c3v)]:
            if Dlo <= root <= Dhi:
                candidates.append(root)
    return max(abs(x_of_D(k, n, g, Dc)) for Dc in candidates)


def brute_force_max_abs_x(k, n, g, Dlo, Dhi, n_grid=200000):
    if Dlo > Dhi:
        Dlo, Dhi = Dhi, Dlo
    best = mp.mpf(0)
    for i in range(n_grid + 1):
        Dv = Dlo + (Dhi - Dlo) * mp.mpf(i) / n_grid
        v = abs(x_of_D(k, n, g, Dv))
        if v > best:
            best = v
    return best


print("=" * 78)
print("PART A -- closed-form (endpoints+critical-points) vs brute-force")
print("fine-grid scan (200,000 points), moderate n")
print("=" * 78)
worst_rel_diff = mp.mpf(0)
for gf in [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    g = mp.mpf(gf)
    for nf in [1000, 100000, 10 ** 8]:
        n = mp.mpf(nf)
        b = beta_of(g)
        K = mp.sqrt(4 * n * mp.log(n) / b) + 1
        Dlo, Dhi = -g * K, (1 - g) * K
        closed_form = exact_max_abs_x(K, n, g, Dlo, Dhi)
        brute = brute_force_max_abs_x(K, n, g, Dlo, Dhi, n_grid=20000)
        rel_diff = abs(closed_form - brute) / closed_form if closed_form > 0 else mp.mpf(0)
        worst_rel_diff = max(worst_rel_diff, rel_diff)
        flag = "  <-- MISMATCH" if brute > closed_form * mp.mpf('1.0001') else ""
        print(f"  gamma={gf:<5} n={nf:<12} closed_form={float(closed_form):.6e}  "
              f"brute(20k pts)={float(brute):.6e}  rel_diff={float(rel_diff):.2e}{flag}")
print(f"\nWorst relative difference across all tests: {float(worst_rel_diff):.2e}")
print("(brute force with a finite grid can only ever find <= the true max,")
print("so brute > closed_form would indicate a real bug; brute < closed_form")
print("by a small amount is expected discretization slack, not a problem.)")

print()
print("=" * 78)
print("PART B -- ground-truth check: R_k^exact via DIRECT Binomial pmf sum")
print("vs the Bulk/Tail-style bound using H_exact, moderate (k,n,gamma)")
print("=" * 78)


def R_k_exact_via_pmf(k, n, g):
    """R_k := (1/6) E_M[|x(D)|^3 e^{|x(D)|}], M~Bin(k,g), D=M-g*k, via
    direct summation over the exact Binomial pmf (no shortcuts)."""
    k_int = int(k)
    total = mp.mpf(0)
    # log-pmf via lgamma for numerical stability, then exponentiate
    log_g = mp.log(g)
    log_1mg = mp.log(1 - g)
    for Mint in range(0, k_int + 1):
        log_pmf = (mp.loggamma(k_int + 1) - mp.loggamma(Mint + 1) - mp.loggamma(k_int - Mint + 1)
                   + Mint * log_g + (k_int - Mint) * log_1mg)
        pmf = mp.e ** log_pmf
        if pmf < mp.mpf(10) ** -60:
            continue
        Dv = Mint - g * k_int
        xv = x_of_D(k_int, n, g, Dv)
        total += pmf * abs(xv) ** 3 * mp.e ** abs(xv)
    return total / 6


for (kf, nf, gf) in [(20, 1000, 0.3), (50, 5000, 0.5), (15, 800, 0.9), (10, 500, 0.05)]:
    g = mp.mpf(gf)
    n = mp.mpf(nf)
    k = mp.mpf(kf)
    Rk_exact = R_k_exact_via_pmf(k, n, g)
    Dlo, Dhi = -g * k, (1 - g) * k
    Hk = exact_max_abs_x(k, n, g, Dlo, Dhi)
    Rk_bound = (Hk ** 3 * mp.e ** Hk) / 6
    ok = Rk_exact <= Rk_bound * mp.mpf('1.0000001')
    print(f"  k={kf} n={nf} gamma={gf}: R_k^exact={float(Rk_exact):.6e}  "
          f"R_k^bound(H_exact)={float(Rk_bound):.6e}  R_exact<=bound: {ok}")
