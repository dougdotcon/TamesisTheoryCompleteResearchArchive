"""
Frente u12-universality — validacao interna da implementacao propria.

Checks:
V1. Contador de pontos ciclicos (peeling de Kahn) vs metodo
    independente (imagem de f^(2^k) com 2^k >= n: o conjunto de
    valores de f iterado n vezes e exatamente o conjunto ciclico).
    100 mapas aleatorios de tamanhos variados => igualdade exata.
V2. Random map puro: E[#pontos ciclicos] ~ sqrt(pi*n/2)
    (Flajolet & Odlyzko 1990) — razao observado/teoria ~ 1.
V3. c=0: phi = 1 exatamente (permutacao pura).
"""

import json
import numpy as np
from u12_reproduction import sample_phi


def cyclic_count_kahn(f):
    n = len(f)
    indeg = np.bincount(f, minlength=n)
    stack = list(np.flatnonzero(indeg == 0))
    removed = 0
    while stack:
        v = stack.pop()
        removed += 1
        w = f[v]
        indeg[w] -= 1
        if indeg[w] == 0:
            stack.append(w)
    return n - removed


def cyclic_count_power(f):
    n = len(f)
    g = f.copy()
    steps = 1
    while steps < n:          # g = f^(steps), duplica ate steps >= n
        g = g[g]
        steps *= 2
    return len(np.unique(g))


def main():
    rng = np.random.default_rng(555)
    out = {}

    # V1: igualdade exata entre os dois contadores
    mismatches = 0
    for _ in range(100):
        n = int(rng.integers(2, 2000))
        kind = rng.random()
        if kind < 0.4:
            f = rng.integers(0, n, size=n)          # random map
        elif kind < 0.7:
            f = rng.permutation(n)                   # permutacao
        else:
            f = rng.permutation(n)                   # ensemble U_1/2
            c = float(rng.uniform(0, 20))
            mask = rng.random(n) < c / n
            f[mask] = rng.integers(0, n, size=int(mask.sum()))
        if cyclic_count_kahn(f) != cyclic_count_power(f):
            mismatches += 1
    out["V1_counter_mismatches_of_100"] = mismatches
    print(f"V1: {mismatches}/100 divergencias entre contadores")

    # V2: random map puro vs sqrt(pi*n/2)
    v2 = []
    for n in [1000, 4000, 16000]:
        counts = []
        for _ in range(300):
            f = rng.integers(0, n, size=n)
            counts.append(cyclic_count_kahn(f))
        obs = float(np.mean(counts))
        theo = float(np.sqrt(np.pi * n / 2))
        v2.append({"n": n, "observed": obs, "theory_sqrt_pi_n_2": theo,
                   "ratio": obs / theo})
        print(f"V2: n={n} E[ciclicos]={obs:.1f} teoria={theo:.1f} "
              f"razao={obs/theo:.3f}")
    out["V2_random_map"] = v2

    # V3: c=0 => phi=1
    phis = [sample_phi(500, 0.0, rng) for _ in range(20)]
    out["V3_c0_all_one"] = bool(all(p == 1.0 for p in phis))
    print(f"V3: c=0 -> phi=1 em 20/20: {out['V3_c0_all_one']}")

    with open("result_validation_checks.json", "w") as fh:
        json.dump(out, fh, indent=2)


if __name__ == "__main__":
    main()
