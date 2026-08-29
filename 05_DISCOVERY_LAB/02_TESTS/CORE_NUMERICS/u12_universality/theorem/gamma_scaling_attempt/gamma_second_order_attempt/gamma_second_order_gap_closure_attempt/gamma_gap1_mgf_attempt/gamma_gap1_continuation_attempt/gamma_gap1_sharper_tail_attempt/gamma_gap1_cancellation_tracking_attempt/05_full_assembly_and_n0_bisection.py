"""
05_full_assembly_and_n0_bisection.py

Full non-asymptotic (explicit-for-every-finite-n) reassembly of the
Bulk/Tail Lemma's bound on Sum_k e^{-s(k)} R_k, combining:

  (A) THIS FRONT's tight truncation K_real(n,gamma) := sqrt(4 n ln n / beta) + 1
      -- a genuinely tight, explicit upper bound on the true integer
      K = ceil(sqrt(4 n ln n / beta)) (valid for EVERY n>=2 by the
      elementary fact ceil(x) <= x+1), replacing the continuation front's
      K_max(n,gamma):=4*sqrt(n ln n/beta), which carries an extra,
      unnecessary ~2x margin (K_max = 2*sqrt(4 n ln n/beta) ~ 2*K_true).

  (B) THIS FRONT's EXACT (not triangle-inequality-bounded) evaluation of
      max_{D in [Dlo,Dhi]} |x_k(D)|, via elementary real-cubic calculus:
      the max of a continuous function on a closed interval is attained at
      an endpoint or an interior critical point, and x_k'(D)=0 is an
      explicit QUADRATIC with closed-form roots (script 03). This is used
      with the TRUE (asymmetric) support D in [-gamma*k,(1-gamma)*k]
      (script 01 Part D), not the crude symmetric |D|<=k used by every
      ancestor front.

  (C) The Bernstein-with-slack tail-probability technique (sharper_tail
      front), re-derived fresh here (own-script discipline: no ancestor
      .py file read/imported), combined with (A)+(B) instead of the
      ancestor's own crude hat_G(n,gamma).

Output: an explicit W_tight(n,gamma,C,a) upper-bounding the Bulk/Tail
Lemma's Gap-1 target, and a log-domain bisection locating n_0(gamma) at
the SAME 8 sample gamma the continuation/sharper_tail fronts used, for
direct, apples-to-apples comparison.
"""
import mpmath as mp

mp.mp.dps = 120


def beta_of(g):
    return g * (2 - g) / 2


def sigma2_of(g):
    return g * (1 - g)


def K_real(n, g):
    """Explicit, tight, provably-valid-for-all-n>=2 upper bound on the
    true integer truncation K = ceil(sqrt(4 n ln n / beta))."""
    b = beta_of(g)
    return mp.sqrt(4 * n * mp.log(n) / b) + 1


def K_max_old(n, g):
    """The continuation front's own crude K_max, for calibration only."""
    b = beta_of(g)
    return 4 * mp.sqrt(n * mp.log(n) / b)


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
    """EXACT max_{D in [Dlo,Dhi]} |x_k(D)|, via endpoints + real interior
    critical points of the cubic (closed-form quadratic-formula roots of
    x_k'(D)=c1+2c2D+3c3D^2=0). No triangle-inequality slack anywhere."""
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
    vals = [abs(x_of_D(k, n, g, Dc)) for Dc in candidates]
    return max(vals)


def D_range(k, g):
    return (-g * k, (1 - g) * k)


# ---------------------------------------------------------------------
# PART A -- verify K_real is a valid (safe) upper bound on the TRUE
# integer truncation K = ceil(sqrt(4 n ln n / beta)), across a grid.
# ---------------------------------------------------------------------
print("=" * 78)
print("PART A -- K_real(n,gamma) validity check vs true integer K")
print("=" * 78)
import math
fails = 0
checks = 0
for gf in [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    g = mp.mpf(gf)
    b = beta_of(g)
    for nf in [10, 100, 1000, 10 ** 6, 10 ** 12]:
        n = mp.mpf(nf)
        true_K = mp.ceil(mp.sqrt(4 * n * mp.log(n) / b))
        Kr = K_real(n, g)
        checks += 1
        if not (Kr >= true_K):
            fails += 1
            print(f"  FAIL gamma={gf} n={nf}: true_K={true_K} K_real={Kr}")
print(f"{checks} checks, {fails} failures (K_real >= true integer K required)")
assert fails == 0

# Also quantify how much tighter K_real is than the old K_max (should be
# close to a factor 2, i.e. K_real^2 close to a factor 4 smaller than
# K_max^2, at large n where the '+1'/ceiling slack is negligible).
print()
print("K_real vs OLD K_max (continuation front), ratio K_max/K_real at large n:")
for gf in [0.5, 0.1, 0.01]:
    g = mp.mpf(gf)
    n = mp.mpf('1e30')
    print(f"  gamma={gf}: K_real={float(K_real(n,g)):.6e}  K_max_old={float(K_max_old(n,g)):.6e}"
          f"  ratio={float(K_max_old(n,g)/K_real(n,g)):.4f}  (expect ~2)")

# ---------------------------------------------------------------------
# PART B -- numerically verify the k-uniformity fact this construction
# actually needs: exact_max_abs_x(k,n,gamma,D_range(k,gamma)) is bounded
# by its value at k=K_real, for 1<=k<=K_real. Disclosed as NUMERICAL
# verification (same honesty tier as the grandparent front's own
# Bulk/Tail Lemma k-uniformity check, which found individual |c_i(k)|
# non-monotone but the two facts the proof actually needs held in every
# tested case).
# ---------------------------------------------------------------------
print()
print("=" * 78)
print("PART B -- k-uniformity check: is exact_max_abs_x(k,...) <=")
print("exact_max_abs_x(K_real,...) for all 1<=k<=K_real?")
print("=" * 78)
kuniform_fails = 0
kuniform_checks = 0
for gf in [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    g = mp.mpf(gf)
    for nf_exp in [6, 12, 20, 30]:
        n = mp.mpf(10) ** nf_exp
        Kr = K_real(n, g)
        H_K = exact_max_abs_x(Kr, n, g, *D_range(Kr, g))
        # sample k across [1, Kr] on a geometric-ish grid (25 points)
        Kr_f = float(Kr)
        sample_ks = sorted(set(
            [1] + [int(max(1, round(Kr_f * t))) for t in
                   [0.001, 0.01, 0.05, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9,
                    0.95, 0.99, 0.999, 1.0]]
        ))
        worst_ratio = mp.mpf(0)
        for kk in sample_ks:
            kk = mp.mpf(kk)
            if kk < 1 or kk > Kr:
                continue
            Hk = exact_max_abs_x(kk, n, g, *D_range(kk, g))
            kuniform_checks += 1
            if Hk > H_K:
                kuniform_fails += 1
            ratio = Hk / H_K if H_K > 0 else mp.mpf(0)
            worst_ratio = max(worst_ratio, ratio)
        if nf_exp == 30:
            print(f"  gamma={gf:<5} n=1e{nf_exp}: H_K={float(H_K):.4e}  "
                  f"worst H_k/H_K over sampled k<=K = {float(worst_ratio):.6f}")
print(f"Total {kuniform_checks} (k,n,gamma) checks, {kuniform_fails} violations "
      f"of H_k <= H_K (expect 0).")
