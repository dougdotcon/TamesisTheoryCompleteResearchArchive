"""
adv02_numeric_check.py -- REFEREE independent numerical verification.

Two INDEPENDENT evaluators of term_m(n,gamma), neither copied from (nor
structurally similar to) the front's own script 03/05 quadrature evaluator:

  (A) EXACT hypergeometric route: I(n,m,gamma) = Integral_0^1 t^m(1-t)^m
      (1-gamma t)^(n-m) dt is a classical Euler integral representation
      of 2F1:
        I(n,m,gamma) = B(m+1,m+1) * 2F1(m-n, m+1; 2m+2; gamma)
      (Euler's integral formula for 2F1, a textbook fact, matched
      against the front's own cited Beta-integral I(n,m,gamma) purely by
      parameter substitution here -- not quadrature at all). Since
      a=m-n is a NEGATIVE INTEGER for n>m, the series TERMINATES after
      n-m+1 terms -- an EXACT finite sum, evaluated here via mpmath's
      hyp2f1 (which sums the terminating series to machine/arbitrary
      precision, no quadrature error whatsoever). Used at n up to a few
      thousand (terminating-series cost grows like n-m).

  (B) A fresh quadrature evaluator, differently structured from the
      front's (no node-seeding near s~m/gamma; plain adaptive tanh-sinh
      over t in [0,1] directly, no t=s/n substitution), used to push to
      much larger n (up to 10^9) where route (A)'s O(n) series-summation
      cost becomes impractical.

Both are compared against the front's closed-form prediction
    term_m(n,gamma) - 1/gamma  ~  A_m(gamma)/n,   A_m(gamma) = m(m+3)/(2g) - m(m+1)/g^2
"""
import mpmath as mp

def A_m(m_val, gamma_val):
    g = mp.mpf(gamma_val)
    mm = mp.mpf(m_val)
    return mm*(mm+3)/(2*g) - mm*(mm+1)/g**2

def term_m_via_2F1(n_val, m_val, gamma_val, dps=60):
    """EXACT (terminating-series) route via Euler's integral formula for 2F1."""
    mp.mp.dps = dps
    g = mp.mpf(gamma_val)
    n_mp = mp.mpf(n_val)
    B = mp.factorial(m_val)**2 / mp.factorial(2*m_val+1)
    hyp = mp.hyp2f1(m_val - n_val, m_val + 1, 2*m_val + 2, g)
    I = B * hyp
    Bm = mp.factorial(m_val)**2 / mp.factorial(2*m_val+1)
    Tnm = mp.binomial(n_val + m_val + 1, 2*m_val+1) * I / Bm
    return (g**m_val / n_mp**m_val) * mp.factorial(m_val) * Tnm

def term_m_via_quad_plain(n_val, m_val, gamma_val, dps=60):
    """Fresh, differently-structured quadrature: DIRECTLY over t in [0,1],
    no t=s/n substitution, no node-seeding -- a genuinely different
    implementation from both the front's script 03/05 and route (A) above."""
    mp.mp.dps = dps
    g = mp.mpf(gamma_val)
    n_mp = mp.mpf(n_val)

    def integrand(t):
        return t**m_val * (1 - t)**m_val * (1 - g*t)**(n_val - m_val)

    I = mp.quad(integrand, [0, 1])
    Bm = mp.factorial(m_val)**2 / mp.factorial(2*m_val+1)
    Tnm = mp.binomial(n_val + m_val + 1, 2*m_val+1) * I / Bm
    return (g**m_val / n_mp**m_val) * mp.factorial(m_val) * Tnm


print("="*100)
print("PART 1: exact (terminating 2F1 series) route, n up to 4000")
print("="*100)
print(f"{'m':>2} {'gamma':>5} {'n':>6} {'n*(term_m-1/g)':>20} {'A_m predicted':>16} {'rel.err':>12}")
for gamma_val in ['0.3', '0.5', '0.8']:
    for m_val in [1, 2, 3, 4]:
        for n_val in [200, 800, 3200]:
            dps = 60
            tm = term_m_via_2F1(n_val, m_val, gamma_val, dps=dps)
            g = mp.mpf(gamma_val)
            lhs = n_val * (tm - 1/g)
            Am = A_m(m_val, gamma_val)
            rel_err = abs((lhs - Am)/Am) if Am != 0 else abs(lhs)
            print(f"{m_val:>2} {gamma_val:>5} {n_val:>6} {mp.nstr(lhs,10):>20} {mp.nstr(Am,10):>16} {mp.nstr(rel_err,6):>12}")

print()
print("Cross-check: route (A) [exact 2F1] vs route (B) [fresh direct quadrature]")
print("agree with each other independently of the closed-form prediction:")
for gamma_val in ['0.3', '0.7']:
    for m_val in [2, 3]:
        for n_val in [500, 2000]:
            tA = term_m_via_2F1(n_val, m_val, gamma_val, dps=60)
            tB = term_m_via_quad_plain(n_val, m_val, gamma_val, dps=60)
            diff = abs(tA - tB)
            print(f"  m={m_val} g={gamma_val} n={n_val}: 2F1={mp.nstr(tA,15)}  quad={mp.nstr(tB,15)}  |diff|={mp.nstr(diff,6)}")

print()
print("="*100)
print("PART 2: fresh quadrature route pushed to very large n (up to 10^9),")
print("        confirming the O(1/n) rate and O(1/n^2) next-order structure")
print("="*100)
print(f"{'m':>2} {'gamma':>5} {'n':>12} {'n*(term_m-1/g)':>20} {'A_m predicted':>16} {'rel.err':>12}")
results = []
for gamma_val in ['0.5']:
    for m_val in [2, 3]:
        for n_val in [10**4, 10**6, 10**8, 10**9]:
            dps = max(60, int(mp.log10(mp.mpf(n_val))) + 30 + 8*m_val)
            tm = term_m_via_quad_plain(n_val, m_val, gamma_val, dps=dps)
            g = mp.mpf(gamma_val)
            lhs = n_val * (tm - 1/g)
            Am = A_m(m_val, gamma_val)
            rel_err = abs((lhs - Am)/Am) if Am != 0 else abs(lhs)
            results.append((m_val, gamma_val, n_val, rel_err))
            print(f"{m_val:>2} {gamma_val:>5} {n_val:>12} {mp.nstr(lhs,12):>20} {mp.nstr(Am,12):>16} {mp.nstr(rel_err,6):>12}")

print()
print("Ratio of successive relative errors (expect ~ n2/n1, confirming O(1/n^2)")
print("next-order structure, i.e. the FULL claimed rate, not just the limit):")
by_key = {}
for (m_val, gamma_val, n_val, rel_err) in results:
    by_key.setdefault((m_val, gamma_val), []).append((n_val, rel_err))
for key, lst in by_key.items():
    lst.sort()
    for i in range(len(lst)-1):
        n1, e1 = lst[i]
        n2, e2 = lst[i+1]
        ratio = e1/e2 if e2 != 0 else mp.mpf('inf')
        expect = mp.mpf(n2)/mp.mpf(n1)
        print(f"  m={key[0]} g={key[1]}: n {n1}->{n2}: ratio={mp.nstr(ratio,6)}  expect~{mp.nstr(expect,6)}")

print()
print("ALL INDEPENDENT NUMERICAL CHECKS COMPLETE.")
