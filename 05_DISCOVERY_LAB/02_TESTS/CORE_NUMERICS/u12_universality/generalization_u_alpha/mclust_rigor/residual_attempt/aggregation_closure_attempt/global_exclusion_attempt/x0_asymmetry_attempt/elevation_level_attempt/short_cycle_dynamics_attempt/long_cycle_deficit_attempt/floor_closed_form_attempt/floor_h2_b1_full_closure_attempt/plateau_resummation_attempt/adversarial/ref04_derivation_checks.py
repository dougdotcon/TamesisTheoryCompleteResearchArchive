"""
Referee (adversarial) checks of ATTEMPT.md Sec 4's matched-asymptotics
derivation, done ENTIRELY from this referee's own hand re-derivation
(see docstring of ref01_fresh_family.py and REFEREE_REPORT.md for the
by-hand algebra) plus this referee's own fresh (P,Q)-family series
(ref01_fresh_family.py) -- no script of the front under review was read.

Part A: numerically verify the TWO EXACT reformulations (E1),(KEY) of
Sec 4.1 hold as identities of the ORIGINAL (unscaled) PDE system, using
this referee's own freshly-built (P,Q) series for Phi(s,g), Psi(s,g),
evaluated (via direct series summation, not the closed (P,Q) form) at a
generic (s,g) point away from s=0 and g=0. This is an independent,
numerical cross-check of the by-hand algebraic derivation of (E1)/(KEY)
given in REFEREE_REPORT.md Sec 4 (that derivation, on its own, is already
fully rigorous -- straightforward substitution/rearrangement of the given
PDE -- this is an added empirical safety net).

Part B: verify (numerically, via finite differences, at several x) that
  R(x)  := sqrt(pi/2)*erfcx(x/sqrt2)   solves   R'  = x*R  - 1,  R(inf)=0
  psi2(x) := 2*x*R(x) - 2              solves   psi2' = x*psi2 + 2*R
exactly as claimed in ATTEMPT.md Sec 4.2/4.3 (this referee's own
independent by-hand symbolic verification of both identities is exact and
reproduced in REFEREE_REPORT.md; this is the numerical cross-check).

Part C: verify the Watson/kernel expansion step of Sec 4.2,
  Phi(x,y) = W(x,y) + eps*(W_x - W_y)(x,y) + O(eps^2)   for y >> eps,
by direct Taylor expansion of the exact renewal kernel in (E2) -- shown
analytically in REFEREE_REPORT.md; here only the elementary consistency
of e^{-y/eps} -> 0 and the moment integrals of the exponential kernel
(int_0^inf e^{-u} du = 1, int_0^inf u e^{-u} du = 1) used in that
expansion are confirmed by direct mpmath quadrature, as an extra
sanity check requiring no further symbolic content.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from ref01_fresh_family import build_family, comb_eval, erfcx, comb_deriv

mp.mp.dps = 50


def part_A(c, s0, g0, K):
    print(f"--- Part A: exact reformulations (E1)/(KEY), c={c}, s0={s0}, g0={g0}, K={K} ---")
    c = mp.mpf(c)
    sc = mp.sqrt(2 * c / mp.pi)
    eps = 1 / mp.sqrt(c)
    a, b = build_family(c, K)
    s0 = mp.mpf(s0); g0 = mp.mpf(g0)

    def seriesA(coeffs, gval, deriv_order=0):
        # coeffs: list of (P,Q) pairs indexed by k -> value at s0 (or ds/ds^deriv_order)
        vals = []
        for k in range(len(coeffs)):
            elt = coeffs[k]
            for _ in range(deriv_order):
                elt = comb_deriv(elt, c, sc)
            vals.append(comb_eval(elt, s0, c))
        r = mp.mpf(0)
        for v in reversed(vals):
            r = r * gval + v
        return r

    Phi = seriesA(a, g0)
    Psi = seriesA(b, g0)
    dPsi_ds = seriesA(b, g0, deriv_order=1)
    x0 = s0 * mp.sqrt(c)
    y0 = g0 * mp.sqrt(c)
    Psi_x = eps * dPsi_ds  # chain rule: d/dx = eps * d/ds

    # I(s0,g0) = int_0^g0 Phi(s0,g') dg' = sum_k a_k(s0) g0^{k+1}/(k+1)
    a0vals = [comb_eval(a[k], s0, c) for k in range(K + 1)]
    Ival = mp.mpf(0)
    for k in reversed(range(K + 1)):
        Ival = Ival * g0 + a0vals[k] * g0 / (k + 2) if False else Ival
    # direct sum (clear, not Horner-tricky) for I:
    Ival = mp.mpf(0)
    gp = g0
    for k in range(K + 1):
        Ival += a0vals[k] * (gp / (k + 1))
        gp *= g0

    # (E1) is stated in SCALED variables: Psi_x =? (x+y)*Psi - I_scaled(x,y),
    # where I_scaled(x,y) := int_0^y Phi(x,y') dy' is an integral over the
    # SCALED y' variable. Ival above was computed as int_0^g0 Phi(s0,g')dg'
    # -- an integral over the UNSCALED g' variable -- and by the same
    # substitution g'=eps*y' used throughout Sec 4.1, int_0^g Phi dg' =
    # eps * I_scaled(x,y). So I_scaled = Ival / eps.
    I_scaled = Ival / eps
    lhs1 = Psi_x
    rhs1 = (x0 + y0) * Psi - I_scaled
    print("  (E1) LHS (eps*dPsi/ds) =", mp.nstr(lhs1, 25))
    print("  (E1) RHS ((x+y)Psi - I_scaled) =", mp.nstr(rhs1, 25))
    print("  (E1) |LHS-RHS| =", mp.nstr(abs(lhs1 - rhs1), 6))

    # W = I + (1 - s0 - g0)*Psi   [since g*Avg_g[Phi] = I exactly]
    W = Ival + (1 - s0 - g0) * Psi
    # KEY: W =? Psi - eps*Psi_x
    rhsKEY = Psi - eps * Psi_x
    print("  (KEY) W (from def)      =", mp.nstr(W, 25))
    print("  (KEY) Psi - eps*Psi_x   =", mp.nstr(rhsKEY, 25))
    print("  (KEY) |W - (Psi-eps Psi_x)| =", mp.nstr(abs(W - rhsKEY), 6))
    return abs(lhs1 - rhs1), abs(W - rhsKEY)


def R(x):
    return mp.sqrt(mp.pi / 2) * erfcx(x / mp.sqrt(2))


def psi2(x):
    return 2 * x * R(x) - 2


def part_B():
    print("--- Part B: R'(x)=xR(x)-1 and psi2'(x)=x*psi2(x)+2R(x) ---")
    h = mp.mpf('1e-20')
    worstR = mp.mpf(0); worstP = mp.mpf(0)
    for xs in ['0', '0.3', '1.0', '2.5', '4.0']:
        x = mp.mpf(xs)
        Rp_num = (R(x + h) - R(x - h)) / (2 * h)
        Rp_pred = x * R(x) - 1
        p2p_num = (psi2(x + h) - psi2(x - h)) / (2 * h)
        p2p_pred = x * psi2(x) + 2 * R(x)
        worstR = max(worstR, abs(Rp_num - Rp_pred))
        worstP = max(worstP, abs(p2p_num - p2p_pred))
        print(f"  x={xs}: |R'_num-R'_pred|={mp.nstr(abs(Rp_num-Rp_pred),4)}  "
              f"|psi2'_num-psi2'_pred|={mp.nstr(abs(p2p_num-p2p_pred),4)}")
    print("  R(0) =", mp.nstr(R(0), 20), " vs sqrt(pi/2) =", mp.nstr(mp.sqrt(mp.pi / 2), 20))
    print("  psi2(0) =", psi2(0), " vs claimed -2")
    return worstR, worstP


def part_C():
    print("--- Part C: exponential-kernel moments used in the Watson expansion ---")
    m0 = mp.quad(lambda u: mp.e**(-u), [0, mp.inf])
    m1 = mp.quad(lambda u: u * mp.e**(-u), [0, mp.inf])
    print("  int_0^inf e^-u du =", mp.nstr(m0, 20), " (expect 1)")
    print("  int_0^inf u e^-u du =", mp.nstr(m1, 20), " (expect 1)")
    return abs(m0 - 1), abs(m1 - 1)


if __name__ == "__main__":
    e1, ekey = part_A(1000, '0.02', '0.05', 220)
    print()
    wr, wp = part_B()
    print()
    c0, c1 = part_C()
    print()
    print("=== SUMMARY ===")
    print("max (E1) residual:", mp.nstr(e1, 6))
    print("max (KEY) residual:", mp.nstr(ekey, 6))
    print("max R-ODE residual (finite-diff limited):", mp.nstr(wr, 6))
    print("max psi2-ODE residual (finite-diff limited):", mp.nstr(wp, 6))
    print("kernel moment residuals:", mp.nstr(c0, 6), mp.nstr(c1, 6))
