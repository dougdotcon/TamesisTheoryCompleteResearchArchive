"""
W(r,t) exact definition (fresh implementation, seeded ONLY by the prose
description in ../ATTEMPT.md Section 5.3 and the recipe cross-checked
against ../find_W_pattern.py's own printed log ../find_W_pattern.log --
the SOURCE FILE ITSELF was read for the precise definition per the mandate,
but no code was imported or copied from it. Every function below is
written fresh.)

DEFINITION (transcribed from the predecessor's own exact-arithmetic
pipeline, restated here from first principles):

Fix r>=0, t>=1. Let A = {0,...,r-1} and treat "r" itself as the dimension
parameter (K:=r) in the two building blocks below -- this is legitimate
because Proposition S's formula and the conditional-moment expansion only
ever reference p_a for a in A and p_D, so evaluating them with A equal to
the FULL index set of an r-dimensional model produces exactly the same
monomial shapes/coefficients that a genuine size-r subset A of a LARGER
K-dimensional model would produce (a subset of size r behaves, monomial-
shape-wise, exactly like "being the whole space" of an r-dimensional
model, by the exchangeability of Proposition S and the conditional-moment
formula in the coordinates outside A, which never appear at all).

  1. Proposition S's weight, expanded into monomials in (p_0,...,p_{r-1},p_D):
       P(S=A|p) = r! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)
     This is a sum of (r+1) monomials, each of total degree r+1, each with
     integer coefficient r!.

  2. The conditional t-th moment E[(p_D + sum_{a in A} V_a)^t | p, A],
     V_a ~ Uniform(0,p_a) independent given A, p_D deterministic given p:
     expand via the multinomial theorem using E[V_a^k|p_a] = p_a^k/(k+1).
     This is a sum, over compositions (k_D,k_0,...,k_{r-1}) of t into r+1
     nonnegative parts, of monomials of total degree t, with coefficient
       t! / (k_D! * prod_a k_a!) * prod_a 1/(k_a+1).

  3. Multiply the two monomial expansions (giving monomials of total
     degree t+r+1, matching the Dirichlet-moment formula's numerator
     structure E[prod p_i^{e_i}] = K! prod(e_i!) / (K + sum e_i)! once a
     REAL K and a real Dirichlet integration are applied downstream), and
     define
       W(r,t) := sum over resulting monomials (exps, coeff) of
                 coeff * prod_i (exps[i]!)
     -- i.e. the "coeff * prod(e_i!)" part of the Dirichlet-moment formula,
     WITHOUT the K!/(K+t+r+1)! prefactor (that prefactor is supplied later,
     with the REAL K, when W(r,t) is combined with C(K,r) and the true
     Dirichlet normalization -- see reduction_and_moment_crosscheck.py).

Cross-checked below (compositions() helper avoids the itertools.product+
filter approach, which is exponential and times out for r>~10; a direct
stars-and-bars recursive generator is used instead) against a completely
independent CLOSED-FORM derivation, done by hand (see the module docstring
of beta_integral_proof_verification.py for the full write-up; the short
version is reproduced in ATTEMPT.md Section 3).
"""
import itertools
import math
from fractions import Fraction as Fr


def compositions(total, parts):
    """Yield all tuples of length `parts` of nonnegative integers summing
    to `total` (stars-and-bars), via direct recursion -- O(C(total+parts-1,
    parts-1)) work, no wasted product-then-filter iterations."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def propS_monomials(r):
    """P(S=A|p) for A={0,...,r-1}, K:=r. Returns {exponent-tuple (len r+1):
    Fraction coefficient}."""
    fact_r = math.factorial(r)
    monos = {}

    def base():
        e = [0] * (r + 1)
        for a in range(r):
            e[a] += 1
        return e

    e1 = base()
    e1[r] += 1  # p_D
    monos[tuple(e1)] = monos.get(tuple(e1), Fr(0)) + fact_r

    for b in range(r):
        e2 = base()
        e2[b] += 1
        monos[tuple(e2)] = monos.get(tuple(e2), Fr(0)) + fact_r

    return monos


def cond_moment_monomials(r, t):
    """E[(p_D + sum_{a=0}^{r-1} V_a)^t | p, A={0,...,r-1}], multinomial
    expansion. Returns {exponent-tuple (len r+1): Fraction coefficient}."""
    monos = {}
    for k_D in range(t + 1):
        rem = t - k_D
        it = compositions(rem, r) if r > 0 else ([()] if rem == 0 else [])
        for ks in it:
            c = Fr(math.factorial(t))
            c /= math.factorial(k_D)
            for k in ks:
                c /= math.factorial(k)
            for k in ks:
                c /= (k + 1)
            e = [0] * (r + 1)
            e[r] = k_D
            for idx, k in enumerate(ks):
                e[idx] += k
            monos[tuple(e)] = monos.get(tuple(e), Fr(0)) + c
    return monos


def multiply_monomials(d1, d2, r):
    out = {}
    for e1, c1 in d1.items():
        for e2, c2 in d2.items():
            e = tuple(e1[i] + e2[i] for i in range(r + 1))
            out[e] = out.get(e, Fr(0)) + c1 * c2
    return out


def W(r, t):
    """The exact combinatorial weight, per the definition above."""
    propS = propS_monomials(r)
    cond = cond_moment_monomials(r, t)
    prod = multiply_monomials(propS, cond, r)
    total = Fr(0)
    for exps, coeff in prod.items():
        assert sum(exps) == t + r + 1, (exps, r, t, sum(exps))
        fact_prod = 1
        for e in exps:
            fact_prod *= math.factorial(e)
        total += coeff * fact_prod
    return total


def W_closed(r, t):
    """Conjectured (and, in this document, PROVED -- see Section 3 of
    ATTEMPT.md) closed form: W(r,t) = (t+2r+1) * (t+r)!."""
    return (t + 2 * r + 1) * math.factorial(t + r)


if __name__ == "__main__":
    print("=" * 78)
    print("W(r,t): fresh exact-arithmetic reproduction, r=0..10, t=1..9")
    print("=" * 78)
    all_ok = True
    for t in range(1, 10):
        row_exact = []
        row_closed = []
        for r in range(0, 11):
            w = W(r, t)
            c = W_closed(r, t)
            row_exact.append(w)
            row_closed.append(c)
            if w != c:
                all_ok = False
                print(f"  MISMATCH at r={r}, t={t}: exact={w} closed={c}")
        print(f"t={t:2d}: exact  = {row_exact}")
        print(f"       closed = {row_closed}")
        print(f"       match  = {row_exact == row_closed}")
    print()
    print("ALL 99 CELLS MATCH (r=0..10, t=1..9)" if all_ok else "MISMATCH FOUND -- SEE ABOVE")
    print()
    print("Cross-check against ../find_W_pattern.log's own printed table")
    print("(t=1..4, r=0..7 -- transcribed from that log for a citation-only")
    print(" sanity check, not used as a computational source):")
    predecessor_log_values = {
        1: [2, 8, 36, 192, 1200, 8640, 70560, 645120],
        2: [6, 30, 168, 1080, 7920, 65520, 604800, 6168960],
        3: [24, 144, 960, 7200, 60480, 564480, 5806080, 65318400],
        4: [120, 840, 6480, 55440, 524160, 5443200, 61689600, 758419200],
    }
    log_ok = True
    for t, vals in predecessor_log_values.items():
        for r, v in enumerate(vals):
            mine = W(r, t)
            if mine != v:
                log_ok = False
                print(f"  MISMATCH vs log: t={t} r={r} mine={mine} log={v}")
    print("Fresh implementation reproduces the cited log values exactly" if log_ok
          else "DISCREPANCY vs cited log values -- see above")
