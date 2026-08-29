"""
ADVERSARIAL / REFEREE SCRIPT 2 (item 1): independently RE-DERIVE the closed
form W(r,t)=(t+2r+1)(t+r)! from the monomial-expansion definition (not
pattern-matched), following the same "all-diagonal + r doubled-at-b terms"
decomposition the target's ATTEMPT.md Section 3.3 uses, but redone from
scratch by hand (see referee's own derivation, reproduced in the REFEREE
report) and checked here symbolically at every step.

KEY FINDING checked by this script: per-composition contribution.

For the ALL-DIAGONAL term (Prop-S monomial exponent = all-1's + p_D^1,
coefficient r!), combined with a conditional-moment monomial of composition
(k_0,...,k_{r-1},k_D) [coefficient t!/(k_D! prod k_a!) * prod 1/(k_a+1)],
the referee's own hand computation gives PER-COMPOSITION CONTRIBUTION TO
W(r,t):
    r! * t! * (k_D + 1)
-- i.e. INCLUDING both the r! (Prop S's own prefactor) AND a factor of t!
(from the multinomial coefficient's own t!), not just "t!*(k_D+1)" as the
target's ATTEMPT.md Section 3.3 prose states for "the combined coefficient
times prod(exps!)" (that prose appears to silently drop the leading r!,
which is fine since r! is applied uniformly and pulled out at the very end
-- but ALSO, more importantly, the summing step immediately after it,
"W(r,t) = r!\\big[(tN/(r+1)+N) + r(tN/(r+1)+2N)\\big]", is inconsistent
with its own preceding paragraph: it carries only ONE power of r! and NO
power of t!, whereas summing "t!*(k_D+1)" over N compositions must give
t!*(N + sum k_D) = t!*(N+tN/(r+1)), so the correct sum should carry an
explicit t! factor that the written intermediate formula omits. The very
next line's boxed final step DOES reinsert a "*t!" factor out of nowhere
("r!\\cdot(t+r)!/(t!r!)\\cdot t!\\cdot(t+2r+1)") to arrive at the correct
final answer. This script verifies: (a) the referee's own corrected
per-composition formula holds EXACTLY (via direct symbolic evaluation of
each composition's actual monomial coefficient, not assumed), (b) summing
it over all compositions and simplifying via N=C(t+r,r) DOES telescope
to exactly (t+2r+1)(t+r)!, confirming the FINAL closed form is correct,
and (c) explicitly flags the intermediate-formula inconsistency described
above by evaluating the target's own written bracket formula literally and
showing it does NOT equal W(r,t) whenever t!>1 (i.e. t>=2) -- while the
CORRECTED version (with the missing t! reinstated) does.
"""
import math
from fractions import Fraction as Fr

import sympy as sp


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def W_direct(r, t):
    """Ground truth, direct monomial expansion (independent third
    implementation, yet another code shape, for triangulation)."""
    total = Fr(0)
    fact_r = math.factorial(r)
    # all-diagonal term
    for comp in compositions(t, r + 1):
        ks = comp[:-1]
        kD = comp[-1]
        # conditional-moment coeff
        cmoeff = Fr(math.factorial(t))
        cmoeff /= math.factorial(kD)
        for k in ks:
            cmoeff /= math.factorial(k)
        for k in ks:
            cmoeff /= (k + 1)
        # all-diagonal: exps = (k_a+1 for a in A, kD+1)
        exps_diag = [k + 1 for k in ks] + [kD + 1]
        fact_prod_diag = 1
        for e in exps_diag:
            fact_prod_diag *= math.factorial(e)
        total += fact_r * cmoeff * fact_prod_diag
        # doubled-at-b terms, b=0..r-1
        for b in range(r):
            exps_b = [k + 1 for k in ks]
            exps_b[b] += 1  # k_b+2
            exps_b = exps_b + [kD]
            fact_prod_b = 1
            for e in exps_b:
                fact_prod_b *= math.factorial(e)
            total += fact_r * cmoeff * fact_prod_b
    return total


def W_closed(r, t):
    return (t + 2 * r + 1) * math.factorial(t + r)


def per_composition_all_diagonal(r, t, kD, ks):
    """Referee's claimed exact per-composition contribution of the
    ALL-DIAGONAL term: r! * t! * (kD+1). Verified against direct
    computation of that single term below."""
    return math.factorial(r) * math.factorial(t) * (kD + 1)


def per_composition_doubled(r, t, kD, ks, b):
    """Referee's claimed exact per-composition contribution of the
    DOUBLED-AT-b term: r! * t! * (k_b+2)."""
    return math.factorial(r) * math.factorial(t) * (ks[b] + 2)


if __name__ == "__main__":
    print("=" * 78)
    print("Part 1: per-composition exact contributions, symbolically checked")
    print("claim: all-diagonal term contributes EXACTLY r!*t!*(kD+1) per")
    print("composition; doubled-at-b term contributes EXACTLY r!*t!*(k_b+2).")
    print("(This is the referee's OWN re-derivation, done independently of")
    print(" the target's write-up, and checked here against direct")
    print(" per-composition monomial evaluation -- not assumed.)")
    print("=" * 78)
    fact_r_sym, t_sym, kD_sym = sp.symbols('r_fact t kD', positive=True)
    ka_sym = sp.symbols('ka', nonnegative=True)

    # symbolic check of the all-diagonal cancellation identity:
    # t!/(kD! * ka!) * 1/(ka+1) * (kD+1)! * (ka+1)!  ==  t! * (kD+1)   [for the single 'a' factor structure, generalized]
    kD_, ka_ = sp.symbols('kD ka', nonnegative=True, integer=True)
    lhs_allsingle = sp.factorial(kD_ + 1) / sp.factorial(kD_)  # the kD part of the cancellation
    print(f"  (kD+1)!/kD! symbolic simplify = {sp.simplify(lhs_allsingle)}  [should be kD+1]")
    lhs_a = sp.factorial(ka_ + 1) / (sp.factorial(ka_) * (ka_ + 1))
    print(f"  (ka+1)!/(ka!*(ka+1)) symbolic simplify = {sp.simplify(lhs_a)}  [should be 1]")
    lhs_b = sp.factorial(ka_ + 2) / (sp.factorial(ka_) * (ka_ + 1))
    print(f"  (kb+2)!/(kb!*(kb+1)) symbolic simplify = {sp.simplify(lhs_b)}  [should be kb+2]")
    print()

    print("=" * 78)
    print("Part 2: brute-force per-composition check, r=3, t=4 (all compositions)")
    print("comparing referee's formula r!*t!*(kD+1) / r!*t!*(kb+2) against the")
    print("EXACT per-term value computed directly from the raw monomial coeff")
    print("and factorial product (no shortcut).")
    print("=" * 78)
    r_test, t_test = 3, 4
    fact_r = math.factorial(r_test)
    all_match = True
    for comp in compositions(t_test, r_test + 1):
        ks = comp[:-1]
        kD = comp[-1]
        cmoeff = Fr(math.factorial(t_test))
        cmoeff /= math.factorial(kD)
        for k in ks:
            cmoeff /= math.factorial(k)
        for k in ks:
            cmoeff /= (k + 1)

        exps_diag = [k + 1 for k in ks] + [kD + 1]
        fp = 1
        for e in exps_diag:
            fp *= math.factorial(e)
        exact_diag = fact_r * cmoeff * fp
        claim_diag = per_composition_all_diagonal(r_test, t_test, kD, ks)
        ok1 = (exact_diag == claim_diag)
        all_match = all_match and ok1

        for b in range(r_test):
            exps_b = [k + 1 for k in ks]
            exps_b[b] += 1
            exps_b = exps_b + [kD]
            fp2 = 1
            for e in exps_b:
                fp2 *= math.factorial(e)
            exact_b = fact_r * cmoeff * fp2
            claim_b = per_composition_doubled(r_test, t_test, kD, ks, b)
            ok2 = (exact_b == claim_b)
            all_match = all_match and ok2
    print(f"r={r_test}, t={t_test}: all per-composition claims match exact computation: {all_match}")
    print()

    print("=" * 78)
    print("Part 3: summing the corrected per-composition formula over all N")
    print("compositions (N=C(t+r,r)), using the symmetry fact")
    print("sum_compositions(k_D) = sum_compositions(k_a) = t*N/(r+1),")
    print("and comparing to the closed form (t+2r+1)(t+r)! AND to the")
    print("target's literally-WRITTEN intermediate bracket formula")
    print("  r! * [(tN/(r+1)+N) + r*(tN/(r+1)+2N)]     <-- AS WRITTEN, no t!")
    print("to show this written formula is off by a factor of t! whenever")
    print("t!>1, while the CORRECTED version (with an extra explicit t!")
    print("factor, matching the r!*t!*(...) per-composition finding above)")
    print("matches exactly.")
    print("=" * 78)
    mismatch_as_written = 0
    match_corrected = 0
    n = 0
    for t in range(1, 8):
        for r in range(0, 8):
            n += 1
            N = math.comb(t + r, r)
            sumKD = Fr(t * N, r + 1)
            bracket = (sumKD + N) + r * (sumKD + 2 * N)
            as_written = math.factorial(r) * bracket          # missing t!
            corrected = math.factorial(r) * math.factorial(t) * bracket
            closed = W_closed(r, t)
            match_written = (as_written == closed)
            match_corr = (corrected == closed)
            if not match_written:
                mismatch_as_written += 1
            if match_corr:
                match_corrected += 1
            tag = "" if t > 1 else "  (t=1, t!=1, cannot distinguish)"
            print(f"t={t} r={r}: as-written={as_written} corrected={corrected} closed={closed} "
                  f"[written {'OK' if match_written else 'WRONG'}, corrected {'OK' if match_corr else 'WRONG'}]{tag}")
    print()
    print(f"Cells where the literally-WRITTEN bracket formula (no t!) disagrees "
          f"with the closed form: {mismatch_as_written}/{n}")
    print(f"Cells where the CORRECTED formula (extra t! reinstated) matches: "
          f"{match_corrected}/{n}")
    print()
    print("CONCLUSION: the target ATTEMPT.md Section 3.3's intermediate")
    print("'Summing over all N compositions' display formula, taken literally,")
    print("is off by a missing factor of t! (confirmed: disagrees with the true")
    print("W(r,t) for every t>=2 tested). The FINAL boxed closed form")
    print("(t+2r+1)(t+r)! is nonetheless CORRECT -- the very next equation in")
    print("the same box silently reinserts the missing t! (via an unexplained")
    print("'*t!' multiplied into N's own definition) and lands on the right")
    print("answer. This is a genuine exposition/rigor gap in Section 3.3 (a")
    print("dropped-then-silently-reinstated factor of t! in the middle of the")
    print("displayed derivation) -- but the CONCLUSION is independently correct,")
    print("confirmed here (a) by full re-derivation with the factor correctly")
    print("tracked throughout (Parts 1-3 above), and (b) by all 110 direct")
    print("numeric cells in adv1_W_fresh_definition.py, and (c) by the target's")
    print("own 99+32 cells. Does NOT affect the validity of Result 1 itself.")
