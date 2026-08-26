"""
assemble.py -- the full D^{*(p)}_r(b) assembly, written FRESH for this front
(no predecessor .py file opened, read, or imported).

Cited, PROVED assembly formula (reproduced unchanged across waves 15/16/18,
THEOREM.md "Estagio 16"/"Estagio 21"/"Estagio 29";
general_p_dstar_extension2_attempt/ATTEMPT.md Sec.1):

  N := 2r+b+1,  beta := b+1

  D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)]
                  - sum_{k=1}^{p} o_k H_{2k-1}(r,b) / 2^{2k-1}

  Q_p(-(v+beta/2)) = E_p(v) + O_p(v)     (even/odd split in v)
  e_{2l} := coeff of v^{2l} in E_p(v)   (l=0,...,floor(p/2))
  o_k    := coeff of v^{2k-1} in O_p(v) (k=1,...,ceil(p/2), padded with 0)
  M_p(N) := sum_l e_{2l} mu_{2l}(N)
  Phi_b(r) := P_b(r) * 2^N
  Strip_p(r,b) := sum_{i=1}^{b} E_p(i - beta/2) * w_i(r,b)
  w_i(r,b) := r!(r+b)! / [(r+i)!(r+b+1-i)!]
  H_{2k-1}(r,b) := P_b(r) * S_{2k-1}(N,r)

P_b(r), the one symbol the cited formula uses without spelling out its
explicit form inline, is pinned down here from the ALSO-cited elementary
identity `P_b * C(N,r+1) = 1/(r+1)` (ATTEMPT.md Sec.2.3 /
general_p_dstar_extension2_attempt/ATTEMPT.md line 288): since
C(N,r+1) = N!/[(r+1)!(r+b)!] (N-r-1=r+b), this identity forces

    P_b(r) = r!(r+b)! / N!,   N = 2r+b+1

-- this was cross-checked directly against Teorema 3 (THEOREM.md
"Estagio 8": D^*_r(0) := lim_n max_m n^2|R_r| = r(3r+1)/32 varphi_r - r/12,
varphi_r = 4^r(r!)^2/(2r+1)!) via ground_truth.D_star, see ATTEMPT.md Sec.5
for the disclosed mis-indexing this uncovered (D^*_r(0) is D^{*(2)}_r(0),
not D^{*(1)}_r(0) -- p=2, the order-1/n^2 term).
"""
from fractions import Fraction
import math

from ingredients import (
    Q_poly, mu_poly, poly_eval, poly_compose_linear, poly_scale, warm_up_moments,
)
from odd_part import build_H_table
from ground_truth import D_star as ground_truth_D_star


def even_odd_split(Q, beta):
    """Given Q_p(u) (ascending Fraction list) and beta=b+1, compute
    Q_p(-(v+beta/2)) as a polynomial in v (ascending Fraction list, via
    poly_compose_linear with u = -1*v - beta/2), then split into even part
    E_p(v) (only even powers survive) and odd part O_p(v) (only odd powers).
    Returns (e, o): e[l] = coeff of v^{2l} in E_p, o[k] = coeff of v^{2k-1}
    in O_p (1-indexed lists, e[0]=constant term, o[0] unused placeholder for
    v^{-1}, real data starts o[1]).
    """
    half_beta = Fraction(beta, 2)
    full = poly_compose_linear(Q, Fraction(-1), -half_beta)  # Q(-(v+beta/2))
    max_deg = len(full) - 1
    e = []
    o = [Fraction(0)]  # o[0] placeholder, unused
    l = 0
    while 2 * l <= max_deg:
        e.append(full[2 * l] if 2 * l < len(full) else Fraction(0))
        l += 1
    k = 1
    while 2 * k - 1 <= max_deg:
        o.append(full[2 * k - 1] if 2 * k - 1 < len(full) else Fraction(0))
        k += 1
    return e, o


class Assembler:
    """Precomputes, once per (p,b) pair, everything needed to evaluate
    D^{*(p)}_r(b) at any r quickly."""

    def __init__(self, p, b):
        self.p = p
        self.b = b
        self.beta = b + 1
        # Q_p(u) has genuine degree 2p (THEOREM.md "Estagio 16": "o proprio
        # documento nomeia explicitamente que Q_p(u) tem grau 2p genuino"),
        # confirmed directly here (deg Q_poly(p) == 2p for every p checked,
        # see ingredients.py self_test / ATTEMPT.md Sec.2.1) -- so the even
        # part E_p(v) needs moments mu_{2l}(N) up to l=p (order 2p), not
        # l=floor(p/2). Warm up the moment table to that full order in ONE
        # pass, before any mu_poly(l) lookups -- avoids the pathological
        # incremental-rebuild pattern mu_poly's lazy growth would otherwise
        # trigger under repeated strictly-increasing calls.
        warm_up_moments(2 * p)
        Q = Q_poly(p)
        self.e, self.o = even_odd_split(Q, self.beta)
        # H_{2k-1}(r,b) table, k=1..p, polynomials in r.
        self.H = build_H_table(p, b)
        # Strip_p(r,b): needs E_p(i - beta/2) for i=1..b -- these are plain
        # numbers (E_p evaluated at v=i-beta/2), not polynomials in r.
        self.Ep_at_i = []
        for i in range(1, b + 1):
            v = Fraction(i) - Fraction(self.beta, 2)
            # E_p(v) = sum_l e_{2l} v^{2l}
            val = Fraction(0)
            for l, coeff in enumerate(self.e):
                val += coeff * (v ** (2 * l))
            self.Ep_at_i.append(val)

    def w_i(self, r, i):
        b = self.b
        num = math.factorial(r) * math.factorial(r + b)
        den = math.factorial(r + i) * math.factorial(r + b + 1 - i)
        return Fraction(num, den)

    def Strip(self, r):
        total = Fraction(0)
        for idx, i in enumerate(range(1, self.b + 1)):
            total += self.Ep_at_i[idx] * self.w_i(r, i)
        return total

    def Phi(self, r):
        N = 2 * r + self.b + 1
        P_b = Fraction(math.factorial(r) * math.factorial(r + self.b), math.factorial(N))
        return P_b * (Fraction(2) ** N)

    def M(self, r):
        N = 2 * r + self.b + 1
        total = Fraction(0)
        for l, coeff in enumerate(self.e):
            if coeff == 0:
                continue
            total += coeff * poly_eval(mu_poly(2 * l), Fraction(N))
        return total

    def odd_sum(self, r):
        total = Fraction(0)
        for k in range(1, self.p + 1):
            ok = self.o[k] if k < len(self.o) else Fraction(0)
            if ok == 0:
                continue
            Hval = poly_eval(self.H[k], Fraction(r))
            total += ok * Hval / (Fraction(2) ** (2 * k - 1))
        return total

    def D_star_full(self, r):
        """The full assembly formula, WITHOUT the r<p shortcut -- used only
        to confirm (self_test below) that Corollary A3's r<p vanishing
        boundary is also forced by the assembled formula's own algebra,
        not merely hard-coded, mirroring the wave-16 referee's own
        structural check on this same point."""
        return Fraction(1, 2) * (self.Phi(r) * self.M(r) - self.Strip(r)) - self.odd_sum(r)

    def D_star(self, r):
        if r < self.p:
            return Fraction(0)
        return self.D_star_full(r)


# ----------------------------------------------------------------------
# Self-tests
# ----------------------------------------------------------------------

def calibration_self_test():
    """Reproduces already-PROVED/already-verified p<=20 values exactly, as
    a sanity gate before trusting the p=41..80 sweep."""
    checks = 0
    fails = 0

    cache = {}

    def get_asm(p, b):
        if (p, b) not in cache:
            cache[(p, b)] = Assembler(p, b)
        return cache[(p, b)]

    for p in range(1, 11):
        for b in (0, 1):
            asm = get_asm(p, b)
            for r in range(0, 60):
                checks += 1
                got = asm.D_star(r)
                want = ground_truth_D_star(p, r, b)
                if got != want:
                    fails += 1
                    print(f"MISMATCH calib p={p} b={b} r={r}: {got} vs {want}")

    for p in range(1, 4):
        for b in (2, 3):
            asm = get_asm(p, b)
            for r in range(0, 40):
                checks += 1
                got = asm.D_star(r)
                want = ground_truth_D_star(p, r, b)
                if got != want:
                    fails += 1
                    print(f"MISMATCH calib p={p} b={b} r={r}: {got} vs {want}")

    print(f"assemble.py calibration_self_test: {checks} checks, {fails} fails")
    return fails == 0


def printed_form_b0(p):
    """D^{*(p)}_r(0), pure polynomial in r (no denominator, since
    Strip_p(r,0)=sum over empty range = 0 trivially). Returns the
    polynomial (ascending Fraction list)."""
    asm = Assembler(p, 0)
    # Build symbolically in r: Phi(r)*M(r) involves 2^N * P_b, not a
    # polynomial in r on its own (varphi_r-type prefactor) -- so we express
    # D^{*(p)}_r(0) = coef * varphi_r_like_term + rem(r), matching the
    # printed-form convention every predecessor front used. Concretely we
    # evaluate numerically at several r and fit is NOT used (would risk
    # interpolation error); instead we build the polynomial parts directly:
    #   Phi_0(r) = 2 * varphi_r  (r!^2/(2r+1)! * 2^{2r+1})
    #   M_p(N), N=2r+1, is itself only evaluable at integer r (mu_poly is a
    #   poly in N, N=2r+1 is linear in r, so M_p as a function of r IS a
    #   polynomial in r after substituting N=2r+1).
    #   odd_sum(r) is a polynomial in r (H_k are polynomials in r).
    # So: D^{*(p)}_r(0) = (1/2)*Phi_0(r)*M_p(2r+1) - odd_sum(r)
    #                    = varphi_r * [M_p(2r+1)] - odd_sum(r)
    # since (1/2)*Phi_0(r) = varphi_r exactly.
    from ingredients import poly_compose_linear as pcl, poly_scale as psc
    from ingredients import poly_add as padd, poly_sub as psub

    # M_p(N) as a poly in N -> substitute N = 2r+1 -> poly in r
    M_poly_N = [Fraction(0)]
    for l, coeff in enumerate(asm.e):
        if coeff == 0:
            continue
        M_poly_N = padd(M_poly_N, psc(mu_poly(2 * l), coeff))
    M_poly_r = pcl(M_poly_N, Fraction(2), Fraction(1))  # N = 2r+1

    coef_r = M_poly_r  # coefficient of varphi_r

    odd_sum_poly = [Fraction(0)]
    for k in range(1, p + 1):
        ok = asm.o[k] if k < len(asm.o) else Fraction(0)
        if ok == 0:
            continue
        odd_sum_poly = padd(odd_sum_poly, psc(asm.H[k], ok / (Fraction(2) ** (2 * k - 1))))

    rem_r = psub([Fraction(0)], odd_sum_poly)  # rem(r) = -odd_sum(r)

    return coef_r, rem_r


def varphi(r):
    return Fraction(4 ** r * math.factorial(r) ** 2, math.factorial(2 * r + 1))


def half_Phi_over_varphi(r, b):
    """(1/2)*Phi_b(r) / varphi_r, evaluated numerically at a concrete
    (r,b) -- used to empirically DISCOVER the exact polynomial-in-r
    prefactor relating Phi_b to varphi_r at a fixed b, before it is
    asserted anywhere. Not assumed to be an integer/polynomial a priori;
    checked at several r for a candidate b before trusting a print."""
    asm = Assembler(1, b)  # p is irrelevant to Phi, any p works
    return Fraction(1, 2) * asm.Phi(r) / varphi(r)


def printed_form_b1(p):
    """D^{*(p)}_r(1) as coef_r*varphi_r + rem_r (pure polynomials in r, no
    denominator) -- valid IFF Strip_p(r,1)=0 identically, which holds
    because Strip_p(r,1) = E_p(1-beta/2)*w_1(r,1), beta=2 at b=1 so
    1-beta/2=0, E_p(0)=Q_p(-1), and Q_p(-1)=0 for every p>=1 tested (see
    Sec.2.4 of ATTEMPT.md). Uses the empirically-discovered-and-verified
    relation (1/2)*Phi_1(r) = varphi_r (checked by half_Phi_over_varphi
    above, self_test below) to express the Phi*M term as coef_r*varphi_r.
    """
    Qm1 = poly_eval(Q_poly(p), Fraction(-1))
    assert Qm1 == 0, f"Q_p(-1) != 0 for p={p}: {Qm1}"

    asm = Assembler(p, 1)
    from ingredients import poly_compose_linear as pcl, poly_scale as psc, poly_add as padd, poly_sub as psub

    M_poly_N = [Fraction(0)]
    for l, coeff in enumerate(asm.e):
        if coeff == 0:
            continue
        M_poly_N = padd(M_poly_N, psc(mu_poly(2 * l), coeff))
    M_poly_r = pcl(M_poly_N, Fraction(2), Fraction(2))  # N = 2r+2 at b=1

    coef_r = M_poly_r  # (1/2)*Phi_1(r) = varphi_r, so this is the varphi_r coefficient

    odd_sum_poly = [Fraction(0)]
    for k in range(1, p + 1):
        ok = asm.o[k] if k < len(asm.o) else Fraction(0)
        if ok == 0:
            continue
        odd_sum_poly = padd(odd_sum_poly, psc(asm.H[k], ok / (Fraction(2) ** (2 * k - 1))))

    rem_r = psub([Fraction(0)], odd_sum_poly)  # rem(r) = -odd_sum(r) (Strip=0)

    return coef_r, rem_r


def r_lt_p_full_formula_self_test(p_list=(41, 50, 61, 70, 80), b_list=(0, 1, 2, 5, 30)):
    """Confirms the r<p vanishing boundary is forced by the FULL assembly
    formula's own algebra (Phi*M - Strip - odd_sum), not merely the
    hard-coded shortcut in D_star -- mirroring the wave-16 referee's own
    structural check (general_p_dstar_extension_attempt/adversarial/
    REFEREE_REPORT.md item (4)-equivalent)."""
    checks = 0
    fails = 0
    for p in p_list:
        for b in b_list:
            asm = Assembler(p, b)
            for r in range(0, p):
                checks += 1
                val = asm.D_star_full(r)
                if val != 0:
                    fails += 1
                    print(f"MISMATCH r<p full-formula p={p} b={b} r={r}: {val}")
    print(f"assemble.py r_lt_p_full_formula_self_test: {checks} checks, {fails} fails")
    return fails == 0


def module_smoke_test_b1():
    """Confirms (1/2)*Phi_1(r) == varphi_r for r=0..50 (the relation
    printed_form_b1 relies on) before it is used to print anything."""
    fails = 0
    checks = 0
    for r in range(0, 51):
        checks += 1
        ratio = half_Phi_over_varphi(r, 1)
        if ratio != 1:
            fails += 1
            print(f"MISMATCH b=1 varphi relation r={r}: ratio={ratio} (want 1)")
    print(f"assemble.py module_smoke_test_b1: {checks} checks, {fails} fails")
    return fails == 0


_SPEED_ROUTE_NOTE = """
NOTE ON SPEED: this front's Assembler itself uses only the straightforward
per-term route (the self.e/self.o loops above) -- no wave-18-style
'combined polynomial' fast path is introduced HERE. The speed engineering
this front actually needed lives one layer down, in odd_part.py: the
H_{2k-1}(r,b) machine is built ONCE per run as a bivariate polynomial
A_k(x,y) (independent of any specific r or b -- see odd_part.py's module
docstring for the (x,y)-reparametrization), then cheaply collapsed to a
plain polynomial-in-r for each b as needed. Without that reparametrization,
building the H_k table from scratch for every one of the 31 b values at
every one of the 40 p values in this front's target range would have been
computationally infeasible in practice at p up to 80 (the recursive
per-(p,b) construction is over the class order p^4-p^5 in cost); with it,
the expensive part is paid once for the whole run. Cross-validated (before
being trusted) against a THIRD, independent, non-bivariate implementation
of the same per-(r,b) depth recursion (odd_part.py self_test item (0)).
"""


if __name__ == "__main__":
    ok1 = calibration_self_test()
    ok2 = module_smoke_test_b1()
    ok3 = r_lt_p_full_formula_self_test()
    ok = ok1 and ok2 and ok3
    print("assemble.py: OK" if ok else "assemble.py: FAILED")
