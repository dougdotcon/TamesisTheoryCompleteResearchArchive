# Numeric support for the bulk/tail Hoeffding-splitting proof STRATEGY
# proposed in ATTEMPT.md Section 3 for (part of) Gap 1. This script does
# NOT touch the exact Binomial pmf (that is script 02's job, the ground
# truth); it evaluates the CRUDE, closed-form quantities that the analytic
# argument itself uses -- the worst-case-over-|D| bound
#   g(t) := |c0| + |c1|*t + |c2|*t^2 + |c3|*t^3   (t = |D|, 0<=t<=k)
# at t = Theta_k = C*sqrt(k ln n) (the proposed bulk/tail split point) and
# at t = k (the true boundary of the Binomial's support, used for the crude
# tail bound), together with the Hoeffding tail probability
#   P(|D| > Theta_k) <= 2 exp(-2 Theta_k^2 / k) = 2 n^{-2C^2}
# (valid whenever Theta_k <= k; Hoeffding's inequality for a sum of k iid
# [0,1]-bounded variables, elementary/classical, same citation tier as
# already used throughout this lineage -- not re-derived here).
#
# Purpose: confirm, with concrete numbers, the two claims ATTEMPT.md
# Section 3 makes:
#   (1) BULK: g(Theta_K) -> 0 as n -> oo (uniformly for k<=K), for ANY fixed
#       split constant C -- i.e. the bulk piece of R_bound(k) is genuinely
#       negligible, at every k<=K, not just "on average".
#   (2) TAIL: the crude worst-case quantity g(K) [at the full support
#       boundary t=K] grows like a FIXED (gamma-dependent) power of n
#       -- NOT exponentially in n -- so that for C large enough (a
#       gamma-dependent threshold, computed below), the union bound
#       K * g(K)^3 * e^{g(K)} * 2 n^{-2C^2} over k<=K still -> 0.
# This is evidence FOR the proof strategy's internal consistency, not a
# substitute for a fully assembled, explicit-constant proof (see
# ATTEMPT.md Section 4 for what remains to make this airtight).
#
# No .py file of any prior front was opened, read, or imported. Pure
# deterministic float64 arithmetic (values involved are all comfortably
# within float64 range/precision for this qualitative/rate-fitting check;
# the CLAIMED-evidence numeric quantities live in script 02, at dps=50).

import math


def coeffs_at_K(K, n, gamma):
    k = float(K); nn = float(n); g = float(gamma)
    c3 = 1.0 / (6 * nn ** 2)
    c2 = (2 * g * k - 2 * k - 2 * nn + 1) / (4 * nn ** 2)
    c1 = (g ** 2 * k ** 2 / 2 - g * k ** 2 - g * k * nn + g * k / 2 + k ** 2 / 2
          + k * nn - k / 2 - nn / 2 + 1.0 / 12) / nn ** 2
    m0 = g * k
    tau_m0 = (m0 ** 3 / 3 + m0 ** 2 * (0.5 - k) + m0 * (k ** 2 - k + 1.0 / 6)) / nn ** 2
    c0 = tau_m0 / 2
    return c0, c1, c2, c3


def g_of_t(t, c0, c1, c2, c3):
    return abs(c0) + abs(c1) * t + abs(c2) * t ** 2 + abs(c3) * t ** 3


def required_C(lam):
    """From the union-bound condition 1/2 + lam - 2C^2 < 0 (K ~ sqrt(n ln n)
    contributes the 1/2 power of n; lam is the empirical LINEAR-IN-ln(n)
    growth rate of g(K), i.e. e^{g(K)} ~ n^lam -- NOT g(K)'s own power-law
    exponent in n, which is the wrong quantity: g(K) itself grows only like
    ln(n), not like a power of n, as Part 1's own printed g(K) column already
    shows (roughly linear growth against ln(n), not against n). See Section 3
    self-correction note in ATTEMPT.md.), i.e. C > C_crit := sqrt(1/4+lam/2).
    A small margin over C_crit (checked: even a 10%-larger C) leaves the
    union bound decaying only EVENTUALLY, but numerically flat/growing out
    to n=1e8 -- polylog/power-of-n prefactors dominate near the critical
    threshold (checked directly, disclosed in ATTEMPT.md Section 3). A
    1.5x margin ON C ITSELF (not on C^2) gives clean, already-visible decay
    by n=1e3, confirmed below. Returns C = 1.5 * C_crit."""
    return 1.5 * math.sqrt(0.25 + lam / 2)


def fit_lambda(ns, gK_vals):
    """Least-squares slope of g(K) against ln(n) across ALL sampled points
    (more robust than a two-point fit)."""
    xs = [math.log(n) for n in ns]
    ys = gK_vals
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    den = sum((x - xbar) ** 2 for x in xs)
    return num / den


if __name__ == "__main__":
    print("=" * 92)
    print("Part 1: BULK piece -- g(Theta_K) at the split point, several C, vs n")
    print("(claim: -> 0 for every fixed C, as n grows; K = 1.5*sqrt(n ln n))")
    print("=" * 92)
    ns = [10 ** e for e in range(3, 9)]  # 1e3 .. 1e8, cheap (no pmf summation)
    gammas = [0.1, 0.3, 0.5, 0.7, 0.9, 0.99]
    Cs = [1, 2, 3, 5]

    for gamma in gammas:
        print(f"\n--- gamma = {gamma} ---")
        prev_gK = {}
        for n in ns:
            K = math.ceil(1.5 * math.sqrt(n * math.log(n)))
            c0, c1, c2, c3 = coeffs_at_K(K, n, gamma)
            bulk_line = []
            for C in Cs:
                theta = min(C * math.sqrt(K * math.log(n)), K)
                g_theta = g_of_t(theta, c0, c1, c2, c3)
                bulk_line.append(f"C={C}: g(Theta)={g_theta:.3e}")
            g_full = g_of_t(K, c0, c1, c2, c3)
            print(f"  n={n:>10d} K={K:>7d}  " + "  ".join(bulk_line) +
                  f"   ||  g(K) [full support]={g_full:.4f}")

    print()
    print("=" * 92)
    print("Part 2: TAIL piece -- CORRECTED exponent extraction.")
    print("g(K) itself grows only like ln(n) (Part 1's own printed g(K) column")
    print("already shows this: e.g. gamma=0.5, g(K) goes 16.9 -> 41.5 as n goes")
    print("1e3 -> 1e8, i.e. roughly LINEAR in ln(n), not in n). The quantity that")
    print("actually matters for the union bound is e^{g(K)} ~ n^lambda, where")
    print("lambda := d(g(K))/d(ln n), fitted here by least squares across ALL")
    print("sampled n (not a naive two-point power-law fit of g(K) itself against n,")
    print("which -- as an earlier version of this script mistakenly did --")
    print("silently underestimates the true exponent lambda by roughly the ratio")
    print("ln(ln n)/ln(n), giving a spuriously small 'mu' and an insufficient C.")
    print("Self-caught before any claim was made; corrected version below.")
    print("=" * 92)
    for gamma in gammas:
        print(f"\n--- gamma = {gamma} ---")
        gK_vals = []
        for n in ns:
            K = math.ceil(1.5 * math.sqrt(n * math.log(n)))
            c0, c1, c2, c3 = coeffs_at_K(K, n, gamma)
            gK_vals.append((n, K, g_of_t(K, c0, c1, c2, c3)))
        lam = fit_lambda(ns, [g for (_, _, g) in gK_vals])
        C_needed = required_C(lam)
        predicted_lam = (1.5 - gamma) * 2.25  # analytic leading-order prediction, see ATTEMPT.md Section 3
        print(f"  fitted lambda (e^{{g(K)}} ~ n^lambda, from g(K) vs ln(n) slope): "
              f"{lam:.4f}   [analytic leading-order prediction (1.5-gamma)*2.25 = {predicted_lam:.4f}]")
        print(f"  required split constant: C > C_crit = {math.sqrt(0.25+lam/2):.4f} "
              f"(using C_used = {C_needed:.4f} = 1.5*C_crit)")
        for (n, K, gK) in gK_vals:
            union_bound = K * (gK ** 3) * math.exp(min(gK, 700)) * 2 * n ** (-2 * C_needed ** 2)
            print(f"    n={n:>10d} K={K:>7d} g(K)={gK:.4f}  "
                  f"union-bound estimate = {union_bound:.3e}")

    print("\nDone.")
