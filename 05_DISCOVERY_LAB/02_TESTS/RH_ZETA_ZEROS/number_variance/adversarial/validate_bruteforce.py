"""
Validacao (c): integral exata (por quebra de pontos) vs integracao numerica
independente (grade fina, ponto medio) em varios L, incluindo os dois L
primarios reais. Usa um conjunto de pontos sintetico (jitter de rede) para
ter um caso pequeno e controlado, mas testa tambem diretamente nos dados
REAIS -- espera: NAO, isto seria tocar dado real antes do lock dos meus
proprios numeros de validacao. Entao aqui uso SOMENTE sintetico. A checagem
cross-estimador contra dado real fica reservada para depois (nao necessaria:
a integral exata e um metodo matematico geral, nao dataset-dependente; validar
em sintetico ja cobre a correcao do metodo).
"""
import json
import numpy as np
from estimator_adv import block_number_variance, _exact_window_integral_single_block, brute_force_number_variance

rng = np.random.default_rng(20260822 + 1)

N = 50000
x = np.sort(np.arange(N, dtype=np.float64) + rng.uniform(-0.45, 0.45, size=N))
x_min, x_max = x[0], x[-1]

test_Ls = [1.0, 5.0, 22.448, 89.793, 210.50366944478924, 718.348,
           1436.695961804594, 2155.043942706891]

out = []
max_rel_diff = 0.0
for L in test_Ls:
    # pega um bloco interior representativo, longe das bordas
    a = x_min + x_max / 2 - 50 * L
    b = x_min + x_max / 2 + 50 * L
    a = max(a, x_min + L)
    b = min(b, x_max - L)

    integral_exact, dx = _exact_window_integral_single_block(x, a, b, L)
    V_exact = integral_exact / dx

    # integracao numerica independente, resolucao fina = L/2000 (mesma
    # resolucao citada no pre-registro para essa checagem, escolhida aqui
    # independentemente pela mesma razao: evitar subamostragem em L pequeno)
    V_bruteforce = brute_force_number_variance(x, L, a, b, resolution=L / 2000.0)

    rel_diff = abs(V_exact - V_bruteforce) / max(abs(V_exact), 1e-12)
    max_rel_diff = max(max_rel_diff, rel_diff)
    out.append(dict(L=L, a=a, b=b, V_exact=V_exact, V_bruteforce=V_bruteforce,
                      rel_diff=rel_diff))
    print(f"L={L:12.4f}  V_exact={V_exact:.6f}  V_bruteforce={V_bruteforce:.6f}  rel_diff={rel_diff:.2e}")

verdict = "PASS" if max_rel_diff < 0.01 else "FAIL"
print(f"\nmax_rel_diff={max_rel_diff:.4e}   VERDICT: {verdict}")

with open("validation_bruteforce_adv.json", "w") as f:
    json.dump(dict(N=N, test_Ls=out, max_rel_diff=max_rel_diff, verdict=verdict), f, indent=2)
