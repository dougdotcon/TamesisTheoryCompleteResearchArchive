"""
Full independent re-derivation of the general-b closed form for
D^{*(p)}_r(b), p=1,2,3,4, from Corollary A3 alone -- steps 1-4 of
ATTEMPT.md sec 2-4, redone from scratch, checked against:
  (a) own_ground_truth.py's D_star (independent Corollary A3 implementation)
  (b) internal cross-checks (three independent computation paths must agree)
  (c) the document's own printed formulas, ONLY as a comparison target
      (never as derivation input)

Nothing here imports general_b_dstar_attempt/*.py.
"""
from fractions import Fraction
import sympy as sp

from own_ground_truth import stirling1_unsigned, D_star, varphi, fact
from abel_identities import S_direct as S_direct_frac  # brute force S_power(N,m), Fraction


def binom_conv(n, k):
    if n < 0 or k < 0 or k > n:
        return Fraction(0)
    num = 1
    for i in range(k):
        num *= (n - i)
    den = 1
    for i in range(1, k + 1):
        den *= i
    return Fraction(num, den)


def P_b_val(r, b):
    N = 2 * r + b + 1
    return Fraction(fact(r) * fact(r + b), fact(N))


# ---------------------------------------------------------------------------
# Step 1 check: the P_b*C(N,alpha) rewrite of c_j^{(r)}(b), and the
# extension-for-free rewrite  D = P_b * sum_{alpha=0}^{r} Q_p(r-alpha) C(N,alpha)
# ---------------------------------------------------------------------------

def Q_p_direct(p, u):
    """Q_p(u) := c(u+1, u+1-p), via my own Stirling table -- direct integer
    evaluation (no interpolation needed here, just for Step-1 checking)."""
    if u + 1 - p < 0:
        return 0
    return stirling1_unsigned(u + 1, u + 1 - p)


def D_via_step1(p, r, b):
    N = 2 * r + b + 1
    Pb = P_b_val(r, b)
    total = Fraction(0)
    for alpha in range(0, r + 1):
        u = r - alpha
        total += Fraction(Q_p_direct(p, u)) * binom_conv(N, alpha)
    return Pb * total


def verify_step1(p_max, r_max, b_max):
    fails = 0
    checks = 0
    for p in range(0, p_max + 1):
        for r in range(0, r_max + 1):
            for b in range(0, b_max + 1):
                a = D_via_step1(p, r, b)
                bnd = D_star(p, r, b)
                checks += 1
                if a != bnd:
                    fails += 1
                    print(f"FAIL step1 p={p} r={r} b={b}: {a} vs {bnd}")
    print(f"verify_step1(p_max={p_max},r_max={r_max},b_max={b_max}): "
          f"{checks} checks, {fails} failures")
    return fails


# also explicitly check the "added terms vanish" extension-for-free claim:
def verify_extension_terms_vanish(p_max, r_max):
    """Terms alpha=r-p+1,...,r (i.e. u=p-1,...,0) must have Q_p(u)=0."""
    fails = 0
    checks = 0
    for p in range(1, p_max + 1):
        for r in range(p, r_max + 1):
            for u in range(0, p):  # u = 0,...,p-1
                checks += 1
                if Q_p_direct(p, u) != 0:
                    fails += 1
                    print(f"FAIL extension-vanish p={p} r={r} u={u}: Q_p={Q_p_direct(p,u)}")
    print(f"verify_extension_terms_vanish(p_max={p_max},r_max={r_max}): "
          f"{checks} checks, {fails} failures")
    return fails


# ---------------------------------------------------------------------------
# Q_p(u) as a symbolic polynomial in u, degree 2p, via Lagrange interpolation
# from MY OWN Stirling table -- then checked against 20 out-of-sample points.
# ---------------------------------------------------------------------------

def build_Qp_poly(p):
    u = sp.symbols('u')
    pts = [(uu, Q_p_direct(p, uu)) for uu in range(0, 2 * p + 1)]
    poly = sp.interpolate(pts, u)
    poly = sp.expand(poly)
    return poly, u


def verify_Qp_out_of_sample(p_max, extra=20):
    fails = 0
    checks = 0
    for p in range(0, p_max + 1):
        poly, u = build_Qp_poly(p)
        for uu in range(2 * p + 1, 2 * p + 1 + extra):
            got = poly.subs(u, uu)
            want = Q_p_direct(p, uu)
            checks += 1
            if sp.simplify(got - want) != 0:
                fails += 1
                print(f"FAIL Qp out-of-sample p={p} u={uu}: {got} vs {want}")
    print(f"verify_Qp_out_of_sample(p_max={p_max}, extra={extra}): "
          f"{checks} checks, {fails} failures")
    return fails


# ---------------------------------------------------------------------------
# Central moments mu_{2l}(N) of Bin(N,1/2), via cumulant generating function
# -- own sympy derivation, then verified by direct summation.
# ---------------------------------------------------------------------------

def derive_moments(max_l):
    """mu_{2l}(N) for l=0..max_l via K(t)=N*log(cosh(t/2)), M(t)=exp(K(t)),
    series in t. Returns dict l -> sympy expr in N."""
    t, N = sp.symbols('t N')
    order = 2 * max_l + 2
    K = N * sp.log(sp.cosh(t / 2))
    M = sp.exp(K)
    series = sp.series(M, t, 0, order).removeO()
    series = sp.expand(series)
    poly_t = sp.Poly(series, t)
    moments = {}
    for l in range(0, max_l + 1):
        deg = 2 * l
        coeff_of_tdeg = poly_t.coeff_monomial(t ** deg) if deg > 0 else poly_t.coeff_monomial(1)
        mu = sp.simplify(coeff_of_tdeg * sp.factorial(deg))
        moments[l] = sp.expand(mu)
    return moments


def verify_moments_direct(moments, N_max):
    N_sym = sp.symbols('N')
    fails = 0
    checks = 0
    for l, expr in moments.items():
        for N in range(0, N_max + 1):
            direct = Fraction(0)
            for alpha in range(0, N + 1):
                direct += Fraction((2 * alpha - N) ** (2 * l), 2 ** (2 * l)) * binom_conv(N, alpha)
            direct = direct / Fraction(2 ** N)
            # note: mu_{2l}(N) := 2^{-N} sum (alpha - N/2)^{2l} C(N,alpha)
            # (alpha - N/2)^{2l} = (2alpha-N)^{2l} / 2^{2l}
            predicted_frac = sp.Rational(expr.subs(N_sym, N))
            checks += 1
            if sp.Rational(direct.numerator, direct.denominator) != predicted_frac:
                fails += 1
                print(f"FAIL moment l={l} N={N}: direct={direct} predicted={predicted_frac}")
    print(f"verify_moments_direct(N_max={N_max}): {checks} checks, {fails} failures")
    return fails


# ---------------------------------------------------------------------------
# Odd-part collapse: Pcollapse(power, r, b) := P_b * S_power(N,r),
# N=2r+b+1, derived recursively from MY OWN general Abel recursion
# (abel_identities.py) + MY OWN general-k prefactor collapse
# (collapse_proposition.py), entirely symbolically in r,b.
# ---------------------------------------------------------------------------

_pcollapse_cache = {}


def Pcollapse_symbolic(power, r_sym, b_sym):
    """power must be odd, >=1. Returns a sympy expression in r_sym,b_sym for
    P_b * S_power(N,r), N=2r+b+1, derived via:
      Pcollapse(1,r,b) = 1                                     [k=0 collapse]
      Pcollapse(2k-1,r,b) = beta^{2k-2}
        + 2r * sum_{s odd,1<=s<=2k-3} C(2k-2,s) * Pcollapse(s, r-1, b+1)
    (beta := b+1), matching the recursive telescoping derived by hand in the
    referee report (Part A/B of abel_identities.py's derivation, re-applied
    here with the general-k collapse folded in at each recursive step)."""
    key = (power, str(r_sym), str(b_sym))
    if power == 1:
        return sp.Integer(1)
    n_exp = power - 1
    beta = b_sym + 1
    total = beta ** n_exp
    for t in range(1, n_exp, 2):
        s = n_exp - t
        coeff = sp.binomial(n_exp, t)
        total += 2 * r_sym * coeff * Pcollapse_symbolic(s, r_sym - 1, b_sym + 1)
    return sp.expand(total)


def Pcollapse_numeric(power, r, b):
    """Concrete-integer version, via the SAME recursion but with Fraction
    arithmetic (redundant with brute force below, used as an intermediate
    consistency check)."""
    if power == 1:
        return Fraction(1)
    n_exp = power - 1
    beta = b + 1
    total = Fraction(beta ** n_exp)
    for t in range(1, n_exp, 2):
        s = n_exp - t
        coeff = sp.binomial(n_exp, t)
        total += 2 * r * int(coeff) * Pcollapse_numeric(s, r - 1, b + 1)
    return total


def Pcollapse_bruteforce(power, r, b):
    N = 2 * r + b + 1
    return P_b_val(r, b) * S_direct_frac(power, N, r)


def verify_Pcollapse(power_max, r_max, b_max):
    fails = 0
    checks = 0
    for power in range(1, power_max + 1, 2):
        for r in range(0, r_max + 1):
            for b in range(0, b_max + 1):
                a = Pcollapse_numeric(power, r, b)
                c = Pcollapse_bruteforce(power, r, b)
                checks += 1
                if a != c:
                    fails += 1
                    print(f"FAIL Pcollapse power={power} r={r} b={b}: numeric={a} bf={c}")
    print(f"verify_Pcollapse(power_max={power_max},r_max={r_max},b_max={b_max}): "
          f"{checks} checks, {fails} failures")
    return fails


# cross-check against the document's PRINTED intermediate odd-sum formulas
# (sec 3.4), purely as a target for comparison -- not used anywhere upstream.
def verify_against_document_odd_formulas():
    r, b = sp.symbols('r b')
    beta = b + 1
    fails = 0

    # P_b sum v C(N,alpha) = -1/2  <=>  Pcollapse(1,r,b) = 1
    lhs1 = Pcollapse_symbolic(1, r, b)
    ok1 = sp.simplify(lhs1 - 1) == 0
    print("k=1 (S_1) collapse matches document's '-1/2' claim:", ok1)
    fails += 0 if ok1 else 1

    # P_b sum v^3 C(N,alpha) = -1/8(beta^2+4r) <=> Pcollapse(3,r,b)=beta^2+4r
    lhs3 = Pcollapse_symbolic(3, r, b)
    ok3 = sp.simplify(lhs3 - (beta ** 2 + 4 * r)) == 0
    print("k=2 (S_3) collapse matches document's beta^2+4r claim:", ok3)
    fails += 0 if ok3 else 1

    # document's S_5 collapse target:
    # beta^4 + 8r((beta+1)^2+1) + 32r(r-1)
    lhs5 = Pcollapse_symbolic(5, r, b)
    target5 = beta ** 4 + 8 * r * ((beta + 1) ** 2 + 1) + 32 * r * (r - 1)
    ok5 = sp.simplify(lhs5 - target5) == 0
    print("k=3 (S_5) collapse matches document's printed bracket:", ok5)
    if not ok5:
        print("   mine:", sp.expand(lhs5))
        print("   doc :", sp.expand(target5))
        print("   diff:", sp.expand(lhs5 - target5))
    fails += 0 if ok5 else 1

    # document's S_7 collapse target:
    # beta^6 + r(12(beta+1)^4+40(beta+1)^2+12) + r(r-1)(96(beta+2)^2+256) + 384r(r-1)(r-2)
    lhs7 = Pcollapse_symbolic(7, r, b)
    target7 = (beta ** 6 + r * (12 * (beta + 1) ** 4 + 40 * (beta + 1) ** 2 + 12)
               + r * (r - 1) * (96 * (beta + 2) ** 2 + 256) + 384 * r * (r - 1) * (r - 2))
    ok7 = sp.simplify(lhs7 - target7) == 0
    print("k=4 (S_7) collapse matches document's printed bracket:", ok7)
    if not ok7:
        print("   mine:", sp.expand(lhs7))
        print("   doc :", sp.expand(target7))
        print("   diff:", sp.expand(lhs7 - target7))
    fails += 0 if ok7 else 1

    return fails


if __name__ == "__main__":
    print("=" * 70)
    print("STEP 1: c_j^{(r)}(b)=P_b*C(N,r-j) rewrite + extension-for-free")
    f_ext = verify_extension_terms_vanish(p_max=10, r_max=40)
    f_s1 = verify_step1(p_max=6, r_max=40, b_max=15)

    print("=" * 70)
    print("Q_p(u) interpolation, out-of-sample (own Stirling table)")
    f_qp = verify_Qp_out_of_sample(p_max=6, extra=25)

    print("=" * 70)
    print("Central moments mu_2, mu_4, mu_6, mu_8 (own cumulant-gen-fn derivation)")
    moments = derive_moments(4)
    for l, e in moments.items():
        print(f"  mu_{2*l}(N) =", e)
    f_mom = verify_moments_direct(moments, N_max=25)

    print("=" * 70)
    print("Odd-part collapse Pcollapse(power,r,b): recursion vs brute force")
    f_pc = verify_Pcollapse(power_max=13, r_max=25, b_max=15)

    print("=" * 70)
    print("Odd-part collapse vs document's printed intermediate formulas (sec 3.4)")
    f_doc = verify_against_document_odd_formulas()

    print("=" * 70)
    total = f_ext + f_s1 + f_qp + f_mom + f_pc + f_doc
    print(f"TOTAL FAILURES: {total}")
