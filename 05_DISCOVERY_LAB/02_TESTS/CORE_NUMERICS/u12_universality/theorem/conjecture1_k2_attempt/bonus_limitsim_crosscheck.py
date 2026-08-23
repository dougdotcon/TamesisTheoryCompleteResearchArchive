"""BONUS (not pre-registered as a required R-item, done for extra
strength): reuse the archive's own pre-existing, independently-written
continuum simulator `limit_characterization/limit_sim.py`
(`one_realization`, wave 2, a from-scratch stick-breaking PD(1) + K
reroutes simulator, predating this document and this document's
derivation entirely) with a FRESH large sample and this front's own
seed, KS-tested against 4x(1-x^2). Run from
`limit_characterization/` so the import resolves; output reproduced
literally below (see bonus_limitsim_crosscheck.log/.json for the actual
run's captured output).

    cd ../../limit_characterization && python3 - <<'PY'
    import sys, json, random
    sys.path.insert(0, '.')
    import numpy as np
    from scipy.stats import kstest
    from limit_sim import one_realization

    SEED0 = 20260835000
    root = np.random.SeedSequence(SEED0)
    child = root.spawn(3)[2]  # distinct child, disjoint from R4/R5 spawns
    npg = np.random.default_rng(child)
    rng = random.Random(int(npg.integers(0, 2**63 - 1)))

    N = 300_000
    xs = np.array([one_realization(2, rng)[0] for _ in range(N)])
    cdf_target = lambda t: 2 * t ** 2 - t ** 4
    st = kstest(xs, cdf_target)
    mean_mc = xs.mean()
    sem_mc = xs.std(ddof=1) / np.sqrt(N)
    target_mean = 8 / 15
    print(f'KS D={st.statistic:.5f} p={st.pvalue:.4f}')
    print(f'mean={mean_mc:.6f} +/- {sem_mc:.6f} vs 8/15={target_mean:.6f} '
          f'z={(mean_mc - target_mean) / sem_mc:+.2f}')
    PY
"""
