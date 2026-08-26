"""
Direct spot-check of the TARGET DOCUMENT's own printed p=41,b=0 closed
form (`printed_forms.log`, a plain-text DATA log -- not a .py file, so
reading it is within the task's discipline, exactly as the wave-18
referee hand-transcribed the wave-18 front's own printed p=21,b=0 form
from ATTEMPT.md prose). Rather than re-typing the ~40-term polynomial by
eye (error-prone at this size), this parses the two lines
(`coef(r) = ...`, `rem(r) = ...`) extracted verbatim via `sed` into
`_p41_b0_coef_raw.txt` / `_p41_b0_rem_raw.txt` (byte-identical to the
document's own file, not retyped) with a small regex parser, then
evaluates the resulting EXACT Fraction polynomial identity

    D^{*(41)}_r(0) = coef(r) * varphi_r + rem(r)

at several concrete r and compares against this referee's own
independent `ground_truth.D_star(41, r, 0)`.
"""
import re
from fractions import Fraction
from math import factorial

import ground_truth as gt

TERM_RE = re.compile(r"([+-])\s*\((\d+)/(\d+)\)\*r(?:\^(\d+))?")


def parse_poly(text):
    """
    Parse a string of the form
        coef(r) = (num/den)*r^41 + (num/den)*r^40 + ... + (num/den)*r^1
    (or `rem(r) = ...`, same shape, possibly starting with a leading
    '-' with no preceding '+') into a dict {power: Fraction}.
    """
    # Normalize: ensure there's a sign token before every term for the
    # regex, and strip the "coef(r) = " / "rem(r)  = " prefix.
    body = text.split("=", 1)[1].strip()
    if not body.startswith("+") and not body.startswith("-"):
        body = "+" + body
    coeffs = {}
    for m in TERM_RE.finditer(body):
        sign, num, den, power = m.groups()
        power = int(power) if power is not None else 1
        val = Fraction(int(num), int(den))
        if sign == "-":
            val = -val
        coeffs[power] = coeffs.get(power, Fraction(0)) + val
    return coeffs


def poly_eval(coeffs, r):
    total = Fraction(0)
    for power, c in coeffs.items():
        total += c * (Fraction(r) ** power)
    return total


def varphi(r):
    return Fraction(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


def run(log=print):
    with open("_p41_b0_coef_raw.txt") as f:
        coef_text = f.read()
    with open("_p41_b0_rem_raw.txt") as f:
        rem_text = f.read()

    coef_poly = parse_poly(coef_text)
    rem_poly = parse_poly(rem_text)

    log(f"parsed coef(r): {len(coef_poly)} nonzero terms, "
        f"degree {max(coef_poly)}")
    log(f"parsed rem(r):  {len(rem_poly)} nonzero terms, "
        f"degree {max(rem_poly)}")

    checks = 0
    fails = 0
    for r in [41, 45, 50, 75, 100, 150, 200]:
        coef_v = poly_eval(coef_poly, r)
        rem_v = poly_eval(rem_poly, r)
        printed_value = coef_v * varphi(r) + rem_v
        gt_value = gt.D_star(41, r, 0)
        checks += 1
        status = "OK" if printed_value == gt_value else "MISMATCH"
        if printed_value != gt_value:
            fails += 1
        log(f"r={r}: printed-form value == ground_truth.D_star(41,r,0)? {status}")
    log(f"spotcheck_printed_p41_b0: {checks} checks, {fails} fails")
    return checks, fails


if __name__ == "__main__":
    run()
