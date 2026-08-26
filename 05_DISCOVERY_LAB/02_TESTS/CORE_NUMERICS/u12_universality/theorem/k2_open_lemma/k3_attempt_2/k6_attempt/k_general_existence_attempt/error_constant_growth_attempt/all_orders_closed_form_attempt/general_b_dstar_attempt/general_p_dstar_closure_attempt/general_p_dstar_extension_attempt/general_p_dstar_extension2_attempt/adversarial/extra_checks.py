"""
Referee's supplementary checks, bundled into one script for
reproducibility:

  (1) Q_p(-1) = 0 for p = 1,...,60 (the target document's Sec.2.4 claim,
      tested with the referee's own from-scratch Q_p implementation).
  (2) The degree bound deg_r H_{2k-1}(r,b) = k-1, leading coefficient
      4^{k-1}(k-1)!, re-checked here for k = 1,...,45 (matching the
      target document's own claimed re-check range), several b values.
  (3) Structural vanishing of Strip_p(r,1) via E_p(0) = Q_p(-1), for
      every p = 21,...,40, using the assembler's own machinery (a second,
      independent route to the same Q_p(-1)=0 fact).
  (4) The r<p region genuinely comes out to ZERO via the FULL assembly
      formula (not a hard-coded shortcut) -- i.e. the empty-Corollary-A3
      -sum boundary is forced by the formula's own algebra, exactly as
      claimed by the target document (and every predecessor).
  (5) A deterministic, non-random, hand-chosen spot-check reaching into
      the reduced-scale p=41,...,60 region.

Written fresh by the referee. No predecessor .py file was read or used.
"""
import math
import time
from fractions import Fraction

from ingredients import Q_poly, poly_eval
from assemble import Assembler
from odd_part import H_odd_fast
from ground_truth import D_star as gt_D_star


def check_Q_p_minus_1(p_max=60):
    checks = 0
    fails = 0
    for p in range(1, p_max + 1):
        v = poly_eval(Q_poly(p), Fraction(-1))
        checks += 1
        if v != 0:
            fails += 1
            print("FAIL Q_p(-1) != 0 at p=", p, v)
    print(f"(1) Q_p(-1)=0 for p=1..{p_max}: {checks} checks, {fails} fails")
    return checks, fails


def finite_diff(vals, order):
    v = list(vals)
    for _ in range(order):
        v = [v[i + 1] - v[i] for i in range(len(v) - 1)]
    return v


def check_degree_bound(k_max=45, b_values=(0, 1, 3, 7, 30)):
    checks = 0
    fails = 0
    for k in range(1, k_max + 1):
        for b in b_values:
            npts = k + 2
            r0 = 5
            vals = [H_odd_fast(k, r, b)[k] for r in range(r0, r0 + npts)]
            fd = finite_diff(vals, k - 1)
            lead = fd[0] / math.factorial(k - 1)
            want = Fraction(4 ** (k - 1) * math.factorial(k - 1))
            checks += 1
            if lead != want:
                fails += 1
                print("FAIL degree-bound leading coeff k,b=", k, b, lead, want)
    print(f"(2) degree bound k=1..{k_max}, b in {b_values}: {checks} checks, {fails} fails")
    return checks, fails


def check_strip_b1_vanishing(p_lo=21, p_hi=40):
    asm = Assembler()
    checks = 0
    fails = 0
    for p in range(p_lo, p_hi + 1):
        e_list, o_list, composed = asm.e_o_lists(p, 1)  # b=1, beta=2
        x = Fraction(1) - Fraction(2, 2)  # i=1, beta=2 -> x = 0
        Ep0 = asm.E_p_eval(e_list, x)
        checks += 1
        if Ep0 != 0:
            fails += 1
            print("FAIL Strip_p(r,1) structural nonzero at p=", p, Ep0)
    print(f"(3) Strip_p(r,1) vanishing (E_p(0)=Q_p(-1)) p={p_lo}..{p_hi}: {checks} checks, {fails} fails")
    return checks, fails


def check_r_lt_p_forced_zero(p_values=(21, 25, 30, 35, 40), b_values=(0, 1, 2, 5)):
    asm = Assembler()
    checks = 0
    fails = 0
    for p in p_values:
        for r in range(0, p):
            for b in b_values:
                N = 2 * r + b + 1
                beta = b + 1
                Pb = Fraction(math.factorial(r) * math.factorial(r + b), math.factorial(N))
                e_list, o_list, _ = asm.e_o_lists(p, b)
                from ingredients import mu_2l_fast
                Mp = sum((c * mu_2l_fast(l, N) for l, c in e_list.items() if c != 0), Fraction(0))
                Phi_b = Pb * Fraction(2 ** N)
                strip = Fraction(0)
                for i in range(1, b + 1):
                    x = Fraction(i) - Fraction(beta, 2)
                    Ep_x = asm.E_p_eval(e_list, x)
                    w_i = Fraction(math.factorial(r) * math.factorial(r + b),
                                    math.factorial(r + i) * math.factorial(r + b + 1 - i))
                    strip += Ep_x * w_i
                max_k = max(o_list.keys()) if o_list else 0
                odd_sum = Fraction(0)
                if max_k > 0:
                    Ht = H_odd_fast(max_k, r, b)
                    for k, ok in o_list.items():
                        if ok == 0:
                            continue
                        odd_sum += ok * Ht[k] / Fraction(2 ** (2 * k - 1))
                full_formula_result = Fraction(1, 2) * (Phi_b * Mp - strip) - odd_sum
                checks += 1
                if full_formula_result != 0:
                    fails += 1
                    print("FAIL r<p full-formula nonzero p,r,b=", p, r, b, full_formula_result)
    print(f"(4) r<p region forced to zero by the FULL formula (not a shortcut), "
          f"p in {p_values}, b in {b_values}: {checks} checks, {fails} fails")
    return checks, fails


def check_p41_60_targeted():
    t0 = time.time()
    checks = 0
    fails = 0
    for p in range(41, 61):
        asm = Assembler()
        for b in [0, 1, 3, 5, 10]:
            for r in [p, p + 1, p + 5, p + 20, p + 40]:
                got = asm.D_star(p, r, b)
                want = gt_D_star(p, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    print("FAIL p41-60 targeted p,r,b=", p, r, b, got, want)
    t1 = time.time()
    print(f"(5) p=41..60 deterministic targeted spot-check: {checks} checks, {fails} fails, {t1 - t0:.1f}s")
    return checks, fails


if __name__ == "__main__":
    total_checks = 0
    total_fails = 0
    for fn in [check_Q_p_minus_1, check_degree_bound, check_strip_b1_vanishing,
               check_r_lt_p_forced_zero, check_p41_60_targeted]:
        c, f = fn()
        total_checks += c
        total_fails += f
    print(f"TOTAL extra_checks: {total_checks} checks, {total_fails} fails")
