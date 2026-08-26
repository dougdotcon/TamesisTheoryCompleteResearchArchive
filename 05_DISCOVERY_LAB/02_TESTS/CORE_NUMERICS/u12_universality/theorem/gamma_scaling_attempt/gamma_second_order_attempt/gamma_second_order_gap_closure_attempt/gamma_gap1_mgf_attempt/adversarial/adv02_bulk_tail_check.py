"""
Adversarial check of ATTEMPT.md Section 3.2, the Bulk/Tail Lemma:

  R_k := (1/6) E_M[ |x(D)|^3 e^{|x(D)|} ]  <=
         (1/6) [ g(Theta_K)^3 e^{g(Theta_K)}  +  2 n^{-2C^2} g(K)^3 e^{g(K)} ]

  for every 1<=k<=K, where Theta_k := C*sqrt(k*ln n), g(t) := |c0|+|c1|t+
  |c2|t^2+|c3|t^3, D := M - gamma*k, M ~ Bin(k, gamma).

This script does two independent things:
  (1) LOGIC AUDIT (symbolic / analytic, no code needed to "prove" -- but
      each of the four sub-steps of the proof is re-derived and checked
      here, not just re-read):
        (a) g is non-decreasing on t>=0 (non-negative coefficients);
        (b) t^3 e^t is non-decreasing on t>=0;
        (c) triangle inequality: |x(D)| <= g(|D|) pointwise;
        (d) Hoeffding's inequality applied correctly: for D a sum of k
            centered Bernoulli(gamma) terms each in an interval of length 1,
            P(|D|>t) <= 2 exp(-2 t^2 / k); evaluated at t=Theta_k=C sqrt(k ln n)
            gives P(|D|>Theta_k) <= 2 n^{-2C^2}, independent of k.
  (2) NUMERIC SPOT-CHECK, exact Binomial pmf (mpmath dps=50), confirming
      the *assembled* inequality
        E_M[g(|D|)^3 e^{g(|D|)}]  <=  g(Theta_K)^3 e^{g(Theta_K)}
                                       + 2 n^{-2C^2} g(K)^3 e^{g(K)}
      holds at several concrete (n, gamma, k, C, K) points -- this is the
      quantity the Bulk/Tail proof bounds BEFORE dividing by 6, checked
      directly against the true expectation via exact pmf summation, no
      shortcuts.

No .py file of any front in this lineage was read or imported. c0..c3
here use the referee's own INDEPENDENTLY-VERIFIED (adv01) derivative-based
formula, which is exact and was confirmed to match ATTEMPT.md's own
derivative-based form precisely.
"""
import mpmath as mp

mp.mp.dps = 50


def tau_val(m, k, n):
    return (m**3/3 + m**2*(mp.mpf('0.5') - k) + m*(k**2 - k + mp.mpf(1)/6)) / n**2


def tau_prime(m, k, n):
    return (m**2 + m*(1 - 2*k) + k**2 - k + mp.mpf(1)/6) / n**2


def tau_double_prime(m, k, n):
    return (2*m + 1 - 2*k) / n**2


def c_coeffs(k, n, gamma):
    """Referee's own independently-verified (adv01) derivative-based c0..c3."""
    gk = gamma * k
    c0 = tau_val(gk, k, n) / 2
    c1 = k*(1-gamma)/n - mp.mpf(1)/(2*n) + tau_prime(gk, k, n)/2
    c2 = -mp.mpf(1)/(2*n) + tau_double_prime(gk, k, n)/4
    c3 = mp.mpf(1)/(6*n**2)
    return c0, c1, c2, c3


def g_func(t, c0, c1, c2, c3):
    return abs(c0) + abs(c1)*t + abs(c2)*t**2 + abs(c3)*t**3


def x_of_D(D, k, n, gamma, c0, c1, c2, c3):
    return c0 + c1*D + c2*D**2 + c3*D**3


def binom_logpmf(k, m, gamma):
    # exact log-pmf via mpmath, dps=50
    return (mp.loggamma(k+1) - mp.loggamma(m+1) - mp.loggamma(k-m+1)
            + m*mp.log(gamma) + (k-m)*mp.log(1-gamma))


print("="*78)
print("PART (1): LOGIC AUDIT")
print("="*78)
print("""
(a) g(t) = |c0|+|c1|t+|c2|t^2+|c3|t^3 -- sum of a constant and three terms
    each of the form (nonneg coeff)*t^p, p=1,2,3 -- is manifestly
    non-decreasing on t>=0. TRUE by construction, no computation needed.

(b) h(t):=t^3 e^t has h'(t) = 3t^2 e^t + t^3 e^t = t^2 e^t (3+t) >= 0 for
    t>=0. TRUE, confirmed by elementary calculus (checked below numerically
    at a few points as a sanity spot-check, not a proof requirement).

(c) Triangle inequality: x(D) = c0+c1 D+c2 D^2+c3 D^3, so
    |x(D)| <= |c0|+|c1||D|+|c2|D^2+|c3||D|^3 = g(|D|).  TRUE, elementary,
    since D^2=|D|^2 and |D^3|=|D|^3 exactly (D real).

(d) Hoeffding: D = sum_{i=1}^k (X_i - gamma), X_i iid Bernoulli(gamma) in
    [0,1] (interval length 1). Hoeffding's inequality (classical, two-sided):
      P(|D| > t) <= 2 exp( -2 t^2 / sum_i (b_i-a_i)^2 ) = 2 exp(-2 t^2 / k).
    At t = Theta_k = C*sqrt(k ln n):
      2 Theta_k^2 / k = 2 C^2 k ln(n) / k = 2 C^2 ln(n)
      => P(|D| > Theta_k) <= 2 exp(-2 C^2 ln n) = 2 n^{-2C^2}.
    This bound is INDEPENDENT of k (the k's cancel exactly) -- confirmed
    algebraically above, matches ATTEMPT.md's claim exactly.
""")

# spot check (b) numerically
for t in [0.001, 0.5, 1.0, 5.0, 20.0]:
    tt = mp.mpf(t)
    h = tt**3 * mp.e**tt
    # numerical derivative via finite difference as a sanity check of monotonicity
    eps = mp.mpf('1e-6')
    h2 = (tt+eps)**3 * mp.e**(tt+eps)
    print(f"  t={t:>8}: h(t)={float(h):.6g}, h(t+eps)-h(t)={float(h2-h):.6g} (should be >=0)")

print("\nAlgebraic identity check: 2*Theta_k^2/k with Theta_k=C*sqrt(k*ln(n)):")
for (C, k, n) in [(1.5, 10, 1000), (2.0, 500, 50000), (1.0, 3, 10)]:
    Ck = mp.mpf(C)
    kk = mp.mpf(k)
    nn = mp.mpf(n)
    Theta_k = Ck * mp.sqrt(kk * mp.log(nn))
    lhs = 2*Theta_k**2/kk
    rhs = 2*Ck**2*mp.log(nn)
    print(f"  C={C}, k={k}, n={n}: 2*Theta_k^2/k = {float(lhs):.10f}, "
          f"2*C^2*ln(n) = {float(rhs):.10f}, match={abs(lhs-rhs) < mp.mpf('1e-40')}")

print("\n" + "="*78)
print("PART (2): NUMERIC SPOT-CHECK of the ASSEMBLED inequality, exact pmf")
print("="*78)
print("""
For several concrete (n, gamma, k, C, K) points, this script computes, via
DIRECT summation over the true Binomial(k,gamma) pmf (mpmath dps=50, no
shortcuts, no Hoeffding bound used in this computation -- only used to
compute the actual expectation being bounded):

    LHS := E_M[ g(|D|)^3 * e^{g(|D|)} ]   (the exact quantity, D=M-gamma*k)

and compares it against the Bulk/Tail Lemma's claimed bound:

    RHS := g(Theta_K)^3 * e^{g(Theta_K)}  +  2 n^{-2C^2} * g(K)^3 * e^{g(K)}

checking LHS <= RHS at every point (the inequality the Lemma claims holds
for EVERY k<=K, uniformly).
""")

print("""
IMPORTANT SUBTLETY, checked explicitly here (this is the crux of whether
the Lemma's final assembled inequality is actually uniform in k, as
claimed): c0,c1,c2,c3 depend on k (they involve tau(gamma*k), tau'(gamma*k),
tau''(gamma*k)). Section 3.3's own usage of "g(Theta_K)" and "g(K)"
substitutes k=K into the c_i(k) formulas throughout (e.g. "|c1|Theta_K"
is evaluated with c1=c1(K)). So the Lemma's final bound, read consistently
with how the front itself uses it in Section 3.3, is a SINGLE, k-independent
pair of numbers g_K(Theta_K), g_K(K) (using K's own coefficients), meant to
bound R_k for EVERY k<=K -- not a per-k varying quantity.

For that to be valid, the proof implicitly needs an UNSTATED extra fact:
|c_i(k)| is non-decreasing in k (so that g_k(t) <= g_K(t) pointwise for
k<=K, which combined with Theta_k<=Theta_K gives g_k(Theta_k)<=g_K(Theta_K)
and g_k(K)<=g_K(K)). This monotonicity-in-k of the coefficients is NEVER
stated or proved anywhere in Section 3.2 -- the proof text only argues
monotonicity of g(.) IN ITS ARGUMENT t (for one fixed k), which is a
different (weaker) fact. This is checked numerically below.
""")

print("Monotonicity-in-k check: is |c_i(k)| non-decreasing for k=1..K?")
mono_fail_examples = []
for (n, gamma, K) in [(500, 0.5, 30), (2000, 0.1, 60), (2000, 0.9, 60),
                       (8000, 0.99, 120), (32000, 0.1, 240)]:
    nn, gg, KK = mp.mpf(n), mp.mpf(gamma), K
    prev = None
    for k in range(1, K+1):
        c0k, c1k, c2k, c3k = c_coeffs(k, nn, gg)
        mags = (abs(c0k), abs(c1k), abs(c2k), abs(c3k))
        if prev is not None:
            for idx, (p, cur) in enumerate(zip(prev, mags)):
                if cur < p - mp.mpf('1e-30'):
                    mono_fail_examples.append((n, gamma, k, idx, float(p), float(cur)))
        prev = mags
    n_fail = sum(1 for e in mono_fail_examples if e[0] == n and e[1] == float(gamma))
    print(f"  n={n:6d} gamma={gamma:5.2f} K={K:4d}: "
          f"monotonicity violations found so far (cumulative)={len(mono_fail_examples)}")

if mono_fail_examples:
    print(f"\n  {len(mono_fail_examples)} monotonicity-in-k violation(s) found. "
          f"First 5 examples (n, gamma, k, coeff-index[0=c0,1=c1,2=c2,3=c3], "
          f"|c_i(k-1)|, |c_i(k)|):")
    for e in mono_fail_examples[:5]:
        print("   ", e)
else:
    print("\n  NO monotonicity-in-k violations found across all tested "
          "(n, gamma, k<=K) ranges: |c_i(k)| is empirically non-decreasing "
          "in k throughout. The implicit fact the Lemma's assembled "
          "inequality relies on (but never states or proves) appears TRUE "
          "in the tested range, but is a genuine unstated logical step.")

print("\n" + "="*78)
print("Numeric spot-check of the FULL assembled inequality, using K's OWN")
print("coefficients for the RHS (matching Section 3.3's actual usage),")
print("and each row's own k for the LHS (the true R_k target)")
print("="*78)

test_points = [
    # (n, gamma, k, K, C)
    (500, 0.5, 5, 30, 1.5),
    (500, 0.5, 25, 30, 1.5),
    (500, 0.5, 30, 30, 1.5),   # k=K itself, the case the proof text directly covers
    (2000, 0.3, 10, 60, 2.0),
    (2000, 0.9, 50, 60, 1.5),
    (8000, 0.1, 100, 120, 1.5),
    (8000, 0.99, 3, 120, 1.5),
]

all_ok = True
for (n, gamma, k, K, C) in test_points:
    nn, gg, kk, KK, CC = mp.mpf(n), mp.mpf(gamma), k, K, mp.mpf(C)
    c0k, c1k, c2k, c3k = c_coeffs(kk, nn, gg)      # this k's own coefficients (for LHS/R_k)
    c0K, c1K, c2K, c3K = c_coeffs(KK, nn, gg)      # K's own coefficients (for RHS, per Sec 3.3 usage)

    # Exact expectation via direct pmf summation over m=0..k (the true R_k target, x6)
    LHS = mp.mpf(0)
    logpmf_vals = [binom_logpmf(kk, m, gg) for m in range(0, k+1)]
    for m in range(0, k+1):
        D = m - gg*kk
        gt = g_func(abs(D), c0k, c1k, c2k, c3k)
        term = mp.e**(logpmf_vals[m]) * gt**3 * mp.e**gt
        LHS += term

    Theta_K = CC * mp.sqrt(KK * mp.log(nn))
    g_ThetaK = g_func(Theta_K, c0K, c1K, c2K, c3K)
    g_K = g_func(KK, c0K, c1K, c2K, c3K)
    bulk = g_ThetaK**3 * mp.e**g_ThetaK
    tail = 2 * nn**(-2*CC**2) * g_K**3 * mp.e**g_K
    RHS = bulk + tail

    ok = LHS <= RHS
    all_ok = all_ok and ok
    print(f"  n={n:6d} gamma={gamma:5.2f} k={k:4d} K={K:4d} C={C}: "
          f"LHS={float(LHS):.6e}  RHS={float(RHS):.6e}  "
          f"(bulk={float(bulk):.4e}, tail={float(tail):.4e})  "
          f"LHS<=RHS: {ok}")

print(f"\nAll {len(test_points)} spot-check points satisfy LHS<=RHS "
      f"(using K's own coefficients for the RHS, as Section 3.3 does): {all_ok}")
