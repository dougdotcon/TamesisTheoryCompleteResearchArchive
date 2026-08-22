"""SUPPLEMENTARY (post-hoc, declared as such): distribution-level tests.

Motivated by the literature identification (Hansen & Jaworski, EJC 21(1)
2014, #P1.18, Theorem 7(ii)): for their 'corrupted permutation' with a
fixed in-degree-2 defects, the cyclic fraction has limit density
2ax(1-x^2)^{a-1} on (0,1). Our derivation gives the same MEAN for K=a
(phi_K = Wallis), and a direct hand computation shows our K=1 limit law
is exactly density 2x. Conjecture tested here (NOT pre-registered):

  (C1) cyclic mass | K reroutes  has CDF  F_K(x) = 1 - (1-x^2)^K ;
  (C2) hence the annealed law is M = min(1, sqrt(E/c)), E ~ Exp(1):
       P(M <= x) = 1 - exp(-c x^2) for x < 1, atom exp(-c) at 1.

KS tests, seeds disjoint from T1-T4 (SeedSequence(777001)).
"""
import json
import math
import sys

import numpy as np
from scipy.stats import kstest

sys.path.insert(0, sys.path[0] or ".")
from limit_sim import one_realization  # noqa: E402
import random  # noqa: E402

OUT = []


def sample_cond_K(K, N, ss):
    npg = np.random.default_rng(ss)
    rng = random.Random(int(npg.integers(0, 2**63 - 1)))
    return np.array([one_realization(K, rng)[0] for _ in range(N)])


def main():
    N = 100_000
    root = np.random.SeedSequence(777001)
    spawns = root.spawn(4)
    for K, ss in zip([1, 2, 3], spawns[:3]):
        xs = sample_cond_K(K, N, ss)
        cdf = lambda x, K=K: 1.0 - np.power(np.clip(1.0 - x * x, 0.0, 1.0), K)
        st = kstest(xs, cdf)
        print(f"[SUP] K={K}: KS D={st.statistic:.5f} p={st.pvalue:.4f} (N={N})",
              flush=True)
        OUT.append(dict(test=f"condK_{K}", D=float(st.statistic),
                        p=float(st.pvalue), N=N))

    # annealed test at c=1: continuous part given K>=1
    c = 1.0
    npg = np.random.default_rng(spawns[3])
    rng = random.Random(int(npg.integers(0, 2**63 - 1)))
    Ks = npg.poisson(c, size=N)
    vals = np.array([one_realization(int(k), rng)[0] for k in Ks])
    atom_mc = float(np.mean(vals >= 1.0 - 1e-9))
    atom_th = math.exp(-c)
    z_atom = (atom_mc - atom_th) / math.sqrt(atom_th * (1 - atom_th) / N)
    cont = vals[vals < 1.0 - 1e-9]
    # conditional CDF given M<1: (1-exp(-c x^2))/(1-exp(-c))
    st = kstest(cont, lambda x: (1.0 - np.exp(-c * x * x)) / (1.0 - math.exp(-c)))
    print(f"[SUP] annealed c=1: atom_MC={atom_mc:.5f} vs e^-1={atom_th:.5f} "
          f"(z={z_atom:+.2f}); continuous KS D={st.statistic:.5f} "
          f"p={st.pvalue:.4f} (n={len(cont)})", flush=True)
    OUT.append(dict(test="annealed_c1", atom_mc=atom_mc, atom_th=atom_th,
                    z_atom=float(z_atom), D=float(st.statistic),
                    p=float(st.pvalue), N=N))

    with open(sys.path[0] + "/supplementary_distribution.json", "w") as fh:
        json.dump(OUT, fh, indent=2)
    print("saved supplementary_distribution.json", flush=True)


if __name__ == "__main__":
    main()
