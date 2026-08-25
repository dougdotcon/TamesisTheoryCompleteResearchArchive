#!/usr/bin/env python3
"""HOSTILE REFEREE check 3: Theorem 1' (ATTEMPT.md sec.5) certified verbatim
at the referee's OWN grid, including points the front never tested
(gamma=0.2, 0.6; n=2^11, 2^13, 2^15, 2^17, 2^19, 2^20), against the
referee's independent certified evaluation of n*phi (ref02 machinery).

Every quantity below is transcribed from the PROSE of ATTEMPT.md sec.5 (not
from any front script):
  K   = ceil( sqrt( (4/beta) n ln n ) ),  beta = g(2-g)/2
  om  = K^3/(4 n^2);   de = exp(gK/(2n)) - 1
  J32 = (1/2)Gamma(5/4)(n/beta)^{5/4} + 2 (3n/(4beta))^{3/4} e^{-3/4}
  J3  = n^2/(2 beta^2) + 2 (3n/(2beta))^{3/2} e^{-3/2}
  rho = e^{-a(K+1)}/(1-e^{-a}) + e^{-gK^2/(4n)}(1+2n/(gK)), a=g(1-ln2)/2
  T   = (n/(2 beta K)) e^{-beta K^2/n}
  U   = (1+de)[G_n + (e^om/(sqrt2 n)) J32] + rho
  Lo  = G_n - 1 - T - (1+de) J3/n^2,   G_n = (1/2) sqrt(pi n / beta)
Claim: Lo <= n phi(n,gn) <= U whenever K <= n/2.
Also audits Theorem 2's envelope claim:
  Theta_n * n^{1/4} -> (Gamma(5/4)/sqrt(2 pi)) beta^{-3/4}.
"""
import math, json
from ref02_gamma_grid import nphi_certified

def envelope(n, g):
    beta = g*(2.0-g)/2.0
    K = math.ceil(math.sqrt((4.0/beta)*n*math.log(n)))
    om = K**3/(4.0*n*n)
    de = math.exp(g*K/(2.0*n)) - 1.0
    G = 0.5*math.sqrt(math.pi*n/beta)
    J32 = 0.5*math.gamma(1.25)*(n/beta)**1.25 \
        + 2.0*(3.0*n/(4.0*beta))**0.75*math.exp(-0.75)
    J3 = n*n/(2.0*beta*beta) + 2.0*(3.0*n/(2.0*beta))**1.5*math.exp(-1.5)
    a = g*(1.0-math.log(2.0))/2.0
    rho = math.exp(-a*(K+1))/(1.0-math.exp(-a)) \
        + math.exp(-g*K*K/(4.0*n))*(1.0+2.0*n/(g*K))
    T = (n/(2.0*beta*K))*math.exp(-beta*K*K/n)
    U = (1.0+de)*(G + math.exp(om)/(math.sqrt(2.0)*n)*J32) + rho
    Lo = G - 1.0 - T - (1.0+de)*J3/(n*n)
    return dict(K=K, G=G, U=U, Lo=Lo, beta=beta, side_ok=(K <= n/2))

def main():
    out = []
    def log(s):
        print(s, flush=True); out.append(s)
    log("=== ref03: Theorem 1' verbatim certification (hostile referee) ===")
    gammas = [0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.9, 1.0]
    ns = [2**j for j in (10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)]
    n_ok = n_fail = n_skip = 0
    const = math.gamma(1.25)/math.sqrt(2.0*math.pi)
    for g in gammas:
        for n in ns:
            e = envelope(n, g)
            if not e['side_ok']:
                log(f"[skip] g={g} n=2^{int(math.log2(n))}: K={e['K']} > n/2 "
                    f"-- theorem makes no claim (side condition fails)")
                n_skip += 1
                continue
            S, budget, Keval = nphi_certified(n, g)
            fuzz = 1e-12*S               # float roundoff allowance (ref04)
            lo_ok = e['Lo'] <= S + budget + fuzz
            hi_ok = S - fuzz <= e['U']   # S is a LOWER bound for nphi
            # stricter: certified interval [S-fuzz, S+budget+fuzz] inside
            # [Lo, U]?
            strict = (e['Lo'] <= S - fuzz) and (S + budget + fuzz <= e['U'])
            th = max(e['U']/e['G']-1.0, 1.0-e['Lo']/e['G'])
            scaled = th*n**0.25/(const*e['beta']**-0.75)
            status = 'PASS' if strict else ('PASS(loose)' if lo_ok and hi_ok else 'FAIL')
            if strict or (lo_ok and hi_ok):
                n_ok += 1
            else:
                n_fail += 1
            log(f"[{status}] g={g:4} n=2^{int(math.log2(n)):2d}: "
                f"Lo={e['Lo']:.6e} nphi in [{S:.6e},{S+budget:.6e}] "
                f"U={e['U']:.6e}  slackLo={(S-e['Lo'])/e['G']:.3e} "
                f"slackU={(e['U']-S-budget)/e['G']:.3e} "
                f"Theta={th:.4e} Theta*n^.25/(cst*b^-.75)={scaled:.4f}")
    log(f"summary: {n_ok} pass, {n_fail} FAIL, {n_skip} skipped (side cond)")
    log(f"asymptotic-constant column should drift toward 1.0 as n grows "
        f"(claimed Theta ~ {const:.6f} * beta^-3/4 * n^-1/4).")
    log(f"Gamma(5/4)/sqrt(2pi) = {const:.10f}  (ATTEMPT claims 0.36158...)")
    with open(__file__.replace('.py','.log'), 'w') as fh:
        fh.write('\n'.join(out)+'\n')

if __name__ == '__main__':
    main()
