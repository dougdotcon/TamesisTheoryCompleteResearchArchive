"""Adversarial from-scratch simulator for the u12 ensemble.

Ensemble: pi = uniform permutation of [n]; each i independently rerouted
with prob p=c/n to Uniform[n]; phi = fraction of cyclic points of f.

Implementation choices (deliberately different from any archive code):
  - reroute via K ~ Binomial(n, c/n), K positions WITHOUT replacement,
    K destinations WITH replacement;
  - cyclic-point detection via pointer doubling: g = f^(2^m), 2^m >= n;
    cyclic points = image(f^N) for N >= n; count via boolean scatter.
"""
import numpy as np


def sample_phi_batch(n, c, batch, rng):
    """Return array of phi values, one per sample in the batch."""
    p = c / n
    f = np.empty((batch, n), dtype=np.int64)
    for b in range(batch):
        perm = rng.permutation(n)
        k = rng.binomial(n, p)
        if k > 0:
            pos = rng.choice(n, size=k, replace=False)
            dest = rng.integers(0, n, size=k)
            perm[pos] = dest
        f[b] = perm
    # pointer doubling: g = f^(2^m) with 2^m >= n
    m = 1
    steps = 0
    while m < n:
        m <<= 1
        steps += 1
    g = f.copy()
    for _ in range(steps):
        g = np.take_along_axis(g, g, axis=1)
    # count image size per row via boolean scatter
    present = np.zeros((batch, n), dtype=bool)
    rows = np.repeat(np.arange(batch), n)
    present[rows, g.ravel()] = True
    return present.sum(axis=1) / n


def run_cell(n, c, n_samples, rng, batch=None):
    """Return (mean, std, sem, n_samples, all_samples)."""
    if batch is None:
        batch = max(1, min(n_samples, int(4e6 // n)))
    vals = np.empty(n_samples)
    done = 0
    while done < n_samples:
        b = min(batch, n_samples - done)
        vals[done:done + b] = sample_phi_batch(n, c, b, rng)
        done += b
    mean = float(vals.mean())
    std = float(vals.std(ddof=1))
    return mean, std, std / np.sqrt(n_samples), n_samples, vals
