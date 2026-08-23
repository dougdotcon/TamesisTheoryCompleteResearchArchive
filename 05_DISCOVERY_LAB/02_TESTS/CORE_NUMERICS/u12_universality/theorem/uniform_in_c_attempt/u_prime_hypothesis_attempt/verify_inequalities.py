"""T5 of DERIVATION_PREREG.md -- sanity checks (mpmath, 40 digits) on the
elementary real-analysis inequalities the hand proof of Claim 4 uses. These
are NOT the proof (the proof is the algebra in ATTEMPT.md); this is a wide
numerical sanity net to catch any transcription error in that algebra.
"""
import mpmath as mp
mp.mp.dps = 40


def phi_K_mp(K):
    return mp.mpf(4) ** K * mp.gamma(K + 1) ** 2 / mp.gamma(2 * K + 2)


def Q_mp(n):
    s = mp.mpf(0)
    prod = mp.mpf(1)
    for j in range(0, n):
        s += prod
        prod *= (1 - mp.mpf(j + 1) / n)
    return s


astar = mp.sqrt(mp.pi) * (1 / mp.sqrt(2) - mp.mpf(1) / 2)
a_final = 1 + mp.sqrt(mp.pi / 2)
print("a* (sharp, not claimed here) =", astar)
print("a  (this document's explicit, non-sharp constant) = 1+sqrt(pi/2) =", a_final)
print()

Ks_wide = [1, 2, 3, 5, 10, 20, 50, 100, 300, 1000, 3000, 10000, 30000, 100000]

print("=== (5a) phi_K sandwich: sqrt(pi)/(2 sqrt(K+1)) < phi_K < sqrt(pi)/(2 sqrt(K)), K>=1 ===")
bad = 0
for K in Ks_wide:
    pk = phi_K_mp(K)
    lo = mp.sqrt(mp.pi) / (2 * mp.sqrt(K + 1))
    hi = mp.sqrt(mp.pi) / (2 * mp.sqrt(K))
    ok = lo < pk < hi
    if not ok:
        bad += 1
        print(f"  VIOLATION K={K}")
print("PASS" if bad == 0 else f"FAIL ({bad})")

print()
print("=== (5b) Q(n) <= 1+sqrt(pi n/2), n=1..100000 (dense small n + wide grid) ===")
bad = 0
for n in list(range(1, 200)) + Ks_wide:
    q = Q_mp(n)
    ub = 1 + mp.sqrt(mp.pi * n / 2)
    if not (q <= ub):
        bad += 1
        print(f"  VIOLATION n={n}")
print("PASS" if bad == 0 else f"FAIL ({bad})")

print()
print("=== (5c) n/sqrt(n+1) >= sqrt(n)-1, n=1..100000 ===")
bad = 0
for n in list(range(1, 200)) + Ks_wide:
    lhs = n / mp.sqrt(n + 1)
    rhs = mp.sqrt(n) - 1
    if not (lhs >= rhs):
        bad += 1
        print(f"  VIOLATION n={n}")
print("PASS" if bad == 0 else f"FAIL ({bad})")

print()
print("=== (5d) assembled bound |phi_n^{(K)}-phi_K| <= a*sqrt(K)/n at n=K+1 and n=K, K=1..100000 ===")
bad = 0
worst_ratio = mp.mpf(0)
for K in Ks_wide:
    pk = phi_K_mp(K)
    # n = K+1 case: use exact M_K formula, proved in T4/Claim 3
    Mk = Q_mp(K + 1) - (K + 1) * pk
    lhs1 = Mk / (K + 1)
    rhs = a_final * mp.sqrt(K) / (K + 1)
    ok1 = lhs1 <= rhs
    # n = K case (K=n boundary): phi_n^{(n)} = Q(n)/n
    diffK = Q_mp(K) - K * pk
    lhs2 = abs(diffK) / K
    rhs2 = a_final * mp.sqrt(K) / K
    ok2 = lhs2 <= rhs2
    r1 = lhs1 / (mp.sqrt(K) / (K + 1)) if K > 0 else mp.mpf(0)
    r2 = lhs2 / (mp.sqrt(K) / K) if K > 0 else mp.mpf(0)
    worst_ratio = max(worst_ratio, r1, r2)
    if not (ok1 and ok2):
        bad += 1
        print(f"  VIOLATION K={K}  ok1={ok1} ok2={ok2}")
print(f"worst observed |phi_n^(K)-phi_K|*n/sqrt(K) over this grid = {float(worst_ratio):.6f}  (bound a={float(a_final):.6f})")
print("PASS" if bad == 0 else f"FAIL ({bad})")

print()
print("=== (5e) interior n also respect the bound (redundant with monotonicity, checked anyway) ===")
bad = 0
for K in [1, 5, 20, 100, 1000]:
    pk = phi_K_mp(K)
    for mult in [1, 2, 5, 20, 100]:
        n = K + mult
        # use exact M_K/n as an upper bound proxy is circular; instead reconstruct
        # phi_n^{(K)} via the SAME closed form used in verify_closed_form (float here)
        def g(i, nn):
            p = mp.mpf(1)
            for l in range(1, i + 1):
                p *= (nn + l) / mp.mpf(nn)
            return p
        A = mp.gamma(K + 1) ** 2 / mp.gamma(2 * K + 2)
        psi = A * sum(mp.binomial(2 * K + 1, K - j) * g(j, n) for j in range(0, K + 1))
        if K == 0:
            phinK = mp.mpf(1)
        else:
            kappa = mp.gamma(K) * mp.gamma(K + 1) / mp.gamma(2 * K + 1)
            psiR = kappa * sum(mp.binomial(2 * K, K - i) * g(i, n) for i in range(1, K + 1))
            phinK = (K / mp.mpf(n)) * psiR + (1 - K / mp.mpf(n)) * psi
        diff = abs(phinK - pk)
        bound = a_final * mp.sqrt(K) / n
        if not (diff <= bound):
            bad += 1
            print(f"  VIOLATION K={K} n={n}")
print("PASS" if bad == 0 else f"FAIL ({bad})")
