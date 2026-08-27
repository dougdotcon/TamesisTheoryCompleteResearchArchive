#!/usr/bin/env python3
"""
Adversarial referee - extra independent checks (tasks 6, 7, 8 of the
referee mandate), written from scratch. Reuses only the loader logic
already established in referee_psd.py (same repo, same author -- not the
front's code).

1. "Morro largo" sanity check (task 6): fit a smooth log-log power-law
   background using PSD points OUTSIDE the claimed 5-10 Hz bump (2.0-5.3 Hz
   and 10.7-13.0 Hz), then check whether the actual PSD at ~7.83 Hz sits
   clearly ABOVE that extrapolated background (bump), and whether there is
   a genuine valley BELOW the background around 10-11 Hz (both signatures
   argue for a real localized feature, not a monotonic background/1/f
   trend or leakage artifact).

2. Harmonics check, done two ways (task 7): (a) reproduce the front's own
   "nearest-bin-to-14.000/21.000Hz" numbers exactly from the JSON, and
   (b) do a genuine windowed local-max search (same method used for the
   primary 5-10Hz peak) in the 12-25 Hz range, to check whether the
   nearest-bin approach is representative of the real spectral content
   nearby, or whether it is dodging much stronger, much narrower
   interference-like spectral lines.

3. Scale-invariance check (task 8): confirm that peak_freq_hz and the
   prominence ratio are IDENTICAL whether the raw int16 ADC counts are
   converted to volts (10/2**15 V/LSB, sourced from a paywalled paper
   abstract, unverifiable directly in this session) or left as raw counts
   -- i.e. that the one unverifiable literature-sourced parameter (the
   +-10V full-scale value) cannot possibly affect the pre-registered
   test's outcome, since Welch PSD peak-finding and the prominence ratio
   are invariant under any positive uniform rescaling of the signal.
"""
import glob
import os

import numpy as np
from scipy.signal import welch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")
SCALE = 10.0 / (2 ** 15)
FS = 1e6 / 3906.0
NPERSEG = 16385

SEGMENTS = ["2014-01-15", "2014-04-15", "2014-07-15"]
CHANNELS = ["NS", "EW"]


def load(segment, channel, as_counts=False):
    d = os.path.join(RAW, segment, channel)
    files = sorted(f for f in glob.glob(os.path.join(d, "*")) if not f.endswith("_info.txt"))
    assert len(files) == 24
    chunks = []
    for f in files:
        raw_bytes = np.fromfile(f, dtype=np.uint8)
        samples = np.frombuffer(raw_bytes.tobytes(), dtype="<i2").astype(np.float64)
        chunks.append(samples if as_counts else samples * SCALE)
    return np.concatenate(chunks)


def psd_of(x):
    return welch(x, fs=FS, window="hann", nperseg=NPERSEG, noverlap=NPERSEG // 2,
                 detrend="constant", scaling="density")


def background_bump_check():
    print("=== Task 6: morro largo vs smooth power-law background ===")
    for segment in SEGMENTS:
        for channel in CHANNELS:
            x = load(segment, channel)
            freqs, psd = psd_of(x)
            bg_mask = ((freqs >= 2.0) & (freqs <= 5.3)) | ((freqs >= 10.7) & (freqs <= 13.0))
            coeffs = np.polyfit(np.log(freqs[bg_mask]), np.log(psd[bg_mask]), deg=1)
            pred = lambda f: np.exp(np.polyval(coeffs, np.log(f)))

            idx_peak = int(np.argmin(np.abs(freqs - 7.83)))
            excess = psd[idx_peak] / pred(freqs[idx_peak])

            val_mask = (freqs >= 9.5) & (freqs <= 11.0)
            idx_val = np.where(val_mask)[0][int(np.argmin(psd[val_mask]))]
            val_ratio = psd[idx_val] / pred(freqs[idx_val])

            print(f"  {segment}/{channel}: slope={coeffs[0]:.3f}  "
                  f"excess@7.83Hz={excess:.3f}x background  "
                  f"valley@{freqs[idx_val]:.3f}Hz={val_ratio:.3f}x background")
    print()


def harmonics_windowed_check():
    print("=== Task 7: harmonics context, nearest-bin vs windowed local-max ===")
    for segment in SEGMENTS:
        for channel in CHANNELS:
            x = load(segment, channel)
            freqs, psd = psd_of(x)
            mask5_10 = (freqs >= 5) & (freqs <= 10)
            idx1 = np.where(mask5_10)[0][int(np.argmax(psd[mask5_10]))]
            mode1_power = psd[idx1]

            i14 = int(np.argmin(np.abs(freqs - 14.0)))
            i21 = int(np.argmin(np.abs(freqs - 21.0)))
            nearest_bin_14 = psd[i14] / mode1_power
            nearest_bin_21 = psd[i21] / mode1_power

            m12_16 = (freqs >= 12) & (freqs <= 16)
            idx_w14 = np.where(m12_16)[0][int(np.argmax(psd[m12_16]))]
            windowed_14 = psd[idx_w14] / mode1_power

            m19_23 = (freqs >= 19) & (freqs <= 23)
            idx_w21 = np.where(m19_23)[0][int(np.argmax(psd[m19_23]))]
            windowed_21 = psd[idx_w21] / mode1_power

            print(f"  {segment}/{channel}: mode1_power={mode1_power:.4e}")
            print(f"    nearest-bin-14.0Hz ratio={nearest_bin_14:.2f}x   "
                  f"windowed-max-12-16Hz ratio={windowed_14:.2f}x at f={freqs[idx_w14]:.4f}Hz")
            print(f"    nearest-bin-21.0Hz ratio={nearest_bin_21:.2f}x   "
                  f"windowed-max-19-23Hz ratio={windowed_21:.2f}x at f={freqs[idx_w21]:.4f}Hz")
    print()


def scale_invariance_check():
    print("=== Task 8: scale-invariance of peak_freq / prominence to the +-10V assumption ===")
    for segment in SEGMENTS:
        for channel in CHANNELS:
            x_volts = load(segment, channel, as_counts=False)
            x_counts = load(segment, channel, as_counts=True)
            f_v, p_v = psd_of(x_volts)
            f_c, p_c = psd_of(x_counts)

            def peak_prom(freqs, psd):
                mask = (freqs >= 5) & (freqs <= 10)
                idx = np.where(mask)[0][int(np.argmax(psd[mask]))]
                pf = freqs[idx]
                nb = (freqs >= pf - 1) & (freqs <= pf + 1)
                med = np.median(psd[nb])
                return pf, psd[idx] / med

            pf_v, prom_v = peak_prom(f_v, p_v)
            pf_c, prom_c = peak_prom(f_c, p_c)
            same = (abs(pf_v - pf_c) < 1e-9) and (abs(prom_v - prom_c) < 1e-9)
            print(f"  {segment}/{channel}: volts(peak={pf_v:.4f},prom={prom_v:.4f}) "
                  f"vs counts(peak={pf_c:.4f},prom={prom_c:.4f})  identical={same}")
    print()


if __name__ == "__main__":
    background_bump_check()
    harmonics_windowed_check()
    scale_invariance_check()
