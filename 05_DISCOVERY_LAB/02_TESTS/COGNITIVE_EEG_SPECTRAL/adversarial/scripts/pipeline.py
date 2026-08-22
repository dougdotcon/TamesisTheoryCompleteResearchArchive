"""
Independent adversarial pipeline for DISC-COGNITIVE-EEG-SPECTRAL-001
(depression arm). Implements PREREGISTRATION.md Sec 2 and Sec 4 from
scratch: 19 named channels, -LE montage as recorded (no re-referencing),
256 Hz, R_lambda=[1,40]Hz, single-segment-per-window "Welch" periodogram
(nperseg=1024, noverlap=512, nfft=1024, Hann periodic window, constant
detrend, density scaling), normalized Shannon spectral entropy per window
per channel (log2(N), N = number of frequency bins IN R_lambda),
artifact rejection (reject a 4s window if ANY of the 19 channels exceeds
+-150 uV peak-to-peak in that window; exclude subject if >50% of windows
rejected), Ibar(X) = mean over non-rejected windows, per channel, then
mean over 19 channels. Raw (non-normalized) band power (Sec 5.3 control)
computed with the same window/channel averaging structure for symmetry.
"""
import sys
import os
import json
import hashlib
import subprocess
import time

sys.path.insert(0, os.path.dirname(__file__))
from edf_reader import EDFFile
from welch_entropy import welch_psd, normalized_shannon_entropy
import numpy as np

CHANNELS_19 = [
    "Fp1", "F3", "C3", "P3", "O1", "F7", "T3", "T5", "Fz",
    "Fp2", "F4", "C4", "P4", "O2", "F8", "T4", "T6", "Cz", "Pz",
]

FS_EXPECTED = 256.0
NPERSEG = 1024
NOVERLAP = 512
NFFT = 1024
STEP = NPERSEG - NOVERLAP
BAND_LO, BAND_HI = 1.0, 40.0
PTP_LIMIT_UV = 150.0
SUBJECT_REJECT_FRAC = 0.5


def md5sum(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download_with_retry(url, dest, expected_md5, max_retries=3, timeout=120):
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            if os.path.exists(dest):
                os.remove(dest)
            r = subprocess.run(
                ["curl", "-sS", "-L", "--fail", "--max-time", str(timeout), "-o", dest, url],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                last_err = f"curl exit {r.returncode}: {r.stderr.strip()[:300]}"
                time.sleep(1.5 * attempt)
                continue
            if not os.path.exists(dest) or os.path.getsize(dest) == 0:
                last_err = "empty or missing file after curl"
                time.sleep(1.5 * attempt)
                continue
            got_md5 = md5sum(dest)
            if got_md5 != expected_md5:
                last_err = f"md5 mismatch: got {got_md5} expected {expected_md5}"
                time.sleep(1.5 * attempt)
                continue
            return True, got_md5, attempt, None
        except Exception as e:
            last_err = str(e)
            time.sleep(1.5 * attempt)
    return False, None, max_retries, last_err


def get_band_bins(freqs):
    mask = (freqs >= BAND_LO) & (freqs <= BAND_HI)
    return mask


def process_edf(path, subject_label):
    edf = EDFFile(path)

    idx_by_name = {}
    for name in CHANNELS_19:
        idx = edf.channel_index(label_exact=f"EEG {name}-LE")
        if idx is None:
            raise ValueError(f"{subject_label}: channel EEG {name}-LE not found; "
                              f"labels present: {[s.label for s in edf.signals]}")
        idx_by_name[name] = idx

    fs_list = set()
    signals = {}
    for name, idx in idx_by_name.items():
        fs = edf.sample_rate(idx)
        fs_list.add(round(fs, 6))
        signals[name] = edf.physical_signal(idx)

    if len(fs_list) != 1:
        raise ValueError(f"{subject_label}: inconsistent sample rates across 19 channels: {fs_list}")
    fs = fs_list.pop()
    if abs(fs - FS_EXPECTED) > 1e-6:
        raise ValueError(f"{subject_label}: unexpected sample rate {fs} (expected {FS_EXPECTED})")

    lengths = {len(v) for v in signals.values()}
    if len(lengths) != 1:
        raise ValueError(f"{subject_label}: channel length mismatch: {lengths}")
    n_samples = lengths.pop()

    n_windows = 1 + (n_samples - NPERSEG) // STEP
    if n_windows < 1:
        raise ValueError(f"{subject_label}: recording too short for one window")

    # stack into (19, n_samples) array in fixed channel order
    chan_array = np.stack([signals[name] for name in CHANNELS_19], axis=0)

    # sliding windows for peak-to-peak artifact check: shape (19, n_windows, NPERSEG)
    starts = np.arange(n_windows) * STEP
    # build windows via explicit indexing (vectorized gather)
    idx_grid = starts[:, None] + np.arange(NPERSEG)[None, :]   # (n_windows, NPERSEG)
    windows_raw = chan_array[:, idx_grid]                       # (19, n_windows, NPERSEG)

    ptp = windows_raw.max(axis=2) - windows_raw.min(axis=2)     # (19, n_windows)
    channel_exceeds = ptp > PTP_LIMIT_UV                        # (19, n_windows)
    window_rejected = channel_exceeds.any(axis=0)                # (n_windows,) -- shared mask across all 19 ch
    n_rejected = int(window_rejected.sum())
    reject_frac = n_rejected / n_windows

    excluded = reject_frac > SUBJECT_REJECT_FRAC

    result = {
        "subject": subject_label,
        "n_samples": int(n_samples),
        "fs": fs,
        "n_windows_raw": int(n_windows),
        "n_windows_rejected": n_rejected,
        "reject_frac": reject_frac,
        "excluded_by_artifact_rule": bool(excluded),
    }

    if excluded:
        result["I_per_channel"] = None
        result["Ibar"] = None
        result["bandpower_per_channel"] = None
        result["bandpower_mean"] = None
        return result

    good_window_idx = np.where(~window_rejected)[0]

    win = None  # periodic hann precomputed inside welch_psd via hann_periodic; reuse via direct call
    from welch_entropy import hann_periodic
    hann_win = hann_periodic(NPERSEG)
    win_sum_sq = np.sum(hann_win ** 2)

    freqs = np.fft.rfftfreq(NFFT, d=1.0 / fs)
    band_mask = get_band_bins(freqs)
    n_band_bins = int(band_mask.sum())

    I_per_channel = np.empty(19, dtype=np.float64)
    bp_per_channel = np.empty(19, dtype=np.float64)

    for ci in range(19):
        seg_data = windows_raw[ci, good_window_idx, :]   # (n_good, NPERSEG)
        seg_data = seg_data - seg_data.mean(axis=1, keepdims=True)  # detrend='constant'
        seg_data = seg_data * hann_win[None, :]
        spec = np.fft.rfft(seg_data, n=NFFT, axis=1)      # (n_good, n_freq)
        psd = (np.abs(spec) ** 2) / (fs * win_sum_sq)
        if NFFT % 2 == 0:
            psd[:, 1:-1] *= 2.0
        else:
            psd[:, 1:] *= 2.0

        psd_band = psd[:, band_mask]                       # (n_good, n_band_bins)
        band_power_raw = psd_band.sum(axis=1)               # raw (non-normalized) band power per window

        p = psd_band / psd_band.sum(axis=1, keepdims=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            logp = np.where(p > 0, np.log2(p), 0.0)
        h = -np.sum(p * logp, axis=1) / np.log2(n_band_bins)   # per-window entropy

        I_per_channel[ci] = h.mean()
        bp_per_channel[ci] = band_power_raw.mean()

    Ibar = float(I_per_channel.mean())
    bp_mean = float(bp_per_channel.mean())

    result["n_band_bins"] = n_band_bins
    result["I_per_channel"] = I_per_channel.tolist()
    result["Ibar"] = Ibar
    result["bandpower_per_channel"] = bp_per_channel.tolist()
    result["bandpower_mean"] = bp_mean
    return result
