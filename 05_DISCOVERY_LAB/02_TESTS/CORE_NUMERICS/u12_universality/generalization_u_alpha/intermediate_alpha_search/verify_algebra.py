"""Symbolic verification of the algebraic claims used in the own-derivation
(FINDINGS.md Sec. 2-3). Not a simulation -- pure algebra/calculus checks via
sympy, run once, output logged to verify_algebra.log.

Checks:
 A) Re-derivation of the master formula H_q(t) from the "bracket" argument,
    for general q(s), matches DERIVATIONS.md's H_q(t) = t - (1-t)*int_0^t
    (1-q(s))/(1-s) ds.
 B) For q(s)=s specifically, bracket(s,t) = q(s) + (1-q(s))*(t-s)/(1-s)
    simplifies to exactly t (identity, independent of s).
 C) Consequence: for q(s)=s and an ARBITRARY (inhomogeneous) event-rate
    density lambda(s) with cumulative Lambda(t) = int_0^t lambda, the
    hazard integral c*H(t) := int_0^t lambda(s)*bracket(s,t) ds equals
    t*Lambda(t) exactly.
 D) M-WEIB(beta): Lambda(t) = c*t^beta => H(t) = c*t^(1+beta); boundary
    checks beta=1 (recovers M-U, H=t^2) and beta->0 (recovers M-SELF/PREV,
    H=t, since Lambda(t)->c constant, an atom at s=0+).
 E) M-CLUST with b/n -> lambda fixed (finite ratio, n->infty): re-derive
    the small-t expansion of H_NEW(t) = t - (1-t)*(t+rho*ln(1-t))/(1-rho)
    (mclust_rigor's mean-field formula, rho constant) and confirm the
    leading order is STILL exactly quadratic in t (beta=1), i.e. this
    axis does NOT produce an intermediate exponent -- only rescales the
    U_{1/2} coefficient.
"""
import sympy as sp

log = open("verify_algebra.log", "w")


def say(msg):
    print(msg)
    log.write(str(msg) + "\n")


s, t, c, beta, a, rho = sp.symbols('s t c beta a rho', positive=True)

say("=== A) master formula re-derivation (general q(s)) ===")
q = sp.Function('q')(s)
bracket = q + (1 - q) * (t - s) / (1 - s)
bracket_expanded = sp.simplify(bracket)
say(f"bracket(s,t) = q(s) + (1-q(s))*(t-s)/(1-s) = {bracket_expanded}")

# integrate symbolically for a GENERIC q by keeping q symbolic; verify the
# algebraic identity termwise instead (matches DERIVATIONS.md eq. derivation
# done by hand in the transcript): expand bracket into  1 - (1-q)*(1-t)/(1-s)
identity_check = sp.simplify(bracket - (1 - (1 - q) * (1 - t) / (1 - s)))
say(f"check bracket == 1-(1-q)(1-t)/(1-s):  residual = {identity_check} (should be 0)")

# So int_0^t bracket ds = t - (1-t) int_0^t (1-q(s))/(1-s) ds = H_q(t).  This
# matches DERIVATIONS.md (1.1) exactly (algebraic identity, not re-derived
# from the Poisson PGFL step here -- that step is inherited unchanged).
say("=> confirms bracket integrates to exactly H_q(t) of DERIVATIONS.md (1.1)\n")

say("=== B) q(s)=s: bracket(s,t) simplifies to exactly t (s-independent) ===")
bracket_qs = bracket.subs(q, s)
bracket_qs_simpl = sp.simplify(bracket_qs)
say(f"bracket(s,t)|_(q=s) = {bracket_qs_simpl}  (should be just 't')")
assert bracket_qs_simpl == t, "IDENTITY FAILED"
say("CONFIRMED: bracket(s,t) = t identically for q(s)=s.\n")

say("=== C) H(t) = t*Lambda(t)/c for q(s)=s and ARBITRARY lambda(s) ===")
lam = sp.Function('lam')(s)
integrand = lam * bracket_qs_simpl  # = lam(s)*t
cH = sp.integrate(integrand, (s, 0, t))
say(f"c*H(t) = int_0^t lambda(s)*t ds = {cH}  (should be t*Lambda(t) with Lambda(t)=int_0^t lambda)")
say("=> confirmed: c*H(t) = t * Lambda(t) exactly, for ANY lambda(s), given q(s)=s.\n")

say("=== D) M-WEIB(beta): Lambda(t) = c*t^beta ===")
Lambda_weib = c * t**beta
H_weib = sp.simplify(t * Lambda_weib / c)
say(f"H_weib(t) = t*Lambda(t)/c = {H_weib} = t^(1+beta)")
say("boundary beta->1: H -> t^2 (recovers M-U exactly). "
    f"Direct substitution: {H_weib.subs(beta, 1)}")
say("boundary beta->0: Lambda(t) -> c (constant, atom at s=0+); "
    f"H -> t^(1) = t. Direct substitution: {H_weib.subs(beta, 0)}"
    "  (recovers M-SELF/M-PREV's H(t)=t exactly)\n")

say("=== D2) tail exponent via Watson's lemma sanity check (numeric, "
    "beta=1/2) ===")
from scipy.integrate import quad
import math


def phi_weib(cval, betav):
    val, _ = quad(lambda tt: math.exp(-cval * tt ** (1 + betav)), 0, 1,
                   epsabs=1e-14, epsrel=1e-13)
    return val


for betav in [0.25, 0.5, 0.75]:
    alpha_pred = 1.0 / (1.0 + betav)
    c_lo, c_hi = 50.0, 4000.0
    f_lo, f_hi = phi_weib(c_lo, betav), phi_weib(c_hi, betav)
    alpha_hat = math.log(f_lo / f_hi) / math.log(c_hi / c_lo)
    say(f"beta={betav}: alpha_predicted=1/(1+beta)={alpha_pred:.6f}  "
        f"quadrature log-log slope (c=50..4000) = {alpha_hat:.6f}")

say("")
say("=== E) M-CLUST with b/n -> rho fixed (n -> infinity): small-t "
    "expansion of H_NEW ===")
H_new = t - (1 - t) * (t + rho * sp.log(1 - t)) / (1 - rho)
series = sp.series(H_new, t, 0, 4).removeO()
series = sp.simplify(series)
say(f"H_NEW(t) small-t series (up to t^3) = {series}")
coeff_t2 = sp.simplify(series.coeff(t, 2))
coeff_t3 = sp.simplify(series.coeff(t, 3))
say(f"coefficient of t^2: {coeff_t2}   (compare to M-U's coefficient 1 at rho=0)")
say(f"coefficient of t^3: {coeff_t3}")
say(f"check coeff_t2 at rho=0: {coeff_t2.subs(rho, 0)}  (should be 1, matching M-U H~t^2)")
say("=> leading order remains EXACTLY t^2 (beta=1) for any fixed rho in (0,1); "
    "b/n->lambda fixed only RESCALES the U_{1/2} coefficient "
    "((2-rho)/(2(1-rho)) instead of 1), it does NOT produce an "
    "intermediate exponent. Ruled out as a source of alpha in (1/2,1).")

log.close()
