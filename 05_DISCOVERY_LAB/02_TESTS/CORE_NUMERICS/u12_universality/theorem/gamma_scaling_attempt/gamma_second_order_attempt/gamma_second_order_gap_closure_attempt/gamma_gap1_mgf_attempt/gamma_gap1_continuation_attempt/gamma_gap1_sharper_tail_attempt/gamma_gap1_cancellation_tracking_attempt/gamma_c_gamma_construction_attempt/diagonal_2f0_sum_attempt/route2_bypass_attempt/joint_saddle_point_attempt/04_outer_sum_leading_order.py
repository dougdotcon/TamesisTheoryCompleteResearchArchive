"""
Script 04: the OUTER sum S_n' = sum_m term_m, leading order, via the
mesoscale profile T_prof(lambda,gamma) derived and verified in script 03.

Central claim of this script (this front's main positive deliverable):

  Treating the sum over m as a continuum integral at leading order
  (Euler-Maclaurin leading term), and substituting m = lambda*sqrt(n),
  dm = sqrt(n) d(lambda):

    S_n' = sum_{m=0}^n term_m  ~  sqrt(n) * Int_0^infty T_prof(lambda,gamma) d(lambda)

  and this integral evaluates, IN CLOSED FORM, to EXACTLY

    Int_0^infty T_prof(lambda,gamma) d(lambda) = (1/2) sqrt(pi/beta),
    beta := gamma(2-gamma)/2,

  i.e. EXACTLY the coefficient of sqrt(n) in G_n := (1/2) sqrt(pi n / beta)
  -- the already-PROVED (Lemma D0 chain, ultimately Theorem 2 of the
  wave-17 front) leading asymptotic of S_n. This is a genuine,
  parameter-free consistency check of the ENTIRE joint saddle-point
  machinery built in scripts 01-03 (Beta-integral closed form -> inner
  Laplace saddle -> Stirling on the outer prefactor -> continuum limit
  over m) against a fact that was NOT used anywhere in deriving
  T_prof(lambda,gamma) -- it emerges, unforced.

Part A: symbolic verification of the integral identity.
Part B: direct high-precision numerical confirmation that S_n' - G_n
        stays BOUNDED (does not diverge) as n grows, at several gamma --
        consistent with (necessary, not sufficient, for) the target
        S_n = G_n + D(gamma) + o(1) statement, and a check that this
        front's numerics reproduce the ancestor-established D(gamma)
        table to within the precision reachable at the n practical here
        (this is NOT a derivation of D(gamma); it is an end-to-end
        numerical sanity check of the whole pipeline, using this front's
        OWN Beta-integral route, independent of every ancestor's raw-sum
        route).
Part C: precise diagnosis, quantified where possible, of exactly what
        additional terms (uniform Watson's-lemma correction to the inner
        integral; Euler-Maclaurin/Poisson correction to the outer sum)
        would be needed to push from "leading sqrt(n) order confirmed"
        to "O(1) constant D(gamma) derived" -- the honest scope boundary
        of this front.
"""
import sympy as sp
import mpmath as mp
from fractions import Fraction as F
from math import comb, factorial

mp.mp.dps = 50

print("=" * 78)
print("Part A: symbolic confirmation that Int_0^inf T_prof(lambda,gamma) dlambda")
print("        EXACTLY equals the G_n coefficient (1/2) sqrt(pi/beta)")
print("=" * 78)

# gamma restricted to (0,1) (its actual domain here) so that 2-gamma is a
# positive real, which is what selects the convergent-Gaussian branch of
# sympy's own Piecewise integral result below.
gamma = sp.symbols('gamma', positive=True)
lam = sp.symbols('lambda', positive=True)
beta = sp.symbols('beta', positive=True)
A_gamma = (2 - gamma) / (2 * gamma)
T_prof = (1 / gamma) * sp.exp(-A_gamma * lam ** 2)

integral_full = sp.integrate(T_prof, (lam, 0, sp.oo))
print("Int_0^inf T_prof(lambda,gamma) d(lambda) [sympy raw, Piecewise since")
print("gamma's domain wasn't pinned to (0,1) inside the integrand itself]:")
print(" ", integral_full)
# Self-caught issue: a first version of this check tried sp.simplify(integral_full
# - target_sub) == 0 directly and it did NOT auto-resolve to 0, even though the
# printed Piecewise's FIRST branch (condition |arg(2-gamma)|<=pi/2, which holds
# for every gamma in (0,2), i.e. always here) is EXACTLY equal to the target --
# a sympy simplification-under-branch-conditions limitation, not a real
# mismatch. Fixed by extracting that first branch explicitly (rather than
# relying on sp.simplify to select it) and confirming it symbolically, THEN
# cross-checking with a numeric sweep over rational gamma in (0,1) as a fully
# independent second confirmation route.
integral = integral_full.args[0][0]  # the branch valid for gamma in (0,2)
print("First (gamma in (0,2)-valid) branch, extracted directly:", integral)

target = sp.Rational(1, 2) * sp.sqrt(sp.pi / beta)
beta_def = gamma * (2 - gamma) / 2
target_sub = sp.simplify(target.subs(beta, beta_def))
print("(1/2) sqrt(pi/beta), beta=gamma(2-gamma)/2, substituted =", target_sub)

diff = sp.simplify(integral - target_sub)
print("Difference (symbolic):", diff)
assert diff == 0, "The leading-order sqrt(n) coefficients do NOT match (symbolic)!"

print()
print("Independent numeric cross-check (rational gamma in (0,1), sympy N()):")
max_num_diff = 0
for gnum, gden in [(1, 7), (1, 3), (2, 5), (1, 2), (3, 4), (9, 10)]:
    g_val = sp.Rational(gnum, gden)
    lhs = float(integral.subs(gamma, g_val))
    rhs = float(target_sub.subs(gamma, g_val))
    d = abs(lhs - rhs)
    max_num_diff = max(max_num_diff, d)
    print(f"  gamma={gnum}/{gden}: integral={lhs:.15f}  target={rhs:.15f}  diff={d:.3e}")
assert max_num_diff < 1e-12
print()
print(">>> CONFIRMED, symbolically, exactly: Int_0^inf T_prof(lambda,gamma) dlambda")
print(">>>   = (1/2) sqrt(pi/beta) = the EXACT, already-PROVED coefficient of")
print(">>>   sqrt(n) in G_n = (1/2) sqrt(pi n/beta).")
print(">>> This is a genuine, unforced, parameter-free cross-check: nothing in the")
print(">>> derivation of T_prof (script 03) used G_n or beta as an input.")

print()
print("=" * 78)
print("Part B: numerical check that S_n' - G_n stays bounded as n grows")
print("        (necessary condition for S_n = G_n + D(gamma) + o(1))")
print("=" * 78)


def T_nm_direct_frac(n, m, gamma_frac):
    total = F(0)
    for j in range(0, n - m + 1):
        total += comb(j + m, m) * comb(n - j, m) * ((1 - gamma_frac) ** j)
    return total


def Sn_prime_exact_via_swap(n, gamma_frac):
    total = F(0)
    for m in range(0, n + 1):
        total += (gamma_frac ** m) * factorial(m) * T_nm_direct_frac(n, m, gamma_frac) / (n ** m)
    return total


def G_n_mp(n, gamma_mp):
    beta_mp = gamma_mp * (2 - gamma_mp) / 2
    return sp.Rational(1, 2) * mp.sqrt(mp.pi * n / beta_mp) if False else mp.mpf('0.5') * mp.sqrt(mp.pi * n / beta_mp)


def D_gamma_known(gamma_mp):
    """D(gamma) = -(1/3)(6-8g+3g^2)/(2-g)^2, the ancestor-established (Lemma E)
    closed form the wave-17 conjectured C(gamma) is exactly equivalent to."""
    return -(mp.mpf(1) / 3) * (6 - 8 * gamma_mp + 3 * gamma_mp ** 2) / (2 - gamma_mp) ** 2


print("(Using the exact double-sum-swap route, script 01's own independently")
print(" re-derived identity, for a direct, ancestor-independent numeric check.)")
print()
for gnum, gden in [(1, 3), (1, 2), (2, 3)]:
    g_frac = F(gnum, gden)
    g_mp = mp.mpf(gnum) / mp.mpf(gden)
    D_known = D_gamma_known(g_mp)
    print(f"gamma={gnum}/{gden}:  known D(gamma) = {mp.nstr(D_known, 10)}, "
          f"target S_n'-G_n -> D(gamma)+1 = {mp.nstr(D_known+1, 10)}")
    for n_val in [50, 100, 200, 400]:
        Sn_prime = Sn_prime_exact_via_swap(n_val, g_frac)
        Sn_prime_mp = mp.mpf(Sn_prime.numerator) / mp.mpf(Sn_prime.denominator)
        Gn = G_n_mp(n_val, g_mp)
        resid = Sn_prime_mp - Gn
        print(f"    n={n_val:>4}: S_n'={mp.nstr(Sn_prime_mp,10)}  G_n={mp.nstr(Gn,10)}  "
              f"S_n'-G_n={mp.nstr(resid,8)}")
    print()

print("Interpretation: the residual S_n'-G_n should be converging toward the")
print("constant D(gamma)+1 (slowly, at the O(n^-1/2) rate this whole sub-lineage")
print("has documented since Lemma D0) as n grows -- consistent with (not a proof")
print("of) the target asymptotic. This uses exact rational arithmetic up to")
print("n=400 (script 01's route); pushing further exactly is combinatorially")
print("expensive (the double sum has O(n^2) terms of growing bit-length) -- a")
print("resource, not mathematical, limitation, matching this lineage's own")
print("convention of disclosing such limits rather than silently stopping.")

print()
print("=" * 78)
print("Part C: precise diagnosis of what remains for the O(1) constant D(gamma)")
print("=" * 78)
print("""
What THIS FRONT established (Parts A-B, scripts 01-03), precisely:
  (1) T(n,m) = Beta-integral closed form (script 01) -- re-verified, not
      new to this front (referee's own extension of the predecessor).
  (2) The INNER saddle t*(n,m,gamma), EXACT closed form (script 02) --
      new. g''(t*)<0 confirmed; t* ~ m/(gamma n) leading order confirmed.
  (3) The MESOSCALE limit profile T_prof(lambda,gamma) = (1/gamma) *
      exp(-((2-gamma)/(2 gamma)) lambda^2), lambda=m/sqrt(n) -- new,
      derived via Laplace/Stirling and independently confirmed numerically
      (script 03, <0.1%-2% relative error depending on lambda, tightening
      as n grows, and shown NOT to be extrapolation noise at the one
      point checked most carefully).
  (4) Int_0^inf T_prof(lambda,gamma) dlambda = (1/2) sqrt(pi/beta) EXACTLY
      -- reproduces the ALREADY-PROVED leading sqrt(n) coefficient of
      S_n, via a route that never used that fact as an input. (Part A.)

What this front did NOT establish -- the precise gap to D(gamma):
  (a) A UNIFORM error bound on the inner Laplace approximation (step 3),
      valid uniformly over m=O(sqrt n) with an EXPLICIT, summable
      remainder -- what was used is a leading-order Laplace/Watson
      approximation with relative error checked to shrink numerically,
      not bounded analytically. The direct analogue of Gap 1's own
      "uniform Taylor-remainder-with-moments bound" requirement
      (gamma_second_order_attempt/ATTEMPT.md Section 5), now for the
      Beta-tilted-moment integral instead of the Binomial MGF.
  (b) The NEXT-ORDER (O(1/sqrt n)) correction to T_prof itself -- i.e.
      T_prof_1(lambda,gamma) in T_prof(lambda,gamma) + T_prof_1(lambda,gamma)/
      sqrt(n) + o(1/sqrt(n)) -- requires carrying the Laplace/Watson
      expansion (script 02-03's g(t*) computation) one order further:
      the next term in Watson's lemma (involving g'''(t*), g''''(t*),
      not just g''(t*)), PLUS the next Stirling correction to m! and to
      (n+m+1)!/(n-m)!, PLUS the (2m+1)/n and m^3/n^2 terms this front's
      own script 03 working notes explicitly dropped as o(1) at leading
      order (script 03 header) -- each of these individually o(1) at
      FIXED lambda, but their SUM, integrated against the O(sqrt n)-many
      terms of the outer sum, contributes at the SAME O(1) order as
      D(gamma) itself (exactly the mechanism that made Lemma D0's own
      correction term, `gamma_second_order_attempt/ATTEMPT.md` Section 3,
      delicate -- an O(k^2/n^2) term that looked negligible pointwise but
      summed to a genuine O(n^-1/2) correction).
  (c) An Euler-Maclaurin / Poisson-summation treatment of
      sum_m T_prof(m/sqrt(n),gamma) (continuum-limit correction, replacing
      Part A's leading-order integral with a discrete sum plus the
      O(1)-order boundary/lattice corrections) -- the direct analogue of
      what Lemma D0 (`gamma_second_order_attempt/ATTEMPT.md` Section 3)
      did for the ORIGINAL k-sum, now needed a SECOND time, for the
      swapped m-sum, and coupled to (b) since the summand itself is only
      known to the precision of (b).
  (d) Combining (b) and (c) into a single, jointly-controlled two-
      variable (t,m) asymptotic with an EXPLICIT o(1) remainder -- the
      literal target the dispatching mandate names.

None of (a)-(d) was completed by this front. This matches the mandate's
own risk disclosure precisely: getting THIS FAR (a verified, closed-form
mesoscale profile whose leading-order sum reproduces a known PROVED fact
exactly) required a genuine two-level Laplace/Stirling derivation; going
the remaining distance to an O(1) constant requires AT LEAST two more
independent orders of asymptotic control (inner Watson's-lemma next
order; outer Euler-Maclaurin next order), each individually comparable in
technical weight to what Gap 1's six prior fronts have found insufficient
time/technique to close in one pass.
""")
