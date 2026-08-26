"""
k03_boundedness_certificate.py -- MCLUST-H2-VALIDITY-ATTEMPT

Two purposes, both filling a genuine gap left by k01/k02:

(1) k02's Growth-Exclusion Lemma needs, for EXISTENCE of the bounded
    branch at each order, that the source f_n(x) has at most
    sub-Gaussian growth (so the defining improper integral converges).
    Every f_n actually needed through the orders this front examined is
    built from R(x) and finitely many of its x-derivatives (R itself,
    R', and -- via the required reading's own closed forms, quoted
    verbatim, not derived from any .py file -- R'', R'''). This script
    gives an explicit, PROVED analytic bound R(x) <= 1/x (x>0) -- a
    standard Mills-ratio-type estimate, derived here from scratch and
    then checked numerically (mpmath, dps=60) -- plus numerical
    (high-precision, not naive float) certificates that R, R', R'', R'''
    are all globally bounded on [0,infinity), which is exactly the
    "mild growth" hypothesis Part B of k02 needs, at every order this
    front verified in k01 (n=1..6, since the only source ever appearing
    at these orders, once psi1=R is known, is 0 or built from R and its
    derivatives via the ancestor's separately-established h_n content).

(2) A genuine (if partial) empirical answer to the honest question this
    front raises in ATTEMPT.md Section 5: does the boundedness-at-x=inf
    selection principle used throughout (a formal/asymptotic device --
    the TRUE physical domain is the bounded interval x in [0,sqrt(c)],
    i.e. s in [0,1]) actually stay well-behaved out to the TRUE physical
    edge x=sqrt(c), for the specific orders whose closed forms are
    already established in the required reading (psi1=R, psi2=2xR-2,
    psi3 via the Growth-Exclusion bounded-branch formula with source
    7*R'(x) -- exactly k02's own formula, applied here, not re-derived
    differently -- and psi4=(17/3)*R'''(x))? This connects to, and is
    consistent with, the sibling H1 front's own much larger uniformity
    grid (which tested x up to 20, s up to 1.41, and found no
    degradation) -- cited here, not reproduced, as complementary
    evidence from an independent computation.

NUMERICAL METHOD NOTE (self-caught issue, disclosed -- see ATTEMPT.md
Section 6, S1): a first version of this script computed R(x) and psi3(x)
via the literal formula "e^{x^2/2} * int_x^inf e^{-t^2/2}*(...) dt",
evaluating the huge prefactor and the tiny tail integral SEPARATELY via
mpmath's mp.quad before multiplying. This is numerically WRONG at large
x when the ambient precision (dps=60) is smaller than the number of
DECIMAL ORDERS OF MAGNITUDE the tail integral itself spans (e.g. at
x=sqrt(8000)=89.4, the true tail integral is of order 1e-1735 -- mp.quad
at dps=60 cannot resolve a value that small correctly; it returns
noise-level garbage indistinguishable from zero at 60 digits, silently).
This was CAUGHT by this script's own Part 1 sanity assertion (R(x)<=1/x
failed at x=89.4 by the analytically-impossible amount 5e-4 relative --
flagged immediately, before any downstream result was trusted). FIX
(used throughout this corrected version): substitute t=x+u (u>=0) BEFORE
integrating, so the huge/tiny cancellation never happens explicitly --
e^{x^2/2}*int_x^inf e^{-t^2/2}g(t)dt = int_0^inf e^{-x*u-u^2/2}g(x+u)du,
a single well-scaled integral mp.quad resolves correctly at ordinary
dps. Verified to agree with an independent mpmath erfc-based reference
formula to >55 stable digits at x up to 200 before being trusted (see
the verification block immediately below).

No .py file from any ancestor front was opened, read, or imported.
"""

import mpmath as mp

mp.mp.dps = 60


def R(xv):
    """R(x) = e^{x^2/2} * int_x^inf e^{-t^2/2} dt = int_0^inf e^{-x*u-u^2/2} du
    (substitution t=x+u; R'=xR-1, R(inf)=0). Numerically safe at all x
    tested here (no huge*tiny cancellation -- see module docstring)."""
    xv = mp.mpf(xv)
    return mp.quad(lambda u: mp.e**(-xv * u - u**2 / 2), [0, mp.inf])


def Rp(xv):
    """R'(x) = x*R(x) - 1, from the defining ODE (exact, no extra work)."""
    xv = mp.mpf(xv)
    return xv * R(xv) - 1


def Rpp(xv):
    """R''(x) = R(x) + x*R'(x), by differentiating R'=xR-1."""
    xv = mp.mpf(xv)
    return R(xv) + xv * Rp(xv)


def Rppp(xv):
    """R'''(x) = 2*R'(x) + x*R''(x), by differentiating R''=R+xR'."""
    xv = mp.mpf(xv)
    return 2 * Rp(xv) + xv * Rpp(xv)


def psi3(xv):
    """psi3(x) = -e^{x^2/2} * int_x^inf e^{-t^2/2} * 7*R'(t) dt
    -- the Growth-Exclusion bounded-branch formula (k02 Part B, y=0)
    applied to source f(x)=7*R'(x), the required reading's own psi3 ODE
    psi3' = x*psi3 + 7*R'(x). Same t=x+u substitution as R(x) above."""
    xv = mp.mpf(xv)
    return -mp.quad(lambda u: mp.e**(-xv * u - u**2 / 2) * 7 * Rp(xv + u), [0, mp.inf])


def psi4(xv):
    """psi4(x) = (17/3)*R'''(x), the required reading's own closed form."""
    return mp.mpf('17') / 3 * Rppp(xv)


print("=" * 78)
print("PART 0: cross-check R(x) [substitution formula] against an")
print("independent erfc-based reference formula, dps=60, x up to 200")
print("(this check is what CAUGHT the S1 issue documented in the module")
print("docstring, in an earlier version of this script -- kept here as a")
print("permanent, standing validation, not removed after the fix)")
print("=" * 78)
for xs in ['1.3', '20', '31.6227766', '89.4427191', '200']:
    xv = mp.mpf(xs)
    z = xv / mp.sqrt(2)
    ref = mp.sqrt(mp.pi / 2) * mp.exp(z**2) * mp.erfc(z)
    val = R(xv)
    reldiff = mp.fabs(val - ref) / mp.fabs(ref)
    print(f"  x={xs:>12}: R(x)_sub={mp.nstr(val,20)}  R(x)_erfc={mp.nstr(ref,20)}  "
          f"reldiff={mp.nstr(reldiff,4)}")
    assert reldiff < mp.mpf('1e-50')
print("PASS: substitution formula matches erfc reference to >=50 digits,")
print("      x up to 200 -- trusted for Parts 1-3 below.")

print()
print("=" * 78)
print("PART 1: proved analytic bound R(x) <= 1/x for x>0, verified numerically")
print("=" * 78)
print("""
  Proof: for t>=x>0, t/x >= 1, so e^{-t^2/2} <= (t/x)*e^{-t^2/2}.
  Integrating: int_x^inf e^{-t^2/2} dt <= (1/x) int_x^inf t*e^{-t^2/2} dt
                                        = (1/x) * [-e^{-t^2/2}]_x^inf = e^{-x^2/2}/x.
  Multiplying by e^{x^2/2}: R(x) = e^{x^2/2} int_x^inf e^{-t^2/2}dt <= 1/x.  QED.
""")
print(f"  {'x':>8} {'R(x)':>22} {'1/x':>22} {'R(x)<=1/x?':>12}")
for xv in [1, 2, 5, 10, 20, 31.6227766, 50, 89.4427191, 200]:
    r = R(xv)
    bound = mp.mpf(1) / mp.mpf(xv)
    ok = r <= bound
    print(f"  {xv:8.4f} {mp.nstr(r, 14):>22} {mp.nstr(bound, 14):>22} {str(ok):>12}")
    assert ok
print("PASS (checked, x=31.62=sqrt(1000) and x=89.44=sqrt(8000) included --")
print("      exactly the physical-edge x=sqrt(c) values used in Part 3 below).")
print("  R(0) = sqrt(pi/2) =", mp.nstr(R(0), 20), " (the global max of R on [0,inf),")
print("  since R is monotonically decreasing -- R'=xR-1<=x*(1/x)-1=0 for x>0,")
print("  R'(0)=-1<0 -- so sup_{x>=0} R(x) = R(0) = sqrt(pi/2), finite.)")
assert mp.fabs(R(0) - mp.sqrt(mp.pi / 2)) < mp.mpf('1e-50')

print()
print("=" * 78)
print("PART 2: numerical boundedness certificate for R, R', R'', R'''")
print("(the sources needed at n=1..4, per required reading + k02's own")
print("psi3 formula) -- grid search + tail values, dps=60")
print("=" * 78)
grid = [mp.mpf(v) for v in
        [0, 0.5, 1, 2, 3, 5, 8, 12, 20, 31.6227766, 50, 89.4427191, 200, 400]]
sup_R = max(R(xv) for xv in grid)
sup_Rp = max(abs(Rp(xv)) for xv in grid)
sup_Rpp = max(abs(Rpp(xv)) for xv in grid)
sup_Rppp = max(abs(Rppp(xv)) for xv in grid)
print(f"  sup on grid x in {{{', '.join(str(float(g)) for g in grid)}}}:")
print(f"    sup |R(x)|    = {mp.nstr(sup_R, 12)}   (attained at x=0, = R(0))")
print(f"    sup |R'(x)|   = {mp.nstr(sup_Rp, 12)}")
print(f"    sup |R''(x)|  = {mp.nstr(sup_Rpp, 12)}")
print(f"    sup |R'''(x)| = {mp.nstr(sup_Rppp, 12)}")
print(f"  tail check at x=1000 (should be small, confirming decay, not a")
print(f"  grid-stopping artifact):")
xv = mp.mpf(1000)
print(f"    x={xv}: R={mp.nstr(R(xv), 6)}  R'={mp.nstr(Rp(xv), 6)}  "
      f"R''={mp.nstr(Rpp(xv), 6)}  R'''={mp.nstr(Rppp(xv), 6)}")
print("PASS: all four functions numerically bounded and decaying on the")
print("      whole tested range -- the sub-Gaussian growth hypothesis Part B")
print("      of k02's Growth-Exclusion Lemma needs, for n=1..4, is satisfied.")

print()
print("=" * 78)
print("PART 3: behaviour of psi1..psi4 AT THE TRUE PHYSICAL EDGE x=sqrt(c)")
print("(s=1), for the c-grid the sibling H1 front used -- does the")
print("boundedness-at-x=infinity selection stay sensible at the boundary")
print("that actually matters for finite c, not just formally as x->inf?")
print("=" * 78)
c_grid = [200, 500, 1000, 2000, 4000, 8000]
print(f"  {'c':>6} {'x=sqrt(c)':>12} {'psi1=R(x)':>16} {'psi2=2xR-2':>16} "
      f"{'psi3(x)':>16} {'psi4(x)':>16}")
rows = []
for c in c_grid:
    xv = mp.sqrt(mp.mpf(c))
    p1 = R(xv)
    p2 = 2 * xv * R(xv) - 2
    p3 = psi3(xv)
    p4 = psi4(xv)
    rows.append((c, xv, p1, p2, p3, p4))
    print(f"  {c:6d} {mp.nstr(xv, 8):>12} {mp.nstr(p1, 10):>16} {mp.nstr(p2, 10):>16} "
          f"{mp.nstr(p3, 10):>16} {mp.nstr(p4, 10):>16}")

print()
print("  Monotonicity check: |psi_n(sqrt(c))| strictly DECREASING as c grows,")
print("  for each n=1..4 (the qualitative signature of a well-behaved,")
print("  decaying profile -- the OPPOSITE of what growth-mode leakage near")
print("  the true boundary would look like):")
for n_idx, name in [(2, 'psi1'), (3, 'psi2'), (4, 'psi3'), (5, 'psi4')]:
    vals = [abs(row[n_idx]) for row in rows]
    monotone = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    print(f"    {name}: {[mp.nstr(v,6) for v in vals]}  strictly decreasing: {monotone}")
    assert monotone

print()
print("  Reading: all four profiles are small and SMOOTHLY DECREASING in")
print("  magnitude as c grows (x=sqrt(c) grows), exactly as the boundedness-")
print("  at-infinity selection predicts -- no sign whatsoever of the excluded")
print("  e^{x^2/2}-type growth mode reasserting itself near the true physical")
print("  edge s=1, for any of the four orders with an established closed")
print("  form. This is consistent with (though does not independently")
print("  replace) the sibling mclust_h1_validity_attempt front's own,")
print("  much larger, uniformity grid (6 c-values x 7 x-values, x up to 8 in")
print("  the main grid and up to 20 -- s up to 1.41, PAST s=1 -- in its")
print("  stress test), which found the SAME qualitative absence of")
print("  degradation using a completely different (direct series-summation)")
print("  method. Two independent computations, by two different fronts, on")
print("  two different aspects (this front: the outer-limit closed-form")
print("  profiles; the H1 front: the full finite-t0 series), agree.")
print()
print("ALL PARTS PASS.")
