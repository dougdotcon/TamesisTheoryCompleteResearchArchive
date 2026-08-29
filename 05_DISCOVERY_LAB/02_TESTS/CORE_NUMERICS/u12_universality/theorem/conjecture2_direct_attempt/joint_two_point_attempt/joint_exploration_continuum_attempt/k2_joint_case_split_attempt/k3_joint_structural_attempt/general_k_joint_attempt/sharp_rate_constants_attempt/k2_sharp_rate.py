"""
k2_sharp_rate.py -- K=2 sharp uniform convergence-rate constant attempt.

Delta_n(x) := F_n^(2)(x) - F_2(x), with F_n^(2) the polynomial extension
of Proposicao D2 (THEOREM.md Estagio 42) to continuous x=k/n in [0,1],
F_2(x) = 1-(1-x^2)^2 the continuum limit (cited, Estagio 15/24).

Target: a genuinely sharp, PROVED, uniform-in-x-in-[0,1], uniform-in-
n>=N0 bound |Delta_n(x)| <= C/n, with C close to the numerically/
asymptotically observed leading constant.

Crude bound on record (Estagio 42 front's own Corollary D2.5): 12/n,
n>=2.
"""
import sympy as sp
from lib_cdf import n, k, x, CDF, F_continuum

log = []


def say(s=""):
    print(s)
    log.append(s)


say("=" * 78)
say("k2_sharp_rate.py -- K=2 sharp rate-constant attempt")
say("=" * 78)

# ---------------------------------------------------------------------
# Step 1: exact Delta_n(x), continuous x, via k -> n*x substitution.
cdf2 = CDF[2]
F2 = F_continuum(2)
delta_raw = cdf2.subs(k, n * x) - F2
delta = sp.cancel(sp.together(delta_raw))
say(f"\n[Step 1] Delta_n(x) (cancelled) = {delta}")

num, den = sp.fraction(delta)
num = sp.expand(num)
den = sp.factor(den)
say(f"  numerator N(n,x) = {num}")
say(f"  denominator D(n) = {den}")

# Cross-check against the ATTEMPT.md-cited form:
#   F_n^(2)(x)-F_2(x) = N(n,x)/[n(n-1)],  N=-n*x^4-n*x^2+2*n*x+x^2-3*x
cited_N = -n * x**4 - n * x**2 + 2 * n * x + x**2 - 3 * x
cited_den = n * (n - 1)
cited_delta = cited_N / cited_den
diff_check = sp.simplify(delta - cited_delta)
say(f"\n  Cross-check against K2_full_cdf_attempt/ATTEMPT.md Sec 5.5 "
    f"cited form:")
say(f"    cited Delta = {cited_delta}")
say(f"    (own_derivation - cited) simplifies to: {diff_check}  "
    f"(expect 0)")
assert diff_check == 0, "MISMATCH vs archive-cited D2.5 intermediate form!"

# ---------------------------------------------------------------------
# Step 2: split N(n,x) into powers of n: N(n,x) = n*g1(x) + g0(x)
N_poly = sp.Poly(num, n)
coeffs = N_poly.all_coeffs()  # highest degree first
deg = N_poly.degree()
say(f"\n[Step 2] N(n,x) as polynomial in n has degree {deg}")
g1 = sp.expand(N_poly.coeff_monomial(n))
g0 = sp.expand(N_poly.coeff_monomial(1)) if N_poly.degree() >= 0 else 0
# more robust: extract via nth coefficients
g1 = sp.expand(sp.diff(num, n))  # since num is degree 1 in n, d/dn gives g1 exactly
g0 = sp.expand(sp.simplify(num - n * g1))
say(f"  N(n,x) = n*g1(x) + g0(x)")
say(f"  g1(x) = {g1}")
say(f"  g0(x) = {g0}")

# So Delta_n(x) = [n*g1(x)+g0(x)] / [n(n-1)] = g1(x)/(n-1) + g0(x)/[n(n-1)]
say(f"\n  => Delta_n(x) = g1(x)/(n-1) + g0(x)/[n(n-1)]")

# n*Delta_n(x) - g1(x) = [n*g1(x)+g0(x)]/(n-1) - g1(x) = [g1(x)+g0(x)]/(n-1)
p = sp.expand(g1 + g0)
say(f"\n  n*Delta_n(x) - g1(x) = p(x)/(n-1),  p(x) = g1(x)+g0(x) = {p}")
say(f"  => Delta_n(x) = g1(x)/n + p(x)/[n(n-1)]")

# ---------------------------------------------------------------------
# Step 3: locate sup_x g1(x) over [0,1] exactly (critical points).
say("\n[Step 3] sup_{x in [0,1]} g1(x), via calculus")
g1p = sp.diff(g1, x)
say(f"  g1'(x) = {g1p}")
crit = sp.solve(sp.Eq(g1p, 0), x)
say(f"  critical points (all roots): {crit}")
real_crit = [c for c in crit if c.is_real]
say(f"  real critical points: {real_crit}")
candidates = [sp.Integer(0), sp.Integer(1)] + \
    [c for c in real_crit if c.is_real and 0 <= c <= 1]
vals = [(c, sp.nsimplify(g1.subs(x, c))) for c in candidates]
say(f"  g1 at candidates: {[(str(c), sp.N(v, 20)) for c, v in vals]}")
max_val = max(vals, key=lambda cv: sp.N(cv[1]))
say(f"  => argmax x* = {max_val[0]} = {sp.N(max_val[0],20)}, "
    f"g1(x*) = {max_val[1]} = {sp.N(max_val[1], 20)}")

M2_exact = max_val[1]
x2_star = max_val[0]

# Verify sign of g1 on [0,1] (need for later bounding): should be >=0.
say(f"\n  g1(x) on [0,1]: g1(0)={g1.subs(x,0)}, g1(1)={g1.subs(x,1)}, "
    f"g1(1/2)={g1.subs(x, sp.Rational(1,2))}")
xs_test = [sp.Rational(i, 100) for i in range(0, 101, 5)]
g1_nonneg = all(sp.N(g1.subs(x, xx)) >= -1e-12 for xx in xs_test)
say(f"  g1(x)>=0 sampled on [0,1] (0.05 grid): {g1_nonneg}")

# Sign / range of p(x) on [0,1]
say(f"\n  p(x) = {p}: p(0)={p.subs(x,0)}, p(1)={p.subs(x,1)}")
pp = sp.diff(p, x)
crit_p = sp.solve(sp.Eq(pp, 0), x)
say(f"  p'(x)={pp}, critical points: {crit_p}")
p_nonpos = all(sp.N(p.subs(x, xx)) <= 1e-12 for xx in xs_test)
say(f"  p(x)<=0 sampled on [0,1]: {p_nonpos}")
p_min = min(sp.N(p.subs(x, xx)) for xx in xs_test)
say(f"  p(x) range sample min ~ {p_min} (expect p(1)=-2 to be the min)")

# ---------------------------------------------------------------------
# Step 4: for FIXED small n, find exact sup_x |Delta_n(x)| via calculus
# on the exact rational function (not a numeric grid) -- this handles
# "small n by direct exhaustive numeric verification" using EXACT
# critical-point algebra, which is stronger than a grid search.
say("\n[Step 4] Exact sup_x |Delta_n(x)| for concrete small n (calculus, "
    "not grid)")


def exact_sup_abs_delta(nn):
    """Return (x*, value, n*value) maximizing |Delta_n(x)| over x in [0,1]
    for a CONCRETE integer n, via exact calculus on the rational function
    Delta_n(x) (numerator/denominator are polynomials in x once n is
    fixed)."""
    dn = delta.subs(n, nn)
    dn = sp.together(dn)
    dnp = sp.diff(dn, x)
    dnp = sp.together(dnp)
    num_p, _ = sp.fraction(sp.cancel(dnp))
    crit_pts = sp.solve(sp.Eq(num_p, 0), x)
    real_pts = [c for c in crit_pts if c.is_real]
    cand = [sp.Integer(0), sp.Integer(1)] + \
        [c for c in real_pts if c.is_real and 0 <= sp.re(c) <= 1]
    best = None
    for c in cand:
        try:
            v = dn.subs(x, c)
            v = sp.nsimplify(v)
        except Exception:
            continue
        av = sp.Abs(v)
        if best is None or sp.N(av) > sp.N(best[1]):
            best = (c, av, v)
    return best


rows = []
for nn in range(2, 41):
    xstar, absval, signedval = exact_sup_abs_delta(nn)
    nval = sp.N(nn * absval, 15)
    rows.append((nn, xstar, signedval, absval, nval))
    say(f"  n={nn:3d}: x*={sp.N(xstar,6)!s:>10}  Delta_n(x*)={sp.N(signedval,10)!s:>14}  "
        f"n*|Delta_n(x*)|={nval}")

with open("k2_exact_sup_table.txt", "w") as f:
    f.write("n, x*, Delta_n(x*), |Delta_n(x*)|, n*|Delta_n(x*)|\n")
    for nn, xstar, signedval, absval, nval in rows:
        f.write(f"{nn}, {sp.N(xstar,12)}, {sp.N(signedval,15)}, "
                f"{sp.N(absval,15)}, {nval}\n")

# ---------------------------------------------------------------------
# Step 5: is n*sup_x|Delta_n(x)| monotone decreasing to M2_exact for
# n >= some N0? Identify where the max flips from the x=1 boundary
# artifact regime to the interior-critical-point regime.
say("\n[Step 5] Behaviour of n*sup_x|Delta_n(x)| vs n; identify N0 where "
    "interior critical point (near x*~0.589) dominates and the sequence")
say("  settles into a bound close to M2_exact.")

nvals = [r[4] for r in rows]
say(f"  M2_exact (sup g1) = {sp.N(M2_exact, 15)} at x*={sp.N(x2_star,15)}")
say(f"  n*sup|Delta_n| sequence (n=2..40): {[float(sp.N(v,8)) for v in nvals]}")

# find first n from which the sequence stays within a small margin of M2
margin_targets = [0.001, 0.005, 0.01, 0.02, 0.05]
for m in margin_targets:
    N0 = None
    for i, r in enumerate(rows):
        nn, xstar, signedval, absval, nval = r
        if all(float(sp.N(rows[j][4], 10)) <= float(sp.N(M2_exact, 10)) + m
               for j in range(i, len(rows))):
            N0 = nn
            break
    say(f"  smallest N0 s.t. n*sup|Delta_n(x)| <= M2_exact+{m} for all "
        f"n in [N0,40] (sampled): {N0}")


# ---------------------------------------------------------------------
# Step 6: FULL CLOSURE ATTEMPT via elementary sign argument (no need
# for delicate joint-critical-point analysis of g1(x)+p(x)/(n-1)).
#
# Key facts (all proved below, exactly, not numerically):
#   (a) g1(x) >= 0 for all x in [0,1]   [g1(x)=x*(2-x-x^3), and
#       2-x-x^3 is strictly decreasing on [0,1] with value 0 at x=1,
#       hence >=0 throughout [0,1]]
#   (b) max_{[0,1]} g1(x) = M2_exact, attained at the UNIQUE real root
#       x2_star of g1'(x)=-4x^3-2x+2=0 in (0,1) [g1' strictly
#       decreasing (g1''=-12x^2-2<0), g1'(0)=2>0, g1'(1)=-4<0, so
#       exactly one root in (0,1); unimodal => that root is the max]
#   (c) p(x) = -x^4-x <= 0 for all x in [0,1], strictly decreasing
#       (p'(x)=-4x^3-1<0 throughout), so min_{[0,1]} p(x) = p(1) = -2
#
# Then, since n*Delta_n(x) = g1(x) + p(x)/(n-1) for n>=2:
#   UPPER:  n*Delta_n(x) <= g1(x) + 0        <= M2_exact          (n>=2)
#   LOWER:  n*Delta_n(x) >= 0     + (-2)/(n-1) = -2/(n-1)          (n>=2)
# So |Delta_n(x)| <= max(M2_exact, 2/(n-1)) / n for ALL n>=2, x in [0,1].
# And 2/(n-1) <= M2_exact  iff  n >= 1+2/M2_exact, i.e. n>=4 (checked
# exactly below) -- so for n>=4 the bound collapses to the SHARP
# |Delta_n(x)| <= M2_exact/n, with M2_exact the EXACT asymptotic
# leading constant (not just close to it).

say("\n" + "=" * 78)
say("[Step 6] FULL CLOSURE attempt: elementary sign argument")
say("=" * 78)

# (a) g1(x)=x*(2-x-x^3) >= 0 on [0,1]: check 2-x-x^3 decreasing, =0 at x=1
factor_check = sp.expand(x * (2 - x - x**3) - g1)
say(f"  g1(x) - x*(2-x-x^3) = {factor_check}  (expect 0)")
assert factor_check == 0
h_ = 2 - x - x**3
hprime = sp.diff(h_, x)
say(f"  h(x):=2-x-x^3, h'(x)={hprime}  (negative on [0,1] since -1-3x^2<0)")
say(f"  h(1) = {h_.subs(x,1)}  (expect 0)  => h(x)>=0 on [0,1] => g1(x)>=0")
assert h_.subs(x, 1) == 0
assert sp.simplify(hprime) == -1 - 3 * x**2  # manifestly negative on reals

# (b) unique critical point of g1 in (0,1), and it is the max
g1pp = sp.diff(g1p, x)
say(f"  g1''(x) = {g1pp}  (manifestly negative for all real x => g1' "
    f"strictly decreasing => at most one root)")
assert sp.simplify(g1pp - (-12 * x**2 - 2)) == 0
say(f"  g1'(0)={g1p.subs(x,0)} (>0),  g1'(1)={g1p.subs(x,1)} (<0)  "
    f"=> exactly one root in (0,1), by IVT + strict monotonicity")
assert g1p.subs(x, 0) == 2 and g1p.subs(x, 1) == -4

# (c) p(x) strictly decreasing on [0,1], min at x=1
pprime = sp.diff(p, x)
say(f"  p(x)=-x^4-x, p'(x)={pprime}  (manifestly negative for x>=0)")
assert sp.simplify(pprime - (-4 * x**3 - 1)) == 0
say(f"  => p strictly decreasing on [0,1] => min_[0,1] p(x) = p(1) = "
    f"{p.subs(x,1)}")
assert p.subs(x, 1) == -2

say(f"\n  Combining: for all n>=2, x in [0,1]:")
say(f"    M2_exact/... UPPER: n*Delta_n(x) <= g1(x) <= M2_exact = "
    f"{sp.N(M2_exact, 20)}")
say(f"    LOWER: n*Delta_n(x) >= -2/(n-1)")
say(f"  => |Delta_n(x)| <= max(M2_exact, 2/(n-1))/n for all n>=2, "
    f"x in [0,1].")

threshold_n = sp.solve(sp.Eq(2 / (n - 1), M2_exact), n)
say(f"\n  Crossover: 2/(n-1) = M2_exact at n = {[sp.N(t,15) for t in threshold_n]}")
n_cross = [t for t in threshold_n if t.is_real][0]
say(f"  n_cross = {sp.N(n_cross, 15)}  => for integer n, 2/(n-1)<=M2_exact "
    f"holds iff n >= {sp.ceiling(n_cross)}")
N0_final = int(sp.ceiling(n_cross))
say(f"  N0 = {N0_final}")

# Explicit numeric check at n=N0-1 and n=N0
for nn in (N0_final - 1, N0_final, N0_final + 1):
    lhs = sp.Rational(2, nn - 1)
    say(f"    n={nn}: 2/(n-1) = {lhs} = {sp.N(lhs,10)}   vs M2_exact = "
        f"{sp.N(M2_exact,10)}   2/(n-1)<=M2_exact: "
        f"{sp.N(lhs,10) <= sp.N(M2_exact,10)}")

say(f"\n  ==> THEOREM (K=2, PROVED): for all n>={N0_final} and all x in "
    f"[0,1]:")
say(f"        |Delta_n(x)| = |F_n^(2)(x)-F_2(x)| <= M2_exact/n")
say(f"      where M2_exact = max_x g1(x) is the EXACT real root value "
    f"{sp.N(M2_exact,20)} (root of 2t^3+t-1=0, i.e. g1'(t)=0)")
say(f"      This constant is SHARP: n*Delta_n(x*(n)) -> M2_exact as "
    f"n->infinity (Step 4 table), so no smaller universal constant "
    f"works for all large n.")

# Independent double check: verify 2*x^3+x-1 is indeed satisfied by x2_star
poly_check = sp.simplify(2 * x2_star**3 + x2_star - 1)
say(f"\n  Double-check x2_star satisfies 2x^3+x-1=0: {poly_check} "
    f"(expect 0)")
assert sp.simplify(2 * x2_star**3 + x2_star - 1) == 0

# ---------------------------------------------------------------------
# Step 7: brute numeric verification of the FINAL closed-form bound
# max(M2_exact,2/(n-1))/n over a dense (n,x) grid, floats only as an
# EXTRA sanity net (the proof above is exact/symbolic and does not
# depend on this).
say("\n" + "=" * 78)
say("[Step 7] Dense numeric grid double-check of final bound (float, "
    "sanity only -- proof is Step 6, exact)")
say("=" * 78)
import random as _random
M2f = float(sp.N(M2_exact, 30))


def delta_n_float(nn, xx):
    return (-nn * xx**4 - nn * xx**2 + 2 * nn * xx + xx**2 - 3 * xx) / (nn * (nn - 1))


worst_ratio = 0.0
worst_case = None
for nn in list(range(2, 200)) + [500, 1000, 5000, 20000]:
    bound = max(M2f, 2.0 / (nn - 1)) / nn
    for i in range(0, 2001):
        xx = i / 2000.0
        val = abs(delta_n_float(nn, xx))
        ratio = val / bound if bound > 0 else 0
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_case = (nn, xx, val, bound)

say(f"  Grid scan n in [2,200]U{{500,1000,5000,20000}}, x on 2001-pt grid "
    f"per n:")
say(f"  worst observed |Delta_n(x)| / bound ratio = {worst_ratio:.10f} "
    f"at (n,x)={worst_case[0:2]}  (must be <=1)")
assert worst_ratio <= 1.0 + 1e-9, "Grid check found a VIOLATION of the bound!"
say("  PASS: no violation found on grid.")

with open("k2_sharp_rate.log", "w") as f:
    f.write("\n".join(log) + "\n")

say("\n[Saved] k2_exact_sup_table.txt, k2_sharp_rate.log")
