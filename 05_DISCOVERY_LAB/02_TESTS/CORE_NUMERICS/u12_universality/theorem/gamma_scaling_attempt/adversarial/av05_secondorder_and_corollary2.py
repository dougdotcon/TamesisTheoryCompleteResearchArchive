#!/usr/bin/env python3
"""
Independent adversarial check (av05) — HOSTILE REFEREE, fresh build.

Part A: second-order conjecture (ATTEMPT.md Sec 7.3, explicitly labeled
CONJECTURED for gamma in (0,1), PROVED at gamma=1). Checks whether
sqrt(n)*(R_n - target) trends toward the closed form

    C(gamma) = -(2/(3 sqrt(pi))) * sqrt(gamma) * (6-8*gamma+3*gamma^2)/(2-gamma)^2

using our OWN independently-built evaluator (same A_k engine as av02/03,
not the front's), via simple two-point Richardson extrapolation.

Part B: Corollary 2 (moving gamma_n, gamma_n -> 0 case). Take
gamma_n = n^(-1/4) (satisfies gamma_n * n^(1/3)/ln n = n^(1/12)/ln n -> oo,
the stated hypothesis) and check phi(n,gamma_n*n)/phi_infty(gamma_n*n) -> 1
as claimed (this is the gamma_n -> 0 sub-case of Corollary 2).
"""
import math
import numpy as np
from scipy.special import erf
import json

def phi_infty(c):
    if c <= 0:
        return 1.0
    return (math.sqrt(math.pi)/2) * c**-0.5 * erf(math.sqrt(c))

def binom_pmf_row(k, q):
    if k == 0:
        return np.array([1.0])
    ms = np.arange(0, k+1)
    logC = np.array([math.lgamma(k+1)-math.lgamma(m+1)-math.lgamma(k-m+1) for m in ms])
    if q <= 0.0:
        pmf = np.zeros(k+1); pmf[0]=1.0; return pmf
    if q >= 1.0:
        pmf = np.zeros(k+1); pmf[-1]=1.0; return pmf
    logpmf = logC + ms*math.log(q) + (k-ms)*math.log(1-q)
    return np.exp(logpmf)

def A_k(n, q, k):
    pmf = binom_pmf_row(k, q)
    factors = np.empty(k+1); factors[0]=1.0
    if k>=1:
        i = np.arange(1,k+1)
        factors[1:] = np.cumprod((n-k+i)/n)
    return float(np.dot(pmf, factors))

def n_phi_sum(n, q, rel_tol=1e-16, patience=80):
    total = 0.0; stall=0; k=1
    while k <= n:
        a = A_k(n, q, k)
        total += a
        if total>0 and a < rel_tol*total:
            stall += 1
            if stall >= patience:
                break
        else:
            stall = 0
        k += 1
    return total

def C_closed_form(gamma):
    return -(2.0/(3*math.sqrt(math.pi))) * math.sqrt(gamma) * (6-8*gamma+3*gamma**2)/(2-gamma)**2

def main():
    log = []
    def p(*a):
        s=" ".join(str(x) for x in a); print(s); log.append(s)

    p("=== av05_secondorder_and_corollary2 ===")
    p("\n--- Part A: second-order conjecture, Richardson x_n = sqrt(n)(R_n - target) ---")
    for gamma in (0.3, 0.5, 0.9, 1.0):
        target = math.sqrt(2.0/(2.0-gamma))
        ns = [2**e for e in (14, 15, 16, 17)]
        xs = []
        for n in ns:
            nphi = n_phi_sum(n, gamma)
            R = (nphi/n)/phi_infty(gamma*n)
            x = math.sqrt(n)*(R-target)
            xs.append(x)
        # Richardson: x_n = C + b/sqrt(n) -> use last two points
        n1, n2 = ns[-2], ns[-1]
        x1, x2 = xs[-2], xs[-1]
        # x = C + b/sqrt(n); solve for C from two points
        s1, s2 = 1/math.sqrt(n1), 1/math.sqrt(n2)
        C_est = (x1*s2 - x2*s1)/(s2-s1)
        C_true = C_closed_form(gamma)
        reldev = abs(C_est-C_true)/abs(C_true) if C_true != 0 else float('nan')
        p(f"gamma={gamma}: x_n at n={ns} = {[f'{x:.6f}' for x in xs]}")
        p(f"  Richardson C_est={C_est:.6f}  C(gamma) closed form={C_true:.6f}  reldev={reldev:.3e}")

    p("\n--- Part B: Corollary 2, gamma_n = n^(-1/4) -> 0, expect ratio -> 1 ---")
    for e in (10, 12, 14, 16, 18):
        n = 2**e
        gamma_n = n**-0.25
        hyp = gamma_n * n**(1/3) / math.log(n)  # should -> infinity
        c = gamma_n*n
        nphi = n_phi_sum(n, gamma_n)
        R = (nphi/n)/phi_infty(c)
        p(f"n=2^{e}={n} gamma_n=n^-1/4={gamma_n:.6f} hyp_stat(gamma_n n^1/3/ln n)={hyp:.3f} "
          f"c={c:.3f} R={R:.8f} |R-1|={abs(R-1):.3e}")

    with open(__file__.replace('.py','.log'),'w') as fh:
        fh.write("\n".join(log)+"\n")

if __name__=="__main__":
    main()
