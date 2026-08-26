"""
Independent, from-scratch implementation of the assembly formula for
D^{*(p)}_r(b), as reproduced verbatim (cited, unchanged since wave 15)
in the target document's Sec.1 / the task mandate's step 6:

  N := 2r+b+1,  beta := b+1

  D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)]
                  - sum_{k=1}^{p} o_k H_{2k-1}(r,b) / 2^{2k-1}

  Q_p(-(v+beta/2)) = E_p(v) + O_p(v)     (even/odd split in v)
  e_{2l} := coeff of v^{2l} in E_p        o_k := coeff of v^{2k-1} in O_p
  M_p(N) := sum_l e_{2l} mu_{2l}(N)
  Phi_b(r) := P_b 2^N,   P_b := r!(r+b)!/N!
  Strip_p(r,b) := sum_{i=1}^b E_p(i - beta/2) w_i(r,b)
  w_i(r,b) := r!(r+b)!/[(r+i)!(r+b+1-i)!]
  H_{2k-1}(r,b) := P_b S_{2k-1}(N,r)

Written fresh by the referee, using ingredients.py (Q_p, mu_{2l}) and
odd_part.py (H_{2k-1}) -- both written fresh by the referee, no
predecessor .py file read or used anywhere.
"""
from fractions import Fraction
import math

from ingredients import Q_poly, mu_2l_fast, poly_eval
from odd_part import H_odd_fast
from ground_truth import D_star as gt_D_star


def poly_compose_linear(poly, a, b_):
    """Compose poly(x) with x = a + b_*t, i.e. return poly(a + b_*t) as a
    polynomial in t. poly is a list of Fraction coefficients (index =
    power). a, b_ are Fraction/int constants."""
    # linear term (a + b_*t)
    lin = [Fraction(a), Fraction(b_)]
    result = [Fraction(0)]
    power = [Fraction(1)]  # lin^0
    for m, c in enumerate(poly):
        if c != 0:
            term = [c * x for x in power]
            # add term into result
            if len(term) > len(result):
                result = result + [Fraction(0)] * (len(term) - len(result))
            for i, v in enumerate(term):
                result[i] += v
        if m != len(poly) - 1:
            # power *= lin
            new_power = [Fraction(0)] * (len(power) + 1)
            for i, pv in enumerate(power):
                if pv == 0:
                    continue
                new_power[i] += pv * lin[0]
                new_power[i + 1] += pv * lin[1]
            power = new_power
    return result


def factorial(n):
    return math.factorial(n)


class Assembler:
    def __init__(self):
        self._pb_cache = {}

    def e_o_lists(self, p, b):
        """Returns (e_list, o_list): e_list[l] = e_{2l} for l=0..p, and
        o_list[k] = o_k for k=1..p (both zero-padded), by composing
        Q_p(u) with u = -(v + beta/2) and splitting by parity."""
        key = (p, b)
        if key in self._pb_cache:
            return self._pb_cache[key]
        beta = b + 1
        qp = Q_poly(p)
        composed = poly_compose_linear(qp, Fraction(-beta, 2), Fraction(-1))
        # composed[i] = coefficient of v^i in Q_p(-(v+beta/2))
        e_list = {}
        o_list = {}
        for i, c in enumerate(composed):
            if i % 2 == 0:
                e_list[i // 2] = c
            else:
                o_list[(i + 1) // 2] = c
        self._pb_cache[key] = (e_list, o_list, composed)
        return e_list, o_list, composed

    def E_p_eval(self, e_list, x):
        """Evaluate E_p(x) = sum_l e_{2l} x^{2l}."""
        total = Fraction(0)
        for l, c in e_list.items():
            if c == 0:
                continue
            total += c * (x ** (2 * l))
        return total

    def D_star(self, p, r, b):
        if r < p:
            return Fraction(0)
        N = 2 * r + b + 1
        beta = b + 1
        Pb = Fraction(factorial(r) * factorial(r + b), factorial(N))

        e_list, o_list, _composed = self.e_o_lists(p, b)

        # M_p(N)
        Mp = Fraction(0)
        for l, c in e_list.items():
            if c == 0:
                continue
            Mp += c * mu_2l_fast(l, N)

        Phi_b = Pb * Fraction(2 ** N)

        # Strip_p(r,b)
        strip = Fraction(0)
        for i in range(1, b + 1):
            x = Fraction(i) - Fraction(beta, 2)
            Ep_x = self.E_p_eval(e_list, x)
            w_i = Fraction(factorial(r) * factorial(r + b),
                            factorial(r + i) * factorial(r + b + 1 - i))
            strip += Ep_x * w_i

        # odd-part sum
        max_k = max(o_list.keys()) if o_list else 0
        odd_sum = Fraction(0)
        if max_k > 0:
            H_table = H_odd_fast(max_k, r, b)
            for k, ok in o_list.items():
                if ok == 0:
                    continue
                odd_sum += ok * H_table[k] / Fraction(2 ** (2 * k - 1))

        result = Fraction(1, 2) * (Phi_b * Mp - strip) - odd_sum
        return result


# ---------------------------------------------------------------------
# Self tests: calibration against ground_truth.D_star for small p,b
# (sanity gate before trusting the p=21..40 sweep).
# ---------------------------------------------------------------------

def calibration_self_test():
    asm = Assembler()
    checks = 0
    fails = 0
    for p in range(1, 11):
        for b in [0, 1, 2, 3]:
            for r in range(0, 30):
                got = asm.D_star(p, r, b)
                want = gt_D_star(p, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    print("FAIL calibration p,r,b=", p, r, b, got, want)
    print(f"assemble.py calibration_self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok = calibration_self_test()
    print("assemble.py calibration:", "OK" if ok else "FAILED")
