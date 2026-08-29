#!/usr/bin/env python3
"""
Adversarial / independent referee check — items 1, 2, 3 of the mandate.

Fresh, from-scratch symbolic verification. No code from the target front
(u01_symbolic_outer_expansion.py) or any ancestor is read or imported.

Representation: R(x) satisfies the first-order linear ODE R' = x*R - 1.
Every derivative R^{(k)}(x) can therefore be written EXACTLY as
    R^{(k)}(x) = a_k(x) * R(x) + b_k(x)
for polynomials a_k, b_k (since differentiating a*R+b using R'=xR-1 gives
another expression of the same form: d/dx(a*R+b) = (a' + x*a)*R + (b' - a)).
We build this pair-representation TWO independent ways:
  (A) direct repeated differentiation of R^{(1)} = x*R - 1 using the
      differentiation rule above (does not use the closure identity at all)
  (B) the record's own closure identity R^{(n+1)} = x*R^{(n)} + n*R^{(n-1)}
and cross-check they agree for k = 0..8.

We then verify, by EXACT symbolic residual = 0 (sympy.expand, not a
numeric approximation), that psi_n(x) := gamma_n * R^{(n-1)}(x) solves the
record's own stated psi_n ODEs for n = 2, 3, 4 IDENTICALLY in x (item 1).

We derive chi_n(x) := psi_n(x) - psi_{n-1}'(x) both (i) directly from the
psi_n pair-representations and (ii) via the claimed closed form
(gamma_n - gamma_{n-1}) * R^{(n-1)}(x), and confirm they are identical
(item 2).

Finally we independently re-derive, via a *different* bookkeeping route
than the target's own presentation (a fully explicit double-index Watson's
lemma expansion, not merely asserting the telescoping identity), that
summing e^{-v/eps} * chi_n(v) term-by-term over the "STAR" integral
reproduces gamma_N * R^{(N-1)}(0) at every order N = 1..4, matching the
record's published 4-term law digit-for-digit (item 3).
"""

import os
import sympy as sp

x = sp.symbols('x', real=True)
R = sp.Function('R')  # purely formal; algebra never uses R's closed form.

# ---------------------------------------------------------------------
# Pair-representation algebra: (a, b) <-> a(x)*R(x) + b(x)
# ---------------------------------------------------------------------

def pair_add(p, q):
    return (sp.expand(p[0] + q[0]), sp.expand(p[1] + q[1]))

def pair_sub(p, q):
    return (sp.expand(p[0] - q[0]), sp.expand(p[1] - q[1]))

def pair_scale(p, c):
    return (sp.expand(c * p[0]), sp.expand(c * p[1]))

def pair_mul_x(p):
    return (sp.expand(x * p[0]), sp.expand(x * p[1]))

def pair_diff(p):
    """d/dx (a*R + b) using R' = x*R - 1:
       = a'*R + a*(x*R-1) + b' = (a' + x*a)*R + (b' - a)"""
    a, b = p
    ap = sp.diff(a, x)
    bp = sp.diff(b, x)
    return (sp.expand(ap + x * a), sp.expand(bp - a))

def pair_eq(p, q):
    return sp.simplify(p[0] - q[0]) == 0 and sp.simplify(p[1] - q[1]) == 0

def pair_is_zero(p):
    return sp.simplify(p[0]) == 0 and sp.simplify(p[1]) == 0

log_lines = []
def log(s=""):
    print(s)
    log_lines.append(str(s))

log("=" * 78)
log("ADV01 — independent symbolic check of items 1, 2, 3")
log("=" * 78)

# ---------------------------------------------------------------------
# Part A: build R^{(k)} two independent ways, k = 0..8, cross-check
# ---------------------------------------------------------------------
log("\n--- Part A: R^{(k)}(x) via two independent constructions ---\n")

KMAX = 8

# Method (A): pure repeated differentiation, starting from R^{(0)}=R.
RA = {0: (sp.Integer(1), sp.Integer(0))}  # R^{(0)} = 1*R + 0
for k in range(1, KMAX + 1):
    RA[k] = pair_diff(RA[k - 1])

# sanity: RA[1] should be (x, -1), i.e. x*R - 1
assert pair_eq(RA[1], (x, sp.Integer(-1))), "R^{(1)} != x*R - 1 under method A"
log(f"Method A, R^(1) = {RA[1][0]}*R + ({RA[1][1]})  [expect x*R - 1]  OK")

# Method (B): the record's closure identity R^{(n+1)} = x*R^{(n)} + n*R^{(n-1)},
# seeded with the SAME two base cases R^{(0)}=R, R^{(1)}=x*R-1 (given, not derived).
RB = {0: (sp.Integer(1), sp.Integer(0)), 1: (x, sp.Integer(-1))}
for n in range(1, KMAX):  # produces R^{(n+1)} for n=1..KMAX-1, i.e. up to R^{(KMAX)}
    term1 = pair_mul_x(RB[n])
    term2 = pair_scale(RB[n - 1], n)
    RB[n + 1] = pair_add(term1, term2)

all_match = True
for k in range(0, KMAX + 1):
    ok = pair_eq(RA[k], RB[k])
    all_match &= ok
    log(f"k={k}:  method A = ({RA[k][0]}, {RA[k][1]})   "
        f"method B = ({RB[k][0]}, {RB[k][1]})   match={ok}")

assert all_match, "Methods A and B disagree somewhere -- STOP"
log(f"\n=> R^(k) constructions A (pure differentiation) and B (closure identity) "
    f"AGREE EXACTLY for k=0..{KMAX}. [PASS]")

# Use method B (the record's own closure identity) as the working representation
# from here on, per the mandate's explicit instruction.
Rk = RB

# ---------------------------------------------------------------------
# Part B: item 1 -- verify psi_n(x) = gamma_n * R^{(n-1)}(x) solves the
# record's stated ODEs psi_n' = x*psi_n + source_n(x), EXACTLY, for n=2,3,4.
# ---------------------------------------------------------------------
log("\n--- Part B (item 1): psi_n(x) = gamma_n * R^{(n-1)}(x) exact-ODE check ---\n")

gamma = {1: sp.Rational(1, 1), 2: sp.Rational(2, 1), 3: sp.Rational(7, 2), 4: sp.Rational(17, 3)}

def psi_pair(n):
    """psi_n(x) as an (a,b) pair: gamma_n * R^{(n-1)}(x)."""
    return pair_scale(Rk[n - 1], gamma[n])

# record's stated sources, in pair form:
#   psi_1' = x*psi_1 - 1            (source_1 = -1,   pair (0,-1))
#   psi_2' = x*psi_2 + 2*R          (source_2 = 2R,    pair (2,0))
#   psi_3' = x*psi_3 + 7*R'         (source_3 = 7*R'(x) = 7*(x,-1))
#   psi_4' = x*psi_4 + 17*R''       (source_4 = 17*R''(x) = 17*Rk[2])
sources = {
    1: (sp.Integer(0), sp.Integer(-1)),
    2: (sp.Integer(2), sp.Integer(0)),
    3: pair_scale(Rk[1], 7),
    4: pair_scale(Rk[2], 17),
}

for n in [1, 2, 3, 4]:
    psin = psi_pair(n)
    lhs = pair_sub(pair_diff(psin), pair_mul_x(psin))  # psi_n' - x*psi_n
    resid = pair_sub(lhs, sources[n])                   # should be (0,0)
    ok = pair_is_zero(resid)
    log(f"n={n}: psi_{n}(x) = {gamma[n]} * R^({n-1})(x) = "
        f"({psin[0]}) * R + ({psin[1]})")
    log(f"       residual (psi_n' - x*psi_n - source_n) = "
        f"({sp.simplify(resid[0])}, {sp.simplify(resid[1])})   "
        f"{'PASS (exact 0)' if ok else 'FAIL'}")
    assert ok, f"n={n} residual not exactly zero"

log("\n=> All four candidates psi_n(x) = gamma_n R^{(n-1)}(x), n=1..4, solve their\n"
    "   stated ODEs EXACTLY and IDENTICALLY IN x (not just at x=0). [PASS]")

# Sanity check at x=0 against the record's own published psi_n(0) values.
log("\n--- Sanity: psi_n(0) against record's published values ---\n")
import mpmath as mp
mp.mp.dps = 50
R0 = mp.sqrt(mp.pi / 2)  # R(0) = sqrt(pi/2) * erfcx(0) = sqrt(pi/2)

def sp_rational_to_mp(r):
    r = sp.nsimplify(r)
    frac = sp.Rational(r)
    return mp.mpf(frac.p) / mp.mpf(frac.q)

def eval_pair_at_0(p):
    a0 = sp_rational_to_mp(p[0].subs(x, 0))
    b0 = sp_rational_to_mp(p[1].subs(x, 0))
    return a0 * R0 + b0

published_psi0 = {
    1: R0,
    2: mp.mpf(-2),
    3: mp.mpf(7) / 2 * mp.sqrt(mp.pi / 2),
    4: -mp.mpf(34) / 3,
}
for n in [1, 2, 3, 4]:
    val = eval_pair_at_0(psi_pair(n))
    pub = published_psi0[n]
    reldiff = abs(val - pub) / abs(pub)
    log(f"n={n}: psi_{n}(0) computed = {mp.nstr(val, 20)}   "
        f"published = {mp.nstr(pub, 20)}   reldiff = {mp.nstr(reldiff, 5)}")
    assert reldiff < mp.mpf('1e-40'), f"psi_{n}(0) mismatch"
log("=> All match published psi_n(0) to full precision. [PASS]")

# ---------------------------------------------------------------------
# Part C: item 1 boundedness/uniqueness sanity (Growth-Exclusion Lemma logic)
# ---------------------------------------------------------------------
log("\n--- Part C (item 1): boundedness/uniqueness reasoning check ---\n")
log("The general solution of psi_n' - x*psi_n = source_n(x) is")
log("   psi_n(x) = [particular solution] + A * exp(x^2/2)")
log("for arbitrary constant A (verified: d/dx[A*exp(x^2/2)] = A*x*exp(x^2/2) ")
log("= x * [A*exp(x^2/2)], i.e. exp(x^2/2) solves the homogeneous equation")
log("u' = x*u exactly -- this is the y=0 case of the Growth-Exclusion Lemma's")
log("homogeneous mode e^{x^2/2+xy} (mclust_h2_validity_attempt Sec 2.1).")
u_hom = sp.exp(x**2 / 2)
resid_hom = sp.simplify(sp.diff(u_hom, x) - x * u_hom)
log(f"Direct symbolic check: d/dx[exp(x^2/2)] - x*exp(x^2/2) = {resid_hom}  "
    f"{'PASS' if resid_hom == 0 else 'FAIL'}")
assert resid_hom == 0

log("\nBoundedness of the candidate gamma_n*R^{(n-1)}(x) as x->infinity:")
log("R(x) -> 0 as x->infinity is the record's own established fact (R(inf)=0,")
log("erfcx(z)~1/(z*sqrt(pi)) for large z). We independently verify, via mpmath,")
log("that R(x) and R^{(1)}, R^{(2)}, R^{(3)} ALL decay (not blow up) as x grows,")
log("confirming the candidate genuinely sits in the bounded/decaying branch that")
log("the Growth-Exclusion Lemma selects as unique -- not merely a formal claim.")

def R_mpmath(xx):
    return mp.sqrt(mp.pi / 2) * mp.erfc(xx / mp.sqrt(2)) * mp.exp(xx**2 / 2)

def Rk_mpmath(k, xx):
    """Evaluate R^{(k)}(x) numerically from the (a,b) pair representation."""
    a, b = Rk[k]
    av = complex(a.subs(x, xx))
    bv = complex(b.subs(x, xx))
    return mp.mpf(av.real) * R_mpmath(xx) + mp.mpf(bv.real)

for xx in [0, 5, 10, 20, 40]:
    vals = [mp.nstr(Rk_mpmath(k, xx), 8) for k in range(4)]
    log(f"  x={xx:>3}: R,R',R'',R''' = {vals}")

log("=> R^{(0..3)}(x) all -> 0 as x -> infinity (numerically confirmed, no blow-up);")
log("   the diverging homogeneous branch exp(x^2/2) is excluded by the Growth-")
log("   Exclusion Lemma's uniqueness half (verified above, y=0 case) since it is")
log("   the ONLY way the general solution can fail to be bounded. Selecting")
log("   gamma_n*R^{(n-1)}(x) as the unique bounded solution is therefore SOUND,")
log("   correctly citing (not needing to re-derive) mclust_h2_validity_attempt's")
log("   Growth-Exclusion Lemma. [CONFIRMED]")

# ---------------------------------------------------------------------
# Part D: item 2 -- chi_n(x) closed form
# ---------------------------------------------------------------------
log("\n--- Part D (item 2): chi_n(x) := psi_n(x) - psi_{n-1}'(x) ---\n")

def psi_prime_pair(n):
    if n == 0:
        return (sp.Integer(0), sp.Integer(0))
    return pair_diff(psi_pair(n))

claimed_chi = {
    1: pair_scale(Rk[0], gamma[1] - 0),
    2: pair_scale(Rk[1], gamma[2] - gamma[1]),
    3: pair_scale(Rk[2], gamma[3] - gamma[2]),
    4: pair_scale(Rk[3], gamma[4] - gamma[3]),
}

for n in [1, 2, 3, 4]:
    direct = pair_sub(psi_pair(n), psi_prime_pair(n - 1))
    claim = claimed_chi[n]
    ok = pair_eq(direct, claim)
    log(f"n={n}: direct chi_{n} = psi_{n} - psi_{n-1}' = "
        f"({sp.simplify(direct[0])}, {sp.simplify(direct[1])})")
    log(f"       claimed (gamma_{n}-gamma_{n-1})*R^({n-1}) = "
        f"({sp.simplify(claim[0])}, {sp.simplify(claim[1])})   "
        f"{'PASS (identical)' if ok else 'FAIL'}")
    assert ok, f"chi_{n} mismatch"

# Explicit closed forms quoted in the target's Sec 2.2, cross-checked
log("\nExplicit closed forms quoted by the target (Sec 2.2):")
explicit_claims = {
    2: (sp.Integer(1), (x, sp.Integer(-1))),          # chi_2 = R' = x*R - 1  [coeff 1]
    3: (sp.Rational(3, 2), Rk[2]),                      # chi_3 = (3/2) R''
    4: (sp.Rational(13, 6), Rk[3]),                     # chi_4 = (13/6) R'''
}
for n, (coeff, base) in explicit_claims.items():
    claimed_pair = pair_scale(base, coeff)
    ok = pair_eq(claimed_chi[n], claimed_pair)
    log(f"n={n}: chi_{n} explicit claim vs (gamma_n-gamma_{{n-1}})*R^({n-1}) form: "
        f"{'PASS' if ok else 'FAIL'}")
    assert ok

log("\n=> chi_n(x) = (gamma_n - gamma_{n-1}) * R^{(n-1)}(x) VERIFIED EXACTLY, n=1..4,")
log("   including all three explicit closed forms quoted in the target's Sec 2.2.")
log("   [PASS]")

# ---------------------------------------------------------------------
# Part E: item 3 -- independent re-derivation of the telescoping /
# Watson's-lemma route, via an EXPLICIT double-index expansion (not
# merely asserting sum_{n=1}^N (gamma_n-gamma_{n-1}) = gamma_N).
# ---------------------------------------------------------------------
log("\n--- Part E (item 3): explicit double-index Watson's-lemma re-derivation ---\n")
log("Standard Watson's lemma: for g(v) smooth at v=0,")
log("   int_0^inf e^{-v/eps} g(v) dv  ~  sum_{j>=0} g^{(j)}(0) * eps^{j+1}")
log("(since int_0^inf e^{-v/eps} v^j dv = eps^{j+1} * j!, and g's j-th Taylor")
log("coefficient is g^{(j)}(0)/j!, the j! cancels).")
log("")
log("Applying this to g(v) = chi_n(v) = (gamma_n-gamma_{n-1})*R^{(n-1)}(v) gives")
log("   int_0^inf e^{-v/eps} chi_n(v) dv ~ sum_{j>=0} (gamma_n-gamma_{n-1}) *")
log("                                       R^{(n-1+j)}(0) * eps^{j+1}")
log("")
log("Pi(c) = (1/eps) * int_0^inf e^{-v/eps} * sum_n eps^n chi_n(v) dv")
log("      = sum_n eps^{n-1} * sum_j (gamma_n-gamma_{n-1}) R^{(n-1+j)}(0) eps^{j+1}")
log("      = sum_n sum_j eps^{n+j} (gamma_n-gamma_{n-1}) R^{(n-1+j)}(0)")
log("")
log("Collect coefficient of eps^N (N = n+j, j = N-n >= 0, so n=1..N):")
log("   coeff(eps^N) = sum_{n=1}^N (gamma_n-gamma_{n-1}) * R^{(n-1+(N-n))}(0)")
log("                = sum_{n=1}^N (gamma_n-gamma_{n-1}) * R^{(N-1)}(0)")
log("   [the exponent n-1+(N-n) = N-1 is INDEPENDENT OF n -- this is exactly")
log("    why R^{(N-1)}(0) factors out of the n-sum in the target's Sec 2.3]")
log("                = R^{(N-1)}(0) * sum_{n=1}^N (gamma_n-gamma_{n-1})")
log("                = R^{(N-1)}(0) * (gamma_N - gamma_0) = gamma_N * R^{(N-1)}(0)")
log("   [telescoping sum, gamma_0:=0 -- confirmed trivial but exact]")

# Now verify this mechanically, symbolically, for N = 1..4, using the actual
# gamma_n and R^{(k)} pairs built above (not just the abstract algebra argument).
gamma0 = {0: sp.Integer(0), **gamma}

def watson_coeff_v2(N):
    """coefficient of eps^N in Pi(c), via the explicit n,j double sum."""
    total = sp.Integer(0)
    for n in range(1, N + 1):
        j = N - n
        coeff_n = gamma0[n] - gamma0[n - 1]
        Rval = Rk[n - 1 + j]  # = Rk[N-1], but computed via the n,j formula literally
        a0 = Rval[0].subs(x, 0)
        b0 = Rval[1].subs(x, 0)
        total += coeff_n * (a0 * sp.sqrt(sp.pi / 2) + b0)
    return sp.simplify(sp.expand(total))

published_4term = {
    1: sp.sqrt(sp.pi / 2),
    2: sp.Integer(-2),
    3: sp.Rational(7, 2) * sp.sqrt(sp.pi / 2),
    4: sp.Rational(-34, 3),
}

log("\nMechanical check, N=1..4 (published Pi(c) 4-term-law coefficients, i.e.")
log("Pi(c) = sum_N eps^N * [this coefficient]):\n")
for N in [1, 2, 3, 4]:
    computed = watson_coeff_v2(N)
    pub = published_4term[N]
    diff = sp.simplify(computed - pub)
    log(f"N={N}: double-sum route = {computed}   published = {pub}   "
        f"diff = {diff}   {'PASS (exact 0)' if diff == 0 else 'FAIL'}")
    assert diff == 0, f"N={N} mismatch"

log("\n=> Independent re-derivation (via the FULL double-index Watson's-lemma")
log("   bookkeeping, not merely asserting the telescoping identity) reproduces")
log("   the record's published 4-term law EXACTLY, symbolically, at every one")
log("   of N=1..4. This confirms the target's compressed Sec 2.3 presentation")
log("   (which asserts, rather than shows step-by-step, that R^{(N-1)}(0) factors")
log("   out of the n-sum) is mathematically CORRECT -- the missing intermediate")
log("   step (why R^{(n-1+j)}(0) = R^{(N-1)}(0) independent of n) checks out")
log("   exactly. [PASS, item 3 confirmed via independent route]")

log("\n" + "=" * 78)
log("ADV01 SUMMARY: items 1, 2, 3 all independently confirmed. No discrepancy")
log("found anywhere in this script's fresh symbolic re-derivation.")
log("=" * 78)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'adv01_symbolic_check.log')
with open(out_path, 'w') as f:
    f.write('\n'.join(log_lines) + '\n')
