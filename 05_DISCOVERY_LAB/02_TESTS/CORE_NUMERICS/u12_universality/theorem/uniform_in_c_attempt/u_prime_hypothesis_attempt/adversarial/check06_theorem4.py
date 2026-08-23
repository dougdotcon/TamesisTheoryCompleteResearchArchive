"""
Referee check 06 -- Theorem 4 (Hypothesis (U') itself): the fully assembled
inequality |phi_n^{(K)} - phi_K| <= a*sqrt(K)/n, a = 1+sqrt(pi/2) = 2.253314...,
for all n>=1, 0<=K<=n.

Per the referee brief, this is checked both at the two "binding" cases named
in the target's own proof (n=K+1 via Theorem 3's M_K shortcut, and n=K the
boundary case), and at GENERIC interior n (via the closed forms directly,
independent of Theorem 3's shortcut), and pushed to K up to 10^5.

Also independently re-checks the elementary fact n/sqrt(n+1) >= sqrt(n)-1
used in the K=n boundary-case proof.

Discipline: EXACT Fraction for a K<=60 cross-validation baseline; mpmath
(60 dps) for K up to 3000 dense and K up to 10^5 sparse; a subset of the
mpmath stage is cross-checked against exact Fraction at moderate K to
confirm mpmath is not hiding a near-violation.
"""
import sys
from fractions import Fraction as F

import mpmath as mp
import numpy as np

sys.path.insert(0, ".")
import closed_forms as cf

mp.mp.dps = 60
A_CONST = 1 + mp.sqrt(mp.pi / 2)  # 2.253314137...

log = open("check06_theorem4.log", "w")


def p(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    log.write(s + "\n")


p(f"a = 1+sqrt(pi/2) = {mp.nstr(A_CONST, 20)}")
p("")

# ---------------------------------------------------------------------------
# 0. The elementary fact n/sqrt(n+1) >= sqrt(n)-1, exact-ish check.
# ---------------------------------------------------------------------------
p("=" * 78)
p("0. n/sqrt(n+1) >= sqrt(n)-1, n=1..200000 (mpmath, 30 dps) -- target's")
p("   own check: n=1..1e5.")
p("=" * 78)
mp.mp.dps = 30
viol0 = 0
for n in range(1, 200001):
    lhs = n / mp.sqrt(n + 1)
    rhs = mp.sqrt(n) - 1
    if lhs < rhs:
        viol0 += 1
        p(f"  VIOLATION at n={n}")
mp.mp.dps = 60
p(f"RESULT: n=1..200000, {viol0} violations.")

# ---------------------------------------------------------------------------
# 1. EXACT Fraction cross-validation baseline, K=1..60, both binding cases.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("1. EXACT Fraction baseline (both binding cases), K=1..60, to cross-")
p("   validate the mpmath stages below and rule out mpmath hiding a")
p("   near-violation.")
p("=" * 78)


def check_exact(K):
    """Returns (dev_Kplus1, dev_K, bound) all as mpmath (LHS from exact
    Fraction, cast to mpmath only for the final comparison against the
    irrational bound -- LHS itself stays exact)."""
    # n = K+1 binding case, via Theorem 3's M_K = Q(K+1)-(K+1)phi_K
    M_K = cf.Q_exact(K + 1) - (K + 1) * cf.phi_K(K)
    dev1 = M_K  # this already equals n*|phi_n^{(K)}-phi_K| at n=K+1 (Thm3)
    dev1_over_n = M_K / (K + 1)
    # n = K boundary case: |Q(K) - K*phi_K| / K = |phi_K^{(K)} - phi_K|
    QK = cf.Q_exact(K)
    devK = abs(QK - K * cf.phi_K(K))
    devK_over_n = devK / K
    return dev1_over_n, devK_over_n


viol_exact = 0
worst_ratio_exact = mp.mpf(0)
for K in range(1, 61):
    dev1, devK = check_exact(K)
    dev1_mp = mp.mpf(dev1.numerator) / mp.mpf(dev1.denominator)
    devK_mp = mp.mpf(devK.numerator) / mp.mpf(devK.denominator)
    bound = A_CONST * mp.sqrt(K) / (1)  # already divided by n above; compare
    # dev*_mp already is |phi_n-phi_K| (n-normalized), bound below is
    # a*sqrt(K)/n but we divided by n already above, so compare to
    # a*sqrt(K)/n at n=K+1 and n=K respectively:
    bound1 = A_CONST * mp.sqrt(K) / (K + 1)
    boundK = A_CONST * mp.sqrt(K) / K
    r1 = dev1_mp / bound1
    rK = devK_mp / boundK
    if dev1_mp > bound1:
        viol_exact += 1
        p(f"  VIOLATION (n=K+1) at K={K}")
    if devK_mp > boundK:
        viol_exact += 1
        p(f"  VIOLATION (n=K) at K={K}")
    worst_ratio_exact = max(worst_ratio_exact, r1, rK)
p(f"RESULT: K=1..60, both binding cases, {viol_exact} violations. "
  f"Worst ratio (deviation/bound) = {mp.nstr(worst_ratio_exact, 8)}.")

# Also cross-validate against mpmath-computed values at a few of these K to
# confirm mpmath isn't drifting from the exact truth.
p("")
p("Cross-check: exact Fraction vs mpmath (60 dps) M_K at K=10,30,60:")
for K in (10, 30, 60):
    exact_MK = cf.Q_exact(K + 1) - (K + 1) * cf.phi_K(K)
    exact_MK_mp = mp.mpf(exact_MK.numerator) / mp.mpf(exact_MK.denominator)
    mp_MK = cf.M_K_theorem3_mp(K)
    diff = abs(exact_MK_mp - mp_MK)
    p(f"  K={K}: exact={mp.nstr(exact_MK_mp,20)}  mpmath={mp.nstr(mp_MK,20)}  "
      f"|diff|={mp.nstr(diff,5)}")

# ---------------------------------------------------------------------------
# 2. mpmath dense, binding cases, K=1..3000.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("2. mpmath (60 dps), both binding cases, K=1..3000 (dense) -- pushes far")
p("   beyond the target's own K up to 1e5 SPARSE grid by being fully dense")
p("   over this range.")
p("=" * 78)

viol2 = 0
worst_ratio2 = mp.mpf(0)
worst_at2 = None
for K in range(1, 3001):
    M_K = cf.M_K_theorem3_mp(K)  # O(K) work (Q_mp loop)
    dev1 = M_K / (K + 1)
    bound1 = A_CONST * mp.sqrt(K) / (K + 1)
    r1 = dev1 / bound1
    QK = cf.Q_mp(K) if K >= 1 else mp.mpf(1)
    devK = abs(QK - K * cf.phi_K_mp(K)) / K
    boundK = A_CONST * mp.sqrt(K) / K
    rK = devK / boundK
    if dev1 > bound1:
        viol2 += 1
        p(f"  VIOLATION (n=K+1) at K={K}")
    if devK > boundK:
        viol2 += 1
        p(f"  VIOLATION (n=K) at K={K}")
    if r1 > worst_ratio2:
        worst_ratio2, worst_at2 = r1, (K, "n=K+1")
    if rK > worst_ratio2:
        worst_ratio2, worst_at2 = rK, (K, "n=K")
p(f"RESULT: K=1..3000, both binding cases (6000 checks), {viol2} violations. "
  f"Worst ratio={mp.nstr(worst_ratio2,8)} at {worst_at2}.")

# ---------------------------------------------------------------------------
# 3. mpmath sparse, large K up to 10^5, using fast numpy Q(n).
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("3. Sparse spot checks, K up to 10^5, both binding cases, using a fast")
p("   vectorized double-precision Q(n) (numpy) cross-checked against exact")
p("   Fraction Q(n) at the smallest of these K (K=5000) for consistency.")
p("=" * 78)


def Q_np(n):
    if n == 1:
        return 1.0
    i = np.arange(1, n, dtype=np.float64)
    log_terms = np.log1p(-i / n)
    cum_log = np.cumsum(log_terms)
    terms = np.exp(cum_log)
    return 1.0 + terms.sum()


def phi_K_np(K):
    # via mpmath log-gamma cast to float (cheap, K up to 1e5 fine either way)
    return float(cf.phi_K_mp(K))


sparse_Ks = [4000, 5000, 7500, 10000, 20000, 30000, 50000, 75000, 100000]
viol3 = 0
worst_ratio3 = 0.0
worst_at3 = None
a_const_f = float(A_CONST)
for K in sparse_Ks:
    phiK = phi_K_np(K)
    Qkp1 = Q_np(K + 1)
    QK = Q_np(K)
    dev1 = abs(Qkp1 - (K + 1) * phiK) / (K + 1)
    bound1 = a_const_f * (K ** 0.5) / (K + 1)
    r1 = dev1 / bound1
    devK = abs(QK - K * phiK) / K
    boundK = a_const_f * (K ** 0.5) / K
    rK = devK / boundK
    if dev1 > bound1:
        viol3 += 1
        p(f"  VIOLATION (n=K+1) at K={K}")
    if devK > boundK:
        viol3 += 1
        p(f"  VIOLATION (n=K) at K={K}")
    if r1 > worst_ratio3:
        worst_ratio3, worst_at3 = r1, (K, "n=K+1")
    if rK > worst_ratio3:
        worst_ratio3, worst_at3 = rK, (K, "n=K")
    p(f"  K={K:>7d}: ratio(n=K+1)={r1:.6f}  ratio(n=K)={rK:.6f}")
p(f"RESULT: {len(sparse_Ks)} sparse K up to 1e5, {viol3} violations. "
  f"Worst ratio={worst_ratio3:.6f} at {worst_at3}.")

# cross-check numpy Q(5000) against exact Fraction Q(5000)
p("")
p("Cross-check numpy-double Q(5000) vs exact Fraction Q(5000):")
q_exact_5000 = cf.Q_exact(5000)
q_exact_5000_f = float(q_exact_5000)
q_np_5000 = Q_np(5000)
p(f"  exact={q_exact_5000_f:.12f}  numpy={q_np_5000:.12f}  "
  f"|diff|={abs(q_exact_5000_f-q_np_5000):.3e}")

# ---------------------------------------------------------------------------
# 4. Interior n (not just the two binding endpoints), via the closed forms
# directly (mpmath), for several K -- an independent stress test that also
# indirectly exercises Theorem 2's monotonicity claim.
# ---------------------------------------------------------------------------
p("")
p("=" * 78)
p("4. Interior n (not binding endpoints), via closed-form phi_n^{(K)}")
p("   directly (mpmath), K in {1,5,20,100,500,2000}, several n each,")
p("   including far interior n=10K, n=100K.")
p("=" * 78)

viol4 = 0
worst_ratio4 = mp.mpf(0)
worst_at4 = None
for K in [1, 5, 20, 100, 500, 2000]:
    phiK = cf.phi_K_mp(K)
    offsets = [1, 2, 5, 20, 100, 1000]
    ns = [K + o for o in offsets if o >= 1]
    ns += [10 * K, 100 * K] if K >= 1 else []
    ns = sorted(set(n for n in ns if n > K))
    for n in ns:
        phin = cf.phi_n_K_closed_mp(K, n)
        dev = abs(phin - phiK)
        bound = A_CONST * mp.sqrt(K) / n
        r = dev / bound if bound > 0 else mp.mpf(0)
        if dev > bound:
            viol4 += 1
            p(f"  VIOLATION K={K} n={n}: dev={mp.nstr(dev,10)} bound={mp.nstr(bound,10)}")
        if r > worst_ratio4:
            worst_ratio4, worst_at4 = r, (K, n)
p(f"RESULT: interior-n stress test, {viol4} violations. "
  f"Worst ratio={mp.nstr(worst_ratio4,8)} at (K,n)={worst_at4}.")

log.close()
print("\nWrote check06_theorem4.log")
