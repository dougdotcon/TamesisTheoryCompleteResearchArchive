"""
Exact-arithmetic verification: does the continuum construction

    M_K' := p_D + sum_{s in S} V_s',   V_s' ~ Uniform(0,p_s) indep given S,
    (p_0,...,p_{K-1},p_D) ~ Dirichlet(1,...,1)  [uniform on the K-simplex],
    S ~ Proposition S's law given p:
        P(S=A|p) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)

have the SAME moments as the target M_K (density f_K(x)=2K x (1-x^2)^{K-1},
proved unconditionally for all K>=1 in THEOREM.md Estagio 24)?

This script computes E[(M_K')^t] EXACTLY (Fraction arithmetic, no floats,
no randomness) via:
  (a) expanding Proposition S's formula for each subset A into monomials,
  (b) expanding E[(p_D + sum_{a in A} V_a)^t | p, A] into monomials via the
      multinomial theorem, using E[V_a^k|p_a] = p_a^k/(k+1) (moment of
      Uniform(0,p_a)),
  (c) integrating each resulting monomial in p_0,...,p_{K-1},p_D exactly
      against the Dirichlet(1,...,1) density using the closed-form Dirichlet
      moment formula
          E[prod_i p_i^{k_i}] = K! * prod_i(k_i!) / (K + sum_i k_i)!
      (a standard, elementary fact about the flat/uniform distribution on
      the K-simplex, re-derived in the comment below, not merely cited).

Target moments E[M_K^t] are computed independently, by direct symbolic/exact
integration of x^t * 2K x (1-x^2)^{K-1} over [0,1] via sympy, exactly -- a
completely independent computational route from (a)-(c) above.

No randomness anywhere in this script.
"""
import itertools
import math
from fractions import Fraction as Fr

import sympy as sp


def dirichlet_monomial_moment(K, exps):
    """E[ p_D^{exps[K]} * prod_{i=0}^{K-1} p_i^{exps[i]} ] for
    (p_0,...,p_{K-1},p_D) ~ Dirichlet(1,...,1) on K+1 parts (uniform on the
    K-simplex). exps has length K+1 (last entry = exponent of p_D).

    Derivation of the formula used (elementary, standard):
    (p_0,...,p_K) ~ Dirichlet(1,...,1) (K+1 ones) has density K! on the
    K-simplex {p_i>=0, sum p_i = 1} w.r.t. the (K-dimensional) Lebesgue
    measure obtained by dropping one coordinate (say p_K) and integrating
    over (p_0,...,p_{K-1}) in the region sum_{i<K} p_i <= 1. The needed
    integral is the classical Dirichlet-integral identity
        int_{simplex} prod_{i=0}^{K} x_i^{k_i} dx  =  prod_i(k_i!) / (K + sum k_i)!
    (x_K := 1 - sum_{i<K} x_i; integral w.r.t. Lebesgue measure on the
    K free coordinates x_0,...,x_{K-1}) -- proved by induction on K via
    Fubini (integrate out x_0 last, using the Beta-function integral
    int_0^{1-r} x_0^{k_0} (1-x_0-r)^{...} ... reduces one dimension at a
    time to the Beta integral int_0^1 u^a (1-u)^b du = a! b!/(a+b+1)!).
    This is the standard "Dirichlet normalizing constant" computation; we
    do not re-derive it from scratch inside this script (it is elementary
    and completely standard -- e.g. any probability text's treatment of
    the Dirichlet distribution) but DO cross-check it numerically below
    (see `_selfcheck_dirichlet_formula`).
    Multiplying by the density K! gives the stated expectation formula.
    """
    assert len(exps) == K + 1
    num = math.factorial(K)
    for e in exps:
        num *= math.factorial(e)
    den = math.factorial(K + sum(exps))
    return Fr(num, den)


def _selfcheck_dirichlet_formula(K, trials=200000, seed=20260933050):
    """Monte Carlo cross-check of dirichlet_monomial_moment against direct
    simulation, for a handful of small exponent vectors. NOT used anywhere
    in the exact proof pipeline -- purely a numerical sanity check that the
    closed-form formula above was implemented / recalled correctly."""
    import numpy as np
    rng = np.random.default_rng(seed)
    # sample K+1 iid Exp(1), normalize -> Dirichlet(1,...,1)
    X = rng.exponential(size=(trials, K + 1))
    P = X / X.sum(axis=1, keepdims=True)
    results = {}
    test_exps = [tuple([1] + [0] * K), tuple([2] + [0] * K),
                 tuple([1, 1] + [0] * (K - 1)) if K >= 1 else None]
    for exps in test_exps:
        if exps is None:
            continue
        vals = np.ones(trials)
        for i, e in enumerate(exps):
            if e:
                vals = vals * (P[:, i] ** e)
        mc = float(vals.mean())
        exact = float(dirichlet_monomial_moment(K, exps))
        results[exps] = (mc, exact, abs(mc - exact))
    return results


def prop_S_monomials(K, A):
    """Return Proposition S's weight P(S=A|p) as a dict {exponent-tuple:
    coefficient}, exponent-tuple of length K+1 (last = p_D exponent),
    coefficient a Fraction (here always an integer, but Fraction for
    uniformity). P(S=A|p) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)
    = m! * prod_A p_a * p_D  +  m! * sum_{b in A} p_b * prod_A p_a
    (the second sum's b-th term has p_b appearing squared)."""
    m = len(A)
    fact_m = math.factorial(m)
    monos = {}

    def base_exp():
        e = [0] * (K + 1)
        for a in A:
            e[a] += 1
        return e

    # term 1: m! * prod_A p_a * p_D
    e1 = base_exp()
    e1[K] += 1  # p_D
    monos[tuple(e1)] = monos.get(tuple(e1), Fr(0)) + fact_m

    # term 2: m! * sum_{b in A} p_b * prod_A p_a  (p_b gets +1 more)
    for b in A:
        e2 = base_exp()
        e2[b] += 1
        monos[tuple(e2)] = monos.get(tuple(e2), Fr(0)) + fact_m

    return monos


def conditional_moment_monomials(K, A, t):
    """Return E[(p_D + sum_{a in A} V_a)^t | p, A] as a dict
    {exponent-tuple: coefficient}, via the multinomial theorem, using
    E[V_a^{k_a}|p_a] = p_a^{k_a}/(k_a+1) for V_a ~ Uniform(0,p_a).
    The deterministic term p_D contributes p_D^{k_D} directly (no division).
    """
    A = list(A)
    m = len(A)
    monos = {}
    # distribute exponent t among (k_D, k_{a_1},...,k_{a_m}) with sum = t
    for k_D in range(t + 1):
        rem = t - k_D
        # iterate over compositions of rem into m nonneg parts
        if m == 0:
            if rem == 0:
                coeff = Fr(math.factorial(t), math.factorial(k_D))  # = 1 when k_D=t
                e = [0] * (K + 1)
                e[K] = k_D
                monos[tuple(e)] = monos.get(tuple(e), Fr(0)) + coeff
            continue
        for ks in itertools.product(range(rem + 1), repeat=m):
            if sum(ks) != rem:
                continue
            multinom_coeff = Fr(math.factorial(t))
            multinom_coeff /= math.factorial(k_D)
            for k in ks:
                multinom_coeff /= math.factorial(k)
            # expectation factor from each Uniform(0,p_a)^{k_a}: 1/(k_a+1)
            val = multinom_coeff
            for k in ks:
                val /= (k + 1)
            e = [0] * (K + 1)
            e[K] = k_D
            for idx, a in enumerate(A):
                e[a] += ks[idx]
            monos[tuple(e)] = monos.get(tuple(e), Fr(0)) + val
    return monos


def multiply_monomials(d1, d2, K):
    out = {}
    for e1, c1 in d1.items():
        for e2, c2 in d2.items():
            e = tuple(e1[i] + e2[i] for i in range(K + 1))
            out[e] = out.get(e, Fr(0)) + c1 * c2
    return out


def E_MKprime_power(K, t):
    """Exact E[(M_K')^t], summing Prop-S(A) * E[(sum...)^t|A] over all
    subsets A of {0,...,K-1}, each term integrated exactly against the
    Dirichlet(1,...,1) density."""
    total = Fr(0)
    for r in range(0, K + 1):
        for A in itertools.combinations(range(K), r):
            propS = prop_S_monomials(K, A)
            cond = conditional_moment_monomials(K, A, t)
            prod = multiply_monomials(propS, cond, K)
            for exps, coeff in prod.items():
                total += coeff * dirichlet_monomial_moment(K, list(exps))
    return total


def target_moment(K, t):
    """E[M_K^t] computed independently via direct exact integration of
    x^t * f_K(x) = x^t * 2K x (1-x^2)^{K-1} over [0,1], sympy exact."""
    x = sp.symbols('x', positive=True)
    dens = 2 * K * x * (1 - x**2) ** (K - 1)
    val = sp.integrate(x**t * dens, (x, 0, 1))
    return Fr(int(sp.fraction(sp.nsimplify(val))[0]), int(sp.fraction(sp.nsimplify(val))[1]))


if __name__ == "__main__":
    print("Self-check of the Dirichlet monomial-moment formula (Monte Carlo, K=3):")
    for exps, (mc, exact, diff) in _selfcheck_dirichlet_formula(3).items():
        print(f"  exps={exps}: MC={mc:.5f} exact={exact} diff={diff:.5f}")
    print()

    print("Exact moment comparison: E[(M_K')^t]  vs  E[M_K^t] (target, independent route)")
    print(f"{'K':>3} {'t':>3} {'E[(M_K prime)^t]':>22} {'target E[M_K^t]':>18} {'match?':>8}")
    all_match = True
    for K in range(1, 8):
        for t in range(1, 6):
            got = E_MKprime_power(K, t)
            tgt = target_moment(K, t)
            ok = (got == tgt)
            all_match = all_match and ok
            print(f"{K:>3} {t:>3} {str(got):>22} {str(tgt):>18} {'OK' if ok else 'MISMATCH':>8}")
    print()
    print("ALL MATCH" if all_match else "SOME MISMATCHES FOUND")
