"""
Hostile referee, K6-EXACT-CLOSURE-ATTEMPT. Supplementary checks,
persisted for reproducibility (matching this archive's convention that
every claim checked during review lives in a script+log, not just
transient interactive commands):

  (A) Sanity-check sympy's Poly.shift(B) semantics on toy examples
      BEFORE trusting it on the real degree-1052/1056 polynomials --
      confirms it truly computes P(y+B) (Taylor shift) as a polynomial
      in the SAME generator, and that the Descartes-style "uniform sign
      after shift => no root exceeds B" certificate behaves exactly as
      expected on a polynomial with a KNOWN root location.

  (B) Confirm n0_boundary=7.2786... is genuinely the LARGER of the two
      candidate boundary crossings the target's own script considers
      (the h6(n,1)=-M6 branch AND the h6(n,1)=+M6 branch), i.e. that
      picking "the relevant one" was not an arbitrary/lucky choice --
      the other branch's own largest candidate (6.2609...) is smaller.

  (C) Confirm the magnitude claim in ATTEMPT.md Sec 7 issue #5 ("S(n)'s
      coefficients run to ~1800 decimal digits, per direct inspection in
      Sec 5.2's integer-evaluation step") refers to EVALUATED VALUES of
      S2(n) at large integers (confirmed: ~1800-1900 digits there), not
      literally the polynomial's own stored coefficients (which top out
      around 540-545 digits) -- a wording precision note, not a
      numerical error (the magnitude itself is accurate).
"""
import sympy as sp

print("=" * 78)
print("(A) Poly.shift(B) semantics sanity check (toy examples)")
print("=" * 78)
nn = sp.Symbol('n')
P = sp.Poly(nn ** 3 - 2 * nn + 5, nn)
shifted = P.shift(3)
expected = sp.expand(P.as_expr().subs(nn, nn + 3))
print(f"P(n)={P.as_expr()}  P.shift(3)={shifted.as_expr()}  "
      f"expected P(n+3)={expected}  match={sp.expand(shifted.as_expr()-expected)==0}")
assert sp.expand(shifted.as_expr() - expected) == 0

# Toy polynomial with KNOWN largest real root = 5: (n-5)(n-2) = n^2-7n+10
Ptoy = sp.Poly((nn - 5) * (nn - 2), nn)
print(f"\nPtoy = (n-5)(n-2) = {Ptoy.as_expr()}  (known largest real root: 5)")
for B in [2, 4, 5, 6]:
    sh = Ptoy.shift(B)
    coeffs = sh.all_coeffs()
    signs = set(sp.sign(c) for c in coeffs if c != 0)
    uniform = len(signs) <= 1
    print(f"  shift({B}): coeffs={coeffs}  signs={signs}  uniform={uniform}  "
          f"(expect uniform for B>=5, mixed for B<5)")
    if B < 5:
        assert not uniform
    else:
        assert uniform
print("CONFIRMED: shift-certificate correctly distinguishes B<root (mixed "
      "signs, inconclusive) from B>=root (uniform signs, proved no root "
      "exceeds B), exactly the behaviour the target's method relies on.")

print()
print("=" * 78)
print("(B) Boundary threshold: confirm 7.2786... is the genuine max across")
print("    BOTH candidate branches the target's own script considers")
print("=" * 78)
n, m, t = sp.symbols('n m t', real=True)
minpoly_M6 = (35429400000000000 * t ** 4 + 17921731935293824 * t ** 3
              - 248044660324924125 * t ** 2 + 350950285900800000 * t
              - 137134080000000000)
Gb = sp.expand(((n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)) * m - 720)

# "lower" branch: m := -h6(n,1); target m=M6 (i.e. h6(n,1)=-M6)
Sb_lower = sp.expand(sp.resultant(sp.Poly(Gb, m), sp.Poly(minpoly_M6.subs(t, m), m)))
roots_lower = [sp.N(r, 20) for r in sp.Poly(Sb_lower, n).real_roots()]
# "upper" branch: m := -h6(n,1); target -m=M6, i.e. m=-M6 (i.e. h6(n,1)=M6)
Sb_upper = sp.expand(sp.resultant(sp.Poly(Gb, m), sp.Poly(minpoly_M6.subs(t, -m), m)))
roots_upper = [sp.N(r, 20) for r in sp.Poly(Sb_upper, n).real_roots()]

print("roots on the h6(n,1)=-M6 branch (relevant one):", roots_lower)
print("roots on the h6(n,1)=+M6 branch (other one):    ", roots_upper)
cand = [r for r in (roots_lower + roots_upper) if r > 5]
n0_boundary = max(cand)
print(f"\nmax candidate > 5 across BOTH branches = {n0_boundary}")
assert abs(float(n0_boundary) - 7.278581437127420988290004) < 1e-15
biggest_other = max(r for r in roots_upper if r > 5)
print(f"largest candidate from the OTHER (h6=+M6) branch alone = {biggest_other}")
assert biggest_other < n0_boundary
print("CONFIRMED: the relevant branch (h6(n,1)=-M6) genuinely dominates -- "
      "picking it was not an arbitrary/lucky simplification; the other "
      "branch's own largest root (6.2609...) is strictly smaller.")

print()
print("=" * 78)
print("(C) Coefficient/evaluated-value magnitude check")
print("=" * 78)
k, x = sp.symbols('k x', real=True)
K = 6
Bracket6 = (
    -k**10 + 25*k**9 + 6*k**8*n**2 - 45*k**8*n - 270*k**8 - 96*k**7*n**2
    + 760*k**7*n + 1650*k**7 - 15*k**6*n**4 + 195*k**6*n**3 - 9*k**6*n**2
    - 5380*k**6*n - 6273*k**6 + 135*k**5*n**4 - 1875*k**5*n**3
    + 4359*k**5*n**2 + 20734*k**5*n + 15345*k**5 + 20*k**4*n**6
    - 330*k**4*n**5 + 1375*k**4*n**4 + 3600*k**4*n**3 - 22441*k**4*n**2
    - 47215*k**4*n - 24080*k**4 - 80*k**3*n**6 + 1440*k**3*n**5
    - 7975*k**3*n**4 + 4641*k**3*n**3 + 50821*k**3*n**2 + 64330*k**3*n
    + 23300*k**3 - 15*k**2*n**8 + 270*k**2*n**7 - 1730*k**2*n**6
    + 3435*k**2*n**5 + 7610*k**2*n**4 - 20391*k**2*n**3 - 58916*k**2*n**2
    - 50320*k**2*n - 12576*k**2 + 15*k*n**8 - 310*k*n**7 + 2360*k*n**6
    - 7055*k*n**5 + 730*k*n**4 + 20526*k*n**3 + 33716*k*n**2 + 20016*k*n
    + 2880*k + 6*n**10 - 105*n**9 + 720*n**8 - 2375*n**7 + 3384*n**6
    - 10*n**5 - 1860*n**4 - 6696*n**3 - 7440*n**2 - 2880*n
)
Dn6 = n ** 7 * (n - 1) * (n - 2) * (n - 3) * (n - 4) * (n - 5)
D6_formula = k * (k + 1) * Bracket6 / Dn6
F6n = sp.cancel(D6_formula.subs(k, n * x))
F6_cont = sp.expand(1 - (1 - x ** 2) ** K)
Delta6 = sp.cancel(F6n - F6_cont)
Num6 = sp.expand(sp.cancel(Delta6 * Dn6))
Npoly_n = sp.Poly(Num6, n)
g6 = sp.expand(Npoly_n.coeff_monomial(n ** Npoly_n.degree()))
g6p = sp.expand(sp.diff(g6, x))
x6star = [c for c in sp.Poly(g6p, x).real_roots() if 0 < sp.N(c) < 1][0]
M6 = sp.simplify(g6.subs(x, x6star))
minpoly_M6_derived = sp.minimal_polynomial(M6, t)
F1 = sp.expand(sp.diff(Num6, x))
F2 = sp.expand(m * Dn6 - n * Num6)
R = sp.expand(sp.resultant(F1, F2, x))
S2 = sp.expand(sp.resultant(sp.Poly(R, m), sp.Poly(minpoly_M6_derived.subs(t, -m), m)))
S2poly = sp.Poly(S2, n)

max_coeff_digits = max(len(str(abs(c))) for c in S2poly.all_coeffs())
print(f"Max digit count among S2(n)'s OWN stored coefficients: {max_coeff_digits}")
for nv in [30, 34, 35, 36]:
    v = S2poly.eval(nv)
    print(f"  S2({nv}) EVALUATED VALUE digit count: {len(str(abs(v)))}")
print("\nCONFIRMS: the '~1800 decimal digits' figure in ATTEMPT.md Sec 7 "
      "issue #5 refers to EVALUATED VALUES of S2(n) at specific large "
      "integers (Sec 5.2's sign-evaluation step), not to the polynomial's "
      "own raw stored coefficients (which top out ~540-545 digits). The "
      "magnitude claimed is accurate; the word 'coefficients' is a loose "
      "description of what is actually an evaluated value -- a wording "
      "precision note, not a numerical error.")
