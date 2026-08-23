"""
Cross-check: the background REFEREE_REPORT's Teorema 3' (p=2 case, PROVED by
a prior referee, error_constant_growth_attempt/adversarial/REFEREE_REPORT.md
Part 3.3, lines 288-320) transcribed EXACTLY as printed, verified against
OWN ground truth (Corollary A3, own Stirling table) -- and, separately,
confirmed to numerically coincide with this front's independently-assembled
p=2 formula (assembled.py's D_assembled(2,r,b)), since both should equal the
same ground truth.
"""
from fractions import Fraction
from own_ground_truth import D_star, varphi, fact
from assembled import D_assembled


def phi(r):
    return varphi(r)


def Phi_b(r, b):
    """Phi_b(r) := 2*varphi_r * prod_{j=1}^b (2r+2j)/(2r+j+1)"""
    val = 2 * phi(r)
    for j in range(1, b + 1):
        val *= Fraction(2 * r + 2 * j, 2 * r + j + 1)
    return val


def E_func(v, beta):
    """E(v) := 3v^4 + (9/2 beta^2 - 3beta - 3) v^2
              + 3/16 beta^4 - 1/4 beta^3 - 3/4 beta^2 + beta"""
    v = Fraction(v)
    beta = Fraction(beta)
    return (3 * v ** 4
            + (Fraction(9, 2) * beta ** 2 - 3 * beta - 3) * v ** 2
            + Fraction(3, 16) * beta ** 4 - Fraction(1, 4) * beta ** 3
            - Fraction(3, 4) * beta ** 2 + beta)


def teorema3prime(r, b):
    N = 2 * r + b + 1
    beta = b + 1
    Phib = Phi_b(r, b)
    bracket = (Fraction(3 * N * (3 * N - 2), 16)
               + (Fraction(9, 2) * beta ** 2 - 3 * beta - 3) * Fraction(N, 4)
               + Fraction(3, 16) * beta ** 4 - Fraction(1, 4) * beta ** 3
               - Fraction(3, 4) * beta ** 2 + beta)
    term1 = Fraction(Phib, 48) * bracket

    strip = Fraction(0)
    for j in range(1, b + 1):
        Ev = E_func(Fraction(j) - Fraction(beta, 2), beta)
        w_j = Fraction(fact(r) * fact(r + b), fact(r + j) * fact(r + b + 1 - j))
        strip += Ev * w_j
    term2 = Fraction(1, 48) * strip

    term3 = Fraction((3 * b + 2) * r, 24)
    term4 = Fraction(b * (3 * b + 1) * (b + 2), 48)

    return term1 - term2 - term3 - term4


def sweep(r_max, b_max):
    fails_gt = 0
    fails_cross = 0
    checks = 0
    for r in range(0, r_max + 1):
        for b in range(0, b_max + 1):
            t3p = teorema3prime(r, b)
            gt = D_star(2, r, b)
            checks += 1
            if t3p != gt:
                fails_gt += 1
                print(f"FAIL Teorema3' vs ground truth r={r} b={b}: {t3p} vs {gt}")
            asm = D_assembled(2, r, b)
            if t3p != asm:
                fails_cross += 1
                print(f"FAIL Teorema3' vs this-front's assembled p=2 r={r} b={b}: {t3p} vs {asm}")
    print(f"sweep(r_max={r_max}, b_max={b_max}): {checks} checks, "
          f"{fails_gt} vs-ground-truth failures, {fails_cross} vs-assembled failures")
    return fails_gt + fails_cross


if __name__ == "__main__":
    f = sweep(r_max=100, b_max=20)
    print(f"TOTAL FAILURES: {f}")
