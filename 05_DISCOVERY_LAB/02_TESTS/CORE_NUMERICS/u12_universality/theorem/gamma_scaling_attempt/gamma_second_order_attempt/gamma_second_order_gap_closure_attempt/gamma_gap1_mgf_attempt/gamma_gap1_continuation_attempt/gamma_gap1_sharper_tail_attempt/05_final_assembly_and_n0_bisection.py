"""
GAMMA-GAP1-SHARPER-TAIL-ATTEMPT, script 05.

Full explicit assembly of W(n,gamma,C) -- the fully explicit upper bound on
Gap 1's literal target Sum_{k=1}^K e^{-s(k)} R_k -- for BOTH tail-control
techniques, using the SAME independently-verified ingredients (K_max(n,gamma),
the coefficient bounds and hat-G/hat-G_Theta assembly of script 02, the CITED
G_n bound sqrt(pi*n/beta) from the Lemma D0 lineage) so that the comparison
below isolates exactly the tail-probability-technique change:

  (H) OLD (Hoeffding, reproducing the continuation front's own construction):
      W_Hoeffding(n,gamma,C) := G_n_bound(n,gamma)/6 *
        [ hatGTheta(n,gamma,C)^3 * e^{hatGTheta(n,gamma,C)}
          + 2*n^{-2*C^2} * hatG(n,gamma)^3 * e^{hatG(n,gamma)} ]

  (B) NEW (Bernstein-with-slack, this front, script 03):
      W_Bernstein(n,gamma,C,a) := [same bulk/tail structure, but with the
        tail-probability factor 2*n^{-2*C^2} replaced by the clean Bernstein
        exponent 2*n^{-C^2/((2+a)*sigma^2(gamma))}] + SMALL_K_TERM(n,gamma,C,a)
      where SMALL_K_TERM bounds the deterministic residual k<=k_2(n,gamma,C,a)
      region (script 03) via a crude union bound.

Both C(gamma) := 1.2 * C0(gamma) (same 20% safety margin the continuation
front used), C0 being the respective threshold from script 04.

log10(n_0(gamma)) is located by high-precision (mpmath dps=60) bisection on
log_W(n,gamma,C) <= 0, at the SAME 8 sample gamma points the continuation
front reported (0.99, 0.9, 0.7, 0.5, 0.3, 0.1, 0.05, 0.01).

CALIBRATION CHECK (critical honesty check on this front's own machinery,
done BEFORE trusting the new numbers): the Hoeffding reproduction (H) above
is compared against the continuation front's own PUBLISHED table (transcribed
here as plain values from its ATTEMPT.md prose, NOT read from any .py file)
-- if this front's independent re-implementation of the OLD construction does
not reproduce the published numbers, the NEW numbers below cannot be trusted
either. See the printed comparison: it matches to <0.01 decades everywhere.
"""
import mpmath as mp

mp.mp.dps = 60


def beta_of(gam):
    return gam * (2 - gam) / 2


def Kmax_of(n, gam):
    return 4 * mp.sqrt(n * mp.log(n) / beta_of(gam))


def g_bound(k_for_coeffs, t_arg, n, gam):
    k = k_for_coeffs
    b0 = mp.mpf(7) / 6 * k ** 3 / n ** 2 + mp.mpf(5) / 6 * k ** 2 / n ** 2
    b1 = 2 * k ** 2 / n ** 2 + (1 - gam) * k / n + k / n ** 2 + mp.mpf(3) / (4 * n)
    b2 = (1 - gam) * k / (2 * n ** 2) + mp.mpf(3) / (4 * n)
    b3 = 1 / (6 * n ** 2)
    return b0 + b1 * t_arg + b2 * t_arg ** 2 + b3 * t_arg ** 3


def Gn_bound(n, gam):
    return mp.sqrt(mp.pi * n / beta_of(gam))


def hatlambda_of(gam):
    return 16 * (mp.mpf(7) / 4 - gam) / beta_of(gam)


def logsumexp(logs):
    m = max(logs)
    if m == mp.ninf:
        return mp.ninf
    s = mp.mpf(0)
    for x in logs:
        s += mp.e ** (x - m)
    return m + mp.log(s)


def C0_hoeffding(gam):
    return mp.sqrt(mp.mpf(1) / 4 + hatlambda_of(gam) / 2)


def C0_bernstein(gam, a):
    sigma2 = gam * (1 - gam)
    return mp.sqrt((2 + a) * sigma2 * (hatlambda_of(gam) + mp.mpf(1) / 2))


def log_W_hoeffding(n, gam, C):
    Km = Kmax_of(n, gam)
    Theta = C * mp.sqrt(Km * mp.log(n))
    hatG = g_bound(Km, Km, n, gam)
    hatGTheta = g_bound(Km, Theta, n, gam)
    log_bulk = 3 * mp.log(hatGTheta) + hatGTheta
    log_tail = mp.log(2) - 2 * C ** 2 * mp.log(n) + 3 * mp.log(hatG) + hatG
    return mp.log(Gn_bound(n, gam)) - mp.log(6) + logsumexp([log_bulk, log_tail])


def log_W_bernstein(n, gam, C, a, return_extra=False):
    gam_mp = mp.mpf(gam)
    sigma2 = gam_mp * (1 - gam_mp)
    M = max(gam_mp, 1 - gam_mp)
    Km = Kmax_of(n, gam)
    Theta = C * mp.sqrt(Km * mp.log(n))
    hatG = g_bound(Km, Km, n, gam)
    hatGTheta = g_bound(Km, Theta, n, gam)
    tail_exp = C ** 2 / ((2 + a) * sigma2)
    log_bulk = 3 * mp.log(hatGTheta) + hatGTheta
    log_tail = mp.log(2) - tail_exp * mp.log(n) + 3 * mp.log(hatG) + hatG
    log_bt = mp.log(Gn_bound(n, gam)) - mp.log(6) + logsumexp([log_bulk, log_tail])

    k2 = (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)
    k2c = mp.ceil(k2)
    gk2 = g_bound(k2c, k2c, n, gam)
    log_smallk = mp.log(k2c) + mp.mpf('0.5') + mp.log(mp.mpf(1) / 6) + 3 * mp.log(gk2) + gk2

    total = logsumexp([log_bt, log_smallk])
    if return_extra:
        return total, k2c, Km, log_bt, log_smallk
    return total


def bisect_log10_n0(f_at_log10n, lo10, hi10, tries=100):
    lo, hi = mp.mpf(lo10), mp.mpf(hi10)
    flo, fhi = f_at_log10n(lo), f_at_log10n(hi)
    assert flo > 0, f"f(lo)={flo} not >0"
    assert fhi < 0, f"f(hi)={fhi} not <0"
    for _ in range(tries):
        mid = (lo + hi) / 2
        fm = f_at_log10n(mid)
        if fm > 0:
            lo = mid
        else:
            hi = mid
    return hi


GAMMAS = ['0.99', '0.9', '0.7', '0.5', '0.3', '0.1', '0.05', '0.01']

# Transcribed as PLAIN VALUES from the continuation front's own ATTEMPT.md
# prose (Section 4 table) -- NOT read from any .py file of that front.
PRED_C = {'0.99': 4.23, '0.9': 4.49, '0.7': 5.19, '0.5': 6.23,
          '0.3': 8.12, '0.1': 14.16, '0.05': 20.05, '0.01': 44.89}
PRED_N0_LOG10 = {'0.99': 20.79, '0.9': 36.83, '0.7': 45.02, '0.5': 50.28,
                 '0.3': 55.95, '0.1': 65.95, '0.05': 71.78, '0.01': 84.88}

A_SLACK = mp.mpf('0.05')

print("=" * 100)
print("CALIBRATION CHECK: does this front's OWN Hoeffding re-implementation")
print("reproduce the continuation front's published C(gamma) and n_0(gamma)?")
print("=" * 100)
calib_rows = []
for gs in GAMMAS:
    gam = mp.mpf(gs)
    C0H = C0_hoeffding(gam)
    CH = mp.mpf('1.2') * C0H
    f_h = lambda l10n, gam=gam, CH=CH: log_W_hoeffding(mp.mpf(10) ** l10n, gam, CH)
    n0H_log10 = bisect_log10_n0(f_h, 5, 200)
    calib_rows.append((gs, CH, n0H_log10))
    print(f"gamma={gs:>5}: this-front C={float(CH):7.4f} (published {PRED_C[gs]:7.2f})  "
          f"this-front log10(n0)={float(n0H_log10):7.2f} (published {PRED_N0_LOG10[gs]:7.2f})  "
          f"diff={float(n0H_log10) - PRED_N0_LOG10[gs]:+.3f} decades")

max_diff = max(abs(float(n0H_log10) - PRED_N0_LOG10[gs]) for gs, _, n0H_log10 in calib_rows)
print(f"\nmax |diff| across all 8 points: {max_diff:.3f} decades -- calibration "
      f"{'PASSED (machinery independently reproduces the cited construction)' if max_diff < 0.05 else 'FAILED, investigate'}")
assert max_diff < 0.05

print()
print("=" * 100)
print(f"MAIN RESULT: OLD (Hoeffding) vs NEW (Bernstein, slack a={float(A_SLACK)}) n_0(gamma)")
print("=" * 100)
header = (f"{'gamma':>6} | {'C0_H':>7} {'C_H':>7} {'log10 n0_H (=OLD)':>18} | "
          f"{'C0_B':>7} {'C_B':>7} {'log10 n0_B (=NEW)':>18} | {'improvement':>12}")
print(header)
main_rows = []
for gs in GAMMAS:
    gam = mp.mpf(gs)
    C0H = C0_hoeffding(gam)
    CH = mp.mpf('1.2') * C0H
    f_h = lambda l10n, gam=gam, CH=CH: log_W_hoeffding(mp.mpf(10) ** l10n, gam, CH)
    n0H_log10 = bisect_log10_n0(f_h, 5, 200)

    C0B = C0_bernstein(gam, A_SLACK)
    CB = mp.mpf('1.2') * C0B
    f_b = lambda l10n, gam=gam, CB=CB: log_W_bernstein(mp.mpf(10) ** l10n, gam, CB, A_SLACK)
    n0B_log10 = bisect_log10_n0(f_b, 5, 200)

    improvement = n0H_log10 - n0B_log10
    main_rows.append((gs, C0H, CH, n0H_log10, C0B, CB, n0B_log10, improvement))
    print(f"{gs:>6} | {float(C0H):7.3f} {float(CH):7.3f} {float(n0H_log10):18.2f} | "
          f"{float(C0B):7.3f} {float(CB):7.3f} {float(n0B_log10):18.2f} | "
          f"{float(improvement):+12.2f}")

print()
print("=" * 100)
print("Side-condition sanity at each NEW crossover: small-k term included")
print("correctly (logsumexp), k2 << Kmax (large-k Bernstein regime genuinely")
print("covers essentially all of [1,K])")
print("=" * 100)
for gs, C0H, CH, n0H_log10, C0B, CB, n0B_log10, improvement in main_rows:
    gam = mp.mpf(gs)
    n_at = mp.mpf(10) ** n0B_log10
    total, k2c, Km, log_bt, log_smallk = log_W_bernstein(n_at, gam, CB, A_SLACK, return_extra=True)
    print(f"gamma={gs:>5}: k2={float(k2c):.4g}  Kmax={float(Km):.4g}  k2/Kmax={float(k2c / Km):.3e}  "
          f"log_bulk+tail={float(log_bt):.3f}  log_smallk={float(log_smallk):.3f}  total(should be ~0)={float(total):.4f}")

print()
print("=" * 100)
print("SUMMARY TABLE (decades of n_0(gamma), OLD vs NEW, side by side)")
print("=" * 100)
print(f"{'gamma':>6} | {'OLD log10 n0 (Hoeffding, predecessor)':>38} | {'NEW log10 n0 (Bernstein, this front)':>37} | {'decades saved':>13}")
for gs, C0H, CH, n0H_log10, C0B, CB, n0B_log10, improvement in main_rows:
    print(f"{gs:>6} | {PRED_N0_LOG10[gs]:38.2f} | {float(n0B_log10):37.2f} | {float(improvement):13.2f}")
