"""Checkpointed computation of M* for the adversarial reproduction.

Modes:
  primary <k> <i0> <i1>   compute M* for windows i0..i1-1 (in the locked
                          sorted-enumeration order) of height k; results are
                          written into slices_adv/height_<k>.npy (NaN = not
                          yet computed). Re-running a done slice is a no-op.
  calibrate <k>           my own grid-bias calibration for height k on the
                          disposable band: per window, M*_2048 on the
                          2048-point grid and M*_512 on its j%4==0 subgrid
                          (identical to the locked 512 grid); diffs written
                          to slices_adv/cal_height_<k>.json.
  bench <k> <n>           time n windows of height k (windows are the FIRST
                          n of the enumeration; results are SAVED to the
                          checkpoint, not thrown away).

All foreground, single process.
"""

import json
import os
import sys
import time

import numpy as np

from rs_zeta_adv import (ZEvaluator, HEIGHTS, M_PER_HEIGHT, N_CAL,
                         primary_starts, calibration_starts, TWO_PI)

SLICE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "slices_adv")
os.makedirs(SLICE_DIR, exist_ok=True)


def _ckpt_path(k):
    return os.path.join(SLICE_DIR, f"height_{k}.npy")


def _load_ckpt(k):
    path = _ckpt_path(k)
    if os.path.exists(path):
        return np.load(path)
    arr = np.full(M_PER_HEIGHT[k], np.nan)
    return arr


def _save_ckpt(k, arr):
    tmp = os.path.join(SLICE_DIR, f"height_{k}.tmp.npy")
    np.save(tmp, arr)
    os.replace(tmp, _ckpt_path(k))


def run_primary_slice(k, i0, i1, batch_windows=None):
    starts = primary_starts(k)
    arr = _load_ckpt(k)
    ev = ZEvaluator()
    t_begin = time.time()
    n_done = 0
    # batch several windows per ev.z call to amortize overhead at low heights
    if batch_windows is None:
        batch_windows = max(1, int(2_000_000 // np.sqrt(HEIGHTS[k] / TWO_PI) // 512)) or 1
        batch_windows = max(1, min(batch_windows, 64))
    todo = [i for i in range(i0, i1) if np.isnan(arr[i])]
    step = TWO_PI / 512
    grid_offsets = step * np.arange(512)
    for b0 in range(0, len(todo), batch_windows):
        idx = todo[b0:b0 + batch_windows]
        tgrid = (starts[idx][:, None] + grid_offsets[None, :]).ravel()
        z = ev.z(tgrid).reshape(len(idx), 512)
        m = np.max(np.log(np.abs(z)), axis=1)
        arr[idx] = m
        n_done += len(idx)
        if time.time() - t_begin > 30 or b0 + batch_windows >= len(todo):
            _save_ckpt(k, arr)
            t_begin = time.time()
    _save_ckpt(k, arr)
    return n_done


def run_calibration(k):
    ev = ZEvaluator()
    starts = calibration_starts(k)
    step = TWO_PI / 2048
    grid_offsets = step * np.arange(2048)
    diffs = []
    t0 = time.time()
    for s in starts:
        tgrid = s + grid_offsets
        z = ev.z(tgrid)
        logabs = np.log(np.abs(z))
        m2048 = float(np.max(logabs))
        m512 = float(np.max(logabs[::4]))  # j%4==0 == locked 512-grid
        diffs.append(m2048 - m512)
    diffs = np.array(diffs)
    c = (16.0 / 15.0) * float(np.mean(diffs))
    ep = (16.0 / 15.0) * float(np.std(diffs, ddof=1)) / np.sqrt(len(diffs))
    out = {"k": k, "T": HEIGHTS[k], "n_cal": len(diffs),
           "mean_diff_2048_512": float(np.mean(diffs)),
           "c_T": c, "EP_c_T": ep,
           "diffs": diffs.tolist(),
           "wallclock_s": time.time() - t0}
    with open(os.path.join(SLICE_DIR, f"cal_height_{k}.json"), "w") as f:
        json.dump(out, f, indent=2)
    return out


def main():
    mode = sys.argv[1]
    if mode == "primary":
        k, i0, i1 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        t0 = time.time()
        n = run_primary_slice(k, i0, i1)
        dt = time.time() - t0
        arr = _load_ckpt(k)
        done = int(np.sum(~np.isnan(arr)))
        print(f"height k={k} T={HEIGHTS[k]:.0e}: slice [{i0},{i1}) "
              f"computed {n} new windows in {dt:.1f}s "
              f"({dt/max(n,1):.4f} s/window); total done {done}/{M_PER_HEIGHT[k]}",
              flush=True)
    elif mode == "calibrate":
        k = int(sys.argv[2])
        out = run_calibration(k)
        print(f"calibration k={k}: c_T={out['c_T']:+.6f} "
              f"EP={out['EP_c_T']:.6f} n={out['n_cal']} "
              f"({out['wallclock_s']:.1f}s)", flush=True)
    elif mode == "bench":
        k, n = int(sys.argv[2]), int(sys.argv[3])
        t0 = time.time()
        run_primary_slice(k, 0, n)
        dt = time.time() - t0
        print(f"bench k={k}: {n} windows in {dt:.2f}s "
              f"= {dt/n:.4f} s/window "
              f"=> full M={M_PER_HEIGHT[k]} ~ {dt/n*M_PER_HEIGHT[k]:.0f}s",
              flush=True)
    else:
        raise SystemExit(f"unknown mode {mode}")


if __name__ == "__main__":
    main()
