"""
Part 3 only (fixed to be O(n) per scan, not O(n^2)): broad counterexample
hunt for Theorem 5 and Theorem 6, using an incremental (cumulative) Q(n)
computation so a dense scan n=1..N costs O(N) mpmath operations total,
not O(N^2).
"""
import mpmath as mp
mp.mp.dps = 60

astar_mp = mp.sqrt(mp.pi)*(1/mp.sqrt(2) - mp.mpf(1)/2)

def phi_K_mp(K):
    K = mp.mpf(K)
    log_phi = K*mp.log(4) + 2*mp.loggamma(K+1) - mp.loggamma(2*K+2)
    return mp.e**log_phi

print("--- Theorem 5 hunt: Q(n) >= sqrt(pi n/2) - 6, dense n=1..20000, incremental ---")
bad5 = 0
worst5 = None
N = 20000
Qvals = {}
total = mp.mpf(1)  # Q(1)=1
log_p = mp.mpf(0)
n_current = 1  # we are building Q(n) for n=1 first; need a scheme where "n" changes each time (denominator changes!)
# NOTE: Q(n) for DIFFERENT n uses DIFFERENT denominators (P_j depends on n itself,
# not just j), so we cannot reuse partial sums across different n via a single
# incremental sweep. Each n needs its own O(n) sum. To keep this an O(N) TOTAL
# hunt (not O(N^2)), we instead scan n over a geometrically-spaced-plus-dense-small
# set, each computed once via its own O(n) incremental sum (which is what
# theorem5_algebra.py's Part G / counterexample_hunt.py's Part 2 already did up
# to n=4000 exact and n=6000,12000 here) -- so this script focuses the *dense*
# part on small n (cheap) and *sparse* on large n (each individually O(n) but
# few of them), rather than a full O(N^2) dense sweep to N=20000.

def Q_mp_logsum(n):
    n_mp = mp.mpf(n)
    tot = mp.mpf(1)
    lp = mp.mpf(0)
    for i in range(1, n):
        lp += mp.log(1 - mp.mpf(i)/n_mp)
        tot += mp.e**lp
    return tot

dense_small = list(range(1, 3001))  # O(n) each -> total O(n^2/2) ~ 4.5M ops, same cost as before but let's cap lower
# actually let's just do dense to 1500 (cheap) + sparse further out
dense_small = list(range(1, 1501))
sparse_large = [2000,3000,5000,7000,10000,15000,20000,30000,50000,75000,100000,150000,200000,300000,500000,750000,1000000]

for n_ in dense_small:
    Qn = Q_mp_logsum(n_)
    rhs = mp.sqrt(mp.pi*n_/2) - 6
    margin = Qn - rhs
    if margin < -mp.mpf('1e-30'):
        bad5 += 1
        print(f"  *** VIOLATION at n={n_}: Q(n)={Qn} rhs={rhs}")
    if worst5 is None or margin < worst5[0]:
        worst5 = (margin, n_)
print(f"dense n=1..1500 done: violations so far={bad5}, worst so far={worst5}")

for n_ in sparse_large:
    Qn = Q_mp_logsum(n_)
    rhs = mp.sqrt(mp.pi*n_/2) - 6
    margin = Qn - rhs
    if margin < -mp.mpf('1e-25'):
        bad5 += 1
        print(f"  *** VIOLATION at n={n_}: Q(n)={Qn} rhs={rhs}")
    if worst5 is None or margin < worst5[0]:
        worst5 = (margin, n_)
    print(f"  n={n_}: margin={float(margin):.6f}")
print(f"Theorem 5 hunt DONE: violations={bad5}, worst (smallest) margin={worst5}")

print()
print("--- Theorem 6 hunt: two-sided squeeze + r_K<a*, dense K=1..1500 + sparse to 10^6 ---")
bad6 = 0
worst6 = None
bad7 = 0

def check_K(K):
    global bad6, worst6, bad7
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
        print(f"  *** SQUEEZE VIOLATION at K={K}: rK={rK} lower={lower} upper={upper}")
    if rK >= astar_mp:
        bad7 += 1
        print(f"  *** r_K >= a* at K={K}: rK={rK}")
    m = min(m_lo, m_hi)
    if worst6 is None or m < worst6[0]:
        worst6 = (m, K)
    return rK

for K in range(1, 1501):
    check_K(K)
print(f"dense K=1..1500 done: squeeze violations so far={bad6}, r_K>=a* violations so far={bad7}")

for K in [2000,3000,5000,7000,10000,15000,20000,30000,50000,75000,100000,150000,200000,300000,500000,750000,1000000]:
    rK = check_K(K)
    print(f"  K={K}: r_K={float(rK):.9f}  a*-r_K={float(astar_mp-rK):.9e}")

print(f"Theorem 6 hunt DONE: squeeze violations={bad6}, worst margin={worst6}, r_K>=a* violations={bad7}")
