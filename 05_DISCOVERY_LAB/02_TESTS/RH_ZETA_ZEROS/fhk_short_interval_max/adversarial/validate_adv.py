"""Validation of the adversarial Z(t) evaluator BEFORE any real test window.

Gates (declared before running):
  V1  |zeta(1/2)| anchor via mpmath (documented; evaluator not used at t=0).
  V2  |Z(t)| vs |zeta(1/2+it)| (mpmath, dps 30) at t in {50, 100, 500, 1000}:
      max abs diff <= 5e-3 (small-t regime, outside test domain; qualitative).
  V3  first zero: bisection root of my Z on [14.0, 14.3] within 5e-3 of
      14.1347251417.
  V4  cross-checks vs mpmath.siegelz (dps 30), seed 424242 (unrelated to the
      test seeds), bands and tolerances:
        t ~ 2e3, 1e4, 1e5, 1e6 : |dZ| <= 5e-4
        t ~ 1e7, 1e8           : |dZ| <= 1e-3
        t ~ 1e9, 1e10, 2.05e10 : |dZ| <= 1e-3
      (double-precision phase noise ~1e-5 rad at 1e10; C0-only bound
      0.053*(t/2pi)^-0.75).
All results written to validation_adv.json / validation_adv.log.
"""

import json
import time

import mpmath
import numpy as np

from rs_zeta_adv import ZEvaluator

LOG = []


def log(msg):
    print(msg, flush=True)
    LOG.append(msg)


def main():
    t_start = time.time()
    ev = ZEvaluator()
    results = {"validated_before_real_windows": True}
    all_pass = True

    # V1: zeta(1/2) anchor
    mpmath.mp.dps = 30
    z_half = mpmath.zeta(mpmath.mpf("0.5"))
    log(f"V1 zeta(1/2) = {z_half}  |zeta(1/2)| = {abs(z_half)}")
    results["V1_zeta_half"] = str(z_half)

    # V2: |Z(t)| vs |zeta(1/2+it)| at moderate t
    v2 = []
    for t in [50.0, 100.0, 500.0, 1000.0]:
        zeta_val = mpmath.zeta(mpmath.mpc("0.5", mpmath.mpf(t)))
        target = float(abs(zeta_val))
        mine = float(abs(ev.z(np.array([t]))[0]))
        d = abs(mine - target)
        v2.append({"t": t, "abs_zeta_mpmath": target, "abs_Z_mine": mine,
                   "abs_diff": d})
        log(f"V2 t={t:8.1f}  |zeta|={target:.10f}  |Z|={mine:.10f}  "
            f"diff={d:.3e}")
    v2_pass = max(r["abs_diff"] for r in v2) <= 5e-3
    results["V2"] = {"rows": v2, "tol": 5e-3, "pass": bool(v2_pass)}
    all_pass &= v2_pass
    log(f"V2 PASS={v2_pass}")

    # V3: first zero by bisection on my Z
    lo, hi = 14.0, 14.3
    zlo = float(ev.z(np.array([lo]))[0])
    zhi = float(ev.z(np.array([hi]))[0])
    assert zlo * zhi < 0, "no sign change bracketing first zero"
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        zm = float(ev.z(np.array([mid]))[0])
        if zlo * zm <= 0:
            hi = mid
        else:
            lo, zlo = mid, zm
    root = 0.5 * (lo + hi)
    ref = 14.1347251417
    v3_pass = abs(root - ref) <= 5e-3
    results["V3"] = {"root": root, "reference": ref,
                     "abs_diff": abs(root - ref), "tol": 5e-3,
                     "pass": bool(v3_pass)}
    all_pass &= v3_pass
    log(f"V3 first zero: mine={root:.7f} ref={ref} "
        f"diff={abs(root-ref):.2e} PASS={v3_pass}")

    # V4: siegelz cross-checks
    bands = [
        (2e3, 4, 5e-4), (1e4, 4, 5e-4), (1e5, 4, 5e-4), (1e6, 4, 5e-4),
        (1e7, 3, 1e-3), (1e8, 3, 1e-3),
        (1e9, 2, 1e-3), (1e10, 2, 1e-3), (2.05e10, 1, 1e-3),
    ]
    rng = np.random.default_rng(424242)
    v4 = []
    v4_pass = True
    for base, npts, tol in bands:
        ts = base + rng.uniform(0.0, 100.0, npts)
        t0 = time.time()
        mine = ev.z(ts)
        for t, zm in zip(ts, mine):
            ref_val = float(mpmath.siegelz(mpmath.mpf(t)))
            d = abs(float(zm) - ref_val)
            ok = d <= tol
            v4_pass &= ok
            v4.append({"t": float(t), "siegelz": ref_val, "Z_mine": float(zm),
                       "abs_diff": d, "tol": tol, "pass": bool(ok)})
            log(f"V4 t={t:.4f}  siegelz={ref_val:+.8f}  "
                f"mine={float(zm):+.8f}  diff={d:.3e}  tol={tol}  ok={ok}")
        log(f"   band {base:.3g} done in {time.time()-t0:.1f}s")
    results["V4"] = {"rows": v4, "pass": bool(v4_pass)}
    all_pass &= v4_pass
    log(f"V4 PASS={v4_pass}")

    results["ALL_PASS"] = bool(all_pass)
    results["wallclock_s"] = time.time() - t_start
    with open("validation_adv.json", "w") as f:
        json.dump(results, f, indent=2)
    with open("validation_adv.log", "w") as f:
        f.write("\n".join(LOG) + "\n")
    log(f"ALL_PASS={all_pass}  ({results['wallclock_s']:.1f}s)")


if __name__ == "__main__":
    main()
