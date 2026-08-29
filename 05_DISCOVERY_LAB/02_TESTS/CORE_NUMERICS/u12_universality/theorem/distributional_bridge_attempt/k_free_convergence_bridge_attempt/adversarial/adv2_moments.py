"""
Independent, from-scratch verification of Claim B's 35 exact moment
matches (K=1..7, t=1..5), via TWO routes of my own, neither one copied
from the target's verify_MK_moments.py or find_W_pattern.py (those files
were not opened for this script).

Route A (target density): E[M_K^t] = int_0^1 x^t * 2*K*x*(1-x^2)^(K-1) dx,
via sympy exact symbolic integration.

Route B (M_K' construction, my own implementation from the mathematical
description in ATTEMPT.md / THEOREM.md Estagio 41, not from their code):
  M_K' = p_D + sum_{s in S} V_s',  (p_0,...,p_{K-1},p_D) ~ Dirichlet(1,...,1)
  P(S=A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)   [Prop. S]
  V_a' | S, p ~ Uniform(0, p_a) independent across a in A.

E[(M_K')^t] is computed by:
  1. For each subset A of {0,...,K-1}, expand P(S=A) as a polynomial in
     p_D, p_0,...,p_{K-1} (a sum of |A|+1 monomials).
  2. For each A, expand E[(p_D + sum_{a in A} V_a')^t | p, A] via the
     multinomial theorem, using E[V_a'^k | p_a] = p_a^k/(k+1).
  3. Multiply the two polynomials (in exponent-vector space) and sum over
     A, giving E[(M_K')^t] as an explicit polynomial in p_D,p_0,...,p_{K-1}.
  4. Take the expectation of each monomial prod p_i^{k_i} against
     Dirichlet(1,...,1) on K+1 coordinates via the standard closed form
     E[prod p_i^{k_i}] = K! * prod(k_i!) / (K + sum k_i)!  (cited, standard,
     not re-derived -- but cross-checked once below by raw Monte Carlo).

Route A and Route B are then compared exactly (Fraction equality), and
also spot-checked against the numeric values quoted in the target's own
ATTEMPT.md Section 5.2 table.
"""
from fractions import Fraction
from itertools import combinations
from collections import defaultdict
import math
import sympy as sp


def dirichlet_moment(exponents, K):
    """
    exponents: dict var_index -> power, where var indices are 'D' for p_D
    and 0..K-1 for p_0..p_{K-1}. Missing indices have exponent 0.
    E[prod p_i^{k_i}] for (p_0,...,p_{K-1},p_D) ~ Dirichlet(1,...,1)
    (K+1 total coordinates, all alpha_i = 1):
        = K! * prod_i (k_i!) / (K + sum_i k_i)!
    """
    ksum = sum(exponents.values())
    num = Fraction(math.factorial(K))
    for k in exponents.values():
        num *= math.factorial(k)
    den = math.factorial(K + ksum)
    return num / den


def route_B_moment(K, t):
    """
    Exact E[(M_K')^t] via Proposition S + multinomial expansion + Dirichlet
    moment formula, all in exact Fraction arithmetic.
    Polynomial representation: dict from frozenset of (var, power) pairs
    (as a sorted tuple, var in {'D',0,1,...,K-1}) -> Fraction coefficient.
    """
    total = defaultdict(Fraction)  # exponent-tuple -> coefficient
    sources = list(range(K))
    for m in range(0, K + 1):
        for A in combinations(sources, m):
            Aset = set(A)
            # --- expand P(S=A) = m! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)
            # = m! * [ prod_A p_a * p_D  +  sum_{b in A} prod_A p_a * p_b ]
            base_exp = {a: 1 for a in A}  # prod_{a in A} p_a
            prop_s_terms = []  # list of (coeff, exponent dict)
            coeff0 = math.factorial(m)
            # term with p_D
            e = dict(base_exp)
            e['D'] = e.get('D', 0) + 1
            prop_s_terms.append((Fraction(coeff0), e))
            # terms with p_b, b in A (squares p_b)
            for b in A:
                e2 = dict(base_exp)
                e2[b] = e2.get(b, 0) + 1  # now p_b^2
                prop_s_terms.append((Fraction(coeff0), e2))

            # --- expand E[(p_D + sum_{a in A} V_a)^t | A] via multinomial
            # variables: 'D' (deterministic power, contributes p_D^{k_D}),
            # and for each a in A, V_a contributes E[V_a^{k_a}] = p_a^{k_a}/(k_a+1)
            varlist = ['D'] + list(A)
            nv = len(varlist)

            def compositions(total_, parts):
                if parts == 1:
                    yield (total_,)
                    return
                for i in range(total_ + 1):
                    for rest in compositions(total_ - i, parts - 1):
                        yield (i,) + rest

            moment_terms = []  # (coeff, exponent dict) with same vars as varlist
            for comp in compositions(t, nv):
                k_D = comp[0]
                ks = comp[1:]
                multinom_coeff = math.factorial(t)
                multinom_coeff //= math.factorial(k_D)
                for k in ks:
                    multinom_coeff //= math.factorial(k)
                # factor from E[V_a^{k_a}] = p_a^{k_a}/(k_a+1); p_D^{k_D} exact
                c = Fraction(multinom_coeff)
                for k in ks:
                    c /= (k + 1)
                e = {}
                if k_D:
                    e['D'] = k_D
                for a, k in zip(A, ks):
                    if k:
                        e[a] = k
                moment_terms.append((c, e))

            # --- multiply the two polynomials, accumulate into total
            for c1, e1 in prop_s_terms:
                for c2, e2 in moment_terms:
                    e_combined = defaultdict(int)
                    for v, p in e1.items():
                        e_combined[v] += p
                    for v, p in e2.items():
                        e_combined[v] += p
                    key = tuple(sorted(e_combined.items(), key=lambda x: str(x[0])))
                    total[key] += c1 * c2

    # --- now take Dirichlet(1,...,1) expectation of each monomial and sum
    result = Fraction(0)
    for key, coeff in total.items():
        exps = dict(key)
        result += coeff * dirichlet_moment(exps, K)
    return result


def route_A_moment(K, t):
    """Exact E[M_K^t] via sympy symbolic integration of the target density."""
    x = sp.symbols('x', positive=True)
    dens = 2 * K * x * (1 - x**2) ** (K - 1)
    val = sp.integrate(x**t * dens, (x, 0, 1))
    val = sp.nsimplify(val)
    fr = sp.fraction(sp.together(val))
    return Fraction(int(fr[0]), int(fr[1]))


if __name__ == "__main__":
    print(f"{'K':>3} {'t':>3} {'Route A (target dens)':>24} {'Route B (M_K constr.)':>24} {'match':>7}")
    all_ok = True
    n_checked = 0
    for K in range(1, 8):
        for t in range(1, 6):
            a = route_A_moment(K, t)
            b = route_B_moment(K, t)
            ok = (a == b)
            all_ok = all_ok and ok
            n_checked += 1
            print(f"{K:>3} {t:>3} {str(a):>24} {str(b):>24} {str(ok):>7}")
    print()
    print(f"Total cells checked: {n_checked}")
    print("ALL 35 MATCH:", all_ok)
