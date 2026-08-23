"""ref2_tables.py -- internal-consistency audit of every number printed in the
tables of `elevation_level_attempt/ATTEMPT.md` (sections 7.1-7.3, 8, 9, 10).

Nothing here re-runs the target's simulation.  Every table is transcribed by
hand from the document and then checked for internal arithmetic consistency:
  * does the printed z follow from the printed mean/sem and the printed dev%?
  * does the printed aggregate chi2 equal the sum of the printed z^2?
  * do the printed rho / bc/n follow from (b, c, n)?
  * does the referee's OWN independent implementation of phi_CAND, phi_EPSR,
    phi_RED, phi_RED2 reproduce the formula value implied by the printed
    (phi_mc, dev%) pair?
  * do the printed lambda-model values follow from (3.1) at the stated bin?
"""
import math

import mpmath as mp

import ref2_formula as F

mp.mp.dps = 30
OUT = []


def say(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s)
    print(s)


def chk(name, got, want, tol, unit=""):
    ok = abs(got - want) <= tol
    say("   %-52s got %12.6f  printed %12.6f  %s%s"
        % (name, got, want, "OK" if ok else "**MISMATCH**", unit))
    return ok


# ===========================================================================
say("=" * 78)
say("ref2_tables.py -- arithmetic audit of ATTEMPT.md tables")
say("=" * 78)

# ---------------------------------------------------------------------------
# Section 9 / T4 grid, transcribed from ATTEMPT.md
# columns: n, b, c, rho_print, bcn_print, phi_mc, sem,
#          (dev%,z) for CAND, EPSR, RED, RED2
# ---------------------------------------------------------------------------
T4 = [
    (32768, 8, 10, 0.0024, 0.002, 0.279944, 0.001045,
     (+0.047, +0.12), (+0.021, +0.06), (-0.012, -0.03), (-0.007, -0.02)),
    (32768, 8, 40, 0.0097, 0.010, 0.138028, 0.000506,
     (-0.953, -2.62), (-1.064, -2.93), (-1.125, -3.10), (-1.100, -3.03)),
    (32768, 8, 160, 0.0384, 0.039, 0.068857, 0.000251,
     (+0.343, +0.94), (-0.143, -0.39), (-0.262, -0.72), (-0.147, -0.40)),
    (65536, 50, 10, 0.0076, 0.008, 0.278910, 0.001005,
     (+0.006, +0.02), (-0.007, -0.02), (-0.109, -0.30), (-0.107, -0.30)),
    (65536, 50, 50, 0.0374, 0.038, 0.123341, 0.000462,
     (+0.522, +1.39), (+0.448, +1.19), (+0.234, +0.62), (+0.250, +0.67)),
    (65536, 50, 150, 0.1083, 0.114, 0.068806, 0.000253,
     (+1.059, +2.85), (+0.810, +2.19), (+0.446, +1.21), (+0.504, +1.37)),
    (65536, 50, 400, 0.2637, 0.305, 0.038341, 0.000144,
     (+1.431, +3.76), (+0.608, +1.61), (+0.021, +0.06), (+0.215, +0.57)),
    (65536, 100, 10, 0.0151, 0.015, 0.279245, 0.001043,
     (+0.612, +1.63), (+0.599, +1.59), (+0.393, +1.05), (+0.395, +1.05)),
    (65536, 100, 50, 0.0735, 0.076, 0.120783, 0.000449,
     (+0.547, +1.46), (+0.470, +1.26), (+0.043, +0.12), (+0.060, +0.16)),
    (65536, 100, 150, 0.2048, 0.229, 0.064180, 0.000237,
     (+0.185, +0.50), (-0.095, -0.26), (-0.815, -2.23), (-0.751, -2.05)),
    (65536, 100, 400, 0.4579, 0.610, 0.032920, 0.000122,
     (+2.104, +5.56), (+0.961, +2.57), (-0.220, -0.60), (+0.039, +0.10)),
    (65536, 100, 600, 0.6014, 0.916, 0.023201, 0.000085,
     (+3.082, +8.12), (+0.718, +1.94), (-0.730, -2.00), (-0.203, -0.55)),
    (65536, 200, 5, 0.0151, 0.015, 0.392217, 0.001427,
     (+0.186, +0.51), (+0.180, +0.49), (-0.117, -0.32), (-0.116, -0.32)),
    (65536, 200, 20, 0.0592, 0.061, 0.192938, 0.000717,
     (+0.940, +2.51), (+0.911, +2.43), (+0.350, +0.94), (+0.356, +0.96)),
    (65536, 200, 60, 0.1674, 0.183, 0.105143, 0.000392,
     (+1.656, +4.37), (+1.550, +4.09), (+0.610, +1.63), (+0.633, +1.69)),
    (65536, 200, 150, 0.3676, 0.458, 0.057935, 0.000216,
     (+2.161, +5.68), (+1.795, +4.73), (+0.326, +0.87), (+0.407, +1.09)),
    (65536, 300, 150, 0.4971, 0.687, 0.051624, 0.000194,
     (+2.851, +7.38), (+2.377, +6.18), (+0.151, +0.40), (+0.250, +0.66)),
    (65536, 400, 100, 0.4571, 0.610, 0.065915, 0.000245,
     (+3.402, +8.86), (+3.108, +8.12), (+0.663, +1.77), (+0.722, +1.93)),
    # the six "extreme" cells
    (65536, 200, 600, 0.8411, 1.831, 0.015106, 0.000056,
     (+8.231, +20.43), (+1.869, +4.93), (-1.179, -3.20), (+0.064, +0.17)),
    (65536, 800, 100, 0.7053, 1.221, 0.048962, 0.000188,
     (+7.012, +17.06), (+6.404, +15.67), (+1.217, +3.13), (+1.320, +3.39)),
    (65536, 100, 1000, 0.7851, 1.526, 0.013780, 0.000051,
     (+8.253, +20.57), (+0.761, +2.04), (-1.102, -3.01), (+0.497, +1.33)),
    (65536, 400, 300, 0.8404, 1.831, 0.020960, 0.000079,
     (+7.426, +18.29), (+4.080, +10.37), (-0.467, -1.24), (+0.126, +0.33)),
    (131072, 200, 800, 0.7061, 1.221, 0.017229, 0.000064,
     (+3.215, +8.34), (+1.044, +2.77), (-0.669, -1.80), (-0.193, -0.52)),
    (131072, 400, 400, 0.7055, 1.221, 0.024225, 0.000091,
     (+3.275, +8.47), (+2.164, +5.66), (-0.310, -0.83), (-0.079, -0.21)),
]

say("")
say("## A. section 9 (T4) -- rho, bc/n, dev%/z consistency, and the referee's")
say("##    own independent evaluation of the four formulas")
say("")
say("   %-22s %9s %9s | %s" % ("cell", "rho", "bc/n", "per-formula checks"))
bad_rho = bad_z = bad_form = 0
chi = {k: 0.0 for k in ("CAND", "EPSR", "RED", "RED2")}
chi18 = {k: 0.0 for k in ("CAND", "EPSR", "RED", "RED2")}
below = {k: 0 for k in ("CAND", "EPSR", "RED", "RED2")}
myfun = {"CAND": F.phi_CAND, "EPSR": F.phi_EPSR, "RED": F.phi_RED,
         "RED2": F.phi_RED2}
rows_out = []
for i, row in enumerate(T4):
    n, b, c, rho_p, bcn_p, phimc, sem = row[:7]
    devs = dict(zip(("CAND", "EPSR", "RED", "RED2"), row[7:]))
    rho = 1 - (1 - c / n) ** b
    if abs(rho - rho_p) > 5e-5:
        bad_rho += 1
        say("   ** rho mismatch b=%d c=%d: computed %.6f printed %.4f"
            % (b, c, rho, rho_p))
    if abs(b * c / n - bcn_p) > 1.1e-3:
        bad_rho += 1
        say("   ** bc/n mismatch b=%d c=%d: computed %.4f printed %.3f"
            % (b, c, b * c / n, bcn_p))
    line = "   n=%6d b=%4d c=%5d rho=%.4f |" % (n, b, c, rho)
    for k in ("CAND", "EPSR", "RED", "RED2"):
        dv, zp = devs[k]
        phif = phimc / (1 + dv / 100.0)          # dev% = (phi_mc/phi_form - 1)*100
        zc = (phimc - phif) / sem
        if abs(zc - zp) > 0.06 * max(1.0, abs(zp)) + 0.02:
            bad_z += 1
            line += " %s z:%+.2f/%+.2f**" % (k, zc, zp)
        mine = float(myfun[k](b, c, n))
        rel = mine / phif - 1
        if abs(rel) > 3e-4:
            bad_form += 1
            line += " %s form:%+.2e**" % (k, rel)
        chi[k] += zp * zp
        if i < 18:
            chi18[k] += zp * zp
        if dv > 0:
            below[k] += 1
    rows_out.append(line)
    say(line)

say("")
say("   rho / bc/n mismatches   : %d" % bad_rho)
say("   z-vs-(dev,sem) mismatches: %d  (tolerance 6%% of z, floor 0.02)" % bad_z)
say("   referee's own formula value vs the value implied by (phi_mc,dev%%): "
    "%d cells beyond 3e-4 relative" % bad_form)
say("")
say("   chi2 recomputed from the printed z, standard 18 cells:")
for k in ("CAND", "EPSR", "RED", "RED2"):
    say("      %-5s %10.2f   (printed %s)" % (k, chi18[k],
        {"CAND": 324.66, "EPSR": 181.50, "RED": 30.20, "RED2": 26.97}[k]))
say("   chi2 recomputed from the printed z, all 24 cells:")
for k in ("CAND", "EPSR", "RED", "RED2"):
    say("      %-5s %10.2f   (printed %s)" % (k, chi[k],
        {"CAND": 1931.87, "EPSR": 602.62, "RED": 64.79, "RED2": 40.71}[k]))
say("   'formula BELOW the MC mean' counts (dev%%>0), 24 cells:")
for k in ("CAND", "EPSR", "RED", "RED2"):
    say("      %-5s %d/24   (printed %s)" % (k, below[k],
        {"CAND": "23/24", "EPSR": "20/24", "RED": "11/24",
         "RED2": "15/24"}[k]))

# ---------------------------------------------------------------------------
say("")
say("## B. section 10 -- the seven-grid pooled table")
GRIDS = [
    ("residual_attempt", 18, 81.60, 49.58, 15.14, 15.33, 15, 14, 11),
    ("aggregation_closure", 18, 73.63, 46.52, 21.59, 20.57, 16, 16, 10),
    ("global_exclusion", 18, 80.06, 43.58, 11.05, 12.27, 12, 12, 8),
    ("x0_asymmetry", 18, 121.78, 71.40, 14.79, 17.47, 18, 17, 15),
    ("referee grid A", 18, 335.56, 183.56, 33.13, 32.83, 16, 15, 10),
    ("referee grid C", 18, 298.80, 152.57, 22.85, 20.93, 15, 14, 10),
    ("this front fresh", 24, 1931.87, 602.62, 64.79, 40.71, 23, 20, 11),
]
tot = [sum(g[i] for g in GRIDS) for i in range(1, 9)]
say("   cells       %6d   (printed 132)" % tot[0])
for j, k in enumerate(("CAND", "EPSR", "RED", "RED2")):
    say("   chi2 %-5s %10.2f   (printed %s)"
        % (k, tot[1 + j], {"CAND": 2923.29, "EPSR": 1149.82,
                           "RED": 183.33, "RED2": 160.10}[k]))
for j, k in enumerate(("CAND", "EPSR", "RED")):
    say("   below %-5s %6d/132  (printed %s)"
        % (k, tot[5 + j], {"CAND": "115/132", "EPSR": "108/132",
                           "RED": "75/132"}[k]))
say("   'standard grids only' (126 cells) =  pooled - (fresh24 - fresh18):")
for j, k in enumerate(("CAND", "EPSR", "RED", "RED2")):
    v = tot[1 + j] - (GRIDS[-1][2 + j] - chi18[k])
    say("      %-5s %10.2f   (printed %s)" % (k, v,
        {"CAND": 1316.08, "EPSR": 728.70, "RED": 148.74, "RED2": 146.36}[k]))
say("   sign test on 75/132: z = %.3f (printed '1.5 sigma')"
    % ((75 - 66) / math.sqrt(132 * 0.25)))
say("   sign test on 115/132: z = %.2f -> p ~ %.1e (printed 1e-17)"
    % ((115 - 66) / math.sqrt(33), math.erfc((115 - 66) / math.sqrt(33)
                                             / math.sqrt(2)) / 2))
say("   sign test on 108/132: z = %.2f -> p ~ %.1e (printed 1e-13)"
    % ((108 - 66) / math.sqrt(33), math.erfc((108 - 66) / math.sqrt(33)
                                             / math.sqrt(2)) / 2))

# median / max |dev%|
say("")
say("## B2. section 10 median/max |dev%| on the 24-cell fresh grid only")
for j, k in enumerate(("CAND", "EPSR", "RED", "RED2")):
    ds = sorted(abs(r[7 + j][0]) for r in T4)
    med = (ds[11] + ds[12]) / 2
    say("   %-5s median|dev| = %.3f  max|dev| = %.3f  (the printed table is "
        "over all 132 cells, so only max is directly comparable: printed "
        "max %s)" % (k, med, ds[-1],
                     {"CAND": 8.253, "EPSR": 6.404, "RED": 2.168,
                      "RED2": 2.186}[k]))

# ---------------------------------------------------------------------------
say("")
say("## C. section 7.3 -- pooled chi2 of the per-bin elevation")
T73 = [(100, 150, 7, 173.2, 1.6), (100, 400, 6, 187.4, 2.0),
       (100, 600, 6, 239.4, 4.7), (200, 150, 7, 421.3, 9.7),
       (300, 150, 7, 650.8, 6.8), (400, 100, 8, 718.9, 3.0),
       (50, 400, 7, 67.1, 8.5), (8, 160, 8, 15.3, 14.6)]
say("   bins  %d   (printed 56)" % sum(r[2] for r in T73))
say("   chi2 vs constant P_lead = %.1f   (printed 2473.4)"
    % sum(r[3] for r in T73))
say("   chi2 vs lambda(t) (3.1) = %.1f   (printed 50.9)"
    % sum(r[4] for r in T73))

# ---------------------------------------------------------------------------
say("")
say("## D. section 7.2 -- ratio table: z consistency and the claimed scatter")
T72 = [(8, 160, 1.00166, 0.00120, +1.39), (50, 400, 0.99816, 0.00121, -1.52),
       (100, 150, 0.99941, 0.00122, -0.48), (100, 400, 0.99941, 0.00123, -0.48),
       (100, 600, 0.99959, 0.00127, -0.32), (200, 150, 0.99756, 0.00118, -2.06),
       (300, 150, 1.00314, 0.00111, +2.82), (400, 100, 1.00047, 0.00112, +0.42)]
nb = 0
for (b, c, r, s, z) in T72:
    zc = (r - 1) / s
    if abs(zc - z) > 0.02:
        nb += 1
        say("   ** z mismatch b=%d c=%d: computed %+.2f printed %+.2f"
            % (b, c, zc, z))
say("   z mismatches: %d" % nb)
rs = [r[2] for r in T72]
m = sum(rs) / len(rs)
sd = math.sqrt(sum((x - m) ** 2 for x in rs) / (len(rs) - 1))
sd0 = math.sqrt(sum((x - 1) ** 2 for x in rs) / len(rs))
msem = sum(r[3] for r in T72) / len(T72)
say("   scatter about the mean (ddof=1) = %.5f ; rms about 1.0 = %.5f ; "
    "mean sem = %.5f" % (sd, sd0, msem))
say("   -> scatter/sem = %.2f (about mean) or %.2f (about 1); the document "
    "states 'scatter across cells (0.0022) is about 1.8x the quoted sems'"
    % (sd / msem, sd0 / msem))

# ---------------------------------------------------------------------------
say("")
say("## E. section 8 -- chi2 = sum z^2, and the z of the continuum column")
T8 = [
    (50, 400, 65536, 0.051656, 0.000133, 0.051739, -0.44, 0.051621, +0.18,
     0.051640, +0.12),
    (100, 400, 65536, 0.060273, 0.000157, 0.060001, +1.23, 0.060132, +0.64,
     0.060181, +0.59),
    (100, 600, 65536, 0.056987, 0.000152, 0.057262, -1.29, 0.057293, -1.43,
     0.057305, -2.08),
    (200, 150, 65536, 0.091104, 0.000237, 0.091093, +0.03, 0.090918, +0.56,
     0.090995, +0.46),
    (300, 150, 65536, 0.101880, 0.000270, 0.101881, -0.00, 0.101494, +1.03,
     0.102041, -0.59),
    (400, 100, 65536, 0.120138, 0.000313, 0.120439, -0.68, 0.120005, +0.30,
     0.120277, -0.44),
]
say("   chi2 vs measured M-U (n'=(1-rho)n)      = %.2f  (printed 3.83)"
    % sum(r[6] ** 2 for r in T8))
say("   chi2 vs measured M-U (n'=(1-rho)(n+c))  = %.2f  (printed 3.93)"
    % sum(r[8] ** 2 for r in T8))
say("   chi2 vs continuum phi_U(c(1-rho))       = %.2f  (printed 5.47)"
    % sum(r[10] ** 2 for r in T8))
say("")
say("   continuum column: printed phi_U(c(1-rho)) vs the referee's own value,")
say("   and the z that follows from the M-CLUST sem alone:")
for (b, c, n, pc, sem, mA, zA, mB, zB, cont, zc) in T8:
    rho = 1 - (1 - c / n) ** b
    mine = float(F.phi_U(c * (1 - rho)))
    zz = (pc - cont) / sem
    say("      b=%3d c=%4d  printed cont %.6f  referee %.6f  (rel %+.2e)  "
        "z_from_sem %+.2f  printed z %+.2f"
        % (b, c, cont, mine, mine / cont - 1, zz, zc))
say("")
say("   the two 'measured M-U' columns use a COMBINED sem that the document")
say("   does not print (the M-U sems are absent), so those z cannot be")
say("   audited from the table alone; implied sem_diff:")
for (b, c, n, pc, sem, mA, zA, mB, zB, cont, zc) in T8:
    if zA != 0:
        say("      b=%3d c=%4d  implied sem_diff(A) = %.6f  (M-CLUST sem "
            "alone = %.6f)" % (b, c, abs(pc - mA) / abs(zA), sem))

# ---------------------------------------------------------------------------
say("")
say("## F. section 7.1 -- does the printed 'lambda model (3.1)' column fall")
say("##    inside the lambda(t) range of its own printed mass bin?")
say("##    (a value OUTSIDE that range proves the column is NOT the closed")
say("##     form (3.1) but the per-step EMPIRICAL pool ratio sum(we)/sum(wm))")


def lam(t, b, c, n, use_tc=True):
    p = c / n
    rho = 1 - (1 - p) ** b
    A = (1 - rho) / (1 - p)
    tc = t / (1 + p / (1 - rho)) if use_tc else t
    return (1 - t) / (A - tc)


T71 = [
    (100, 600, 65536, [((0.000, 0.005), 2.4951), ((0.005, 0.010), 2.5122),
                       ((0.010, 0.020), 2.5362), ((0.020, 0.035), 2.5721),
                       ((0.035, 0.060), 2.6174), ((0.060, 0.100), 2.6684)]),
    (400, 100, 65536, [((0.000, 0.005), 1.8481), ((0.010, 0.020), 1.8667),
                       ((0.035, 0.060), 1.9101), ((0.060, 0.100), 1.9434),
                       ((0.100, 0.180), 1.9797), ((0.180, 1.000), 2.0400)]),
]
for (b, c, n, bins) in T71:
    say("   b=%d c=%d n=%d  (P_lead=%.4f, lambda(0)=%.4f)"
        % (b, c, n, 1 / (1 - (1 - (1 - c / n) ** b)), lam(0, b, c, n)))
    for (lo, hi), val in bins:
        l0, l1 = lam(lo, b, c, n), lam(min(hi, 0.5), b, c, n)
        inside = (min(l0, l1) - 5e-3) <= val <= (max(l0, l1) + 5e-3)
        say("      bin [%.3f,%.3f]  printed %.4f   lambda range [%.4f,%.4f]  %s"
            % (lo, hi, val, l0, l1, "inside" if inside else "**OUTSIDE**"))

with open("ref2_tables.log", "w") as fh:
    fh.write("\n".join(OUT) + "\n")
print("\n[written] ref2_tables.log")
