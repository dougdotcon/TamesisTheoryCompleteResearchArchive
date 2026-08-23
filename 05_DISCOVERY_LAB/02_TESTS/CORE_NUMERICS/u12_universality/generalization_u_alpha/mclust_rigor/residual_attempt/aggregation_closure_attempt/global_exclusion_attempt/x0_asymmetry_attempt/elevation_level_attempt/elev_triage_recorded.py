#!/usr/bin/env python3
"""
elev_triage_recorded.py -- CHEAP TRIAGE ONLY.

Evaluates the candidate `phi_RED` (and its conditional half `phi_U(c(1-rho))`)
against Monte-Carlo means ALREADY RECORDED by earlier fronts / the referee.
No new simulation, no new seed.  Same convention as every predecessor: this is
screening, NOT validation.  The decision about `phi_RED` is taken by
`elev_validate.py` with fresh seeds.

Recorded grids read (read-only):
  ../adversarial/ref_mc_A_*.json          seed 20260823701 (has phi_notR!)
  ../adversarial/ref_mc_C_*.json          seed 20260823703 (has phi_notR!)
  ../x0_asym_validate_results.json        seed 20260822943
  ../../mclust_global_validate_results.json                seed 20260822911
  ../../../mclust_aggregation_validate_results.json        seed 20260822904
  ../../../../mclust_residual_validate_results.json        seed 720330339
"""
import glob
import json
import math
import os
import sys

import elev_formula as F

HERE = os.path.dirname(os.path.abspath(__file__))


def load_ref_grid(tag):
    cells = []
    for fn in sorted(glob.glob(os.path.join(HERE, "..", "adversarial", f"ref_mc_{tag}_*.json"))):
        d = json.load(open(fn))
        cells.extend(d["cells"])
    cells.sort(key=lambda r: (r["b"], r["c"]))
    return cells


def load_plain(relpath, key_phi="phi_mc", key_sem="sem"):
    fn = os.path.join(HERE, relpath)
    if not os.path.exists(fn):
        return None
    d = json.load(open(fn))
    rows = d["cells"] if isinstance(d, dict) and "cells" in d else d
    if isinstance(d, dict) and "results" in d:
        rows = d["results"]
    out = []
    for r in rows:
        phi = r.get("phi_mc")
        sem = r.get("sem_phi", r.get("sem", r.get("sem_mc")))
        if phi is None or sem is None:
            continue
        out.append(dict(n=r["n"], b=r["b"], c=r["c"], phi_mc=phi, sem_phi=sem))
    return out


def chi2(rows, fname):
    s = 0.0
    for r in rows:
        pred = fname(r["b"], r["c"], r["n"])
        s += ((r["phi_mc"] - pred) / r["sem_phi"]) ** 2
    return s


def main():
    print("=" * 100)
    print("CHEAP TRIAGE on ALREADY-RECORDED Monte-Carlo means (no new seed, no new simulation)")
    print("=" * 100)

    for tag, seed in (("A", 20260823701), ("C", 20260823703)):
        cells = load_ref_grid(tag)
        if not cells:
            print(f"referee grid {tag}: not found")
            continue
        print()
        print(f"--- referee grid {tag} (seed {seed}), {len(cells)} cells ---")
        print(" TEST 0 (the decisive mechanism-level one): measured phi(cyclic | x0 not in R)")
        print("         vs phi_V4 (constant elevation P_lead)  vs  phi_U(c(1-rho)) (this front)")
        print(f"{'n':>8} {'b':>5} {'c':>6} {'rho':>7} | {'phi_notR meas':>13} {'sem':>9} |"
              f" {'phi_V4':>10} {'dev%':>7} {'z':>7} | {'phi_U(c(1-r))':>13} {'dev%':>7} {'z':>7}")
        c2v4 = c2red = 0.0
        for r in cells:
            b, c, n = r["b"], r["c"], r["n"]
            rho = F.rho_of(b, c, n)
            m, s = r["phi_notR"], r["sem_phi_notR"]
            v4 = F.phi_V4(b, c, n)
            rd = F.phi_notR_RED(b, c, n)
            dv4, zv4 = 100 * (m - v4) / v4, (m - v4) / s
            drd, zrd = 100 * (m - rd) / rd, (m - rd) / s
            c2v4 += zv4 ** 2
            c2red += zrd ** 2
            print(f"{n:>8} {b:>5} {c:>6.0f} {rho:>7.4f} | {m:>13.6f} {s:>9.6f} |"
                  f" {v4:>10.6f} {dv4:>+7.2f} {zv4:>+7.2f} | {rd:>13.6f} {drd:>+7.2f} {zrd:>+7.2f}")
        print(f"  chi2 on phi(cyclic|x0 not in R):  phi_V4 = {c2v4:8.2f}    phi_U(c(1-rho)) = {c2red:8.2f}"
              f"   ({len(cells)} cells)")

        print()
        print(" TEST 0b: measured eps  vs eps_ref (formula of record)  vs eps_RED (this front)")
        c2er = c2ed = 0.0
        for r in cells:
            b, c, n = r["b"], r["c"], r["n"]
            rho = F.rho_of(b, c, n)
            rs = F.rho_start_of(b, c, n)
            T = F.T_V4(b, c, n)
            eref = (rs / rho) * F.phi_runstart_V4(b, c, n) + (1 + c * T) / ((1 - rho) * n)
            ered = F.eps_RED(b, c, n)
            m, s = r["eps"], r["sem_eps"]
            c2er += ((m - eref) / s) ** 2
            c2ed += ((m - ered) / s) ** 2
            print(f"{n:>8} {b:>5} {c:>6.0f} {rho:>7.4f} | meas={m:.6e} +-{s:.1e} |"
                  f" ref={eref:.6e} ({100*(m-eref)/eref:+6.2f}%)  RED={ered:.6e} ({100*(m-ered)/ered:+6.2f}%)")
        print(f"  chi2 on eps: eps_ref = {c2er:9.1f}   eps_RED = {c2ed:9.1f}")

        print()
        print(" TEST 0c: full phi")
        print(f"{'n':>8} {'b':>5} {'c':>6} {'rho':>7} | {'phi_mc':>10} {'sem':>9} |"
              f" {'CAND dev%':>10} {'z':>7} | {'EPSR dev%':>10} {'z':>7} | {'RED dev%':>10} {'z':>7}")
        cc = ce = cr = 0.0
        for r in cells:
            b, c, n = r["b"], r["c"], r["n"]
            rho = F.rho_of(b, c, n)
            m, s = r["phi_mc"], r["sem_phi"]
            pc, pe, pr = F.phi_CAND(b, c, n), F.phi_EPSR(b, c, n), F.phi_RED(b, c, n)
            zc, ze, zr = (m - pc) / s, (m - pe) / s, (m - pr) / s
            cc += zc ** 2
            ce += ze ** 2
            cr += zr ** 2
            print(f"{n:>8} {b:>5} {c:>6.0f} {rho:>7.4f} | {m:>10.6f} {s:>9.6f} |"
                  f" {100*(m-pc)/pc:>+10.3f} {zc:>+7.2f} | {100*(m-pe)/pe:>+10.3f} {ze:>+7.2f} |"
                  f" {100*(m-pr)/pr:>+10.3f} {zr:>+7.2f}")
        print(f"  chi2 ({len(cells)} cells): phi_CAND = {cc:8.2f}   phi_EPSR = {ce:8.2f}   phi_RED = {cr:8.2f}")

    print()
    print("--- other recorded grids (phi only) ---")
    others = [
        ("x0_asym_validate (20260822943)", "../x0_asym_validate_results.json"),
        ("global_exclusion (20260822911)", "../../mclust_global_validate_results.json"),
        ("aggregation      (20260822904)", "../../../mclust_aggregation_validate_results.json"),
        ("residual         (720330339)  ", "../../../../mclust_residual_validate_results.json"),
    ]
    for name, rel in others:
        rows = load_plain(rel)
        if not rows:
            print(f"{name}: NOT FOUND ({rel})")
            continue
        a = chi2(rows, F.phi_CAND)
        b_ = chi2(rows, F.phi_EPSR)
        c_ = chi2(rows, F.phi_RED)
        print(f"{name}: {len(rows):2d} cells   chi2  CAND={a:8.2f}   EPSR={b_:8.2f}   RED={c_:8.2f}")


if __name__ == "__main__":
    main()
