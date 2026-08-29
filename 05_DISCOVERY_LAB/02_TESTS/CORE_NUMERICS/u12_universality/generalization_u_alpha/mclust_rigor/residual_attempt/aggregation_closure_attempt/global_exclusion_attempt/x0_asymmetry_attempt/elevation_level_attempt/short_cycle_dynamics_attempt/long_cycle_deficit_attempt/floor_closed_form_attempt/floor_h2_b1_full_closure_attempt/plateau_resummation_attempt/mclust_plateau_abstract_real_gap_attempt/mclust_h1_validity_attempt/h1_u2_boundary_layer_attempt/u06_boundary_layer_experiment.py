"""
u06_boundary_layer_experiment.py

THE MAIN NEW EXPERIMENT of this front: a direct numerical test of (U2)'s
claim specifically INSIDE the boundary layer x = O(eps) -- i.e. x = eps*u
for FIXED u, as eps -> 0 (c -> infinity) -- which NO ancestor front tested
(every ancestor grid used x FIXED, independent of eps: mclust_h1_validity_
attempt's own grid was x in {0,0.5,1,2,4,6,8}, none of it rescaled with
eps; grep-confirmed against that front's own k04/k05/k07 scripts' prose,
never opened as code here).

For each c in a ladder, and each u in {0,1,2,4} (giving x = eps*u = u/
sqrt(c), i.e. s = x/sqrt(c) = u/c -- genuinely inside the boundary layer,
shrinking FASTER than eps itself as c grows), this script:

  1. Builds the (P,Q)-family (u02_family_series.py, this front's own
     fresh implementation, independently validated against 5 published
     anchors + Phi(0,0.002) + the c=1000 plateau in u03_validate_anchors.py)
     at K=400, dps=250 -- sizing empirically probed (u04, u05) to give
     >=24 stable digits via the SAME two-t0 (c*t0=60 vs 80) convergence
     check this lineage uses throughout, at every c in the ladder
     1000..64000 (this experiment does not need >=100-digit precision
     the way the ancestor asymptotic-law fits did -- only enough digits
     to see an O(eps^5) effect cleanly against the O(eps^4) term, which
     24+ stable digits comfortably provides even at the smallest eps
     tested).

  2. Computes W_inf(x;c) DIRECTLY from the exact KEY identity
     W = Psi - eps*Psi_x, i.e. NUMERICALLY, with NO detour through F and
     the (ODE-F) hypotheses (ii)/(iii) of mclust_h1_validity_attempt
     Section 2.3 -- Psi(s,t0->plateau) and Psi_x(s,t0->plateau) =
     (1/sqrt(c)) Psi_s are both computed directly by summing the b_k(s)
     series and its s-derivative series (via this front's own fam_deriv
     applied to each b_k, an INDEPENDENT computation from the a_k-based
     Phi/F route).

  3. ALSO computes F(x;c) = Phi(s,t0->plateau) (the a_k series) as a
     genuine, independent NUMERICAL CHECK of hypothesis (ii)
     (lim Psi = lim Phi = F) -- no ancestor front verified this
     numerically; it was only assumed/consistency-checked at leading
     order (mclust_h1_validity_attempt Section 2.3's own disclosure,
     "not independently verified numerically beyond a leading-order
     consistency check").

  4. Compares the numerically-computed W_inf(x;c) against this front's
     DERIVED outer-expansion prediction (u01_symbolic_outer_expansion.py, Part 2):

       W_pred(x;eps) = eps*R(x) + eps^2*R'(x) + eps^3*(3/2)*R''(x)
                       + eps^4*(13/6)*R'''(x)

     at x = eps*u -- i.e. this SAME formula, built from x-FIXED entire
     functions, evaluated AT THE SHRINKING boundary-layer point -- and
     tracks the residual ratio (W_inf_numeric - W_pred)/eps^5 as eps -> 0
     at FIXED u. If this ratio stays BOUNDED (ideally converges) as
     eps -> 0, that is direct numerical evidence that the SAME outer
     coefficients remain valid all the way into the boundary layer (no
     distinct "inner" correction is numerically detectable at this
     order) -- exactly the content (U2) claims. If it diverges/blows up,
     that is direct numerical evidence AGAINST (U2)'s uniform validity
     at this specific scale.

  5. A bridge/consistency point at FIXED x=1 (s=1/sqrt(c), NOT rescaled
     with eps) is included for continuity with mclust_h1_validity_
     attempt's own (different, x-fixed) uniformity grid.
"""
from mpmath import mp, mpf, sqrt, pi, erfc, exp
from u02_family_series import build_family, fam_eval, fam_deriv, erfcx

K = 400
DPS = 250
C_LADDER = [1000, 4000, 16000, 64000]
U_LIST = [0, 1, 2, 4]  # boundary-layer: x = eps*u, s = u/c


def series_sum(fam_list, s, Eval, t0, K_use):
    total = mpf(0)
    t0p = mpf(1)
    for k in range(K_use + 1):
        total += fam_eval(fam_list[k], s, Eval) * t0p
        t0p *= t0
    return total


def R_and_derivs(x):
    """R(x)=sqrt(pi/2) erfcx(x/sqrt2), via mpmath erfc directly (x stays
    small/modest throughout this front's grid -- no large-argument branch
    needed); R',R'',R''' via the record's own closure identity
    R^{(n+1)}=x R^{(n)} + n R^{(n-1)} (cited, not re-derived here -- see
    u01_symbolic_outer_expansion.py for the from-scratch symbolic verification of
    this identity, n=0..5)."""
    z = x / sqrt(2)
    R0 = sqrt(pi / 2) * erfcx(z)
    R1 = x * R0 - 1
    R2 = x * R1 + 1 * R0
    R3 = x * R2 + 2 * R1
    return R0, R1, R2, R3


results = []

for c in C_LADDER:
    c_val = mpf(c)
    mp.dps = DPS
    a, b, cv, sc = build_family(c_val, K, dps=DPS)
    eps = 1 / sqrt(c_val)
    t0_lo = mpf(60) / c_val
    t0_hi = mpf(80) / c_val

    points = [("bridge x=1", mpf(1) / sqrt(c_val))]
    for u in U_LIST:
        points.append((f"u={u}", mpf(u) / c_val))  # s = x/sqrt(c) = (eps*u)/sqrt(c) = u/c

    for label, s in points:
        mp.dps = DPS
        x_val = s * sqrt(c_val)
        Eval = erfcx(s * sqrt(c_val / 2))

        # Phi (F) plateau, two-t0 check
        F_lo = series_sum(a, s, Eval, t0_lo, K)
        F_hi = series_sum(a, s, Eval, t0_hi, K)
        F_reldiff = abs(F_lo - F_hi) / abs(F_hi) if F_hi != 0 else abs(F_lo - F_hi)

        # Psi plateau, two-t0 check (independent series, b_k not a_k)
        Psi_lo = series_sum(b, s, Eval, t0_lo, K)
        Psi_hi = series_sum(b, s, Eval, t0_hi, K)
        Psi_reldiff = abs(Psi_lo - Psi_hi) / abs(Psi_hi) if Psi_hi != 0 else abs(Psi_lo - Psi_hi)

        # Psi_x = (1/sqrt(c)) * d/ds[Psi] -- via fam_deriv on every b_k
        bprime = [fam_deriv(bk, c_val, sc) for bk in b]
        Psix_lo = series_sum(bprime, s, Eval, t0_lo, K) / sqrt(c_val)
        Psix_hi = series_sum(bprime, s, Eval, t0_hi, K) / sqrt(c_val)
        Psix_reldiff = (abs(Psix_lo - Psix_hi) / abs(Psix_hi)
                         if Psix_hi != 0 else abs(Psix_lo - Psix_hi))

        # W_inf = Psi - eps * Psi_x   (KEY, exact, no hypothesis ii/iii needed)
        W_inf = Psi_hi - eps * Psix_hi

        # hypothesis (ii) check: does Psi's plateau equal Phi's plateau?
        hyp_ii_reldiff = abs(Psi_hi - F_hi) / abs(F_hi) if F_hi != 0 else abs(Psi_hi - F_hi)

        # predicted outer expansion (this front's derived chi_n), evaluated
        # AT THE SAME x (possibly deep inside the boundary layer)
        R0, R1, R2, R3 = R_and_derivs(x_val)
        W_pred4 = eps * R0 + eps**2 * R1 + eps**3 * (mpf(3) / 2) * R2 + eps**4 * (mpf(13) / 6) * R3

        resid5 = (W_inf - W_pred4) / eps**5

        results.append(dict(
            c=c, label=label, x=x_val, s=s, eps=eps,
            F_reldiff=F_reldiff, Psi_reldiff=Psi_reldiff, Psix_reldiff=Psix_reldiff,
            hyp_ii_reldiff=hyp_ii_reldiff,
            W_inf=W_inf, W_pred4=W_pred4, resid5=resid5,
        ))

        print(f"c={c:6d} {label:10s} x={float(x_val):.6e} eps={float(eps):.6e}  "
              f"F_reldiff={float(F_reldiff):.3e} Psi_reldiff={float(Psi_reldiff):.3e} "
              f"Psix_reldiff={float(Psix_reldiff):.3e}  hyp_ii_reldiff={float(hyp_ii_reldiff):.3e}")
        print(f"    W_inf={W_inf}")
        print(f"    W_pred4={W_pred4}")
        print(f"    resid5=(W_inf-W_pred4)/eps^5={resid5}")

import pickle
with open("u06_results.pkl", "wb") as f:
    pickle.dump([{k: str(v) for k, v in r.items()} for r in results], f)

print("\nDone. Results pickled to u06_results.pkl (string-serialized mpf).")
