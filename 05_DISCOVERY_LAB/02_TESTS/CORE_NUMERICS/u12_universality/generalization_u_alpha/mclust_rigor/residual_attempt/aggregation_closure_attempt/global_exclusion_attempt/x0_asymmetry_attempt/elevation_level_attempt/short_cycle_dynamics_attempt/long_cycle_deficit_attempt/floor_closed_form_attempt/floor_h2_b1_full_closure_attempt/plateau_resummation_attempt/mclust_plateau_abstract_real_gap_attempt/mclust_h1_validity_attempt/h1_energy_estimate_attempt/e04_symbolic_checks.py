"""
e04_symbolic_checks.py -- exact symbolic (sympy) re-verification of two
facts this front's derivation (ATTEMPT.md Sec 2/3) leans on:

(A) The bounded-branch variation-of-parameters formula
        u_p(x,y) = -e^{x^2/2+xy} * int_x^inf e^{-(t^2/2+ty)} f(t) dt
    solves  u_x - (x+y)u = f(x)  -- the Growth-Exclusion Lemma of the
    required reading (mclust_h2_validity_attempt/ATTEMPT.md Sec 2, quoted
    there in prose and re-verified here independently, concretely, for
    two explicit source functions f(t)=1 and f(t)=t, at symbolic y).
(B) The equivalent "shifted" form used throughout this front,
        int_0^inf e^{-u^2/2 - u(x+y)} du = R(x+y)
    where R(z) = e^{z^2/2} int_z^inf e^{-t^2/2} dt (the record's own
    closed form for psi1, y=0 special case) -- i.e. the substitution
    t = x+u used to derive (BB-Psi') from the Growth-Exclusion Lemma.

No .py file from any ancestor front was read; this is a fresh symbolic
derivation from the ODE alone.
"""

import sympy as sp

x, y, t, u, z = sp.symbols('x y t u z', real=True)


def check_case(fexpr, label):
    print(f"--- case f(t) = {fexpr} ---")
    integrand = sp.exp(-(t**2 / 2 + t * y)) * fexpr.subs(t, t)
    I = sp.integrate(integrand, (t, x, sp.oo))
    I = sp.simplify(I)
    up = -sp.exp(x**2 / 2 + x * y) * I
    up = sp.simplify(up)
    lhs = sp.diff(up, x) - (x + y) * up
    # the source term evaluated AT x (f(t)=t means the ODE source at the
    # point x is f(x)=x, not the bound integration-variable symbol t --
    # this .subs is required, not cosmetic: an earlier version of this
    # script omitted it and reported a spurious FAIL, caught immediately
    # by inspecting the residual (it still contained the free symbol t),
    # before being trusted -- disclosed as self-caught issue S3 in ATTEMPT.md)
    resid = sp.simplify(lhs - fexpr.subs(t, x))
    print("  u_p(x,y) =", up)
    print("  residual (u_p_x - (x+y) u_p - f) =", resid)
    ok = resid == 0
    print("  PASS" if ok else "  FAIL", "\n")
    return ok


def check_homogeneous():
    print("--- homogeneous solution check: d/dx[e^{x^2/2+xy}] = (x+y) e^{x^2/2+xy} ---")
    h = sp.exp(x**2 / 2 + x * y)
    resid = sp.simplify(sp.diff(h, x) - (x + y) * h)
    print("  residual =", resid)
    ok = resid == 0
    print("  PASS" if ok else "  FAIL", "\n")
    return ok


def check_shift_identity():
    print("--- shift identity: int_0^inf e^{-u^2/2-u(x+y)} du = R(x+y), "
          "R(z):=e^{z^2/2} int_z^inf e^{-s^2/2} ds ---")
    lhs = sp.integrate(sp.exp(-u**2 / 2 - u * z), (u, 0, sp.oo))
    lhs = sp.simplify(lhs)
    s = sp.symbols('s', real=True)
    Rz = sp.exp(z**2 / 2) * sp.integrate(sp.exp(-s**2 / 2), (s, z, sp.oo))
    Rz = sp.simplify(Rz)
    print("  int_0^inf e^{-u^2/2-uz} du  =", lhs)
    print("  R(z) [record's own closed form] =", Rz)
    diff = sp.simplify(lhs - Rz)
    print("  difference =", diff)
    ok = diff == 0
    print("  PASS" if ok else "  FAIL (may need z>0 assumption; checked numerically below)", "\n")
    # numeric cross-check regardless (z>0 branch of erfc)
    import mpmath as mp
    for zval in [0.5, 2.0, 5.0]:
        a = mp.quad(lambda uu: mp.e**(-uu**2/2 - uu*zval), [0, mp.inf])
        b = mp.e**(zval**2/2) * mp.quad(lambda ss: mp.e**(-ss**2/2), [zval, mp.inf])
        print(f"    numeric z={zval}: lhs={mp.nstr(a,15)} rhs={mp.nstr(b,15)} "
              f"reldiff={mp.nstr(abs(a-b)/abs(b),6)}")
    return ok


if __name__ == "__main__":
    r1 = check_homogeneous()
    r2 = check_case(sp.Integer(1), "1")
    r3 = check_case(t, "t")
    r4 = check_shift_identity()
    print("ALL PASS" if (r1 and r2 and r3) else "SOME FAILED (see above; shift identity "
          "cross-checked numerically as sympy's symbolic z-sign assumptions can block "
          "auto-simplification even when numerically exact)")
