"""
Validacao (a): rede regular (espacamento deterministico = 1).
Ground truth esperado: V_hat(L) proximo de 0 (nao exatamente 0 por efeito de
borda de bloco, mas pequeno frente a escala O(0.1-1) usada na analise real).
"""
import json
import numpy as np
from estimator_adv import block_number_variance

results = {}
rng_note = "sem seed (deterministico, sem aleatoriedade)"

N = 200000
x = np.arange(N, dtype=np.float64) * 1.0  # espacamento exatamente 1

# usar a MESMA forma de grade de L que a analise real (mult * logT-like scale)
# aqui simplesmente testamos varios L representativos, incluindo os L
# primarios reais (2155.04 e 210.50) e o L secundario, e um L pequeno.
test_Ls = [1.0, 5.0, 10.0, 20.0, 50.0, 100.0, 250.0,  # integer L -> V=0 exato
           210.50366944478924, 1436.695961804594, 2155.043942706891,  # L's reais
           7.3, 15.75]  # nao-inteiros arbitrarios extra

# NOTA (achado durante a validacao, nao um bug): para uma rede perfeitamente
# regular (espacamento 1) e L NAO-INTEIRO, a variancia teorica exata NAO e 0,
# e sim f*(1-f) onde f = parte fracionaria de L. Derivacao: como y varia
# uniformemente sobre um periodo, n(L;y) vale floor(L) com probabilidade
# (1-f) e floor(L)+1 com probabilidade f (media = floor(L)+f = L, correto);
# Var = (1-f)*f^2 + f*(1-f)^2 = f*(1-f). So para L INTEIRO a variancia e
# exatamente 0. Isso e usado como alvo teorico exato (nao apenas "~0"),
# validacao mais forte que um limiar arbitrario.
out = []
for L in test_Ls:
    x_range = x[-1] - x[0]
    B = max(int(x_range // (4.0 * L)), 3)
    res = block_number_variance(x, L, B)
    f = L - np.floor(L)
    V_theory = f * (1.0 - f)
    diff = res["V_hat"] - V_theory
    out.append(dict(L=L, B_requested=B, V_theory=V_theory, diff=diff, **res))
    print(f"L={L:12.4f}  B_used={res['n_blocks_used']:4d}  V_hat={res['V_hat']:.6f}  "
          f"V_theory(f(1-f))={V_theory:.6f}  diff={diff:.2e}  SE={res['SE']:.2e}")

results["N"] = N
results["test_Ls"] = out
results["verdict"] = "PASS" if all(abs(r["diff"]) < 1e-6 for r in out if r["n_blocks_used"] > 0) else "FAIL"

with open("validation_lattice_adv.json", "w") as f:
    json.dump(results, f, indent=2)

print()
print("VERDICT:", results["verdict"])
