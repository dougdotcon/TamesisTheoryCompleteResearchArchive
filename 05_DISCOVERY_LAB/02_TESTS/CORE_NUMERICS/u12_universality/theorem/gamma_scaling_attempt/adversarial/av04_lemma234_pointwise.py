#!/usr/bin/env python3
"""
Independent adversarial check (av04) — HOSTILE REFEREE, fresh build.

Pointwise numerical audit of Lemma 2 (product sandwich), Lemma 3
(a priori decay), and Lemma 4 (Gaussian replacement) of ATTEMPT.md,
re-typed from their STATEMENTS only (proofs re-checked by hand in this
session's transcript, not re-derived in code) -- exhaustive-grid style
spot check for violations, fresh code, no front script opened.

Lemma 2. For 1<=m<=k<=n:
  (a) P_{k,m} <= exp(-sigma_k(m))
  (b) if k<=n/2: P_{k,m} >= exp(-sigma_k(m) - k^3/n^2)
  where sigma_k(x) = x(2k-x-1)/(2n), P_{k,m}=prod_{i=1}^m (1-(k-i)/n).

Lemma 3. For 1<=k<=n, gamma in (0,1]:
  A_k <= exp(-a_gamma*k) + exp(-gamma*k*(k-1)/(4n))
  where a_gamma = gamma*(1-ln2)/2.

Lemma 4. For 1<=k<=n:
  (upper) A_k <= (1+eps_k) exp(-s(k)), eps_k = (k/n)*sqrt(k/2)*exp(k^3/(4n^2))
  (lower, k<=n/2) A_k >= (1 - k^3/n^2) exp(-s(k))
  where s(k) = sigma_k(gamma*k) = beta*k^2/n - gamma*k/(2n), beta=gamma(2-gamma)/2.
"""
import math
import numpy as np

def sigma_k(k, x, n):
    return x*(2*k - x - 1) / (2.0*n)

def P_km(n, k, m):
    if m == 0:
        return 1.0
    i = np.arange(1, m+1)
    return float(np.prod(1 - (k - i)/n))

def logP_km(n, k, m):
    """log P_{k,m}, computed term-by-term to stay meaningful even when
    P_{k,m} itself would underflow float64 (e.g. sigma_k(m) > ~700):
    needed because exp(-sigma) ALSO underflows to exactly 0.0 in that
    regime, and comparing the raw (possibly-nonzero-subnormal) P_{k,m}
    against a literal 0.0 produces spurious 'violations' that are pure
    float64-underflow artifacts, not real inequality failures."""
    if m == 0:
        return 0.0
    i = np.arange(1, m+1)
    return float(np.sum(np.log(1 - (k - i)/n)))

def A_k_and_s(n, gamma, k):
    beta = gamma*(2-gamma)/2
    q = gamma
    ms = np.arange(0, k+1)
    logC = np.array([math.lgamma(k+1)-math.lgamma(m+1)-math.lgamma(k-m+1) for m in ms])
    if q <= 0:
        pmf = np.zeros(k+1); pmf[0]=1.0
    elif q >= 1:
        pmf = np.zeros(k+1); pmf[-1]=1.0
    else:
        pmf = np.exp(logC + ms*math.log(q) + (k-ms)*math.log(1-q))
    factors = np.empty(k+1); factors[0]=1.0
    if k>=1:
        i = np.arange(1,k+1)
        factors[1:] = np.cumprod((n-k+i)/n)
    Ak = float(np.dot(pmf, factors))
    s = sigma_k(k, gamma*k, n)
    return Ak, s

def main():
    log = []
    def p(*a):
        s=" ".join(str(x) for x in a); print(s); log.append(s)

    p("=== av04_lemma234_pointwise ===")

    viol2a = viol2b = viol3 = viol4u = viol4l = 0
    checked2 = checked3 = checked4 = 0

    for (n, gamma) in [(65536, 0.3), (65536, 0.8), (4096, 0.15), (4096, 0.95)]:
        beta = gamma*(2-gamma)/2
        a_g = gamma*(1-math.log(2))/2
        Kn = min(n, max(50, math.ceil(math.sqrt((4.0/beta)*n*math.log(n)))*3))
        p(f"--- n={n} gamma={gamma} beta={beta:.6f} a_gamma={a_g:.6f} checking k=1..{Kn} ---")
        for k in range(1, Kn+1):
            # Lemma 2: check at m=k (worst case, largest sigma) and a couple of interior m's
            for m in sorted(set([1, k//3 or 1, (2*k)//3 or 1, k])):
                if m < 1 or m > k:
                    continue
                logPkm = logP_km(n, k, m)
                sig = sigma_k(k, m, n)
                checked2 += 1
                # (a) P_{k,m} <= exp(-sigma)  <=>  log P <= -sigma  (log-space,
                # robust to float64 underflow of exp(-sigma) at large sigma)
                if logPkm > -sig + 1e-9:
                    viol2a += 1
                if k <= n/2:
                    # (b) P_{k,m} >= exp(-sigma - k^3/n^2) <=> logP >= -sigma-k^3/n^2
                    if logPkm < -sig - k**3/n**2 - 1e-9:
                        viol2b += 1
            # Lemma 3
            Ak, s = A_k_and_s(n, gamma, k)
            checked3 += 1
            bound3 = math.exp(-a_g*k) + math.exp(-gamma*k*(k-1)/(4*n))
            if Ak > bound3*(1+1e-10):
                viol3 += 1
            # Lemma 4
            checked4 += 1
            eps_k = (k/n)*math.sqrt(k/2.0)*math.exp(k**3/(4*n**2))
            upper = (1+eps_k)*math.exp(-s)
            if Ak > upper*(1+1e-10):
                viol4u += 1
            if k <= n/2:
                lower = (1 - k**3/n**2)*math.exp(-s)
                if Ak < lower*(1-1e-10):
                    viol4l += 1

    p(f"\nLemma2(a) P<=exp(-sigma): {checked2} checked, {viol2a} violations")
    p(f"Lemma2(b) P>=exp(-sigma-k^3/n^2) (k<=n/2): violations={viol2b}")
    p(f"Lemma3 A_k<=exp(-a_g k)+exp(-g k(k-1)/4n): {checked3} checked, {viol3} violations")
    p(f"Lemma4 upper A_k<=(1+eps_k)exp(-s(k)): {checked4} checked, {viol4u} violations")
    p(f"Lemma4 lower A_k>=(1-k^3/n^2)exp(-s(k)) (k<=n/2): violations={viol4l}")

    total_viol = viol2a+viol2b+viol3+viol4u+viol4l
    p(f"\nTOTAL VIOLATIONS: {total_viol}")

    with open(__file__.replace('.py','.log'),'w') as fh:
        fh.write("\n".join(log)+"\n")

if __name__=="__main__":
    main()
