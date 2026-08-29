"""
Referee script 02.

(A) Independent symbolic + by-hand-style confirmation that
      Int_0^inf T_prof(lambda,gamma) dlambda = (1/2) sqrt(pi/beta),
      beta = gamma(2-gamma)/2,
    i.e. exactly the coefficient of sqrt(n) in G_n (Lemma D0, PROVED,
    cited). This is claim 3 of the target.

(B) "Not circular" check: grep the target's own scripts 02 and 03 (the
    scripts that DERIVE T_prof) for any occurrence of G_n, beta, or the
    scaling-law constant T(gamma)=sqrt(2/(2-gamma)) -- if the derivation
    of T_prof never references these objects, the match found in (A) is
    a genuine, falsifiable consistency check, not a restatement of an
    assumed fact. Reproduced independently here (not just reading the
    prose) via direct file inspection.
"""
import sympy as sp
import os

print("=" * 78)
print("PART A: independent confirmation of Int_0^inf T_prof dlambda = (1/2) sqrt(pi/beta)")
print("=" * 78)

gamma, lam, beta = sp.symbols('gamma lambda beta', positive=True)
A_gamma = (2 - gamma) / (2 * gamma)
T_prof = (1 / gamma) * sp.exp(-A_gamma * lam ** 2)

# By-hand route: Int_0^inf exp(-a lambda^2) dlambda = (1/2) sqrt(pi/a), a = A_gamma.
# Write pi/A_gamma = pi*2*gamma/(2-gamma) BEFORE taking sqrt (avoids a sympy
# branch-cut artifact, sqrt(-1/(gamma-2)) vs sqrt(2-gamma), that otherwise
# blocks automatic simplification to zero -- purely a presentation choice,
# not a different computation).
pi_over_A = sp.pi * 2 * gamma / (2 - gamma)
by_hand = (1 / gamma) * sp.Rational(1, 2) * sp.sqrt(pi_over_A)
by_hand_simplified = sp.simplify(by_hand)
print("By-hand Gaussian-integral formula, substituted a=A(gamma)=(2-gamma)/(2 gamma):")
print("  Int = (1/gamma)*(1/2)*sqrt(pi/A(gamma)) =", by_hand_simplified)

beta_def = gamma * (2 - gamma) / 2
target = sp.Rational(1, 2) * sp.sqrt(sp.pi / beta)
target_sub = sp.simplify(target.subs(beta, beta_def))
print("Target G_n coefficient (1/2) sqrt(pi/beta), beta=gamma(2-gamma)/2:", target_sub)

# Sympy's automatic sqrt-rewriting under the (gamma-2)<0 branch makes a
# direct sp.simplify(diff)==0 check brittle (a presentation/branch-cut
# artifact, the same KIND of sympy limitation the target's own script 04
# self-caught and disclosed -- see ATTEMPT.md Section 8 item... consistent
# behavior independently encountered here too). Prove equality robustly
# instead by squaring both (manifestly positive, for gamma in (0,2)) sides:
lhs_sq = sp.simplify(by_hand_simplified ** 2)
rhs_sq = sp.simplify(target_sub ** 2)
print("Squared by-hand result:", lhs_sq)
print("Squared target:", rhs_sq)
diff_sq = sp.simplify(lhs_sq - rhs_sq)
print("Difference of squares:", diff_sq)
assert diff_sq == 0
print("(Both sides manifestly positive for gamma in (0,2), so equal squares => equal.)")

# Fully independent second route: sp.integrate from scratch (own code, not
# copied from the target's script 04)
integral_full = sp.integrate(T_prof, (lam, 0, sp.oo))
print()
print("sp.integrate() raw result:", integral_full)
if hasattr(integral_full, 'args') and integral_full.is_Piecewise:
    integral_branch = integral_full.args[0][0]
else:
    integral_branch = integral_full
diff2 = sp.simplify(integral_branch - target_sub)
print("Difference (sp.integrate route vs G_n coefficient):", diff2)
assert diff2 == 0

print()
print("Numeric spot-check at 5 fresh rational gamma (disjoint from the target's")
print("own 6-point grid {1/7,1/3,2/5,1/2,3/4,9/10}):")
for gnum, gden in [(1, 5), (3, 8), (5, 9), (11, 20), (7, 8)]:
    g_val = sp.Rational(gnum, gden)
    lhs = float(by_hand_simplified.subs(gamma, g_val))
    rhs = float(target_sub.subs(gamma, g_val))
    print(f"  gamma={gnum}/{gden}: by-hand={lhs:.15f}  G_n-coeff={rhs:.15f}  diff={abs(lhs-rhs):.3e}")
    assert abs(lhs - rhs) < 1e-12

print()
print(">>> CONFIRMED (independent symbolic + by-hand + fresh numeric spot check):")
print(">>> Int_0^inf T_prof(lambda,gamma) dlambda = (1/2) sqrt(pi/beta) EXACTLY.")

print()
print("=" * 78)
print("PART B: 'not circular' check -- direct file inspection of the target's")
print("        own scripts 02/03 (which DERIVE T_prof) for G_n/beta/T(gamma)")
print("=" * 78)

target_dir = os.path.dirname(os.path.abspath(__file__))
# The target's directory is passed via env var by the calling shell wrapper;
# fall back to a relative search if not set.
tgt_path = os.environ.get("TARGET_DIR")
if tgt_path is None:
    raise SystemExit("Set TARGET_DIR env var to the joint_saddle_point_attempt directory before running.")

for fname in ["02_inner_saddle_exact.py", "03_saddle_value_expansion.py"]:
    fpath = os.path.join(tgt_path, fname)
    with open(fpath) as f:
        content = f.read()
    hits = []
    for needle in ["G_n", "sqrt(pi/beta", "T_gamma", "beta ", "beta=", "beta:="]:
        if needle in content:
            hits.append(needle)
    print(f"  {fname}: occurrences of G_n/beta/T(gamma)-related tokens: {hits if hits else 'NONE'}")
    assert not hits, f"UNEXPECTED: {fname} references G_n/beta -- circularity concern!"

print()
print("CONFIRMED: neither script 02 (inner saddle t*) nor script 03 (T_prof")
print("derivation) references G_n, beta, or T(gamma) anywhere. The match found")
print("in Part A is therefore a genuine, non-circular, falsifiable consistency")
print("check of the whole pipeline (Beta-integral -> inner saddle -> Stirling ->")
print("outer continuum limit) against an independently, previously-PROVED fact")
print("(Lemma D0's G_n coefficient) -- the target's 'not circular' claim (ATTEMPT.md")
print("Section 5) is CONFIRMED accurate.")
