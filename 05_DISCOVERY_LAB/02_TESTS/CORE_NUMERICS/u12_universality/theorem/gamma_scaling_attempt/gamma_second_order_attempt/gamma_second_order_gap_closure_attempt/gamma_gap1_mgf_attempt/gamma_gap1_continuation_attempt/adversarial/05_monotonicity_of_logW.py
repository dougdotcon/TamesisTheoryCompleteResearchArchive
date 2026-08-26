"""
Adversarial referee script 05.

Independent check of the target's Sec.4 Step 6 "no hidden oscillation"
claim: scan log W(n,gamma,C(gamma)) (reconstructed identically to script
04, which matched the target's own n_1 and n_0 values almost exactly)
on a fine grid in x=log10(n), from n_1(gamma) through many decades past
the certified crossover n_0(gamma), and confirm there is no local
increase anywhere (i.e. logW is monotonically non-increasing throughout).

Two sample gammas tested: 0.5 and 0.01 (one moderate, one near the hard
gamma->0 edge).
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
    m = max(la, lb)
    return m + mp.log(mp.e ** (la - m) + mp.e ** (lb - m))


def logW_at_x(x, g, C):
    n = mp.power(10, x)
    Gt = GhatTheta_of(n, g, C)
    Gk = Ghat_of(n, g)
    la = 3 * mp.log(Gt) + Gt
    lb = mp.log(2) - 2 * C ** 2 * mp.log(n) + 3 * mp.log(Gk) + Gk
    bracket_log = logsumexp2(la, lb)
    return mp.log(Gn_bound_of(n, g)) + mp.log(mp.mpf(1) / 6) + bracket_log


def find_n1(g):
    b = beta_of(g)
    return mp.ceil(16384 / b ** 2)


# reuse n0 values found independently in script 04
n0_x = {mp.mpf('0.5'): mp.mpf('50.2760'), mp.mpf('0.01'): mp.mpf('84.8813')}

for g in [mp.mpf('0.5'), mp.mpf('0.01')]:
    C = C_of(g)
    n1 = find_n1(g)
    x_start = mp.log10(n1)
    x_end = n0_x[g] + 60  # >60 decades beyond the certified crossover
    print(f"\n=== gamma={float(g)}: scanning x=log10(n) from {float(x_start):.4f} "
          f"(n_1) to {float(x_end):.4f} (n0+60 decades) ===")
    N_POINTS = 4000
    xs = [x_start + (x_end - x_start) * i / (N_POINTS - 1) for i in range(N_POINTS)]
    prev = None
    increasing_found = False
    max_increase = mp.mpf(0)
    worst_x = None
    for x in xs:
        val = logW_at_x(x, g, C)
        if prev is not None and val > prev:
            increasing_found = True
            inc = val - prev
            if inc > max_increase:
                max_increase = inc
                worst_x = x
        prev = val
    print(f"  Points scanned: {N_POINTS}")
    print(f"  increasing_found = {increasing_found}")
    if increasing_found:
        print(f"  WORST local increase: {float(max_increase)} at x~{float(worst_x)}")
    else:
        print("  No local increase anywhere in the scanned range -- "
              "logW is monotonically non-increasing on this grid.")
    # also report endpoints for sanity
    print(f"  logW(x_start) = {float(logW_at_x(x_start, g, C)):.6f}  "
          f"(should be large positive, near n_1)")
    print(f"  logW(x_end)   = {float(logW_at_x(x_end, g, C)):.6f}  "
          f"(should be very large negative, 60 decades past n0)")
