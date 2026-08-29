"""
lib_cdf.py -- shared exact symbolic definitions for D-SHARP-RATE-CONSTANTS-ATTEMPT
(wave 25, front a).

Transcribes, VERBATIM from THEOREM.md, the three closed-form finite-n CDFs
already PROVED and referee-ACCEPTed in the archive:

  - Proposicao D2 (K=2), THEOREM.md Estagio 42, line ~6262
  - Proposicao D3 (K=3), THEOREM.md Estagio 40, line ~6028
  - Proposicao D4 (K=4), THEOREM.md Estagio 43, line ~6351-6354

and the continuum-limit CDFs F_K(x) = 1 - (1-x^2)^K, cited from the
general-K continuum theorem of Estagio 24 (f_{M_K}(x) = 2*K*x*(1-x^2)^(K-1)).

These formulas are CITED, not re-derived: this front's job is the NEW
analytic content of Delta_n(x) := F_n^(K)(x) - F_K(x) and its sharp rate,
not the combinatorial proofs behind D2/D3/D4 themselves.

No probabilistic content is re-derived here -- only algebra/calculus.
"""

import sympy as sp

n, k, x = sp.symbols('n k x', positive=True)


def D2_formula():
    """Proposicao D2 (Estagio 42): P(M_n^(2) <= k/n), valid n>=2, 0<=k<=n-1."""
    return k * (k + 1) * (2 * n**2 - 3 * n + k - k**2) / (n**3 * (n - 1))


def D3_formula():
    """Proposicao D3 (Estagio 40): P(M_n^(3) <= k/n), valid n>=3, 0<=k<=n-1.

    P = k(k+1)[k^4 - 4k^3 - (3n^2-9n-5)k^2 + (3n^2-11n-2)k
                + (3n^4-12n^3+12n^2+2n)] / [n^4(n-1)(n-2)]
    """
    bracket = (k**4 - 4 * k**3 - (3 * n**2 - 9 * n - 5) * k**2
               + (3 * n**2 - 11 * n - 2) * k
               + (3 * n**4 - 12 * n**3 + 12 * n**2 + 2 * n))
    return k * (k + 1) * bracket / (n**4 * (n - 1) * (n - 2))


def D4_formula():
    """Proposicao D4 (Estagio 43): P(M_n^(4) <= k/n), valid n>=4, 0<=k<=n-1.

    P = k(k+1) Q(n,k) / [n^5 (n-1)(n-2)(n-3)]
    Q(n,k) = -k^6 + 9k^5 + (4n^2-18n-31)k^4 + (-16n^2+80n+51)k^3
             + (-6n^4+42n^3-55n^2-120n-40)k^2
             + (6n^4-50n^3+97n^2+70n+12)k
             + 4n^6-30n^5+74n^4-52n^3-30n^2-12n
    """
    Q = (-k**6 + 9 * k**5
         + (4 * n**2 - 18 * n - 31) * k**4
         + (-16 * n**2 + 80 * n + 51) * k**3
         + (-6 * n**4 + 42 * n**3 - 55 * n**2 - 120 * n - 40) * k**2
         + (6 * n**4 - 50 * n**3 + 97 * n**2 + 70 * n + 12) * k
         + 4 * n**6 - 30 * n**5 + 74 * n**4 - 52 * n**3 - 30 * n**2 - 12 * n)
    return k * (k + 1) * Q / (n**5 * (n - 1) * (n - 2) * (n - 3))


def F_continuum(K):
    """F_K(x) = 1 - (1-x^2)^K, cited from Estagio 24 (density 2*K*x*(1-x^2)^(K-1))."""
    return 1 - (1 - x**2)**K


CDF = {2: D2_formula(), 3: D3_formula(), 4: D4_formula()}
DENOM = {
    2: n**3 * (n - 1),
    3: n**4 * (n - 1) * (n - 2),
    4: n**5 * (n - 1) * (n - 2) * (n - 3),
}
NMIN = {2: 2, 3: 3, 4: 4}
