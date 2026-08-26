"""
print_closed_forms.py -- prints and cross-validates the b=0,1 closed forms
for p=41,...,80 (new, previously-unprinted in this lineage), pure
polynomials in r (no denominator), via assemble.printed_form_b0/b1.
"""
from fractions import Fraction

from ingredients import Q_poly, poly_eval
from assemble import printed_form_b0, printed_form_b1, varphi
from ground_truth import D_star as ground_truth_D_star
from odd_part import build_A_table


def poly_str(coeffs, var="r"):
    """coeffs ascending Fraction list -> human-readable string, descending
    powers."""
    terms = []
    for i in range(len(coeffs) - 1, -1, -1):
        c = coeffs[i]
        if c == 0:
            continue
        sign = "-" if c < 0 else "+"
        mag = abs(c)
        if i == 0:
            term = f"({mag})"
        elif i == 1:
            term = f"({mag})*{var}"
        else:
            term = f"({mag})*{var}^{i}"
        terms.append((sign, term))
    if not terms:
        return "0"
    out = terms[0][1] if terms[0][0] == "+" else f"-{terms[0][1]}"
    for sign, term in terms[1:]:
        out += f" {sign} {term}"
    return out


def run(p_lo=41, p_hi=80, log=True):
    build_A_table(p_hi)
    total_checks = 0
    total_fails = 0
    q_neg1_checks = 0
    q_neg1_fails = 0

    lines = []
    for p in range(p_lo, p_hi + 1):
        # Q_p(-1) = 0 check (justifies the b=1 clean form; also structurally
        # relevant to b=0 since Strip_p(r,0) is trivially empty regardless).
        qm1 = poly_eval(Q_poly(p), Fraction(-1))
        q_neg1_checks += 1
        if qm1 != 0:
            q_neg1_fails += 1
            print(f"Q_{p}(-1) != 0: {qm1}")

        coef0, rem0 = printed_form_b0(p)
        coef1, rem1 = printed_form_b1(p)

        # Cross-validate both printed forms against ground truth at five
        # concrete r values.
        for r in (0, 5, 17, 50, 150):
            if r < p:
                continue
            want0 = ground_truth_D_star(p, r, 0)
            got0 = poly_eval(coef0, Fraction(r)) * varphi(r) + poly_eval(rem0, Fraction(r))
            total_checks += 1
            if got0 != want0:
                total_fails += 1
                print(f"MISMATCH printed b=0 p={p} r={r}: {got0} vs {want0}")

            want1 = ground_truth_D_star(p, r, 1)
            got1 = poly_eval(coef1, Fraction(r)) * varphi(r) + poly_eval(rem1, Fraction(r))
            total_checks += 1
            if got1 != want1:
                total_fails += 1
                print(f"MISMATCH printed b=1 p={p} r={r}: {got1} vs {want1}")

        lines.append(f"p={p}, b=0:")
        lines.append(f"  coef(r) = {poly_str(coef0)}")
        lines.append(f"  rem(r)  = {poly_str(rem0)}")
        lines.append(f"p={p}, b=1:")
        lines.append(f"  coef(r) = {poly_str(coef1)}")
        lines.append(f"  rem(r)  = {poly_str(rem1)}")
        lines.append("")

    if log:
        print(f"Q_p(-1)=0 check: p={p_lo}..{p_hi}: {q_neg1_checks} checks, {q_neg1_fails} fails")
        print(f"printed-form cross-validation: {total_checks} checks, {total_fails} fails")

    return lines, total_checks, total_fails, q_neg1_checks, q_neg1_fails


if __name__ == "__main__":
    lines, checks, fails, qc, qf = run()
    with open("printed_forms.log", "w") as f:
        f.write("\n".join(lines))
    print(f"Wrote {len(lines)} lines to printed_forms.log")
    ok = fails == 0 and qf == 0
    print("print_closed_forms.py: OK" if ok else "print_closed_forms.py: FAILED")
