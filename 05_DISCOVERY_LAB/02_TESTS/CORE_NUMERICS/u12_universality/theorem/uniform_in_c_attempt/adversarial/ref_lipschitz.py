"""
Adversarial referee -- items 1 and 2.

(i)   Lema 3.1 (equi-Lipschitz, constant 1, uniform in n): explicit coupling
      re-built here, then stress-tested exactly.
(ii)  The non-monotonicity remark of ATTEMPT 3.1(ii): the n=3 example is
      reproduced, and the SHARPER counterexample the remark actually needs
      (the event {1 cyclic} itself flipping UP under the shared-V coupling)
      is exhibited.
(iii) Teorema A: the sub-bound sup_c |phi_inf'(c)| <= 1/3, and the explicit
      finite-n grid inequality omega_n(C) <= max_i |Delta_n(iC/M)| + 4C/(3M).
"""

from fractions import Fraction as F
import mpmath as mp

from ref_engine import chain_phi, chain_phi_float

mp.mp.dps = 40


def cyclic_points(f):
    """set of points lying on a cycle of the functional digraph x -> f[x]."""
    n = len(f)
    out = set()
    for s in range(n):
        x, seen = s, {s}
        for _ in range(n):
            x = f[x]
            if x == s:
                out.add(s)
                break
            if x in seen:
                break
            seen.add(x)
    return out


def build_f(n, pi, S, U):
    """f(x) = U[x] if x in S else pi[x].  0-indexed."""
    f = list(pi)
    for x in S:
        f[x] = U[x]
    return f


print("=" * 74)
print("1. LEMA 3.1 -- the coupling, re-built and audited")
print("=" * 74)
print("""
Coupling (re-derived independently):  0 <= c < c' <= n.  On one space take
V_1..V_n iid U(0,1), xi_i := 1{V_i < c/n}, xi'_i := 1{V_i < c'/n}; take ONE
uniform permutation pi and ONE family U_1..U_n of iid Uniform[n], shared.
  * marginals: (pi, xi, U) has exactly the Definition-1 law at c, and
    (pi, xi', U) exactly the law at c'.  [xi_i iid Bern(c/n); xi'_i iid
    Bern(c'/n); pi and U independent of the V's in both.]
  * E := {xi_i = xi'_i for all i}.  On E, f(x) = U_x 1{xi_x=1} + pi(x)
    1{xi_x=0} coincides with f' TERM BY TERM at every x, so f = f' as maps,
    hence 1{1 cyclic for f} = 1{1 cyclic for f'} pointwise on E.
  * |phi(n,c)-phi(n,c')| = |E[1_A - 1_A']| <= E|1_A - 1_A'| = P(A tri A')
    <= P(E^c) <= sum_i P(xi_i != xi'_i) = n * (c'-c)/n = c'-c.
  * reduction to c' <= n: under Definition 1's q = min(c/n,1), phi(n,.) is
    constant on [n,inf), so for c <= n < c' the LHS equals |phi(n,c)-phi(n,n)|
    <= n-c <= c'-c, and for n <= c < c' the LHS is 0.  VALID.
Verdict on the argument: correct, and the constant 1 is uniform in n.
""")

print("Exact stress test of |phi(n,c)-phi(n,c')| <= |c-c'| :")
qs = [F(k, 12) for k in range(13)]
worst = F(0)
viol = 0
ncell = 0
for n in range(1, 9):
    vals = {q: chain_phi(n, q) for q in qs}
    for a in qs:
        for b in qs:
            if a >= b:
                continue
            ncell += 1
            lhs = abs(vals[a] - vals[b])
            rhs = (b - a) * n          # |c - c'| = n |q - q'|
            if lhs > rhs:
                viol += 1
                print("   VIOLATION", n, a, b, lhs, rhs)
            r = lhs / rhs
            if r > worst:
                worst = r
print(f"   n=1..8, all {ncell} pairs on a 13-point q-grid: {viol} violations.")
print(f"   worst ratio |dphi| / |dc| = {float(worst):.6f} "
      f"(= {worst}) -- comfortably below 1.")

print()
print("   Sharper: is the TRUE Lipschitz constant <= 1/3 (ATTEMPT 3.2)?")
for n in (2, 4, 8, 16):
    m = 200
    vals = [chain_phi(n, F(k, m)) for k in range(m + 1)]
    mx = max(abs(vals[k + 1] - vals[k]) * m / n for k in range(m))
    print(f"     n={n:3d}  max grid slope = {float(mx):.8f}   "
          f"1/3 - 1/(3n^2) = {float(F(1,3) - F(1, 3*n*n)):.8f}")

print()
print("=" * 74)
print("2. The non-monotonicity remark of ATTEMPT 3.1(ii)")
print("=" * 74)
pi = [1, 2, 0]          # 0->1->2->0, i.e. the cycle (1 2 3) in 1-indexing
fA = build_f(3, pi, {0}, [0, 0, 0])
fB = build_f(3, pi, {0, 1}, [0, 1, 0])
print(f"   pi = (1 2 3);  reroute {{1}}, U_1=1   -> f = {[x+1 for x in fA]}"
      f"   cyclic points = {sorted(x+1 for x in cyclic_points(fA))}"
      f"   count = {len(cyclic_points(fA))}")
print(f"   pi = (1 2 3);  reroute {{1,2}}, U_1=1,U_2=2 -> f = {[x+1 for x in fB]}"
      f"   cyclic points = {sorted(x+1 for x in cyclic_points(fB))}"
      f"   count = {len(cyclic_points(fB))}")
print("   => the document's stated counterexample REPRODUCES exactly:")
print("      adding one reroute took the cyclic COUNT from 1 to 2.")
print()
print("   BUT note what it does and does not show: 1 is cyclic in BOTH")
print("   configurations, so this example does not by itself show the")
print("   *event* {1 cyclic} -- the only functional phi(n,.) depends on --")
print("   is non-monotone.  Here is a counterexample that does, and that is")
print("   realisable inside Lema 3.1's own shared-(pi,U) coupling:")
pi2 = [0, 1]                       # pi = identity on {1,2}
fC = build_f(2, pi2, {0}, [1, 0])          # xi = (1,0)
fD = build_f(2, pi2, {0, 1}, [1, 0])       # xi'= (1,1), SAME pi, SAME U
print(f"      n=2, pi=id, U_1=2, U_2=1.")
print(f"      xi =(1,0): f  = {[x+1 for x in fC]}  -> 1 cyclic? "
      f"{0 in cyclic_points(fC)}")
print(f"      xi'=(1,1): f' = {[x+1 for x in fD]}  -> 1 cyclic? "
      f"{0 in cyclic_points(fD)}")
print("      Same pi, same U, xi <= xi' pointwise, and the indicator goes")
print("      0 -> 1.  So {1 cyclic} is genuinely NOT monotone in xi, and no")
print("      monotone-coupling proof of monotonicity of phi(n,.) exists.")
print("      The document's conclusion is right; its example is weaker than")
print("      its conclusion.  (Nothing downstream depends on either.)")

print()
print("=" * 74)
print("3. TEOREMA A -- the two constants and the grid inequality")
print("=" * 74)
print("""
phi_inf(c) = int_0^1 e^{-c t^2} dt.  Differentiation under the integral is
legitimate (|d/dc e^{-ct^2}| = t^2 e^{-ct^2} <= t^2, integrable, uniformly for
c >= 0), giving phi_inf'(c) = -int_0^1 t^2 e^{-ct^2} dt, so
      |phi_inf'(c)| = int_0^1 t^2 e^{-ct^2} dt <= int_0^1 t^2 dt = 1/3
for every c >= 0, with equality only at c = 0.  CONFIRMED.
""")
g = lambda c: mp.quad(lambda t: t**2 * mp.e**(-c * t**2), [0, 1])
print("   sup_c int_0^1 t^2 e^{-ct^2} dt, sampled:")
for c in (0, mp.mpf('0.001'), 1, 5, 50):
    print(f"     c={float(c):<8} value = {mp.nstr(g(c), 12)}")
print(f"     1/3 = {mp.nstr(mp.mpf(1)/3, 12)}   -> sup = 1/3 attained at c=0. OK")

phi_inf = lambda c: mp.quad(lambda t: mp.e**(-c * t**2), [0, 1])

print()
print("   Direct audit of the finite-n inequality")
print("      omega_n(C) <= max_{0<=i<=M} |Delta_n(iC/M)| + 4C/(3M)")
print("   (LHS computed on a fine 2001-point grid; both sides in float):")
for (n, C, M) in [(60, 5, 4), (60, 5, 16), (120, 10, 8), (200, 20, 10),
                  (200, 2, 3), (400, 50, 25)]:
    ts = [C * k / 2000.0 for k in range(2001)]
    lhs = max(abs(chain_phi_float(n, min(c / n, 1.0)) - float(phi_inf(c)))
              for c in ts)
    gp = [C * i / M for i in range(M + 1)]
    rhs = max(abs(chain_phi_float(n, min(c / n, 1.0)) - float(phi_inf(c)))
              for c in gp) + 4.0 * C / (3.0 * M)
    print(f"     n={n:4d} C={C:3d} M={M:3d}   omega_n={lhs:.8f}   "
          f"bound={rhs:.8f}   {'OK' if lhs <= rhs else '*** VIOLATION ***'}")
print("""
   The grid step is correct: every c in [0,C] lies in some [c_i, c_{i+1}] of
   width C/M, and Delta_n is (1 + 1/3)-Lipschitz uniformly in n, so
   |Delta_n(c)| <= |Delta_n(c_i)| + (4/3)(C/M).  (Taking the NEAREST grid
   point would give 2C/(3M); the stated 4C/(3M) is valid but a factor 2
   loose.  Harmless.)
""")
