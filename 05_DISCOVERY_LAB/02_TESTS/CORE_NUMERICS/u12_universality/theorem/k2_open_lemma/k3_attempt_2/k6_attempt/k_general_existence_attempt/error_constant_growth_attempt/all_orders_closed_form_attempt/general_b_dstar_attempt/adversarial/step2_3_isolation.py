"""
Isolates Step 2 (substitution u=-(v+beta/2)) + Step 3 (even/odd split +
reflection collapse of the even part into full-symmetric-sum minus strip)
from Step 4 (the Pcollapse machinery for the odd part), by comparing:

  raw_target(p,r,b) := sum_{alpha=0}^r Q_p(r-alpha) C(N,alpha)      [Step-1 form]

against

  (1/2)*(FullEvenSum - StripEvenSum) + OddSumRaw(direct, NOT via Pcollapse)

If these match, Steps 2-3 are correct independent of whether Step 4's
recursive collapse (verified separately in full_rederivation.py /
assembled.py) is correct.
"""
from fractions import Fraction
import sympy as sp

from full_rederivation import Q_p_direct, binom_conv
from assembled import get_p_data, full_even_sum, strip_even_sum, beta_sym


def raw_target(p, r, b):
    N = 2 * r + b + 1
    total = Fraction(0)
    for alpha in range(0, r + 1):
        u = r - alpha
        total += Fraction(Q_p_direct(p, u)) * binom_conv(N, alpha)
    return total


def odd_sum_raw_direct(p, r, b, oc):
    N = 2 * r + b + 1
    beta_val = b + 1
    total = Fraction(0)
    for alpha in range(0, r + 1):
        vv = Fraction(2 * alpha - N, 2)
        Oval = Fraction(0)
        for k, co in oc.items():
            coeff = sp.Rational(co.subs(beta_sym, beta_val))
            Oval += Fraction(coeff.p, coeff.q) * vv ** (2 * k - 1)
        total += Oval * binom_conv(N, alpha)
    return total


def sweep(r_max, b_max):
    fails = 0
    checks = 0
    for p in [1, 2, 3, 4]:
        ec, oc = get_p_data(p)
        for r in range(0, r_max + 1):
            for b in range(0, b_max + 1):
                N = 2 * r + b + 1
                beta_val = b + 1
                fes = full_even_sum(p, N, beta_val, ec)
                fes_frac = Fraction(sp.Rational(fes).p, sp.Rational(fes).q)
                ses = strip_even_sum(r, b, ec, N, beta_val)
                osraw = odd_sum_raw_direct(p, r, b, oc)
                reconstructed = Fraction(1, 2) * (fes_frac - ses) + osraw
                target = raw_target(p, r, b)
                checks += 1
                if reconstructed != target:
                    fails += 1
                    print(f"FAIL step2/3 isolation p={p} r={r} b={b}: "
                          f"{reconstructed} vs {target}")
    print(f"step2_3_isolation sweep(r_max={r_max}, b_max={b_max}): "
          f"{checks} checks, {fails} failures")
    return fails


if __name__ == "__main__":
    f = sweep(r_max=30, b_max=15)
    print(f"TOTAL FAILURES: {f}")
