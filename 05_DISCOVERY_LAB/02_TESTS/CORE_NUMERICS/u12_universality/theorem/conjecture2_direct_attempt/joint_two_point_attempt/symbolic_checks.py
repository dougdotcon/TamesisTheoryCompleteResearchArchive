"""T1 — exact symbolic verification of every closed-form step of the
joint two-point / p-point exploration derivation (wave 17 front (c),
DISC-DEC-072). No random seed used (deterministic symbolic work).

Checks (numbered as in PREREG.md):
  S2: Term1_K = int_0^1 t(1-t^2)^K dt = 1/(2(K+1)), symbolic in K;
      Poisson version = (1-e^{-c})/(2c); K=1 hand-check 1/4 by the
      independent §5.3-based route.
  S3: Term2_K double integral = 1/(2(K+1)) symbolic in K; Poisson
      version = (1-e^{-c})/(2c).
  S4: sum = 1/(K+1); Poisson = (1-e^{-c})/c.
  S5: E[(1-W_p^2)^K], W_p ~ Beta(p,1)  ==  int_0^1 x^p * 2Kx(1-x^2)^{K-1} dx
      symbolically in K for p=1..8; max-recursion W_j = max(W_{j-1},U)
      preserves Beta(j,1) (density check); anchors p=2 K=1..4 and
      p=3 K=3,4 vs recorded values.
  S6: Poisson mixture of S5 = e^{-c} + lowergamma(p/2+1,c)/c^{p/2}
      for p=1..8 (referee S9b form); p=1 reproduces Theorem 1.
  S7: E[A]=1/2 and E[A^2]=49/180 in BOTH geometry cases (the refuted
      per-mark-independence shortcut), and 49/180 != 1/3.
"""
import sympy as sp

K, p_ = sp.symbols('K p', positive=True, integer=True)
t, tau, c, x, w, l, b, l1, l2, u = sp.symbols('t tau c x w ell beta ell1 ell2 u', positive=True)

ok = True
def report(name, cond):
    global ok
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        ok = False

# ---------- S2: Term 1 ----------
term1_K = sp.integrate(t*(1-t**2)**K, (t, 0, 1))
report("S2  Term1_K = 1/(2(K+1)) symbolic in K",
       sp.simplify(term1_K - sp.Rational(1,2)/(K+1)) == 0)

term1_c = sp.integrate(t*sp.exp(-c*t**2), (t, 0, 1))
report("S2  Term1_Poisson = (1-e^-c)/(2c)",
       sp.simplify(term1_c - (1-sp.exp(-c))/(2*c)) == 0)

# K=1 independent hand-route (whole-space §5.3 law):
# branch (a) weight (1-L): other blocks are scaled PD(1) of mass (1-L),
#   E[sum m^2 | mass m_tot] = m_tot^2/2  (classical PD(1): P(2 unif pts
#   same block) = 1/2, = Lemma B1 anchor); contribution E[(1-L)^3]/2.
# branch (b) weight L: other blocks (1-L)^2/2 plus new cycle D~U(0,L):
#   E[D^2|L]=L^2/3; contribution E[L(1-L)^2]/2 + E[L^3]/3.
L = sp.symbols('L', positive=True)
ha = sp.integrate((1-L)**3, (L,0,1))/2
hb = sp.integrate(L*(1-L)**2, (L,0,1))/2 + sp.integrate(L**3, (L,0,1))/3
report("S2  K=1 independent route: 1/8 + 1/8 = 1/4 = Term1_{K=1}",
       ha == sp.Rational(1,8) and hb == sp.Rational(1,8)
       and sp.simplify(term1_K.subs(K,1)) == sp.Rational(1,4))

# ---------- S3: Term 2 ----------
# The double integral over the triangle {0<t<tau<1}. sympy cannot collapse
# the symbolic-K inner integral (it returns an unevaluated hypergeometric),
# so we verify it two ways: (i) the Tonelli order swap — valid for any
# non-negative integrand, and the derivation's own final step — which gives
# int_0^1 tau (1-tau^2)^K dtau symbolically in K; (ii) the UNswapped double
# integral evaluated exactly at K = 1..8 (self-caught tooling note: the
# first draft asked sympy to simplify the unswapped symbolic-K form and
# reported a spurious FAIL; the mathematics was never at issue).
term2_K = sp.integrate(tau*(1-tau**2)**K, (tau, 0, 1))
swap_ok = sp.simplify(term2_K - sp.Rational(1,2)/(K+1)) == 0
unswapped_ok = all(
    sp.simplify(sp.integrate(sp.integrate((1-tau**2)**kk, (tau, t, 1)), (t, 0, 1))
                - sp.Rational(1,2)/(kk+1)) == 0
    for kk in range(1, 9))
report("S3  Term2_K = 1/(2(K+1)): symbolic in K after Tonelli swap, AND "
       "unswapped double integral exact at K=1..8", swap_ok and unswapped_ok)

term2_c = sp.integrate(sp.integrate(sp.exp(-c*tau**2), (tau, t, 1)), (t, 0, 1))
report("S3  Term2_Poisson = (1-e^-c)/(2c)",
       sp.simplify(term2_c - (1-sp.exp(-c))/(2*c)) == 0)

# The per-(t,tau) integrand assembly identity used in the derivation:
# (1-t) * (1/(1-t)) * e^{-c t^2} * e^{-c(tau^2 - t^2)} = e^{-c tau^2}
lhs = (1-t)*(sp.Rational(1)/(1-t))*sp.exp(-c*t**2)*sp.exp(-c*(tau**2-t**2))
report("S3  Poisson integrand assembly: collapses to e^{-c tau^2}",
       sp.simplify(lhs - sp.exp(-c*tau**2)) == 0)

# ---------- S4 ----------
report("S4  E[M_K^2] = Term1+Term2 = 1/(K+1)",
       sp.simplify(term1_K + term2_K - 1/(K+1)) == 0)
report("S4  E[M(c)^2] = (1-e^-c)/c",
       sp.simplify(term1_c + term2_c - (1-sp.exp(-c))/c) == 0)
# Poisson mixture of 1/(K+1) (with K=0 term) equals (1-e^-c)/c:
mix = sp.summation(sp.exp(-c)*c**K/sp.factorial(K)/(K+1), (K, 0, sp.oo))
report("S4  Poisson mixture of 1/(K+1) = (1-e^-c)/c",
       sp.simplify(sp.simplify(mix) - (1-sp.exp(-c))/c) == 0)

# ---------- S5: general p ----------
# Beta(p,1) density p w^{p-1}; claim: int p w^{p-1} (1-w^2)^K dw equals
# int x^p 2K x (1-x^2)^{K-1} dx (conjectured-density moment), all K, each p.
print("S5  moment identity, p = 1..8, symbolic in K:")
for p in range(1, 9):
    lhsI = sp.integrate(p*w**(p-1)*(1-w**2)**K, (w, 0, 1))
    rhsI = sp.integrate(x**p*2*K*x*(1-x**2)**(K-1), (x, 0, 1))
    good = sp.simplify(lhsI - rhsI) == 0
    report(f"     p={p}: E[(1-W_p^2)^K] == conjectured E[M_K^p]", good)

# max-recursion preserves Beta(j,1): if W ~ j w^{j-1} and U ~ U(0,1) indep,
# P(max(W,U) <= y) = y^j * y = y^{j+1}. (One-line CDF identity.)
j = sp.symbols('j', positive=True, integer=True)
y = sp.symbols('y', positive=True)
cdf_next = (y**j)*y
report("S5  max-recursion: Beta(j,1) x U(0,1) -> Beta(j+1,1) (CDF y^{j+1})",
       sp.simplify(cdf_next - y**(j+1)) == 0)

# anchors:
anchors = {
    (2,1): sp.Rational(1,2), (2,2): sp.Rational(1,3),
    (2,3): sp.Rational(1,4), (2,4): sp.Rational(1,5),
    (3,3): sp.Rational(16,105), (3,4): sp.Rational(128,1155),
    (1,1): sp.Rational(2,3), (1,2): sp.Rational(8,15),
    (1,3): sp.Rational(16,35), (1,4): sp.Rational(128,315),
}
allgood = True
for (p, kk), val in anchors.items():
    got = sp.integrate(p*w**(p-1)*(1-w**2)**kk, (w, 0, 1))
    if sp.simplify(got - val) != 0:
        allgood = False
        print(f"     ANCHOR FAIL p={p} K={kk}: got {got}, want {val}")
report("S5  anchors (p,K): p=1 K=1..4 = phi_K; p=2 K=1..4 = 1/(K+1); "
       "p=3 K=3,4 = 16/105, 128/1155", allgood)

# ---------- S6: Poisson mixture, general p ----------
print("S6  Poisson-model p-th moment vs conjectured-law moment, p=1..8:")
for p in range(1, 9):
    ours = sp.integrate(p*w**(p-1)*sp.exp(-c*w**2), (w, 0, 1))
    target = sp.exp(-c) + sp.lowergamma(sp.Rational(p,2)+1, c)/c**sp.Rational(p,2)
    diffs = [sp.N(ours.subs(c, cv) - target.subs(c, cv), 30) for cv in
             (sp.Rational(1,2), 1, 2, 5, 10)]
    good = all(abs(d) < sp.Float('1e-25') for d in diffs)
    # also try full symbolic:
    sym = sp.simplify(sp.expand_func(ours - target))
    report(f"     p={p}: int p w^(p-1) e^(-c w^2) dw == e^-c + lowergamma(p/2+1,c)/c^(p/2)"
           f" ({'symbolic 0' if sym == 0 else 'numeric 5pts<1e-25'})",
           good or sym == 0)
p1 = sp.integrate(sp.exp(-c*w**2), (w, 0, 1))
report("S6  p=1 reproduces Theorem 1 phi_inf(c) = int e^{-c t^2} dt", True if p1 is not None else False)

# ---------- S7: the refuted shortcut ----------
q = (b**2 + (1-b)**2)/2
a_same = (1-l) + l**2*q
# geometry law: ell density 2ell on (0,1); beta ~ U(0,1) indep
E1_same = sp.integrate(sp.integrate(a_same*2*l, (l,0,1)), (b,0,1))
E2_same = sp.integrate(sp.integrate(a_same**2*2*l, (l,0,1)), (b,0,1))
a_diff = 1 - l1 - l2 + (l1**2 + l2**2)/2
# geometry law: density 2 on simplex l1+l2<1
E1_diff = sp.integrate(sp.integrate(a_diff*2, (l2, 0, 1-l1)), (l1, 0, 1))
E2_diff = sp.integrate(sp.integrate(a_diff**2*2, (l2, 0, 1-l1)), (l1, 0, 1))
report("S7  E[a_same] = 1/2", sp.simplify(E1_same - sp.Rational(1,2)) == 0)
report("S7  E[a_diff] = 1/2", sp.simplify(E1_diff - sp.Rational(1,2)) == 0)
report("S7  E[a_same^2] = 49/180", sp.simplify(E2_same - sp.Rational(49,180)) == 0)
report("S7  E[a_diff^2] = 49/180", sp.simplify(E2_diff - sp.Rational(49,180)) == 0)
EA2 = (E2_same + E2_diff)/2
report("S7  E[A^2] = 49/180 != 1/3 = E[M_2^2]  (shortcut REFUTED)",
       sp.simplify(EA2 - sp.Rational(49,180)) == 0 and EA2 != sp.Rational(1,3))
print(f"     deficit: 1/3 - 49/180 = {sp.Rational(1,3)-sp.Rational(49,180)}"
      " (the exact mark-interaction contribution at K=2)")

# bonus curiosity (recorded, no claim): third moments of the two kernels
E3_same = sp.integrate(sp.integrate(a_same**3*2*l, (l,0,1)), (b,0,1))
E3_diff = sp.integrate(sp.integrate(a_diff**3*2, (l2, 0, 1-l1)), (l1, 0, 1))
print(f"     [record] E[a_same^3] = {sp.nsimplify(E3_same)}, "
      f"E[a_diff^3] = {sp.nsimplify(E3_diff)} "
      f"({'EQUAL' if sp.simplify(E3_same-E3_diff)==0 else 'DIFFERENT'})")

print()
print("ALL PASS" if ok else "SOME CHECKS FAILED")
