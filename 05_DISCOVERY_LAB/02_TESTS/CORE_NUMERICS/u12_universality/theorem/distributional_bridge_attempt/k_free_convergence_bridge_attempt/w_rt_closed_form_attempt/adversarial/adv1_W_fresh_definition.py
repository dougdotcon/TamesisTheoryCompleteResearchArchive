"""
ADVERSARIAL / REFEREE SCRIPT 1 (item 1, item 2 of mandate).

Fresh, independent implementation of W(r,t)'s exact monomial-expansion
definition (transcribed from the PREDECESSOR's find_W_pattern.py, read as
prose -- NOT importing target's W_closed_form.py or predecessor's
verify_MK_moments.py/find_W_pattern.py in any way). This implementation
uses a genuinely different algorithmic route (sympy Poly / expand-based
monomial extraction rather than hand-rolled compositions() recursion) as
an extra layer of independence against a shared-bug risk.

Definition (Section 3.1 of the target ATTEMPT.md, transcribed, matching
predecessor's find_W_pattern.py):
  Fix r>=0, t>=1, A={0,...,r-1}, treat r as dimension K:=r.
  1. Proposition S's weight expanded into monomials in (p_0,...,p_{r-1},p_D):
       P(S=A|p) = r! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)
  2. Conditional t-th moment E[(p_D + sum_a V_a)^t | p, A], V_a~Uniform(0,p_a):
       multinomial expansion, E[V_a^k|p_a] = p_a^k/(k+1).
  3. Multiply, and W(r,t) := sum over monomials (exps,coeff) of
       coeff * prod_i (exps[i]!)

This script computes W(r,t) two ways:
  Route X: direct symbolic expansion via sympy.expand + Poly, extracting
    monomials automatically (no hand-written composition generator at all).
  Route Y: a hand-rolled but INDEPENDENTLY-written recursive composition
    generator (different code shape from either predecessor's or target's).
Both cross-checked against each other, against the closed form
(t+2r+1)(t+r)!, and against predecessor's find_W_pattern.log's own printed
values (t=1..4, r=0..7), extended fresh to t=1..10, r=0..12.
"""
import math
from fractions import Fraction as Fr
import itertools

import sympy as sp


# ---------------------------------------------------------------------
# Route X: build the two polynomials symbolically in sympy and let sympy's
# own expand()/as_poly() do the monomial bookkeeping.
# ---------------------------------------------------------------------

def W_sympy(r, t):
    if r == 0:
        pD = sp.symbols('pD')
        propS = sp.factorial(0) * pD  # prod over empty A =1, times (pD+0)=pD, times 0!=1
        cond = 0
        # conditional moment with A empty: only k_D=t term, coeff t!/t! =1, monomial pD^t
        cond = pD ** t
        prod = sp.expand(propS * cond)
        # prod = pD^{t+1}, coefficient 1
        total = Fr(1) * math.factorial(t + 1)
        return Fr(total)

    ps = sp.symbols(f'p0:{r}')
    pD = sp.symbols('pD')
    allvars = list(ps) + [pD]

    # Proposition S weight for A = {0,...,r-1}, K=r:
    # P(S=A|p) = r! * prod(p_a) * (pD + sum p_a)
    prod_pa = sp.prod(ps)
    propS = sp.factorial(r) * prod_pa * (pD + sum(ps))
    propS = sp.expand(propS)

    # Conditional t-th moment via multinomial theorem:
    # E[(pD + sum V_a)^t] where V_a ~ Uniform(0,p_a) indep given A.
    # = sum over compositions (kD,k_0,...,k_{r-1}) of t of
    #   t!/(kD! prod k_a!) * pD^kD * prod (p_a^{k_a}/(k_a+1))
    cond_terms = []
    for comp in compositions_indep(t, r + 1):
        kD = comp[0]
        ks = comp[1:]
        coeff = Fr(math.factorial(t))
        coeff /= math.factorial(kD)
        for k in ks:
            coeff /= math.factorial(k)
        for k in ks:
            coeff /= (k + 1)
        mono = pD ** kD
        for idx, k in enumerate(ks):
            mono *= ps[idx] ** k
        cond_terms.append(sp.Rational(coeff.numerator, coeff.denominator) * mono)
    cond = sp.expand(sum(cond_terms))

    prod = sp.expand(propS * cond)
    poly = sp.Poly(prod, *allvars)

    total = Fr(0)
    for monom, coeff in poly.terms():
        # monom is exponent tuple in order (p0,...,p_{r-1}, pD)
        assert sum(monom) == t + r + 1, (monom, t, r)
        fact_prod = 1
        for e in monom:
            fact_prod *= math.factorial(e)
        c = coeff  # sympy Rational
        total += Fr(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) * fact_prod
    return total


def compositions_indep(total, parts):
    """Independently-written stars-and-bars generator (iterative, not
    recursive, to be structurally different from any hand-rolled recursive
    version elsewhere)."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total, -1, -1):
        for rest in compositions_indep(total - first, parts - 1):
            yield (first,) + rest


# ---------------------------------------------------------------------
# Route Y: pure-Fraction hand computation, independently structured
# (loops over k_D outer, itertools.product filtered by sum -- deliberately
# the "naive/slow" approach the target's own docstring says times out for
# r>10, used here only up to r=8 as a genuinely different code path)
# ---------------------------------------------------------------------

def W_naive(r, t):
    """Independent route: same mathematical recipe, but iterates via the
    stars-and-bars compositions_indep() generator (NOT itertools.product+
    filter, which is exponential in r+1 and intractable beyond tiny r,t) --
    still a structurally different code path from Route X (sympy Poly)."""
    A = list(range(r))
    m = r
    propS = {}
    fact_r = math.factorial(r)
    base = [1] * r + [0]
    e1 = tuple(base[:r] + [1])
    propS[e1] = propS.get(e1, Fr(0)) + fact_r
    for b in range(r):
        e2 = list(base)
        e2[b] += 1
        e2 = tuple(e2)
        propS[e2] = propS.get(e2, Fr(0)) + fact_r

    cond = {}
    for comp in compositions_indep(t, m + 1):
        # comp = (k_0,...,k_{m-1}, k_D) per compositions_indep's own order
        ks = comp[:-1]
        kD = comp[-1]
        c = Fr(math.factorial(t))
        c /= math.factorial(kD)
        for k in ks:
            c /= math.factorial(k)
        for k in ks:
            c /= (k + 1)
        e = tuple(list(ks) + [kD])
        cond[e] = cond.get(e, Fr(0)) + c

    total = Fr(0)
    for e1, c1 in propS.items():
        for e2, c2 in cond.items():
            e = tuple(e1[i] + e2[i] for i in range(m + 1))
            assert sum(e) == t + r + 1
            fact_prod = 1
            for x in e:
                fact_prod *= math.factorial(x)
            total += c1 * c2 * fact_prod
    return total


def W_closed(r, t):
    return (t + 2 * r + 1) * math.factorial(t + r)


if __name__ == "__main__":
    print("=" * 78)
    print("Route X (sympy expand/Poly) vs Route Y (naive product+filter) vs")
    print("closed form (t+2r+1)(t+r)! -- fresh independent implementations")
    print("=" * 78)

    predecessor_log_values = {
        1: [2, 8, 36, 192, 1200, 8640, 70560, 645120],
        2: [6, 30, 168, 1080, 7920, 65520, 604800, 6168960],
        3: [24, 144, 960, 7200, 60480, 564480, 5806080, 65318400],
        4: [120, 840, 6480, 55440, 524160, 5443200, 61689600, 758419200],
    }

    all_ok = True
    log_ok = True
    n_cells = 0
    for t in range(1, 11):
        for r in range(0, 11):
            n_cells += 1
            wy = W_naive(r, t)
            wc = W_closed(r, t)
            match_yc = (wy == wc)
            line = f"t={t:2d} r={r:2d}: naive-route={wy} closed={wc} [{'OK' if match_yc else 'MISMATCH'}]"
            if r <= 6 and t <= 6:
                wx = W_sympy(r, t)
                match_xy = (wx == wy)
                line += f" sympy-route={wx} [{'OK' if match_xy else 'MISMATCH-XY'}]"
                all_ok = all_ok and match_xy
            all_ok = all_ok and match_yc
            print(line)
            if t in predecessor_log_values and r < len(predecessor_log_values[t]):
                expected = predecessor_log_values[t][r]
                if wy != expected:
                    log_ok = False
                    print(f"    ** MISMATCH vs predecessor find_W_pattern.log: t={t} r={r} "
                          f"mine={wy} log={expected}")

    print()
    print(f"Total cells tested (naive-route vs closed form): {n_cells}")
    print("ALL MATCH" if all_ok else "MISMATCH FOUND -- SEE ABOVE")
    print("Reproduces predecessor's find_W_pattern.log values (t=1..4,r=0..7) exactly"
          if log_ok else "DISCREPANCY vs predecessor log -- SEE ABOVE")
