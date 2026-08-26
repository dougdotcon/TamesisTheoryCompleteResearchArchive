"""
Adversarial referee script 04.

Independent from-scratch reconstruction of the final assembled bound
W(n,gamma,C) (Sec.4 Step 5 of the target ATTEMPT.md) and its explicit
crossover n_0(gamma), worked entirely in log-space (mpmath dps=60) as
the target front claims to have done, at THREE of the eight reported
sample gamma values: 0.99, 0.5, 0.01 (spanning the whole reported
range). No .py file of any front was read; every formula below is
reconstructed purely from the ATTEMPT.md prose, cross-validated in
script 03 (the Ghat formula and C(gamma) values already matched the
target's table exactly there).

Reconstruction:
  beta(gamma)      = gamma*(2-gamma)/2
  K_max(n,gamma)   = 4*sqrt(n*ln(n)/beta)                    [script 03 (B)]
  c0_bound(k)      = (7/6)k^3/n^2 + (5/6)k^2/n^2              [script 02]
  c1_bound(k)      = 2k^2/n^2 + (1-gamma)k/n + k/n^2 + 3/(4n) [script 02]
  c2_bound(k)      = (1-gamma)k/(2n^2) + 3/(4n)                [script 02]
  c3               = 1/(6n^2)                                  [script 02, exact]
  Ghat(n,gamma)    = c0_bound(K_max)+c1_bound(K_max)*K_max
                      +c2_bound(K_max)*K_max^2+c3*K_max^3       [script 03 (A)]
  Theta_max(n,gamma,C) = C*sqrt(K_max*ln(n))     ["identical construction,
                      evaluated at t=Theta_K<=C*sqrt(K_max*ln n)", Sec.4 Step4]
  GhatTheta(n,gamma,C) = c0_bound(K_max)+c1_bound(K_max)*Theta_max
                      +c2_bound(K_max)*Theta_max^2+c3*Theta_max^3
                      ["the identical construction" applied at t=Theta_max
                       instead of t=K_max, same coefficient bounds at k=K_max]
  Gn_bound(n,gamma)= sqrt(pi*n/beta)     [cited "explicit generous version" of
                      G_n=(1/2)sqrt(pi*n/beta), Sec.4 Step5]
  W(n,gamma,C)     = Gn_bound * (1/6) * [ GhatTheta^3*exp(GhatTheta)
                                    + 2*n^(-2C^2) * Ghat^3*exp(Ghat) ]
  lambdahat(gamma) = 16*(7/4-gamma)/beta        [script 03 (C), leading term of Ghat]
  C0(gamma)        = sqrt(1/4 + lambdahat/2)
  C(gamma)         = 1.2 * C0(gamma)            [matched target's table exactly, script 03]

We locate n_0(gamma) := inf{n : log W(n,gamma,C(gamma)) <= 0} by bisection
in x:=log10(n), then compare the resulting log10(n_0) against the target's
reported table values.
"""
import mpmath as mp

mp.mp.dps = 60


def beta_of(g):
    return g * (2 - g) / 2


def Kmax_of(n, g):
    b = beta_of(g)
    return 4 * mp.sqrt(n * mp.log(n) / b)


def c0_bound(k, n, g):
    return mp.mpf(7) / 6 * k ** 3 / n ** 2 + mp.mpf(5) / 6 * k ** 2 / n ** 2


def c1_bound(k, n, g):
    return 2 * k ** 2 / n ** 2 + (1 - g) * k / n + k / n ** 2 + mp.mpf(3) / 4 / n


def c2_bound(k, n, g):
    return (1 - g) * k / (2 * n ** 2) + mp.mpf(3) / 4 / n


def c3_exact(n):
    return mp.mpf(1) / (6 * n ** 2)


def g_poly(t, k, n, g):
    """g(t) using coefficient bounds evaluated at k (the 'per Sec.0, c_i(K)
    throughout' convention), polynomial evaluated at t."""
    return (c0_bound(k, n, g) + c1_bound(k, n, g) * t
            + c2_bound(k, n, g) * t ** 2 + c3_exact(n) * t ** 3)


def Ghat_of(n, g):
    Km = Kmax_of(n, g)
    return g_poly(Km, Km, n, g)


def GhatTheta_of(n, g, C):
    Km = Kmax_of(n, g)
    Theta_max = C * mp.sqrt(Km * mp.log(n))
    return g_poly(Theta_max, Km, n, g)


def Gn_bound_of(n, g):
    b = beta_of(g)
    return mp.sqrt(mp.pi * n / b)


def lambdahat_of(g):
    b = beta_of(g)
    return 16 * (mp.mpf(7) / 4 - g) / b


def C0_of(g):
    return mp.sqrt(mp.mpf(1) / 4 + lambdahat_of(g) / 2)


def C_of(g):
    return mp.mpf('1.2') * C0_of(g)


def logsumexp2(la, lb):
    """log(e^la + e^lb), stable."""
    m = max(la, lb)
    return m + mp.log(mp.e ** (la - m) + mp.e ** (lb - m))


def logW_of(n, g, C):
    Gt = GhatTheta_of(n, g, C)
    Gk = Ghat_of(n, g)
    la = 3 * mp.log(Gt) + Gt
    lb = mp.log(2) - 2 * C ** 2 * mp.log(n) + 3 * mp.log(Gk) + Gk
    bracket_log = logsumexp2(la, lb)
    return mp.log(Gn_bound_of(n, g)) + mp.log(mp.mpf(1) / 6) + bracket_log


def logW_at_x(x, g, C):
    """x = log10(n)."""
    n = mp.power(10, x)
    return logW_of(n, g, C)


def find_n1(g):
    """n_1(gamma) := ceil(16384/beta^2), the target's own claimed threshold
    for K<=n/2 (reconstructed identically from prose, Sec.4 Step 1-2)."""
    b = beta_of(g)
    return mp.ceil(16384 / b ** 2)


def bisect_crossover(g, C, x_lo, x_hi, tol=mp.mpf('1e-6')):
    f_lo = logW_at_x(x_lo, g, C)
    f_hi = logW_at_x(x_hi, g, C)
    assert f_lo > 0, f"f_lo={f_lo} not >0 at x_lo={x_lo} (bracket too high)"
    assert f_hi < 0, f"f_hi={f_hi} not <0 at x_hi={x_hi} (bracket too low)"
    while x_hi - x_lo > tol:
        x_mid = (x_lo + x_hi) / 2
        f_mid = logW_at_x(x_mid, g, C)
        if f_mid > 0:
            x_lo = x_mid
        else:
            x_hi = x_mid
    return (x_lo + x_hi) / 2


# reported table (from target ATTEMPT.md Sec.4 Step 5), for comparison only
reported = {
    mp.mpf('0.99'): (mp.mpf('4.23'), 65550, 20.79),
    mp.mpf('0.9'): (mp.mpf('4.49'), 66867, 36.83),
    mp.mpf('0.7'): (mp.mpf('5.19'), 79141, 45.02),
    mp.mpf('0.5'): (mp.mpf('6.23'), 116509, 50.28),
    mp.mpf('0.3'): (mp.mpf('8.12'), 251965, 55.95),
    mp.mpf('0.1'): (mp.mpf('14.16'), 1815402, 65.95),
    mp.mpf('0.05'): (mp.mpf('20.05'), 6893991, 71.78),
    mp.mpf('0.01'): (mp.mpf('44.89'), 165490771, 84.88),
}

test_gammas = [mp.mpf('0.99'), mp.mpf('0.5'), mp.mpf('0.01')]

# rough per-gamma search brackets for log10(n), widened generously
brackets = {
    mp.mpf('0.99'): (10, 40),
    mp.mpf('0.5'): (20, 70),
    mp.mpf('0.01'): (40, 110),
}

print("gamma | our C(gamma) | reported C(gamma) | our n_1 | reported n_1 | "
      "our log10(n0) | reported log10(n0) | match?")
results = {}
for g in test_gammas:
    C = C_of(g)
    n1_ours = find_n1(g)
    Crep, n1rep, log10n0rep = reported[g]
    x_lo, x_hi = brackets[g]
    # verify bracket signs; expand if necessary
    while logW_at_x(mp.mpf(x_lo), g, C) < 0:
        x_lo -= 5
    while logW_at_x(mp.mpf(x_hi), g, C) > 0:
        x_hi += 10
    x0 = bisect_crossover(g, C, mp.mpf(x_lo), mp.mpf(x_hi))
    results[g] = x0
    match = "YES (within 1.5 in log10 units, same order of magnitude)" \
        if abs(x0 - log10n0rep) < 1.5 else "NO -- DISCREPANCY"
    print(f"{float(g):.2f} | {float(C):.4f} | {float(Crep):.4f} | "
          f"{int(n1_ours)} | {n1rep} | {float(x0):.4f} | {log10n0rep} | {match}")

print("\nDirect log10(n0) comparison summary:")
for g in test_gammas:
    Crep, n1rep, log10n0rep = reported[g]
    print(f"  gamma={float(g):.2f}: our log10(n0)={float(results[g]):.3f}  "
          f"vs reported ~10^{log10n0rep}  "
          f"(delta={float(results[g])-log10n0rep:+.3f})")

# sign confirmation just below/above our own crossover, to 4 decimal digits
# (mirroring the target's own claimed verification methodology)
print("\nSign confirmation at our own crossover +/- 0.001 in log10(n):")
for g in test_gammas:
    C = C_of(g)
    x0 = results[g]
    f_below = logW_at_x(x0 - mp.mpf('0.001'), g, C)
    f_above = logW_at_x(x0 + mp.mpf('0.001'), g, C)
    print(f"  gamma={float(g):.2f}: logW(just below)={float(f_below):.6f} (>0? {f_below>0}), "
          f"logW(just above)={float(f_above):.6f} (<0? {f_above<0})")
    assert f_below > 0 and f_above < 0
