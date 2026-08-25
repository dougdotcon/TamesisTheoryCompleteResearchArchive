#!/usr/bin/env python3
"""
REFEREE Monte Carlo library -- a FRESH, from-scratch implementation of the
abstract recursive 'gap re-entry' process, built ONLY from the prose
specification of record (parent ATTEMPT.md SS3.1/SS4/SS5, its referee
report SS3, and the front-under-review's SS0 restatement).  None of the
front's scripts (abstract_proc.py, f0*.py) or the parent's (fcd_t3.py,
abstract_sim.py) were read, opened, or imported.

Process (state (s,g), mode G or E; marks arrive at rate c per unit of
explored mass s; c=1000 throughout the lineage's target cell):
  - mode G ("actively sweeping the gap"): s increases and g decreases
    together; if g reaches 0 before the next mark -> SUCCESS.
  - at a mark (inter-mark mass increment ~ Exp(c)):
      kill        w.p. s        -> FAIL
      land-in-gap w.p. g        -> new gap ~ Unif(0, g), mode -> G
      generic     w.p. 1-s-g    -> mode -> E (g unchanged)
  - mode E ("generic exploration"): s accrues; nothing but marks matter.
  - target:  Phi(0,t0)  = P(success | start mode G at (0,t0))
             Psi(s0,g0) = P(success | start mode E at (s0,g0))
"""
import numpy as np


def simulate(rng, N, g0, c=1000.0, start_in_G=True, s0=0.0):
    """Simulate N independent walkers; return (n_success, phat, sem)."""
    s = np.full(N, float(s0))
    g = np.full(N, float(g0))
    inG = np.full(N, bool(start_in_G))
    nsucc = 0
    it = 0
    while s.size:
        it += 1
        assert it < 100000, "runaway event loop"
        u = rng.exponential(1.0 / c, size=s.size)
        # mode-G walkers whose remaining gap closes before the next mark
        win = inG & (u >= g)
        nsucc += int(win.sum())
        keep = ~win
        s, g, inG, u = s[keep], g[keep], inG[keep], u[keep]
        if s.size == 0:
            break
        # advance to the mark
        s = s + u
        g = np.where(inG, g - u, g)
        # resolve the mark  (kill w.p. s / gap w.p. g / else generic)
        r = rng.random(s.size)
        dead = r < s
        gap = (~dead) & (r < s + g)
        generic = (~dead) & ~gap
        v = rng.random(s.size)              # new-gap fraction for gap-landers
        g = np.where(gap, g * v, g)
        inG = np.where(gap, True, np.where(generic, False, inG))
        keep = ~dead
        s, g, inG = s[keep], g[keep], inG[keep]
    phat = nsucc / N
    sem = np.sqrt(max(phat * (1 - phat), 1e-300) / N)
    return nsucc, phat, sem
