"""
adv03_matching_and_equivalence.py -- REFEREE independent checks of

  (a) the front's Section 4 matched-asymptotics CLAIM 1 / CLAIM 2, via a
      by-hand bivariate Taylor expansion (NOT the front's own
      sqrtn-symbol-and-limit trick, see below) -- a genuinely different
      sympy code path, and

  (b) the front's Section 6 "logical equivalence" argument, both
      DIRECTIONS explicitly (the front's own script 05 Part C only
      writes out the forward substitution; here both directions are
      spelled out and checked), plus an independent from-scratch
      verification, from PRIMARY combinatorial definitions (not any
      cited closed form), that S_n'(gamma) = 1 + S_n(gamma) actually
      holds -- the one non-trivial CITED-not-rederived fact this
      front's Section 6 argument critically leans on.
"""
import sympy as sp
from sympy import symbols, simplify, Rational, exp, series, oo

print("="*78)
print("PART (a): Section 4 matching claims, independent bivariate approach")
print("="*78)

lam, g = symbols('lambda gamma', positive=True)
sqn = symbols('sqn', positive=True)  # sqn := sqrt(n), independent formal var

A_m_formula_of_m = lambda mm: mm*(mm+3)/(2*g) - mm*(mm+1)/g**2
A_over_n = simplify(A_m_formula_of_m(lam*sqn) / sqn**2)
A_over_n = sp.expand(A_over_n)
print(f"A_m(g)/n at m=lambda*sqrt(n): {A_over_n}")

# independent extraction: treat as a polynomial in 1/sqn (degree <=1 here)
# by substituting sqn = 1/u and doing an ordinary Laurent/Taylor split in u
u = symbols('u', positive=True)
expr_u = A_over_n.subs(sqn, 1/u)
expr_u = sp.expand(expr_u)
print(f"Same expr with sqn=1/u (u=1/sqrt(n)):  {expr_u}")
c_u0 = expr_u.coeff(u, 0)   # sqn-independent piece
c_u1 = expr_u.coeff(u, 1)   # coefficient of u=1/sqrt(n)
print(f"  u^0 term (O(1) in n): {c_u0}")
print(f"  u^1 term (O(1/sqrt(n))): {c_u1}")

T_prof = (1/g)*exp(-((2-g)/(2*g))*lam**2)
T_prof_taylor = series(T_prof, lam, 0, 4).removeO()
Tprof_lam2 = T_prof_taylor.coeff(lam, 2)
Tprof_const = T_prof_taylor.coeff(lam, 0)

claim1_inner = simplify(c_u0/lam**2)
claim1_diff = simplify(claim1_inner - Tprof_lam2)
print(f"\nCLAIM 1: inner lambda^2 coeff = {claim1_inner}, T_prof's own = {Tprof_lam2}")
print(f"  difference = {claim1_diff}")
assert claim1_diff == 0
print("  CONFIRMED (independent route).")

Delta_total_x_sqrtn = Rational(3,2)*lam - lam**3/6 - lam/g
Delta_lin = sp.series(Delta_total_x_sqrtn, lam, 0, 2).removeO().coeff(lam, 1)
predicted2 = simplify(Tprof_const * Delta_lin)
claim2_inner = simplify(c_u1/lam)
claim2_diff = simplify(claim2_inner - predicted2)
print(f"\nCLAIM 2: inner lambda^1 coeff = {claim2_inner}, T_prof(0)*Delta_lin = {predicted2}")
print(f"  difference = {claim2_diff}")
assert claim2_diff == 0
print("  CONFIRMED (independent route).")

print()
print("="*78)
print("PART (b): Section 6 logical-equivalence algebra, BOTH directions")
print("          spelled out explicitly (front's script only shows forward)")
print("="*78)

Snp, Gn, D, cross, C, sqrtgam = symbols("S_n_prime G_n D cross C sqrtgam")
Sn = symbols("S_n")

# Cited fact 1 (PROVED elsewhere, re-verified numerically in Part (c) below):
#   S_n'(g) = 1 + S_n(g)
# Cited fact 2 (predecessor, PROVED up to a term shown -> 0):
#   S_n'(g) - G_n(g) - 1/(2g) = cross   [in the n->infinity limit]
# Cited fact 3 (Lemma E, PROVED, BOTH directions):
#   S_n = G_n + D + o(1)  <=>  sqrt(n)(R_n - T(g)) -> C = (2/sqrt(pi))*sqrt(g)*D

# ---- forward direction: assume the LIMIT statement S_n = G_n + D  -------
# (i.e. the o(1) already taken to its limit) and show cross is FORCED
eq_from_Sn = sp.Eq(Snp, 1 + Gn + D)          # S_n'=1+S_n and S_n=G_n+D
forced_cross = sp.solve(sp.Eq(Snp - Gn - 1/(2*g), cross).subs(Snp, 1+Gn+D), cross)[0]
print(f"Forward: IF S_n=G_n+D (i.e. Lemma-E's hypothesis with this D) THEN cross -> {forced_cross}")
target = D + 1 - 1/(2*g)
assert simplify(forced_cross - target) == 0
print(f"  = D + 1 - 1/(2g) = the predecessor's cited conjectural target.  MATCHES.")

# ---- backward direction: assume cross -> D+1-1/(2g) and DERIVE S_n=G_n+D
eq2 = sp.Eq(Snp - Gn - Rational(1,1)/(2*g), target)
Snp_forced = sp.solve(eq2, Snp)[0]
print(f"\nBackward: IF cross -> D+1-1/(2g) THEN S_n' -> {sp.simplify(Snp_forced)}")
Sn_forced = simplify(Snp_forced - 1)
print(f"  => S_n = S_n'-1 -> {Sn_forced}  = G_n + D.  MATCHES Lemma-E's hypothesis exactly.")
assert simplify(Sn_forced - (Gn + D)) == 0

print()
print("Both directions check out as PURE algebra, given:")
print("  (1) S_n'=1+S_n  (cited identity -- independently re-verified from")
print("      PRIMARY combinatorial definitions in Part (c) below, not just")
print("      quoted),")
print("  (2) the predecessor's decomposition S_n'-G_n-1/(2g) = cross + o(1)")
print("      with the o(1) term independently shown -> 0 (predecessor,")
print("      Poisson-summation + exact-decomposition confirmation, cited),")
print("  (3) Lemma E itself (PROVED, both directions, Estagio 26 / re-")
print("      confirmed by an independent referee in gamma_second_order_")
print("      attempt/adversarial/REFEREE_REPORT.md).")
print("So the front's claimed 'crossover -> D(g)+1-1/(2g) IFF C(g)' is a")
print("VALID, non-overstated logical consequence -- REFEREE CONFIRMS.")

print()
print("="*78)
print("PART (c): independent re-verification, from PRIMARY definitions, of")
print("          S_n'(gamma) = 1 + S_n(gamma)")
print("="*78)
print("A_k(n,g) := sum_{mm=0}^{k} C(k,mm) g^mm (1-g)^(k-mm) * P_{k,mm},")
print("P_{k,mm} := prod_{i=1}^{mm} (1 - (k-i)/n)   [empty product = 1 for mm=0]")
print("S_n(g) := sum_{k=1}^{n} A_k(n,g)")
print()
print("term_m(n,g) := (g/n)^m * m! * T(n,m),")
print("T(n,m) := sum_{j=0}^{n-m} C(j+m,m)*C(n-j,m)*(1-g)^j")
print("S_n'(g) := sum_{m=0}^{n} term_m(n,g)")
print()

from sympy import Rational as R, binomial, factorial

def A_k(n_val, k_val, g_val):
    total = 0
    for mm in range(0, k_val+1):
        P = 1
        for i in range(1, mm+1):
            P *= (1 - R(k_val - i, n_val))
        total += binomial(k_val, mm) * g_val**mm * (1-g_val)**(k_val-mm) * P
    return sp.nsimplify(total) if False else sp.simplify(total)

def S_n(n_val, g_val):
    return sp.simplify(sum(A_k(n_val, k, g_val) for k in range(1, n_val+1)))

def T_nm(n_val, m_val, g_val):
    total = 0
    for j in range(0, n_val-m_val+1):
        total += binomial(j+m_val, m_val) * binomial(n_val-j, m_val) * (1-g_val)**j
    return sp.simplify(total)

def term_m(n_val, m_val, g_val):
    return sp.simplify((g_val/n_val)**m_val * factorial(m_val) * T_nm(n_val, m_val, g_val))

def Sprime_n(n_val, g_val):
    return sp.simplify(sum(term_m(n_val, m, g_val) for m in range(0, n_val+1)))

mismatches = 0
checks = 0
for n_val in [3, 4, 5, 6]:
    for g_val in [R(1,3), R(2,5), R(3,7)]:
        lhs = Sprime_n(n_val, g_val)
        rhs = 1 + S_n(n_val, g_val)
        checks += 1
        ok = simplify(lhs - rhs) == 0
        print(f"  n={n_val} g={g_val}: S_n'={lhs}  1+S_n={rhs}  match={ok}")
        if not ok:
            mismatches += 1
print(f"\n{checks-mismatches}/{checks} exact matches. mismatches={mismatches}")
assert mismatches == 0
print("CONFIRMED (independently, from PRIMARY definitions, exact rational")
print("arithmetic): S_n'(gamma) = 1 + S_n(gamma) holds at every point tested.")
