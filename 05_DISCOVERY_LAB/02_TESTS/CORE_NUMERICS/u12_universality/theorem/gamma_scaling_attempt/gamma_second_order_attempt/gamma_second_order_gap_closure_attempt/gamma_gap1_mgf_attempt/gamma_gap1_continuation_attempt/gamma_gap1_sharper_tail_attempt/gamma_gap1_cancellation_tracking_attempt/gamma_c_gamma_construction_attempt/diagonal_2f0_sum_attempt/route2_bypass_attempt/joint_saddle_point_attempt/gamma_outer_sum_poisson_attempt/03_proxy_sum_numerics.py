#!/usr/bin/env python3
"""
Script 03 -- GAMMA-OUTER-SUM-POISSON-ATTEMPT.

Direct numerical confirmation of script 02's central closed-form claim:

    sum_{m=0}^infty T_prof(m/sqrt(n), gamma)
        = sqrt(n) * int_0^infty T_prof(lambda,gamma) dlambda + 1/(2*gamma)
          + O(exp(-c(gamma) n)),   c(gamma) = 2*pi^2*gamma/(2-gamma).

Tested here on the T_PROF PROXY ITSELF (the "frozen mesoscale profile"),
i.e. with NO dependence on the true finite-n term_m(n,gamma) yet -- that
cross-check against the true discrete sum is script 04.  This script
isolates and stress-tests the Poisson-summation machinery on its own,
exactly (not approximately) defined object.
"""
import mpmath as mp

mp.mp.dps = 60

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def T_prof(lam, gamma):
    return (1 / gamma) * mp.e ** (-((2 - gamma) / (2 * gamma)) * lam ** 2)


def phi_n(m, n, gamma):
    return T_prof(m / mp.sqrt(n), gamma)


def continuum_integral(n, gamma):
    """sqrt(n) * int_0^infty T_prof(lambda,gamma) dlambda, closed form (cited, Estagio 56)."""
    beta = gamma * (2 - gamma) / 2
    return mp.sqrt(n) * mp.mpf('0.5') * mp.sqrt(mp.pi / beta)


def predicted_sum(n, gamma):
    return continuum_integral(n, gamma) + 1 / (2 * gamma)


def exact_discrete_sum(n, gamma, M=None):
    """sum_{m=0}^M T_prof(m/sqrt(n),gamma), M chosen large enough that the
    tail (m > M) is far below working precision (Gaussian decay)."""
    if M is None:
        # tail term at m=M is ~ exp(-alpha*M^2/n); choose M so this is << 10^-(dps-10)
        alpha = (2 - gamma) / (2 * gamma)
        target_log = (mp.mp.dps - 10) * mp.log(10)
        M = int(mp.sqrt(target_log * n / alpha)) + 5
    total = mp.mpf(0)
    for m in range(0, M + 1):
        total += phi_n(m, n, gamma)
    return total, M


log("=" * 78)
log("PART A: sum_{m=0}^infty T_prof(m/sqrt(n),gamma) vs predicted closed form,")
log("        across n and gamma; residual should shrink like exp(-c(gamma) n).")
log("        Working precision (dps) is set PER (gamma,n) point, generously")
log("        above c(gamma)*n/ln(10), so the residual is resolved cleanly and")
log("        not merely reporting round-off noise at the working precision.")
log("=" * 78)

gammas = [mp.mpf('0.2'), mp.mpf('0.5'), mp.mpf('0.8')]
n_values = [1, 2, 3, 4, 6, 8, 10, 13, 16]

results = {}
for gamma in gammas:
    c_gamma = 2 * mp.pi ** 2 * gamma / (2 - gamma)
    log(f"\ngamma = {float(gamma)}, predicted rate c(gamma) = 2*pi^2*gamma/(2-gamma) = {float(c_gamma):.6f}")
    log(f"{'n':>4} {'dps':>5} {'residual':>16} {'log(residual)':>16} {'-c*n (predicted)':>18} {'ratio log/pred':>16}")
    row = []
    for n in n_values:
        needed_dps = int(float(c_gamma) * n / 2.302585) + 40
        mp.mp.dps = needed_dps
        exact_sum, M_used = exact_discrete_sum(n, gamma)
        pred = predicted_sum(n, gamma)
        residual = exact_sum - pred
        log_res = mp.log(abs(residual))
        predicted_log = -c_gamma * n
        ratio = log_res / predicted_log
        log(f"{n:>4} {needed_dps:>5} {float(residual):>16.4e} {float(log_res):>16.3f} "
            f"{float(predicted_log):>18.3f} {float(ratio):>16.5f}")
        row.append((n, residual, log_res))
    results[float(gamma)] = row
mp.mp.dps = 60

log("")
log("=" * 78)
log("PART B: fit the empirical log-residual slope vs n (least squares over all")
log("        points) and compare to the predicted -c(gamma)")
log("=" * 78)
for gamma in gammas:
    c_gamma = 2 * mp.pi ** 2 * gamma / (2 - gamma)
    row = results[float(gamma)]
    ns = [mp.mpf(r[0]) for r in row]
    lrs = [r[2] for r in row]
    nbar = sum(ns) / len(ns)
    lbar = sum(lrs) / len(lrs)
    num = sum((ni - nbar) * (li - lbar) for ni, li in zip(ns, lrs))
    den = sum((ni - nbar) ** 2 for ni in ns)
    slope = num / den
    log(f"gamma={float(gamma)}: least-squares slope over n={n_values} = {float(slope):.6f}, "
        f"predicted -c(gamma) = {float(-c_gamma):.6f}, ratio = {float(slope/(-c_gamma)):.6f}")

log("")
log("=" * 78)
log("PART C: push n further (with matching precision) to confirm the residual")
log("        keeps tracking exp(-c(gamma) n) precisely -- not merely 'small'")
log("        but genuinely EXPONENTIALLY small (contrast with the O(n^-1/2)/")
log("        O(n^-1) POWER-LAW scale of the other two fronts' corrections)")
log("=" * 78)
for gamma in [mp.mpf('0.5')]:
    c_gamma = 2 * mp.pi ** 2 * gamma / (2 - gamma)
    for n in [10, 20, 30]:
        needed_dps = int(float(c_gamma) * n / 2.302585) + 40
        mp.mp.dps = needed_dps
        exact_sum, M_used = exact_discrete_sum(n, gamma)
        pred = predicted_sum(n, gamma)
        residual = exact_sum - pred
        predicted_mag = mp.e ** (-c_gamma * n)
        ratio = abs(residual) / predicted_mag
        log(f"gamma={float(gamma)}, n={n} (dps={needed_dps}): |residual|={float(abs(residual)):.6e}, "
            f"predicted magnitude exp(-c*n)={float(predicted_mag):.6e}, ratio={float(ratio):.6f}")
mp.mp.dps = 60

with open("03_proxy_sum_numerics.log", "w") as f:
    f.write("\n".join(LOG) + "\n")
print("\nLog written to 03_proxy_sum_numerics.log")
