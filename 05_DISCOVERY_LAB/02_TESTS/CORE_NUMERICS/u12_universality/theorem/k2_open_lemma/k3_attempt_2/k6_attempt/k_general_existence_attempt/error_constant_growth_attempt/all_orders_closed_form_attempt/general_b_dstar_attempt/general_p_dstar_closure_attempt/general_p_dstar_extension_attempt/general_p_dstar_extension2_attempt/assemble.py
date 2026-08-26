"""
assemble.py -- the general-p closed-form assembly for D^{*(p)}_r(b),
p=21 and beyond, fresh implementation for this front (wave 18,
GENERAL-P-DSTAR-EXTENSION2-ATTEMPT).

Assembly formula (PROVED given its cited ingredients; reproduced verbatim
from general_p_dstar_closure_attempt/ATTEMPT.md Sec 2, restated unchanged
by general_p_dstar_extension_attempt/ATTEMPT.md Sec 1 -- neither
predecessor's SCRIPTS were read, only their ATTEMPT.md prose, per the
task mandate):

  N := 2r+b+1, beta := b+1,

  D^{*(p)}_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)]
                    - sum_{k=1}^{p} o_k * H_{2k-1}(r,b) / 2^{2k-1}

  Q_p(-(v+beta/2)) = E_p(v) + O_p(v)     (even/odd split in v)
  e_{2l} := coeff of v^{2l} in E_p       (l=0,...,p)
  o_k    := coeff of v^{2k-1} in O_p     (k=1,...,p)
  M_p(N) := sum_l e_{2l} * mu_{2l}(N)
  Phi_b(r) := P_b * 2^N = 2*phi_r*prod_{j=1}^{b} (2r+2j)/(2r+j+1)   [(E1), cited]
  Strip_p(r,b) := sum_{i=1}^{b} E_p(i - beta/2) * w_i(r,b)
  w_i(r,b) := r!(r+b)! / [ (r+i)!(r+b+1-i)! ]
  H_{2k-1}(r,b) := (this file's odd_part.build_H_table -- see that file
                    for the from-scratch re-derivation of its recursion
                    from the cited S_{2k-1} recursion)

Ingredients used from this directory's own from-scratch implementations
(each independently self-tested against brute force / known PROVED
formulas before being trusted here -- see ingredients.py, odd_part.py):
  - Q_poly(p) (ingredients.py)
  - central_moment_poly(l) (ingredients.py)
  - build_H_table(K_max, b) (odd_part.py)
  - phi_r, D_star (ground_truth.py -- the independent arbiter)

Exact Fraction arithmetic throughout. No floating point, no sympy in the
hot loop (a small, clearly-marked sympy-based routine is used ONLY for
printing a handful of representative symbolic-in-r closed forms, never
for the verification sweep).
"""

from fractions import Fraction
import math
import time

from ingredients import (
    Q_poly, poly_eval, poly_compose_linear, poly_add, poly_scale, poly_trim,
    central_moment_poly,
)
from odd_part import build_H_table
import ground_truth as gt


# ---------------------------------------------------------------------------
# Even/odd split of Q_p(-(v+beta/2)), for a FIXED concrete integer b.
# ---------------------------------------------------------------------------

def even_odd_split(p, b):
    """Returns (e, o): e[l] = coeff of v^{2l} in E_p(v), o[k] = coeff of
    v^{2k-1} in O_p(v), where Q_p(-(v+beta/2)) = E_p(v)+O_p(v),
    beta=b+1. Substitution u = a*v + c with a=-1, c=-beta/2, via
    poly_compose_linear (general polynomial composition, exact)."""
    beta = b + 1
    Qp = Q_poly(p)
    Rp = poly_compose_linear(Qp, a=Fraction(-1), c=Fraction(-beta, 2))
    e = {}
    o = {}
    for n, c in enumerate(Rp):
        if n % 2 == 0:
            e[n // 2] = c
        else:
            o[(n + 1) // 2] = c
    return e, o


def E_p_eval(e, x):
    """E_p(x) = sum_l e[l] x^{2l}, evaluated at a concrete Fraction x."""
    total = Fraction(0)
    x = Fraction(x)
    for l, el in e.items():
        if el == 0:
            continue
        total += el * x ** (2 * l)
    return total


# ---------------------------------------------------------------------------
# Phi_b(r) and the strip weights w_i(r,b), concrete integers.
# ---------------------------------------------------------------------------

def Phi_b_of_r(r, b):
    """Phi_b(r) = 2*phi_r*prod_{j=1}^{b}(2r+2j)/(2r+j+1), (E1), cited."""
    ratio = Fraction(1)
    for j in range(1, b + 1):
        ratio *= Fraction(2 * r + 2 * j, 2 * r + j + 1)
    return 2 * gt.phi_r(r) * ratio


def w_i(r, b, i):
    """w_i(r,b) = r!(r+b)! / [(r+i)!(r+b+1-i)!], exact. Uses the cached
    factorial from ground_truth.py (a pure speed optimization -- see
    that file's cache and its self-test confirming it matches
    math.factorial exactly)."""
    num = gt.factorial(r) * gt.factorial(r + b)
    den = gt.factorial(r + i) * gt.factorial(r + b + 1 - i)
    return Fraction(num, den)


# ---------------------------------------------------------------------------
# The full assembly, for a fixed (p,b), evaluated over a range of r --
# precomputes everything that does not depend on r ONCE per (p,b).
# ---------------------------------------------------------------------------

class Assembler:
    """Precomputes, once per (p,b): Q_p's even/odd split, the H_k
    polynomial-in-r table (k=1..p), the central moment polynomials
    mu_{2l}(N) for l=0..p, AND (speed optimization, cross-validated
    against the direct per-term sums before being trusted -- see
    _speed_selftest below) two COMBINED polynomials:
      combined_mu_poly(N)  := sum_l e_l * mu_{2l}(N)      [replaces M_p]
      combined_H_poly(r)   := sum_k (o_k/2^{2k-1}) H_k(r)  [replaces H_sum]
    built once per (p,b) by summing the underlying polynomials (each
    O(p) work), so that evaluating D^{*(p)}_r(b) at each r in a sweep
    costs a SINGLE Horner evaluation of each (O(p) per r, not O(p^2) --
    the direct per-term route evaluates p separate polynomials of
    increasing degree at every r). The strip weights E_p(i-beta/2), which
    do not depend on r at all, are likewise precomputed once per (p,b).
    """

    def __init__(self, p, b):
        self.p = p
        self.b = b
        self.beta = b + 1
        self.e, self.o = even_odd_split(p, b)
        self.H = build_H_table(p, b)
        self._mu = {l: central_moment_poly(l) for l in self.e if self.e[l] != 0}

        combined_mu = [Fraction(0)]
        for l, el in self.e.items():
            if el == 0:
                continue
            combined_mu = poly_add(combined_mu, poly_scale(self._mu[l], el))
        self.combined_mu_poly = poly_trim(combined_mu)

        combined_H = [Fraction(0)]
        for k in range(1, p + 1):
            ok = self.o.get(k, Fraction(0))
            if ok == 0:
                continue
            combined_H = poly_add(combined_H, poly_scale(self.H[k], ok / (Fraction(2) ** (2 * k - 1))))
        self.combined_H_poly = poly_trim(combined_H)

        self.strip_terms = []
        for i in range(1, b + 1):
            x = Fraction(i) - Fraction(self.beta, 2)
            self.strip_terms.append(E_p_eval(self.e, x))

    # --- slow (direct per-term) route: kept for cross-validation only ---

    def M_p_slow(self, N):
        total = Fraction(0)
        for l, el in self.e.items():
            if el == 0:
                continue
            total += el * poly_eval(self._mu[l], N)
        return total

    def Strip_slow(self, r):
        b = self.b
        if b == 0:
            return Fraction(0)
        beta = self.beta
        total = Fraction(0)
        for i in range(1, b + 1):
            x = Fraction(i) - Fraction(beta, 2)
            total += E_p_eval(self.e, x) * w_i(r, b, i)
        return total

    def H_sum_slow(self, r):
        total = Fraction(0)
        for k in range(1, self.p + 1):
            ok = self.o.get(k, Fraction(0))
            if ok == 0:
                continue
            total += ok * poly_eval(self.H[k], r) / (Fraction(2) ** (2 * k - 1))
        return total

    # --- fast (combined-polynomial) route: used for the production sweep ---

    def M_p(self, N):
        return poly_eval(self.combined_mu_poly, N)

    def Strip(self, r):
        if self.b == 0:
            return Fraction(0)
        total = Fraction(0)
        for i in range(1, self.b + 1):
            total += self.strip_terms[i - 1] * w_i(r, self.b, i)
        return total

    def H_sum(self, r):
        return poly_eval(self.combined_H_poly, r)

    def D_star(self, r):
        N = 2 * r + self.b + 1
        phi_term = Fraction(1, 2) * (Phi_b_of_r(r, self.b) * self.M_p(N) - self.Strip(r))
        return phi_term - self.H_sum(r)


def speed_route_selftest(p_values=(1, 2, 5, 10), b_values=(0, 1, 3), r_values=(0, 1, 5, 17, 42)):
    """Cross-validates the fast (combined-polynomial) route against the
    slow (direct per-term) route, character-for-character, BEFORE the
    fast route is trusted for the main sweep -- same discipline as both
    predecessor fronts applied to their own fast-vs-slow ingredient
    routes."""
    checks = 0
    fails = 0
    for p in p_values:
        for b in b_values:
            asm = Assembler(p, b)
            for r in r_values:
                N = 2 * r + b + 1
                checks += 1
                if asm.M_p(N) != asm.M_p_slow(N):
                    fails += 1
                    print(f"SPEED MISMATCH M_p p={p} b={b} r={r}")
                checks += 1
                if asm.Strip(r) != asm.Strip_slow(r):
                    fails += 1
                    print(f"SPEED MISMATCH Strip p={p} b={b} r={r}")
                checks += 1
                if asm.H_sum(r) != asm.H_sum_slow(r):
                    fails += 1
                    print(f"SPEED MISMATCH H_sum p={p} b={b} r={r}")
    print(f"speed_route_selftest: {checks} checks, {fails} fails")
    return fails == 0


# ---------------------------------------------------------------------------
# Exhaustive verification sweep.
# ---------------------------------------------------------------------------

def verify_range(p, r_max, b_max, verbose_every=None):
    checks = 0
    fails = 0
    fail_examples = []
    t0 = time.time()
    for b in range(0, b_max + 1):
        asm = Assembler(p, b)
        for r in range(0, r_max + 1):
            got = asm.D_star(r)
            want = gt.D_star(p, r, b)
            checks += 1
            if got != want:
                fails += 1
                if len(fail_examples) < 10:
                    fail_examples.append((p, r, b, got, want))
    elapsed = time.time() - t0
    return checks, fails, fail_examples, elapsed


# ---------------------------------------------------------------------------
# Symbolic-in-r printed closed forms, b=0 and b=1 ONLY (pure Fraction
# poly-in-r arithmetic -- no sympy needed; Strip is identically 0 at b=0,
# and identically 0 at b=1 because Q_p(-1)=0 for every p>=1, verified in
# ingredients.py's self_test -- see the derivation note there).
# ---------------------------------------------------------------------------

def printed_form_b0(p):
    """Returns (coef_poly, remainder_poly): D^{*(p)}_r(0) =
    coef_poly(r)*phi_r + remainder_poly(r), exact Fraction coefficient
    lists in r."""
    asm = Assembler(p, 0)
    # M_p(N(r)), N=2r+1 (b=0) -- compose each mu_{2l} poly-in-N with
    # N = 2r+1, sum weighted by e_l, to get a poly-in-r directly.
    coef = [Fraction(0)]
    for l, el in asm.e.items():
        if el == 0:
            continue
        mu_r = poly_compose_linear(asm._mu[l], a=2, c=1)
        coef = poly_add(coef, poly_scale(mu_r, el))
    # remainder(r) = -sum_k o_k H_k(r) / 2^{2k-1}   (Strip==0 at b=0)
    rem = [Fraction(0)]
    for k in range(1, p + 1):
        ok = asm.o.get(k, Fraction(0))
        if ok == 0:
            continue
        term = poly_scale(asm.H[k], -ok / (Fraction(2) ** (2 * k - 1)))
        rem = poly_add(rem, term)
    return poly_trim(coef), poly_trim(rem)


def printed_form_b1(p):
    """Same as printed_form_b0 but b=1. Strip_p(r,1) = E_p(0)*w_1(r,1) =
    Q_p(-1) * 1/(r+1) = 0 (Q_p(-1)=0, verified) -- so the remainder is
    STILL a pure polynomial (no 1/(r+1) term survives), exactly as
    printed_form_b0, just with N=2r+2."""
    asm = Assembler(p, 1)
    # Sanity: Strip must vanish identically for this to be valid; check
    # at a few concrete r before trusting the polynomial-only remainder
    # construction below.
    for r in (0, 3, 7, 20):
        s = asm.Strip(r)
        if s != 0:
            raise AssertionError(f"Strip_p(r,1) != 0 at p={p}, r={r}: {s} "
                                  f"-- printed_form_b1's polynomial-only "
                                  f"assumption is violated, do not print.")
    coef = [Fraction(0)]
    for l, el in asm.e.items():
        if el == 0:
            continue
        mu_r = poly_compose_linear(asm._mu[l], a=2, c=2)  # N=2r+2
        coef = poly_add(coef, poly_scale(mu_r, el))
    rem = [Fraction(0)]
    for k in range(1, p + 1):
        ok = asm.o.get(k, Fraction(0))
        if ok == 0:
            continue
        term = poly_scale(asm.H[k], -ok / (Fraction(2) ** (2 * k - 1)))
        rem = poly_add(rem, term)
    return poly_trim(coef), poly_trim(rem)


def _format_poly(poly, varname="r"):
    terms = []
    for n in range(len(poly) - 1, -1, -1):
        c = poly[n]
        if c == 0:
            continue
        if n == 0:
            terms.append(f"{c}")
        elif n == 1:
            terms.append(f"({c})*{varname}")
        else:
            terms.append(f"({c})*{varname}^{n}")
    return " + ".join(terms) if terms else "0"


# ---------------------------------------------------------------------------
# Self-tests / calibration against previously PROVED formulas (p<=10,
# b=0,1) -- run BEFORE the exhaustive p>=21 sweep, exactly mirroring both
# predecessors' calibration-first discipline.
# ---------------------------------------------------------------------------

def calibration_self_test():
    checks = 0
    fails = 0
    for p in range(1, 11):
        for b in (0, 1):
            asm = Assembler(p, b)
            for r in range(0, 60):
                got = asm.D_star(r)
                want = gt.D_star(p, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    print(f"CALIBRATION MISMATCH p={p} r={r} b={b}: got {got} want {want}")
    # Also b=2,3 at p=1,2,3 (predecessor's own printed instances,
    # reproduced via ground_truth's Corollary A3, not a separate hand
    # formula -- ground_truth.py itself was already calibrated against
    # those printed instances where available, see ground_truth.py).
    for p in range(1, 4):
        for b in (2, 3):
            asm = Assembler(p, b)
            for r in range(0, 40):
                got = asm.D_star(r)
                want = gt.D_star(p, r, b)
                checks += 1
                if got != want:
                    fails += 1
                    print(f"CALIBRATION MISMATCH(b>=2) p={p} r={r} b={b}: got {got} want {want}")
    print(f"assemble.py calibration_self_test: {checks} checks, {fails} fails")
    return fails == 0


if __name__ == "__main__":
    ok1 = speed_route_selftest()
    ok2 = calibration_self_test()
    ok = ok1 and ok2
    print("assemble.py calibration: OK" if ok else "assemble.py calibration: FAILURES")
