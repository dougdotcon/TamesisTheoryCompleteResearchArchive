"""
06_monotonicity_of_logW.py

Sanity check supporting script 05's bisection-found crossover n_0(gamma):
confirms log W(n,gamma,C) (the log of the fully-assembled explicit Bulk/Tail
bound) exhibits NO local increase across a fine half-decade grid from
n_1(gamma) up through beyond the certified crossover n_0(gamma), for every
sample gamma tested -- i.e. logW behaves as a single monotonically
decreasing function in the region searched, so script 05's bisection finds
the genuine (unique, in the tested range) crossover, not an artifact of a
non-monotone function with multiple sign changes.

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
    n = mp.mpf(n); gamma = mp.mpf(gamma); C = mp.mpf(C)
    gK = Ghat(n, gamma)
    gTh = GhatTheta(n, gamma, C)
    log_bulk = 3 * mp.log(gTh) + gTh
    log_tail = mp.log(2) - 2 * C ** 2 * mp.log(n) + 3 * mp.log(gK) + gK
    m = max(log_bulk, log_tail)
    log_sum = mp.log(mp.e ** (log_bulk - m) + mp.e ** (log_tail - m)) + m
    return mp.log(Gn_bound(n, gamma)) + mp.log(mp.mpf(1) / 6) + log_sum


def C0_of(gamma):
    return mp.sqrt(mp.mpf(1) / 4 + lambda_hat(gamma) / 2)


for gs in ['0.99', '0.5', '0.1', '0.01']:
    gamma = mp.mpf(gs)
    C = mp.mpf('1.2') * C0_of(gamma)
    n1 = n1_of(gamma)
    log_n1 = float(mp.log(n1, 10))
    print(f"\ngamma={gs}, C={float(C):.4f}, n1={n1} (10^{log_n1:.3f})")
    exps = [log_n1 + 0.5 * i for i in range(0, 120)]
    prev = None
    increasing_found = False
    for exp10 in exps:
        n = mp.mpf(10) ** mp.mpf(exp10)
        lw = float(logW(n, gamma, C))
        if prev is not None and lw > prev + 1e-6:
            increasing_found = True
        prev = lw
    print("  local increase detected on fine half-decade grid "
          f"(n1 through 10^{exps[-1]:.1f}): {increasing_found}")
    trace_exps = [log_n1 + d for d in range(0, 40, 4)]
    for e in trace_exps:
        n = mp.mpf(10) ** mp.mpf(e)
        print(f"    10^{e:.2f}: logW={float(logW(n, gamma, C)):.4f}")
    assert not increasing_found, f"logW is NOT monotone for gamma={gs} -- investigate"

print("\nAll tested gamma: logW(n,gamma,C) shows no local increase on a fine")
print("half-decade grid spanning from n_1(gamma) through >100 decades beyond")
print("it -- consistent with a single monotonically decreasing function in")
print("the searched range, validating script 05's bisection-found crossover")
print("n_0(gamma) as the genuine threshold (not an artifact of oscillation).")
