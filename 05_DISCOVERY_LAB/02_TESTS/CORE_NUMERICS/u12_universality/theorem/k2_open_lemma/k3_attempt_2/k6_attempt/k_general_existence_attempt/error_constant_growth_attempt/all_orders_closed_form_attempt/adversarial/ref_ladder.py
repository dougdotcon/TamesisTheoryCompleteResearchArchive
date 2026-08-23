"""
ADVERSARIAL REFEREE, items 2 and 3: an INDEPENDENT general-order epsilon-ladder,
built from the order-p receiver ODE and source relation that I re-derived by hand
(see REFEREE_REPORT.md Part 2).  Nothing is read from the target's order_ladder.py.

MY OWN HAND DERIVATION (reproduced here so the code can be audited against it):

  eps = 1/n,  t = m/n,  s = a/n,  (m-1)/n = t - eps EXACTLY,
  and for h_{r-1}(n-m+1,b):  s' = (n-m+1)/n = (1-t) + eps EXACTLY.

  eta^[p]_r(t,b) := Psi^[p]_r(1-t,b),  hence  (Psi^[p])^(i)(1-t) = (-1)^i (eta^[p])^(i)(t).

  RECEIVER ODE (order p):
    t (Phi^[p]_r)'(t,b) + (1+r+b) Phi^[p]_r(t,b)
      = [p==0]
      + r    sum_{i=0}^{p}   ((-1)^i / i!)   (eta^[p-i]_{r-1})^(i)(t,b)
      + t    sum_{i=2}^{p+1} ((-1)^i / i!)   (Phi^[p+1-i]_r)^(i)(t,b)
      + (1+r+b) sum_{i=1}^{p} ((-1)^(i+1)/i!)(Phi^[p-i]_r)^(i)(t,b)

  equivalently, since (eta^[q])^(i)(t) = (-1)^i (Psi^[q])^(i)(1-t), the r-block is
      r sum_{i=0}^{p} (1/i!) (Psi^[p-i]_{r-1})^(i)(1-t,b)     -- ALL SIGNS +.
  (This second form is used in the code; the first is used in the report.  They
   are the same thing and each is a check on the other's signs.)

  SOURCE RELATION (order p), no Taylor expansion needed:
    Psi^[p]_r(s,b) = [p==1] + r Psi^[p-1]_{r-1}(s,b+1)
                     + (1-s) Phi^[p]_r(1-s,b+1) - (1+b+r) Phi^[p-1]_r(1-s,b+1)

  Solving the ODE is trivial coefficient-wise: if RHS = sum rho_k x^k then
    Phi^[p]_r = sum_k rho_k/(k+1+r+b) x^k,   denominator never 0.
"""
from fractions import Fraction as F
from math import factorial
import sys
from functools import lru_cache

# ---------------------------------------------------------------- polynomials
# a polynomial is a tuple of Fractions, index = power of its variable


def padd(*ps):
    L = max((len(p) for p in ps), default=0)
    out = [F(0)] * L
    for p in ps:
        for i, c in enumerate(p):
            out[i] += c
    return trim(out)


def pscale(p, c):
    return trim([c * x for x in p])


def pmulx(p):
    """multiply by the variable"""
    return trim([F(0)] + list(p))


def pdiff(p, k=1):
    q = list(p)
    for _ in range(k):
        q = [q[i] * i for i in range(1, len(q))]
        if not q:
            q = [F(0)]
    return trim(q)


def preflect(p):
    """given coeffs of q(x), return coeffs of q(1-x)."""
    out = [F(0)] * len(p)
    for i, c in enumerate(p):
        if c == 0:
            continue
        # (1-x)^i = sum_j C(i,j) (-x)^j
        from math import comb
        for jj in range(0, i + 1):
            out[jj] += c * comb(i, jj) * ((-1) ** jj)
    return trim(out)


def peval(p, x):
    v = F(0)
    for c in reversed(p):
        v = v * x + c
    return v


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p) if p else (F(0),)


ZERO = (F(0),)


def iszero(p):
    return all(c == 0 for c in p)


# ------------------------------------------------------------------ the ladder
class Ladder:
    def __init__(self):
        self._phi = {}
        self._psi = {}

    def Phi(self, p, r, b):
        """Phi^[p]_r(.,b) as coeffs in t."""
        key = (p, r, b)
        if key in self._phi:
            return self._phi[key]
        assert p >= 0 and r >= 0
        rhs = [F(1)] if p == 0 else [F(0)]
        rhs = tuple(F(x) for x in rhs)
        # r-block:  r * sum_{i=0}^{p} (1/i!) (Psi^[p-i]_{r-1})^(i)(1-t, b)
        if r >= 1:
            acc = ZERO
            for i in range(0, p + 1):
                psi = self.Psi(p - i, r - 1, b)          # in s
                d = pdiff(psi, i)                        # d/ds
                acc = padd(acc, pscale(preflect(d), F(1, factorial(i))))
            rhs = padd(rhs, pscale(acc, F(r)))
        # t-block:  t sum_{i=2}^{p+1} ((-1)^i/i!) (Phi^[p+1-i]_r)^(i)
        acc = ZERO
        for i in range(2, p + 2):
            q = p + 1 - i
            if q < 0:
                continue
            acc = padd(acc, pscale(pdiff(self.Phi(q, r, b), i),
                                   F((-1) ** i, factorial(i))))
        rhs = padd(rhs, pmulx(acc))
        # (1+r+b)-block: sum_{i=1}^{p} ((-1)^(i+1)/i!)(Phi^[p-i]_r)^(i)
        acc = ZERO
        for i in range(1, p + 1):
            q = p - i
            acc = padd(acc, pscale(pdiff(self.Phi(q, r, b), i),
                                   F((-1) ** (i + 1), factorial(i))))
        rhs = padd(rhs, pscale(acc, F(1 + r + b)))
        # solve t Phi' + (1+r+b) Phi = rhs
        sol = trim([rhs[kk] / F(kk + 1 + r + b) for kk in range(len(rhs))])
        self._phi[key] = sol
        return sol

    def Psi(self, p, r, b):
        """Psi^[p]_r(.,b) as coeffs in s."""
        key = (p, r, b)
        if key in self._psi:
            return self._psi[key]
        if p < 0:
            return ZERO
        out = (F(1),) if p == 1 else ZERO
        if r >= 1 and p >= 1:
            out = padd(out, pscale(self.Psi(p - 1, r - 1, b + 1), F(r)))
        # (1-s) Phi^[p]_r(1-s, b+1)
        ph = preflect(self.Phi(p, r, b + 1))             # Phi^[p](1-s) in s
        one_minus_s = (F(1), F(-1))
        prod = [F(0)] * (len(ph) + 1)
        for i, c in enumerate(ph):
            prod[i] += c * one_minus_s[0]
            prod[i + 1] += c * one_minus_s[1]
        out = padd(out, trim(prod))
        if p >= 1:
            out = padd(out, pscale(preflect(self.Phi(p - 1, r, b + 1)), F(-(1 + b + r))))
        self._psi[key] = trim(out)
        return self._psi[key]


# ------------------------------------------------------------- Stirling (own)
_S = {}


def c1(N, M):
    """unsigned Stirling number of the first kind, own recursion."""
    if (N, M) in _S:
        return _S[(N, M)]
    if N == 0 and M == 0:
        v = 1
    elif N == 0 or M == 0 or M > N:
        v = 0
    else:
        v = c1(N - 1, M - 1) + (N - 1) * c1(N - 1, M)
    _S[(N, M)] = v
    return v


def A(r, j, b):
    if j > r or j < 0:
        return F(0)
    num = 1
    for i in range(r - j + 1, r + 1):
        num *= i
    den = 1
    for i in range(1, j + 2):
        den *= (r + b + i)
    return F(num, den)


# ------------------------------------------------------------------------ main
def main():
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    RMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    BMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    L = Ladder()
    fails = []

    print("=" * 74)
    print("PART A -- the ladder is self-starting; base cases come out right")
    print("=" * 74)
    for b in range(0, 4):
        p0 = L.Phi(0, 0, b)
        assert p0 == (F(1, b + 1),), p0
        for p in range(1, 6):
            assert iszero(L.Phi(p, 0, b)), (p, b, L.Phi(p, 0, b))
        assert L.Psi(0, 0, b) == trim([F(1, b + 2), F(-1, b + 2)]), L.Psi(0, 0, b)
        assert L.Psi(1, 0, b) == (F(1, b + 2),), L.Psi(1, 0, b)
        for p in range(2, 6):
            assert iszero(L.Psi(p, 0, b)), (p, b)
    print("  Phi^[0]_0 = 1/(b+1); Phi^[p>=1]_0 = 0;")
    print("  Psi^[0]_0 = (1-s)/(b+2); Psi^[1]_0 = 1/(b+2); Psi^[p>=2]_0 = 0.  b=0..3   OK")
    print("  (nothing hard-coded: g_0 = 1/(b+1) EMERGES from the ODE)")

    print()
    print("=" * 74)
    print("PART B -- my ladder vs the already-PROVED c_k, d_k, e_k (ground truth)")
    print("=" * 74)
    from math import comb
    n_ck = n_dk = n_ek = 0
    for r in range(0, 13):
        for b in range(0, 5):
            F0, G0, H0 = L.Phi(0, r, b), L.Phi(1, r, b), L.Phi(2, r, b)
            for k in range(0, r + 3):
                # c_k^{(r)}(b) = r!/(r-k)! / prod_{i=1}^{k+1}(r+b+i)   [k6 Sec.2.3]
                want = A(r, k, b) if k <= r else F(0)
                got = F0[k] if k < len(F0) else F(0)
                n_ck += 1
                if got != want:
                    fails.append(("c_k", r, b, k, got, want))
                # d_k^{(r)}(b) = C(k+2,2) r!/(r-k-1)! / prod_{i=1}^{k+2}(r+b+i)
                if k <= r - 1:
                    num = 1
                    for i in range(r - k - 1 + 1, r + 1):
                        num *= i
                    den = 1
                    for i in range(1, k + 3):
                        den *= (r + b + i)
                    want = F(comb(k + 2, 2) * num, den)
                else:
                    want = F(0)
                got = G0[k] if k < len(G0) else F(0)
                n_dk += 1
                if got != want:
                    fails.append(("d_k", r, b, k, got, want))
                # e_k^{(r)}(b) = (3k+8)(k+1)(k+2)(k+3)/24 * r!/(r-k-2)! / prod_{i=1}^{k+3}
                if k <= r - 2:
                    num = 1
                    for i in range(r - k - 2 + 1, r + 1):
                        num *= i
                    den = 1
                    for i in range(1, k + 4):
                        den *= (r + b + i)
                    want = F((3 * k + 8) * (k + 1) * (k + 2) * (k + 3) * num, 24 * den)
                else:
                    want = F(0)
                got = H0[k] if k < len(H0) else F(0)
                n_ek += 1
                if got != want:
                    fails.append(("e_k", r, b, k, got, want))
    print(f"  c_k^(r)(b) [k6 Sec.2.3, PROVED] : {n_ck} checks")
    print(f"  d_k^(r)(b) [k6 Sec.3.3, PROVED] : {n_dk} checks")
    print(f"  e_k^(r)(b) [ecg Thm 1,  PROVED] : {n_ek} checks")
    print(f"  mismatches: {len([f for f in fails])}")

    print()
    print("=" * 74)
    print("PART C -- the MANDATED fourth rung (I_r, M_r) at p=3, and M_2(0,0)")
    print("=" * 74)
    # I_r(t,b) = sum_k C(k+4,2)C(k+4,4) r!/(r-k-3)! t^k / prod_{i=1}^{k+4}(r+b+i)
    nI = nM = 0
    for r in range(0, 22):
        for b in range(0, 7):
            I = L.Phi(3, r, b)
            for k in range(0, r + 3):
                if k <= r - 3:
                    num = 1
                    for i in range(r - k - 3 + 1, r + 1):
                        num *= i
                    den = 1
                    for i in range(1, k + 5):
                        den *= (r + b + i)
                    want = F(comb(k + 4, 2) * comb(k + 4, 4) * num, den)
                else:
                    want = F(0)
                got = I[k] if k < len(I) else F(0)
                nI += 1
                if got != want:
                    fails.append(("I_r", r, b, k, got, want))
            # M_r(s,b) = sum_k C(k+4,2)C(k+4,4) r!/(r-k-2)! (1-s)^k / prod_{i=1}^{k+3}(r+b+1+i)
            M = preflect(L.Psi(3, r, b))     # coeffs in u = 1-s
            for k in range(0, r + 3):
                if k <= r - 2:
                    num = 1
                    for i in range(r - k - 2 + 1, r + 1):
                        num *= i
                    den = 1
                    for i in range(1, k + 4):
                        den *= (r + b + 1 + i)
                    want = F(comb(k + 4, 2) * comb(k + 4, 4) * num, den)
                else:
                    want = F(0)
                got = M[k] if k < len(M) else F(0)
                nM += 1
                if got != want:
                    fails.append(("M_r", r, b, k, got, want))
    print(f"  I_r closed form vs my ODE ladder : {nI} checks")
    print(f"  M_r closed form vs my ODE ladder : {nM} checks")
    print(f"  cumulative mismatches: {len(fails)}")
    print(f"  I_0 = {L.Phi(3,0,0)}  I_1 = {L.Phi(3,1,0)}  I_2 = {L.Phi(3,2,0)}")
    print(f"  I_3(t,0) = {L.Phi(3,3,0)}   (target says 3/70)")
    print(f"  I_4(t,0) = {L.Phi(3,4,0)}   (target says 3/35 + 5/63 t)")
    print(f"  I_5(t,0) = {L.Phi(3,5,0)}   (target says 5/42 + 25/126 t + 25/308 t^2)")
    m200 = peval(L.Psi(3, 2, 0), F(0))
    print(f"  ** M_2(0,0) = {m200}   (must be 1/10, the 1/n^3 coeff of PROVED psi_n^(3),R)")
    if m200 != F(1, 10):
        fails.append(("M_2(0,0)", m200))
    for pp, want, nm in [(0, F(11, 30), "Hhat_2(0,0)"), (1, F(13, 20), "K_2(0,0)"),
                         (2, F(23, 60), "L_2(0,0)")]:
        got = peval(L.Psi(pp, 2, 0), F(0))
        print(f"     {nm} = {got}  (must be {want})")
        if got != want:
            fails.append((nm, got, want))

    print()
    print("=" * 74)
    print("PART D -- THEOREM M at all orders p<=%d (incl. p=4,5,6 beyond prior work)" % PMAX)
    print("=" * 74)
    nM2 = 0
    per_p = {}
    for p in range(0, PMAX + 1):
        cnt = 0
        for r in range(0, RMAX + 1):
            for b in range(0, BMAX + 1):
                Ph = L.Phi(p, r, b)
                for k in range(0, r + 3):
                    if 0 <= k <= r - p:
                        want = F(c1(k + p + 1, k + 1)) * A(r, k + p, b)
                    else:
                        want = F(0)
                    got = Ph[k] if k < len(Ph) else F(0)
                    nM2 += 1
                    cnt += 1
                    if got != want:
                        fails.append(("ThmM", p, r, b, k, got, want))
                # degree and vanishing
                if p > r:
                    if not iszero(Ph):
                        fails.append(("Phi!=0 for p>r", p, r, b))
                else:
                    deg = len(trim(Ph)) - 1
                    if not iszero(Ph) and deg != r - p:
                        fails.append(("deg", p, r, b, deg, r - p))
        per_p[p] = cnt
    print(f"  Theorem M vs my independent ODE ladder: {nM2} exact (p,r,b,k) checks")
    print(f"    per order p: " + ", ".join(f"p={p}:{c}" for p, c in per_p.items()))
    print(f"  cumulative mismatches: {len(fails)}")

    print()
    print("=" * 74)
    print("PART E -- the h-side: Psi^[p]_r = sum_k c(k+p+1,k+1) A_{k+p-1}^(r)(b+1)(1-s)^k")
    print("           and the claimed ASYMMETRIC termination at p = r+1")
    print("=" * 74)
    nH = 0
    term_ok = True
    for p in range(0, PMAX + 2):
        for r in range(0, 11):
            for b in range(0, 4):
                Ps = preflect(L.Psi(p, r, b))     # coeffs in u = 1-s
                for k in range(0, r + 4):
                    kk = k + p - 1
                    if 0 <= kk <= r and (p >= 1 or k >= 1):
                        want = F(c1(k + p + 1, k + 1)) * A(r, kk, b + 1)
                    else:
                        want = F(0)
                    got = Ps[k] if k < len(Ps) else F(0)
                    nH += 1
                    if got != want:
                        fails.append(("h-side", p, r, b, k, got, want))
                if p > r + 1 and not iszero(Ps):
                    term_ok = False
                    fails.append(("Psi!=0 for p>r+1", p, r, b))
                if p == r + 1 and iszero(Ps):
                    term_ok = False
                    fails.append(("Psi==0 AT p=r+1 (asymmetry would be FALSE)", p, r, b))
    print(f"  h-side closed form: {nH} exact checks")
    print(f"  termination asymmetry (Psi nonzero AT p=r+1, zero for p>r+1): "
          f"{'CONFIRMED' if term_ok else 'VIOLATED'}")
    for r in range(0, 5):
        print(f"    r={r}: Psi^[{r+1}]_{r}(s,0) = {L.Psi(r+1, r, 0)}"
              f"   Psi^[{r+2}]_{r}(s,0) = {L.Psi(r+2, r, 0)}")
    print(f"  cumulative mismatches: {len(fails)}")

    print()
    print("=" * 74)
    print("PART F -- Corollary A3: D*^(p)_r(b) = Phi^[p]_r(1,b)")
    print("=" * 74)
    import sympy as sp
    ok = 0
    bad = 0
    for r in range(0, 61):
        phir = sp.Rational(4 ** r * sp.factorial(r) ** 2, sp.factorial(2 * r + 1))
        d0 = peval(L.Phi(0, r, 0), F(1))
        d1 = peval(L.Phi(1, r, 0), F(1))
        d2 = peval(L.Phi(2, r, 0), F(1))
        w0 = sp.Rational(d0.numerator, d0.denominator)
        w1 = sp.Rational(d1.numerator, d1.denominator)
        w2 = sp.Rational(d2.numerator, d2.denominator)
        for got, want in [(w0, phir), (w1, sp.Rational(r, 4) * phir),
                          (w2, sp.Rational(r * (3 * r + 1), 32) * phir - sp.Rational(r, 12))]:
            if sp.simplify(got - want) == 0:
                ok += 1
            else:
                bad += 1
                fails.append(("D*", r, got, want))
    print(f"  D*^(0)=phi_r, D*^(1)=r phi_r/4, D*^(2)=r(3r+1)/32 phi_r - r/12, r=0..60")
    print(f"    {ok} exact agreements, {bad} failures")
    # via the Stirling form as well
    bad2 = 0
    for p in range(0, 6):
        for r in range(0, 25):
            for b in range(0, 4):
                lhs = peval(L.Phi(p, r, b), F(1))
                rhs = sum(A(r, j, b) * F(c1(j + 1, j + 1 - p)) for j in range(p, r + 1))
                if lhs != rhs:
                    bad2 += 1
                    fails.append(("D*Stirling", p, r, b))
    print(f"  D*^(p)_r(b) = sum_{{j=p}}^r c_j^(r)(b) c(j+1,j+1-p): p<=5, r<=24, b<=3 -> {bad2} failures")

    print()
    print("=" * 74)
    print(f"LADDER VERDICT: {len(fails)} total mismatches")
    if fails:
        for f in fails[:20]:
            print("  ", f)
    print("=" * 74)
    return len(fails)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
