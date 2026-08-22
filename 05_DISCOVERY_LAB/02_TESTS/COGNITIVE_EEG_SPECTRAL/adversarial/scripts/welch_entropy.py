"""
Independent, from-scratch implementation of:
  - Welch PSD estimation (Welch 1967), matching scipy.signal.welch's
    default conventions for window='hann', detrend='constant',
    scaling='density', return_onesided=True, average='mean' --
    but implemented here without calling scipy.signal.welch, per the
    adversarial-reproduction mandate (own PSD computation).
  - Normalized Shannon spectral entropy per PREREGISTRATION.md Sec 2.

Convention notes (checked explicitly, since this is exactly the kind of
detail a bug could hide in):
  - Hann window: PERIODIC convention (matches scipy.signal.get_window
    default fftbins=True, which is what a bare string window='hann'
    argument to scipy.signal.welch resolves to) --
        w[n] = 0.5 - 0.5*cos(2*pi*n / M),  n = 0..M-1
    NOT the symmetric convention (which would divide by M-1).
  - Detrend: subtract the per-segment mean ('constant').
  - nfft == nperseg here (no zero padding).
  - Scaling 'density': divide by (fs * sum(window**2)); one-sided
    spectrum: double all bins except DC (and Nyquist, if nfft is even).
  - Averaging across segments: arithmetic mean of periodograms.
"""
import numpy as np


def hann_periodic(m):
    n = np.arange(m)
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * n / m)


def welch_psd(x, fs, nperseg=1024, noverlap=512, nfft=1024):
    """Returns (freqs, psd) matching scipy.signal.welch(x, fs, window='hann',
    nperseg=nperseg, noverlap=noverlap, nfft=nfft, detrend='constant',
    scaling='density', return_onesided=True, average='mean')."""
    x = np.asarray(x, dtype=np.float64)
    step = nperseg - noverlap
    n = len(x)
    if n < nperseg:
        raise ValueError("segment shorter than nperseg")
    n_segs = 1 + (n - nperseg) // step

    win = hann_periodic(nperseg)
    win_sum_sq = np.sum(win ** 2)

    n_freq = nfft // 2 + 1
    periodograms = np.empty((n_segs, n_freq), dtype=np.float64)

    for i in range(n_segs):
        start = i * step
        seg = x[start:start + nperseg]
        seg = seg - seg.mean()          # detrend='constant'
        seg = seg * win
        spec = np.fft.rfft(seg, n=nfft)
        psd = (np.abs(spec) ** 2) / (fs * win_sum_sq)
        # one-sided doubling: double all bins except DC, and Nyquist if nfft even
        if nfft % 2 == 0:
            psd[1:-1] *= 2.0
        else:
            psd[1:] *= 2.0
        periodograms[i] = psd

    psd_mean = periodograms.mean(axis=0)
    freqs = np.fft.rfftfreq(nfft, d=1.0 / fs)
    return freqs, psd_mean, n_segs


def normalized_shannon_entropy(psd_band):
    """PREREGISTRATION.md Sec 2: p_i = P(f_i)/sum P(f_j) over band bins only;
    I(X) = -sum(p_i log2 p_i) / log2(N), N = number of bins IN THE BAND
    (not total FFT bins)."""
    psd_band = np.asarray(psd_band, dtype=np.float64)
    total = psd_band.sum()
    if total <= 0:
        raise ValueError("non-positive total power in band")
    p = psd_band / total
    n = len(p)
    if n < 2:
        raise ValueError("need >=2 bins in band for normalized entropy (log2(N) with N>=2)")
    # 0 log 0 := 0
    nz = p > 0
    h = -np.sum(p[nz] * np.log2(p[nz]))
    return h / np.log2(n)
