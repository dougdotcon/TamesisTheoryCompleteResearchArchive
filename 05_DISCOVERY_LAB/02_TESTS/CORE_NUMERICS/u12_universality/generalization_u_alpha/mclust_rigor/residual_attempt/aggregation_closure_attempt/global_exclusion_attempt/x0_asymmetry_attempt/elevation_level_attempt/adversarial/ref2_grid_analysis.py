"""ref2_grid_analysis.py -- the referee's own fresh-seed phi grid, scored
against every candidate formula.

phi        : sum|cyc| / (N n)                        [the full phi]
phi_notR   : sum|cyc \\ R| / sum|R^c|                 [the conditional half --
             the quantity the reduction claim (4.2) is directly about, with no
             eps model in it at all]
Errors: delta method (instances i.i.d.), cross-checked against bootstrap.
"""
import glob
import math
import os

import numpy as np

import ref2_formula as F

OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s, flush=True)


FORMS = [("CAND", F.phi_CAND), ("EPSR", F.phi_EPSR), ("RED", F.phi_RED),
         ("REDB", F.phi_REDB), ("RED2", F.phi_RED2), ("RED2B", F.phi_RED2B)]
CONDS = [("phi_U(c')", lambda b, c, n: F.phi_U(c * (1 - F.rho_of(b, c, n)))),
         ("phi_U(c'')", lambda b, c, n: F.phi_U(c * (1 - float(c) / n) ** (b - 1))),
         ("phi_V4", F.phi_V4)]

say("=" * 118)
say("ref2_grid_analysis.py -- referee's own fresh 24-cell grid "
    "(seeds 20260824940+), own engine")
say("=" * 118)
say("%-24s %6s %9s %10s | %s" % ("cell", "rho", "phi_mc", "sem",
                                 "  ".join("%9s" % k for k, _ in FORMS)))
chi = {k: 0.0 for k, _ in FORMS}
chi18 = {k: 0.0 for k, _ in FORMS}
below = {k: 0 for k, _ in FORMS}
chic = {k: 0.0 for k, _ in CONDS}
rowsc = []
ncell = 0
for i in range(24):
    p = "parts/grid_%02d.npz" % i
    if not os.path.exists(p):
        continue
    d = np.load(p)
    n, b, c, N, sd = d["meta"]
    n, b, c, N = int(n), int(b), int(c), int(N)
    cyc = d["n_cyc"].astype(np.float64)
    cn = d["n_cyc_notR"].astype(np.float64)
    nr = d["n_notR"].astype(np.float64)
    m = cyc.shape[0]
    phi = cyc.sum() / (m * n)
    sem = cyc.std(ddof=1) / (n * math.sqrt(m))
    cond = cn.sum() / nr.sum()
    scond = (cn - cond * nr).std(ddof=1) / (nr.mean() * math.sqrt(m))
    rho = float(F.rho_of(b, c, n))
    line = "n=%6d b=%4d c=%5d %6.4f %9.6f %10.6f |" % (n, b, c, rho, phi, sem)
    for k, fn in FORMS:
        v = float(fn(b, c, n))
        z = (phi - v) / sem
        chi[k] += z * z
        if i < 18:
            chi18[k] += z * z
        if phi > v:
            below[k] += 1
        line += " %+8.2f" % z
    say(line + "   (%d inst)" % m)
    zc = []
    for k, fn in CONDS:
        v = float(fn(b, c, n))
        z = (cond - v) / scond
        chic[k] += z * z
        zc.append(z)
    rowsc.append((n, b, c, rho, cond, scond, zc))
    ncell += 1

say("")
say("chi2 on the FULL phi, %d cells:" % ncell)
for k, _ in FORMS:
    say("   %-6s chi2 = %9.2f   (18 standard cells: %8.2f)   below-MC %d/%d"
        % (k, chi[k], chi18[k], below[k], ncell))
say("")
say("The CONDITIONAL half phi(cyclic | x0 notin R) -- no eps model on either "
    "side, this is the reduction claim itself:")
say("%-24s %6s %11s %10s | %9s %9s %9s"
    % ("cell", "rho", "phi_notR", "sem", "z phi_U(c')", "z phi_U(c'')", "z phi_V4"))
for (n, b, c, rho, cond, scond, zc) in rowsc:
    say("n=%6d b=%4d c=%5d %6.4f %11.6f %10.6f | %+9.2f %+9.2f %+9.2f"
        % (n, b, c, rho, cond, scond, zc[0], zc[1], zc[2]))
say("")
say("chi2 on phi(cyclic|x0 notin R), %d cells:" % ncell)
for k, _ in CONDS:
    say("   %-12s chi2 = %9.2f" % (k, chic[k]))

with open("ref2_grid_analysis.log", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
