# Hostile-referee check 2 (extension front): the H_k(r,b) machine, via a THIRD route
# (neither the front's recursion-evaluation+interpolation nor the closure attempt's
# sympy.cancel), plus computational confirmation of this referee's degree-bound PROOF
#   deg_r H_{2k-1}(r,b) = k-1   (leading coefficient 4^{k-1}(k-1)!, independent of b).
#
# Accepted inputs (cited, PROVED upstream):
#   S_{2k-1}(N,m) := sum_{i=0}^m (N-2i)^{2k-1} C(N,i)
#   H_{2k-1}(r,b) := P_b * S_{2k-1}(N,r),   N = 2r+b+1,  P_b = r!(r+b)!/N!
#   the wave-14/15 recursion:
#     S_{2k-1}(N,m) = (N-2m)^{2k-2}(m+1)C(N,m+1)
#                     + 2N sum_{s odd,1<=s<=2k-3} C(2k-2,s) S_s(N-1,m-1),
#     base S_1(N,m) = (m+1) C(N,m+1),  convention S_s(.,-1) = 0.
#   (E2) with j=0: P_b * C(N, r+1) = 1/(r+1).
#
# NEW polynomial factorization (this referee, proof in REFEREE_REPORT.md section 2):
#   define A_1(N,m) := m+1,
#          A_k(N,m) := (m+1) * [ (N-2m)^{2k-2}
#                                + 2 sum_{s odd,1<=s<=2k-3} C(2k-2,s) A_{(s+1)/2}(N-1,m-1) ]
#   Then S_{2k-1}(N,m) = A_k(N,m) * C(N,m+1) for every integer m >= 0 (induction on k,
#   using C(N,m+1) = C(N-1,m) * N/(m+1)), and hence
#   H_{2k-1}(r,b) = A_k(2r+b+1, r) / (r+1) = B_k(2r+b+1, r),
#   where A_k = (m+1) B_k -- a polynomial in (r,b) with integer coefficients.
#   Substituting N = 2r+b+1 makes (N - 2m - shift-corrections) constant in r at every
#   recursion level, giving deg_r A_k = k, deg_r B_k = k-1, lead 4^{k-1}(k-1)!.
#
# Exact arithmetic only. No randomness.

from fractions import Fraction
from math import comb, factorial
import time
import sympy as sp

Nsym, msym, rsym, bsym = sp.symbols("N m r b")

KMAX = 20  # k up to 20 (power 39) -- everything p=20 needs


def build_A_polys(kmax=KMAX):
    """A_k(N,m) polynomials, k=1..kmax, via the recursion above (sympy exact)."""
    A = {1: sp.Poly(msym + 1, Nsym, msym)}
    for k in range(2, kmax + 1):
        acc = (Nsym - 2 * msym) ** (2 * k - 2)
        for s in range(1, 2 * k - 2, 2):
            j = (s + 1) // 2
            Ashift = A[j].as_expr().subs({Nsym: Nsym - 1, msym: msym - 1})
            acc += 2 * comb(2 * k - 2, s) * Ashift
        A[k] = sp.Poly(sp.expand((msym + 1) * acc), Nsym, msym)
    return A


def S_brute(power, N, m):
    """Brute-force direct summation (no recursion)."""
    return sum((N - 2 * i) ** power * comb(N, i) for i in range(0, m + 1))


def H_brute(k, r, b):
    """P_b * S_{2k-1}(N, r), direct."""
    N = 2 * r + b + 1
    Pb = Fraction(factorial(r) * factorial(r + b), factorial(N))
    return Pb * S_brute(2 * k - 1, N, r)


def main():
    t0 = time.time()
    A = build_A_polys(KMAX)
    print(f"--- built A_k(N,m) polynomials, k=1..{KMAX}, in {time.time()-t0:.2f}s ---")

    # 0) sanity: the two smallest closed forms
    B1 = sp.cancel(A[1].as_expr() / (msym + 1))
    B2 = sp.cancel(A[2].as_expr() / (msym + 1))
    print("B_1(N,m) =", sp.expand(B1), "   (expect 1, i.e. H_1 = 1)")
    H3 = sp.expand(B2.subs({Nsym: 2 * rsym + bsym + 1, msym: rsym}))
    print("H_3(r,b) =", H3, "   (expect (b+1)^2 + 4r, closure attempt's k=2 bracket * -8)")
    assert sp.expand(H3 - ((bsym + 1) ** 2 + 4 * rsym)) == 0

    # 1) identity check vs brute force: H_{2k-1}(r,b) == A_k(N,r)/(r+1), k=1..20
    checks = fails = 0
    rs = list(range(0, 13)) + [16, 20, 30, 50]
    bs = [0, 1, 2, 3, 5, 8, 13, 30]
    t0 = time.time()
    for k in range(1, KMAX + 1):
        Aexpr = A[k]
        for r in rs:
            for b in bs:
                N = 2 * r + b + 1
                val = Fraction(int(Aexpr.eval((N, r))), r + 1)
                want = H_brute(k, r, b)
                checks += 1
                if val != want:
                    fails += 1
                    print(f"MISMATCH k={k} r={r} b={b}: A-route={val} brute={want}")
    print(f"A_k-route vs brute-force P_b*S_(2k-1)(N,r): k=1..{KMAX}, "
          f"r in {rs}, b in {bs}: {checks} checks, fails={fails} "
          f"({time.time()-t0:.1f}s)")
    assert fails == 0

    # 2) divisibility + degree + leading coefficient, b SYMBOLIC (generic b)
    print("--- degree/leading-coefficient check, b symbolic ---")
    for k in range(1, KMAX + 1):
        Hk = sp.expand(A[k].as_expr().subs({Nsym: 2 * rsym + bsym + 1, msym: rsym}))
        q, rem = sp.div(sp.Poly(Hk, rsym), sp.Poly(rsym + 1, rsym))
        assert rem.is_zero, f"A_k(2r+b+1,r) not divisible by (r+1) at k={k}"
        Hpoly = sp.Poly(q.as_expr(), rsym)  # coefficients in b
        deg = Hpoly.degree()
        lead = sp.expand(Hpoly.LC())
        assert deg == k - 1, (k, deg)
        expected_lead = 4 ** (k - 1) * factorial(k - 1)
        assert sp.simplify(lead - expected_lead) == 0, (k, lead)
    print(f"for every k=1..{KMAX}: (r+1) | A_k(2r+b+1, r), deg_r H_(2k-1) = k-1, "
          f"leading coeff = 4^(k-1) (k-1)!  (b symbolic) -- OK")

    # 3) stress test of the front's interpolation self-check logic:
    #    an UNDER-guessed degree (k-2 instead of k-1) interpolant through k-1 nodes
    #    must disagree with the true polynomial at EVERY integer point off the nodes
    #    (difference = lead * prod(r - r_i), zero only ON the nodes). Demonstrate.
    print("--- wrong-degree-guess stress test (under-guess by one) ---")
    for k in [5, 12, 20]:
        b = 3
        Hk = sp.expand(sp.cancel(
            A[k].as_expr().subs({Nsym: 2 * rsym + b + 1, msym: rsym}) / (rsym + 1)))
        offset = 40
        nodes = list(range(offset, offset + k - 1))          # k-1 nodes: degree k-2 fit
        vals = [Fraction(int(sp.Integer(Hk.subs(rsym, x)))) for x in nodes]
        # Newton divided differences for the (wrong, degree k-2) interpolant
        coef = list(vals)
        for j in range(1, len(nodes)):
            for i in range(len(nodes) - 1, j - 1, -1):
                coef[i] = (coef[i] - coef[i - 1]) / (nodes[i] - nodes[i - j])
        def interp(x):
            acc = Fraction(0)
            for c, x0 in zip(reversed(coef), reversed(nodes[:-1])):
                acc = acc * (x - x0)
                acc += c
            return acc
        n_caught = 0
        held_out = list(range(offset + k - 1, offset + k - 1 + 12))
        for x in held_out:
            true = Fraction(int(sp.Integer(Hk.subs(rsym, x))))
            if interp(x) != true:
                n_caught += 1
        print(f"  k={k}, b={b}: degree-(k-2) fit through k-1 nodes: "
              f"{n_caught}/{len(held_out)} held-out points disagree "
              f"(theory says: all of them must)")
        assert n_caught == len(held_out)

    print("ALL REFEREE H_k CHECKS PASSED")
    return A


if __name__ == "__main__":
    main()
