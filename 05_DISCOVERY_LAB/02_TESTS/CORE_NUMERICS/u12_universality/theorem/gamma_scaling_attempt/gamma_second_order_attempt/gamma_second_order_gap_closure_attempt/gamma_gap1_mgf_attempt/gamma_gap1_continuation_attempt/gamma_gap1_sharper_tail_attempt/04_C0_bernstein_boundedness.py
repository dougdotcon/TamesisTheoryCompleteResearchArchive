"""
GAMMA-GAP1-SHARPER-TAIL-ATTEMPT, script 04.

This is the flagship structural finding of this front.

Setup (cited from required reading, kappa_0(gamma), lambda(gamma) from the
continuation front, Estagio 36; hat-lambda(gamma) from the continuation
front's own Step 3, the growth rate of the EXPLICIT crude hat-G(n,gamma)
bound used in the actual assembled n_0(gamma) construction -- NOT the
tighter idealized asymptotic lambda(gamma)):

  beta(gamma)      := gamma*(2-gamma)/2
  kappa_0(gamma)   := 8/(gamma*(2-gamma))               [Estagio 36]
  lambda(gamma)    := kappa_0(gamma)*(3/2-gamma)
                     = 4*(3-2*gamma)/(gamma*(2-gamma))   [Estagio 36, UNBOUNDED on (0,1)]
  hat-lambda(gamma):= 16*(7/4-gamma)/beta(gamma)          [continuation Step 3]

Under Hoeffding, the Bulk/Tail Lemma's split constant C must satisfy
  C^2 > 1/4 + hat-lambda(gamma)/2  =:  C0_Hoeffding(gamma)^2.
Since hat-lambda(gamma) -> +infinity as gamma->0+ (same divergence as
lambda(gamma), same root cause: kappa_0(gamma)~4/gamma), NO single
gamma-independent C works on all of (0,1) under Hoeffding -- this is the
continuation front's own already-catalogued finding, reproduced here as the
baseline.

Under Bernstein-with-slack-a (script 03), the analogous threshold is
  C^2 > (2+a)*sigma^2(gamma)*(hat-lambda(gamma)+1/2) =: C0_Bernstein(gamma,a)^2,
  sigma^2(gamma):=gamma(1-gamma).

THE KEY NEW FACT PROVED HERE (exact algebra, not just numeric sampling):
C0_Bernstein(gamma,a)^2 is BOUNDED on the entire open interval (0,1), for
every fixed a>0 -- because sigma^2(gamma)*hat-lambda(gamma) itself has a
FINITE limit as gamma->0+ (the shrinking variance sigma^2~gamma exactly
compensates the divergence hat-lambda~28/gamma coming from kappa_0~4/gamma).
This directly resolves, via a different tail-control technique, the very
unboundedness that the continuation front (Estagio 36) proved for
lambda(gamma)/hat-lambda(gamma) alone: a SINGLE gamma-independent C now
works uniformly across the ENTIRE open interval (0,1), not merely on
compact subsets [gamma_0,1) as under Hoeffding.
"""
import sympy as sp

gam, a = sp.symbols('gamma a', positive=True)
beta = gam * (2 - gam) / 2
kappa0 = 4 / beta
lam = sp.simplify(kappa0 * (sp.Rational(3, 2) - gam))
hatlam = sp.simplify(16 * (sp.Rational(7, 4) - gam) / beta)
sigma2 = gam * (1 - gam)

print("beta(gamma)        =", beta)
print("kappa_0(gamma)      =", sp.simplify(kappa0))
print("lambda(gamma)       =", lam, "  (continuation front, Estagio 36; UNBOUNDED as gamma->0)")
print("hat-lambda(gamma)   =", hatlam, "  (continuation front Step 3; growth rate of the EXPLICIT hat-G)")
print()

C0H_sq = sp.simplify(sp.Rational(1, 4) + hatlam / 2)
C0B_sq = sp.simplify((2 + a) * sigma2 * (hatlam + sp.Rational(1, 2)))
print("C0_Hoeffding(gamma)^2  = 1/4 + hat-lambda/2          =", C0H_sq)
print("C0_Bernstein(gamma,a)^2 = (2+a)*sigma^2*(hat-lambda+1/2) =", C0B_sq)

print()
print("=" * 78)
print("Sanity check: reproduces the continuation front's own published C(gamma)")
print("=" * 78)
for gv, pred_C in [(sp.Rational(99, 100), 4.23), (sp.Rational(1, 100), 44.89)]:
    C0H = sp.sqrt(C0H_sq.subs(gam, gv))
    myC = float(sp.Rational(6, 5) * C0H)
    print(f"gamma={float(gv)}: 1.2*C0_Hoeffding = {myC:.4f}  (continuation's published C(gamma) = {pred_C})")

print()
print("=" * 78)
print("C0_Hoeffding(gamma)^2 DIVERGES as gamma->0+ (baseline, already known)")
print("=" * 78)
lim0H = sp.limit(C0H_sq, gam, 0, dir='+')
print("lim_{gamma->0+} C0_Hoeffding^2 =", lim0H)
assert lim0H is sp.oo

print()
print("=" * 78)
print("C0_Bernstein(gamma,a)^2 is BOUNDED on (0,1) for EVERY fixed a>0 -- the")
print("key new structural finding of this front (exact algebra, not sampling)")
print("=" * 78)
for a_val in [sp.Rational(1, 20), sp.Rational(1, 10), sp.Rational(1, 5), 1, 2]:
    lim0B = sp.limit(C0B_sq.subs(a, a_val), gam, 0, dir='+')
    lim1B = sp.limit(C0B_sq.subs(a, a_val), gam, 1, dir='-')
    print(f"a={float(a_val):<6}: lim_{{gamma->0+}} C0_Bernstein^2 = {lim0B} = {float(lim0B):.3f}  "
          f"(FINITE)   lim_{{gamma->1-}} = {lim1B}")
    assert lim0B.is_finite

general_lim0 = sp.simplify(sp.limit(C0B_sq, gam, 0, dir='+'))
print()
print("General closed form of the boundary value as a function of a:")
print("  lim_{gamma->0+} C0_Bernstein(gamma,a)^2 =", general_lim0, "  (finite for every a>0)")

print()
print("=" * 78)
print("Exact-algebra proof that C0_Bernstein(gamma,a)^2 is monotone DECREASING")
print("on (0,1) for every fixed a>0 (hence sup = the gamma->0+ boundary value")
print("above, attained only in the limit; inf = 0 at gamma->1-)")
print("=" * 78)
# d/dgamma of C0B_sq(gamma,a) has a numerator independent of 'a' up to the
# overall (2+a) prefactor (which does not affect where the derivative
# vanishes) -- so it suffices to certify sign for one representative a.
f = sp.simplify(C0B_sq.subs(a, 1))
fprime = sp.simplify(sp.diff(f, gam))
num, den = sp.fraction(sp.together(fprime))
num = sp.expand(num)
print("f(gamma) := C0_Bernstein(gamma,a=1)^2 =", f)
print("f'(gamma) numerator =", num)
roots = sp.real_roots(sp.Poly(num, gam))
print("real roots of the numerator:", [float(r) for r in roots])
roots_in_01 = [r for r in roots if 0 < r < 1]
print("real roots inside (0,1):", roots_in_01, " (must be empty)")
assert roots_in_01 == []
val_mid = float(num.subs(gam, sp.Rational(1, 2)))
print(f"numerator at gamma=1/2 (representative interior point): {val_mid}  "
      f"(sign is then constant throughout (0,1), since no root exists there)")
assert val_mid < 0
print("=> f'(gamma) < 0 throughout (0,1): C0_Bernstein(gamma,a)^2 is exact-algebra-")
print("   proved STRICTLY DECREASING on (0,1), for every fixed a>0 (the (2+a)")
print("   prefactor scales f but does not move the roots of f').")

print()
print("=" * 78)
print("Concrete table: C0_Hoeffding vs C0_Bernstein(a=0.05), the value used in")
print("this front's final n_0(gamma) construction (script 05)")
print("=" * 78)
A_FINAL = sp.Rational(1, 20)
print(f"{'gamma':>7} | {'C0_Hoeffding':>13} | {'C0_Bernstein(a=0.05)':>21} | {'ratio C0B/C0H':>13}")
for gv in [sp.Rational(99, 100), sp.Rational(9, 10), sp.Rational(7, 10), sp.Rational(1, 2),
           sp.Rational(3, 10), sp.Rational(1, 10), sp.Rational(1, 20), sp.Rational(1, 100)]:
    ch = sp.sqrt(C0H_sq.subs(gam, gv))
    cb = sp.sqrt(C0B_sq.subs({gam: gv, a: A_FINAL}))
    print(f"{float(gv):7.2f} | {float(ch):13.4f} | {float(cb):21.4f} | {float(cb / ch):13.4f}")

print()
print("Dense numeric scan confirming the exact-algebra sup, a=0.05:")
import mpmath as mp
mp.mp.dps = 30
maxv = mp.mpf(0)
argmax = None
for i in range(1, 20000):
    g = mp.mpf(i) / 20000
    sigma2n = g * (1 - g)
    hatlamn = 16 * (mp.mpf(7) / 4 - g) / (g * (2 - g) / 2)
    v = (mp.mpf(2) + mp.mpf('0.05')) * sigma2n * (hatlamn + mp.mpf('0.5'))
    if v > maxv:
        maxv = v
        argmax = g
print(f"numeric sup over 19999-point grid: {float(maxv):.5f} at gamma={float(argmax):.5f}")
print(f"exact-algebra predicted sup (gamma->0+): {float(sp.N(general_lim0.subs(a, A_FINAL))):.5f}")

print()
print("CONCLUSION: unlike lambda(gamma)/hat-lambda(gamma) alone (Hoeffding route,")
print("provably unbounded, continuation front Estagio 36), C0_Bernstein(gamma,a)^2")
print("is exact-algebra-proved BOUNDED and MONOTONE on the entire open interval")
print("(0,1) for every fixed a>0. A SINGLE gamma-independent C now suffices for")
print("the ENTIRE open interval (0,1), not just compact subsets [gamma_0,1).")
