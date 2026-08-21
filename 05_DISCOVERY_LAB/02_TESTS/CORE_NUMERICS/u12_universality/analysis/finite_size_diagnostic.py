"""
Frente u12-universality — DIAGNOSTICO POS-HOC (nao muda vereditos
pre-declarados; ver METHODOLOGY_NOTE.md e RESULTS_SUMMARY.md).

Pergunta: o desvio sistematico phi_medido - (1+c)^(-1/2) observado nas
grades primaria/adversarial encolhe com n (efeito de tamanho finito)
ou persiste (limite n->inf diferente de (1+c)^(-1/2))?

Protocolo: c in {0.5, 2, 10, 50}; n in {1000, 4000, 16000, 64000};
N=400 amostras por celula; seed base 99001122 (novo, independente).
"""

import json
import numpy as np
from u12_reproduction import sample_phi

C_VALUES = [0.5, 2.0, 10.0, 50.0]
N_VALUES = [1000, 4000, 16000, 64000]
N_SAMPLES = 400
SEED = 99001122


def main():
    ss = np.random.SeedSequence(SEED)
    children = ss.spawn(len(N_VALUES) * len(C_VALUES))
    idx = 0
    rows = []
    for n in N_VALUES:
        for c in C_VALUES:
            rng = np.random.default_rng(children[idx]); idx += 1
            phis = np.array([sample_phi(n, c, rng)
                             for _ in range(N_SAMPLES)])
            theory = (1 + c) ** -0.5
            mean = phis.mean()
            sem = phis.std(ddof=1) / np.sqrt(N_SAMPLES)
            dev = mean - theory
            rows.append({"n": n, "c": c, "phi_mean": float(mean),
                         "phi_sem": float(sem), "phi_theory": float(theory),
                         "deviation": float(dev),
                         "deviation_over_sem": float(dev / sem)})
            print(f"  n={n:6d} c={c:5.1f}  phi={mean:.4f}+/-{sem:.4f}  "
                  f"teoria={theory:.4f}  desvio={dev:+.4f} "
                  f"({dev/sem:+.1f} SEM)", flush=True)
    out = {"test": "finite_size_diagnostic_posthoc", "seed_base": SEED,
           "n_samples": N_SAMPLES, "rows": rows}
    with open("result_finite_size_diagnostic.json", "w") as fh:
        json.dump(out, fh, indent=2)


if __name__ == "__main__":
    main()
