"""
Adversarial independent re-derivation of the phi_n formula (ATTEMPT.md
Section 3.1):

  phi_n = sum_{m=0}^{n-1} (d/dx - d/dy)^m [omega_{n-m}](x,y)

claimed to follow from combining:
  (a) the all-orders Watson-operator generalization  Phi ~ sum_{m>=0} eps^m (d/dx-d/dy)^m W
  (b) W = Psi - eps*Psi_x                                              (KEY, exact, required reading)
  (c) Psi = sum_{n>=1} eps^n psi_n(x,y),  Phi = sum_{n>=1} eps^n phi_n(x,y)
  (d) omega_k := psi_k - d(psi_{k-1})/dx,  psi_0 := 0

We re-derive this from scratch (own algebra, not copied from the target),
first by hand (see accompanying prose in the referee report), then verify
mechanically with sympy using TRUNCATED POWER SERIES in eps up to order 6,
with psi_k represented as abstract sympy Function objects of (x,y) (kept
fully general -- NOT assumed y-independent here, since this is a check of
the OPERATOR ALGEBRA / bookkeeping identity itself, which must hold
formally regardless of what psi_k turns out to be).
"""
import sympy as sp

x, y, eps = sp.symbols('x y eps')
N = 6  # truncation order to check

psi = {0: sp.Integer(0)}
for k in range(1, N+1):
    psi[k] = sp.Function(f'psi{k}')(x, y)

# Step 1: W = Psi - eps*Psi_x, truncated to O(eps^N)
Psi_series = sum(eps**k * psi[k] for k in range(1, N+1))
Psi_x_series = sp.diff(Psi_series, x)
W_series = sp.expand(Psi_series - eps*Psi_x_series)
W_poly = sp.Poly(W_series, eps)  # coefficients extracted per power of eps... but psi are functions, use series tools instead
W_coeffs = {}
for n in range(0, N+1):
    W_coeffs[n] = W_series.coeff(eps, n)
print("Step 1: W = Psi - eps*Psi_x, per-order coefficients w_n (eps^n):")
for n in range(1, N+1):
    expected_omega_n = psi.get(n, 0) - sp.diff(psi.get(n-1, sp.Integer(0)), x)
    match = sp.simplify(W_coeffs[n] - expected_omega_n) == 0
    print(f"  w_{n} = {W_coeffs[n]}   (expected omega_{n} = psi_{n} - d(psi_{n-1})/dx)   match={match}")
    assert match
print("PASS: W's eps^n coefficient is exactly omega_n = psi_n - psi_{n-1}' at every order,")
print("      independently confirming omega_0 = 0 (since psi_0 = psi_{-1} := 0).\n")

# Step 2: Phi ~ sum_{m=0}^{N} eps^m (d/dx-d/dy)^m W, truncate the OUTER sum over m
# and the INNER W to order N as well, then collect coefficient of eps^n in the
# double sum for n = 1..N.
def op_power(expr, m):
    total = 0
    for j in range(0, m+1):
        coeff = sp.binomial(m, j) * (-1)**j
        term = expr
        if m - j > 0:
            term = sp.diff(term, x, m-j)
        if j > 0:
            term = sp.diff(term, y, j)
        total += coeff*term
    return total

print("Step 2: Phi ~ sum_m eps^m (d/dx-d/dy)^m W, collect coefficient phi_n of eps^n")
print("        and compare against the CLAIMED formula phi_n = sum_{m=0}^{n-1} (d/dx-d/dy)^m[omega_{n-m}]\n")

# Self-test of the extraction mechanism itself (caught during development: .coeff()
# on an un-expanded Mul(const, Add(...)) silently returns a WRONG, eps-contaminated
# result -- this is a bug in the extraction method below, not in the target's math.
# Confirm the fix (expand before coeff) actually removes all residual eps-dependence.
_test_opW = sp.expand(op_power(W_series, 2))
_test_extract = _test_opW.coeff(eps, 1)
assert not _test_extract.has(eps), (
    "Self-test FAILED: extracted coefficient still contains eps -- "
    ".coeff() extraction is unreliable without expand(); do not trust results below."
)
print("Self-test: coeff() extraction (post sp.expand fix) is eps-free at m=2 probe -- OK.\n")

all_match = True
for n in range(1, N+1):
    # Direct route: Phi_series_full = sum_{m=0}^{n} eps^m * op_power(W_series, m), then take coeff eps^n.
    # Only need m=0..n (higher m contributes eps^{>n} at leading order from W's own eps^1 term).
    phi_n_direct = 0
    for m in range(0, n+1):
        # coefficient of eps^n in eps^m * op_power(W_series, m) is coefficient of eps^{n-m} in op_power(W_series,m)
        # NOTE: op_power's internal "coeff*term" accumulation is NOT auto-distributed by
        # sympy (Mul(const, Add(...)) stays unexpanded), so .coeff() must be called on an
        # EXPANDED expression or it silently misses/mis-buckets terms. Caught by self-test
        # below before trusting this extraction for the main comparison.
        opW = sp.expand(op_power(W_series, m))
        coeff_part = opW.coeff(eps, n-m) if (n-m) >= 0 else 0
        phi_n_direct += coeff_part
    phi_n_direct = sp.expand(phi_n_direct)

    # Claimed formula
    omega = {}
    for k in range(0, n+1):
        omega[k] = psi.get(k, sp.Integer(0)) - sp.diff(psi.get(k-1, sp.Integer(0)), x) if k >= 1 else sp.Integer(0)
    phi_n_claimed = 0
    for m in range(0, n):  # m = 0..n-1
        phi_n_claimed += op_power(omega[n-m], m)
    phi_n_claimed = sp.expand(phi_n_claimed)

    match = sp.simplify(phi_n_direct - phi_n_claimed) == 0
    all_match &= match
    print(f"n={n}: direct-from-operator-series phi_n vs claimed-formula phi_n   match={match}")
    if not match:
        print("   direct  :", phi_n_direct)
        print("   claimed :", phi_n_claimed)

assert all_match
print("\nPASS (n=1..6): the claimed formula")
print("  phi_n = sum_{m=0}^{n-1} (d/dx-d/dy)^m [omega_{n-m}]")
print("is EXACTLY the eps^n coefficient of Phi ~ sum_m eps^m (d/dx-d/dy)^m W combined with")
print("W = Psi - eps*Psi_x -- independently re-derived from the stated inputs, matching")
print("ATTEMPT.md Section 3.1's formula exactly, at every order tested.")
