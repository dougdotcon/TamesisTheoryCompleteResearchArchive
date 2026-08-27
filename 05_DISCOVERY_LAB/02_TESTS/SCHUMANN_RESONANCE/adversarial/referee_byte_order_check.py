#!/usr/bin/env python3
"""
Adversarial referee check #1: independent byte-order determination.

Written from scratch by the adversarial reviewer session, WITHOUT reading
analysis/compute_psd.py, analysis/download_segments.py, or
analysis/range_zip.py first (per referee mandate).

Loads two raw binary files directly from data/raw/, decodes them BOTH as
little-endian and big-endian int16, and reports summary statistics plus
one additional, independent diagnostic (lag-1 autocorrelation) not
mentioned in the front's provenance writeup, to check whether the
LE-vs-BE conclusion is robust to a criterion the front did not already
pick.
"""
import numpy as np

SCALE = 10.0 / (2 ** 15)  # V/LSB, +-10V rail, 16-bit signed (1 sign + 15 mag)

FILES = [
    "data/raw/2014-01-15/NS/smplGRTU1_sensor_0_1401150054",
    "data/raw/2014-07-15/EW/smplGRTU1_sensor_1_1407150057",
]


def lag1_autocorr(x):
    x = x - x.mean()
    return float(np.sum(x[:-1] * x[1:]) / np.sum(x[:-1] ** 2))


def report(path):
    raw_bytes = np.fromfile(path, dtype=np.uint8)
    le = np.frombuffer(raw_bytes.tobytes(), dtype="<i2")
    be = np.frombuffer(raw_bytes.tobytes(), dtype=">i2")

    print(f"=== {path} ===")
    print(f"total bytes: {raw_bytes.size}, samples: {le.size}")
    for name, ints in [("LE", le), ("BE", be)]:
        v = ints.astype(np.float64) * SCALE
        frac_extreme = np.mean(
            (ints.astype(np.int64) == -32768) | (ints.astype(np.int64) == 32767)
        )
        print(
            f"  {name}: mean={v.mean(): .6f} V  std={v.std(): .6f} V  "
            f"min={v.min(): .6f} V  max={v.max(): .6f} V  "
            f"frac_at_int16_extreme={frac_extreme:.6%}  "
            f"lag1_autocorr={lag1_autocorr(v):.4f}"
        )
    print(f"  theoretical uniform-noise std over +-10V rail: 10/sqrt(3) = {10/np.sqrt(3):.6f} V")
    print()


if __name__ == "__main__":
    for f in FILES:
        report(f)
