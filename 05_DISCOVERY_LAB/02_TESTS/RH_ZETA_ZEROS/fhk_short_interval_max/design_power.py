"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- fixacao do desenho a partir do piloto
de tempo (phase0_timing.json) e conta de poder projetada, ANTES do lock.

Regra de orcamento (mandato da frente): computacao total sobre dado real
<= ~3 h (10800 s). Alocacao: piloto (~150 s ja gasto) + calibracao de vies
de grade (~510 s) + analise primaria (<= ~9000 s).

Desenho candidato avaliado aqui (fixado se couber no orcamento):
  alturas primarias T em {1e4,...,1e10} (7 decadas), grade 512 pts/intervalo,
  M por altura {2000 x5, 1600 (1e9), 1000 (1e10)}; holdout SELADO: T=1e11.

Poder projetado: EP da inclinacao da WLS de mean(M*)-loglogT sobre
logloglogT, pesos M/sd^2, com sd(M*) por altura EXTRAPOLADO linearmente em
loglogT dos 3 pontos medidos na triagem (0.4388@1e5, 0.4856@1e7,
0.5572@1e9). Numeros finais de poder entram no PREREGISTRATION.md; os pesos
da analise real usarao sd EMPIRICO (declarado la).
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

HEIGHTS = [1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10]
M = {1e4: 2000, 1e5: 2000, 1e6: 2000, 1e7: 2000, 1e8: 2000,
     1e9: 1600, 1e10: 1000}
GRID = 512
N_CAL = {1e4: 80, 1e5: 80, 1e6: 60, 1e7: 60, 1e8: 24, 1e9: 16, 1e10: 8}

# sd(M*) medidos na triagem (item10_fhk_result.json) e ajuste linear em loglogT
sd_meas = {1e5: 0.4388, 1e7: 0.4856, 1e9: 0.5572}


def sd_proj(T):
    x = np.array([np.log(np.log(t)) for t in sd_meas])
    y = np.array(list(sd_meas.values()))
    b, a = np.polyfit(x, y, 1)
    return float(b * np.log(np.log(T)) + a)


def main():
    timing = json.load(open(HERE / "phase0_timing.json"))
    c512 = {r["T"]: r["sec_per_interval_grid512"] for r in timing["rows"]}
    c2048 = {r["T"]: r["sec_per_interval_grid2048"] for r in timing["rows"]}

    cost_primary = sum(M[T] * c512[T] for T in HEIGHTS)
    cost_cal = sum(N_CAL[T] * (c512[T] + c2048[T]) for T in HEIGHTS)
    cost_pilot = sum(
        r.get("n_pilot", 0) * (r["sec_per_interval_grid512"]
                               + r["sec_per_interval_grid2048"]) * 2
        for r in timing["rows"])  # ~2x por warmups

    x = np.array([np.log(np.log(np.log(T))) for T in HEIGHTS])
    sds = np.array([sd_proj(T)for T in HEIGHTS])
    ms = np.array([M[T] for T in HEIGHTS], dtype=float)
    w = ms / sds**2
    xb = np.sum(w * x) / np.sum(w)
    var_slope = 1.0 / np.sum(w * (x - xb) ** 2)
    se = float(np.sqrt(var_slope))

    out = {
        "heights_primary": HEIGHTS, "M": {f"{T:.0e}": M[T] for T in HEIGHTS},
        "grid_points": GRID, "interval_length": "2*pi",
        "holdout_sealed": {"T": 1e11, "M": 600, "grid_points": GRID,
                           "seed": 20260823,
                           "projected_sec_per_interval":
                               timing["holdout_1e11_projection"][
                                   "projected_sec_per_interval_grid512"]},
        "n_calibration_grid_bias": {f"{T:.0e}": N_CAL[T] for T in HEIGHTS},
        "budget_seconds": {"cap": 10800,
                           "primary_projected": cost_primary,
                           "grid_bias_calibration_projected": cost_cal,
                           "phase0_pilot_spent_approx": cost_pilot,
                           "total_projected": cost_primary + cost_cal + cost_pilot},
        "sd_projected_per_height": {f"{T:.0e}": float(s)
                                    for T, s in zip(HEIGHTS, sds)},
        "power_sampling_only": {
            "se_slope_projected": se,
            "asymptotic_separation": 0.5,
            "sigma_separation_asymptotic": 0.5 / se,
            "note": ("separacao CALIBRADA (curvas de altura finita iid exata "
                     "vs CUE) e computada pelas validacoes e entra no "
                     "pre-registro como poder real")},
    }
    json.dump(out, open(HERE / "DESIGN.json", "w"), indent=2)
    print(f"custo primario projetado: {cost_primary:.0f}s; calibracao: "
          f"{cost_cal:.0f}s; total ~{out['budget_seconds']['total_projected']:.0f}s "
          f"(teto 10800s)")
    print(f"EP(inclinacao) projetado = {se:.4f} -> separacao assintotica "
          f"0.5 = {0.5/se:.1f} sigma")
    print("[design] salvo DESIGN.json")


if __name__ == "__main__":
    main()
