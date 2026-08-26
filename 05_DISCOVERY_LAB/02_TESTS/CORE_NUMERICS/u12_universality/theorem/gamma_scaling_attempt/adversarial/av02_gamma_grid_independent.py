#!/usr/bin/env python3
"""
Independent adversarial check (av02) — HOSTILE REFEREE, fresh build.

Rebuilds, purely from Lemma 1's STATEMENT in ATTEMPT.md (never opens the
front's .py scripts, never opens the prior stalled referee's ref02*.py),
an evaluator of

    n*phi(n, gamma*n) = sum_{k=1}^n A_k(n,q),  A_k = E_{M~Bin(k,q)}[P_{k,M}]

with float64 arithmetic and an ADAPTIVE self-truncation (not borrowed from
the front's K formula in section 5 -- we just stop summing once terms are
provably negligible for a long stretch), then compares

    R(n,gamma) := phi(n,gamma*n) / phi_infty(gamma*n)

against the claimed limit sqrt(2/(2-gamma)), across a gamma-grid and an
n-grid up to 2**18 (matching the front's own reported grid so the
replication is apples-to-apples), and checks the convergence RATE
(claimed O(n^{-1/4}) proved, O(n^{-1/2}) observed empirically by the
front).

phi_infty(c) computed two independent ways: (i) direct high-accuracy
quadrature of int_0^1 exp(-c t^2) dt (scipy.integrate.quad), (ii) the
closed form (sqrt(pi)/2) c^{-1/2} erf(sqrt(c)) (Theorem 1 of THEOREM.md,
cited, not re-derived) -- these must agree to high precision or something
is wrong with either the target formula or my quadrature.

No randomness. Deterministic recursion only.
"""
import math
from scipy.special import erf, comb as sp_comb
from scipy.integrate import quad
import numpy as np
import time, json

def phi_infty_closedform(c):
    if c == 0:
        return 1.0
    return (math.sqrt(math.pi)/2) * c**-0.5 * erf(math.sqrt(c))

def phi_infty_quad(c):
    val, err = quad(lambda t: math.exp(-c*t*t), 0, 1, epsabs=1e-14, epsrel=1e-13)
    return val

def binom_pmf_row(k, q):
    """Return array pmf[0..k] for Binomial(k,q), via log-space for stability."""
    if k == 0:
        return np.array([1.0])
    ms = np.arange(0, k+1)
    # log C(k,m) + m*log(q) + (k-m)*log(1-q)
    logC = np.array([math.lgamma(k+1) - math.lgamma(m+1) - math.lgamma(k-m+1) for m in ms])
    if q <= 0.0:
        pmf = np.zeros(k+1); pmf[0] = 1.0; return pmf
    if q >= 1.0:
        pmf = np.zeros(k+1); pmf[-1] = 1.0; return pmf
    logpmf = logC + ms*math.log(q) + (k-ms)*math.log(1-q)
    return np.exp(logpmf)

def A_k(n, q, k):
    """A_k(n,q) = sum_m C(k,m) q^m (1-q)^{k-m} * prod_{i=1}^m (n-k+i)/n"""
    pmf = binom_pmf_row(k, q)
    # B(k,m) = prod_{i=1}^m (n-k+i)/n, cumulative
    ms = np.arange(0, k+1)
    factors = np.empty(k+1)
    factors[0] = 1.0
    if k >= 1:
        i = np.arange(1, k+1)
        f = (n - k + i) / n
        factors[1:] = np.cumprod(f)
    return float(np.dot(pmf, factors))

def n_phi_sum(n, gamma, rel_tol=1e-16, patience=60, kmax_cap=None):
    """Compute sum_{k=1}^n A_k(n,q) with q=gamma, adaptively truncating once
    a run of `patience` consecutive k's contribute < rel_tol relative to the
    running total (self-certifying stop, not using the front's K formula)."""
    q = gamma
    total = 0.0
    stall = 0
    kmax = n if kmax_cap is None else min(n, kmax_cap)
    k = 1
    last_report_k = 0
    while k <= kmax:
        a = A_k(n, q, k)
        total += a
        if total > 0 and a < rel_tol * total:
            stall += 1
            if stall >= patience:
                break
        else:
            stall = 0
        k += 1
    return total, k-1  # k-1 = last k actually summed (truncation point)

def main():
    log = []
    def p(*a):
        s = " ".join(str(x) for x in a)
        print(s); log.append(s)

    p("=== av02_gamma_grid_independent ===")

    # sanity: phi_infty two ways
    p("-- phi_infty sanity: closed form vs quadrature --")
    for c in (0.5, 3.7, 50.0, 500.0):
        a = phi_infty_closedform(c)
        b = phi_infty_quad(c)
        p(f"  c={c}: closed={a:.15f} quad={b:.15f} reldiff={abs(a-b)/b:.3e}")

    gammas = [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    ns = [2**e for e in (8, 10, 12, 14, 16, 18)]

    results = {}
    t0 = time.time()
    for gamma in gammas:
        results[gamma] = {}
        p(f"--- gamma={gamma} ---")
        for n in ns:
            c = gamma * n
            nphi, ktrunc = n_phi_sum(n, gamma)
            phi = nphi / n
            pinf = phi_infty_closedform(c)
            R = phi / pinf
            target = math.sqrt(2.0/(2.0-gamma))
            err = R - target
            results[gamma][n] = dict(R=R, target=target, err=err, ktrunc=ktrunc)
            p(f"  n={n:>7d} c={c:>10.2f} ktrunc={ktrunc:>6d} R={R:.10f} target={target:.10f} "
              f"err={err:+.6e} sqrtn*err={math.sqrt(n)*err:+.6f}")
        # empirical rate: err(n/2)/err(n) should approach front's claimed sqrt(2)~1.414
        # (empirically observed O(n^-1/2)) or at least approach some limit >=1
        errs = [results[gamma][n]['err'] for n in ns]
        p(f"  ratio err(n/2)/err(n) across doublings: " +
          ", ".join(f"{errs[i]/errs[i+1]:.4f}" for i in range(len(errs)-1) if errs[i+1] != 0))

    p(f"\nTotal wall time: {time.time()-t0:.1f}s")

    with open(__file__.replace('.py', '.json'), 'w') as fh:
        json.dump(results, fh, indent=1, default=str)
    with open(__file__.replace('.py', '.log'), 'w') as fh:
        fh.write("\n".join(log) + "\n")

if __name__ == "__main__":
    main()
