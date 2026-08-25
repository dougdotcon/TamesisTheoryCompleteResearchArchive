#!/usr/bin/env python3
"""HOSTILE REFEREE check 2: independent high-power replication of the
gamma-grid convergence (ATTEMPT.md sec.7.1) at HIGHER power than the front
(n up to 2^20 on the full grid, 2^22 at spot gammas; front stopped at 2^18),
including gamma values the front never tested (0.25, 0.65, 0.85).

Evaluator built ONLY from Lemma 1 (independently re-proved and brute-force
validated in ref01) + the referee's own certified error budget:

  n*phi(n,gn) = sum_{k=1}^n A_k,  A_k = E[P_{k,M_k}],  M_k~Bin(k,g).

Certified truncations (both proved by the referee from scratch, see report):
  (T1) tail k>K:  sum_{k>K} A_k <= rho(K)
       rho(K) = e^{-a(K+1)}/(1-e^{-a}) + e^{-g K^2/(4n)} (1 + 2n/(gK)),
       a = g(1-ln2)/2   [re-derivation of ATTEMPT (2.1), audited by hand]
  (T2) binomial window |m - gk| <= w_k, w_k = ceil(8 sqrt(k))+1:
       neglected mass <= 2 exp(-2 w_k^2 / k) <= 2e-128 * k-count (Hoeffding)
Both are added to an explicit error budget; float roundoff cross-checked in
ref04 against mpmath dps=40.  Deterministic; referee seeds 20260869000+
reserved-unused.
"""
import json, math, time
import numpy as np

LGAMMA_CACHE = {}

def lgamma_table(N):
    if N not in LGAMMA_CACHE:
        LGAMMA_CACHE[N] = np.array([math.lgamma(i+1) for i in range(N+1)])
    return LGAMMA_CACHE[N]

def nphi_certified(n, g, extra_exponent=45.0):
    """Return (S, budget) with  S <= n*phi(n,gn) <= S + budget  (up to float
    roundoff, bounded separately)."""
    a = g*(1.0-math.log(2.0))/2.0
    # choose K so both tail parts < ~1e-19 absolute
    K1 = math.sqrt((4.0*n/g)*(extra_exponent + 0.5*math.log(n)+5))
    K2 = 62.0/a
    K = int(math.ceil(max(K1, K2)))
    K = min(K, n)
    lg = lgamma_table(K+2)
    S = 0.0
    win_err = 0.0
    if g >= 1.0:
        # degenerate: A_k = P_{k,k}
        for k in range(1, K+1):
            i = np.arange(1, k+1, dtype=np.float64)
            S += math.exp(np.log((n-k+i)/n).sum())
    else:
        lq, l1q = math.log(g), math.log1p(-g)
        for k in range(1, K+1):
            w = int(math.ceil(8.0*math.sqrt(k))) + 1
            mlo = max(0, int(math.floor(g*k)) - w)
            mhi = min(k, int(math.ceil(g*k)) + w)
            m = np.arange(mlo, mhi+1)
            logpmf = lg[k] - lg[m] - lg[k-m] + m*lq + (k-m)*l1q
            # log P_{k,m} = sum_{i=1}^m log((n-k+i)/n); need up to mhi
            i = np.arange(1, mhi+1, dtype=np.float64)
            clog = np.concatenate(([0.0], np.log((n-k+i)/n).cumsum()))
            S += float(np.exp(logpmf + clog[m]).sum())
            win_err += 2.0*math.exp(-2.0*w*w/k)
    # truncation tail bound (proved, Lemma 3 route)
    if K < n:
        rho = math.exp(-a*(K+1))/(1.0-math.exp(-a)) \
            + math.exp(-g*K*K/(4.0*n))*(1.0 + 2.0*n/(g*K))
    else:
        rho = 0.0
    return S, rho + win_err, K

def phi_inf(c):
    # (sqrt(pi)/2) c^{-1/2} erf(sqrt(c)); erfc route for large c accuracy
    rc = math.sqrt(c)
    return (math.sqrt(math.pi)/2.0)/rc * (1.0 - math.erfc(rc))

def main():
    gammas = [0.1,0.2,0.25,0.3,0.4,0.5,0.6,0.65,0.7,0.8,0.85,0.9,0.99,1.0]
    ns_all = [2**j for j in range(8, 21)]           # 256 .. 1,048,576
    ns_deep = [2**21, 2**22]                        # spot checks
    deep_g = {0.2, 0.5, 1.0}
    data = {}
    out = []
    def log(s):
        print(s, flush=True); out.append(s)
    log("=== ref02: independent gamma-grid replication (hostile referee) ===")
    log("n up to 2^20 full grid; 2^21..2^22 at gamma in {0.2,0.5,1.0}")
    t00 = time.time()
    for g in gammas:
        tgt = math.sqrt(2.0/(2.0-g))
        data[str(g)] = {}
        ns = ns_all + (ns_deep if g in deep_g else [])
        prev_err = None
        log(f"-- gamma={g}  target sqrt(2/(2-g)) = {tgt:.12f}")
        for n in ns:
            t0 = time.time()
            S, budget, K = nphi_certified(n, g)
            c = g*n
            pinf = phi_inf(c)
            R = (S/n)/pinf
            Rhi = ((S+budget)/n)/pinf
            err = R - tgt
            ratio = (prev_err/err) if (prev_err is not None and err != 0) else float('nan')
            log(f"   n=2^{int(math.log2(n)):2d} K={K:6d} nphi={S:.10e} "
                f"budget/nphi={budget/S:.1e} R={R:.10f} R-tgt={err:+.3e} "
                f"err(n/2)/err(n)={ratio:6.4f} below={'Y' if Rhi < tgt else 'N'}"
                f" ({time.time()-t0:.1f}s)")
            data[str(g)][str(n)] = dict(nphi=S, budget=budget, K=K, R=R,
                                        target=tgt, err=err)
            prev_err = err
    log(f"total time {time.time()-t00:.0f}s")
    # cross-check against the front's published table excerpt (ATTEMPT 7.1,
    # n=2^18) -- typed in from the .md, not from any script:
    front = {0.1:1.0256418673, 0.2:1.0536343736, 0.3:1.0841136908,
             0.4:1.1174389803, 0.5:1.1540659874, 0.6:1.1945670586,
             0.7:1.2396676769, 0.8:1.2903013199, 0.9:1.3476917252,
             0.99:1.4064644540, 1.0:1.4134793898}
    worst = 0.0
    for g, Rf in front.items():
        mine = data[str(g)][str(2**18)]['R']
        d = abs(mine - Rf)
        worst = max(worst, d)
        flag = 'OK' if d < 5e-10 else 'DISCREPANT'
        log(f"[X] front table n=2^18 gamma={g}: front {Rf:.10f} vs referee "
            f"{mine:.10f}  |diff|={d:.2e} {flag}")
    log(f"[X] worst |diff| vs front's published n=2^18 column: {worst:.2e}")
    with open(__file__.replace('.py','.json'), 'w') as fh:
        json.dump(data, fh, indent=1)
    with open(__file__.replace('.py','.log'), 'w') as fh:
        fh.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    main()
