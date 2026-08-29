"""
Independent Monte Carlo test of Claim B (M_K' =_d M_K, i.e. F_{M_K'}(x) =
1-(1-x^2)^K) at larger K than the exact symbolic moment check
(verify_MK_moments.py, K<=7) reaches -- via direct simulation of M_K' from
its own defining construction (Dirichlet(1,...,1) arcs realized as spacings
of K i.i.d. Uniform(0,1) order statistics; S via the dest-chase/cycle
construction; V_s via the landing-position rule), and a one-sample
Kolmogorov-Smirnov test against the closed-form target CDF
F_K(x) = 1-(1-x^2)^K.

No code from any other front is used. Reserved seeds only.
"""
import math
import random

from coupling_bound_check import find_cycles


def sample_MK_prime(K, rng):
    xi = sorted(rng.random() for _ in range(K))
    eta = [rng.random() for _ in range(K)]
    cumQ = [0.0] * (K + 1)
    for t in range(K):
        cumQ[t + 1] = xi[t]
    qD = 1.0 - cumQ[K]

    dest = []
    for j in range(K):
        z = eta[j]
        t = None
        for tt in range(K):
            if cumQ[tt] < z <= cumQ[tt + 1]:
                t = tt
                break
        if t is None:
            t = K
        dest.append(t)

    S = find_cycles(dest, K)
    M = qD
    for s in S:
        j = None
        for jj in range(K):
            if dest[jj] == s:
                j = jj
                break
        Vp = cumQ[s + 1] - eta[j]
        M += Vp
    return M


def ks_statistic(samples, cdf_fn):
    xs = sorted(samples)
    n = len(xs)
    D = 0.0
    for i, x in enumerate(xs):
        F_emp_right = (i + 1) / n
        F_emp_left = i / n
        F_target = cdf_fn(x)
        D = max(D, abs(F_emp_right - F_target), abs(F_emp_left - F_target))
    return D


def target_F(K, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    return 1 - (1 - x * x) ** K


def ks_pvalue_asymptotic(D, n):
    # Kolmogorov distribution asymptotic p-value (standard, cited formula)
    lam = (math.sqrt(n) + 0.12 + 0.11 / math.sqrt(n)) * D
    if lam < 0.2:
        return 1.0
    s = 0.0
    for k in range(1, 101):
        s += (-1) ** (k - 1) * math.exp(-2 * k * k * lam * lam)
    return max(0.0, min(1.0, 2 * s))


if __name__ == "__main__":
    RESERVED_SEED_BASE = 20260933300
    Ks = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20]
    trials = 40000
    print(f"{'K':>3} {'trials':>7} {'mean(MK_prime)':>15} {'target phi_K':>13} "
          f"{'D_KS':>8} {'p-value':>9}")
    for idx, K in enumerate(Ks):
        seed = RESERVED_SEED_BASE + idx
        rng = random.Random(seed)
        samples = [sample_MK_prime(K, rng) for _ in range(trials)]
        mean = sum(samples) / trials
        # target mean phi_K = 4^K (K!)^2/(2K+1)!
        phi_K = (4 ** K) * (math.factorial(K) ** 2) / math.factorial(2 * K + 1)
        D = ks_statistic(samples, lambda x: target_F(K, x))
        p = ks_pvalue_asymptotic(D, trials)
        print(f"{K:>3} {trials:>7} {mean:>15.6f} {phi_K:>13.6f} {D:>8.5f} {p:>9.4f} (seed={seed})")
