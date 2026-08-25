# verify_final_rate.py -- T4: certified verification, at scale, of the
# reassembled SHARP rate (Teorema R of this front's ATTEMPT.md):
#
#     |phi(n,c) - phi_inf(c)|  <=  (a* sqrt(c) + kappa_B) / n
#     for all integers n >= 4 and all 0 <= c <= n,
#     a* = sqrt(pi)(1/sqrt2 - 1/2),  kappa_B = sup_c c^2 I2(c) in (0.28048, 0.2805).
#
# Certified direction: LHS upper bracket vs RHS lower bound
#     RHS_lo = (ASTAR_LO * sqrt_lo(c) + KAPPA_LO)/n,  KAPPA_LO = 0.28048 < kappa_B,
# so every PASS certifies the theorem's inequality at that (n,c).
# Also checked per-half (the two summands of the assembly):
#     |A_n(c)| <= a* sqrt(c)/n     (exact rational A_n)
#     |B_n(c)| <= c^2 I2(c)/n      (bracketed B_n)
# plus the exact Lema 5.1 identity  sum_K b_K phi_K = int_0^1 (1-ct^2/n)^n dt.
# All Fraction; no float in any certified comparison. Deterministic; no seed.

import sys, time
from fractions import Fraction
from math import comb
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from engine import (phi_K, Q_exact, Q_bracket_truncated, phi_nK_table,
                    phi_finite, phi_inf_bracket, I2_bracket,
                    ASTAR_LO, ASTAR_HI, KAPPA_LO, sqrt_lo, sqrt_hi)

t0 = time.time()
fails = 0
total_cells = 0
max_ratio = Fraction(0)      # max over cells of LHS_hi / RHS_lo (certified <=1 needed)
max_ratio_cell = None


def c_grid(n):
    cs = set(Fraction(j * n, 40) for j in range(41))
    for extra in [Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2),
                  Fraction(2284, 1000), Fraction(4086754546, 10**9),
                  Fraction(5), Fraction(10),
                  n - Fraction(1, 4), n - Fraction(1, 2), n - 1]:
        if 0 <= extra <= n:
            cs.add(extra)
    return sorted(cs)


def check_cell(n, c, phin, tag=""):
    """Certified check of the final inequality at (n, c). phin = phi(n,c) exact."""
    global fails, total_cells, max_ratio, max_ratio_cell
    total_cells += 1
    lo, hi = phi_inf_bracket(c)
    lhs_hi = max(abs(phin - lo), abs(phin - hi))
    rhs_lo = (ASTAR_LO * sqrt_lo(c) + KAPPA_LO) / n
    if lhs_hi > rhs_lo:
        fails += 1
        print(f"  VIOLATION{tag} n={n} c={c}: LHS<= {float(lhs_hi):.9f} "
              f"RHS>= {float(rhs_lo):.9f}")
        return
    r = lhs_hi / rhs_lo
    if r > max_ratio:
        max_ratio, max_ratio_cell = r, (n, c)


# ---- T4a: main grid ------------------------------------------------------
print("== T4a: full grid, exact phi(n,c) via mixture + closed forms ==")
n_list = (list(range(4, 25)) + [28, 32, 40, 48, 56, 64, 80, 96, 112, 128,
                                160, 192, 224, 256, 320, 384, 448, 512, 1024])
for n in n_list:
    tab = phi_nK_table(n)
    cs = c_grid(n) if n <= 512 else \
        sorted(set(Fraction(j * n, 8) for j in range(9))
               | {Fraction(1), Fraction(5), n - Fraction(1, 4)})
    for c in cs:
        check_cell(n, c, phi_finite(n, c, tab))
    print(f"  n={n}: {len(cs)} c-values done  [{time.time()-t0:.0f}s]")

# ---- T4b: per-half checks + Lema 5.1 identity ---------------------------
print("== T4b: per-half |A_n|, |B_n| and the exact Lema 5.1 identity ==")
half_fails = 0
half_cells = 0
for n in [8, 32, 128]:
    tab = phi_nK_table(n)
    phiKs = [phi_K(K) for K in range(n + 1)]
    for c in [Fraction(j * n, 10) for j in range(11)] + [n - Fraction(1, 2)]:
        if not (0 <= c <= n):
            continue
        half_cells += 1
        p = Fraction(c, n)
        q = 1 - p
        w = [comb(n, K) * p**K * q ** (n - K) for K in range(n + 1)]
        mixK = sum(wk * fk for wk, fk in zip(w, phiKs))          # sum b_K phi_K
        poly = sum(comb(n, k) * (-p) ** k * Fraction(1, 2 * k + 1)
                   for k in range(n + 1))                        # int_0^1 (1-ct^2/n)^n dt
        if mixK != poly:
            half_fails += 1
            print(f"  LEMA 5.1 IDENTITY FAIL n={n} c={c}")
        phin = phi_finite(n, c, tab)
        A = phin - mixK                                          # exact rational
        if abs(A) > ASTAR_LO * sqrt_lo(c) / n and c > 0:
            half_fails += 1
            print(f"  A-HALF VIOLATION n={n} c={c}: |A|={float(abs(A)):.3e} "
                  f"vs {float(ASTAR_LO*sqrt_lo(c)/n):.3e}")
        lo, hi = phi_inf_bracket(c)
        B_hi = max(abs(mixK - lo), abs(mixK - hi))
        i2lo, _ = I2_bracket(c)
        if B_hi > c * c * i2lo / n if c > 0 else B_hi > 0:
            half_fails += 1
            print(f"  B-HALF VIOLATION n={n} c={c}: |B|<={float(B_hi):.3e} "
                  f"vs c^2 I2/n>={float(c*c*i2lo/n):.3e}")
print(f"[{'PASS' if half_fails == 0 else 'FAIL'}] {half_cells} cells x 3 checks, "
      f"{half_fails} violations  [{time.time()-t0:.0f}s]")
fails += (half_fails != 0)

# ---- T4c: boundary line c = n, large n ----------------------------------
print("== T4c: boundary c=n (phi(n,n)=Q(n)/n exactly), n to 30000 ==")
for n in list(range(4, 601)) + [700, 800, 1000, 1500, 2000, 3000]:
    check_cell(n, Fraction(n), Q_exact(n) / n, tag="/bnd")
print(f"  exact-Q boundary n=4..600 + sparse to 3000 done  [{time.time()-t0:.0f}s]")
for n in [5000, 10000, 30000]:
    qlo, qhi = Q_bracket_truncated(n)
    c = Fraction(n)
    lo, hi = phi_inf_bracket(c)
    lhs_hi = max(abs(qlo / n - lo), abs(qhi / n - hi),
                 abs(qlo / n - hi), abs(qhi / n - lo))
    rhs_lo = (ASTAR_LO * sqrt_lo(c) + KAPPA_LO) / n
    total_cells += 1
    ok = lhs_hi <= rhs_lo
    if not ok:
        fails += 1
    print(f"  n={n}: n*LHS <= {float(n*lhs_hi):.6f} vs n*RHS >= {float(n*rhs_lo):.6f} "
          f"[{'ok' if ok else 'VIOLATION'}]")

print(f"\n== SUMMARY ==")
print(f"cells checked (certified): {total_cells}")
print(f"violations of the final inequality: "
      f"{fails if fails else 0} (target: 0)")
if max_ratio_cell:
    print(f"max LHS/RHS ratio: {float(max_ratio):.6f} at n={max_ratio_cell[0]}, "
          f"c={max_ratio_cell[1]} (= {float(max_ratio_cell[1]):.4f})")
print(f"time: {time.time()-t0:.1f}s")
sys.exit(1 if fails else 0)
