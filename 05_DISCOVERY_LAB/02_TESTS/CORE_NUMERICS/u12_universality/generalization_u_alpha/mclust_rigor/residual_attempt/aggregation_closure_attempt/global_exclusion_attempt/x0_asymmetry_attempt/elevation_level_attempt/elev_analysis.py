#!/usr/bin/env python3
"""
elev_analysis.py -- deterministic analysis of everything this front measured.
No simulation, no new seed.  Sections:

  1. T1/T2  the elevation as a function of t (pool probe)
  2. T3     the formula-free reduction test
  3. T4     the fresh 18-cell grid + the six beyond-anything-tested cells
  4.        chain-mass refinement phi_RED2 (derived, reported, not adopted)
  5.        sign test / summary
"""
import glob
import json
import math
import os

import numpy as np
from scipy import integrate

import elev_formula as F

HERE = os.path.dirname(os.path.abspath(__file__))


def sec(t):
    print()
    print("=" * 104)
    print(t)
    print("=" * 104)


# --------------------------------------------------------------------- part 4
def H_delta(u, delta):
    """Master formula H in the collapsed world when the chain points of R are
    counted in the kill mass:  q(u) = u(1 + delta(1-u))  gives
        (1-q(s))/(1-s) = 1 - delta s   =>   H(t) = t^2 + (delta/2) t^2 (1-t).
    (derived in ATTEMPT SS6.3)"""
    return u * u * (1.0 + 0.5 * delta * (1.0 - u))


def phi_U_delta(c, delta):
    v, _ = integrate.quad(lambda u: math.exp(-c * H_delta(u, delta)), 0, 1,
                          epsabs=1e-13, epsrel=1e-13, limit=400)
    return v


def T_U_delta(c, delta):
    v, _ = integrate.quad(lambda u: (1 - u) * math.exp(-c * H_delta(u, delta)), 0, 1,
                          epsabs=1e-13, epsrel=1e-13, limit=400)
    return v


def delta_chain(b, c, n, relative_to_MU=False):
    """The visited points of R (run starts hit + chain points) also kill an f-draw,
    but they are NOT part of the collapsed mass.  Their count at collapsed mass u is
    c' u /(1-rho), so  q(u) = u (1 + delta (1-u)),  delta = c/((1-rho) n).
    Relative to M-U at (c', n'), which carries its own delta_MU = c/n, the EXTRA is
    delta_extra = c rho /((1-rho) n).   (ATTEMPT SS6.3)"""
    r = F.rho_of(b, c, n)
    return c * (r if relative_to_MU else 1.0) / ((1.0 - r) * n)


def phi_RED2(b, c, n):
    r = F.rho_of(b, c, n)
    rs = F.rho_start_of(b, c, n)
    cp = F.c_eff(b, c, n)
    d = delta_chain(b, c, n)
    phiu = phi_U_delta(cp, d)
    T = T_U_delta(cp, d)
    eps = (rs / r) * T + (1.0 + cp * T) / ((1.0 - r) * n)
    return (1.0 - r) * phiu + r * eps


# --------------------------------------------------------------------- part 1
def part1():
    sec("PART 1 -- T1/T2: the per-target closure elevation AS A FUNCTION OF t "
        "(own walk simulator, exogenous probe, seeds 20260823810-817)")
    files = sorted(glob.glob(os.path.join(HERE, "pool_probe_b*_c*.json")))
    if not files:
        print("no pool-probe results found")
        return
    print("lam_measured : the elevation measured by Horvitz-Thompson against the master")
    print("               formula's own density K/((1-s) n)")
    print("lam_model    : the same quantity computed from THIS FRONT's pool law (3.1)")
    print("P_lead       : the CONSTANT that phi_CAND / phi_EPSR / phi_CAND5 / phi_GLOBAL use")
    print("ratio_exact  : sum(hits)/sum(w_exact) -- must be 1.000 if the pool law is right")
    rows = []
    for fn in files:
        d = json.load(open(fn))
        print()
        print(f"  n={d['n']} b={d['b']} c={d['c']:.0f} rho={d['rho']:.4f} "
              f"P_lead={d['P_lead']:.4f} P_exact={d['P_exact']:.4f} "
              f"walks={d['n_walks']} steps={d['n_steps']:,} audit_fail={d['audit_fail']}")
        print(f"    {'mass bin':>16} {'hits':>10} | {'lam meas':>9} {'+-':>7} | {'lam model':>9} |"
              f" {'P_lead':>8} | {'meas/model':>10} {'+-':>7} | {'meas/P_lead':>11}")
        for bn in d["bins"]:
            if bn["n_hits"] < 200:
                continue
            print(f"    [{bn['lo']:.3f},{bn['hi']:.3f}]{'':>4} {bn['n_hits']:>10.0f} |"
                  f" {bn['lam_measured']:>9.4f} {bn['sem_lam']:>7.4f} | {bn['lam_model']:>9.4f} |"
                  f" {d['P_lead']:>8.4f} | {bn['ratio_exact']:>10.5f} {bn['sem_ratio']:>7.5f} |"
                  f" {bn['lam_measured']/d['P_lead']:>11.5f}")
        a = d["agg"]
        print(f"    {'AGGREGATE':>16} {'':>10} | {a['lam_measured']:>9.4f} {a['sem_lam']:>7.4f} |"
              f" {a['lam_model']:>9.4f} | {d['P_lead']:>8.4f} | {a['ratio_exact']:>10.5f}"
              f" {a['sem_ratio']:>7.5f} | {a['lam_measured']/d['P_lead']:>11.5f}")
        print(f"    live-arc-start estimator (cross-check, low statistics): "
              f"meas={a['lam_measured_live']:.4f}+-{a['sem_lam_live']:.4f} "
              f"model={a['lam_model_live']:.4f} ratio={a['ratio_exact_live']:.5f}+-{a['sem_ratio_live']:.5f}")
        rows.append(d)

    print()
    print("  SUMMARY -- is the elevation a CONSTANT (what every formula of this lineage assumes)")
    print("  or the t-dependent lam(t) of eq. (3.1)?  chi2 of the measured lam per mass bin")
    print("  against each hypothesis (bins with >= 2000 hits only):")
    print(f"  {'b':>5} {'c':>6} {'rho':>7} | {'bins':>4} | {'lam range measured':>22} |"
          f" {'chi2 vs P_lead':>14} | {'chi2 vs lam(t)':>14} | {'ratio_exact':>11} {'+-':>7} {'z':>6}")
    tot_const = tot_model = 0.0
    ndf = 0
    for d in rows:
        a = d["agg"]
        c_const = c_model = 0.0
        k = 0
        lo = hi = None
        for bn in d["bins"]:
            if bn["n_hits"] < 2000 or bn["sem_lam"] <= 0:
                continue
            c_const += ((bn["lam_measured"] - d["P_lead"]) / bn["sem_lam"]) ** 2
            c_model += ((bn["lam_measured"] - bn["lam_model"]) / bn["sem_lam"]) ** 2
            k += 1
            lo = bn["lam_measured"] if lo is None else lo
            hi = bn["lam_measured"]
        tot_const += c_const
        tot_model += c_model
        ndf += k
        z = (a["ratio_exact"] - 1.0) / a["sem_ratio"]
        print(f"  {d['b']:>5} {d['c']:>6.0f} {d['rho']:>7.4f} | {k:>4} |"
              f" {lo:>9.4f} -> {hi:>9.4f} | {c_const:>14.1f} | {c_model:>14.1f} |"
              f" {a['ratio_exact']:>11.5f} {a['sem_ratio']:>7.5f} {z:>+6.2f}")
    print(f"  {'POOLED':>5} {'':>6} {'':>7} | {ndf:>4} | {'':>22} | {tot_const:>14.1f} |"
          f" {tot_model:>14.1f} |")


# --------------------------------------------------------------------- part 2
def part2():
    sec("PART 2 -- T3: the FORMULA-FREE reduction test  "
        "M-CLUST(b,c,n) | x0 not in R   ==   M-U(c(1-rho), (1-rho)n)")
    fn = os.path.join(HERE, "elev_reduction_results.json")
    if not os.path.exists(fn):
        print("no reduction results found")
        return
    rows = json.load(open(fn))["rows"]
    by = {}
    for r in rows:
        by.setdefault(tuple(r["src"]), {})[r["kind"]] = r
    print(f"  {'b':>5} {'c':>6} {'rho':>7} | {'M-CLUST phi(.|x0 notin R)':>25} |"
          f" {'M-U (n=(1-r)n)':>16} {'z':>6} | {'M-U (n=(1-r)(n+c))':>19} {'z':>6} |"
          f" {'phi_U(c(1-rho))':>15} {'z':>6}")
    chi_A = chi_B = chi_F = 0.0
    k = 0
    for src, g in sorted(by.items(), key=lambda kv: (kv[0][1], kv[0][2])):
        if "src" not in g:
            continue
        n, b, c = src
        rho = F.rho_of(b, c, n)
        s = g["src"]
        m, sm = s["phi_notR"], s["sem_phi_notR"]
        line = f"  {b:>5} {c:>6.0f} {rho:>7.4f} | {m:>15.6f} +-{sm:<8.6f} |"
        for kind, acc in (("muA", "A"), ("muB", "B")):
            if kind in g:
                q, sq = g[kind]["phi_notR"], g[kind]["sem_phi_notR"]
                z = (m - q) / math.hypot(sm, sq)
                line += f" {q:>16.6f} {z:>+6.2f} |" if kind == "muA" else f" {q:>19.6f} {z:>+6.2f} |"
                if kind == "muA":
                    chi_A += z * z
                else:
                    chi_B += z * z
        pu = F.phi_notR_RED(b, c, n)
        zf = (m - pu) / sm
        chi_F += zf * zf
        line += f" {pu:>15.6f} {zf:>+6.2f}"
        print(line)
        k += 1
    print(f"  chi2 over {k} cells:  vs M-U(n'=(1-rho)n) = {chi_A:.2f}   "
          f"vs M-U(n'=(1-rho)(n+c)) = {chi_B:.2f}   vs the continuum phi_U(c(1-rho)) = {chi_F:.2f}")
    print("  (the two M-U columns are MEASURED, not computed: no master formula enters this test)")


# --------------------------------------------------------------------- part 3
def part3():
    sec("PART 3 -- T4: fresh-seed validation (seeds 20260823820-843, own engine)")
    fn = os.path.join(HERE, "elev_validate_results.json")
    if not os.path.exists(fn):
        print("no validation results found")
        return
    d = json.load(open(fn))
    cells = d["cells"]
    print(f"  {'n':>7} {'b':>4} {'c':>6} {'rho':>7} {'bc/n':>6} | {'phi_mc':>10} {'sem':>9} |"
          f" {'CAND%':>8} {'z':>6} | {'EPSR%':>8} {'z':>6} | {'RED%':>8} {'z':>6} | {'RED2%':>8} {'z':>6}")
    tot = dict(CAND=0.0, EPSR=0.0, RED=0.0, RED2=0.0)
    tot18 = dict(CAND=0.0, EPSR=0.0, RED=0.0, RED2=0.0)
    sgn = dict(CAND=0, EPSR=0, RED=0, RED2=0)
    n18 = 0
    for i, r in enumerate(cells):
        n, b, c = r["n"], r["b"], r["c"]
        rho = F.rho_of(b, c, n)
        m, s = r["phi_mc"], r["sem_phi"]
        vals = dict(CAND=F.phi_CAND(b, c, n), EPSR=F.phi_EPSR(b, c, n),
                    RED=F.phi_RED(b, c, n), RED2=phi_RED2(b, c, n))
        line = (f"  {n:>7} {b:>4} {c:>6.0f} {rho:>7.4f} {b*c/n:>6.3f} |"
                f" {m:>10.6f} {s:>9.6f} |")
        for k in ("CAND", "EPSR", "RED", "RED2"):
            p = vals[k]
            z = (m - p) / s
            tot[k] += z * z
            if i < 18:
                tot18[k] += z * z
            if p < m:
                sgn[k] += 1
            line += f" {100*(m-p)/p:>+8.3f} {z:>+6.2f} |"
        if i < 18:
            n18 += 1
        print(line.rstrip("|"))
    print()
    print(f"  chi2 over the standard 18-cell grid : "
          + "   ".join(f"{k}={tot18[k]:8.2f}" for k in ("CAND", "EPSR", "RED", "RED2")))
    print(f"  chi2 over all {len(cells)} cells          : "
          + "   ".join(f"{k}={tot[k]:8.2f}" for k in ("CAND", "EPSR", "RED", "RED2")))
    print(f"  formula BELOW the MC mean in : "
          + "   ".join(f"{k}={sgn[k]}/{len(cells)}" for k in ("CAND", "EPSR", "RED", "RED2")))

    print()
    print("  the conditional half on its own (phi(cyclic|x0 notin R), measured):")
    print(f"  {'n':>7} {'b':>4} {'c':>6} {'rho':>7} | {'measured':>10} {'sem':>9} |"
          f" {'phi_V4':>10} {'dev%':>8} {'z':>6} | {'phi_U(c(1-r))':>13} {'dev%':>8} {'z':>6}")
    cv = cr = 0.0
    for r in cells:
        n, b, c = r["n"], r["b"], r["c"]
        rho = F.rho_of(b, c, n)
        m, s = r["phi_notR"], r["sem_phi_notR"]
        v4, rd = F.phi_V4(b, c, n), F.phi_notR_RED(b, c, n)
        zv, zr = (m - v4) / s, (m - rd) / s
        cv += zv * zv
        cr += zr * zr
        print(f"  {n:>7} {b:>4} {c:>6.0f} {rho:>7.4f} | {m:>10.6f} {s:>9.6f} |"
              f" {v4:>10.6f} {100*(m-v4)/v4:>+8.3f} {zv:>+6.2f} |"
              f" {rd:>13.6f} {100*(m-rd)/rd:>+8.3f} {zr:>+6.2f}")
    print(f"  chi2: phi_V4 = {cv:.2f}    phi_U(c(1-rho)) = {cr:.2f}   ({len(cells)} cells)")

    # ---- eps: the formula of record's channels vs the same channels under the reduction
    print()
    print("  eps = P(cyclic | x0 in R), measured on the same fresh grid:")
    ce = cr2 = 0.0
    for r in cells:
        n, b, c = r["n"], r["b"], r["c"]
        rho = F.rho_of(b, c, n)
        rs = F.rho_start_of(b, c, n)
        T = F.T_V4(b, c, n)
        eref = (rs / rho) * F.phi_runstart_V4(b, c, n) + (1 + c * T) / ((1 - rho) * n)
        ered = F.eps_RED(b, c, n)
        m, s = r["eps"], r["sem_eps"]
        ce += ((m - eref) / s) ** 2
        cr2 += ((m - ered) / s) ** 2
    print(f"    chi2 ({len(cells)} cells): eps_ref (formula of record) = {ce:.1f}    "
          f"eps_RED (this front) = {cr2:.1f}")

    # ---- cross-validation of MY engine against the recorded grids of this lineage
    print()
    print("  CROSS-VALIDATION of this front's engine against Monte-Carlo means recorded by")
    print("  earlier runs of the lineage (mandatory before trusting a new simulator):")
    mine = {(r["n"], r["b"], r["c"]): r for r in cells}
    import glob as _g
    for tag, seed in (("referee A", 20260823701), ("referee C", 20260823703)):
        rows = []
        for fn in sorted(_g.glob(os.path.join(HERE, "..", "adversarial",
                                              f"ref_mc_{tag[-1]}_*.json"))):
            rows.extend(json.load(open(fn))["cells"])
        k = c2 = 0
        zmax = 0.0
        zs = []
        for r in rows:
            key = (r["n"], r["b"], r["c"])
            if key not in mine:
                continue
            m = mine[key]
            z = (m["phi_mc"] - r["phi_mc"]) / math.hypot(m["sem_phi"], r["sem_phi"])
            zs.append(z)
            c2 += z * z
            zmax = max(zmax, abs(z))
            k += 1
        if k:
            print(f"    vs {tag} (seed {seed}): {k} cells, chi2/dof = {c2:.1f}/{k}, "
                  f"|z|max = {zmax:.2f}, mean z = {np.mean(zs):+.3f}")
    for name, rel in (("x0_asym (943)", "../x0_asym_validate_results.json"),
                      ("global_excl (911)", "../../mclust_global_validate_results.json")):
        fn2 = os.path.join(HERE, rel)
        if not os.path.exists(fn2):
            continue
        d2 = json.load(open(fn2))
        rows = d2["cells"] if isinstance(d2, dict) and "cells" in d2 else d2
        k = c2 = 0
        zs = []
        for r in rows:
            key = (r["n"], r["b"], r["c"])
            s2 = r.get("sem_phi", r.get("sem"))
            if key not in mine or s2 is None:
                continue
            m = mine[key]
            z = (m["phi_mc"] - r["phi_mc"]) / math.hypot(m["sem_phi"], s2)
            zs.append(z)
            c2 += z * z
            k += 1
        if k:
            print(f"    vs {name}: {k} cells, chi2/dof = {c2:.1f}/{k}, mean z = {np.mean(zs):+.3f}")


# --------------------------------------------------------------------- part 5
def part5():
    sec("PART 5 -- the O(c/n) pieces this front deliberately dropped, sized")
    print("  delta       = c/((1-rho) n)      -- the chain-point kill mass vs the continuum")
    print("  delta_extra = c rho/((1-rho) n)   -- the same, vs M-U at (c', n') which has its own")
    print(f"  {'n':>7} {'b':>4} {'c':>6} {'rho':>7} | {'c/n':>9} | {'delta':>9} | {'delta_extra':>11} |"
          f" {'phi_RED2/phi_RED-1':>19} | {'T3 shift pred':>13}")
    cells = [(32768, 8, 160.0), (65536, 50, 400.0), (65536, 100, 400.0),
             (65536, 200, 150.0), (65536, 300, 150.0), (65536, 400, 100.0),
             (65536, 100, 600.0), (65536, 200, 600.0), (65536, 100, 1000.0),
             (65536, 800, 100.0), (65536, 400, 300.0), (131072, 200, 800.0)]
    for (n, b, c) in cells:
        rho = F.rho_of(b, c, n)
        d = delta_chain(b, c, n)
        de = delta_chain(b, c, n, relative_to_MU=True)
        r1, r2 = F.phi_RED(b, c, n), phi_RED2(b, c, n)
        print(f"  {n:>7} {b:>4} {c:>6.0f} {rho:>7.4f} | {c/n:>9.2e} | {d:>9.5f} | {de:>11.5f} |"
              f" {100*(r2/r1-1):>+18.3f}% | {-100*de/4:>+12.3f}%")


if __name__ == "__main__":
    part1()
    part2()
    part3()
    part5()
