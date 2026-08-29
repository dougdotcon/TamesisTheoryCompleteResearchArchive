"""
Three independent computational routes to E[(M_K')^t], cross-checked
against each other and against the archive's known target E[M_K^t]
(THEOREM.md Estagio 24, f_K(x)=2Kx(1-x^2)^{K-1}). Every function here is
written fresh for this front -- no import from any predecessor script.

Route 1 (direct subset enumeration): the most literal computation --
for every subset A of {0,...,K-1}, expand Proposition S's weight and the
conditional t-th moment into monomials in the REAL K+1 variables
(p_0,...,p_{K-1},p_D), multiply, and integrate each monomial exactly
against the Dirichlet(1,...,1) density via the standard closed-form
Dirichlet moment formula E[prod p_i^{k_i}] = K! prod(k_i!) / (K+sum k_i)!.
This never groups subsets by size and never references W(r,t) at all.

Route 2 (r-grouped, via W(r,t)): uses the closed form W(r,t)=(t+2r+1)(t+r)!
proved in W_closed_form.py, and the reduction identity

    E[(M_K')^t] = K! * sum_{r=0}^K C(K,r) * W(r,t) / (K+t+r+1)!

(justified by exchangeability: Proposition S's weight and the conditional
moment, for a subset A of size r, depend on p only through {p_a : a in A}
and p_D, symmetrically -- so the monomial shapes/coefficients contributed
by ANY size-r subset are identical, and there are exactly C(K,r) of them;
grouping subsets by size and factoring out the common contribution is
exactly what W(r,t) captures. This is verified empirically below by Route
1 vs Route 2 agreeing exactly.)

Route 3 (target, independent of both): direct symbolic integration of
x^t * 2Kx(1-x^2)^{K-1} over [0,1] via sympy -- no reference to Proposition
S, Dirichlet moments, or W(r,t) at all.

If all three agree exactly (Fraction arithmetic, no floats), this
validates: (a) the W(r,t) closed form itself (Route 2 uses it), (b) the
exchangeability-based reduction identity (Route 1 vs Route 2), and (c)
that E[(M_K')^t] really does match the archive's already-proved target
moment (Route 1/2 vs Route 3) -- i.e. Claim B's moment-matching claim,
for every (K,t) tested.
"""
import itertools
import math
from fractions import Fraction as Fr

import sympy as sp

import W_closed_form as wcf  # same directory, this front's own file


# ---------------------------------------------------------------------
# Route 1: direct subset enumeration, full K-dimensional monomial algebra
# ---------------------------------------------------------------------

def propS_monomials_K(K, A):
    m = len(A)
    fact_m = math.factorial(m)
    monos = {}

    def base():
        e = [0] * (K + 1)
        for a in A:
            e[a] += 1
        return e

    e1 = base()
    e1[K] += 1
    monos[tuple(e1)] = monos.get(tuple(e1), Fr(0)) + fact_m
    for b in A:
        e2 = base()
        e2[b] += 1
        monos[tuple(e2)] = monos.get(tuple(e2), Fr(0)) + fact_m
    return monos


def cond_moment_monomials_K(K, A, t):
    A = list(A)
    m = len(A)
    monos = {}
    for k_D in range(t + 1):
        rem = t - k_D
        it = wcf.compositions(rem, m) if m > 0 else ([()] if rem == 0 else [])
        for ks in it:
            c = Fr(math.factorial(t))
            c /= math.factorial(k_D)
            for k in ks:
                c /= math.factorial(k)
            for k in ks:
                c /= (k + 1)
            e = [0] * (K + 1)
            e[K] = k_D
            for idx, a in enumerate(A):
                e[a] += ks[idx]
            monos[tuple(e)] = monos.get(tuple(e), Fr(0)) + c
    return monos


def multiply_monomials_K(d1, d2, K):
    out = {}
    for e1, c1 in d1.items():
        for e2, c2 in d2.items():
            e = tuple(e1[i] + e2[i] for i in range(K + 1))
            out[e] = out.get(e, Fr(0)) + c1 * c2
    return out


def dirichlet_moment(K, exps):
    num = math.factorial(K)
    for e in exps:
        num *= math.factorial(e)
    den = math.factorial(K + sum(exps))
    return Fr(num, den)


def E_MKprime_route1(K, t):
    total = Fr(0)
    for r in range(0, K + 1):
        for A in itertools.combinations(range(K), r):
            propS = propS_monomials_K(K, A)
            cond = cond_moment_monomials_K(K, A, t)
            prod = multiply_monomials_K(propS, cond, K)
            for exps, coeff in prod.items():
                total += coeff * dirichlet_moment(K, list(exps))
    return total


# ---------------------------------------------------------------------
# Route 2: r-grouped, via the proved closed form W(r,t)
# ---------------------------------------------------------------------

def E_MKprime_route2(K, t):
    total = Fr(0)
    for r in range(0, K + 1):
        c = math.comb(K, r)
        w = wcf.W_closed(r, t)
        total += Fr(c * w, math.factorial(K + t + r + 1))
    return total * math.factorial(K)


# ---------------------------------------------------------------------
# Route 3: target, fresh sympy integration, independent of Prop S entirely
# ---------------------------------------------------------------------

def target_route3(K, t):
    x = sp.symbols('x', positive=True)
    dens = 2 * K * x * (1 - x ** 2) ** (K - 1)
    val = sp.integrate(x ** t * dens, (x, 0, 1))
    val = sp.nsimplify(sp.simplify(val))
    num, den = sp.fraction(val)
    return Fr(int(num), int(den))


if __name__ == "__main__":
    print("=" * 78)
    print("Three-route cross-check of E[(M_K')^t], K=1..8, t=1..6")
    print("=" * 78)
    header = f"{'K':>3} {'t':>3} {'route1 (direct)':>22} {'route2 (via W)':>22} {'route3 (target)':>18}  match"
    print(header)
    all_ok = True
    for K in range(1, 9):
        for t in range(1, 7):
            r1 = E_MKprime_route1(K, t)
            r2 = E_MKprime_route2(K, t)
            r3 = target_route3(K, t)
            ok = (r1 == r2 == r3)
            all_ok = all_ok and ok
            print(f"{K:>3} {t:>3} {str(r1):>22} {str(r2):>22} {str(r3):>18}  {'OK' if ok else 'MISMATCH'}")
    print()
    print("ALL 48 CELLS: routes 1, 2, 3 agree exactly" if all_ok else "MISMATCH FOUND -- SEE ABOVE")
    print()
    print("This validates simultaneously: (a) the W(r,t) closed form,")
    print("(b) the exchangeability-based r-grouping reduction identity,")
    print("(c) that E[(M_K')^t] matches the archive's proved target E[M_K^t].")
