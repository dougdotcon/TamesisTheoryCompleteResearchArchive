"""
Adversarial independent verification of the general telescoping identity,
ATTEMPT.md Section 3.2:

  Claim: IF psi_1,...,psi_{n-1} are already y-independent (pure functions of x),
  THEN phi_n = psi_n(x,y) EXACTLY, i.e. f_n := psi_n - phi_n = 0 identically,
  where
    omega_k := psi_k - d(psi_{k-1})/dx     (psi_0 := 0)
    phi_n   := sum_{m=0}^{n-1} (d/dx - d/dy)^m [omega_{n-m}](x,y)

This script is built FRESH from the prose recursion given in ATTEMPT.md
Section 3.1/3.2 -- no .py file from the target front or any ancestor front
in the mclust_rigor lineage was opened, read, or imported. This is an
independent construction (own variable names, own loop structure) checking
the SAME purely algebraic identity, at n=4 and n=5 -- values NOT already
spot-checked by the orchestrating session (which did n=2,3 by hand/sympy).

Method: represent psi_1,...,psi_{n-1} as abstract sympy Function(x) objects
(genuinely y-independent -- sympy will correctly return 0 for any d/dy
applied to them), and psi_n as an abstract Function(x,y). Build omega_k for
k=1..n from these. Build phi_n via the binomial expansion of the operator
(d/dx-d/dy)^m applied to each omega_{n-m}. Compute f_n = psi_n - phi_n and
check it is IDENTICALLY (symbolically) zero.
"""
import sympy as sp

x, y = sp.symbols('x y')

def build_psis(n):
    """psi_0 = 0 (as a plain zero, not a Function); psi_1..psi_{n-1} are
    y-independent Function(x) objects; psi_n is a genuine Function(x,y)."""
    psis = {0: sp.Integer(0)}
    for k in range(1, n):
        psis[k] = sp.Function(f'psi{k}')(x)   # y-independent by construction
    psis[n] = sp.Function(f'psi{n}')(x, y)    # genuinely bivariate
    return psis

def build_omegas(psis, n):
    """omega_k := psi_k - d(psi_{k-1})/dx, for k = 1..n."""
    omegas = {}
    for k in range(1, n+1):
        omegas[k] = psis[k] - sp.diff(psis[k-1], x)
    return omegas

def apply_op_power(expr, m):
    """Apply (d/dx - d/dy)^m to expr via explicit binomial expansion:
    sum_{j=0}^m C(m,j) (-1)^j d^{m-j}/dx^{m-j} d^j/dy^j [expr]."""
    total = 0
    for j in range(0, m+1):
        coeff = sp.binomial(m, j) * (-1)**j
        term = expr
        if m - j > 0:
            term = sp.diff(term, x, m - j)
        if j > 0:
            term = sp.diff(term, y, j)
        total += coeff * term
    return sp.expand(total)

def build_phi_n(omegas, n):
    """phi_n := sum_{m=0}^{n-1} (d/dx-d/dy)^m [omega_{n-m}]."""
    total = 0
    for m in range(0, n):
        total += apply_op_power(omegas[n-m], m)
    return sp.expand(total)

print("="*70)
print("Independent construction and check of f_n = psi_n - phi_n = 0")
print("(fresh script, own variable/loop structure, from prose recursion only)")
print("="*70)

results = {}
for n in [2, 3, 4, 5, 6, 7]:
    psis = build_psis(n)
    omegas = build_omegas(psis, n)
    phi_n = build_phi_n(omegas, n)
    f_n = sp.expand(psis[n] - phi_n)
    f_n_simplified = sp.simplify(f_n)
    results[n] = f_n_simplified
    status = "PASS (f_n == 0)" if f_n_simplified == 0 else f"FAIL (f_n = {f_n_simplified})"
    print(f"n={n}: {status}")
    if f_n_simplified != 0:
        print("   RAW (unsimplified) f_n:", f_n)

print()
all_pass = all(v == 0 for v in results.values())
print("ALL n=2..7 PASS:" , all_pass)
assert all_pass, "Telescoping identity FAILED at some n -- independent check disagrees with ATTEMPT.md!"

print()
print("="*70)
print("Focused re-run at the two orders explicitly requested (n=4, n=5),")
print("printing the full intermediate build for audit.")
print("="*70)
for n in [4, 5]:
    print(f"\n--- n={n} ---")
    psis = build_psis(n)
    omegas = build_omegas(psis, n)
    print("omega_k for k=1..n:")
    for k in range(1, n+1):
        print(f"  omega_{k} = {omegas[k]}")
    phi_n = build_phi_n(omegas, n)
    print(f"phi_{n} (raw, expanded) = {phi_n}")
    f_n = sp.simplify(sp.expand(psis[n] - phi_n))
    print(f"f_{n} = psi_{n} - phi_{n} (simplified) = {f_n}")
    assert f_n == 0

print("\nALL FOCUSED n=4,5 CHECKS PASSED (independent script, matches by-hand re-derivation).")
