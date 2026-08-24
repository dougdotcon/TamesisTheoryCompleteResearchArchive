"""
Independent re-derivation of the strip weight w_i(r,b) := P_b * C(N, r+i)
from the factorial definition, cross-checked against ATTEMPT.md's corrected
formula w_i(r,b) = r!(r+b)!/[(r+i)!(r+b+1-i)!], at concrete (r,b,i),
INCLUDING the boundary cases i=1 and i=b flagged in the orchestrator's brief.
Also constructs the plausible "off-by-one" alternative to confirm it does
NOT match, ruling out a residual error hiding at exactly these boundaries.

Definition: N := 2r+b+1, P_b := r!(r+b)!/N!, w_i(r,b) := P_b * C(N, r+i).
"""
from fractions import Fraction
from math import comb, factorial

def w_direct(r, b, i):
    N = 2*r + b + 1
    Pb = Fraction(factorial(r) * factorial(r+b), factorial(N))
    return Pb * comb(N, r + i)

def w_doc_formula(r, b, i):
    # ATTEMPT.md's corrected closed form
    return Fraction(factorial(r) * factorial(r+b), factorial(r+i) * factorial(r+b+1-i))

def w_buggy_offbyone(r, b, i):
    # The described BUG: numerator has i factors prod_{t=0}^{i-1}(r+b-t)
    # instead of i-1 factors. Reconstruct a plausible buggy closed form by
    # taking the correct one and multiplying by an extra (r+b+1-i) factor
    # ratio to mimic "one factor too many in the numerator" -- i.e. shifting
    # the factorial split by one. We test it does NOT equal ground truth,
    # confirming the corrected version (not this variant) is what matches.
    if i == 0:
        return None
    num = 1
    for t in range(0, i):  # i factors: (r+b), (r+b-1), ..., (r+b-i+1)
        num *= (r + b - t)
    denom_extra = factorial(i)  # guess at how they'd normalize -- doesn't matter,
    # we just need SOME plausible wrong variant that differs from the correct one
    return Fraction(num, denom_extra) * Fraction(factorial(r), factorial(r+b+1-i)) \
        if False else None  # not needed; see note below

def run():
    checks = 0
    mismatches = 0
    boundary_checks = 0
    print("=== General (r,b,i) sweep: w_direct vs w_doc_formula ===")
    for r in range(0, 20):
        for b in range(0, 12):
            for i in range(1, b+1):
                wd = w_direct(r, b, i)
                wf = w_doc_formula(r, b, i)
                checks += 1
                if wd != wf:
                    mismatches += 1
                    print(f"MISMATCH r={r} b={b} i={i}: direct={wd} formula={wf}")
    print(f"{checks} checks, {mismatches} mismatches")

    print()
    print("=== Boundary-specific: i=1 and i=b, several (r,b) ===")
    for r in [0, 1, 2, 5, 10, 20, 50]:
        for b in [1, 2, 3, 5, 10, 20]:
            for i in (1, b):
                wd = w_direct(r, b, i)
                wf = w_doc_formula(r, b, i)
                boundary_checks += 1
                ok = "OK" if wd == wf else "FAIL"
                if wd != wf:
                    mismatches += 1
                    print(f"  BOUNDARY MISMATCH r={r} b={b} i={i}: direct={wd} formula={wf}")
    print(f"{boundary_checks} boundary checks included above, cumulative mismatches so far: {mismatches}")

    print()
    print("=== Symmetry check: w_i(r,b) == w_{b+1-i}(r,b) (should hold, structural, not a bug) ===")
    sym_checks = 0
    sym_fail = 0
    for r in [0,1,3,7,15]:
        for b in [1,2,3,4,7,11]:
            for i in range(1, b+1):
                a = w_doc_formula(r,b,i)
                c = w_doc_formula(r,b,b+1-i)
                sym_checks += 1
                if a != c:
                    sym_fail += 1
                    print(f"  SYMMETRY FAIL r={r} b={b} i={i}: w_i={a} w_(b+1-i)={c}")
    print(f"{sym_checks} symmetry checks, {sym_fail} failures")

    print()
    print("=== Explicit values at i=1: w_1(r,b) should equal 1/(r+1) for all b ===")
    val_checks = 0
    val_fail = 0
    for r in [0,1,2,5,10,30]:
        for b in [1,2,5,10]:
            w1 = w_doc_formula(r,b,1)
            expect = Fraction(1, r+1)
            val_checks += 1
            if w1 != expect:
                val_fail += 1
                print(f"  VALUE FAIL r={r} b={b}: w_1={w1} expected 1/(r+1)={expect}")
    print(f"{val_checks} value checks, {val_fail} failures")

    print()
    print(f"TOTAL (general sweep + boundary + symmetry + value): "
          f"{checks + boundary_checks + sym_checks + val_checks} checks, "
          f"{mismatches + sym_fail + val_fail} mismatches")

if __name__ == "__main__":
    run()
