"""
06_bernstein_plus_tight_bisection.py

Final assembly: THIS FRONT's tight, exact-cubic-max coefficient bound
(scripts 01-03, 05) COMBINED with the Bernstein-with-slack tail-control
technique (sharper_tail front's angle, re-derived fresh here) to build a
fully explicit, non-asymptotic W_tight(n,gamma,C,a) bounding the Bulk/Tail
Lemma's Gap-1 target Sum_k e^{-s(k)} R_k, then log-domain bisection for the
crossover n_0(gamma) at the SAME 8 sample gamma the continuation
(Hoeffding) and sharper_tail (Bernstein-only) fronts used.

W_tight(n,gamma,C,a) :=
   G_n_bound(n,gamma) * (1/6) * [ H_Theta^3 * exp(H_Theta)
                                    + 2*n^{-C^2/((2+a)*sigma^2)} * H_K^3*exp(H_K) ]
   + (1/6) * k_2(n,gamma,C,a) * exp(1/2) * H_K^3 * exp(H_K)

where:
  H_K       := exact_max_abs_x(K_real, n, gamma, D_min(K_real), D_max(K_real))
               [THIS FRONT: exact cubic max over the TRUE asymmetric
                support, no triangle-inequality slack -- scripts 01-03]
  H_Theta   := exact_max_abs_x(K_real, n, gamma, intersect([-Theta_K,Theta_K],
               [D_min(K_real),D_max(K_real)]))
  Theta_K   := C*sqrt(K_real*ln(n))
  K_real    := sqrt(4 n ln n/beta)+1  [THIS FRONT: tight truncation, script 05]
  G_n_bound := sqrt(pi*n/beta)        [CITED, Lemma D0 lineage, reused as-is]
  sigma^2   := gamma(1-gamma), M:=max(gamma,1-gamma)  [Bernstein ingredients]
  k_2       := (2*M*C/(3*a*sigma^2))^2 * ln(n)   [Bernstein slack construction,
                sharper_tail front, re-derived fresh, unaffected by this
                front's coefficient-bound change]
  C0_tight(gamma,a)^2 := (2+a)*sigma^2(gamma)*(lambda_tight(gamma)+1/2)
  C(gamma) := 1.2 * C0_tight(gamma,a)     [same 1.2x margin convention as
              every ancestor front, for apples-to-apples comparability]
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


def log_W_tight(n, g, a, margin=mp.mpf('1.2')):
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
    if Dlo_bulk < Dhi_bulk:
        H_Theta = exact_max_abs_x(Kr, n, g, Dlo_bulk, Dhi_bulk)
    else:
        H_Theta = mp.mpf(0)

    G_n_bound = mp.sqrt(mp.pi * n / b)

    k_2 = (2 * M * C / (3 * a * sigma2)) ** 2 * mp.log(n)
    # NOTE (self-caught bug, fixed): the small-k (k<k_2) residual must be
    # bounded using the cubic's value AT k~k_2 (k_2 = O(ln n), so its own
    # D-range/coefficients are tiny), NOT at k=K_real (K_real=O(sqrt(n ln n)),
    # whose H_K is astronomically larger and makes the "trivial" small-k
    # union bound swamp the entire construction -- caught by this front by
    # noticing logW was growing, not shrinking, with n; see ATTEMPT.md
    # Section 8 self-caught-issues disclosure).
    k2_ceil = mp.ceil(k_2)
    if k2_ceil < 1:
        k2_ceil = mp.mpf(1)
    Dlo_k2, Dhi_k2 = D_range(k2_ceil, g)
    H_k2 = exact_max_abs_x(k2_ceil, n, g, Dlo_k2, Dhi_k2)

    log_bulk_term = 3 * mp.log(H_Theta) + H_Theta if H_Theta > 0 else mp.mpf('-inf')
    log_tail_prob_term = mp.log(2) - (C ** 2 / ((2 + a) * sigma2)) * mp.log(n)
    log_smallk_term = mp.log(k_2) + mp.mpf('0.5') + 3 * mp.log(H_k2) + H_k2
    log_HK_term = 3 * mp.log(H_K) + H_K

    log_G_n = mp.log(G_n_bound)
    log_sixth = -mp.log(6)

    # W = G_n*(1/6)*bulk_term
    #   + G_n*(1/6)*tail_prob_term*HK_term      [k>=k_2 region, Bernstein]
    #   + (1/6)*smallk_term                     [k<k_2 region, deterministic,
    #                                             uses H_k2, NOT H_K -- fixed]
    def logsumexp2(x, y):
        hi = max(x, y)
        return hi + mp.log(mp.e ** (x - hi) + mp.e ** (y - hi))

    log_term_A = log_G_n + log_sixth + log_bulk_term
    log_term_B = log_G_n + log_sixth + log_tail_prob_term + log_HK_term
    log_term_C = log_sixth + log_smallk_term

    logW = logsumexp2(logsumexp2(log_term_A, log_term_B), log_term_C)
    return logW, dict(C=C, Kr=Kr, H_K=H_K, H_Theta=H_Theta, k_2=k_2,
                       H_k2=H_k2, G_n_bound=G_n_bound,
                       log_term_A=log_term_A, log_term_B=log_term_B,
                       log_term_C=log_term_C)


def find_n0(g, a, lo_exp, hi_exp, tol_bits=200):
    """Bisect (in log10(n) space) for the crossover where logW first
    becomes <= 0."""
    lo = mp.mpf(lo_exp)
    hi = mp.mpf(hi_exp)
    f_lo, _ = log_W_tight(mp.mpf(10) ** lo, g, a)
    f_hi, _ = log_W_tight(mp.mpf(10) ** hi, g, a)
    assert f_lo > 0 and f_hi < 0, f"bad bracket: f_lo={float(f_lo)}, f_hi={float(f_hi)} at gamma={g}"
    for _ in range(80):
        mid = (lo + hi) / 2
        fm, _ = log_W_tight(mp.mpf(10) ** mid, g, a)
        if fm > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < mp.mpf(10) ** -12:
            break
    return (lo + hi) / 2


# ---------------------------------------------------------------------
# Same 8 sample gamma as continuation/sharper_tail fronts, a=0.05
# ---------------------------------------------------------------------
a = mp.mpf('0.05')
gammas = [mp.mpf(x) for x in ['0.99', '0.9', '0.7', '0.5', '0.3', '0.1', '0.05', '0.01']]

# OLD published values (transcribed as plain numbers from the ancestor
# ATTEMPT.md prose, per this lineage's own calibration-check convention --
# NOT read from any ancestor .py/.log file).
OLD_HOEFFDING = {  # continuation front, Estagio 36
    '0.99': 20.79, '0.9': 36.83, '0.7': 45.02, '0.5': 50.28,
    '0.3': 55.95, '0.1': 65.95, '0.05': 71.78, '0.01': 84.88,
}
OLD_BERNSTEIN = {  # sharper_tail front, Estagio 37
    '0.99': 17.72, '0.9': 33.64, '0.7': 44.57, '0.5': 50.35,
    '0.3': 55.51, '0.1': 63.06, '0.05': 67.08, '0.01': 75.79,
}

def log_W_tight_margin(n, g, a, margin):
    return log_W_tight(n, g, a, margin=margin)


def find_n0_for_margin(g, a, margin, hi_max=95, step=3):
    """Linear scan (exponent grid, step-sized) for a sign change of
    log_W_tight, then bisect within the bracketing pair. Returns None if
    no sign change found in [2, hi_max]."""
    exps = list(range(2, hi_max + 1, step))
    prev_e, prev_f = None, None
    for e in exps:
        f, _ = log_W_tight_margin(mp.mpf(10) ** e, g, a, margin)
        if prev_f is not None and prev_f > 0 and f < 0:
            lo, hi = mp.mpf(prev_e), mp.mpf(e)
            for _ in range(70):
                mid = (lo + hi) / 2
                fm, _ = log_W_tight_margin(mp.mpf(10) ** mid, g, a, margin)
                if fm > 0:
                    lo = mid
                else:
                    hi = mid
                if hi - lo < mp.mpf(10) ** -10:
                    break
            return (lo + hi) / 2
        prev_e, prev_f = e, f
    return None  # not found


def optimize_margin(g, a, margin_grid):
    """Coarse-then-refine search over the split-constant margin
    (C := margin * C0_tight(gamma,a)) to minimize the resulting n_0(gamma).
    This is a legitimate optimization within the proof's free parameter
    (the Bulk/Tail Lemma holds for ANY C>C0_tight -- Section 3.2's proof,
    re-derived fresh in this front's own ATTEMPT.md, places no further
    constraint on C), not a new mathematical claim -- disclosed as a
    numerically-tuned choice, exactly as the ancestor fronts' own '1.2x'
    convention was."""
    best = None
    for m in margin_grid:
        n0 = find_n0_for_margin(g, a, m)
        if n0 is not None and (best is None or n0 < best[1]):
            best = (m, n0)
    return best


print("=" * 110)
print(f"{'gamma':>7} | {'best margin':>11} | {'C(gamma)':>10} | {'log10 n0 (TIGHT, this front)':>28} "
      f"| {'OLD Hoeffding':>14} | {'OLD Bernstein':>14} | {'decades vs Bern.':>16}")
print("=" * 110)

results = {}
margins_coarse = [mp.mpf(x) for x in
                   ['1.01', '1.05', '1.1', '1.2', '1.5', '2', '3', '5', '8', '12', '20', '35', '60', '100']]
for g in gammas:
    gs = str(g)
    best_m, best_n0 = optimize_margin(g, a, margins_coarse)
    # refine with a finer grid around best_m (multiplicative +/- 40%)
    fine_grid = [best_m * mp.mpf(f) for f in
                 ['0.6', '0.7', '0.8', '0.9', '0.95', '1.0', '1.05', '1.1', '1.2', '1.4', '1.7']]
    fine_grid = [m for m in fine_grid if m > 1]
    best_m2, best_n02 = optimize_margin(g, a, fine_grid)
    if best_n02 is not None and best_n02 < best_n0:
        best_m, best_n0 = best_m2, best_n02

    C0sq = C0_tight_sq(g, a)
    C = best_m * mp.sqrt(C0sq)
    results[gs] = best_n0
    old_h = OLD_HOEFFDING.get(gs)
    old_b = OLD_BERNSTEIN.get(gs)
    saved_vs_bern = old_b - float(best_n0)
    print(f"{gs:>7} | {float(best_m):>11.3f} | {float(C):>10.4f} | {float(best_n0):>28.4f} "
          f"| {old_h:>14.2f} | {old_b:>14.2f} | {saved_vs_bern:>16.2f}")

print()
print("=" * 78)
print("Diagnostics at the certified crossover (all 8 gamma, best margin)")
print("=" * 78)
best_margins = {}
for g in gammas:
    gs = str(g)
    if gs not in results:
        continue
    best_m, _ = optimize_margin(g, a, margins_coarse)
    fine_grid = [best_m * mp.mpf(f) for f in
                 ['0.6', '0.7', '0.8', '0.9', '0.95', '1.0', '1.05', '1.1', '1.2', '1.4', '1.7']]
    fine_grid = [m for m in fine_grid if m > 1]
    best_m2, best_n02 = optimize_margin(g, a, fine_grid)
    if best_n02 is not None:
        best_m = best_m2
    best_margins[gs] = best_m
    n0 = mp.mpf(10) ** results[gs]
    logW, diag = log_W_tight(n0, g, a, margin=best_m)
    print(f"gamma={gs}: n0=1e{float(results[gs]):.2f}  logW={float(logW):.4f}  "
          f"margin={float(best_m):.3f}  C={float(diag['C']):.4f}  K_real={float(diag['Kr']):.3e}  "
          f"H_K={float(diag['H_K']):.3e}  H_Theta={float(diag['H_Theta']):.3e}  "
          f"H_k2={float(diag['H_k2']):.3e}  k_2={float(diag['k_2']):.3e}  "
          f"k_2/K_real={float(diag['k_2']/diag['Kr']):.3e}\n"
          f"    logTermA(bulk)={float(diag['log_term_A']):.3f}  "
          f"logTermB(Bernstein tail)={float(diag['log_term_B']):.3f}  "
          f"logTermC(small-k)={float(diag['log_term_C']):.3f}")
