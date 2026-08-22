"""residual_attempt -- stage C (DISC-DEC-033, MCLUST-RESIDUAL-RIGOR).

Sanity check ONLY (reuses wave-4's recorded MC values, own seeds
SeedSequence(20260822018), no new simulation here -- same reuse
discipline as ../mclust_decompose.py) of the SECOND candidate correction
derived from scratch in ATTEMPT.md sec 3: the CLOSURE HAZARD itself
(not just the kill probability q(s)) is mis-specified in wave 4's
phi_NEW, because wave 4 left the master formula's (1-t)/(1-s) survival
factor "unaltered" (their own words, DERIVATION_MCLUST_FIXED.md sec 4)
while only correcting q(s).

Derivation summary (full version in ATTEMPT.md sec 3):
normal pi-stepping (the process that "closure into an existing arc
start" competes over) can NEVER land on a shadowed interior block
member -- proven exactly by the same shadowing lemma wave 4 already
used for the encounter rate (sec 2 of DERIVATION_MCLUST_FIXED.md): if
x not in R then pi(x) is never a shadowed point (shadowed q has
pi^{-1}(q) in R by construction of blocks, so pi(x)=q would force
x in R, contradiction). Since R-depletion is negligible (wave 4's own
finding, sec 3: consumed R mass by chains/run-starts is <=0.22% of n
even at the most extreme stress point), essentially ALL of R (fraction
rho of the whole space) remains permanently "invisible" to normal
pi-stepping -- it can never be landed on by a normal step, and can
never itself be an arc-start (arc-starts are "survive" landings, which
by construction land on fresh NON-R mass). So the closure hazard,
which wave 4 (following the unmodified master formula) computes as
1/(1-r) [uniform draw from the (1-r)n remaining UNVISITED points],
should really be 1/(1-r-rho) [uniform draw from the (1-r)n - rho*n
remaining NON-SHADOWED unvisited points -- shadowed mass structurally
can never be a normal-step target, so it should not dilute the
closure-competition pool].

Re-deriving the master formula (DERIVATIONS.md sec 1) with this hazard
in place of 1/(1-r) (keeping q_CLUST(s)=s/(1-rho) from wave 4 UNCHANGED,
since that piece concerns the FULL-n uniform destination draws, a
different physical process untouched by the shadowing argument) gives,
after a suspicious-looking but exact cancellation:

    (1 - q_CLUST(s)) / (1 - s - rho) = 1/(1-rho)   identically in s

    H_v3(t) = t^2 / (1-rho),        t in [0, 1-rho)
    phi_v3(c) = (1/(1-rho)) * int_0^{1-rho} exp(-c t^2/(1-rho)) dt
              = (1/sqrt(1-rho)) * int_0^{sqrt(1-rho)} exp(-c u^2) du

(substitute u = t/sqrt(1-rho)). Consistency checks: rho->0 recovers
phi_U(c) exactly; H_v3((1-rho)^-) = (1-rho) matches the general theory's
H(T^-)=T at the (rescaled) upper limit T=1-rho.
"""
import json
import math
import os

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
WAVE4 = os.path.dirname(HERE)


def phi_U(c):
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t), 0, 1)
    return v


def rho_of(c, n, b):
    return 1.0 - (1.0 - c / n) ** b


def H_NEW(t, rho):
    if rho < 1e-12:
        return t * t
    if t < 1e-13:
        return 0.0
    return t - (1.0 - t) * (t + rho * math.log(1.0 - t)) / (1.0 - rho)


def phi_NEW(c, n, b):
    rho = rho_of(c, n, b)
    v, _ = integrate.quad(lambda t: math.exp(-c * H_NEW(t, rho)), 0, 1, limit=200)
    return v


def phi_V3(c, n, b):
    """Closed form: (1/sqrt(1-rho)) * int_0^{sqrt(1-rho)} exp(-c u^2) du."""
    rho = rho_of(c, n, b)
    if rho < 1e-12:
        return phi_U(c)
    upper = math.sqrt(1.0 - rho)
    v, _ = integrate.quad(lambda u: math.exp(-c * u * u), 0, upper)
    return v / upper


def phi_V3_direct(c, n, b):
    """Same thing, unsubstituted form -- cross-check the algebra numerically."""
    rho = rho_of(c, n, b)
    if rho < 1e-12:
        return phi_U(c)
    T = 1.0 - rho
    v, _ = integrate.quad(lambda t: math.exp(-c * t * t / (1.0 - rho)), 0, T)
    return v / (1.0 - rho)


def main():
    with open(os.path.join(WAVE4, "mclust_validate_results.json")) as fh:
        d = json.load(fh)

    print(f"{'n':>7} {'b':>4} {'c':>7} {'rho':>7} {'bc/n':>8} | {'MC':>9} | "
          f"{'OLD dev%':>9} | {'NEW dev%':>9} | {'V3 dev%':>9} | {'cross-check':>12}")
    rows = []
    max_cross_diff = 0.0
    for r in d["cells"]:
        n, b, c = r["n"], r["b"], r["c"]
        rho = r["rho_formula"]
        mc = r["phi_mc"]
        old = r["phi_old"]
        new = r["phi_new"]
        v3 = phi_V3(c, n, b)
        v3d = phi_V3_direct(c, n, b)
        cross = abs(v3 - v3d)
        max_cross_diff = max(max_cross_diff, cross)
        dev = lambda x: (mc - x) / x * 100
        bcn = b * c / n
        print(f"{n:7d} {b:4d} {c:7.1f} {rho:7.4f} {bcn:8.4f} | {mc:9.6f} | "
              f"{dev(old):9.2f} | {dev(new):9.2f} | {dev(v3):9.2f} | diff={cross:.2e}")
        rows.append(dict(n=n, b=b, c=c, rho=rho, bcn=bcn, mc=mc, sem=r["sem"],
                          phi_old=old, phi_new=new, phi_v3=v3, phi_v3_direct=v3d,
                          dev_old_pct=dev(old), dev_new_pct=dev(new),
                          dev_v3_pct=dev(v3)))

    print(f"\nmax |phi_v3 - phi_v3_direct| across grid (algebra cross-check): {max_cross_diff:.3e}")
    with open(os.path.join(HERE, "stageC_v3_reuse_check.json"), "w") as fh:
        json.dump(rows, fh, indent=2)
    print("saved stageC_v3_reuse_check.json")


if __name__ == "__main__":
    main()
