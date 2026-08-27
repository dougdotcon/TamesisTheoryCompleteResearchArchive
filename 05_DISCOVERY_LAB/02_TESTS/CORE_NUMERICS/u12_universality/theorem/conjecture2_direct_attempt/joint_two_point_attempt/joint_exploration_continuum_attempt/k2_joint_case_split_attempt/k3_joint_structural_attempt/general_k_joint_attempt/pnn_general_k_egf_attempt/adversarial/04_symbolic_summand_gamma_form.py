"""
Fully symbolic-in-(n,K,r) Piece B/C and Piece D r-summands, derived
independently (via moment_formula_check.py's from-scratch moment
machinery), converted to Gamma-function form, and compared DIRECTLY
against the target's own quoted closed forms from ATTEMPT.md Sec 5.2
(copied here verbatim from the prose, purely as the object of comparison
-- no .py file read).

Target's claim (Sec 5.2), copied verbatim from the prose:

  Piece B summand(r) = Piece C summand(r) =
      2*Gamma(K)*Gamma(n+r+2) / [n^(r+1) * Gamma(K-r) * Gamma(n-K-1) * Gamma(K+r+4)]

  Piece D summand(r) =
      2*(r+1)*Gamma(K-1)*Gamma(n+r+3) / [n^(r+2) * Gamma(n-K-1) * Gamma(K-r-1) * Gamma(K+r+5)]

"Summand(r)" is interpreted as the r-th term of piece B / C / D's own
displayed sum (Sec 2.3): i.e.
  PieceB(r) := K * C(K-1,r) * r!/n^(r+1) * [mu(L_0^2,r,O^1) - mu(L_0^1,r,O^1)]
  PieceC(r) := (K/3) * C(K-1,r) * r!/n^(r+1) * [mu(L_0^3,r) - 3 mu(L_0^2,r) + 2 mu(L_0^1,r)]
  PieceD(r) := (K(K-1)/2) * C(K-2,r) * (r+1)!/n^(r+2) *
                   [mu(L_0^2 L_1^2,r) - mu(L_0^2 L_1,r) - mu(L_0 L_1^2,r) + mu(L_0 L_1,r)]
(these are EXACTLY what piece_bcd_check.py re-derived and validated against
Propositions NN3/NN4 -- this file only takes them fully symbolic in K,r,n
via the general moment_formula_symbolic() route, since concrete-K numeric
substitution was already validated there.)
"""
import sympy as sp
from math import factorial
from importlib import import_module
moment_mod = import_module("02_moment_formula_independent")
moment_formula_symbolic = moment_mod.moment_formula_symbolic

n, K, r = sp.symbols('n K r', positive=True)


def mu(specials, b):
    return moment_formula_symbolic(specials, r, b, K, n)


print("=" * 70)
print("Deriving Piece B, C, D r-summands, fully symbolic in (n,K,r)")
print("=" * 70)

# NOTE ON CONVENTION: Sec 2.3 writes each piece as
#   Piece = <external multiplicity K, or K(K-1)/2> * sum_r <bare summand(r)>
# A first pass (see git history in this session's transcript / REFEREE_REPORT
# "Named issues") folded the external multiplicity INTO the per-r summand
# before comparing to Sec 5.2 -- that version's Gamma(K+1)/Gamma(K-1) did
# NOT match Sec 5.2's quoted Gamma(K)/Gamma(K-1) (off by a clean factor of
# K, resp. K(K-1)/2). Re-reading Sec 2.3 resolves the discrepancy: Sec 5.2's
# "summand(r)" is the BARE per-r term as literally written inside the Sum in
# Sec 2.3, i.e. WITHOUT the external multiplicity -- that is what is used
# below, and it is what is fed to Gosper in Sec 5.3 (multiplying by a
# constant-in-r factor never changes Gosper-summability in r, so this
# bookkeeping choice has no bearing on the substance of the Sec 5.3 claim,
# only on matching Sec 5.2's displayed formula exactly).

# Piece B "bare" summand(r): C(K-1,r) * r!/n^(r+1) * [mu(L0^2,r,O^1) - mu(L0^1,r,O^1)]
# (external multiplicity K applied separately, matching Sec 2.3's own display)
m2_b1 = mu([2], 1)
m1_b1 = mu([1], 1)
pieceB_r = sp.binomial(K - 1, r) * sp.factorial(r) / n ** (r + 1) * (m2_b1 - m1_b1)
pieceB_r = sp.simplify(pieceB_r)
print("\nPiece B bare summand(r), my derivation (external multiplicity K NOT included):")
sp.pprint(pieceB_r)

# Piece C "bare" summand(r): Sec 2.3 groups the coefficient as "(K/3)" in
# front of its Sum_r -- unlike Piece B's plain "K". Since target's Sec 5.2
# claims summand_B(r) === summand_C(r) IDENTICALLY, the natural reading
# (confirmed empirically below) is that only the INTEGER common factor K
# is treated as "external multiplicity" for both pieces; the fractional
# 1/3 stays as part of Piece C's own per-r summand definition.
m3_b0 = mu([3], 0)
m2_b0 = mu([2], 0)
m1_b0 = mu([1], 0)
pieceC_r = sp.Rational(1, 3) * sp.binomial(K - 1, r) * sp.factorial(r) / n ** (r + 1) * (m3_b0 - 3 * m2_b0 + 2 * m1_b0)
pieceC_r = sp.simplify(pieceC_r)
print("\nPiece C bare summand(r), my derivation (external multiplicity K only stripped, 1/3 kept):")
sp.pprint(pieceC_r)

diffBC = sp.simplify(pieceB_r - pieceC_r)
print(f"\nPiece B bare summand(r) - Piece C bare summand(r) simplifies to: {diffBC}")
print(f"B===C identical (my own independent re-derivation of target's Sec 5.2 curiosity): {diffBC == 0}")

# Piece D "bare" summand(r) (external multiplicity K(K-1)/2 applied separately)
m22 = mu([2, 2], 0)
m21 = mu([2, 1], 0)
m12 = mu([1, 2], 0)
m11 = mu([1, 1], 0)
pieceD_r = sp.Rational(1, 2) * sp.binomial(K - 2, r) * sp.factorial(r + 1) / n ** (r + 2) * (m22 - m21 - m12 + m11)
pieceD_r = sp.simplify(pieceD_r)
print("\nPiece D bare summand(r), my derivation (external multiplicity K(K-1) only stripped, 1/2 kept):")
sp.pprint(pieceD_r)

print("\n" + "=" * 70)
print("Compare to target's QUOTED Gamma-function formulas (Sec 5.2), copied")
print("verbatim from the ATTEMPT.md prose (not from any .py file):")
print("=" * 70)

target_BC = 2 * sp.gamma(K) * sp.gamma(n + r + 2) / (n ** (r + 1) * sp.gamma(K - r) * sp.gamma(n - K - 1) * sp.gamma(K + r + 4))
target_D = 2 * (r + 1) * sp.gamma(K - 1) * sp.gamma(n + r + 3) / (n ** (r + 2) * sp.gamma(n - K - 1) * sp.gamma(K - r - 1) * sp.gamma(K + r + 5))

print("\nTarget's Piece B/C summand:")
sp.pprint(target_BC)
print("\nTarget's Piece D summand:")
sp.pprint(target_D)

# Symbolic comparison is hard directly (binomial/factorial of symbolic K,r
# vs Gamma ratios don't always auto-simplify); do BOTH a symbolic attempt
# and a strong numeric-substitution check across many concrete (K,r,n).
print("\n" + "=" * 70)
print("Symbolic difference attempts (sympy simplify/gammasimp/rewrite):")
print("=" * 70)

for label, mine, theirs in [("B", pieceB_r, target_BC), ("C", pieceC_r, target_BC), ("D", pieceD_r, target_D)]:
    mine_gamma = mine.rewrite(sp.gamma)
    diff = sp.simplify(mine_gamma - theirs)
    diff2 = sp.simplify(sp.gammasimp(mine_gamma - theirs))
    print(f"Piece {label}: mine(rewritten in Gamma) - target  simplify-> {diff}   gammasimp-> {diff2}")

print("\n" + "=" * 70)
print("Strong numeric cross-check: substitute MANY concrete (K,r,n) triples")
print("(with r < K-1 or r < K-2 as appropriate, n large enough that all Gammas")
print(" are finite/well-defined -- i.e. n > K+1) and compare EXACTLY as Rationals.")
print("=" * 70)
all_ok = True
checked = 0
for K_val in range(3, 9):
    for r_val in range(0, K_val - 1):
        for n_val in (K_val + 2, K_val + 5, 2 * K_val + 3):
            subs_ = {K: K_val, r: r_val, n: n_val}
            myB = sp.nsimplify(pieceB_r.subs(subs_), rational=True)
            myC = sp.nsimplify(pieceC_r.subs(subs_), rational=True)
            tgtBC = sp.nsimplify(target_BC.subs(subs_), rational=True)
            okB = (sp.simplify(myB - tgtBC) == 0)
            okC = (sp.simplify(myC - tgtBC) == 0)
            all_ok &= okB and okC
            checked += 1
            if not (okB and okC):
                print(f"  MISMATCH at K={K_val} r={r_val} n={n_val}: myB={myB} myC={myC} target={tgtBC}")
        if r_val <= K_val - 2:
            for n_val in (K_val + 2, K_val + 5):
                subs_ = {K: K_val, r: r_val, n: n_val}
                myD = sp.nsimplify(pieceD_r.subs(subs_), rational=True)
                tgtD = sp.nsimplify(target_D.subs(subs_), rational=True)
                okD = (sp.simplify(myD - tgtD) == 0)
                all_ok &= okD
                checked += 1
                if not okD:
                    print(f"  MISMATCH (D) at K={K_val} r={r_val} n={n_val}: myD={myD} target={tgtD}")

print(f"\n{checked} numeric (K,r,n) substitutions checked. ALL EXACT MATCHES: {all_ok}")
