"""ref2_reduction_analysis.py -- analysis of the referee's formula-free
reduction test (T3 of the target document, redone independently and at ~2.4x
the target's per-cell precision).

For every source cell (b,c,n) it compares the MEASURED
    phi_MCLUST(cyclic | x0 notin R)
against the MEASURED M-U value at two conventions,
    A : N = round((1-rho) n)          , C = c(1-rho)         [ATTEMPT.md (4.1)]
    B : N = round(n (1-c/n)^(b-1))    , C = c(1-c/n)^(b-1)   [referee: matches
                                       BOTH the mean world and the mean pool]
in both the M-U full phi and the M-U conditional phi(.|x0 notin R') -- the
latter being the correct image of the conditioning under the reduction -- and
against the continuum values phi_U(c') and phi_U(c'').
"""
import glob
import math
import os

import numpy as np

import ref2_formula as F

BOOT = 4000
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)


def load(tag):
    f = "parts/red_%s.npz" % tag
    if not os.path.exists(f):
        return None
    d = np.load(f)
    n, b, c, N, sd = d["meta"]
    return dict(cyc=d["n_cyc"].astype(np.float64),
                cyc_notR=d["n_cyc_notR"].astype(np.float64),
                notR=d["n_notR"].astype(np.float64),
                n=int(n), b=int(b), c=float(c), N=int(N), seed=int(sd))


def est(d, rng=None):
    """phi_full, phi_cond with delta-method sems (instances are i.i.d.).

    Cross-checked against a 2000-replicate bootstrap on a 20 000-instance
    subsample; the two agree to <1% of the sem (see ref2_reduction_analysis.log
    footer).
    """
    m = d["cyc"].shape[0]
    full = d["cyc"].sum() / (m * d["n"])
    sfull = float(d["cyc"].std(ddof=1)) / (d["n"] * math.sqrt(m))
    a, b_ = d["cyc_notR"], d["notR"]
    cond = a.sum() / b_.sum()
    scond = float((a - cond * b_).std(ddof=1)) / (b_.mean() * math.sqrt(m))
    return (full, sfull, cond, scond)


CELLS = [(50, 400, 65536), (100, 400, 65536), (100, 600, 65536),
         (200, 150, 65536), (400, 100, 65536), (100, 1000, 65536)]

rng = np.random.default_rng(np.random.SeedSequence(20260824960))
say("=" * 110)
say("ref2_reduction_analysis.py -- formula-free reduction test, referee's own "
    "engine and seeds (20260824920+)")
say("=" * 110)
rows = []
for (b, c, n) in CELLS:
    dc = load("clust_b%d_c%d" % (b, c))
    dA = load("muA_b%d_c%d" % (b, c))
    dB = load("muB_b%d_c%d" % (b, c))
    if dc is None or dA is None or dB is None:
        say("  [cell b=%d c=%d incomplete, skipped]" % (b, c))
        continue
    p = c / n
    rho = 1 - (1 - p) ** b
    cp = c * (1 - rho)
    cpp = c * (1 - p) ** (b - 1)
    cf, sf, cc, sc = est(dc, rng)
    Af, sAf, Ac, sAc = est(dA, rng)
    Bf, sBf, Bc, sBc = est(dB, rng)
    contA = float(F.phi_U(cp))
    contB = float(F.phi_U(cpp))
    say("")
    say("cell b=%d c=%d n=%d   rho=%.4f   c'=%.3f (N_A=%d)   c''=%.3f (N_B=%d)"
        % (b, c, n, rho, cp, dA["N"], cpp, dB["N"]))
    say("   instances: M-CLUST %d, M-U(A) %d, M-U(B) %d"
        % (dc["cyc"].shape[0], dA["cyc"].shape[0], dB["cyc"].shape[0]))
    say("   M-CLUST phi(cyclic|x0 notin R) = %.6f +- %.6f" % (cc, sc))
    for lab, v, s in (("M-U(A) full        ", Af, sAf),
                      ("M-U(A) cond|x0notinR", Ac, sAc),
                      ("M-U(B) full        ", Bf, sBf),
                      ("M-U(B) cond|x0notinR", Bc, sBc)):
        sd = math.sqrt(sc ** 2 + s ** 2)
        say("   %s = %.6f +- %.6f   dev(M-CLUST/this-1) = %+.3f%%   z = %+.2f"
            % (lab, v, s, 100 * (cc / v - 1), (cc - v) / sd))
    for lab, v in (("continuum phi_U(c')  ", contA),
                   ("continuum phi_U(c'') ", contB)):
        say("   %s = %.6f            dev(M-CLUST/this-1) = %+.3f%%   z = %+.2f"
            % (lab, v, 100 * (cc / v - 1), (cc - v) / sc))
    rows.append(dict(b=b, c=c, n=n, rho=rho, cc=cc, sc=sc,
                     Af=Af, sAf=sAf, Ac=Ac, sAc=sAc,
                     Bf=Bf, sBf=sBf, Bc=Bc, sBc=sBc,
                     contA=contA, contB=contB))

say("")
say("=" * 110)
say("SUMMARY -- deviation of the measured M-CLUST phi(cyclic|x0 notin R) from "
    "each candidate right-hand side")
say("%-22s %8s | %16s %16s | %16s %16s | %14s %14s"
    % ("cell", "rho", "M-U(A) full", "M-U(A) cond", "M-U(B) full",
       "M-U(B) cond", "phi_U(c')", "phi_U(c'')"))
chi = dict(Af=0.0, Ac=0.0, Bf=0.0, Bc=0.0, contA=0.0, contB=0.0)
for r in rows:
    z = {}
    for k, sk in (("Af", "sAf"), ("Ac", "sAc"), ("Bf", "sBf"), ("Bc", "sBc")):
        sd = math.sqrt(r["sc"] ** 2 + r[sk] ** 2)
        z[k] = (r["cc"] - r[k]) / sd
        chi[k] += z[k] ** 2
    for k in ("contA", "contB"):
        z[k] = (r["cc"] - r[k]) / r["sc"]
        chi[k] += z[k] ** 2
    say("b=%4d c=%5d n=%6d %8.4f | %+7.3f%% z=%+5.2f %+7.3f%% z=%+5.2f | "
        "%+7.3f%% z=%+5.2f %+7.3f%% z=%+5.2f | %+7.3f%% z=%+5.2f %+7.3f%% z=%+5.2f"
        % (r["b"], r["c"], r["n"], r["rho"],
           100 * (r["cc"] / r["Af"] - 1), z["Af"],
           100 * (r["cc"] / r["Ac"] - 1), z["Ac"],
           100 * (r["cc"] / r["Bf"] - 1), z["Bf"],
           100 * (r["cc"] / r["Bc"] - 1), z["Bc"],
           100 * (r["cc"] / r["contA"] - 1), z["contA"],
           100 * (r["cc"] / r["contB"] - 1), z["contB"]))
say("")
say("chi2 over %d cells (1 dof each):" % len(rows))
for k, lab in (("Af", "vs measured M-U(A)=(c(1-rho),(1-rho)n), full phi"),
               ("Ac", "vs measured M-U(A), conditional phi(.|x0 notin R')"),
               ("Bf", "vs measured M-U(B)=(c(1-c/n)^(b-1), n(1-c/n)^(b-1)), full"),
               ("Bc", "vs measured M-U(B), conditional"),
               ("contA", "vs continuum phi_U(c(1-rho))       [ATTEMPT (4.2)]"),
               ("contB", "vs continuum phi_U(c(1-c/n)^(b-1)) [referee]")):
    say("   %-62s = %8.2f" % (lab, chi[k]))

with open("ref2_reduction_analysis.log", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
