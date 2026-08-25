# Hostile-referee check 4 (extension front): the PRINTED closed forms.
# Reads the front's assemble_ext.log (reading printed *output* is allowed by the
# discipline; the front's .py files were never read) and verifies every printed
# closed form -- all 20 (p=11..20, b=0,1) plus all 6 (p in {11,15,20}, b=2,3) --
# numerically against this referee's OWN Corollary A3 ground truth at
# r = 0..60 and r in {150, 200, 300}.  varphi_r = 4^r (r!)^2 / (2r+1)!.
# Also: the ATTEMPT.md hand-typeset p=11 forms (b=0,1,2) are checked against the
# log's machine-printed forms by ordered-integer-sequence comparison (catches any
# transcription slip in a coefficient, exponent, or denominator).
# Exact arithmetic only. No randomness.

from fractions import Fraction
from math import factorial
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref_ground_truth as gt

LOG = os.path.join(HERE, "..", "assemble_ext.log")
ATTEMPT = os.path.join(HERE, "..", "ATTEMPT.md")

rsym = sp.Symbol("r")


def parse_log_forms():
    """-> {(p,b): (coeff_expr, rem_expr)} from assemble_ext.log printed blocks."""
    with open(LOG) as fh:
        lines = fh.readlines()
    forms = {}
    i = 0
    hdr = re.compile(r"^p=(\d+), b=(\d+):\s*$")
    while i < len(lines):
        m = hdr.match(lines[i])
        if m:
            p, b = int(m.group(1)), int(m.group(2))
            c_line = lines[i + 1]
            r_line = lines[i + 2]
            assert "varphi_r coeff =" in c_line and "remainder" in r_line, (p, b)
            cexpr = sp.sympify(c_line.split("=", 1)[1].strip(), locals={"r": rsym})
            rexpr = sp.sympify(r_line.split("=", 1)[1].strip(), locals={"r": rsym})
            forms[(p, b)] = (cexpr, rexpr)
            i += 3
        else:
            i += 1
    return forms


def eval_form(cexpr, rexpr, r):
    # NOTE: deliberately no sp.nsimplify anywhere in this referee suite -- the
    # substituted values below are exact sympy Rationals by construction, which
    # is precisely the lesson of the front's own disclosed section-2.4 bug.
    c = cexpr.subs(rsym, sp.Integer(r))
    rm = rexpr.subs(rsym, sp.Integer(r))
    assert c.is_Rational and rm.is_Rational
    phi = Fraction(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))
    return Fraction(int(c.p), int(c.q)) * phi + Fraction(int(rm.p), int(rm.q))


def digit_runs(s):
    return re.findall(r"\d+", s)


def attempt_vs_log_p11():
    """Ordered-integer-sequence comparison, ATTEMPT.md's p=11 printed block vs log."""
    with open(ATTEMPT) as fh:
        txt = fh.read()
    # the printed p=11 block in section 3.3: six display lines
    start = txt.index("D^{*(11)}_r(0)")
    end = txt.index("Every `b=0,1` instance")
    block = txt[start:end]
    att_runs = digit_runs(block)

    with open(LOG) as fh:
        log_txt = fh.read()
    log_blocks = []
    for key in ["p=11, b=0:", "p=11, b=1:", "p=11, b=2:"]:
        s = log_txt.index(key)
        e = log_txt.index("p=1", s + 4)  # next p=11/p=12 header
        log_blocks.append(log_txt[s:e])
    log_runs = []
    for lb in log_blocks:
        log_runs.extend(digit_runs(lb))
    return att_runs, log_runs


def main():
    forms = parse_log_forms()
    print(f"parsed {len(forms)} printed closed forms from assemble_ext.log: "
          f"{sorted(forms)}")
    expect = {(p, b) for p in range(11, 21) for b in (0, 1)} | \
             {(p, b) for p in (11, 15, 20) for b in (2, 3)}
    assert set(forms) == expect, set(forms) ^ expect

    checks = fails = 0
    rvals = list(range(0, 61)) + [150, 200, 300]
    for (p, b), (cexpr, rexpr) in sorted(forms.items()):
        bad = 0
        for r in rvals:
            got = eval_form(cexpr, rexpr, r)
            want = gt.D_star(p, r, b)
            checks += 1
            if got != want:
                fails += 1
                bad += 1
                print(f"  MISMATCH p={p} b={b} r={r}")
        print(f"log form p={p:2d} b={b}: {len(rvals)} r-values "
              f"(0..60,150,200,300) vs referee A3 -> {'OK' if bad == 0 else 'FAIL'}")
    print(f"printed-form numeric verification: {checks} checks, fails={fails}")
    assert fails == 0

    att_runs, log_runs = attempt_vs_log_p11()
    same = att_runs == log_runs
    print(f"ATTEMPT.md p=11 printed block vs log (ordered integer sequences): "
          f"{len(att_runs)} vs {len(log_runs)} tokens, identical={same}")
    if not same:
        # print first divergence for the report
        for i, (a, l) in enumerate(zip(att_runs, log_runs)):
            if a != l:
                print(f"  first divergence at token {i}: ATTEMPT={a} log={l}")
                break
        if len(att_runs) != len(log_runs):
            print("  (length mismatch)")
    assert same
    print("ALL PRINTED-FORM CHECKS PASSED")


if __name__ == "__main__":
    main()
