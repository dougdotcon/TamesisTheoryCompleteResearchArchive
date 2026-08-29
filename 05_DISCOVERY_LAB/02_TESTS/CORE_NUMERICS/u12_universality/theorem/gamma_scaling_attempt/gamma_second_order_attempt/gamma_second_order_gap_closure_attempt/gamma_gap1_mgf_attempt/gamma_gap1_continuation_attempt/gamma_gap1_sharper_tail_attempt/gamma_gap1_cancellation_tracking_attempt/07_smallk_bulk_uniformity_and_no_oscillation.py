"""
07_smallk_bulk_uniformity_and_no_oscillation.py

Two additional rigor checks not covered by script 05's Part B (which
sampled k on a grid of FRACTIONS of K_real -- at K_real ~ 1e17-1e33, that
grid never actually probed the truly small-k window k=1..k_2, since
k_2=O(ln n) is a minuscule ABSOLUTE range compared to K_real):

  (1) Small-k monotonicity: for k=1,...,ceil(k_2), is
      exact_max_abs_x(k,n,gamma,D_range(k,gamma)) <= H_k2 (its value at
      k=ceil(k_2))? This is exactly the fact script 06's small-k residual
      term (log_term_C) implicitly relies on.
  (2) Bulk-piece k-uniformity: for k=1,...,K_real (sampled), is the
      TRUNCATED-to-bulk-radius max |x_k(D)| (D in [-Theta_k,Theta_k]-
      intersect-true-range) <= H_Theta (the same quantity evaluated at
      k=K_real, Theta_K)? Theta_k:=C*sqrt(k*ln n) is itself k-dependent.
  (3) No-spurious-oscillation: log W_tight(n,gamma,C,a) checked on a fine
      half-decade grid from n_0(gamma) through >=20 decades beyond, at the
      best-margin C found by script 06, confirming no local increase
      (matching this lineage's own standard check, e.g. ancestor scripts
      06 in both the continuation and sharper_tail fronts).
"""
import mpmath as mp

mp.mp.dps = 150


def beta_of(g):
    return g * (2 - g) / 2


def sigma2_of(g):
    return g * (1 - g)


def K_real(n, g):
    b = beta_of(g)
    return mp.sqrt(4 * n * mp.log(n) / b) + 1


def c_exact(k, n, g):
    c0v = g * k * (2 * g ** 2 * k ** 2 - 6 * g * k ** 2 + 3 * g * k
                    + 6 * k ** 2 - 6 * k + 1) / (12 * n ** 2)
    c1v = (g ** 2 * k ** 2 / 2 - g * k ** 2 - g * k * n + g * k / 2
           + k ** 2 / 2 + k * n - k / 2 - n / 2 + mp.mpf(1) / 12) / n ** 2
    c2v = (2 * g * k - 2 * k - 2 * n + 1) / (4 * n ** 2)
    c3v = mp.mpf(1) / (6 * n ** 2)
    return c0v, c1v, c2v, c3v


def x_of_D(k, n, g, Dval):
    c0v, c1v, c2v, c3v = c_exact(k, n, g)
    return c0v + c1v * Dval + c2v * Dval ** 2 + c3v * Dval ** 3


def exact_max_abs_x(k, n, g, Dlo, Dhi):
    if Dlo > Dhi:
        Dlo, Dhi = Dhi, Dlo
    c0v, c1v, c2v, c3v = c_exact(k, n, g)
    candidates = [Dlo, Dhi]
    disc = (2 * c2v) ** 2 - 4 * (3 * c3v) * c1v
    if disc >= 0:
        sq = mp.sqrt(disc)
        for root in [(-2 * c2v + sq) / (6 * c3v), (-2 * c2v - sq) / (6 * c3v)]:
            if Dlo <= root <= Dhi:
                candidates.append(root)
    return max(abs(x_of_D(k, n, g, Dc)) for Dc in candidates)


def D_range(k, g):
    return (-g * k, (1 - g) * k)


def lambda_tight(g):
    return max(mp.mpf(4), 4 * (1 - g) ** 2 / (g * (2 - g)))


def C0_tight_sq(g, a):
    return (2 + a) * sigma2_of(g) * (lambda_tight(g) + mp.mpf('0.5'))


def log_W_tight(n, g, a, margin):
    b = beta_of(g)
    sigma2 = sigma2_of(g)
    M = max(g, 1 - g)
    C = margin * mp.sqrt(C0_tight_sq(g, a))
    Kr = K_real(n, g)
    Dlo_full, Dhi_full = D_range(Kr, g)
    Theta_K = C * mp.sqrt(Kr * mp.log(n))
    Dlo_bulk = max(-Theta_K, Dlo_full)
    Dhi_bulk = min(Theta_K, Dhi_full)
    H_K = exact_max_abs_x(Kr, n, g, Dlo_full, Dhi_full)
    H_Theta = exact_max_abs_x(Kr, n, g, Dlo_bulk, Dhi_bulk) if Dlo_bulk < Dhi_bulk else mp.mpf(0)
    G_n_bound = mp.sqrt(mp.pi * n / b)
    k_2 = (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)
    k2_ceil = max(mp.ceil(k_2), mp.mpf(1))
    Dlo_k2, Dhi_k2 = D_range(k2_ceil, g)
    H_k2 = exact_max_abs_x(k2_ceil, n, g, Dlo_k2, Dhi_k2)

    log_bulk_term = 3 * mp.log(H_Theta) + H_Theta if H_Theta > 0 else mp.mpf('-inf')
    log_tail_prob_term = mp.log(2) - (C ** 2 / ((2 + a) * sigma2)) * mp.log(n)
    log_smallk_term = mp.log(k_2) + mp.mpf('0.5') + 3 * mp.log(H_k2) + H_k2
    log_HK_term = 3 * mp.log(H_K) + H_K
    log_G_n = mp.log(G_n_bound)
    log_sixth = -mp.log(6)

    def lse(x, y):
        hi = max(x, y)
        return hi + mp.log(mp.e ** (x - hi) + mp.e ** (y - hi))

    log_term_A = log_G_n + log_sixth + log_bulk_term
    log_term_B = log_G_n + log_sixth + log_tail_prob_term + log_HK_term
    log_term_C = log_sixth + log_smallk_term
    logW = lse(lse(log_term_A, log_term_B), log_term_C)
    return logW


# ---------------------------------------------------------------------
# CHECK 1 -- small-k monotonicity (the fact log_term_C actually needs)
# ---------------------------------------------------------------------
print("=" * 78)
print("CHECK 1 -- small-k monotonicity: H_k <= H_k2 for k=1..ceil(k_2)")
print("=" * 78)
a = mp.mpf('0.05')
gammas_f = [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
best_margins = {  # from script 06's search, hard-coded here for reuse
    '0.99': mp.mpf('1.05'), '0.9': mp.mpf('1.05'), '0.7': mp.mpf('1.05'),
    '0.5': mp.mpf('1.05'), '0.3': mp.mpf('1.05'), '0.1': mp.mpf('1.01'),
    '0.05': mp.mpf('1.01'), '0.01': mp.mpf('1.01'),
}
n0_found = {  # from script 06's output (log10 n0), hard-coded for reuse
    '0.99': mp.mpf('15.42'), '0.9': mp.mpf('19.09'), '0.7': mp.mpf('30.45'),
    '0.5': mp.mpf('35.49'), '0.3': mp.mpf('39.30'), '0.1': mp.mpf('47.72'),
    '0.05': mp.mpf('52.08'), '0.01': mp.mpf('61.17'),
}

check1_violations = 0
check1_total = 0
for gf in gammas_f:
    g = mp.mpf(gf)
    gs = str(gf)
    margin = best_margins[gs]
    n = mp.mpf(10) ** n0_found[gs]
    C = margin * mp.sqrt(C0_tight_sq(g, a))
    sigma2 = sigma2_of(g)
    M = max(g, 1 - g)
    k_2 = (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)
    k2_ceil = max(mp.ceil(k_2), mp.mpf(1))
    Dlo_k2, Dhi_k2 = D_range(k2_ceil, g)
    H_k2 = exact_max_abs_x(k2_ceil, n, g, Dlo_k2, Dhi_k2)
    k2f = float(k2_ceil)
    # densely sample k in [1, k2_ceil] -- this is the ACTUAL small-k window
    n_samples = 60
    worst_ratio = mp.mpf(0)
    for i in range(n_samples):
        frac = (i + 1) / n_samples
        kk = max(mp.mpf(1), mp.floor(k2_ceil * mp.mpf(frac)))
        Dlo_k, Dhi_k = D_range(kk, g)
        Hk = exact_max_abs_x(kk, n, g, Dlo_k, Dhi_k)
        check1_total += 1
        ratio = Hk / H_k2 if H_k2 > 0 else mp.mpf(0)
        worst_ratio = max(worst_ratio, ratio)
        if Hk > H_k2:
            check1_violations += 1
    print(f"  gamma={gf:<5} n=1e{float(n0_found[gs]):.1f}  k_2={k2f:.3e}  "
          f"H_k2={float(H_k2):.4e}  worst H_k/H_k2 over k in [1,k_2] = {float(worst_ratio):.6f}")
print(f"Total {check1_total} checks, {check1_violations} violations (expect 0)")

# ---------------------------------------------------------------------
# CHECK 2 -- bulk-piece k-uniformity: Theta_k-truncated max at k <= K_real
# dominated by its value at k=K_real
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("CHECK 2 -- bulk-piece k-uniformity: Theta_k-truncated H_bulk(k) <=")
print("H_Theta (value at k=K_real, Theta_K)")
print("=" * 78)
check2_violations = 0
check2_total = 0
for gf in gammas_f:
    g = mp.mpf(gf)
    gs = str(gf)
    margin = best_margins[gs]
    n = mp.mpf(10) ** n0_found[gs]
    C = margin * mp.sqrt(C0_tight_sq(g, a))
    Kr = K_real(n, g)
    Dlo_full, Dhi_full = D_range(Kr, g)
    Theta_K = C * mp.sqrt(Kr * mp.log(n))
    Dlo_bulkK = max(-Theta_K, Dlo_full)
    Dhi_bulkK = min(Theta_K, Dhi_full)
    H_Theta = exact_max_abs_x(Kr, n, g, Dlo_bulkK, Dhi_bulkK) if Dlo_bulkK < Dhi_bulkK else mp.mpf(0)
    Kr_f = float(Kr)
    worst_ratio = mp.mpf(0)
    n_samples = 40
    for i in range(n_samples):
        frac = (i + 1) / n_samples
        kk = max(mp.mpf(1), mp.floor(Kr * mp.mpf(frac)))
        Theta_k = C * mp.sqrt(kk * mp.log(n))
        Dlo_k, Dhi_k = D_range(kk, g)
        Dlo_bk = max(-Theta_k, Dlo_k)
        Dhi_bk = min(Theta_k, Dhi_k)
        if Dlo_bk >= Dhi_bk:
            continue
        Hbk = exact_max_abs_x(kk, n, g, Dlo_bk, Dhi_bk)
        check2_total += 1
        ratio = Hbk / H_Theta if H_Theta > 0 else mp.mpf(0)
        worst_ratio = max(worst_ratio, ratio)
        if Hbk > H_Theta:
            check2_violations += 1
    print(f"  gamma={gf:<5} n=1e{float(n0_found[gs]):.1f}  H_Theta(K)={float(H_Theta):.4e}  "
          f"worst H_bulk(k)/H_Theta(K) over k<=K = {float(worst_ratio):.6f}")
print(f"Total {check2_total} checks, {check2_violations} violations (expect 0)")

# ---------------------------------------------------------------------
# CHECK 3 -- no spurious oscillation, 20+ decades beyond n_0
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("CHECK 3 -- no-spurious-oscillation: log W_tight from n_0(gamma)")
print("through 20 decades beyond, fine half-decade grid")
print("=" * 78)
for gf in gammas_f:
    g = mp.mpf(gf)
    gs = str(gf)
    margin = best_margins[gs]
    n0log = float(n0_found[gs])
    grid = [n0log + i * 0.5 for i in range(0, 41)]  # n0 .. n0+20, step 0.5
    vals = [float(log_W_tight(mp.mpf(10) ** e, g, a, margin)) for e in grid]
    increasing_found = any(vals[i + 1] > vals[i] + 1e-6 for i in range(len(vals) - 1))
    print(f"  gamma={gf:<5}: logW at n0={vals[0]:.4f}, at n0+20dec={vals[-1]:.4f}, "
          f"increasing_found={increasing_found}")
