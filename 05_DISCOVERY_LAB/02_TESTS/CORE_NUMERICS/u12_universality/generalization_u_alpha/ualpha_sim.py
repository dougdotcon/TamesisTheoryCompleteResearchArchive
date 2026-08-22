"""Front C (u12-generalization-u-alpha, wave 3): pre-registered runs B1-B2.

Finite-n simulator (n = 2^15) for the mechanism family of
METHODOLOGY_NOTE.md: f = pi (uniform permutation) except on the
rerouted set R, where f is redirected per mechanism. Cyclic points are
counted as the distinct image of f^(2^15) (iterated squaring; method
independently validated by the wave-2 adversarial front). Compared
against the targets DERIVED in DERIVATIONS.md and tabulated in
predictions.json BEFORE this script was run.

Batteries, seeds, N and acceptance criteria pre-registered in
METHODOLOGY_NOTE.md (B1: mean curves, SeedSequence(20260822), N=3000;
B2: conditional K=1, SeedSequence(84206), N=20000). Single execution.
"""
import json
import math
import os
import sys
import time

import numpy as np
from scipy.stats import chi2

N = 32768
LOG2N = 15
B = 8            # M-CLUST block length
P = 0.5          # M-MIX atom
TBITS = 31       # M-INTRA power range (declared bias <= n/2^31)
C_GRID = [0.5, 2.0, 10.0, 40.0, 160.0]
MECHS = ["M-U", "M-CLUST8", "M-MIX50", "M-PREV", "M-INTRA"]
N_MEAN = 3000
N_K1 = 20000
HERE = os.path.dirname(os.path.abspath(__file__))


def cyclic_fraction(f):
    """#cyclic points of f / n via distinct image of f^(2^15)."""
    F = f
    for _ in range(LOG2N):
        F = F[F]
    mask = np.zeros(N, dtype=bool)
    mask[F] = True
    return mask.sum() / N


def pi_power_apply(pi, idx, T):
    """Return pi^{T[j]}(idx[j]) via binary exponentiation (TBITS bits)."""
    dest = idx.copy()
    Pk = pi
    for k in range(TBITS):
        sel = (T >> k) & 1 == 1
        if sel.any():
            dest[sel] = Pk[dest[sel]]
        if k < TBITS - 1:
            Pk = Pk[Pk]
    return dest


def build_f(mech, c, rng, force_K1=False):
    pi = rng.permutation(N).astype(np.int32)
    f = pi.copy()
    if force_K1:
        R = np.array([rng.integers(0, N)], dtype=np.int32)
    elif mech == "M-CLUST8":
        seeds = np.flatnonzero(rng.random(N) < c / N).astype(np.int32)
        blocks = [seeds]
        cur = seeds
        for _ in range(B - 1):
            cur = pi[cur]
            blocks.append(cur)
        R = np.unique(np.concatenate(blocks)) if seeds.size else seeds
    else:
        R = np.flatnonzero(rng.random(N) < c / N).astype(np.int32)
    if R.size == 0:
        return f
    if mech in ("M-U", "M-CLUST8"):
        f[R] = rng.integers(0, N, R.size, dtype=np.int32)
    elif mech == "M-MIX50":
        dest = rng.integers(0, N, R.size, dtype=np.int32)
        coin = rng.random(R.size) < P
        dest[coin] = R[coin]
        f[R] = dest
    elif mech == "M-PREV":
        inv = np.empty(N, dtype=np.int32)
        inv[pi] = np.arange(N, dtype=np.int32)
        f[R] = inv[R]
    elif mech == "M-INTRA":
        T = rng.integers(0, 1 << TBITS, R.size, dtype=np.int64)
        f[R] = pi_power_apply(pi, R, T)
    else:
        raise ValueError(mech)
    return f


def run_cell(mech, c, n_real, seed_seq, force_K1=False):
    rng = np.random.default_rng(seed_seq)
    vals = np.empty(n_real)
    for i in range(n_real):
        vals[i] = cyclic_fraction(build_f(mech, c, rng, force_K1))
    m = vals.mean()
    sem = vals.std(ddof=1) / math.sqrt(n_real)
    return m, sem


def main():
    t0 = time.time()
    with open(os.path.join(HERE, "predictions.json")) as fh:
        pred = json.load(fh)
    log = open(os.path.join(HERE, "ualpha_sim.log"), "w")

    def say(msg):
        print(msg, flush=True)
        log.write(msg + "\n")
        log.flush()

    say("# u12-generalization-u-alpha B1-B2 | n=%d | started %s"
        % (N, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
    out = {"n": N, "runs": {"B1": {}, "B2": {}}, "criteria": {}}

    # ---------------- B1: mean curves ----------------
    spawns = np.random.SeedSequence(20260822).spawn(len(MECHS) * len(C_GRID))
    for mi, mech in enumerate(MECHS):
        rows = []
        for ci, c in enumerate(C_GRID):
            ss = spawns[mi * len(C_GRID) + ci]
            m, sem = run_cell(mech, c, N_MEAN, ss)
            tgt = pred["targets"].get(mech, {}).get(str(c))
            z = (m - tgt) / sem if tgt is not None else None
            rows.append(dict(c=c, phi=m, sem=sem, target=tgt, z=z))
            say("[B1] %-8s c=%-5g phi=%.6f+-%.6f%s" % (
                mech, c, m, sem,
                "" if tgt is None else " target=%.6f z=%+.2f" % (tgt, z)))
        out["runs"]["B1"][mech] = rows

    # ---------------- B2: conditional K=1 ----------------
    k1_mechs = ["M-U", "M-MIX50", "M-PREV", "M-INTRA"]
    spawns = np.random.SeedSequence(84206).spawn(len(k1_mechs))
    for mech, ss in zip(k1_mechs, spawns):
        m, sem = run_cell(mech, None, N_K1, ss, force_K1=True)
        tgt = pred["K1_exact"][mech]
        z = (m - tgt) / sem
        out["runs"]["B2"][mech] = dict(phi1=m, sem=sem, target=tgt, z=z)
        say("[B2] %-8s K=1 phi1=%.6f+-%.6f target=%.6f z=%+.2f" % (
            mech, m, sem, tgt, z))

    # ---------------- criteria ----------------
    # control lane: M-U per-c pass
    mu_rows = {r["c"]: r for r in out["runs"]["B1"]["M-U"]}
    bias_limited = [c for c in C_GRID if abs(mu_rows[c]["z"]) >= 4]
    say("[CTRL] bias-limited c cells (M-U |z|>=4): %s" % (bias_limited or "none"))

    c1 = {}
    for mech in ["M-U", "M-CLUST8", "M-MIX50", "M-PREV"]:
        rows = out["runs"]["B1"][mech]
        zs, excl, band_ok = [], [], []
        for r in rows:
            if r["c"] in bias_limited:
                excl.append(r["c"])
                continue
            ok = abs(r["z"]) < 4
            if mech == "M-CLUST8" and r["c"] in (40.0, 160.0) and not ok:
                ok = abs(r["phi"] - r["target"]) / r["target"] < 2 * B * r["c"] / N
                if ok:
                    band_ok.append(r["c"])
            zs.append((r["c"], r["z"], ok))
        chi = sum(z * z for _, z, _ in zs)
        dof = len(zs)
        pv = float(chi2.sf(chi, dof)) if dof else None
        cells_ok = all(ok for _, _, ok in zs)
        passed = bool(cells_ok and (pv is None or pv >= 0.01))
        c1[mech] = dict(chi2=chi, dof=dof, p=pv, cells_ok=cells_ok,
                        excluded_bias_limited=excl, band_accepted=band_ok,
                        passed=passed)
        say("[C1] %-8s chi2=%.2f dof=%d p=%s cells_ok=%s band=%s -> %s" % (
            mech, chi, dof, "n/a" if pv is None else "%.4f" % pv,
            cells_ok, band_ok or "-", "PASS" if passed else "FAIL"))
    out["criteria"]["C1"] = c1

    c2 = {}
    for mech, r in out["runs"]["B2"].items():
        ok = abs(r["z"]) < 4
        c2[mech] = dict(z=r["z"], passed=bool(ok))
        say("[C2] %-8s K=1 z=%+.2f -> %s" % (mech, r["z"], "PASS" if ok else "FAIL"))
    out["criteria"]["C2"] = c2

    c3 = {}
    for mech in MECHS:
        rows = {r["c"]: r for r in out["runs"]["B1"][mech]}
        r10, r160 = rows[10.0], rows[160.0]
        a_hat = math.log(r10["phi"] / r160["phi"]) / math.log(16.0)
        sig = math.sqrt((r10["sem"] / r10["phi"]) ** 2
                        + (r160["sem"] / r160["phi"]) ** 2) / math.log(16.0)
        a_tgt = pred["slope_targets"][mech]
        ok = abs(a_hat - a_tgt) < max(0.06, 3 * sig)
        c3[mech] = dict(alpha_hat=a_hat, sigma=sig, alpha_target=a_tgt,
                        passed=bool(ok))
        say("[C3] %-8s alpha_hat=%.4f+-%.4f target=%.4f -> %s" % (
            mech, a_hat, sig, a_tgt, "PASS" if ok else "FAIL"))
    out["criteria"]["C3"] = c3

    # M-INTRA descriptive comparison vs heuristic (report-only)
    for c in [10.0, 40.0, 160.0]:
        hv = pred["M-INTRA_heuristic_phi"][str(c)]
        mv = {r["c"]: r for r in out["runs"]["B1"]["M-INTRA"]}[c]["phi"]
        say("[INTRA-HEUR report-only] c=%g phi_MC=%.4f heuristic=%.4f ratio=%.3f"
            % (c, mv, hv, mv / hv))

    ok_all = (all(v["passed"] for v in c1.values())
              and all(v["passed"] for v in c2.values())
              and all(v["passed"] for v in c3.values()))
    out["all_passed"] = bool(ok_all)
    out["bias_limited_cells"] = bias_limited
    say("# ALL PRE-REGISTERED CRITERIA PASSED: %s" % ok_all)
    say("# wall time: %.1f s" % (time.time() - t0))
    with open(os.path.join(HERE, "ualpha_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    say("# saved ualpha_results.json")
    log.close()


if __name__ == "__main__":
    main()
