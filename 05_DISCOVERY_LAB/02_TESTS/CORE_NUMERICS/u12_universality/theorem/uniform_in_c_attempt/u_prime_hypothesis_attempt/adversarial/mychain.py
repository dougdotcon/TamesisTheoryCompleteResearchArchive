"""
Independent, from-scratch reimplementation of the (a,b,r) exploration-walk
Markov chain, written ONLY from the transition-rule statements in the PRIMARY
SOURCE `theorem/k2_open_lemma/k3_attempt_2/ATTEMPT.md` Sec.2 (read directly by
the referee, not from this front's own `chain.py`, which is never opened).

State while tracing the forward orbit of a fixed reference point x*:
  a := # of pi-queries made so far (points permanently removed from the
       future pi-target pool)
  b := # of points reached via a U-jump onto fresh territory (still available
       as future pi-targets)
  r := # of the K sources not yet reached by the walk

g(a,b,r) := P(x* eventually cyclic), starting at a NON-source point, about to
            make a pi-query.
h(a,b,r) := P(x* eventually cyclic), starting AT a source, about to draw its
            own U.

Transition rules (Proposition, k3_attempt_2/ATTEMPT.md Sec.2), m := n-a:

  g(a,b,r) = 1/m + (r/m) h(a+1,b,r-1) + ((m-1-r-b)/m) g(a+1,b,r)
  h(a,b,r) = 1/n + (r/n) h(a,b+1,r-1) + ((n-1-a-b-r)/n) g(a,b+1,r)

with the "continue" coefficient vanishing exactly at the terminal state, so
the recursion is finite and well-founded (a+b strictly increases with every
recursive call and is bounded by n).

psi_n^{(K)}   = g(0,0,K)
psi_n^{(K),R} = h(0,0,K-1)     (K >= 1)

phi_n^{(K)} = (K/n) psi_n^{(K),R} + (1 - K/n) psi_n^{(K)}     (Reduction Lemma A,
              k2_open_lemma/ATTEMPT.md Sec.2 -- also re-derived and used only as
              a bookkeeping identity here, not assumed correct without check;
              see check01 for an independent symbolic sanity pass on it too.)

This entire module is independent of every .py file living under
u_prime_hypothesis_attempt/ (verify_decomposition.py, verify_closed_form.py,
verify_inequalities.py) and under uniform_in_c_attempt/ (chain.py) -- none of
those files were read by the author of this module.
"""
from fractions import Fraction


def make_solver(n):
    memo_g = {}
    memo_h = {}

    def g(a, b, r):
        key = (a, b, r)
        if key in memo_g:
            return memo_g[key]
        m = n - a
        assert m >= 1, (a, b, r, n)
        val = Fraction(1, m)
        if r > 0:
            val += Fraction(r, m) * h(a + 1, b, r - 1)
        cont_num = m - 1 - r - b
        assert cont_num >= 0, ("g continue coeff negative", a, b, r, n)
        if cont_num != 0:
            val += Fraction(cont_num, m) * g(a + 1, b, r)
        memo_g[key] = val
        return val

    def h(a, b, r):
        key = (a, b, r)
        if key in memo_h:
            return memo_h[key]
        val = Fraction(1, n)
        if r > 0:
            val += Fraction(r, n) * h(a, b + 1, r - 1)
        cont_num = n - 1 - a - b - r
        assert cont_num >= 0, ("h continue coeff negative", a, b, r, n)
        if cont_num != 0:
            val += Fraction(cont_num, n) * g(a, b + 1, r)
        memo_h[key] = val
        return val

    return g, h


def psi(n, K):
    """psi_n^{(K)} = P(generic non-source point is cyclic)."""
    g, h = make_solver(n)
    return g(0, 0, K)


def psi_R(n, K):
    """psi_n^{(K),R} = P(a rerouted source point is cyclic), K >= 1."""
    assert K >= 1
    g, h = make_solver(n)
    return h(0, 0, K - 1)


def phi(n, K):
    """phi_n^{(K)} via Reduction Lemma A, from psi/psi_R computed by THIS
    independent chain (not via the closed forms this front derives).
    NOTE: only valid for n > K -- the chain's own transition-rule domain
    (primary source: "every reachable state (a,b,r) with a+b+r<n") requires
    a genuine non-source reference point to exist. K=n (all points sources)
    is a different quantity, checked separately against Q(n)/n."""
    assert n > K, "chain domain requires n>K; K=n is the separate boundary case"
    if K == 0:
        g, h = make_solver(n)
        v = g(0, 0, 0)
        assert v == 1, v
        return Fraction(1, 1)
    g, h = make_solver(n)
    ps = g(0, 0, K)
    psR = h(0, 0, K - 1)
    return Fraction(K, n) * psR + Fraction(1 - Fraction(K, n)) * ps


def phi_direct(n, K):
    """phi_n^{(K)} computed directly as the average over ALL n points, i.e.
    (K*psi_R + (n-K)*psi)/n -- an alternate but algebraically identical route
    through the SAME g/h primitives, kept separate as an extra sanity check
    that Lemma A's weights were transcribed correctly here."""
    if K == 0:
        return phi(n, 0)
    g, h = make_solver(n)
    ps = g(0, 0, K)
    psR = h(0, 0, K - 1)
    return (K * psR + (n - K) * ps) / n


if __name__ == "__main__":
    # Minimal self-test: K=0 always gives phi=1 (no sources -> f=pi, a
    # permutation, every point cyclic), for several n.
    for n in range(1, 8):
        assert phi(n, 0) == 1, (n, phi(n, 0))
    # phi(n,n): every point rerouted -> uniform random mapping; sanity that
    # psi_R and psi coincide there is checked in check07 against Q(n)/n.
    print("mychain.py self-test OK")
