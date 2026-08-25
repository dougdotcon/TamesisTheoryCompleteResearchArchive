"""
abstract_proc.py -- fresh, from-scratch (re-)implementation of the abstract
recursive "gap re-entry" process from floor_closed_form_attempt/ATTEMPT.md
SS3.1/SS4 (T3), built directly from the PROSE description (state (s,g), mode
G/E, mark rate c, kill/gap-hit/generic resolution) and independently from
the governing PDE system re-derived in f01_series_derivation.py -- this file
was written without opening fcd_t3.py or any other script in the parent
floor_closed_form_attempt/ directory (matching the standing "re-derive, don't
import, the thing you are trying to independently corroborate" convention
used by every referee in this lineage). It IS structurally similar to
fcd_t3.py's simulate_one, which is expected and correct -- it is simulating
the SAME stated process, not a different one; the value of writing it fresh
is that any bug in fcd_t3.py would not silently propagate here, and vice
versa.

Two entry points:
  simulate_from_G(t0, c, rng)  -- start in mode G at (s=0, g=t0); returns
      True/False (success). This is exactly the physical Phi(0,t0)=phi(t0)
      quantity this document studies.
  simulate_from_E(s0, g0, c, rng) -- start in mode E at (s=s0, g=g0); returns
      True/False. This is Psi(s0,g0), needed to test the closed-form/series
      predictions for Psi directly (f02).
"""
import numpy as np

MAX_STEPS = 400000


def simulate_from_G(t0, c, rng):
    s = 0.0
    g = t0
    mode = 'G'
    for _ in range(MAX_STEPS):
        T = rng.exponential(1.0 / c)
        if mode == 'G':
            if T >= g:
                return True
            s += T
            g -= T
        else:
            s += T
        if s >= 1.0:
            return False
        u = rng.random()
        if u < s:
            return False
        elif u < s + g:
            g = g * rng.random()
            mode = 'G'
        else:
            mode = 'E'
    return False


def simulate_from_E(s0, g0, c, rng):
    s = s0
    g = g0
    mode = 'E'
    for _ in range(MAX_STEPS):
        T = rng.exponential(1.0 / c)
        if mode == 'G':
            if T >= g:
                return True
            s += T
            g -= T
        else:
            s += T
        if s >= 1.0:
            return False
        u = rng.random()
        if u < s:
            return False
        elif u < s + g:
            g = g * rng.random()
            mode = 'G'
        else:
            mode = 'E'
    return False


def phi_hat(t0, c, N, rng):
    succ = sum(simulate_from_G(t0, c, rng) for _ in range(N))
    p = succ / N
    se = np.sqrt(p * (1 - p) / N)
    return p, se


def psi_hat(s0, g0, c, N, rng):
    succ = sum(simulate_from_E(s0, g0, c, rng) for _ in range(N))
    p = succ / N
    se = np.sqrt(p * (1 - p) / N)
    return p, se
