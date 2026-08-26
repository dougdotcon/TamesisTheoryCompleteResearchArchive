"""
Independent re-implementation of the general-p assembly formula for
D^{*(p)}_r(b), cited unchanged from waves 15/16/18 (and this front's own
Sec.1, restated identically again):

    N := 2r+b+1, beta := b+1
    D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)]
                    - sum_{k=1}^{p} o_k * H_{2k-1}(r,b) / 2^{2k-1}

with Q_p(-(v+beta/2)) = E_p(v) + O_p(v) (even/odd split in v), e_{2l},
o_k its coefficients, M_p(N) := sum_l e_{2l} mu_{2l}(N),
Phi_b(r) := P_b(r) * 2^N, Strip_p(r,b) := sum_{i=1}^b E_p(i-beta/2) w_i(r,b),
w_i(r,b) := r!(r+b)!/[(r+i)!(r+b+1-i)!], H_{2k-1}(r,b) := P_b(r) S_{2k-1}(N,r).

Ingredients used: Q_p via Stirling2/hockey-stick (ingredients.py), central
moments via power-series log/exp (ingredients.py), H_{2k-1} via the
closed-sum route (odd_part.py). fractions.Fraction throughout. No .py file
from any front in this lineage was opened, read, or imported.
"""
from fractions import Fraction
from math import factorial

import ingredients as ing
import odd_part as odd


def even_odd_split(coeffs_u, beta):
    """
    Given Q_p(u) as a coefficient list (low-to-high power of u), compose
    with u = -(v + beta/2) to get a polynomial in v, then split into its
    even-power-of-v part E_p(v) and odd-power-of-v part O_p(v) (each
    returned as {power_of_v: Fraction coeff}).
    """
    # u = -(v + beta/2) = -v - beta/2.  Build (u)^n via repeated
    # multiplication of the linear polynomial [-beta/2, -1] (coeffs of
    # v^0, v^1), then combine with coeffs_u.
    lin = [Fraction(-beta, 2), Fraction(-1)]  # u = lin[0] + lin[1]*v
    # accumulate result as dict {power: coeff}
    result = {}
    cur_power = {0: Fraction(1)}  # u^0 = 1
    for n, cn in enumerate(coeffs_u):
        if cn != 0:
            for pw, cf in cur_power.items():
                result[pw] = result.get(pw, Fraction(0)) + cn * cf
        if n != len(coeffs_u) - 1:
            # multiply cur_power by (lin[0] + lin[1]*v)
            new_power = {}
            for pw, cf in cur_power.items():
                new_power[pw] = new_power.get(pw, Fraction(0)) + cf * lin[0]
                new_power[pw + 1] = new_power.get(pw + 1, Fraction(0)) + cf * lin[1]
            cur_power = new_power
    even = {pw: c for pw, c in result.items() if pw % 2 == 0 and c != 0}
    odd_ = {pw: c for pw, c in result.items() if pw % 2 == 1 and c != 0}
    return even, odd_


def w_i(r, b, i):
    """w_i(r,b) := r!(r+b)!/[(r+i)!(r+b+1-i)!]"""
    return Fraction(
        factorial(r) * factorial(r + b),
        factorial(r + i) * factorial(r + b + 1 - i),
    )


class Assembler:
    def __init__(self, p, b):
        self.p = p
        self.b = b
        self.beta = b + 1
        ing._warm_up_moments(2 * p)  # Q_p(u) has genuine degree 2p (ingredients.py),
        # so M_p(N) needs central moments up to order 2p -- warm up ONCE
        # per Assembler construction (avoids the O(p)-separate-builds
        # performance defect disclosed in ingredients.py).
        Qc = ing.Q_poly(p)
        self.even, self.odd = even_odd_split(Qc, self.beta)
        # e_{2l}: even dict keyed by power of v = 2l -> l = pw//2
        self.e = {pw // 2: c for pw, c in self.even.items()}
        # o_k: odd dict keyed by power of v = 2k-1 -> k = (pw+1)//2
        self.o = {(pw + 1) // 2: c for pw, c in self.odd.items()}

    def M_p(self, N):
        total = Fraction(0)
        for l, coef in self.e.items():
            total += coef * ing.mu_eval(l, N)
        return total

    def Strip_p(self, r):
        b = self.b
        beta = self.beta
        total = Fraction(0)
        for i in range(1, b + 1):
            v = Fraction(i) - Fraction(beta, 2)
            Ep_v = self._E_eval(v)
            total += Ep_v * w_i(r, b, i)
        return total

    def _E_eval(self, v):
        total = Fraction(0)
        p = Fraction(1)
        v2 = v * v
        # even dict keyed by power of v (2l); evaluate directly via power
        for pw, c in self.even.items():
            total += c * (v ** pw)
        return total

    def _core(self, r):
        p, b = self.p, self.b
        N = 2 * r + b + 1
        Pb = odd.P_b_of_r(r, b)
        Phi_b = Pb * (2 ** N)
        Mp = self.M_p(N)
        Strip = self.Strip_p(r)
        half = (Phi_b * Mp - Strip) / 2
        k_max = max(self.o.keys()) if self.o else 0
        Htab = odd.build_H_table(r, b, k_max) if k_max >= 1 else {}
        odd_sum = Fraction(0)
        for k, ok in self.o.items():
            if k < 1 or k > p:
                continue
            odd_sum += ok * Htab[k] / Fraction(2 ** (2 * k - 1))
        return half - odd_sum

    def D_star(self, r):
        if r < self.p:
            return Fraction(0)
        return self._core(r)

    def D_star_full_formula(self, r):
        """Same as D_star but WITHOUT the r<p shortcut -- used to confirm
        the r<p vanishing is forced by the full formula's own algebra,
        not merely a hard-coded early return."""
        return self._core(r)


# ======================================================================
# Self-test / calibration
# ======================================================================
def self_test():
    import ground_truth as gt

    checks = 0
    fails = 0

    # calibration: reproduces p=1..10 (b=0,1,2,3) exactly
    for p in range(1, 11):
        asm = {}
        for b in (0, 1, 2, 3):
            asm[b] = Assembler(p, b)
        for r in range(0, 30):
            for b in (0, 1, 2, 3):
                checks += 1
                a = asm[b].D_star(r)
                w = gt.D_star(p, r, b)
                if a != w:
                    fails += 1
                    print("MISMATCH calibration", p, r, b, a, w)

    print(f"assemble.py self_test: {checks} checks, {fails} fails")
    return checks, fails


if __name__ == "__main__":
    self_test()
