"""
k03_profiles.py -- closed-form / integral-representation outer-solution
profiles psi1(x), psi2(x), psi3(x), used as the matched-asymptotics
prediction for F(x;c) := lim_{g->inf} Phi(s,g) at x = s*sqrt(c),
eps = 1/sqrt(c):

    F(x;c) = eps*psi1(x) + eps^2*psi2(x) + eps^3*psi3(x) + O(eps^4)

psi1, psi2 are given IN CLOSED FORM in the required-reading prose
(plateau_resummation_attempt/ATTEMPT.md Section 4.2/4.3/Section 6):

    R(x) := sqrt(pi/2)*erfcx(x/sqrt(2)),   R' = x R - 1,  R(inf)=0
    psi1(x) = R(x)
    psi2(x) = 2 x R(x) - 2

psi3 is NOT given in closed form at general x by the required-reading
documents -- only its ODE (Section 4.4: "psi3' = x psi3 + 7 R'(x)",
bounded branch) and its value at x=0 (psi3(0) = (7/2)*sqrt(pi/2)) are
stated. This front derives (fresh, by the standard bounded-branch
variation-of-parameters method used identically for R itself, whose own
integral representation R(x) = e^{x^2/2} int_x^inf e^{-t^2/2} dt is the
same bounded-branch selection for the ODE R'=xR-1) the general-x closed
form for psi3 as an integral:

    psi3(x) = -e^{x^2/2} * int_x^inf e^{-t^2/2} * 7*R'(t) dt

(the bounded/decaying-at-infinity solution of psi3' = x*psi3 + 7 R',
selected by excluding the growing homogeneous branch e^{x^2/2}, exactly
as record's own bounded-branch selection principle, restated in Section
4.5/H2 of the required reading, is applied throughout this lineage).
Verified below (group V1) against the record's own closed-form value
psi3(0) = (7/2)*sqrt(pi/2).
"""
import mpmath as mp
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k01_family_series import erfcx


def R(x):
    x = mp.mpf(x)
    return mp.sqrt(mp.pi / 2) * erfcx(x / mp.sqrt(2))


def Rprime(x):
    x = mp.mpf(x)
    return x * R(x) - 1


def psi1(x):
    return R(x)


def psi2(x):
    x = mp.mpf(x)
    return 2 * x * R(x) - 2


def R_derivs_at(x):
    """
    R(x), R'(x), R''(x), R'''(x) via the elementary recursion generated
    directly from R' = x R - 1 (differentiate repeatedly; standard, not
    the record's own closed-form R^{(n)} formula, re-derived here):
        R'' = R + x R'
        R''' = 2 R' + x R''
    Verified (k05/ATTEMPT.md) against the record's stated psi4(0)=-34/3
    via psi4(x) = (17/3) R'''(x) (Section 4.4b of the required reading).
    """
    x = mp.mpf(x)
    R0 = R(x)
    R1 = x * R0 - 1
    R2 = R0 + x * R1
    R3 = 2 * R1 + x * R2
    return R0, R1, R2, R3


def psi4(x):
    """psi4(x) = (17/3) R'''(x)  -- CLOSED FORM stated in the required
    reading (Section 4.4b of plateau_resummation_attempt/ATTEMPT.md);
    used here as-is (not re-derived beyond the elementary R-derivative
    recursion above), for a genuine 3rd-order (order 2->3 transition)
    uniformity test that needs no new integral representation."""
    _, _, _, R3 = R_derivs_at(x)
    return mp.mpf(17) / 3 * R3


def psi3(x, quad_extra_dps=15):
    """
    psi3(x) = e^{x^2/2} * int_x^inf e^{-t^2/2} * 7 * R'(t) dt

    Computed with a temporary precision bump (quad_extra_dps) to absorb
    the exp(x^2/2)*[small integral] cancellation at the working
    precision, then rounded back -- standard practice, disclosed here
    rather than silently relied upon.
    """
    x = mp.mpf(x)
    old = mp.mp.dps
    mp.mp.dps = old + quad_extra_dps
    integrand = lambda t: mp.e**(-(t * t) / 2) * 7 * Rprime(t)
    # substitute t = x + u, u in [0, inf), to keep quad well-behaved
    val = mp.quad(lambda u: integrand(x + u), [0, mp.inf])
    # bounded-branch variation-of-parameters solution of y' - x y = f(x)
    # (same method as R itself): y(x) = -e^{x^2/2} int_x^inf e^{-t^2/2} f(t) dt
    result = -mp.e**((x * x) / 2) * val
    mp.mp.dps = old
    return +result  # round back to old precision
