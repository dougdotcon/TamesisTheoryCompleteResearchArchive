"""
GAMMA-GAP1-SHARPER-TAIL-ATTEMPT, script 02.

Part A. Fresh, independent symbolic (sympy) re-derivation of
x(D) := delta(D) + tau(M)/2  as an exact cubic polynomial in D,
D:=M-gamma*k, M~Bin(k,gamma), from the two cited exact identities
(required reading, grandparent ATTEMPT.md Sections 1-2):
  tau(m) := sum_{i=1}^m ((k-i)/n)^2
  delta(D) := D*(2k(1-gamma) - D - 1) / (2n)
Cross-checked against the grandparent front's post-adversarial-CORRECTED
closed form for c_0 (the referee found and fixed a spurious extra factor of
gamma in five of six terms of the originally-stated closed form; the
corrected form is what is checked here).

Part B. Independent numerical verification (mpmath dps=50) of the elementary,
fully-explicit coefficient bounds cited from required reading (continuation
ATTEMPT.md Step 3, itself referee-reviewed and confirmed correct in Estagio
36's adversarial report):
  |c0(k)| <= (7/6) k^3/n^2 + (5/6) k^2/n^2
  |c1(k)| <= 2 k^2/n^2 + (1-gamma) k/n + k/n^2 + 3/(4n)
  |c2(k)| <= (1-gamma) k/(2n^2) + 3/(4n)
  c3      = 1/(6n^2)                              (exact)
These bounds do not depend on which tail-control technique (Hoeffding vs
Bernstein) is used downstream -- they are cited here (not re-derived from
the raw triangle-inequality regrouping algebra, which is a stylistic choice
without unique "right" form), then independently verified on a wide grid,
including astronomically large n (up to 10^80) since that is the regime
this front's own n_0(gamma) construction (script 05) will operate in.

Part C. Fresh re-assembly of hat-G(n,gamma) := g_bound(K_max,K_max,n,gamma)
from the Part-B coefficient bounds, cross-checked to match the continuation
front's own stated closed form exactly (sympy zero-difference check) --
this hat-G formula is REUSED as-is in this front's construction (script 05),
since it does not depend on the tail-control technique either.
"""
import sympy as sp
import mpmath as mp

print("=" * 78)
print("PART A: fresh symbolic re-derivation of x(D)'s exact cubic form")
print("=" * 78)

k, n, gam, D, m, i = sp.symbols('k n gamma D m i', positive=True)

tau_m = sp.simplify(sp.summation(((k - i) / n) ** 2, (i, 1, m)))
print("tau(m) =", tau_m)

M = gam * k + D
tau_M = tau_m.subs(m, M)
delta_D = D * (2 * k * (1 - gam) - D - 1) / (2 * n)
x_D = sp.expand(delta_D + tau_M / 2)
x_poly = sp.Poly(x_D, D)
print("degree of x(D) in D:", x_poly.degree(), "(must be exactly 3)")
assert x_poly.degree() == 3
c3, c2, c1, c0 = [sp.simplify(c) for c in x_poly.all_coeffs()]
print("c3 =", c3)
print("c2 =", c2)
print("c1 =", c1)
print("c0 =", c0)

c0_grandparent_corrected = (gam * k) / (12 * n ** 2) * (
    2 * gam ** 2 * k ** 2 - 6 * gam * k ** 2 + 3 * gam * k + 6 * k ** 2 - 6 * k + 1
)
diff0 = sp.simplify(c0 - c0_grandparent_corrected)
print("c0 - c0_grandparent_CORRECTED (must be 0):", diff0)
assert diff0 == 0

# second independent route: derivative-based assembly (tau, tau', tau'' at m=gamma*k)
tau_prime = sp.diff(tau_m, m)
tau_pprime = sp.diff(tau_m, m, 2)
c1_alt = k * (1 - gam) / n - 1 / (2 * n) + tau_prime.subs(m, gam * k) / 2
c2_alt = -1 / (2 * n) + tau_pprime.subs(m, gam * k) / 4
c0_alt = tau_m.subs(m, gam * k) / 2
print()
print("route 2 (derivative-based) cross-check, all differences must be 0:")
print("  c0 - c0_alt:", sp.simplify(c0 - c0_alt))
print("  c1 - c1_alt:", sp.simplify(c1 - c1_alt))
print("  c2 - c2_alt:", sp.simplify(c2 - c2_alt))
print("  c3 - 1/(6n^2):", sp.simplify(c3 - sp.Rational(1, 6) / n ** 2))
assert sp.simplify(c0 - c0_alt) == 0
assert sp.simplify(c1 - c1_alt) == 0
assert sp.simplify(c2 - c2_alt) == 0

subs_pt = {gam: sp.Rational(1, 2), k: 10, n: 100}
print()
print("referee test-point (gamma=1/2,k=10,n=100): c0 =", c0.subs(subs_pt),
      " (must equal 51/4000, the value independently confirmed by the referee)")
assert c0.subs(subs_pt) == sp.Rational(51, 4000)

print()
print("=" * 78)
print("PART B: independent numerical verification of coefficient bounds")
print("=" * 78)
mp.mp.dps = 50


def exact_c(k_, n_, gam_):
    k_ = mp.mpf(k_); n_ = mp.mpf(n_); gam_ = mp.mpf(gam_)
    c3_ = 1 / (6 * n_ ** 2)
    c2_ = (2 * gam_ * k_ - 2 * k_ - 2 * n_ + 1) / (4 * n_ ** 2)
    c1_ = (gam_ ** 2 * k_ ** 2 / 2 - gam_ * k_ ** 2 - gam_ * k_ * n_ + gam_ * k_ / 2
           + k_ ** 2 / 2 + k_ * n_ - k_ / 2 - n_ / 2 + mp.mpf(1) / 12) / n_ ** 2
    c0_ = gam_ * k_ * (2 * gam_ ** 2 * k_ ** 2 - 6 * gam_ * k_ ** 2 + 3 * gam_ * k_
                        + 6 * k_ ** 2 - 6 * k_ + 1) / (12 * n_ ** 2)
    return c0_, c1_, c2_, c3_


def coeff_bounds(k_, n_, gam_):
    k_ = mp.mpf(k_); n_ = mp.mpf(n_); gam_ = mp.mpf(gam_)
    b0 = mp.mpf(7) / 6 * k_ ** 3 / n_ ** 2 + mp.mpf(5) / 6 * k_ ** 2 / n_ ** 2
    b1 = 2 * k_ ** 2 / n_ ** 2 + (1 - gam_) * k_ / n_ + k_ / n_ ** 2 + mp.mpf(3) / (4 * n_)
    b2 = (1 - gam_) * k_ / (2 * n_ ** 2) + mp.mpf(3) / (4 * n_)
    b3 = 1 / (6 * n_ ** 2)
    return b0, b1, b2, b3


checked = 0
violations = 0
ns = [10, 50, 200, 1000, 10 ** 4, 10 ** 6, 10 ** 8, 10 ** 12, 10 ** 20, 10 ** 40, 10 ** 80]
gammas = [0.005, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 0.995]
for n_val in ns:
    for gam_f in gammas:
        kmax = max(1, n_val // 2)
        ks = sorted(set([1, 2, kmax // 4 + 1, kmax // 2 + 1, (3 * kmax) // 4 + 1, kmax]))
        for k_val in ks:
            if k_val < 1 or k_val > n_val:
                continue
            c0e, c1e, c2e, c3e = exact_c(k_val, n_val, gam_f)
            b0, b1, b2, b3 = coeff_bounds(k_val, n_val, gam_f)
            checked += 1
            if abs(c0e) > b0 + mp.mpf('1e-60'):
                violations += 1
                print("VIOLATION c0", n_val, gam_f, k_val)
            if abs(c1e) > b1 + mp.mpf('1e-60'):
                violations += 1
                print("VIOLATION c1", n_val, gam_f, k_val)
            if abs(c2e) > b2 + mp.mpf('1e-60'):
                violations += 1
                print("VIOLATION c2", n_val, gam_f, k_val)
            if abs(c3e - b3) > mp.mpf('1e-60'):
                violations += 1
                print("VIOLATION c3 exact mismatch", n_val, gam_f, k_val)
print(f"checked={checked} violations={violations} "
      f"(n up to 10^80, matching the astronomical scale this front's own n_0(gamma) will need)")
assert violations == 0

print()
print("=" * 78)
print("PART C: fresh assembly of hat-G(n,gamma), cross-check vs continuation's")
print("stated closed form")
print("=" * 78)
Km = sp.symbols('K_m', positive=True)
absc0 = sp.Rational(7, 6) * Km ** 3 / n ** 2 + sp.Rational(5, 6) * Km ** 2 / n ** 2
absc1 = 2 * Km ** 2 / n ** 2 + (1 - gam) * Km / n + Km / n ** 2 + sp.Rational(3, 4) / n
absc2 = (1 - gam) * Km / (2 * n ** 2) + sp.Rational(3, 4) / n
c3_sym = 1 / (6 * n ** 2)
g_Km = sp.expand(absc0 + absc1 * Km + absc2 * Km ** 2 + c3_sym * Km ** 3)
print("g_bound(K_max,K_max,n,gamma) [this front's hat-G] =")
print(" ", sp.collect(g_Km, Km))

hatG_claimed = (sp.Rational(10, 3) + (1 - gam) / 2) * Km ** 3 / n ** 2 + \
               (sp.Rational(7, 4) - gam) * Km ** 2 / n + \
               sp.Rational(11, 6) * Km ** 2 / n ** 2 + \
               sp.Rational(3, 4) * Km / n
diff = sp.simplify(g_Km - hatG_claimed)
print("difference vs continuation's stated hat-G (must be 0):", diff)
assert diff == 0

print()
print("All Part A/B/C checks passed.")
