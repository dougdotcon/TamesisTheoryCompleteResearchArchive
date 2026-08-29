#!/usr/bin/env python3
"""
Script 03 -- the genuine mesoscale next-order correction to T_prof(lambda,
gamma) coming from the F(n,m,gamma) = (gamma/n)^m (n+m+1)!/((n-m)! m!)
piece, done CORRECTLY (i.e. accounting for the fact that T_prof itself is
the joint limit of ln F + ln I_leading, not of ln F alone -- see
ATTEMPT.md Sec 3 for the careful bookkeeping this script implements).

CITED, not re-derived here:
  - t*(n,m,gamma) = [2m+gamma n - sqrt(gamma^2 n^2 + 4(1-gamma) m^2)] / (2 gamma (m+n))
      [Estagio 56, PROVED]
  - g(t) := m ln t + m ln(1-t) + (n-m) ln(1-gamma t)   [Estagio 54/56, PROVED]
  - I_leading(n,m,gamma) := exp(g(t*)) * sqrt(2*pi / (-g''(t*)))
      [Estagio 56, the leading Laplace/Watson approx whose correction the
       predecessor front named Delta]
  - T_prof(lambda,gamma) = (1/gamma) * exp[-((2-gamma)/(2 gamma)) lambda^2]
      [Estagio 56, PROVED, lambda := m/sqrt(n)]
  - Delta(n,m,gamma) ~ 1/(12 lambda) * 1/sqrt(n), gamma-independent
      [predecessor front b, gamma_c_gamma_uniform_watson_remainder_attempt,
       PROVED/verified there]

DEFINE (this front):
  A(n,m,gamma) := ln F(n,m,gamma) + ln I_leading(n,m,gamma)   [EXACT, finite n,m]
  B(n,m,gamma) := A(n,m,gamma) - ln T_prof(lambda,gamma)      [-> 0 as n->infty]

Goal: extract K(lambda,gamma), the coefficient of the LEADING (1/sqrt(n))
term of B(n,m,gamma) at mesoscale m=lambda*sqrt(n). This K(lambda,gamma) is
defined so that

  term_m(n,gamma) = T_prof(lambda,gamma) * [1 + Delta_m(n,m,gamma)
                                               + Delta(n,m,gamma) + O(1/n)],
  Delta_m(n,m,gamma) := K(lambda,gamma)/sqrt(n)

i.e. Delta_m is EXACTLY the residual correction attributable to
"everything besides the already-cited Delta" -- by construction this
absorbs the F-piece's own next-order behavior AND any next-order
correction of I_leading's role in matching T_prof jointly with F (both
pieces genuinely entangle in how T_prof's m ln m cancellation works, so
Delta_m below is NOT claimed to be "F alone, in complete isolation from
I" -- this scoping caveat is stated explicitly, matching this lineage's
own discipline of not overclaiming a cleaner separation than what was
actually shown).

Method: substitute n = 1/eps**2, m = lambda/eps (so lambda = m/sqrt(n)
exactly, eps = 1/sqrt(n)), and Puiseux/Laurent-expand A(n,m,gamma) in eps
around eps=0. A first attempt uses sympy .series() directly; if this
times out (predecessor precedent: a similar full combined series did
not terminate within 300s), fall back to extracting order-by-order via
repeated sympy.limit() of remainders -- the SAME workaround technique
the predecessor used and disclosed.
"""
import sympy as sp
from sympy import symbols, sqrt, log, ln, exp, pi, Rational, simplify, series, limit, oo, nsimplify
import time

n, m, g, lam, eps = symbols('n m gamma lambda epsilon', positive=True)

print("="*78)
print("PART A: exact building blocks (all CITED closed forms, substituted,")
print("        not re-derived)")
print("="*78)

# t*(n,m,gamma), CITED
tstar = (2*m + g*n - sp.sqrt(g**2*n**2 + 4*(1-g)*m**2)) / (2*g*(m+n))

# g(t), CITED
t = symbols('t', positive=True)
g_of_t = m*log(t) + m*log(1-t) + (n-m)*log(1-g*t)

g_at_tstar = g_of_t.subs(t, tstar)

# g''(t), needed for A := -g''(t*)
gpp = sp.diff(g_of_t, t, 2)
gpp_at_tstar = gpp.subs(t, tstar)
A_curv = -gpp_at_tstar

print("t*(n,m,gamma) [cited]:", tstar)
print()
print("Building g(t*), -g''(t*) symbolically (exact substitution, no")
print("approximation yet) -- these are large expressions, not printed in full.")

# ln F(n,m,gamma), CITED/derived in script 01 (exact algebra)
lnF = m*log(g/n) + sp.loggamma(n+m+2) - sp.loggamma(n-m+1) - sp.loggamma(m+1)

# ln I_leading(n,m,gamma) = g(t*) + (1/2) ln(2*pi) - (1/2) ln(A_curv)
lnIlead = g_at_tstar + Rational(1,2)*log(2*pi) - Rational(1,2)*log(A_curv)

A_total = lnF + lnIlead   # = ln F + ln I_leading, EXACT

# ln T_prof(lambda,gamma), CITED
lnTprof = log(1/g) - ((2-g)/(2*g)) * lam**2

print()
print("="*78)
print("PART B: substitute mesoscale n=1/eps^2, m=lambda/eps and attempt a")
print("        direct Puiseux series of B = A_total - lnTprof in eps")
print("="*78)

n_sub = 1/eps**2
m_sub = lam/eps

A_total_eps = A_total.subs([(n, n_sub), (m, m_sub)])
B_expr = A_total_eps - lnTprof.subs(lam, lam)   # lnTprof already in terms of lam only

print("Attempting sympy series of B(eps) around eps=0 (timeout-guarded)...")
t0 = time.time()
try:
    import signal
    class Timeout(Exception):
        pass
    def handler(signum, frame):
        raise Timeout()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(240)
    B_series = sp.series(B_expr, eps, 0, 2).removeO()
    signal.alarm(0)
    elapsed = time.time() - t0
    print(f"Direct series() SUCCEEDED in {elapsed:.1f}s")
    print("B(eps) series (through eps^1):")
    print(" ", sp.simplify(B_series))
    DIRECT_SERIES_OK = True
except Exception as e:
    signal.alarm(0)
    elapsed = time.time() - t0
    print(f"Direct series() FAILED/timed out after {elapsed:.1f}s: {type(e).__name__}: {e}")
    print("Falling back to the predecessor's own disclosed workaround:")
    print("coefficient-by-coefficient extraction via sympy.limit, at fixed")
    print("numeric (lambda,gamma) sample points first (numeric-symbolic hybrid),")
    print("then symbolic confirmation at a few rational (lambda,gamma).")
    DIRECT_SERIES_OK = False

print()
print(f"[timing] Part B direct-series attempt total wall time: {time.time()-t0:.1f}s")
