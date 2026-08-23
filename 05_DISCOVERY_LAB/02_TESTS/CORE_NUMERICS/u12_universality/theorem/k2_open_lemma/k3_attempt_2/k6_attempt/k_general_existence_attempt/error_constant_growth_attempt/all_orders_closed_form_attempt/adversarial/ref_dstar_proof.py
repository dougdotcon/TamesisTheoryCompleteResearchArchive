"""
ADVERSARIAL REFEREE:
  (A) confirm the b=1 correction against the wave-10 referee's Theorem 3' (p=2);
  (B) carry out the proof route the target names in Sec.6.3 item 4 but does not
      execute, and thereby UPGRADE D*^(p)_r(0) at p=3,4,5 from NUMERICALLY
      VERIFIED to PROVED.

STRUCTURE THEOREM (mine).  Write N = 2r+1, S = N - 2X with X ~ Bin(N,1/2), i.e.
S is a sum of N i.i.d. +-1.  Then, with Q_p(j) := e_p(1,...,j) = c(j+1,j+1-p),
a polynomial in j of degree 2p, and A_j^{(r)}(0) = (phi_r/4^r) C(2r+1, r-j):

    D*^(p)_r(0) = (phi_r/4^r) sum_{i=0}^{r} C(N,i) Q_p(r-i)          [i := r-j]
                = (phi_r/4^r) sum_{i=0}^{r} C(N,i) R_p(v),  v := (N-2i)/2 = r+1/2-i,
                  R_p(v) := Q_p(v - 1/2), degree 2p.

Split R_p = E_p + O_p into even and odd parts.

  EVEN.  i <-> N-i maps v <-> -v and is a bijection of {i<=r} onto {i>=r+1}
  (exact because N is ODD, so there is no middle term).  Hence
      sum_{i<=r} C(N,i) E_p(v) = (1/2) sum_{i=0}^{N} C(N,i) E_p(v)
                               = 2^{N-1} E[E_p(S/2)].
  E[S^{2k}] is a polynomial in N of degree k (S is a sum of N iid mean-zero
  +-1's), so E[E_p(S/2)] is a polynomial in N -- hence in r -- of degree <= p.
  Since 2^{N-1} = 4^r, this block contributes  phi_r * U_p(r),  deg U_p <= p.

  ODD.  i<=r  <=>  S = N-2i >= 1  <=>  S > 0, and S never vanishes (N odd), so
      sum_{i<=r} C(N,i) O_p(v) = 2^N E[O_p(S/2) 1{S>0}] = 2^{N-1} E[O_p(|S|/2)].
  So this block contributes  (phi_r/4^r) 2^{N-1} E[O_p(|S|/2)] = phi_r E[O_p(|S|/2)].
  The classical fact E|S|^{2k+1} = (C(2r,r)/4^r) * W_k(r) with W_k a POLYNOMIAL
  (verified exactly below, and W_0 = 2r+1) plus (phi_r/4^r) C(2r,r) = 1/(2r+1)
  makes this block a RATIONAL function with the phi_r killed:
      phi_r E[O_p(|S|/2)] = sum_k (o_k / 2^{2k+1}) * W_k(r)/(2r+1) =: V_p(r).
  So the whole odd block is phi_r-free, and V_p is a polynomial once (2r+1)|W_k.

CONCLUSION (proved, given the two classical moment facts, both verified exactly
here over a wide range and both standard):
      D*^(p)_r(0) = U_p(r) phi_r + V_p(r),  deg U_p <= p, deg V_p <= DV(p),
with DV(p) read off exactly below.  Interpolating on enough points then PROVES
the closed form, since the interpolation matrix is nonsingular (checked exactly).
"""
from fractions import Fraction as F
from math import comb, factorial
import sympy as sp
from ref_sim import A
from ref_ladder import c1

r_s = sp.Symbol('r')


def phi(r):
    return F(4 ** r * factorial(r) ** 2, factorial(2 * r + 1))


def Dstar(p, r, b=0):
    return sum(A(r, j, b) * F(c1(j + 1, j + 1 - p)) for j in range(p, r + 1))


fails = []
print("=" * 78)
print("(A)  the b=1 correction, confirmed against the wave-10 referee's Theorem 3'")
print("=" * 78)


def theorem3prime(r, b):
    """wave-10 REFEREE_REPORT.md Part 3.3, transcribed from its prose (p=2 only)."""
    N = 2 * r + b + 1
    beta = F(b + 1)
    Pb = F(factorial(r) * factorial(r + b), factorial(N))
    Phib = Pb * 2 ** N

    def E(v):
        return 3 * v ** 4 + (F(9, 2) * beta ** 2 - 3 * beta - 3) * v ** 2 \
            + (F(3, 16) * beta ** 4 - F(1, 4) * beta ** 3 - F(3, 4) * beta ** 2 + beta)

    val = Phib / 48 * (F(3 * N * (3 * N - 2), 16)
                       + (F(9, 2) * beta ** 2 - 3 * beta - 3) * F(N, 4)
                       + F(3, 16) * beta ** 4 - F(1, 4) * beta ** 3
                       - F(3, 4) * beta ** 2 + beta)
    strip = sum((E(F(j) - beta / 2) * F(factorial(r) * factorial(r + b),
                                        factorial(r + j) * factorial(r + b + 1 - j))
                 for j in range(1, b + 1)), F(0))          # F(0) start: keep exact
    return val - strip * F(1, 48) - F((3 * b + 2) * r, 24) \
        - F(b * (3 * b + 1) * (b + 2), 48)


bad = 0
for b in range(0, 5):
    for r in range(0, 41):
        if theorem3prime(r, b) != Dstar(2, r, b):
            bad += 1
print(f"  Theorem 3' (transcribed) vs MY D*^(2)_r(b): r<=40, b<=4 -> {bad} mismatches")
if bad:
    fails.append(("thm3prime", bad))

b1_forms = {
    1: ((r_s + 1) / 4, sp.Rational(-1, 4)),
    2: ((r_s + 1) * (3 * r_s + 8) / 32, -(5 * r_s + 6) / 24),
    3: ((r_s + 1) * (5 * r_s ** 2 + 39 * r_s + 32) / 128, -(r_s + 1) * (7 * r_s + 12) / 48),
    4: ((r_s + 1) * (105 * r_s ** 3 + 1765 * r_s ** 2 + 3314 * r_s + 1536) / 6144,
        -(45 * r_s ** 3 + 229 * r_s ** 2 + 306 * r_s + 120) / 480),
}
print()
print("  MY b=1 closed forms, exact out-of-sample test to r=400:")
for p, (U, V) in b1_forms.items():
    bad = 0
    for r in range(0, 401):
        u = sp.Rational(U.subs(r_s, r))
        v = sp.Rational(V.subs(r_s, r))
        if F(u.p, u.q) * phi(r) + F(v.p, v.q) != Dstar(p, r, 1):
            bad += 1
    tag = ""
    if p == 2:
        agree = all(theorem3prime(r, 1) == Dstar(2, r, 1) for r in range(0, 40))
        tag = "   [== Theorem 3' at b=1: PROVED]" if agree else ""
    print(f"    p={p}: D*^({p})_r(1) = [{sp.factor(U)}] phi_r + [{sp.factor(V)}]"
          f"   -> {bad} failures over r=0..400{tag}")
    if bad:
        fails.append(("b1", p, bad))

print()
print("  WHY b=1 works and b>=2 does not (structural):")
print("    Theorem 3' prefactor  Phi_b(r)/phi_r = 2 * prod_{j=1}^{b} (2r+2j)/(2r+j+1)")
for b in range(0, 5):
    e = 2 * sp.prod([(2 * r_s + 2 * j) / (2 * r_s + j + 1) for j in range(1, b + 1)])
    print(f"      b={b}: {sp.cancel(e)}"
          + ("      <- constant, so a polynomial-in-r x phi_r basis suffices" if b <= 1
             else "   <- NOT polynomial in r: basis cannot work"))

print()
print("=" * 78)
print("(B)  the structure theorem, and the resulting PROOF of the p=3,4,5 forms")
print("=" * 78)

# --- classical fact 1: E[S^{2k}] is a polynomial in N of degree k
print("  fact 1: E[S^{2k}] (S = sum of N iid +-1) is a polynomial in N of degree k")
N_s = sp.Symbol('N')
ok = True
for k in range(0, 8):
    pts = []
    for N in range(1, 4 * k + 8):
        m = sum(sp.binomial(N, i) * (N - 2 * i) ** (2 * k) for i in range(0, N + 1)) / sp.Integer(2) ** N
        pts.append((N, sp.Rational(m)))
    poly = sp.interpolate(pts[:k + 1], N_s)
    bad = sum(1 for (N, v) in pts if sp.Rational(poly.subs(N_s, N)) != v)
    print(f"    k={k}: deg {sp.Poly(poly, N_s).degree()} (want {k}), "
          f"{bad} failures over N=1..{4*k+7}")
    if bad or sp.Poly(poly, N_s).degree() != max(k, 0):
        ok = ok and (bad == 0)
        if bad:
            fails.append(("evenmoment", k))

# --- classical fact 2: E|S|^{2k+1} = (C(2r,r)/4^r) W_k(r), W_k a polynomial,
#     and (2r+1) | W_k(r)
print()
print("  fact 2: for N = 2r+1, E|S|^{2k+1} = (C(2r,r)/4^r) * W_k(r), W_k polynomial")
Wk = {}
for k in range(0, 7):
    pts = []
    for r in range(0, 6 * k + 12):
        N = 2 * r + 1
        s = sum(sp.binomial(N, i) * (N - 2 * i) ** (2 * k + 1) for i in range(0, r + 1))
        # sum_{i<=r} C(N,i) S^{2k+1} = 2^{N-1} E|S|^{2k+1}
        val = sp.Rational(s * 2, sp.Integer(2) ** N)          # = E|S|^{2k+1}
        w = sp.Rational(val * sp.Integer(4) ** r, sp.binomial(2 * r, r))
        pts.append((r, w))
    deg = None
    for d in range(0, 3 * k + 6):
        poly = sp.interpolate(pts[:d + 1], r_s)
        if all(sp.Rational(poly.subs(r_s, rr)) == v for (rr, v) in pts):
            deg = d
            Wk[k] = sp.expand(poly)
            break
    q, rem = sp.div(sp.Poly(Wk[k], r_s), sp.Poly(2 * r_s + 1, r_s))
    isdiv = (rem.as_expr() == 0)
    print(f"    k={k}: W_k(r) = {sp.factor(Wk[k])}, degree {deg}, "
          f"divisible by (2r+1): {isdiv}")
    if not isdiv:
        fails.append(("odddiv", k))

print()
print("  => STRUCTURE: D*^(p)_r(0) = U_p(r) phi_r + V_p(r) with")
print("       deg U_p <= p                     (even block, fact 1)")
maxdegV = {}
for p in range(1, 7):
    # O_p has odd powers v^{2k+1} with 2k+1 <= 2p-1, so k <= p-1; V_p is a
    # combination of W_k(r)/(2r+1), deg = deg W_k - 1.
    dv = max(sp.Poly(Wk[k], r_s).degree() - 1 for k in range(0, p))
    maxdegV[p] = dv
    print(f"       deg V_p <= {dv}  at p={p}   (odd block, fact 2)")

print()
print("  => PROOF BY INTERPOLATION (the form is now known, so matching enough")
print("     points is a proof, not a fit):")
doc_forms = {
    3: ((5 * r_s ** 3 + 9 * r_s ** 2 + 2 * r_s) / 128, -r_s ** 2 / 12),
    4: ((105 * r_s ** 4 + 610 * r_s ** 3 + 123 * r_s ** 2 - 70 * r_s) / 6144,
        -r_s ** 3 / 16 - 7 * r_s ** 2 / 240 + r_s / 120),
    5: ((189 * r_s ** 5 + 2590 * r_s ** 4 + 855 * r_s ** 3 - 490 * r_s ** 2 - 72 * r_s) / 24576,
        -r_s ** 4 / 24 - 3 * r_s ** 3 / 40 + r_s ** 2 / 30),
}
for p in [3, 4, 5]:
    nU, nV = p + 1, maxdegV[p] + 1
    unk = sp.symbols(f'u0:{nU}') + sp.symbols(f'v0:{nV}')
    U, V = list(unk[:nU]), list(unk[nU:])
    npts = nU + nV
    eqs = []
    for rr in range(0, npts):
        pr = sp.Rational(phi(rr).numerator, phi(rr).denominator)
        d = Dstar(p, rr, 0)
        eqs.append(sp.Eq(sum(U[q] * rr ** q * pr for q in range(nU))
                         + sum(V[q] * rr ** q for q in range(nV)),
                         sp.Rational(d.numerator, d.denominator)))
    # nonsingularity of the interpolation matrix
    M = sp.Matrix([[sp.Rational(phi(rr).numerator, phi(rr).denominator) * rr ** q
                    for q in range(nU)] + [sp.Rational(rr ** q) for q in range(nV)]
                   for rr in range(0, npts)])
    det = M.det()
    sol = sp.solve(eqs, U + V, dict=True)[0]
    fU = sp.expand(sum(sol[U[q]] * r_s ** q for q in range(nU)))
    fV = sp.expand(sum(sol[V[q]] * r_s ** q for q in range(nV)))
    same = (sp.simplify(fU - doc_forms[p][0]) == 0 and sp.simplify(fV - doc_forms[p][1]) == 0)
    print(f"    p={p}: unknowns {npts} (degU<={p}, degV<={maxdegV[p]}), "
          f"interpolation det {'!= 0 (nonsingular)' if det != 0 else '== 0 (SINGULAR!)'}")
    print(f"          recovered  U_p = {sp.factor(fU)}")
    print(f"                     V_p = {sp.factor(fV)}")
    print(f"          == the DOCUMENT'S printed form: {'YES -> now PROVED' if same else 'NO'}")
    if det == 0:
        fails.append(("singular", p))
    if not same:
        fails.append(("upgrade-mismatch", p))
    bad = sum(1 for rr in range(0, 401)
              if F(sp.Rational(fU.subs(r_s, rr)).p, sp.Rational(fU.subs(r_s, rr)).q) * phi(rr)
              + F(sp.Rational(fV.subs(r_s, rr)).p, sp.Rational(fV.subs(r_s, rr)).q) != Dstar(p, rr, 0))
    print(f"          belt-and-braces exact check r=0..400: {bad} failures")
    if bad:
        fails.append(("upgrade-oos", p, bad))

print()
print("  same upgrade at p=6,7 (never stated by the document):")
for p in [6, 7]:
    if p not in maxdegV:
        dv = max(sp.Poly(Wk[k], r_s).degree() - 1 for k in range(0, min(p, 7)))
        maxdegV[p] = dv
    nU, nV = p + 1, maxdegV[p] + 1
    unk = sp.symbols(f'y0:{nU}') + sp.symbols(f'z0:{nV}')
    U, V = list(unk[:nU]), list(unk[nU:])
    npts = nU + nV
    eqs = []
    for rr in range(0, npts):
        pr = sp.Rational(phi(rr).numerator, phi(rr).denominator)
        d = Dstar(p, rr, 0)
        eqs.append(sp.Eq(sum(U[q] * rr ** q * pr for q in range(nU))
                         + sum(V[q] * rr ** q for q in range(nV)),
                         sp.Rational(d.numerator, d.denominator)))
    sol = sp.solve(eqs, U + V, dict=True)[0]
    fU = sp.expand(sum(sol[U[q]] * r_s ** q for q in range(nU)))
    fV = sp.expand(sum(sol[V[q]] * r_s ** q for q in range(nV)))
    bad = sum(1 for rr in range(0, 251)
              if F(sp.Rational(fU.subs(r_s, rr)).p, sp.Rational(fU.subs(r_s, rr)).q) * phi(rr)
              + F(sp.Rational(fV.subs(r_s, rr)).p, sp.Rational(fV.subs(r_s, rr)).q) != Dstar(p, rr, 0))
    lead = sp.Poly(fU, r_s).LC()
    dbl = 1
    for i in range(1, 2 * p, 2):
        dbl *= i
    want = sp.Rational(dbl, 4 ** p * factorial(p))
    print(f"    p={p}: U_p = {sp.factor(fU)}")
    print(f"          V_p = {sp.factor(fV)}   [{bad} failures r=0..250]")
    print(f"          leading coeff {lead} vs (2p-1)!!/(4^p p!) = {want}: "
          f"{'MATCH' if sp.simplify(lead-want)==0 else 'MISMATCH'}")
    if bad:
        fails.append(("p67", p, bad))

print()
print("=" * 78)
print(f"VERDICT: {len(fails)} problems")
for f in fails[:20]:
    print("  ", f)
print("=" * 78)
