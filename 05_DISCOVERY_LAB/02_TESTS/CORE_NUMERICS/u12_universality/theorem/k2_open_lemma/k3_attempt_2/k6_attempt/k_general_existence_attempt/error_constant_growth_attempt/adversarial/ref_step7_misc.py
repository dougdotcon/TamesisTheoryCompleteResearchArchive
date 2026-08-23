"""STEP 7 -- residual audit points raised while reading the target's prose."""

from fractions import Fraction as Fr
from math import comb
from ref_core import Ladder, Chain, peval, phi

print("=" * 78)
print("STEP 7  residual audit points")
print("=" * 78)

lad = Ladder(42, 4)

print()
print("(7a) Sec 5.1's displayed combination '4A_3 - A_1 = -2r(2r+1)C(2r,r)',")
print("     read with A_p := sum_{i<=r}(N-2i)^p C(N,i) as the two lines above define:")
for r in (2, 3, 5, 10):
    N = 2 * r + 1
    A1 = sum((N - 2 * i) * comb(N, i) for i in range(0, r + 1))
    A3 = sum((N - 2 * i) ** 3 * comb(N, i) for i in range(0, r + 1))
    print("      r=%2d  4A_3-A_1 = %-14d   -2r(2r+1)C(2r,r) = %-14d   equal=%s"
          % (r, 4 * A3 - A1, -2 * r * (2 * r + 1) * comb(2 * r, r),
             4 * A3 - A1 == -2 * r * (2 * r + 1) * comb(2 * r, r)))
print("     read with A_p := sum_{i<=r} v^p C(N,i)  (v = i - N/2), it IS correct:")
for r in (2, 3, 5, 10):
    N = 2 * r + 1
    a1 = sum((Fr(i) - Fr(N, 2)) * comb(N, i) for i in range(0, r + 1))
    a3 = sum((Fr(i) - Fr(N, 2)) ** 3 * comb(N, i) for i in range(0, r + 1))
    print("      r=%2d  4a_3-a_1 = %-14s   equal=%s"
          % (r, 4 * a3 - a1, 4 * a3 - a1 == -2 * r * (2 * r + 1) * comb(2 * r, r)))

print()
print("(7b) Sec 5.2's stated Stirling mechanism: 'the factor 2^{b+1} in 2^N exactly")
print("     cancels the 2^{-(b+1)} in the prefactor r!(r+b)!/(2r+b+1)!'.")
print("     The prefactor contains NO power of 2.  The real cancellation is")
print("       rho_b(r) := 2^b [(r+b)!/r!] [(2r+1)!/(2r+b+1)!] = prod_j (2r+2j)/(2r+j+1) -> 1")
for b in (1, 2, 3, 5):
    for r in (10, 1000, 100000):
        rho = Fr(1)
        for j in range(1, b + 1):
            rho *= Fr(2 * r + 2 * j, 2 * r + j + 1)
        print("        b=%d r=%-7d rho_b(r)=%.10f   1+b(b-1)/(4r)=%.10f"
              % (b, r, float(rho), 1 + b * (b - 1) / (4 * r)))

print()
print("(7c) Corollary 1a says H_r(.,b) is 'strictly increasing on [0,1]'.")
for r in (0, 1, 2, 3):
    print("      H_%d(t,0) = %s   -> %s"
          % (r, [str(c) for c in lad.H[(r, 0)]],
             "CONSTANT (not strictly increasing)" if len(lad.H[(r, 0)]) <= 1
             else "strictly increasing"))
print("     max_{[0,1]}|H_r| = H_r(1,b) still holds in every case (coefficients >= 0).")

print()
print("(7d) executive-summary item 4 says F_r(2,b)/F_r(1,b) = Theta((9/8)^r) for general b;")
print("     Sec 6.2 derives it only at b=0.  Measured:")
for b in (0, 1, 2, 3):
    row = "      b=%d :" % b
    for r in (20, 30, 40):
        v = peval(lad.F[(r, b)], 2) / peval(lad.F[(r, b)], 1)
        v1 = peval(lad.F[(r - 1, b)], 2) / peval(lad.F[(r - 1, b)], 1)
        row += "  r=%d ratio=%.6f" % (r, float(v / v1))
    print(row + "   (9/8 = 1.125)")

print()
print("(7e) the sixth cross-check, straight from MY simulator: h_2(0,0) vs")
print("     11/30 + 13/(20n) + 23/(60n^2) + 1/(10n^3)")
for n in (5, 6, 8, 11, 17):
    ch = Chain(n, 2, 1)
    want = Fr(11, 30) + Fr(13, 20 * n) + Fr(23, 60 * n ** 2) + Fr(1, 10 * n ** 3)
    print("      n=%2d  h_2(0,0)=%-18s want=%-18s match=%s"
          % (n, ch.h[(2, 0, 0)], want, ch.h[(2, 0, 0)] == want))

print()
print("(7f) Sec 4 item 2 lists only F_r,G_r,Hhat_r,K_r as the polynomials of bounded")
print("     degree; the 3-term argument also needs H_r and L_r.  Degrees:")
for r in range(0, 7):
    print("      r=%d  deg F=%d deg G=%s deg H=%s deg Hhat=%d deg K=%d deg L=%s"
          % (r, len(lad.F[(r, 0)]) - 1,
             len(lad.G[(r, 0)]) - 1, len(lad.H[(r, 0)]) - 1,
             len(lad.Hh[(r, 0)]) - 1, len(lad.K[(r, 0)]) - 1,
             len(lad.L[(r, 0)]) - 1))

print()
print("(7g) Theorem 2's C^(3) recursion uses coefficient 1 on D^(3)_r(b+1) where the")
print("     predecessor's Sec 6 used 2.  Both are finite, so Theorem 2 stands either")
print("     way; the 1 is justified by the target's own Sec 6.1 ([0,1] not <=2),")
print("     but Sec 4 calls the recursion 'identical', which it is not.")
