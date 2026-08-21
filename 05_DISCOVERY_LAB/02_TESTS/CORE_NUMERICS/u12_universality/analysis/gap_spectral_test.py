"""
Frente u12-universality — Teste R3: gap(n) = 2/n, lambda_2 = (n-2)/n
para o operador de UMA particao de quicksort com pivo uniforme em S_n.

Implementacao propria (nao reutiliza stage_34_2/34_3):
  L[sigma' | sigma] = (1/n) * #{pivos p : particao(sigma, p) = sigma'}
onde particao(sigma, p) remove o valor-pivo sigma[p], poe os menores a
esquerda (ordem relativa preservada), o pivo, e os maiores a direita
— exatamente a definicao operacional de stage_34_2_operator.py:327-349,
reimplementada de forma independente.

Criterio pre-declarado (METHODOLOGY_NOTE.md, R3):
  para n=3..7: | |lambda_2| - (n-2)/n | < 1e-8  e  |gap - 2/n| < 1e-8.
"""

import json
from itertools import permutations
import numpy as np


def partition_step(perm, pivot_idx):
    arr = list(perm)
    pivot = arr.pop(pivot_idx)
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    return tuple(left + [pivot] + right)


def build_operator(n):
    perms = list(permutations(range(n)))
    index = {p: i for i, p in enumerate(perms)}
    m = len(perms)
    L = np.zeros((m, m))
    for j, p in enumerate(perms):
        for k in range(n):
            q = partition_step(p, k)
            L[index[q], j] += 1.0 / n
    return L


def main():
    results = []
    all_pass = True
    for n in range(3, 8):
        L = build_operator(n)
        eig = np.linalg.eigvals(L)
        mags = np.sort(np.abs(eig))[::-1]
        lam1, lam2 = mags[0], mags[1]
        gap = lam1 - lam2
        ok = (abs(lam2 - (n - 2) / n) < 1e-8) and (abs(gap - 2 / n) < 1e-8)
        all_pass &= ok
        results.append({
            "n": n, "dim": L.shape[0],
            "lambda_1_abs": float(lam1),
            "lambda_2_abs": float(lam2),
            "gap": float(gap),
            "claim_lambda2": (n - 2) / n,
            "claim_gap": 2 / n,
            "abs_dev_lambda2": float(abs(lam2 - (n - 2) / n)),
            "abs_dev_gap": float(abs(gap - 2 / n)),
            "pass": bool(ok),
        })
        print(f"n={n}: |l2|={lam2:.10f} (claim {(n-2)/n:.10f})  "
              f"gap={gap:.10f} (claim {2/n:.10f})  "
              f"{'PASS' if ok else 'FAIL'}", flush=True)
    out = {"test": "gap_spectral_R3", "all_pass": bool(all_pass),
           "results": results}
    with open("result_gap_spectral.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("R3:", "REPRODUZIDO (exato)" if all_pass else "NAO reproduzido")


if __name__ == "__main__":
    main()
