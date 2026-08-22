"""
Validacao (b): processo de Poisson (taxa 1). Ground truth conhecido:
V(L) = L exatamente, para QUALQUER L, num processo de Poisson homogeneo
(variancia de uma contagem Poisson = media = L*taxa). Testado na MESMA grade
real (mult*logT) de zeros1 e zeros3, com o MESMO B(L) do DESIGN.json, para
que a validacao cubra exatamente o regime estatistico usado na analise real
(poucos blocos nos pontos primarios).

seed: 20260822 (data do lock, sem relacao com o seed do primario, escolhida
independentemente para esta reproducao adversarial).
"""
import json
import numpy as np
from estimator_adv import block_number_variance

rng = np.random.default_rng(20260822)

# grade real (copiada do DESIGN.json, que ja li -- e parte do design travado,
# nao um resultado de V(L)).
zeros1_grid = [
    (1, 11.22418720159839, 2227), (1.5, 16.836280802397585, 1484),
    (2, 22.44837440319678, 1113), (3, 33.67256160479517, 742),
    (4, 44.89674880639356, 556), (6, 67.34512320959034, 371),
    (8, 89.79349761278712, 278), (12, 134.69024641918068, 185),
    (16, 179.58699522557424, 139), (24, 269.38049283836136, 92),
    (32, 359.1739904511485, 69), (48, 538.7609856767227, 46),
    (64, 718.347980902297, 34), (96, 1077.5219713534455, 23),
    (128, 1436.695961804594, 17), (192, 2155.043942706891, 11),
]
zeros3_grid = [
    (1, 26.312958680598655, 95), (1.5, 39.46943802089798, 63),
    (2, 52.62591736119731, 47), (3, 78.93887604179596, 31),
    (4, 105.25183472239462, 23), (6, 157.87775208359193, 15),
    (8, 210.50366944478924, 11),
]

x_range_zeros1 = 99998.95581061838
x_range_zeros3 = 10000.086866729916

N_REPLICAS = 8

results = {"zeros1_scale": [], "zeros3_scale": []}

for label, grid, x_range in [("zeros1_scale", zeros1_grid, x_range_zeros1),
                               ("zeros3_scale", zeros3_grid, x_range_zeros3)]:
    print(f"=== {label} (x_range={x_range:.2f}) ===")
    n_points_expected = int(round(x_range))
    for mult, L, B in grid:
        z_list = []
        vhat_list = []
        for rep in range(N_REPLICAS):
            # processo de Poisson taxa 1 sobre [0, x_range]: gaps ~ Exp(1)
            n_pts = rng.poisson(x_range)
            gaps = rng.exponential(1.0, size=max(n_pts, 10))
            x = np.cumsum(gaps)
            x = x[x <= x_range]
            if x.size < 20:
                continue
            res = block_number_variance(x, L, B)
            if res["n_blocks_used"] < 2:
                continue
            V_hat = res["V_hat"]
            SE = res["SE"]
            z = (V_hat - L) / SE if SE > 0 else float("nan")
            z_list.append(z)
            vhat_list.append(V_hat)
        z_arr = np.array(z_list)
        print(f"  mult={mult:<6} L={L:10.3f} B={B:4d}  "
              f"V_hat(mean over {len(vhat_list)} reps)={np.mean(vhat_list):.3f}  "
              f"target(L)={L:.3f}  z_range=[{z_arr.min():.2f},{z_arr.max():.2f}]  "
              f"mean|z|={np.mean(np.abs(z_arr)):.2f}")
        results[label].append(dict(mult=mult, L=L, B=B,
                                     V_hat_mean=float(np.mean(vhat_list)),
                                     z_values=z_arr.tolist()))

# criterio de aceite: |z| < 3 na GRANDE maioria dos pontos/replicas
all_z = [z for label in results for entry in results[label] for z in entry["z_values"]]
all_z = np.array(all_z)
frac_within_3 = np.mean(np.abs(all_z) < 3.0)
print(f"\nFracao de |z|<3 em todos pontos/replicas: {frac_within_3:.3f} (n={all_z.size})")
verdict = "PASS" if frac_within_3 > 0.85 else "FAIL"
print("VERDICT:", verdict)

results["frac_within_3"] = float(frac_within_3)
results["verdict"] = verdict
with open("validation_poisson_adv.json", "w") as f:
    json.dump(results, f, indent=2)
