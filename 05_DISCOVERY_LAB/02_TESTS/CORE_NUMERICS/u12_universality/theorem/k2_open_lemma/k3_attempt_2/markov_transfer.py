"""
Core module: the K-uniform "discrete exploration Markov chain" / transfer-matrix
machinery used throughout this attempt (ATTEMPT.md SS2-3). Not specific to K=3 --
implements g_r(m,b), h_r(a,b) for ANY r via a single mechanical algorithm (exact
telescoped hockey-stick summation, executed symbolically by sympy), then specializes
to K=3 (and, as a bonus check on the general-K pattern found along the way, K=4,5).

State of the discrete exploration walk from a fixed reference point x* under f (pi
plus K rerouted "sources"), see ATTEMPT.md SS2 for the full derivation of the
transition rules from elementary permutation-exchangeability facts:

  a = number of pi-images already revealed (queried) so far
  b = number of points visited via a reroute (U) landing on FRESH territory so far
      (still available, from pi's perspective, as a future pi-target -- a possible
      "collision" not present in the K=1 analysis)
  r = number of the K sources not yet visited by the walk

g(a,b,r) = P(x* eventually cyclic | currently at a NON-source point, about to query pi)
h(a,b,r) = P(x* eventually cyclic | currently at a SOURCE, about to draw its own U)

Transition rules (m := n-a = size of the still-unassigned pi-target pool):

  g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r)
  h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)

psi_n^{(K)} = g(0,0,K).

Solved exactly via: g_r(m,b) = [sum_{k=j}^{m} c_r(k) C(k,j)] / C(m,j), j=r+b+1,
c_r(k) = 1/k + (r/k) h_{r-1}(n-k+1,b) -- see ATTEMPT.md SS3 for the by-hand r=0,1
derivation that this script's r=0,1 output is checked against verbatim.
"""
import sympy as sp

n, a_sym, m, k = sp.symbols('n a m k', positive=True)
b = sp.Symbol('b', integer=True, nonnegative=True)


def h_closed_from_g(r, a_expr, b_expr, g_r_of_m, h_prev_of_a):
    """h_r(a,b) = 1/n + (r/n) h_{r-1}(a,b+1) + ((n-1-a-b-r)/n) g_r(a,b+1)."""
    term_h = sp.Integer(0)
    if r >= 1:
        term_h = sp.Rational(r, 1) / n * h_prev_of_a(a_expr, b_expr + 1)
    term_g = (n - 1 - a_expr - b_expr - r) / n * g_r_of_m(n - a_expr, b_expr + 1)
    return sp.simplify(sp.Rational(1, 1) / n + term_h + term_g)


def g_closed_via_telescoping(r, h_prev_of_a, b_expr=b):
    """Solve g_r(m,b) in closed form (symbolic b) via exact telescoped summation."""
    j = r + b_expr + 1
    if r == 0:
        c_r_k = sp.Rational(1, 1) / k
    else:
        h_of_k = h_prev_of_a(n - k + 1, b_expr)
        c_r_k = sp.simplify(sp.Rational(1, 1) / k + sp.Rational(r, 1) / k * h_of_k)
    summand = sp.simplify(c_r_k * sp.binomial(k, j))
    total = sp.simplify(sp.summation(summand, (k, j, m)))
    g_of_m = sp.simplify(total / sp.binomial(m, j))

    def g_r_func(m_expr, b_expr2=b_expr):
        e = g_of_m
        if b_expr2 is not b_expr:
            e = e.subs(b_expr, b_expr2)
        e = e.subs(m, m_expr)
        return sp.simplify(e)

    return g_r_func, g_of_m


def g0_func(m_expr, b_expr=b):
    return sp.Rational(1, 1) / (b_expr + 1)


def build_levels(max_r):
    """Return dict r -> (g_r_func, h_r_func) for r=0..max_r."""
    levels = {}
    g_prev = g0_func

    def h0_func(a_expr, b_expr=b):
        return h_closed_from_g(0, a_expr, b_expr, g0_func, None)

    levels[0] = (g0_func, h0_func)
    h_prev = h0_func
    for r in range(1, max_r + 1):
        g_r, _ = g_closed_via_telescoping(r, h_prev)

        def make_h(r_=r, g_r_=g_r, h_prev_=h_prev):
            def h_r_func(a_expr, b_expr=b):
                return h_closed_from_g(r_, a_expr, b_expr, g_r_, h_prev_)
            return h_r_func

        h_r = make_h()
        levels[r] = (g_r, h_r)
        h_prev = h_r
    return levels


def psi_closed_form(K):
    """psi_n^{(K)} = g_K(m=n, b=0), exact closed form in n."""
    levels = build_levels(K)
    g_K, _ = levels[K]
    return sp.simplify(g_K(n, 0))


def psi_rerouted_closed_form(K):
    """psi_n^{(K),R} = h_{K-1}(a=0, b=0): the reference point IS one of the K
    sources; the other K-1 are "remaining" at the moment it draws its own U."""
    assert K >= 1
    levels = build_levels(K - 1)
    _, h_Km1 = levels[K - 1]
    return sp.simplify(h_Km1(0, 0))


def phi_K_wallis(K):
    return sp.Rational(4 ** K * sp.factorial(K) ** 2, sp.factorial(2 * K + 1))


def phi_closed_form(K):
    """Lemma A recombination: phi_n^{(K)} = (K/n) psi^R + (1-K/n) psi."""
    psi = psi_closed_form(K)
    psiR = psi_rerouted_closed_form(K)
    expr = sp.Rational(K, 1) / n * psiR + (1 - sp.Rational(K, 1) / n) * psi
    return sp.simplify(sp.together(expr))


if __name__ == "__main__":
    for K in range(0, 6):
        psi = psi_closed_form(K)
        phiK = phi_K_wallis(K)
        lim = sp.limit(psi, n, sp.oo)
        c1 = sp.limit((psi - phiK) * n, n, sp.oo)
        print(f"K={K}: psi_n^({K}) = {psi}")
        print(f"       limit = {lim}  (phi_{K}={phiK}, match={lim==phiK})")
        print(f"       1/n coefficient = {c1}  (K*phi_K/4 = {sp.simplify(sp.Rational(K,4)*phiK)})")
