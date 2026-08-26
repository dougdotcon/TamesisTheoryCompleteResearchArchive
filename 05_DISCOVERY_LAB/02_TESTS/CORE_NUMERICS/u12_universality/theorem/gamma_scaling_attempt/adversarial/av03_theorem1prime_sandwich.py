#!/usr/bin/env python3
"""
Independent adversarial check (av03) — HOSTILE REFEREE, fresh build.

Re-types, literally from ATTEMPT.md Section 5's DEFINITIONS (not from any
.py script of the front or the prior stalled referee), the finite-n
envelope of "Theorem 1'" and checks the sandwich

    Lo(gamma,n) <= n*phi(n, gamma*n) <= U(gamma,n)

against an independently-computed n*phi(n,gamma*n) (same evaluator as
av02, re-verified against av01's exact brute force at n=3,4,5 first,
then used at scale). Definitions (beta, a_gamma, G_n, K, omega, delta,
J_3/2, J_3, rho, T, U, Lo) are copied symbol-for-symbol from the prose of
ATTEMPT.md Sec 5 -- this script is the independent "does the algebra as
printed actually sandwich the true value" check, not a re-derivation of
why it should.
"""
import math
import numpy as np
from scipy.special import gamma as Gamma_fn
import json

def beta_of(gamma):
    return gamma*(2-gamma)/2

def a_gamma_of(gamma):
    return gamma*(1-math.log(2))/2

def binom_pmf_row(k, q):
    if k == 0:
        return np.array([1.0])
    ms = np.arange(0, k+1)
    logC = np.array([math.lgamma(k+1) - math.lgamma(m+1) - math.lgamma(k-m+1) for m in ms])
    if q <= 0.0:
        pmf = np.zeros(k+1); pmf[0] = 1.0; return pmf
    if q >= 1.0:
        pmf = np.zeros(k+1); pmf[-1] = 1.0; return pmf
    logpmf = logC + ms*math.log(q) + (k-ms)*math.log(1-q)
    return np.exp(logpmf)

def A_k(n, q, k):
    pmf = binom_pmf_row(k, q)
    factors = np.empty(k+1)
    factors[0] = 1.0
    if k >= 1:
        i = np.arange(1, k+1)
        f = (n - k + i) / n
        factors[1:] = np.cumprod(f)
    return float(np.dot(pmf, factors))

def n_phi_sum(n, gamma, rel_tol=1e-16, patience=80):
    q = gamma
    total = 0.0
    stall = 0
    k = 1
    while k <= n:
        a = A_k(n, q, k)
        total += a
        if total > 0 and a < rel_tol * total:
            stall += 1
            if stall >= patience:
                break
        else:
            stall = 0
        k += 1
    return total

def envelope(n, gamma):
    beta = beta_of(gamma)
    a_g = a_gamma_of(gamma)
    K = math.ceil(math.sqrt((4.0/beta) * n * math.log(n)))
    omega = K**3 / (4.0 * n**2)
    delta = math.exp(gamma*K/(2*n)) - 1.0
    J32 = 0.5*Gamma_fn(1.25)*(n/beta)**1.25 + 2*(3*n/(4*beta))**0.75*math.exp(-0.75)
    J3 = n**2/(2*beta**2) + 2*(3*n/(2*beta))**1.5*math.exp(-1.5)
    Gn = 0.5*math.sqrt(math.pi*n/beta)
    # rho(K): geometric part + gaussian tail part
    rho = math.exp(-a_g*(K+1))/(1-math.exp(-a_g)) + math.exp(-gamma*K*K/(4*n))*(1 + 2*n/(gamma*K))
    T = n/(2*beta*K) * math.exp(-beta*K*K/n)
    U = (1+delta)*(Gn + math.exp(omega)/(math.sqrt(2)*n)*J32) + rho
    Lo = Gn - 1 - T - (1+delta)*J3/n**2
    side_ok = (K <= n/2)
    return dict(K=K, omega=omega, delta=delta, J32=J32, J3=J3, Gn=Gn, rho=rho, T=T,
                U=U, Lo=Lo, side_ok=side_ok, beta=beta)

def main():
    log = []
    def p(*a):
        s = " ".join(str(x) for x in a); print(s); log.append(s)

    p("=== av03_theorem1prime_sandwich ===")
    gammas = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    ns = [2**e for e in (10, 12, 14, 16, 18)]

    total_checked = 0
    total_violations = 0
    results = []
    for gamma in gammas:
        for n in ns:
            env = envelope(n, gamma)
            nphi = n_phi_sum(n, gamma)
            ok = (env['Lo'] <= nphi <= env['U'])
            total_checked += 1
            if not ok:
                total_violations += 1
            slack_lo = nphi - env['Lo']
            slack_hi = env['U'] - nphi
            p(f"gamma={gamma:.2f} n={n:>7d} side_ok(K<=n/2)={env['side_ok']!s:5} "
              f"Lo={env['Lo']:.6f} nphi={nphi:.6f} U={env['U']:.6f} "
              f"slack_lo={slack_lo:.4e} slack_hi={slack_hi:.4e} sandwich_holds={ok}")
            results.append(dict(gamma=gamma, n=n, **{k: env[k] for k in ('K','side_ok','Lo','U')},
                                 nphi=nphi, ok=ok))

    p(f"\nTOTAL: {total_checked} points checked, {total_violations} violations "
      f"({total_checked-total_violations}/{total_checked} sandwich holds)")

    with open(__file__.replace('.py', '.json'), 'w') as fh:
        json.dump(results, fh, indent=1, default=str)
    with open(__file__.replace('.py', '.log'), 'w') as fh:
        fh.write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
