"""
Analise pre-registrada de DISC-COSMOLOGY-MOND-SPARC-002 (pivotado).

Implementa EXATAMENTE a Secao 4 de ../PREREGISTRATION.md:
- carrega o split discovery/holdout ja gerado e commitado
  (../data/discovery_holdout_split.json)
- usa APENAS as 120 galaxias de descoberta -- o holdout (55) permanece
  selado, nunca lido por este script
- calcula g_bar/g_obs reais a partir de
  02_TESTS/COSMOLOGY_MOND_SPARC/data/Rotmod_LTG/*.dat (mesma proveniencia
  do piloto, reaproveitada)
- ajusta g-dagger por minimos quadrados nao-lineares (espaco linear,
  leitura literal do texto travado -- nenhuma escolha feita apos ver o
  resultado)
- bootstrap por galaxia (nao por ponto) para IC de 95%
- verifica se a0_A (~1.08e-10, Holographic Bridge) e/ou a0_B (~6.8e-10,
  MOND Emergence) caem dentro do IC

Nao ha dado embutido/fabricado. Qualquer arquivo faltante e um erro
fatal, nao um fallback silencioso.
"""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import curve_fit

HERE = Path(__file__).resolve().parent
TEST_DIR = HERE.parent
SPARC_DATA_DIR = TEST_DIR.parent / "COSMOLOGY_MOND_SPARC" / "data"
ROTMOD_DIR = SPARC_DATA_DIR / "Rotmod_LTG"
SPLIT_FILE = TEST_DIR / "data" / "discovery_holdout_split.json"

KPC_TO_M = 3.0856775814913673e19  # IAU-standard parsec definition
KM_TO_M = 1000.0

UPSILON_DISK = 0.50  # McGaugh, Lelli & Schombert 2016, 3.6um
UPSILON_BUL = 0.7

A0_A = 299792458.0 * ((70.0 * 1000.0) / 3.086e22) / (2 * np.pi)  # Holographic Bridge, a0=cH0/(2pi)
A0_B = 299792458.0 * ((70.0 * 1000.0) / 3.086e22)                 # MOND Emergence, a0=cH0
G_DAGGER_LITERATURE = 1.20e-10  # McGaugh et al. 2016, checagem de sanidade apenas


def load_rotmod(name):
    path = ROTMOD_DIR / f"{name}_rotmod.dat"
    if not path.exists():
        raise FileNotFoundError(f"arquivo rotmod real ausente para {name}: {path}")
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            cols = [float(x) for x in line.split()]
            rows.append(cols)
    arr = np.array(rows)
    rad_kpc, vobs, errv, vgas, vdisk, vbul = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3], arr[:, 4], arr[:, 5]
    return rad_kpc, vobs, vgas, vdisk, vbul


def compute_g_bar_g_obs(rad_kpc, vobs, vgas, vdisk, vbul):
    """Formula verificada de McGaugh, Lelli & Schombert 2016 (PRL 117, 201101)."""
    v_bar_sq = (
        UPSILON_DISK * vdisk * np.abs(vdisk)
        + UPSILON_BUL * vbul * np.abs(vbul)
        + vgas * np.abs(vgas)
    )
    # v_bar_sq pode ser negativo em poucos pontos (quadratura com preservacao
    # de sinal) -- excluir esses pontos da analise (fisicamente indefinido
    # para g_bar), registrar quantos foram excluidos
    valid = v_bar_sq > 0
    r_m = rad_kpc[valid] * KPC_TO_M
    v_bar_m_s = np.sqrt(v_bar_sq[valid]) * KM_TO_M
    v_obs_m_s = vobs[valid] * KM_TO_M

    g_bar = v_bar_m_s ** 2 / r_m
    g_obs = v_obs_m_s ** 2 / r_m
    n_excluded = int(np.sum(~valid))
    return g_bar, g_obs, n_excluded


def rar_model(g_bar, g_dagger):
    return g_bar / (1.0 - np.exp(-np.sqrt(g_bar / g_dagger)))


# g_dagger e ~1e-10 em unidades SI: o Jacobiano numerico por diferencas
# finitas do scipy.optimize.curve_fit tem passo relativo padrao ~1e-8,
# que nessa escala absoluta fica abaixo da precisao de ponto flutuante
# efetiva e o otimizador nao se move (verificado nesta sessao: o "ajuste"
# retornava exatamente o palpite inicial p0 para varios p0 diferentes,
# com residuo relativo de ~129% -- um nao-ajuste disfarcado de ajuste).
# Reparametrizacao para unidades de 1e-10 m/s^2 (fator de escala fixo,
# NAO um parametro livre -- apenas normalizacao numerica) resolve isso
# sem mudar o que esta sendo estimado.
SCALE = 1e-10


def rar_model_scaled(g_bar_scaled, g_dagger_scaled):
    return g_bar_scaled / (1.0 - np.exp(-np.sqrt(g_bar_scaled / g_dagger_scaled)))


def load_discovery_points(galaxy_names):
    all_g_bar, all_g_obs = [], []
    per_galaxy = {}
    total_excluded = 0
    for name in galaxy_names:
        rad_kpc, vobs, vgas, vdisk, vbul = load_rotmod(name)
        g_bar, g_obs, n_excl = compute_g_bar_g_obs(rad_kpc, vobs, vgas, vdisk, vbul)
        total_excluded += n_excl
        if len(g_bar) == 0:
            continue
        per_galaxy[name] = (g_bar, g_obs)
        all_g_bar.append(g_bar)
        all_g_obs.append(g_obs)
    return per_galaxy, np.concatenate(all_g_bar), np.concatenate(all_g_obs), total_excluded


def fit_g_dagger(g_bar, g_obs):
    """Ajuste nao-linear de minimos quadrados de g-dagger (espaco linear,
    unidades de aceleracao escaladas por SCALE para estabilidade numerica
    -- ver nota acima de rar_model_scaled). Verifica convergencia real
    testando dois pontos de partida distintos e exigindo que concordem."""
    g_bar_s = g_bar / SCALE
    g_obs_s = g_obs / SCALE

    fits = []
    for p0_scaled in (1.0, 3.0):  # dois palpites iniciais distintos
        popt, _ = curve_fit(
            rar_model_scaled, g_bar_s, g_obs_s, p0=[p0_scaled],
            bounds=(1e-3, 1e3), method="trf", xtol=1e-14, ftol=1e-14,
        )
        fits.append(popt[0])

    if abs(fits[0] - fits[1]) / max(fits[0], fits[1]) > 1e-4:
        raise RuntimeError(
            f"ajuste nao convergiu de forma consistente entre pontos de "
            f"partida distintos: {fits[0]:.6f} vs {fits[1]:.6f} (unidades "
            f"de {SCALE:.0e} m/s^2) -- parar, nao reportar resultado"
        )
    return fits[0] * SCALE


def main():
    split = json.load(open(SPLIT_FILE))
    discovery_names = split["discovery_galaxies"]
    assert len(discovery_names) == 120, f"esperado 120 galaxias de descoberta, achado {len(discovery_names)}"
    print(f"[1] Amostra de descoberta carregada: {len(discovery_names)} galaxias (holdout selado, nao lido)")

    per_galaxy, g_bar_all, g_obs_all, n_excluded = load_discovery_points(discovery_names)
    print(f"    Pontos totais (pooled): {len(g_bar_all)}")
    print(f"    Pontos excluidos (v_bar^2 <= 0): {n_excluded}")

    g_dagger_point = fit_g_dagger(g_bar_all, g_obs_all)
    print(f"\n[2] g-dagger ajustado (amostra de descoberta, pooled): {g_dagger_point:.4e} m/s^2")
    print(f"    Checagem de sanidade vs literatura ({G_DAGGER_LITERATURE:.2e}): "
          f"razao = {g_dagger_point / G_DAGGER_LITERATURE:.3f}")

    print("\n[3] Bootstrap por galaxia (1000 replicas, reamostragem com reposicao de quais galaxias entram)")
    rng = np.random.RandomState(20260812)
    names = list(per_galaxy.keys())
    boot_estimates = []
    for i in range(1000):
        sampled = rng.choice(names, size=len(names), replace=True)
        bg = np.concatenate([per_galaxy[n][0] for n in sampled])
        bo = np.concatenate([per_galaxy[n][1] for n in sampled])
        try:
            g_d = fit_g_dagger(bg, bo)
            boot_estimates.append(g_d)
        except RuntimeError:
            continue

    boot_estimates = np.array(boot_estimates)
    ci_low, ci_high = np.percentile(boot_estimates, [2.5, 97.5])
    print(f"    Replicas bem-sucedidas: {len(boot_estimates)}/1000")
    print(f"    IC 95%: [{ci_low:.4e}, {ci_high:.4e}] m/s^2")

    a0_a_in_ci = ci_low <= A0_A <= ci_high
    a0_b_in_ci = ci_low <= A0_B <= ci_high

    print(f"\n[4] a0_A (Holographic Bridge, cH0/2pi) = {A0_A:.4e} -- dentro do IC? {a0_a_in_ci}")
    print(f"    a0_B (MOND Emergence, cH0)         = {A0_B:.4e} -- dentro do IC? {a0_b_in_ci}")

    if a0_a_in_ci and not a0_b_in_ci:
        verdict = "H_A_SURVIVES_H_B_FALSIFIED"
    elif a0_b_in_ci and not a0_a_in_ci:
        verdict = "H_B_SURVIVES_H_A_FALSIFIED"
    elif a0_a_in_ci and a0_b_in_ci:
        verdict = "BOTH_SURVIVE_INCONCLUSIVE"
    else:
        verdict = "BOTH_FALSIFIED"

    print(f"\n[5] VEREDITO PRE-REGISTRADO: {verdict}")

    result = {
        "test_id": "DISC-COSMOLOGY-MOND-SPARC-002",
        "n_discovery_galaxies": len(discovery_names),
        "n_points_pooled": int(len(g_bar_all)),
        "n_points_excluded": n_excluded,
        "g_dagger_point_estimate": float(g_dagger_point),
        "g_dagger_ci_95_low": float(ci_low),
        "g_dagger_ci_95_high": float(ci_high),
        "n_bootstrap_success": int(len(boot_estimates)),
        "a0_A_holographic_bridge": A0_A,
        "a0_B_mond_emergence": A0_B,
        "a0_A_in_ci": bool(a0_a_in_ci),
        "a0_B_in_ci": bool(a0_b_in_ci),
        "g_dagger_literature_mcgaugh2016": G_DAGGER_LITERATURE,
        "sanity_ratio_to_literature": float(g_dagger_point / G_DAGGER_LITERATURE),
        "verdict": verdict,
    }
    out_path = HERE / "result_primary.json"
    json.dump(result, open(out_path, "w"), indent=2)
    print(f"\n[6] Resultado salvo em: {out_path}")
    return result


if __name__ == "__main__":
    main()
