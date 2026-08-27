#!/usr/bin/env python3
"""
Adversarial referee reexecution of DISC-SCHUMANN-RESONANCE-001.

Written from scratch by the adversarial reviewer session (separate from the
agent that produced RESULTS_PRIMARY.md), per 00_GOVERNANCE/AGENTS.md
"Separacao de papeis". Does NOT import or read
analysis/{compute_psd,download_segments,range_zip}.py.

Loads the already-downloaded raw binary files under data/raw/<segment>/<ch>/,
decodes as little-endian int16, scales to volts, concatenates chronologically,
computes Welch PSD exactly per PREREGISTRATION.md Section 4, and reports:
  - dominant 5-10 Hz peak frequency
  - whether it falls in the locked tolerance band [6.70, 8.35] Hz
  - prominence ratio (peak power / median power in +-1 Hz neighborhood)
  - power near 14 Hz / 21 Hz (harmonics context)
  - a sensitivity check on nperseg (round vs floor vs ceil vs a materially
    different alternative window length)
"""
import glob
import json
import os

import numpy as np
from scipy.signal import welch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")

SCALE = 10.0 / (2 ** 15)  # V/LSB
SAMPLING_PERIOD_USEC = 3906.0  # confirmed by direct read of all 144 _info.txt
FS = 1e6 / SAMPLING_PERIOD_USEC

SEGMENTS = ["2014-01-15", "2014-04-15", "2014-07-15"]
CHANNELS = {"NS": "NS", "EW": "EW"}

TOL_LOW, TOL_HIGH = 6.70, 8.35
SEARCH_LOW, SEARCH_HIGH = 5.0, 10.0


def load_channel_segment(segment, channel):
    d = os.path.join(RAW, segment, channel)
    files = sorted(
        f for f in glob.glob(os.path.join(d, "*")) if not f.endswith("_info.txt")
    )
    assert len(files) == 24, f"expected 24 hourly files, got {len(files)} in {d}"
    chunks = []
    for f in files:
        raw_bytes = np.fromfile(f, dtype=np.uint8)
        samples = np.frombuffer(raw_bytes.tobytes(), dtype="<i2").astype(np.float64)
        chunks.append(samples * SCALE)
    x = np.concatenate(chunks)
    return x


def dominant_peak_and_prominence(freqs, psd, lo, hi):
    mask = (freqs >= lo) & (freqs <= hi)
    idx_local = np.argmax(psd[mask])
    idx_global = np.where(mask)[0][idx_local]
    peak_freq = freqs[idx_global]
    peak_power = psd[idx_global]

    nb_mask = (freqs >= peak_freq - 1.0) & (freqs <= peak_freq + 1.0) & (~(
        np.arange(len(freqs)) == idx_global
    ))
    neighborhood_median = np.median(psd[nb_mask])
    prominence = peak_power / neighborhood_median
    return peak_freq, peak_power, prominence, neighborhood_median


def genuine_local_maxima_in_band(freqs, psd, lo, hi):
    """bins strictly greater than both immediate neighbors, inside [lo,hi]"""
    maxima = []
    for i in range(1, len(freqs) - 1):
        if lo <= freqs[i] <= hi and psd[i] > psd[i - 1] and psd[i] > psd[i + 1]:
            maxima.append((float(freqs[i]), float(psd[i])))
    return maxima


def harmonics_check(freqs, psd, mode1_power):
    out = {}
    for label, center in [("mode2_14hz", 14.0), ("mode3_21hz", 21.0)]:
        mask = (freqs >= center - 1.0) & (freqs <= center + 1.0)
        p = psd[mask].max()
        out[label] = {"peak_power": float(p), "ratio_to_mode1": float(p / mode1_power)}
    return out


def analyze(segment, channel, nperseg_mode="round"):
    x = load_channel_segment(segment, channel)
    n_expected = 24 * 921600
    assert x.size == n_expected, f"{segment}/{channel}: got {x.size} samples, expected {n_expected}"

    raw_np = 64 * FS
    if nperseg_mode == "round":
        nperseg = int(round(raw_np))
    elif nperseg_mode == "floor":
        nperseg = int(np.floor(raw_np))
    elif nperseg_mode == "ceil":
        nperseg = int(np.ceil(raw_np))
    else:
        raise ValueError(nperseg_mode)

    noverlap = nperseg // 2

    freqs, psd = welch(
        x,
        fs=FS,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        detrend="constant",
        scaling="density",
    )

    n_welch_segments = 1 + (x.size - nperseg) // (nperseg - noverlap)

    peak_freq, peak_power, prominence, nb_median = dominant_peak_and_prominence(
        freqs, psd, SEARCH_LOW, SEARCH_HIGH
    )
    in_band = TOL_LOW <= peak_freq <= TOL_HIGH
    maxima_in_band = genuine_local_maxima_in_band(freqs, psd, TOL_LOW, TOL_HIGH)
    harmonics = harmonics_check(freqs, psd, peak_power)

    return {
        "segment": segment,
        "channel": channel,
        "nperseg_mode": nperseg_mode,
        "nperseg": nperseg,
        "fs": FS,
        "n_samples": int(x.size),
        "n_welch_segments_avg": int(n_welch_segments),
        "freq_resolution_hz": float(freqs[1] - freqs[0]),
        "peak_freq_hz": float(peak_freq),
        "peak_power": float(peak_power),
        "in_tolerance_band": bool(in_band),
        "prominence": float(prominence),
        "neighborhood_median_power": float(nb_median),
        "genuine_local_maxima_in_band": maxima_in_band,
        "n_genuine_local_maxima_in_band": len(maxima_in_band),
        "harmonics_check": harmonics,
        "freqs": freqs,
        "psd": psd,
    }


def shape_profile(freqs, psd, lo=5.0, hi=10.0, step=0.5):
    """Coarse PSD shape sampled every `step` Hz, for eyeballing 'morro largo'."""
    prof = []
    f = lo
    while f <= hi + 1e-9:
        idx = int(np.argmin(np.abs(freqs - f)))
        prof.append((round(freqs[idx], 4), float(psd[idx])))
        f += step
    return prof


def main():
    print(f"FS = {FS!r}")
    print(f"nperseg (round) = {int(round(64*FS))}, (floor) = {int(np.floor(64*FS))}, (ceil) = {int(np.ceil(64*FS))}")
    print()

    results = {}
    for segment in SEGMENTS:
        for channel in CHANNELS:
            key = f"{segment}/{channel}"
            print(f"=== {key} (nperseg=round, primary) ===")
            r = analyze(segment, channel, nperseg_mode="round")
            results[key] = r
            print(
                f"  peak_freq={r['peak_freq_hz']:.4f} Hz  in_band={r['in_tolerance_band']}  "
                f"prominence={r['prominence']:.3f}x  n_welch_avg={r['n_welch_segments_avg']}  "
                f"freq_res={r['freq_resolution_hz']:.5f} Hz"
            )
            print(f"  genuine local maxima in [{TOL_LOW},{TOL_HIGH}]: {r['genuine_local_maxima_in_band']}")
            print(f"  harmonics: {r['harmonics_check']}")
            print(f"  shape profile 5-10Hz (0.5Hz steps): {shape_profile(r['freqs'], r['psd'])}")
            print()

    # nperseg sensitivity check: alternative modes + a materially different
    # window length (32s instead of 64s) to see if any verdict flips
    print("=== nperseg sensitivity check ===")
    sensitivity = {}
    for segment in SEGMENTS:
        for channel in CHANNELS:
            key = f"{segment}/{channel}"
            sensitivity[key] = {}
            for mode in ["floor", "ceil"]:
                r = analyze(segment, channel, nperseg_mode=mode)
                sensitivity[key][mode] = {
                    "nperseg": r["nperseg"],
                    "peak_freq_hz": r["peak_freq_hz"],
                    "in_band": r["in_tolerance_band"],
                    "prominence": r["prominence"],
                }
                print(
                    f"  {key} [{mode}, nperseg={r['nperseg']}]: peak={r['peak_freq_hz']:.4f} Hz "
                    f"in_band={r['in_tolerance_band']} prominence={r['prominence']:.3f}x"
                )
            # materially different: 32s window (half length -> ~2x freq resolution loss, ~2x more averaging)
            x = load_channel_segment(segment, channel)
            nperseg32 = int(round(32 * FS))
            noverlap32 = nperseg32 // 2
            freqs32, psd32 = welch(
                x, fs=FS, window="hann", nperseg=nperseg32, noverlap=noverlap32,
                detrend="constant", scaling="density",
            )
            pf, pp, prom, nbm = dominant_peak_and_prominence(freqs32, psd32, SEARCH_LOW, SEARCH_HIGH)
            sensitivity[key]["32s_window"] = {
                "nperseg": nperseg32, "peak_freq_hz": float(pf),
                "in_band": bool(TOL_LOW <= pf <= TOL_HIGH), "prominence": float(prom),
            }
            print(
                f"  {key} [32s window, nperseg={nperseg32}]: peak={pf:.4f} Hz "
                f"in_band={TOL_LOW <= pf <= TOL_HIGH} prominence={prom:.3f}x"
            )
    print()

    # Save a serializable summary (drop the raw freq/psd arrays)
    summary = {}
    for key, r in results.items():
        r2 = {k: v for k, v in r.items() if k not in ("freqs", "psd")}
        r2["shape_profile_5_10hz"] = shape_profile(r["freqs"], r["psd"])
        summary[key] = r2
    summary["nperseg_sensitivity"] = sensitivity
    summary["fs"] = FS
    summary["nperseg_round"] = int(round(64 * FS))
    summary["nperseg_floor"] = int(np.floor(64 * FS))
    summary["nperseg_ceil"] = int(np.ceil(64 * FS))

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "referee_results.json")
    with open(out_path, "w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
