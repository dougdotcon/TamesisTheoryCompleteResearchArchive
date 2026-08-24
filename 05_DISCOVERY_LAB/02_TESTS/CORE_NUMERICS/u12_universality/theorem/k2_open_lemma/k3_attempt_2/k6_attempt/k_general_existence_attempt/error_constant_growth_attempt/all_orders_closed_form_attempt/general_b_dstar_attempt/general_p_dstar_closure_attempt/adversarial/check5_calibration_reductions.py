"""
Independent re-verification of several of ATTEMPT.md's Section 3.1
calibration-reduction table entries, chosen as most likely to hide a
transcription error (highest-degree polynomials): p=4,b=1 (the most
complex one in the table), plus p=3,b=1 and p=2,b=3 (a b>=2 case with the
(2r+3) denominator pattern) as additional spot-checks.

Method: evaluate the document's PRINTED closed form (transcribed here by
hand from ATTEMPT.md Section 3.1, char for char) at many concrete integer
r, using the exact rational value of varphi_r = 4^r (r!)^2/(2r+1)!, and
compare against Corollary A3 ground truth (own from-scratch Stirling
table, independent of ground_truth.py).
"""
from fractions import Fraction
from math import factorial

def stirling1_table(nmax):
    c = [[0]*(nmax+1) for _ in range(nmax+1)]
    c[0][0] = 1
    for n in range(1, nmax+1):
        for k in range(0, n+1):
            c[n][k] = c[n-1][k-1] if k-1 >= 0 else 0
            c[n][k] += (n-1)*c[n-1][k] if k <= n-1 else 0
    return c

def D_ground_truth(p, r, b, c):
    total = Fraction(0)
    for j in range(p, r+1):
        M = j+1-p
        stirl = c[j+1][M]
        if stirl == 0:
            continue
        num = Fraction(factorial(r), factorial(r-j))
        denom = 1
        for i in range(1, j+2):
            denom *= (r+b+i)
        cj = num / denom
        total += cj * stirl
    return total

def varphi_r(r):
    return Fraction(4**r * factorial(r)**2, factorial(2*r+1))

def formula_p4_b1(r):
    # (r+1)(105 r^3 + 1765 r^2 + 3314 r + 1536)/6144 * varphi_r
    #  - (45 r^3 + 229 r^2 + 306 r + 120)/480
    coef = Fraction((r+1)*(105*r**3 + 1765*r**2 + 3314*r + 1536), 6144)
    rem = Fraction(45*r**3 + 229*r**2 + 306*r + 120, 480)
    return coef*varphi_r(r) - rem

def formula_p3_b1(r):
    # (r+1)(5 r^2 + 39 r + 32)/128 * varphi_r - (r+1)(7r+12)/48
    coef = Fraction((r+1)*(5*r**2 + 39*r + 32), 128)
    rem = Fraction((r+1)*(7*r+12), 48)
    return coef*varphi_r(r) - rem

def formula_p2_b3(r):
    # (r+3)(3 r^2 + 49 r + 118)/(16(2r+3)) * varphi_r
    #  - (r+3)(11 r^2 + 75 r + 118)/(24 (r+1)(r+2))
    coef = Fraction((r+3)*(3*r**2 + 49*r + 118), 16*(2*r+3))
    rem = Fraction((r+3)*(11*r**2 + 75*r + 118), 24*(r+1)*(r+2))
    return coef*varphi_r(r) - rem

def run():
    c_table = stirling1_table(300)
    tests = [
        ("p=4,b=1", 4, 1, formula_p4_b1),
        ("p=3,b=1", 3, 1, formula_p3_b1),
        ("p=2,b=3", 2, 3, formula_p2_b3),
    ]
    total = 0
    total_fail = 0
    for name, p, b, f in tests:
        ok = 0
        fail = 0
        for r in range(0, 250):
            gt = D_ground_truth(p, r, b, c_table)
            fv = f(r)
            if gt == fv:
                ok += 1
            else:
                fail += 1
                if fail <= 5:
                    print(f"  MISMATCH {name} r={r}: ground_truth={gt} formula={fv}")
        print(f"{name}: r=0..249, {ok} match, {fail} mismatch")
        total += ok + fail
        total_fail += fail
    print(f"TOTAL: {total} checks, {total_fail} mismatches")

if __name__ == "__main__":
    run()
