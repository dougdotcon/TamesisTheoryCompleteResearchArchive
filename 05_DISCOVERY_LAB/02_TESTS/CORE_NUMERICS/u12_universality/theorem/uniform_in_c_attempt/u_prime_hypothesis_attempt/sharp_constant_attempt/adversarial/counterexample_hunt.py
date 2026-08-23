"""
Dedicated counterexample hunt + self-consistency check on the target
document's own stated figures (grid sizes, worst margins).

Part 1: does the document's §2 sentence "grid n=1,...,59 plus
n in {80,120,200,400,800,1500,3000,6000,12000}" actually total the "66/66"
figure reported in the Files section? (Pure arithmetic on the document's
own prose, not a math claim about Q(n).)

Part 2: independently verify Q(n) >= sqrt(pi n/2) - 6 AT exactly n=6000 and
n=12000 (the two values named in §2's prose but seemingly not reflected in
the "66/66"/"n up to 3000" Files-section figure), via a fast mpmath
log-sum Q(n) (cross-checked against exact Fraction at a smaller n to
confirm the log-sum method itself is correct).

Part 3: a broad, somewhat adversarial hunt for any (n) violating Theorem 5
or (K) violating Theorem 6's two-sided squeeze, scanning many values,
including edge cases (n=1, very large n, K near where 6/sqrt(K) ~ a*, etc).
"""
import mpmath as mp
from fractions import Fraction as F

mp.mp.dps = 60

print("=== Part 1: arithmetic on the document's own stated grid ===")
grid_dense = list(range(1, 60))  # "n=1,...,59"
grid_sparse = [80,120,200,400,800,1500,3000,6000,12000]
total_as_written = len(grid_dense) + len(grid_sparse)
print(f"len(n=1..59) = {len(grid_dense)}")
print(f"len({{80,...,12000}}) = {len(grid_sparse)}")
print(f"total if §2's prose grid is taken literally = {total_as_written}")
print("document's Files section claims: 66/66")
grid_sparse_no_6k_12k = [80,120,200,400,800,1500,3000]
total_without_6k12k = len(grid_dense) + len(grid_sparse_no_6k_12k)
print(f"total if 6000,12000 are DROPPED from the sparse set = {total_without_6k12k}")

print()
print("=== Part 2: verify Q(n)>=sqrt(pi n/2)-6 exactly at n=6000, n=12000 ===")

def Q_exact_frac(n):
    total = F(1)
    p = F(1)
    for i in range(1, n):
        p *= F(n - i, n)
        total += p
    return total

def Q_mp_logsum(n):
    n_mp = mp.mpf(n)
    total = mp.mpf(1)
    log_p = mp.mpf(0)
    for i in range(1, n):
        log_p += mp.log(1 - mp.mpf(i)/n_mp)
        total += mp.e**log_p
    return total

# cross-validate the log-sum method against exact Fraction at a moderate n
n_check = 2000
Q_exact_val = Q_exact_frac(n_check)
Q_exact_mp = mp.mpf(Q_exact_val.numerator)/mp.mpf(Q_exact_val.denominator)
Q_logsum_val = Q_mp_logsum(n_check)
print(f"cross-check at n={n_check}: exact Fraction Q(n)={Q_exact_mp}")
print(f"                            mpmath log-sum Q(n)={Q_logsum_val}")
print(f"                            |diff|={abs(Q_exact_mp-Q_logsum_val)} (expect ~0, method validated)")

for n_ in [6000, 12000]:
    Qn = Q_mp_logsum(n_)
    rhs = mp.sqrt(mp.pi*n_/2) - 6
    margin = Qn - rhs
    print(f"n={n_}: Q(n)={Qn}  sqrt(pi n/2)-6={rhs}  margin={margin}  "
          f"{'HOLDS' if margin >= 0 else '*** VIOLATION ***'}")

print()
print("=== Part 3: broad counterexample hunt ===")

def phi_K_mp(K):
    K = mp.mpf(K)
    log_phi = K*mp.log(4) + 2*mp.loggamma(K+1) - mp.loggamma(2*K+2)
    return mp.e**log_phi

astar_mp = mp.sqrt(mp.pi)*(1/mp.sqrt(2) - mp.mpf(1)/2)

print("--- Theorem 5 hunt: Q(n) >= sqrt(pi n/2) - 6, n=1..2000 dense + sparse to 10^6 ---")
bad5 = 0
worst5 = None
# dense small-n exact
for n_ in range(1, 2001):
    Qn_frac = None
# use log-sum for speed across the whole dense range (already cross-validated above)
log_p = mp.mpf(0)
running = {}
for n_ in range(1, 2001):
    Qn = Q_mp_logsum(n_)
    rhs = mp.sqrt(mp.pi*n_/2) - 6
    margin = Qn - rhs
    if margin < -mp.mpf('1e-30'):
        bad5 += 1
        print(f"  *** VIOLATION at n={n_}: Q(n)={Qn} rhs={rhs}")
    if worst5 is None or margin < worst5[0]:
        worst5 = (margin, n_)
for n_ in [3000,5000,10000,20000,50000,100000,300000,1000000]:
    Qn = Q_mp_logsum(n_)
    rhs = mp.sqrt(mp.pi*n_/2) - 6
    margin = Qn - rhs
    if margin < -mp.mpf('1e-25'):
        bad5 += 1
        print(f"  *** VIOLATION at n={n_}: Q(n)={Qn} rhs={rhs}")
    if worst5 is None or margin < worst5[0]:
        worst5 = (margin, n_)
print(f"Theorem 5 hunt: n=1..2000 dense + sparse to 10^6, violations={bad5}, worst margin={worst5}")

print("\n--- Theorem 6 hunt: two-sided squeeze on r_K=M_K/sqrt(K), K=1..2000 dense + sparse to 2*10^5 ---")
bad6 = 0
worst6 = None
for K in list(range(1, 2001)) + [3000,5000,10000,30000,50000,100000,200000]:
    K_mp = mp.mpf(K)
    phiK = phi_K_mp(K)
    QK1 = Q_mp_logsum(K+1)
    MK = QK1 - (K+1)*phiK
    rK = MK/mp.sqrt(K_mp)
    lower = astar_mp - (mp.sqrt(mp.pi)/2)/K_mp - 6/mp.sqrt(K_mp)
    upper = astar_mp + 1/mp.sqrt(K_mp) + astar_mp/(2*K_mp)
    m_lo = rK - lower
    m_hi = upper - rK
    if m_lo < -mp.mpf('1e-25') or m_hi < -mp.mpf('1e-25'):
        bad6 += 1
        print(f"  *** VIOLATION at K={K}: rK={rK} lower={lower} upper={upper}")
    m = min(m_lo, m_hi)
    if worst6 is None or m < worst6[0]:
        worst6 = (m, K, 'lo' if m_lo < m_hi else 'hi')
print(f"Theorem 6 squeeze hunt: violations={bad6}, worst margin(min of both sides)={worst6}")

print("\n--- direct check: does r_K ever reach/exceed a* itself, K up to 2*10^5? ---")
bad7 = 0
for K in [1,2,5,10,50,100,500,1000,5000,10000,50000,100000,200000]:
    K_mp = mp.mpf(K)
    phiK = phi_K_mp(K)
    QK1 = Q_mp_logsum(K+1)
    MK = QK1 - (K+1)*phiK
    rK = MK/mp.sqrt(K_mp)
    ok = rK < astar_mp
    if not ok:
        bad7 += 1
        print(f"  *** r_K >= a* at K={K}: rK={rK} a*={astar_mp}")
    print(f"  K={K}: r_K={float(rK):.9f}  a*={float(astar_mp):.9f}  a*-r_K={float(astar_mp-rK):.9e}")
print(f"violations (r_K>=a*) = {bad7}")
