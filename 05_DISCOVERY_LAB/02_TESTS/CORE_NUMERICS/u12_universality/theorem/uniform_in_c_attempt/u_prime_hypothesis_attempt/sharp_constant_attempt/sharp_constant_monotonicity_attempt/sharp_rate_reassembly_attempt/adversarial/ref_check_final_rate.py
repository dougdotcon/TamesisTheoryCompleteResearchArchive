# ref_check_final_rate.py -- referee check R4: Teorema R's final inequality,
#   |phi(n,c) - phi_inf(c)| <= (a* sqrt(c) + kappa_B)/n,  n>=4, 0<=c<=n,
# replicated head-on with the referee's own engine, certified conservative:
#   LHS_hi = max over the phi_inf bracket (phi(n,c) exact rational),
#   RHS_lo = (ASTAR_LO * sqrt_lo(c) + 0.28048)/n   [0.28048 < kappa_B],
# so every PASS is a machine proof of the theorem's inequality at that cell.
#
# R4a: interior grids, n = 4..24 all, then 28..512 selected, n=1024 reduced;
#      c-grid includes the near-boundary cells c = n, n-1/4, n-1/2, n-1.
# R4b: the two halves separately + the Lema 5.1 identity, n in {8,32,128}.
# R4c: boundary line c=n via phi(n,n)=Q(n)/n: exact n=4..600 +
#      {700,800,1000,1500,2000,3000}; certified truncated Q at
#      {5000,10000,30000,50000}  (50000 beyond the target's 30000).
import sys, time
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ref_engine import (phi_K, Q_exact, Q_bracket_truncated, phi_nK_table,
                        phi_mix, phi_inf_bracket, I2_bracket, sqrt_bracket,
                        ASTAR_LO, SQRT_PI_LO, SQRT_PI_HI)
from math import comb

t0 = time.time()
fails = 0
cells = 0
KLO = F(28048, 10**5)      # certified < kappa_B  (R3)
worst = (F(0), None)

def check_cell(n, c, phi_val, tag=""):
    """phi_val = exact rational phi(n,c). Returns ratio."""
    global fails, cells, worst
    cells += 1
    lo, hi = phi_inf_bracket(c)
    lhs_hi = max(abs(phi_val - lo), abs(phi_val - hi))
    rhs_lo = (ASTAR_LO * sqrt_bracket(c)[0] + KLO) / n
    ok = lhs_hi <= rhs_lo
    if not ok:
        fails += 1
        print(f"  ** VIOLATION n={n} c={float(c):.4f} {tag} "
              f"LHS<= {float(lhs_hi):.6e} RHS>= {float(rhs_lo):.6e}")
    r = lhs_hi / rhs_lo
    if r > worst[0]:
        worst = (r, (n, float(c), tag))
    return r

def cgrid(n):
    base = [F(1, 4), F(1, 2), F(1), F(3, 2), F(2), F(3)]
    v = F(4)
    while v < n:
        base.append(v)
        v *= 2
    base += [F(n, 2), F(3 * n, 4), F(n) - 1, F(n) - F(1, 2),
             F(n) - F(1, 4), F(n)]
    return sorted(set(x for x in base if 0 < x <= n))

print("== R4a: interior grids ==")
ns_small = list(range(4, 25))
ns_big = [28, 32, 40, 48, 64, 96, 128, 192, 256, 384, 512]
for n in ns_small + ns_big:
    tab = phi_nK_table(n)
    grid = cgrid(n)
    if n >= 256:
        grid = [F(1, 2), F(1), F(2), F(8), F(32), F(128), F(n, 2),
                F(n) - 1, F(n) - F(1, 2), F(n) - F(1, 4), F(n)]
    for c in grid:
        check_cell(n, c, phi_mix(n, c, tab))
    print(f"  n={n}: {len(grid)} cells done, cum cells={cells}, "
          f"elapsed {time.time()-t0:.0f}s", flush=True)
# n=1024, reduced grid
n = 1024
tab = phi_nK_table(n)
for c in [F(1), F(32), F(512), F(n) - 1, F(n) - F(1, 2), F(n)]:
    check_cell(n, c, phi_mix(n, c, tab))
print(f"  n=1024: 6 cells done, cum cells={cells}, "
      f"elapsed {time.time()-t0:.0f}s", flush=True)

print("== R4b: the two halves + Lema 5.1 identity ==")
half_bad = 0
for n in [8, 32, 128]:
    tab = phi_nK_table(n)
    phiK_list = [phi_K(K) for K in range(n + 1)]
    for c in [F(1, 2), F(1), F(2), F(5), F(10), F(20), F(n, 2),
              F(n) - 1, F(n)]:
        if not (0 < c <= n):
            continue
        p, q = c.numerator, c.denominator
        a, b = p, n * q - p
        D = F((n * q)**n)
        bK = [F(comb(n, K) * a**K * b**(n - K)) / D for K in range(n + 1)]
        # A_n exact:
        A = sum(bK[K] * (tab[K] - phiK_list[K]) for K in range(n + 1))
        okA = abs(A) <= ASTAR_LO * sqrt_bracket(c)[0] / n
        # Lema 5.1 identity: sum_K bK phi_K == sum_k C(n,k)(-c/n)^k/(2k+1)
        S1 = sum(bK[K] * phiK_list[K] for K in range(n + 1))
        S2 = sum(F(comb(n, k) * (-p)**k, (n * q)**k) / (2 * k + 1)
                 for k in range(n + 1))
        okI = (S1 == S2)
        # B_n bracket vs c^2 I2(c)/n (conservative: I2 lower bound)
        phv = phi_mix(n, c, tab)
        lo, hi = phi_inf_bracket(c)
        B_lo, B_hi = phv - hi - A, phv - lo - A
        Babs_hi = max(abs(B_lo), abs(B_hi))
        i2lo = I2_bracket(c)[0]
        okB = Babs_hi <= c * c * i2lo / n
        okS = B_hi <= F(1, 10**30)      # Lema 5.1 sign: B_n <= 0
        if not (okA and okI and okB and okS):
            half_bad += 1
            print(f"  ** HALF-CHECK FAIL n={n} c={float(c):.3f} "
                  f"A:{okA} I:{okI} B:{okB} sign:{okS}")
    print(f"  n={n}: halves+identity done, elapsed {time.time()-t0:.0f}s",
          flush=True)
if half_bad == 0:
    print("  all per-half checks pass (A-half, B-half, Lema 5.1 identity, "
          "B_n<=0)")
fails += half_bad

print("== R4c: boundary line c=n via phi(n,n)=Q(n)/n ==")
bcells = 0
for n in list(range(4, 601)) + [700, 800, 1000, 1500, 2000, 3000]:
    c = F(n)
    check_cell(n, c, Q_exact(n) / n, tag="bdry")
    bcells += 1
print(f"  exact boundary n=4..600 + sparse to 3000: {bcells} cells, "
      f"elapsed {time.time()-t0:.0f}s", flush=True)
for n in [5000, 10000, 30000, 50000]:
    cells += 1
    bcells += 1
    Qlo, Qhi = Q_bracket_truncated(n)
    slo, shi = sqrt_bracket(n)
    # phi_inf(n) in (sqrt(pi)/(2 sqrt n) - 2^-n/(2n), sqrt(pi)/(2 sqrt n))
    pi_lo = SQRT_PI_LO / (2 * shi) - F(1, 2 * n * 2**n)
    pi_hi = SQRT_PI_HI / (2 * slo)
    lhs_hi = max(abs(Qlo / n - pi_hi), abs(Qhi / n - pi_lo))
    rhs_lo = (ASTAR_LO * slo + KLO) / n
    ok = lhs_hi <= rhs_lo
    if not ok:
        fails += 1
    r = lhs_hi / rhs_lo
    if r > worst[0]:
        worst = (r, (n, float(n), "bdry-trunc"))
    print(f"  n={n} (truncated Q): ratio={float(r):.6f} pass={ok}")

print(f"== R4 SUMMARY: {cells} certified cells, {fails} violations ==")
print(f"  worst LHS/RHS = {float(worst[0]):.6f} at {worst[1]}")
print(f"  elapsed {time.time()-t0:.0f}s")
sys.exit(1 if fails else 0)
