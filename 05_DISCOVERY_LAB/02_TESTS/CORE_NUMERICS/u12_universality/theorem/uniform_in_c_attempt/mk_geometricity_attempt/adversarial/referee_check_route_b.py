"""
REFEREE independent check 6 -- Section 4 (Route B): the referee re-derives
the algebra of steps (a)/(b) from scratch, and independently spot-checks
the target document's characterization of archive state for step (c)
against the PRIMARY sources (not the target's citation of them).

(a) Half-sum identity underlying F_r(2,0) <= phi_r * 2^r:
    Already proved independently in referee_check_crude_bound.py part (i).
    Here we additionally re-derive, from scratch, the SHARPER bound
    F_r(2,0) <= phi_r * 2^r starting from the primary-source closed form

        F_r(2,0) = (phi_r/4^r) * sum_{i=0}^r 2^{r-i} C(2r+1,i)

    (error_constant_growth_attempt/ATTEMPT.md Section 6.2, line ~597),
    read directly from the primary source -- NOT reused from the target's
    own route_b_arithmetic.py (not read).

(b) Proposicao 6's boxed recursion (error_constant_growth_attempt/ATTEMPT.md
    Section 6.1, PROVED, read directly from the primary source):

        D'_r(b) := [r C'_{r-1}(b) + A_r(b)] / (r+b+1)
        C'_r(b) := B_r(b) + [r/(b+r+1)] C'_{r-1}(b+1) + D'_r(b+1)

    Substituting D'_r(b+1) into C'_r(b) should give exactly

        C'_r(b) = B_r(b) + A_r(b+1)/(r+b+2)
                  + C'_{r-1}(b+1) * [r/(b+r+1) + r/(r+b+2)]

    and, since b>=0 implies both bracketed fractions are <1, dropping the
    denominator on the A_r(b+1) term gives the ledger's quoted crude bound

        C'_r(b) <= (B_r(b) + A_r(b+1)) + 2 C'_{r-1}(b+1).

    Verified symbolically from scratch (sympy, r/b/A/B/C' as free symbols).

(c) Spot-check of the target's diagnosis that a general-b geometric bound
    on A_r(b), B_r(b) is genuinely NOT established anywhere in the archive
    -- done by reading (not this script, see referee report prose) the
    PRIMARY sources error_constant_growth_attempt/ATTEMPT.md Section 6.3's
    status table and Section 8.3's open-items list, and
    k_general_existence_attempt/ATTEMPT.md Section 9's scorecard row 7,
    directly.
"""
import sympy as sp
from math import comb, factorial
from fractions import Fraction

print("=== (a) F_r(2,0) <= phi_r * 2^r, from the primary-source closed form ===")


def phi_frac(rv):
    return Fraction(4**rv * factorial(rv)**2, factorial(2 * rv + 1))


def F_r_2_0_exact(rv):
    """F_r(2,0) = (phi_r/4^r) sum_{i=0}^r 2^{r-i} C(2r+1,i), exact Fraction,
    from error_constant_growth_attempt/ATTEMPT.md Sec 6.2 (primary source)."""
    phir = phi_frac(rv)
    s = sum(2**(rv - i) * comb(2 * rv + 1, i) for i in range(0, rv + 1))
    return phir * Fraction(s, 4**rv)


viol_sharp = 0
viol_ledger = 0
for rv in range(0, 100):
    Fval = F_r_2_0_exact(rv)
    phir = phi_frac(rv)
    sharp_bound = phir * 2**rv
    ledger_bound = 2 * phir * 2**rv
    if Fval > sharp_bound:
        viol_sharp += 1
        print(f"  SHARP BOUND VIOLATED at r={rv}: F_r(2,0)={Fval}, bound={sharp_bound}")
    if Fval > ledger_bound:
        viol_ledger += 1
        print(f"  LEDGER BOUND VIOLATED at r={rv}: F_r(2,0)={Fval}, bound={ledger_bound}")

print(f"r=0..99: sharp bound (phi_r*2^r) violations: {viol_sharp}")
print(f"r=0..99: ledger bound (2*phi_r*2^r) violations: {viol_ledger}")
print()
print("Derivation of the sharp bound, re-derived independently:")
print("  2^{r-i} <= 2^r for all i>=0 (since i>=0 => r-i<=r).")
print("  => sum_{i=0}^r 2^{r-i} C(2r+1,i) <= 2^r * sum_{i=0}^r C(2r+1,i) = 2^r * 2^{2r} = 2^{3r}")
print("     (using the half-sum identity proved independently in referee_check_crude_bound.py).")
print("  => F_r(2,0) = (phi_r/4^r) * [that sum] <= phi_r * 2^{3r}/4^r = phi_r * 2^r.  QED (matches target's claim).")
print()

print("=== (b) Proposicao 6 recursion substitution, symbolic, from scratch ===")
r, b = sp.symbols('r b', positive=True)
Ar1, Br, Crm1 = sp.symbols("A_r_bp1 B_r C_rm1_bp1")  # A_r(b+1), B_r(b), C'_{r-1}(b+1)

# D'_r(b+1) := [r C'_{r-1}(b+1) + A_r(b+1)] / (r + (b+1) + 1) = [...]/(r+b+2)
Dprime_bp1 = (r * Crm1 + Ar1) / (r + b + 2)

# C'_r(b) := B_r(b) + r/(b+r+1) * C'_{r-1}(b+1) + D'_r(b+1)
Cprime_r_b = Br + (r / (b + r + 1)) * Crm1 + Dprime_bp1

expanded = sp.expand(Cprime_r_b)

# Target claim: C'_r(b) = B_r(b) + A_r(b+1)/(r+b+2) + C'_{r-1}(b+1)*[r/(b+r+1)+r/(r+b+2)]
claimed = Br + Ar1 / (r + b + 2) + Crm1 * (r / (b + r + 1) + r / (r + b + 2))

diff = sp.simplify(expanded - claimed)
print(f"C'_r(b) [from boxed recursion, substituted] - [target's claimed form] = {diff}")
sub_ok = (diff == 0)
print(f"Substitution algebra: {'MATCH' if sub_ok else 'MISMATCH'}")
print()

print("Coefficient bound check: r/(b+r+1) < 1 and r/(r+b+2) < 1 for all r>0,b>=0")
coef1 = r / (b + r + 1)
coef2 = r / (r + b + 2)
viol_coef = 0
for rv in range(1, 60):
    for bv in range(0, 30):
        c1 = Fraction(rv, bv + rv + 1)
        c2 = Fraction(rv, rv + bv + 2)
        if c1 >= 1 or c2 >= 1:
            viol_coef += 1
            print(f"  COEFFICIENT >= 1 at r={rv},b={bv}: c1={c1}, c2={c2}")
print(f"r=1..59, b=0..29: coefficient violations: {viol_coef}")
print()
print("Hence C'_r(b) <= B_r(b) + A_r(b+1) [dropping denom r+b+2>1] + 2 C'_{r-1}(b+1)")
print("[since coef1+coef2 < 1+1 = 2], exactly the ledger's quoted crude inequality.")
print("Ledger algebra: VERIFIED, matches Section 4 of the target document exactly.")
print()

overall = (viol_sharp == 0 and viol_ledger == 0 and sub_ok and viol_coef == 0)
print(f"OVERALL (a)+(b): {'ALL CHECKS PASS' if overall else 'FAILURE DETECTED'}")
print()
print("=== (c) Archive-state spot-check (textual, cross-referenced against primary sources) ===")
print("""
Read directly (not via the target's citation):

error_constant_growth_attempt/ATTEMPT.md Section 6.3 status table (line ~621):
  "A_r(b), B_r(b) -- the tail/substitution constants | geometric, ratio ->9/8 |
   NUMERICALLY CHARACTERIZED, mechanism proved (Lemma 7)"
  "D'_r(b), C'_r(b) -- improved rigorous bound | geometric, measured ratio 1.240
   at r=45, slowly decreasing | PROVED bound; rate NUMERICALLY CHARACTERIZED"

error_constant_growth_attempt/ATTEMPT.md Section 8.3 "What remains open" (line ~722-737):
  item 1: "A polynomial-in-r rigorous bound... no closed-form sup_[0,1]|q_k(.,b)|
   is derived here" (i.e. no general-b closed-form / tight bound on the pieces
   that make up A_r(b),B_r(b) beyond the crude coefficient-sum norm of Lemma 7).
  item 4: "The exact rate of the improved bound D'_r(b) -- measured 1.240 at
   r=45, plausibly heading to 9/8 but not established."

k_general_existence_attempt/ATTEMPT.md Section 9 scorecard row 7 (line 542):
  "Closed-form expressions for D_r(b),C_r(b),A_r(b) for general r |
   NOT ATTEMPTED -- defined by an explicit terminating recursion/procedure instead"

CONCLUSION: the target document's diagnosis -- that a general-b geometric
CLOSED-FORM bound on A_r(b),B_r(b) is genuinely not established anywhere in
the archive, only "NUMERICALLY CHARACTERIZED, mechanism proved" at b=0
(Lemma 7's F_r(2,0)) -- is ACCURATE relative to the primary sources actually
consulted here. Minor imprecision noted: the target's own Section 0 citation
paraphrases Section 8.3 item 1 as literally reading "closed-form for A_r(b),
B_r(b) not attempted", which is not a verbatim quote (the actual item 1 text
is about a *polynomial-in-r bound via sup-norm*, not verbatim "closed form for
A_r(b),B_r(b)") -- but the SUBSTANCE of the claim (no rigorous general-b
geometric bound exists, only numerically characterized) is fully supported by
the Section 6.3 status-table line quoted above, which the target also cites
correctly elsewhere (Section 4, "own reading found no route..."). This is a
paraphrase-accuracy nit, not a substantive misrepresentation of archive state.
""")
