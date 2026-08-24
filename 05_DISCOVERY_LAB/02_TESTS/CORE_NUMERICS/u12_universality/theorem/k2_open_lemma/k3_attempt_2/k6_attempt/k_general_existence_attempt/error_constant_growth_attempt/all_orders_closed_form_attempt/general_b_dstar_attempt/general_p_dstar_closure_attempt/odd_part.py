"""
The H_k(r,b) machine: P_b * S_{2k-1}(N,r) as an EXPLICIT rational function
of r,b (no factorials, no binomials), for arbitrary k -- the piece that
turns the referee's general-k odd-power identity (cited, PROVED) into an
actually-closed-form contribution to D^{*(p)}_r(b).

Two elementary identities are derived (not merely cited) since they are the
one-line glue that makes the whole general-p assembly mechanical:

  (E1)  Phi_b(r) := P_b * 2^N  =  2*varphi_r * prod_{j=1}^b (2r+2j)/(2r+j+1)
        (already established, general_b_dstar_attempt / the referee's
        Teorema 3'; re-derived and spot-checked here for safety, not
        re-proved from scratch since it is standing input).

  (E2)  P_b * C(N-j, r-j+1)  =  [r]_j / ( [N]_j * (r-j+1) )
        where [x]_j := x(x-1)...(x-j+1), N = 2r+b+1.
        Proof: C(N-j,r-j+1) = (N-j)! / [ (r-j+1)! * (N-j-(r-j+1))! ]
               and N-j-(r-j+1) = N-r-1 = r+b  (constant in j, from N=2r+b+1).
        So C(N-j,r-j+1) = (N-j)!/[(r-j+1)!(r+b)!], and
        P_b * C(N-j,r-j+1) = [r!(r+b)!/N!] * (N-j)!/[(r-j+1)!(r+b)!]
                            = r!*(N-j)! / [N! * (r-j+1)!]
                            = ([r]_j/[N]_j) / (r-j+1).      QED (elementary).
        This is the j-indexed special case of the general-k collapse
        proposition (parent Sec 3.4, PROVED); re-derived independently here
        because it is used at every recursion depth below.

Using (E2), the referee's cited recursion for S_{2k-1}(N,m) is unrolled
directly into an explicit rational function of (r,b) -- this is the
"mechanical write-out" the referee's report names as what remains.
"""

import sympy as sp
from functools import lru_cache

r, b = sp.symbols('r b')
N_expr = 2 * r + b + 1
beta_expr = b + 1


def falling(x, j):
    """[x]_j = x(x-1)...(x-j+1), explicit polynomial product (j small int)."""
    out = sp.Integer(1)
    for i in range(j):
        out *= (x - i)
    return out


@lru_cache(maxsize=None)
def H(power, depth=0):
    """H_k(r,b) = P_b * S_{power}(N,r) unrolled via the referee's cited
    recursion (S_{2k-1}) combined with identity (E2) above, applied at
    every depth. `power` is the odd exponent (2k-1); `depth` tracks the
    total number of (N-1,m-1) shifts already applied (used internally by
    the recursion -- callers should always use depth=0).

    Returns an explicit sympy expression in r,b (Rational coefficients,
    finite sum of products of linear/polynomial factors -- no factorials,
    no binomials remain).
    """
    beta_local = beta_expr + depth
    lead = beta_local ** (power - 1) * falling(r, depth) / falling(N_expr, depth)
    if power == 1:
        return sp.expand(lead)
    total = lead
    Nd = N_expr - depth
    for s in range(1, power - 1, 2):
        coeff = sp.binomial(power - 1, s)
        total += 2 * Nd * coeff * H(s, depth + 1)
    return sp.expand(total)


_H_reduced_cache = {}


def H_reduced(power):
    """H_k(r,b), fully combined over a common denominator and cancelled.

    The raw recursive unrolling of H() builds a sum of terms each of shape
    [r]_d / [N]_d for various depths d; H_k(r,b) is mathematically always a
    genuine POLYNOMIAL in r,b (this is exactly the content of the general-k
    collapse proposition, cited), but the individual summands can have
    apparent (removable) poles at small r,b where [N]_d vanishes while
    [r]_d vanishes too. sp.cancel combines everything over one denominator
    and removes the common factor, producing the true polynomial -- this
    is verified below (H_reduced always comes back with unit denominator).
    """
    if power in _H_reduced_cache:
        return _H_reduced_cache[power]
    raw = H(power)
    combined = sp.cancel(sp.together(raw))
    num, den = sp.fraction(combined)
    if sp.expand(den - 1) != 0:
        raise ValueError(f"H_{power}: did not reduce to a polynomial! denominator={den}")
    poly = sp.expand(num)
    _H_reduced_cache[power] = poly
    return poly


_H_reduced_b_cache = {}


def H_reduced_at_b(power, b_val):
    """Same content as H_reduced(power).subs(b, b_val), but with b
    substituted to a concrete integer BEFORE the fraction-cancellation
    step. Mathematically identical (b is just substituted at a different
    point in the pipeline); done this way purely for performance -- with b
    concrete, [N]_depth is a univariate polynomial in r alone, so
    sp.cancel/together has far less work to do than in the fully
    symbolic-in-(r,b) case. This matters only for large power (large p);
    cross-checked against H_reduced(...).subs(b,b_val) for every power
    actually used in this front's verification (see verify_H_at_b_matches
    below) before being relied on for any p>=... value.
    """
    key = (power, b_val)
    if key in _H_reduced_b_cache:
        return _H_reduced_b_cache[key]
    raw = H(power).subs(b, b_val)
    combined = sp.cancel(sp.together(raw))
    num, den = sp.fraction(combined)
    if sp.expand(den - 1) != 0:
        raise ValueError(f"H_{power}(b={b_val}): did not reduce to a polynomial! denominator={den}")
    poly = sp.expand(num)
    _H_reduced_b_cache[key] = poly
    return poly


def verify_H_at_b_matches(powers=(1, 3, 5, 7, 9), b_vals=(0, 1, 3, 5)):
    """H_reduced_at_b must agree with H_reduced(...).subs(b,b_val) exactly,
    for every power/b_val checked -- confirms the reordering of
    substitution vs. cancellation changes nothing mathematically."""
    print("--- verifying H_reduced_at_b matches H_reduced(power).subs(b,.) ---")
    fails = 0
    total = 0
    for power in powers:
        full = H_reduced(power)
        for bv in b_vals:
            total += 1
            a = sp.expand(full.subs(b, bv))
            c = H_reduced_at_b(power, bv)
            if sp.expand(a - c) != 0:
                fails += 1
                print(f"MISMATCH power={power} b={bv}")
    print(f"H_reduced_at_b cross-check: {total} checks, fails={fails}")
    return fails


def verify_E2(jmax=10, rmax=15, bmax=10):
    """Verify (E2) directly: P_b*C(N-j,r-j+1) == [r]_j/([N]_j*(r-j+1))."""
    print(f"--- verifying (E2): P_b*C(N-j,r-j+1) = [r]_j/([N]_j*(r-j+1)) ---")
    import math
    fails = 0
    total = 0
    for rv in range(0, rmax + 1):
        for bv in range(0, bmax + 1):
            Nv = 2 * rv + bv + 1
            Pb = sp.Rational(math.factorial(rv) * math.factorial(rv + bv), math.factorial(Nv))
            for j in range(0, min(jmax, rv + 2) + 1):
                total += 1
                lhs = Pb * sp.binomial(Nv - j, rv - j + 1)
                rj = falling(rv, j)
                Nj = falling(Nv, j)
                denom = Nj * (rv - j + 1)
                rhs = sp.Rational(rj, denom) if denom != 0 else (sp.Integer(0) if rj == 0 else None)
                if denom == 0:
                    # (r-j+1)=0 means j=r+1: rj should also be 0 (falling(r,r+1) has factor r-r=0)
                    if rj != 0:
                        fails += 1
                        print("denom-zero but rj != 0:", rv, bv, j, rj)
                    continue
                if lhs != rhs:
                    fails += 1
                    print(f"MISMATCH r={rv} b={bv} j={j}: lhs={lhs} rhs={rhs}")
    print(f"(E2) checks: {total}, fails={fails}")
    return fails


def S_bruteforce(power, Nv, m):
    if m < 0:
        return sp.Integer(0)
    total = sp.Integer(0)
    for i in range(0, m + 1):
        total += (Nv - 2 * i) ** power * sp.binomial(Nv, i)
    return total


def verify_H_bruteforce(powers=(1, 3, 5, 7, 9, 11), rmax=12, bmax=8):
    """Verify H(power) symbolic expression against P_b*S_power(N,r) computed
    by direct brute-force summation, for concrete integer r,b."""
    print(f"--- verifying H_k(r,b) vs brute force P_b*S_power(N,r), powers={powers} ---")
    import math
    fails = 0
    total = 0
    Hexprs = {p: H_reduced(p) for p in powers}
    for power in powers:
        expr = Hexprs[power]
        for rv in range(0, rmax + 1):
            for bv in range(0, bmax + 1):
                total += 1
                Nv = 2 * rv + bv + 1
                Pb = sp.Rational(math.factorial(rv) * math.factorial(rv + bv), math.factorial(Nv))
                brute = Pb * S_bruteforce(power, Nv, rv)
                pred = expr.subs({r: rv, b: bv})
                if sp.simplify(brute - pred) != 0:
                    fails += 1
                    print(f"MISMATCH power={power} r={rv} b={bv}: brute={brute} pred={pred}")
    print(f"H_k brute-force checks: {total}, fails={fails}")
    return fails


def verify_H_matches_parent_printed():
    """Cross-check H_1..H_4 (equivalently -H_k/2^{2k-1} = P_b*sum v^{2k-1}C)
    against the parent document's printed k=1,2,3,4 brackets in Sec 3.4."""
    print("--- cross-check vs parent-printed P_b*sum v^{2k-1}C(N,alpha) brackets ---")
    beta = beta_expr
    parent = {
        1: sp.Rational(-1, 2),
        3: sp.Rational(-1, 8) * (beta ** 2 + 4 * r),
        5: sp.Rational(-1, 32) * (beta ** 4 + 8 * r * ((beta + 1) ** 2 + 1) + 32 * r * (r - 1)),
        7: sp.Rational(-1, 128) * (beta ** 6 + r * (12 * (beta + 1) ** 4 + 40 * (beta + 1) ** 2 + 12)
                                    + r * (r - 1) * (96 * (beta + 2) ** 2 + 256) + 384 * r * (r - 1) * (r - 2)),
    }
    fails = 0
    for k2m1, expr in parent.items():
        mine = sp.expand(-H_reduced(k2m1) / sp.Integer(2) ** k2m1)
        diff = sp.simplify(mine - expr)
        ok = (diff == 0)
        print(f"power={k2m1}: matches parent printed bracket exactly: {ok}")
        if not ok:
            fails += 1
            print("  residual:", diff)
    return fails


def verify_Phi_identity(rmax=15, bmax=15):
    """(E1): Phi_b(r) := P_b*2^N  ==  2*varphi_r*prod_{j=1}^b (2r+2j)/(2r+j+1).
    Established input; spot-checked here for safety before use."""
    import math
    print("--- spot-checking (E1): Phi_b(r) = P_b*2^N = 2*varphi_r*prod(...) ---")
    fails = 0
    total = 0
    for rv in range(0, rmax + 1):
        varphi = sp.Rational(4 ** rv * math.factorial(rv) ** 2, math.factorial(2 * rv + 1))
        for bv in range(0, bmax + 1):
            total += 1
            Nv = 2 * rv + bv + 1
            Pb = sp.Rational(math.factorial(rv) * math.factorial(rv + bv), math.factorial(Nv))
            lhs = Pb * 2 ** Nv
            rhs = 2 * varphi
            for j in range(1, bv + 1):
                rhs *= sp.Rational(2 * rv + 2 * j, 2 * rv + j + 1)
            if lhs != rhs:
                fails += 1
                print(f"MISMATCH r={rv} b={bv}: lhs={lhs} rhs={rhs}")
    print(f"(E1) checks: {total}, fails={fails}")
    return fails


if __name__ == "__main__":
    f0 = verify_E2(jmax=12, rmax=15, bmax=10)
    f1 = verify_Phi_identity(rmax=15, bmax=15)
    f2 = verify_H_bruteforce(powers=(1, 3, 5, 7, 9, 11, 13), rmax=12, bmax=8)
    f3 = verify_H_matches_parent_printed()
    f4 = verify_H_at_b_matches(powers=(1, 3, 5, 7, 9), b_vals=(0, 1, 3, 5))
    print()
    print("=== odd_part.py summary ===")
    print(f"(E2) elementary identity: fails={f0}")
    print(f"(E1) Phi_b(r)=P_b*2^N spot-check: fails={f1}")
    print(f"H_k vs brute force (k up to 7, power up to 13): fails={f2}")
    print(f"H_k vs parent printed k=1..4 brackets: fails={f3}")
    print(f"H_reduced_at_b vs H_reduced(...).subs(b,.): fails={f4}")
    assert f0 == 0 and f1 == 0 and f2 == 0 and f3 == 0 and f4 == 0, "ODD-PART FAILURE"
    print("ALL ODD-PART CHECKS PASSED")
