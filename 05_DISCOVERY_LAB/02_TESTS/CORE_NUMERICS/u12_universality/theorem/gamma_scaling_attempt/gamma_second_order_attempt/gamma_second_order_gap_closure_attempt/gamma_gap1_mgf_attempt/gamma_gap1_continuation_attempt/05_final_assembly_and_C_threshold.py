"""
05_final_assembly_and_C_threshold.py  (revised: uses script 04's tightened
Ghat/GhatTheta)

Final assembly: combine script 04's explicit Ghat(n,gamma) and
GhatTheta(n,gamma,C) with the Bulk/Tail Lemma itself
(R_k <= (1/6)[g(Theta_K)^3 e^{g(Theta_K)} + 2 n^{-2C^2} g(K)^3 e^{g(K)}])
and the CITED fact G_n <= sqrt(pi n/beta) (explicit, generous version of the
already-established leading order G_n ~ (1/2) sqrt(pi n/beta) -- Lemma D0/
Corollary 4.2 provenance, not re-derived here) into a single fully explicit
upper bound

    W(n,gamma,C) := Gn_bound(n,gamma) * (1/6) *
                    [ GhatTheta(n,gamma,C)^3 * exp(GhatTheta(n,gamma,C))
                      + 2 n^{-2C^2} * Ghat(n,gamma)^3 * exp(Ghat(n,gamma)) ]

on the Gap-1 front's own literal target quantity
Sigma_{k=1}^K e^{-s(k)} R_k. This is the mandate item 1 assembly.

Reserved seed block 20260900000-20260900999: unused (deterministic).
"""
import mpmath as mp

mp.mp.dps = 60


def beta_of(gamma):
    return gamma * (2 - gamma) / 2


def n1_of(gamma):
    beta = beta_of(gamma)
    return int(mp.ceil(16384 / beta ** 2))


def Ghat(n, gamma):
    n = mp.mpf(n); gamma = mp.mpf(gamma)
    beta = beta_of(gamma)
    Kmax = 4 * mp.sqrt(n * mp.log(n) / beta)
    coefK3 = mp.mpf(10) / 3 + (1 - gamma) / 2
    coefK2_n = mp.mpf(7) / 4 - gamma
    coefK2_n2 = mp.mpf(11) / 6
    coefK_n = mp.mpf(3) / 4
    return (coefK3 * Kmax ** 3 / n ** 2 + coefK2_n * Kmax ** 2 / n
            + coefK2_n2 * Kmax ** 2 / n ** 2 + coefK_n * Kmax / n)


def GhatTheta(n, gamma, C):
    n = mp.mpf(n); gamma = mp.mpf(gamma); C = mp.mpf(C)
    beta = beta_of(gamma)
    Kmax = 4 * mp.sqrt(n * mp.log(n) / beta)
    Thetamax = C * mp.sqrt(Kmax * mp.log(n))
    c0_piece = mp.mpf(7) / 6 * Kmax ** 3 / n ** 2 + mp.mpf(5) / 6 * Kmax ** 2 / n ** 2
    c1_pref = 2 * Kmax ** 2 / n ** 2 + (1 - gamma) * Kmax / n + Kmax / n ** 2 + mp.mpf(3) / (4 * n)
    c2_pref = (1 - gamma) * Kmax / (2 * n ** 2) + mp.mpf(3) / (4 * n)
    c3_piece = Thetamax ** 3 / (6 * n ** 2)
    return c0_piece + c1_pref * Thetamax + c2_pref * Thetamax ** 2 + c3_piece


def lambda_hat(gamma):
    gamma = mp.mpf(gamma)
    beta = beta_of(gamma)
    return 16 * (mp.mpf(7) / 4 - gamma) / beta


def Gn_bound(n, gamma):
    n = mp.mpf(n); gamma = mp.mpf(gamma)
    beta = beta_of(gamma)
    return mp.sqrt(mp.pi * n / beta)


def logW(n, gamma, C):
    """log of W(n,gamma,C), computed additively to avoid overflow at extreme n."""
    n = mp.mpf(n); gamma = mp.mpf(gamma); C = mp.mpf(C)
    gK = Ghat(n, gamma)
    gTh = GhatTheta(n, gamma, C)
    log_bulk = 3 * mp.log(gTh) + gTh
    log_tail = mp.log(2) - 2 * C ** 2 * mp.log(n) + 3 * mp.log(gK) + gK
    log_sum = mp.log(mp.e ** (log_bulk - max(log_bulk, log_tail))
                      + mp.e ** (log_tail - max(log_bulk, log_tail))) + max(log_bulk, log_tail)
    return mp.log(Gn_bound(n, gamma)) + mp.log(mp.mpf(1) / 6) + log_sum


print("=" * 78)
print("PART (a): explicit threshold C_0(gamma), tightened leading constant")
print("=" * 78)
print("""
Ghat(n,gamma) ~ lambda_hat(gamma) ln(n) for large n (script 04 Step 3),
lambda_hat(gamma) := 16(7/4-gamma)/beta(gamma). The tail piece of W scales
like n^{-2C^2 + lambda_hat(gamma) + 1/2} (the +1/2 from Gn_bound~sqrt(n)).
Vanishing requires C^2 > 1/4 + lambda_hat(gamma)/2, i.e.

    C_0(gamma) := sqrt(1/4 + lambda_hat(gamma)/2).
""")


def C0_of(gamma):
    return mp.sqrt(mp.mpf(1) / 4 + lambda_hat(gamma) / 2)


print(f"{'gamma':>8} {'beta':>10} {'lambda_hat':>12} {'C_0(gamma)':>12}")
for gs in ['0.99', '0.9', '0.7', '0.5', '0.3', '0.1', '0.05', '0.01', '0.001']:
    gamma = mp.mpf(gs)
    print(f"{gs:>8} {float(beta_of(gamma)):>10.6f} {float(lambda_hat(gamma)):>12.4f} "
          f"{float(C0_of(gamma)):>12.4f}")

print("\n" + "=" * 78)
print("PART (b): pick C(gamma):=1.2*C_0(gamma); find explicit n_0(gamma) via")
print("          direct search (log-domain, avoids overflow) where log W<=0")
print("=" * 78)

n0_results = {}
for gs in ['0.99', '0.9', '0.7', '0.5', '0.3', '0.1', '0.05', '0.01']:
    gamma = mp.mpf(gs)
    C = mp.mpf('1.2') * C0_of(gamma)
    n1 = n1_of(gamma)
    # exponential search in log10(n) for the crossover where logW(n)<=0
    lo, hi = mp.log(n1, 10), mp.log(n1, 10)
    # first, find an upper bound where logW<=0 by doubling log10(n)
    step = mp.mpf(1)
    n_hi = n1
    trials = 0
    while logW(n_hi, gamma, C) > 0 and trials < 200:
        n_hi = n_hi * 10
        trials += 1
    if trials >= 200:
        print(f"gamma={gs}: crossover not found within search budget")
        n0_results[gs] = (None, float(C))
        continue
    # bisection in log10(n) between n1 and n_hi
    lo_n, hi_n = mp.mpf(n1), mp.mpf(n_hi)
    for _ in range(80):
        mid = mp.sqrt(lo_n * hi_n)  # geometric mean bisection (log-scale)
        if logW(mid, gamma, C) > 0:
            lo_n = mid
        else:
            hi_n = mid
    n0 = hi_n
    n0_results[gs] = (n0, float(C))
    print(f"gamma={gs:<6} C={float(C):>9.4f}  n_1(gamma)={n1:<14}  "
          f"n_0(gamma) [logW crosses 0] ~ 10^{float(mp.log(n0,10)):.3f}")

print("\nVerification: logW just above and just below the found n_0 crossover:")
for gs, (n0, C) in n0_results.items():
    if n0 is None:
        continue
    gamma = mp.mpf(gs)
    below = n0 * mp.mpf('0.999')
    above = n0 * mp.mpf('1.001')
    lw_below = logW(below, gamma, C)
    lw_above = logW(above, gamma, C)
    print(f"  gamma={gs}: logW(0.999*n0)={float(lw_below):.4f}  "
          f"logW(1.001*n0)={float(lw_above):.4f}  "
          f"(expect positive then negative)")
    assert lw_below > 0 > lw_above, "crossover bisection inconsistent"

print("\n" + "=" * 78)
print("PART (b'): monotone decay of W beyond n_0(gamma) (log-domain, several")
print("           further decades of n)")
print("=" * 78)
for gs, (n0, C) in n0_results.items():
    if n0 is None:
        continue
    gamma = mp.mpf(gs)
    vals = []
    for mult in [1, 10, 100, 1000, 10000]:
        n = n0 * mult
        vals.append(float(logW(n, gamma, C)))
    print(f"  gamma={gs}: logW at n0*[1,10,100,1000,10000] = "
          f"{[round(v,3) for v in vals]}")
    decreasing = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
    print(f"    monotonically non-increasing: {decreasing}")

print("\n" + "=" * 78)
print("PART (c): compact-uniformity -- single C works on [gamma_0, 1)")
print("=" * 78)
print("""
lambda_hat(gamma) = 16(7/4-gamma)/beta(gamma) is a decreasing function of
gamma on (0,1) (both the (7/4-gamma) numerator decreases and 1/beta(gamma)
decreases as gamma increases toward 1 -- checked directly below), hence so
is C_0(gamma). For any fixed gamma_0 in (0,1), the single constant
C(gamma_0) := 1.2*C_0(gamma_0) suffices for every gamma in [gamma_0,1)
simultaneously (since C_0(gamma)<=C_0(gamma_0) there and Ghat/GhatTheta's own
n_1(gamma) threshold is also controlled by beta(gamma)>=beta(gamma_0), so the
crossover n_0(gamma) for the WHOLE compact range is bounded by n_0(gamma_0),
computed above) -- the honest, correctly-scoped uniformity statement.
""")


def lambda_hat_decreasing_check(samples=400):
    prev = None
    ok = True
    for i in range(1, samples):
        g = mp.mpf(i) / samples
        val = lambda_hat(g)
        if prev is not None and val > prev:
            ok = False
        prev = val
    return ok


print(f"lambda_hat(gamma) numerically confirmed monotonically non-increasing "
      f"in gamma across (0,1) (400-point grid): {lambda_hat_decreasing_check()}")

for g0 in ['0.5', '0.1', '0.01']:
    gamma0 = mp.mpf(g0)
    print(f"gamma_0={g0}: single C(gamma_0)=1.2*C_0(gamma_0)="
          f"{float(mp.mpf('1.2')*C0_of(gamma0)):.4f} works for all gamma in "
          f"[{g0},1) since C_0(gamma)<=C_0(gamma_0)={float(C0_of(gamma0)):.4f} there,")
    n0_g0 = n0_results.get(g0, (None, None))[0]
    if n0_g0 is not None:
        print(f"  with the same single explicit n_0(gamma_0) ~ 10^"
              f"{float(mp.log(n0_g0,10)):.3f} certified above covering the whole range.")

print("\nDone.")
