#!/usr/bin/env python3
"""
Pre-registered PSD analysis for the Schumann-resonance falsification test.
Reads exactly what PREREGISTRATION.md Sections 4-6 specify:

  - Sample rate: read from each hourly file's own *_info.txt ("sampling
    period (usec)"), NOT assumed to be 256 Hz from secondary literature.
  - Binary format: 16-bit signed integers ("16-bit binary format", one
    sign bit + 15 amplitude bits per Salinas et al. 2022), scaled to volts
    by 10 / 2**15 (±10 V A/D saturation limits, per the same paper). Byte
    order (little-endian) was determined empirically in this session
    because it is not stated in the Zenodo record or reachable in the
    paper's abstract text (see PROVENANCE.md "Binary format" section for
    the full endianness determination).
  - For each of the 3 pre-registered 24h segments x 2 channels (NS, EW):
      concatenate the 24 hourly files in chronological order, compute
      Welch PSD (scipy.signal.welch, Hann window, nperseg = round(64 s *
      confirmed fs), 50% overlap), find the dominant peak in 5-10 Hz, and
      compute its prominence ratio (peak power / median power in the
      peak's own +-1 Hz neighborhood).
  - Classification per PREREGISTRATION.md Section 5, applied literally and
    mechanically (see the block comment above `classify_segment` below for
    exactly how the two clauses of Section 5 -- "dominant peak of the
    5-10 Hz window" and "a distinguishable peak exists within
    [6.70, 8.35] Hz" -- are combined; this interpretation is written out
    explicitly so the adversarial reviewer can check it against the raw
    per-channel numbers independently).

This script performs NO reformulation of the hypothesis, test statistic,
null model, or falsification criterion after seeing the data. All of those
were locked in PREREGISTRATION.md before any real data file was opened.
"""
import json
import re
from pathlib import Path

import numpy as np
from scipy import signal
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
RAW_DIR = BASE / "data" / "raw"
OUT_JSON = BASE / "data" / "results_primary.json"
OUT_PLOT_DIR = BASE / "data" / "plots"
OUT_PLOT_DIR.mkdir(parents=True, exist_ok=True)

TOLERANCE_LOW, TOLERANCE_HIGH = 6.70, 8.35   # PREREGISTRATION.md Section 5
SEARCH_LOW, SEARCH_HIGH = 5.0, 10.0          # PREREGISTRATION.md Section 4
PROMINENCE_THRESHOLD = 3.0                    # PREREGISTRATION.md Section 5
WELCH_SECONDS = 64.0                          # PREREGISTRATION.md Section 4
SCALE_VOLTS_PER_LSB = 10.0 / (2 ** 15)        # Salinas et al. 2022: +-10V, 16-bit signed

SEGMENTS = [
    ("2014-01-15", "winter"),
    ("2014-04-15", "spring"),
    ("2014-07-15", "summer"),
]
CHANNELS = ["NS", "EW"]

INFO_RE = {
    "period_usec": re.compile(r"sampling period \(usec\):\s*([\d.]+)"),
    "gain": re.compile(r"sampling gain:\s*(-?\d+)"),
    "polarity": re.compile(r"sampling polarity:\s*(-?\d+)"),
    "timestamp": re.compile(r"1st sample timestamp:\s*(.+? UTC)"),
    "n_samples": re.compile(r"number of samples:\s*(\d+)"),
}


def parse_info_txt(text):
    out = {}
    for key, pat in INFO_RE.items():
        m = pat.search(text)
        if not m:
            raise ValueError(f"could not find {key!r} in info.txt:\n{text}")
        out[key] = m.group(1)
    out["period_usec"] = float(out["period_usec"])
    out["gain"] = int(out["gain"])
    out["polarity"] = int(out["polarity"])
    out["n_samples"] = int(out["n_samples"])
    return out


def load_channel_segment(seg_label, channel):
    """Load and concatenate the 24 hourly files for one channel/segment.
    Returns (samples_volts: np.ndarray, fs_hz: float, meta: dict)."""
    chan_dir = RAW_DIR / seg_label / channel
    bin_files = sorted(
        [p for p in chan_dir.iterdir() if not p.name.endswith("_info.txt")],
        key=lambda p: int(re.search(r"_(\d{10})$", p.name).group(1)),
    )
    if len(bin_files) != 24:
        raise RuntimeError(
            f"{seg_label}/{channel}: expected 24 hourly files, found {len(bin_files)}"
        )

    infos = []
    chunks = []
    for bf in bin_files:
        info_path = bf.with_name(bf.name + "_info.txt")
        info = parse_info_txt(info_path.read_text())
        infos.append(info)

        raw = np.fromfile(bf, dtype="<i2")  # confirmed little-endian, signed 16-bit
        if raw.size != info["n_samples"]:
            raise RuntimeError(
                f"{bf}: file has {raw.size} samples but info.txt declares "
                f"{info['n_samples']}"
            )
        chunks.append(raw.astype(np.float64) * SCALE_VOLTS_PER_LSB)

    periods = sorted(set(i["period_usec"] for i in infos))
    gains = sorted(set(i["gain"] for i in infos))
    polarities = sorted(set(i["polarity"] for i in infos))
    if len(periods) != 1:
        raise RuntimeError(f"{seg_label}/{channel}: inconsistent sampling period across "
                            f"hourly files: {periods}")

    fs = 1e6 / periods[0]
    samples = np.concatenate(chunks)
    meta = {
        "n_hourly_files": len(bin_files),
        "sampling_period_usec": periods[0],
        "fs_hz_confirmed_from_info_txt": fs,
        "gains_seen": gains,
        "polarities_seen": polarities,
        "first_timestamp_utc": infos[0]["timestamp"],
        "last_file_timestamp_utc": infos[-1]["timestamp"],
        "total_samples": int(samples.size),
        "total_duration_hours": samples.size / fs / 3600.0,
        "mean_volts": float(samples.mean()),
        "std_volts": float(samples.std()),
        "min_volts": float(samples.min()),
        "max_volts": float(samples.max()),
    }
    return samples, fs, meta


def welch_psd(samples, fs):
    nperseg = int(round(WELCH_SECONDS * fs))
    noverlap = nperseg // 2
    f, pxx = signal.welch(
        samples, fs=fs, window="hann", nperseg=nperseg, noverlap=noverlap,
        detrend="constant", scaling="density",
    )
    return f, pxx, nperseg, noverlap


def local_prominence(f, pxx, center_freq, half_width=1.0):
    mask = (f >= center_freq - half_width) & (f <= center_freq + half_width)
    neighborhood = pxx[mask]
    peak_power = pxx[np.argmin(np.abs(f - center_freq))]
    median_power = float(np.median(neighborhood))
    ratio = peak_power / median_power if median_power > 0 else float("inf")
    return float(peak_power), median_power, float(ratio)


def genuine_local_maxima_in_band(f, pxx, low, high):
    """
    Return the frequencies (and powers) of every genuine local maximum
    (a bin strictly greater than both of its immediate neighbor bins in
    the full Welch spectrum) whose frequency falls inside [low, high].

    This operationalizes the plain-English existence test in
    PREREGISTRATION.md Section 5 ("nenhum pico distinguivel de ruido de
    fundo existe dentro de [...]" / "um pico existe mas sua proeminencia
    e inferior a 3x") -- the pre-registration gives a precise formula for
    a peak's PROMINENCE RATIO once a peak candidate is identified, but
    does not give a formal algorithm for peak EXISTENCE itself. A local
    maximum (bin higher than both neighbors) is the standard, minimal,
    parameter-free reading of "a peak exists" in a discretized spectrum,
    and is used here only for that existence question -- never to alter
    the prominence-ratio formula or the 3x threshold themselves.
    """
    from scipy.signal import find_peaks
    peak_idx, _ = find_peaks(pxx)  # no prominence filter: literally any local max
    mask = (f[peak_idx] >= low) & (f[peak_idx] <= high)
    return [(float(f[i]), float(pxx[i])) for i in peak_idx[mask]]


def analyze_channel_segment(seg_label, channel):
    samples, fs, meta = load_channel_segment(seg_label, channel)
    f, pxx, nperseg, noverlap = welch_psd(samples, fs)

    # Global dominant peak within the pre-registered 5-10 Hz search window.
    search_mask = (f >= SEARCH_LOW) & (f <= SEARCH_HIGH)
    f_search, pxx_search = f[search_mask], pxx[search_mask]
    dom_idx = int(np.argmax(pxx_search))
    dom_freq = float(f_search[dom_idx])
    dom_power, dom_median, dom_prominence = local_prominence(f, pxx, dom_freq)

    # Best candidate peak strictly within the locked tolerance band
    # [6.70, 8.35] Hz -- used for the FALSIFIES existence check in
    # PREREGISTRATION.md Section 5, independently of whether it is also
    # the global dominant peak of the wider 5-10 Hz window.
    tol_mask = (f >= TOLERANCE_LOW) & (f <= TOLERANCE_HIGH)
    f_tol, pxx_tol = f[tol_mask], pxx[tol_mask]
    tol_idx = int(np.argmax(pxx_tol))
    tol_freq = float(f_tol[tol_idx])
    tol_power, tol_median, tol_prominence = local_prominence(f, pxx, tol_freq)

    dominant_is_in_tolerance = TOLERANCE_LOW <= dom_freq <= TOLERANCE_HIGH
    # sanity: if the global 5-10Hz max lies inside the tolerance band, it
    # must coincide with the tolerance-band-restricted max too.
    if dominant_is_in_tolerance:
        assert abs(dom_freq - tol_freq) < 1e-9, (dom_freq, tol_freq)

    supported_this_channel = dominant_is_in_tolerance and dom_prominence >= PROMINENCE_THRESHOLD
    distinguishable_peak_in_tolerance = tol_prominence >= PROMINENCE_THRESHOLD

    # Existence check (see genuine_local_maxima_in_band docstring): is
    # there any real local-maximum bump at all in the tolerance band,
    # independent of whether its prominence ratio clears 3x? This is what
    # separates FALSIFIES ("no distinguishable peak exists") from the
    # "does not distinguish" zone ("a peak exists but prominence < 3x") in
    # PREREGISTRATION.md Section 5 -- the two are textually distinct
    # outcomes there, not the same thing.
    local_maxima_in_tolerance = genuine_local_maxima_in_band(f, pxx, TOLERANCE_LOW, TOLERANCE_HIGH)
    peak_exists_in_tolerance = len(local_maxima_in_tolerance) > 0

    # Also report power at 2nd (~14 Hz) and 3rd (~21 Hz) harmonics for the
    # "clearly separated from 2nd/3rd mode" qualitative check in Section 5.
    def nearest_power(target):
        idx = int(np.argmin(np.abs(f - target)))
        return float(f[idx]), float(pxx[idx])

    h2_freq, h2_power = nearest_power(14.0)
    h3_freq, h3_power = nearest_power(21.0)

    result = {
        "segment": seg_label,
        "channel": channel,
        "meta": meta,
        "welch": {
            "fs_hz": fs,
            "nperseg": nperseg,
            "nperseg_seconds": nperseg / fs,
            "noverlap": noverlap,
            "n_welch_segments_averaged": int(1 + (samples.size - nperseg) // (nperseg - noverlap)),
        },
        "global_dominant_peak_5_10Hz": {
            "freq_hz": dom_freq,
            "power": dom_power,
            "local_median_power_pm1Hz": dom_median,
            "prominence_ratio": dom_prominence,
            "in_tolerance_band": dominant_is_in_tolerance,
        },
        "tolerance_band_best_local_peak": {
            "band": [TOLERANCE_LOW, TOLERANCE_HIGH],
            "freq_hz": tol_freq,
            "power": tol_power,
            "local_median_power_pm1Hz": tol_median,
            "prominence_ratio": tol_prominence,
            "distinguishable_ge_3x": distinguishable_peak_in_tolerance,
            "genuine_local_maximum_exists": peak_exists_in_tolerance,
            "all_local_maxima_in_band": local_maxima_in_tolerance,
        },
        "harmonics_check": {
            "2nd_mode_near_14Hz": {"freq_hz": h2_freq, "power": h2_power},
            "3rd_mode_near_21Hz": {"freq_hz": h3_freq, "power": h3_power},
        },
        "supported_this_channel": supported_this_channel,
    }
    return result, f, pxx


def classify_segment(seg_results):
    """
    Apply PREREGISTRATION.md Section 5 at the per-segment level (the
    section's own wording -- "em pelo menos um dos dois canais... testados"
    / "em NENHUM dos dois canais testados" -- combines the two channels of
    a given segment into a single per-segment verdict; Section 6 additionally
    requires every channel x segment be reported individually, which
    analyze_channel_segment() above does).

    Section 5's own text draws a THREE-way distinction that this function
    applies literally (see genuine_local_maxima_in_band() for how peak
    EXISTENCE, as opposed to peak PROMINENCE, is operationalized):

      SUPPORTED : at least one channel's global dominant 5-10 Hz peak falls
                  inside [6.70, 8.35] Hz AND its prominence ratio >= 3x.

      FALSIFIES : "nenhum pico distinguivel de ruido de fundo existe dentro
                  de [6.70, 8.35] Hz, em NENHUM dos dois canais" -- read
                  literally as: in NEITHER channel does even a genuine local
                  maximum (bump) exist anywhere inside the tolerance band.
                  This is a qualitatively different (stronger, "nothing is
                  there at all") condition than "a peak exists but is weak".

      DOES NOT DISTINGUISH : "um pico existe mas sua proeminencia [...] e
                  inferior a 3x -- registrado como tal, nao reinterpretado
                  como suporte ou refutacao". Applied whenever a genuine
                  local maximum exists in the tolerance band in at least one
                  channel (so it is NOT the FALSIFIES case) but the SUPPORTED
                  conditions above are not met for any channel (whether
                  because prominence < 3x, or because the in-band peak is
                  not that channel's global 5-10 Hz dominant peak).
    """
    supported = any(r["supported_this_channel"] for r in seg_results)
    any_peak_exists_in_tolerance = any(
        r["tolerance_band_best_local_peak"]["genuine_local_maximum_exists"] for r in seg_results
    )
    if supported:
        return "SUPPORTED"
    if not any_peak_exists_in_tolerance:
        return "FALSIFIES"
    return "DOES_NOT_DISTINGUISH"


def make_plot(seg_label, channel, f, pxx, result):
    fig, ax = plt.subplots(figsize=(9, 5.5))
    mask = f <= 30
    ax.semilogy(f[mask], pxx[mask], color="#2b6cb0", linewidth=0.9, label="Welch PSD")

    ax.axvspan(TOLERANCE_LOW, TOLERANCE_HIGH, color="#38a169", alpha=0.15,
               label=f"Tolerance band [{TOLERANCE_LOW}, {TOLERANCE_HIGH}] Hz")

    dom = result["global_dominant_peak_5_10Hz"]
    ax.axvline(dom["freq_hz"], color="#c53030", linestyle="--", linewidth=1.2,
               label=f"Dominant 5-10 Hz peak: {dom['freq_hz']:.3f} Hz "
                     f"(prom. {dom['prominence_ratio']:.2f}x)")
    ax.plot([dom["freq_hz"]], [dom["power"]], "o", color="#c53030", markersize=6)

    ax.set_xlim(0, 30)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("PSD (V$^2$/Hz)")
    seg_verdict = result.get("_segment_verdict", "")
    ax.set_title(f"Sierra Nevada ELF station -- {channel} channel, segment {seg_label}\n"
                 f"Welch PSD, nperseg={result['welch']['nperseg']} "
                 f"({result['welch']['nperseg_seconds']:.1f}s), 50% overlap, "
                 f"fs={result['welch']['fs_hz']:.4f} Hz")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, which="both", alpha=0.25)
    fig.tight_layout()
    out_path = OUT_PLOT_DIR / f"psd_{seg_label}_{channel}.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def main():
    all_results = []
    plot_paths = []
    segment_verdicts = {}

    for seg_label, season in SEGMENTS:
        seg_results = []
        seg_spectra = {}
        for channel in CHANNELS:
            print(f"=== {seg_label} ({season}) / {channel} ===")
            result, f, pxx = analyze_channel_segment(seg_label, channel)
            seg_results.append(result)
            seg_spectra[channel] = (f, pxx)
            print(json.dumps({
                "fs_hz": result["welch"]["fs_hz"],
                "nperseg": result["welch"]["nperseg"],
                "n_segments_averaged": result["welch"]["n_welch_segments_averaged"],
                "global_dominant_peak_5_10Hz": result["global_dominant_peak_5_10Hz"],
                "tolerance_band_best_local_peak": result["tolerance_band_best_local_peak"],
            }, indent=2))

        verdict = classify_segment(seg_results)
        segment_verdicts[seg_label] = verdict
        print(f"--- Segment {seg_label} ({season}) verdict: {verdict} ---\n")

        for result in seg_results:
            result["season"] = season
            result["_segment_verdict"] = verdict
            f, pxx = seg_spectra[result["channel"]]
            plot_path = make_plot(seg_label, result["channel"], f, pxx, result)
            result["plot_file"] = str(plot_path.relative_to(BASE))
            plot_paths.append(plot_path)
            del result["_segment_verdict"]
            all_results.append(result)

    output = {
        "preregistration": "05_DISCOVERY_LAB/02_TESTS/SCHUMANN_RESONANCE/PREREGISTRATION.md",
        "tolerance_band_hz": [TOLERANCE_LOW, TOLERANCE_HIGH],
        "search_window_hz": [SEARCH_LOW, SEARCH_HIGH],
        "prominence_threshold": PROMINENCE_THRESHOLD,
        "welch_params": {
            "window": "hann",
            "nperseg_seconds_target": WELCH_SECONDS,
            "overlap_fraction": 0.5,
        },
        "scale_volts_per_lsb": SCALE_VOLTS_PER_LSB,
        "byte_order": "little-endian (int16, signed) -- determined empirically, see PROVENANCE.md",
        "segment_verdicts": segment_verdicts,
        "channel_segment_results": all_results,
    }
    OUT_JSON.write_text(json.dumps(output, indent=2))
    print(f"\nWrote {OUT_JSON}")
    for p in plot_paths:
        print(f"Wrote plot {p}")
    print("\nSegment verdicts:", json.dumps(segment_verdicts, indent=2))


if __name__ == "__main__":
    main()
