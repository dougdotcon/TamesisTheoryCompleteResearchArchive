"""
ADVERSARIAL REFEREE, items 4 and 5: the later numerical claims.

  * Corollary A2 (residual is exactly its own tail; identically 0 for p>r),
    checked against MY raw simulator and MY ladder.
  * psi_n^(K) for K=0..8 from Corollary A1, vs MY raw simulator (exact),
    including the three NEW formulas psi_n^(6,7,8) printed in Sec.5.
  * the multiplier table of Sec.3.1, regenerated independently.
  * D*^(p)_r(0) closed forms at p=3,4,5 -- fitted by ME on 2p+1 points and
    tested out of sample to r=300.
  * the NEGATIVE claim of Sec.6.3 item 3 / scorecard row 13: that the same
    {r^q phi_r} u {r^q} basis FAILS out of sample for b>=1.
  * the leading-coefficient pattern (2p-1)!!/(4^p p!).
"""
from fractions import Fraction as F
from math import comb, factorial
import sys
import sympy as sp

from ref_sim import Raw, A, P, g_hat, h_hat
from ref_ladder import Ladder, c1, peval, iszero, trim, preflect

fails = []
L = Ladder()
n_sym = sp.Symbol('n')


def phi(r):
    return F(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


def Dstar(p, r, b=0):
    """D*^(p)_r(b) = Phi^[p]_r(1,b) = sum_{j=p}^r c_j^(r)(b) c(j+1,j+1-p)."""
    return sum(A(r, j, b) * F(c1(j + 1, j + 1 - p)) for j in range(p, r + 1))


print("=" * 74)
print("PART G -- Sec.3.1 multiplier table, regenerated from MY ladder")
print("=" * 74)
print("  p\\k |" + "".join(f"{k:>12d}" for k in range(0, 7)))
tab_target = {
    0: [1, 1, 1, 1, 1, 1, 1],
    1: [1, 3, 6, 10, 15, 21, 28],
    2: [2, 11, 35, 85, 175, 322, 546],
    3: [6, 50, 225, 735, 1960, 4536, 9450],
    4: [24, 274, 1624, 6769, 22449, 63273, 157773],
    5: [120, 1764, 13132, 67284, 269325, 902055, 2637558],
    6: [720, 13068, 118124, 723680, 3416930, 13339535, 44990231],
    7: [5040, 109584, 1172700, 8409500, 45995730, 206070150, 790943153],
}
for p in range(0, 8):
    row = []
    for k in range(0, 7):
        # read the multiplier off MY ladder at a large enough r, several (r,b)
        vals = set()
        for r in range(k + p, k + p + 5):
            for b in range(0, 4):
                Ph = L.Phi(p, r, b)
                co = Ph[k] if k < len(Ph) else F(0)
                den = A(r, k + p, b)
                if den != 0:
                    vals.add(co / den)
        assert len(vals) == 1, (p, k, vals)
        v = vals.pop()
        assert v.denominator == 1
        row.append(v.numerator)
    ok = (row == tab_target[p])
    print(f"  {p:3d}  |" + "".join(f"{x:>12d}" for x in row) + ("   MATCH" if ok else "   *** MISMATCH ***"))
    if not ok:
        fails.append(("table", p, row, tab_target[p]))
print("  (the multiplier is r- and b-independent: each entry above was read off")
print("   from 20 distinct (r,b) pairs and every one agreed)")
print("  column k=0 is p! ; column k=1 is (p+1)! H_{p+1}:", end=" ")
ok = all(tab_target[p][0] == factorial(p) for p in range(8)) and \
     all(sp.Rational(tab_target[p][1]) == sp.factorial(p + 1) * sum(sp.Rational(1, i) for i in range(1, p + 2))
         for p in range(8))
print("CONFIRMED" if ok else "*** FALSE ***")
if not ok:
    fails.append("cols")

print()
print("=" * 74)
print("PART H -- Corollary A2: the expansion terminates; residual = its own tail")
print("=" * 74)
n_ok = 0
n_zero = 0
for n in range(3, 21):
    Rw = Raw(n)
    for r in range(0, min(7, n - 1) + 1):
        for b in range(0, min(4, n - 1 - r) + 1):
            for m in range(b + r + 1, n + 1):
                t = F(m, n)
                exact = Rw.gr(r, m, b)
                # full sum over p = 0..r must equal the exact value
                tot = sum(F(1, n ** p) * peval(L.Phi(p, r, b), t) for p in range(0, r + 1))
                n_ok += 1
                if tot != exact:
                    fails.append(("A2-sum", n, r, b, m, tot, exact))
                # residual R^(p) = exact - sum_{q<p} must equal sum_{q=p}^{r}
                for p in range(0, r + 3):
                    part = sum(F(1, n ** q) * peval(L.Phi(q, r, b), t) for q in range(0, p))
                    tail = sum(F(1, n ** q) * peval(L.Phi(q, r, b), t) for q in range(p, r + 1))
                    if exact - part != tail:
                        fails.append(("A2-tail", n, r, b, m, p))
                    if p > r:
                        n_zero += 1
                        if exact - part != 0:
                            fails.append(("A2-nonzero-tail-p>r", n, r, b, m, p))
            for a in range(0, n - b - r):
                s = F(a, n)
                exact = Rw.hr(r, a, b)
                tot = sum(F(1, n ** p) * peval(L.Psi(p, r, b), s) for p in range(0, r + 2))
                n_ok += 1
                if tot != exact:
                    fails.append(("A2-h-sum", n, r, b, a, tot, exact))
print(f"  g and h reconstructed EXACTLY from the finite ladder: {n_ok} exact points")
print(f"  residual identically 0 once p>r : {n_zero} instances checked")
print(f"  mismatches so far: {len(fails)}")

print()
print("=" * 74)
print("PART I -- Corollary A1: psi_n^(K) = g_K(n,0), K=0..8, vs MY raw simulator")
print("=" * 74)


def psi_closed(K):
    """Corollary A1 as an exact rational function of n."""
    return sp.simplify(sum(sp.Rational(factorial(K) ** 2, factorial(K - j) * factorial(K + j + 1))
                           * sp.prod([n_sym + i for i in range(1, j + 1)]) / n_sym ** j
                           for j in range(0, K + 1)))


target_psi = {
    6: (2048, 3072, 4293, 4638, 3529, 1662, 360, 6006),
    7: (16384, 28672, 48818, 67550, 70819, 52192, 23868, 5040, 51480),
    8: (32768, 65536, 131870, 223472, 300913, 306016, 219100, 97632, 20160, 109395),
}
for K in range(0, 9):
    pc = psi_closed(K)
    # confront with the raw simulator at every n from K+1 up to 22
    bad = 0
    npts = 0
    for n in range(K + 1, 23):
        Rw = Raw(n)
        got = Rw.gr(K, n, 0)
        want = pc.subs(n_sym, n)
        npts += 1
        if sp.Rational(got.numerator, got.denominator) != want:
            bad += 1
            fails.append(("psi", K, n, got, want))
    print(f"  K={K}: {sp.nsimplify(sp.factor(sp.together(pc)))}")
    print(f"        vs raw simulator at n={K+1}..22 : {npts} points, {bad} mismatches")
    if K in target_psi:
        c = target_psi[K]
        num = sum(c[i] * n_sym ** (K - i) for i in range(0, K + 1))
        den = c[-1] * n_sym ** K
        doc = sp.together(num / den)
        same = sp.simplify(doc - pc) == 0
        print(f"        vs the DOCUMENT'S PRINTED psi_n^({K}): "
              f"{'IDENTICAL' if same else '*** DIFFERS ***'}")
        if not same:
            fails.append(("psi-printed", K, sp.simplify(doc - pc)))

# the brute-force-confirmed anchor value
Rw = Raw(7)
g67 = Rw.gr(6, 7, 0)
print(f"  anchor: g_6(7,0) = {g67}   (published brute-force value 355081/823543): "
      f"{'MATCH' if g67 == F(355081, 823543) else '*** MISMATCH ***'}")
if g67 != F(355081, 823543):
    fails.append(("g6(7,0)", g67))

# the two "not in any prior document" 1/n^2 coefficients
for K, want in [(6, sp.Rational(1431, 2002)), (7, sp.Rational(2219, 2340))]:
    ser = sp.series(psi_closed(K).subs(n_sym, 1 / sp.Symbol('e', positive=True)),
                    sp.Symbol('e', positive=True), 0, 4).removeO()
    co = sp.expand(ser).coeff(sp.Symbol('e', positive=True), 2)
    print(f"  1/n^2 coefficient of psi_n^({K}) = {co}   (Estagio 8 reported {want}): "
          f"{'MATCH' if sp.simplify(co - want) == 0 else '*** MISMATCH ***'}")
    if sp.simplify(co - want) != 0:
        fails.append(("psi-coef", K, co, want))

print()
print("=" * 74)
print("PART J -- D*^(p)_r(0) at p=3,4,5: MY OWN fit, then out-of-sample to r=300")
print("=" * 74)
r_s = sp.Symbol('r')
doc_forms = {
    3: (5 * r_s ** 3 + 9 * r_s ** 2 + 2 * r_s) / 128,
    4: (105 * r_s ** 4 + 610 * r_s ** 3 + 123 * r_s ** 2 - 70 * r_s) / 6144,
    5: (189 * r_s ** 5 + 2590 * r_s ** 4 + 855 * r_s ** 3 - 490 * r_s ** 2 - 72 * r_s) / 24576,
}
doc_poly = {
    3: -r_s ** 2 / 12,
    4: -r_s ** 3 / 16 - 7 * r_s ** 2 / 240 + r_s / 120,
    5: -r_s ** 4 / 24 - 3 * r_s ** 3 / 40 + r_s ** 2 / 30,
}
for p in range(0, 6):
    # basis: {r^q phi_r : q=0..p} u {r^q : q=0..p-1}, i.e. 2p+1 unknowns
    nb1 = p + 1
    nb2 = p
    unk = sp.symbols(f'A0:{nb1}') + sp.symbols(f'B0:{max(nb2,1)}')
    Acoef = list(unk[:nb1])
    Bcoef = list(unk[nb1:nb1 + nb2])

    def model(rr):
        pr = sp.Rational(phi(rr).numerator, phi(rr).denominator)
        return sum(Acoef[q] * rr ** q * pr for q in range(nb1)) + \
               sum(Bcoef[q] * rr ** q for q in range(nb2))

    fitpts = list(range(0, 2 * p + 1 + 2))[:2 * p + 1] if p > 0 else [0]
    eqs = []
    for rr in fitpts:
        d = Dstar(p, rr, 0)
        eqs.append(sp.Eq(model(rr), sp.Rational(d.numerator, d.denominator)))
    sol = sp.solve(eqs, list(Acoef) + list(Bcoef), dict=True)
    if not sol:
        print(f"  p={p}: NO SOLUTION on the fit points -- basis inadequate")
        continue
    sol = sol[0]
    fitted_phi = sp.expand(sum(sol[Acoef[q]] * r_s ** q for q in range(nb1)))
    fitted_pol = sp.expand(sum(sol[Bcoef[q]] * r_s ** q for q in range(nb2))) if nb2 else sp.Integer(0)
    print(f"  p={p}: fitted on r={fitpts}  ->  D* = ({sp.factor(fitted_phi)})*phi_r + ({fitted_pol})")
    if p in doc_forms:
        agree = (sp.simplify(fitted_phi - doc_forms[p]) == 0 and
                 sp.simplify(fitted_pol - doc_poly[p]) == 0)
        print(f"        vs the DOCUMENT'S printed form: "
              f"{'IDENTICAL' if agree else '*** DIFFERS ***'}")
        if not agree:
            fails.append(("Dstar-form", p, sp.simplify(fitted_phi - doc_forms[p]),
                          sp.simplify(fitted_pol - doc_poly[p])))
    # out of sample, exact, to r=300
    bad = 0
    tested = 0
    for rr in range(0, 301):
        if rr in fitpts:
            continue
        pr = phi(rr)
        pred = F(sp.Rational(fitted_phi.subs(r_s, rr)).p, sp.Rational(fitted_phi.subs(r_s, rr)).q) * pr \
            + F(sp.Rational(fitted_pol.subs(r_s, rr)).p, sp.Rational(fitted_pol.subs(r_s, rr)).q)
        tested += 1
        if pred != Dstar(p, rr, 0):
            bad += 1
    print(f"        out-of-sample EXACT test, r=0..300 : {tested} points, {bad} failures")
    if bad:
        fails.append(("Dstar-oos", p, bad))

print()
print("  leading-in-r coefficient vs (2p-1)!!/(4^p p!):")
for p in range(0, 6):
    lead = sp.Rational(doc_forms[p].as_poly(r_s).LC()) if p in doc_forms else \
        [sp.Integer(1), sp.Rational(1, 4), sp.Rational(3, 32)][p]
    dbl = 1
    for i in range(1, 2 * p, 2):
        dbl *= i
    want = sp.Rational(dbl, 4 ** p * factorial(p))
    print(f"    p={p}: {lead}  vs (2p-1)!!/(4^p p!) = {want}   "
          f"{'MATCH' if sp.simplify(lead-want)==0 else '*** MISMATCH ***'}")

print()
print("=" * 74)
print("PART K -- the NEGATIVE claim (scorecard row 13): the same basis FAILS for b>=1")
print("=" * 74)
for p in [2, 3]:
    for b in [1, 2, 3]:
        nb1, nb2 = p + 1, p
        unk = sp.symbols(f'C0:{nb1}') + sp.symbols(f'D0:{max(nb2,1)}')
        Ac, Bc = list(unk[:nb1]), list(unk[nb1:nb1 + nb2])

        def model(rr):
            pr = sp.Rational(phi(rr).numerator, phi(rr).denominator)
            return sum(Ac[q] * rr ** q * pr for q in range(nb1)) + \
                   sum(Bc[q] * rr ** q for q in range(nb2))
        fitpts = list(range(0, 2 * p + 1))
        eqs = [sp.Eq(model(rr), sp.Rational(Dstar(p, rr, b).numerator,
                                            Dstar(p, rr, b).denominator)) for rr in fitpts]
        sol = sp.solve(eqs, list(Ac) + list(Bc), dict=True)
        if not sol:
            print(f"  p={p}, b={b}: fit itself has no solution")
            continue
        sol = sol[0]
        fp = sp.expand(sum(sol[Ac[q]] * r_s ** q for q in range(nb1)))
        fq = sp.expand(sum(sol[Bc[q]] * r_s ** q for q in range(nb2))) if nb2 else sp.Integer(0)
        bad = tested = 0
        for rr in range(2 * p + 1, 2 * p + 1 + 61):
            pr = phi(rr)
            v1 = sp.Rational(fp.subs(r_s, rr))
            v2 = sp.Rational(fq.subs(r_s, rr))
            pred = F(v1.p, v1.q) * pr + F(v2.p, v2.q)
            tested += 1
            if pred != Dstar(p, rr, b):
                bad += 1
        print(f"  p={p}, b={b}: fitted on {len(fitpts)} points, out-of-sample "
              f"{bad}/{tested} FAILURES  -> basis {'REFUTED' if bad > tested*0.5 else 'NOT refuted'}")
print("  (target claims 54-56 failures out of 61 at p=2 and p=3, b=1,2,3)")

print()
print("=" * 74)
print(f"CHECKS VERDICT: {len(fails)} mismatches")
for f in fails[:20]:
    print("  ", f)
print("=" * 74)
sys.exit(1 if fails else 0)
