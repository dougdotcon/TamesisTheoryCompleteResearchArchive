"""
Validacao (d): checagem analitica/numerica do Modelo A.

1) Verifica que o termo pi^2*L se cancela EXATAMENTE contra -2*pi*L*Si(2*pi*L)
   no limite L->infinito (Si(x)->pi/2), produzindo o crescimento log-lento
   (1/pi^2)*[log(2*pi*L) + gamma0 + 1] citado no pre-registro. Se essa
   cancelacao NAO acontecer numericamente para L grande, ha erro de
   sinal/termo na formula transcrita.

2) Verifica que V_A(L) -> 0 quando L -> 0 (limite trivial: janela vazia).

3) Verifica que V_A(L) e sempre >= 0 (e uma variancia).

4) Compara a magnitude de V_A(L) nos 2 L primarios reais contra a ordem de
   grandeza esperada (log-crescimento lento, na casa de 1.0-1.2 para
   L~200-2200, jamais proximo de 0.3-0.5 como o V_hat empirico do piloto
   sugeriu) -- checagem de sanidade qualitativa antes de tocar dado real.
"""
import json
import numpy as np
from estimator_adv import model_A, EULER_GAMMA

out = {}

# (1) cancelamento assintotico
Ls_large = [1e2, 1e3, 1e4, 1e5, 1e6]
asym_check = []
for L in Ls_large:
    V = model_A(L)
    V_asym_approx = (np.log(2 * np.pi * L) + EULER_GAMMA + 1.0) / (np.pi ** 2)
    diff = V - V_asym_approx
    asym_check.append(dict(L=L, V_A=float(V), V_asym_approx=float(V_asym_approx), diff=float(diff)))
    print(f"L={L:10.1e}  V_A={V:.6f}  V_asym(log-only)={V_asym_approx:.6f}  diff={diff:.2e}")
out["asymptotic_cancellation"] = asym_check
# diff deve ser O(1/L) -> 0 (resto do cos(2piL) e outros termos O(1/L) do Si/Ci)
cancel_pass = abs(asym_check[-1]["diff"]) < 1e-4

# (2) limite L->0
Ls_small = [1e-6, 1e-4, 1e-2, 1e-1]
small_check = []
for L in Ls_small:
    V = model_A(L)
    small_check.append(dict(L=L, V_A=float(V)))
    print(f"L={L:10.1e}  V_A={V:.8f}  (esperado -> 0)")
out["small_L_limit"] = small_check
small_pass = abs(small_check[0]["V_A"]) < 1e-6

# (3) nao-negatividade numa grade densa
Ls_dense = np.linspace(0.01, 3000, 20000)
Vs_dense = model_A(Ls_dense)
min_V = float(np.min(Vs_dense))
print(f"\nMin V_A em grade densa [0.01,3000]: {min_V:.6f} (deve ser >= -eps numerico)")
nonneg_pass = min_V > -1e-6
out["min_V_A_dense_grid"] = min_V

# (4) valores nos L primarios reais
L_zeros1_primary = 2155.043942706891
L_zeros3_primary = 210.50366944478924
V_A_zeros1 = float(model_A(L_zeros1_primary))
V_A_zeros3 = float(model_A(L_zeros3_primary))
print(f"\nModelo A em L_zeros1_primario={L_zeros1_primary:.3f}: V_A={V_A_zeros1:.6f}")
print(f"Modelo A em L_zeros3_primario={L_zeros3_primary:.3f}: V_A={V_A_zeros3:.6f}")
out["model_A_at_primary_Ls"] = dict(zeros1=V_A_zeros1, zeros3=V_A_zeros3)

verdict = "PASS" if (cancel_pass and small_pass and nonneg_pass) else "FAIL"
print(f"\ncancel_pass={cancel_pass}  small_pass={small_pass}  nonneg_pass={nonneg_pass}")
print("VERDICT:", verdict)
out["verdict"] = verdict

with open("validation_model_a_asymptotic.json", "w") as f:
    json.dump(out, f, indent=2)
