import numpy as np

def simulate_one(t0, c, rng):
    """Exact abstract recursive process (continuum idealization, THROWAWAY exploratory sim).
    State: s = total explored mass so far (t0-g_consumed + s_E), g = current remaining gap
           (only meaningful while type-G; track g directly).
    We track (s, g) where g is the CURRENT remaining gap of x0's cycle (shrinks only via
    type-G progress or a gap-hit reentry), and s is TOTAL mass explored so far (grows via
    both type-G progress and type-E excursions).
    mode: 'G' or 'E'.
    """
    s = 0.0
    g = t0
    mode = 'G'
    for _ in range(200000):
        T = rng.exponential(1.0 / c)
        if mode == 'G':
            if T >= g:
                return True  # success: swept remaining gap with no mark
            # mark occurs after consuming T of the gap
            s = s + T
            g = g - T
            # s should equal (t0 - g) + s_E_accumulated_so_far automatically since
            # we're adding T (the just-consumed gap mass) directly to s.
        else:  # mode 'E'
            s = s + T
            # g unchanged
        if s >= 1.0:
            return False  # exhausted universe without success (shouldn't really happen for reasonable params)
        # resolve mark destination: uniform over remaining "conceptual" [0,1)
        # kill prob = s (mass already explored, INCLUDING this s update)
        # gap-hit prob = g (current remaining gap)
        # else: type-E
        u = rng.random()
        if u < s:
            return False  # kill
        elif u < s + g:
            # land within remaining gap g, uniform position -> new gap ~ Unif(0, g)
            g = g * rng.random()
            mode = 'G'
        else:
            mode = 'E'
    return False  # safety fallback (shouldn't be reached)


def phi_abstract(t0, c, N, rng):
    succ = 0
    for _ in range(N):
        if simulate_one(t0, c, rng):
            succ += 1
    return succ / N


if __name__ == "__main__":
    # THROWAWAY exploratory seed
    rng = np.random.default_rng(np.random.SeedSequence(20260833901))
    c = 1000
    N = 20000
    for t0 in [1e-4, 0.0019, 0.0053, 0.0114, 0.0229, 0.0458, 0.0916, 0.1831, 0.3738, 0.7477]:
        p = phi_abstract(t0, c, N, rng)
        se = np.sqrt(p*(1-p)/N)
        print(f"t0={t0:.5f}  phi_abstract={p:.5f}+-{se:.5f}")
