"""SPARC-FMULTI-STAGE2 -- analise primaria sobre a amostra de DESCOBERTA
real (30.203 sistemas), aplicando a auto-calibracao completa de f_multi
(Chae 2023 Eqs. 11-13) ANTES de qualquer ajuste de a0.

Executa EXATAMENTE a sequencia de chamadas especificada em
PREREGISTRATION_STAGE2.md (LOCKED, DISC-DEC-029), Secao 4:

    1. calibrate_f_multi(..., return_raw=True)      -> f_multi_hat
    2. extrair delta_obs-newt(bin) corrigido de calib["final_result"]
    3. fit_a0() em 2 pontos de partida (x0=1.0, x0=5.0)
    4. bootstrap_a0_refit() usando calib["final_raw"] (NAO uma chamada
       manual reconstruida de run_delta_obs_newt_selfcal -- ver Secao
       4.5/12.4 do pre-registro, resolvido por DISC-DEC-029 via o
       parametro aditivo return_raw de calibrate_f_multi)
    5. regra de decisao da Secao 5 (camada mecanica + camada
       interpretativa obrigatoria sobre o vies residual 1,4-1,6x)
    6. os 5 gatilhos adversariais da Secao 6, cada um checado e reportado
       explicitamente, disparado ou nao

Nenhum parametro numerico deste script foi escolhido apos ver o dado --
todos vem literalmente da tabela da Secao 4.6 do pre-registro travado.

============================================================================
Disciplina do holdout selado (Secao 8 do pre-registro, linha vermelha)
============================================================================
Este script LE `discovery_holdout_split.json` (nao ha' outra forma de obter
a lista de pares de descoberta), mas usa SOMENTE a chave
`discovery_pair_ids` (e o inteiro `n_discovery`, uma contagem, nao uma
lista) -- as chaves `holdout_pair_ids` e `n_holdout` NUNCA sao acessadas,
em lugar nenhum deste arquivo. Isso e' verificado explicitamente pelo grep
de Secao 9.3 (reaplicado a este script especificamente, ver
`STAGE2_9_3_GREP_CHECK.txt` gerado por este mesmo script antes de tocar
qualquer coluna real). O split do disco (`n_holdout=12944`,
`seed=20260814`) e' conhecido de `PREREGISTRATION.md` Secao 2 -- nao
precisa ser lido do arquivo para nenhum proposito deste script.
"""

from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

THIS_DIR = Path(__file__).resolve().parent            # fmulti_selfcal_stage1/analysis
STAGE1_DIR = THIS_DIR.parent                            # fmulti_selfcal_stage1/
MC_DEPROJ_DIR = STAGE1_DIR.parent                        # COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/
CWB_DIR = MC_DEPROJ_DIR.parent / "COSMOLOGY_WIDE_BINARIES"
LOCKED_ANALYSIS_DIR = MC_DEPROJ_DIR / "analysis"

sys.path.insert(0, str(THIS_DIR))
sys.path.insert(0, str(LOCKED_ANALYSIS_DIR))

import selfcal_pipeline as sp  # noqa: E402  (fmulti_selfcal_stage1/analysis, LOCKED do Estagio 1)
import deprojection_common as dc  # noqa: E402  (LOCKED, so' importado)
import delta_obs_newt as don  # noqa: E402  (LOCKED, so' usado para BIN_EDGES_LOG_GN_SPARC003)

QF_SAMPLE_PATH = CWB_DIR / "data" / "quality_filtered_sample.parquet"
SPLIT_PATH = CWB_DIR / "data" / "discovery_holdout_split.json"
HWANG_SUBSET_PATH = MC_DEPROJ_DIR / "data" / "hwang_eccentricity_subset.parquet"

RESULTS_DIR = STAGE1_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
OUT_JSON = RESULTS_DIR / "result_stage2_primary.json"
GREP_CHECK_OUT = RESULTS_DIR / "STAGE2_9_3_GREP_CHECK.txt"

# ---------------------------------------------------------------------
# Parametros numericos -- TODOS literais da tabela da Secao 4.6 do
# pre-registro travado (PREREGISTRATION_STAGE2.md). Nenhum escolhido
# depois de ver dado real.
# ---------------------------------------------------------------------
BIN_EDGES = don.BIN_EDGES_LOG_GN_SPARC003
ANCHOR_BIN = 4
N_MC = 200
SEED_STAGE2 = 20260822
N_BOOTSTRAP_STAGE2 = 2000
F_LO, F_HI = 0.0, 0.9
XTOL = 5e-4
INCLUDE_WOBBLE = True
REAL_GETS_ASTROMETRIC_NOISE = False  # default de run_delta_obs_newt_selfcal, NAO sobrescrito
X0_LIST = (1.0, 5.0)

C_LIGHT = 299792458.0
H0_SI = 70.0 * 1000.0 / 3.086e22
A0_A = C_LIGHT * H0_SI / (2.0 * np.pi)   # Ponte Holografica, 1.082288e-10
A0_B = C_LIGHT * H0_SI                   # MOND Emergence, 6.800218e-10

# Vies residual conhecido do Estagio 1 (RESULTS_SUMMARY_STAGE1.md Secao 3/5,
# carregado para este Estagio pela Secao 7 do pre-registro travado) --
# NAO um numero medido aqui, um fato ja documentado ANTES de qualquer dado
# real deste Estagio ser tocado.
BIAS_FACTOR_LO = 1.4
BIAS_FACTOR_HI = 1.6

F_MULTI_LITERATURE_LO = 0.25
F_MULTI_LITERATURE_HI = 0.47

STAGE1_RESIDUAL_DEX_LO = 0.15
STAGE1_RESIDUAL_DEX_HI = 0.22

RUWE_FLAG_THRESHOLD = 1.4  # limiar padrao Gaia de "ajuste astrometrico ruim"

# ---------------------------------------------------------------------
# Checagem 9.3 (reaplicada a ESTE script especificamente, por exigencia
# textual da Secao 9.3 do pre-registro) -- grep dos 4 nomes de arquivo de
# dado real travados neste proprio arquivo-fonte, ANTES de tocar qualquer
# coluna. Loga o resultado (nao materializa nenhum conteudo do holdout,
# so' conta ocorrencias de string).
# ---------------------------------------------------------------------

def run_section_9_3_grep_self_check() -> dict:
    src = Path(__file__).read_text()
    targets = [
        "quality_filtered_sample.parquet",
        "hwang_eccentricity_subset.parquet",
        "discovery_holdout_split.json",
        "catalog.parquet",
    ]
    occurrences = {t: len(re.findall(re.escape(t), src)) for t in targets}
    # catalog.parquet (arquivo bruto NAO commitado) precisa dar zero em
    # contexto de USO REAL (path/read_parquet/open), nao zero em contagem
    # de string bruta -- o proprio texto desta funcao de checagem MENCIONA
    # o nome ao explicar o que ela procura, o que inflaria uma contagem
    # ingenua de string sem indicar uso real algum. Checagem por LINHA:
    # sinaliza somente se "catalog.parquet" aparece numa linha que tambem
    # contem um padrao de I/O real (abertura de arquivo/atribuicao de path).
    io_context_re = re.compile(r"(read_parquet|open\(|_PATH\s*=|Path\()")
    catalog_parquet_real_use_lines = [
        line for line in src.splitlines()
        if "catalog.parquet" in line and io_context_re.search(line)
    ]
    catalog_parquet_real_use = bool(catalog_parquet_real_use_lines)
    # Confirma explicitamente que a chave holdout_pair_ids/n_holdout NUNCA
    # aparece como acesso de dicionario neste arquivo-fonte.
    holdout_key_access = bool(re.search(r'\[\s*["\']holdout_pair_ids["\']\s*\]', src)) \
        or bool(re.search(r'\[\s*["\']n_holdout["\']\s*\]', src))
    result = {
        "file_checked": str(Path(__file__).resolve()),
        "locked_real_data_filenames_occurrences_raw_string_count": occurrences,
        "catalog_parquet_real_io_use_lines": catalog_parquet_real_use_lines,
        "note": (
            "Ocorrencias esperadas: os 3 nomes de arquivo REAL usados por "
            "este Estagio (quality_filtered_sample.parquet, "
            "hwang_eccentricity_subset.parquet, discovery_holdout_split.json) "
            "aparecem em PATH_x = ... e comentarios/docstrings -- uso "
            "autorizado explicitamente pela Secao 2 do pre-registro para "
            "este Estagio (ao contrario do Estagio 1, que nao podia tocar "
            "nenhum). catalog.parquet (arquivo bruto NAO commitado, mais "
            "amplo que quality_filtered_sample.parquet) aparece so' em "
            "PROSA (esta docstring/comentarios explicando o que a checagem "
            "procura) -- 'catalog_parquet_real_io_use_lines' deve ficar "
            "vazio, confirmando que nenhuma linha de I/O real (read_parquet/ "
            "open/definicao de _PATH) referencia esse arquivo."
        ),
        "holdout_dict_key_access_found": holdout_key_access,
        "pass": bool(
            not catalog_parquet_real_use and not holdout_key_access
        ),
    }
    with open(GREP_CHECK_OUT, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return result


# ---------------------------------------------------------------------
# Passo 1 -- carrega SOMENTE a amostra de descoberta (30.203 sistemas).
# Le discovery_holdout_split.json apenas para extrair discovery_pair_ids
# e n_discovery (uma CONTAGEM, nao uma lista) -- holdout_pair_ids e
# n_holdout NUNCA sao acessados aqui nem em nenhum outro lugar deste
# arquivo (Secao 8 do pre-registro: linha vermelha explicita).
# ---------------------------------------------------------------------

def load_discovery_sample() -> tuple[pd.DataFrame, int]:
    qf = pd.read_parquet(QF_SAMPLE_PATH)
    hw = pd.read_parquet(HWANG_SUBSET_PATH)
    with open(SPLIT_PATH) as f:
        split = json.load(f)

    # SOMENTE estas duas chaves sao acessadas -- nunca holdout_pair_ids,
    # nunca n_holdout (Secao 8, linha vermelha explicita do pre-registro).
    discovery_ids = set(split["discovery_pair_ids"])
    n_discovery_declared = int(split["n_discovery"])

    qf = qf.rename(columns={"Source1": "source_id1", "Source2": "source_id2"})
    qf["source_id1"] = qf["source_id1"].astype(np.int64)
    qf["source_id2"] = qf["source_id2"].astype(np.int64)

    merged = qf.merge(hw, on=["source_id1", "source_id2"], how="inner")
    if len(merged) != len(qf):
        raise RuntimeError(
            f"Cruzamento com catalogo de Hwang incompleto: {len(merged)} de "
            f"{len(qf)} sistemas."
        )

    pair_id = merged["source_id1"].astype(str) + "_" + merged["source_id2"].astype(str)
    mask_discovery = pair_id.isin(discovery_ids)
    disc = merged.loc[mask_discovery].reset_index(drop=True)

    if len(disc) != n_discovery_declared:
        raise RuntimeError(
            f"Contagem de descoberta nao bate: obtida {len(disc)}, "
            f"esperada {n_discovery_declared}."
        )
    if len(disc) != 30203:
        raise RuntimeError(f"Amostra de descoberta != 30203 (obtida {len(disc)}).")

    return disc, n_discovery_declared


def compute_vp_real_si(disc: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Chae (2023) Eq.4, ja travada em SPARC-003/004 -- v_p =
    4.74047e-3 * dmu[mas/yr] * d_mean_pc[pc] (km/s), SI abaixo."""
    dmu_mas_yr = np.sqrt(
        (disc["pmRA1"].to_numpy(np.float64) - disc["pmRA2"].to_numpy(np.float64)) ** 2
        + (disc["pmDE1"].to_numpy(np.float64) - disc["pmDE2"].to_numpy(np.float64)) ** 2
    )
    d_mean_pc = disc["d_mean_pc"].to_numpy(np.float64)
    v_p_km_s = dc.MAS_YR_TO_KM_S_PER_PC * dmu_mas_yr * d_mean_pc
    return v_p_km_s * 1000.0, dmu_mas_yr


def main():
    t0 = time.time()
    print("=" * 78)
    print("SPARC-FMULTI-STAGE2 -- analise primaria (amostra de descoberta real)")
    print("PREREGISTRATION_STAGE2.md LOCKED, DISC-DEC-029")
    print("=" * 78)

    print("\n[9.3 self-check] grep deste proprio arquivo pelos 4 nomes de "
          "dado real travados + acesso a chaves de holdout...")
    grep_result = run_section_9_3_grep_self_check()
    print(f"    {json.dumps(grep_result, indent=2, ensure_ascii=False)}")
    if not grep_result["pass"]:
        raise RuntimeError(
            "Checagem 9.3 FALHOU neste script (catalog.parquet referenciado "
            "e/ou acesso a chave de holdout encontrado) -- PARANDO antes de "
            "tocar qualquer dado real."
        )

    # ------------------------------------------------------------------
    print("\n[1] Carregando amostra de descoberta (30.203 sistemas, "
          "holdout NUNCA acessado)...")
    disc, n_discovery = load_discovery_sample()
    n_sys = len(disc)
    print(f"    n_discovery carregado = {n_sys}")

    print("\n[2] Construindo colunas de insumo (Secao 2 do pre-registro)...")
    v_p_real_si, dmu_mas_yr = compute_vp_real_si(disc)
    s_m = disc["sepAU"].to_numpy(np.float64) * dc.AU_M
    M1_cat_kg = disc["M1_Msun"].to_numpy(np.float64) * dc.MSUN_KG
    M2_cat_kg = disc["M2_Msun"].to_numpy(np.float64) * dc.MSUN_KG
    e_m = disc["e"].to_numpy(np.float64)
    e_lo = disc["e0"].to_numpy(np.float64)
    e_hi = disc["e1"].to_numpy(np.float64)
    alpha_ecc = disc["alpha"].to_numpy(np.float64)
    dpm_sig = disc["dpm_sig"].to_numpy(np.float64)
    d_mean_pc = disc["d_mean_pc"].to_numpy(np.float64)
    pmra_err1 = disc["e_pmRA1"].to_numpy(np.float64)
    pmra_err2 = disc["e_pmRA2"].to_numpy(np.float64)
    pmde_err1 = disc["e_pmDE1"].to_numpy(np.float64)
    pmde_err2 = disc["e_pmDE2"].to_numpy(np.float64)
    RUWE1 = disc["RUWE1"].to_numpy(np.float64)
    RUWE2 = disc["RUWE2"].to_numpy(np.float64)
    print(f"    v_p_real: mediana={np.median(v_p_real_si)/1000.0:.4f} km/s")
    print(f"    M1_cat mediana={np.median(disc['M1_Msun']):.4f} Msun, "
          f"M2_cat mediana={np.median(disc['M2_Msun']):.4f} Msun")

    # ------------------------------------------------------------------
    print(f"\n[3] Passo 1 do pre-registro -- calibrate_f_multi(return_raw=True) "
          f"(n_mc={N_MC}, seed={SEED_STAGE2}, xtol={XTOL}, "
          f"n_bootstrap_final={N_BOOTSTRAP_STAGE2}, anchor_bin={ANCHOR_BIN})...")
    print("    ATENCAO: isto envolve varias avaliacoes completas de "
          "run_delta_obs_newt_selfcal (bisseccao brentq) sobre os 30.203 "
          "sistemas -- pode levar dezenas de minutos.")
    t_calib0 = time.time()
    calib = sp.calibrate_f_multi(
        s=s_m, v_p_real=v_p_real_si, M1_cat=M1_cat_kg, M2_cat=M2_cat_kg,
        e_m=e_m, e_lo=e_lo, e_hi=e_hi, alpha_ecc=alpha_ecc, dpm_sig=dpm_sig,
        d_mean_pc=d_mean_pc,
        pmra_err1=pmra_err1, pmra_err2=pmra_err2,
        pmde_err1=pmde_err1, pmde_err2=pmde_err2,
        bin_edges=BIN_EDGES, anchor_bin=ANCHOR_BIN, n_mc=N_MC, seed=SEED_STAGE2,
        f_lo=F_LO, f_hi=F_HI, xtol=XTOL, include_wobble=INCLUDE_WOBBLE,
        n_bootstrap_final=N_BOOTSTRAP_STAGE2, return_raw=True,
    )
    t_calib1 = time.time()
    f_multi_hat = calib["f_multi_calibrated"]
    converged_bracket = calib["converged_bracket"]
    print(f"    tempo calibrate_f_multi: {t_calib1 - t_calib0:.1f}s")
    print(f"    f_multi_hat = {f_multi_hat:.6f}")
    print(f"    converged_bracket = {converged_bracket}")
    print(f"    bracket: {calib['bracket']}")

    # ------------------------------------------------------------------
    # Gatilho 2 da Secao 6 -- converged_bracket False PARA a analise aqui,
    # nao prossegue para ajuste de a0/veredito (STOP, nao forcar).
    # ------------------------------------------------------------------
    at_boundary = min(abs(f_multi_hat - F_LO), abs(f_multi_hat - F_HI)) < XTOL
    trigger2_fired = bool((not converged_bracket) or at_boundary)

    if not converged_bracket:
        elapsed = time.time() - t0
        result = {
            "test_id": "SPARC-FMULTI-STAGE2",
            "preregistration_path": (
                "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/"
                "fmulti_selfcal_stage1/PREREGISTRATION_STAGE2.md"
            ),
            "STOPPED_PER_SECTION_6_TRIGGER_2": True,
            "reason": (
                "calib['converged_bracket'] == False -- a bisseccao NAO "
                "encontrou uma troca de sinal de delta_ancora(f_multi) no "
                "intervalo [f_lo, f_hi] declarado. Por instrucao explicita "
                "da Secao 4.2/6 item 2 do pre-registro, isto e' por si so' "
                "um gatilho adversarial de descoberta de nulo -- PARAR e "
                "reportar em vez de prosseguir a um veredito de a0."
            ),
            "n_discovery_used": int(n_sys),
            "n_mc": N_MC, "seed_stage2": SEED_STAGE2,
            "calibrate_f_multi_result_no_raw": {
                k: v for k, v in calib.items() if k != "final_raw"
            },
            "elapsed_seconds": elapsed,
        }
        with open(OUT_JSON, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print("\n*** converged_bracket=False -- PARANDO conforme Secao 6 "
              "item 2 do pre-registro. Resultado parcial salvo. ***")
        return result

    # ------------------------------------------------------------------
    print("\n[4] Passo 2 do pre-registro -- extraindo delta_obs-newt(bin) "
          "corrigido de calib['final_result']...")
    final_result = calib["final_result"]
    delta_corrected = np.array(final_result["delta_obs_newt_primary"])
    gN_bin_median = np.array(final_result["gN_bin_median_si"])
    n_sys_per_bin = final_result["n_systems_per_bin"]
    frac_has_multi = final_result["frac_has_multi"]
    frac_nonzero_wobble = final_result["frac_nonzero_wobble"]
    delta_ci95_lo = final_result.get("bootstrap", {}).get("ci95_lo")
    delta_ci95_hi = final_result.get("bootstrap", {}).get("ci95_hi")
    print(f"    delta_obs_newt_primary (corrigido) = "
          f"{[f'{x:+.4f}' for x in delta_corrected]}")
    print(f"    gN_bin_median_si = {gN_bin_median.tolist()}")
    print(f"    n_systems_per_bin = {n_sys_per_bin}")
    print(f"    frac_has_multi (no f_multi_hat) = {frac_has_multi:.4f}")
    print(f"    frac_nonzero_wobble = {frac_nonzero_wobble:.4f}")
    if delta_ci95_lo is not None:
        print(f"    IC95% delta (bootstrap n={N_BOOTSTRAP_STAGE2}, do proprio "
              f"final_result): lo={[f'{x:+.4f}' for x in delta_ci95_lo]} "
              f"hi={[f'{x:+.4f}' for x in delta_ci95_hi]}")

    # ------------------------------------------------------------------
    print("\n[5] Passo 3 do pre-registro -- fit_a0() em 2 pontos de partida...")
    a0_fit_x1 = sp.fit_a0(gN_bin_median, delta_corrected, x0=1.0)
    a0_fit_x5 = sp.fit_a0(gN_bin_median, delta_corrected, x0=5.0)
    print(f"    a0_fit (x0=1.0) = {a0_fit_x1}")
    print(f"    a0_fit (x0=5.0) = {a0_fit_x5}")
    x0_agreement = None
    x0_converged_same = False
    if a0_fit_x1 is not None and a0_fit_x5 is not None:
        x0_agreement = abs(a0_fit_x1 - a0_fit_x5) / max(abs(a0_fit_x1), abs(a0_fit_x5), 1e-30)
        x0_converged_same = x0_agreement < 1e-4
    print(f"    diferenca relativa entre pontos de partida = {x0_agreement}")
    print(f"    convergiram para o mesmo valor (rel_diff<1e-4)? {x0_converged_same}")
    a0_fit = a0_fit_x1 if a0_fit_x1 is not None else a0_fit_x5

    # ------------------------------------------------------------------
    print(f"\n[6] Passo 4-5 do pre-registro -- bootstrap_a0_refit() usando "
          f"calib['final_raw'] (n_bootstrap={N_BOOTSTRAP_STAGE2}, "
          f"seed={SEED_STAGE2 + 999_999})...")
    t_boot0 = time.time()
    ci = sp.bootstrap_a0_refit(
        calib["final_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP_STAGE2,
        seed=SEED_STAGE2 + 999_999, x0_list=X0_LIST,
    )
    t_boot1 = time.time()
    print(f"    tempo bootstrap_a0_refit: {t_boot1 - t_boot0:.1f}s")
    print(f"    ci['x0=1.0'] = {ci['x0=1.0']}")
    print(f"    ci['x0=5.0'] = {ci['x0=5.0']}")

    ci_lo_x1 = ci["x0=1.0"]["ci95_lo_si_m_s2"]
    ci_hi_x1 = ci["x0=1.0"]["ci95_hi_si_m_s2"]
    ci_lo_x5 = ci["x0=5.0"]["ci95_lo_si_m_s2"]
    ci_hi_x5 = ci["x0=5.0"]["ci95_hi_si_m_s2"]

    boot_x0_agree = bool(
        ci_lo_x1 is not None and ci_lo_x5 is not None
        and abs(ci_lo_x1 - ci_lo_x5) / max(abs(ci_lo_x1), abs(ci_lo_x5), 1e-30) < 0.05
        and abs(ci_hi_x1 - ci_hi_x5) / max(abs(ci_hi_x1), abs(ci_hi_x5), 1e-30) < 0.05
    )
    print(f"    x0=1.0 e x0=5.0 concordam no IC (tol relativa 5%)? {boot_x0_agree}")

    a0_ci95_lo = ci_lo_x1
    a0_ci95_hi = ci_hi_x1

    # ------------------------------------------------------------------
    print("\n[7] Regra de decisao -- camada MECANICA (Secao 5, primeira parte)...")
    if a0_ci95_lo is not None and a0_ci95_hi is not None:
        a0_A_survives_mech = bool(a0_ci95_lo <= A0_A <= a0_ci95_hi)
        a0_B_survives_mech = bool(a0_ci95_lo <= A0_B <= a0_ci95_hi)
    else:
        a0_A_survives_mech = False
        a0_B_survives_mech = False
    print(f"    IC95% a0 (x0=1.0, refit primario) = [{a0_ci95_lo}, {a0_ci95_hi}]")
    print(f"    a0_A ({A0_A:.6e}) dentro do IC? {a0_A_survives_mech}")
    print(f"    a0_B ({A0_B:.6e}) dentro do IC? {a0_B_survives_mech}")

    if a0_A_survives_mech and a0_B_survives_mech:
        verdict_mechanical = "INCONCLUSIVE_BOTH_SURVIVE"
    elif a0_A_survives_mech and not a0_B_survives_mech:
        verdict_mechanical = "H_A_SUPPORTED_H_B_FALSIFIED"
    elif a0_B_survives_mech and not a0_A_survives_mech:
        verdict_mechanical = "H_B_SUPPORTED_H_A_FALSIFIED"
    else:
        verdict_mechanical = "BOTH_FALSIFIED"
    print(f"    Veredito MECANICO (Secao 5, camada 1): {verdict_mechanical}")

    # ------------------------------------------------------------------
    print("\n[8] Camada INTERPRETATIVA obrigatoria (Secao 5, segunda parte) "
          f"-- dividir a0_fit e o IC95% pelo fator de vies residual "
          f"[{BIAS_FACTOR_LO}, {BIAS_FACTOR_HI}]x do Estagio 1...")
    interpretive_layer_applies = bool(verdict_mechanical != "INCONCLUSIVE_BOTH_SURVIVE")
    debiased_ci_lo = None
    debiased_ci_hi = None
    a0_A_survives_debiased = None
    a0_B_survives_debiased = None
    interpretive_override = False
    if interpretive_layer_applies and a0_ci95_lo is not None and a0_ci95_hi is not None:
        # Intervalo de-vies mais GENEROSO possivel: divide a borda inferior
        # pelo maior fator (1.6x, puxa mais para baixo) e a borda superior
        # pelo menor fator (1.4x, puxa menos para baixo) -- produz o
        # intervalo de-viesado mais LARGO fisicamente defensavel dado o
        # range de vies documentado, dando a H_A/H_B o beneficio maximo da
        # duvida antes de aceitar uma falsificacao limpa.
        debiased_ci_lo = a0_ci95_lo / BIAS_FACTOR_HI
        debiased_ci_hi = a0_ci95_hi / BIAS_FACTOR_LO
        a0_A_survives_debiased = bool(debiased_ci_lo <= A0_A <= debiased_ci_hi)
        a0_B_survives_debiased = bool(debiased_ci_lo <= A0_B <= debiased_ci_hi)
        interpretive_override = bool(
            (a0_A_survives_debiased and not a0_A_survives_mech)
            or (a0_B_survives_debiased and not a0_B_survives_mech)
        )
        print(f"    IC de-viesado (dividido por {BIAS_FACTOR_LO}-{BIAS_FACTOR_HI}x) = "
              f"[{debiased_ci_lo:.6e}, {debiased_ci_hi:.6e}]")
        print(f"    a0_A dentro do IC de-viesado? {a0_A_survives_debiased}")
        print(f"    a0_B dentro do IC de-viesado? {a0_B_survives_debiased}")
        print(f"    Camada interpretativa MUDA o veredito (override)? {interpretive_override}")
    else:
        print("    Camada interpretativa nao se aplica -- veredito mecanico ja "
              "e' INCONCLUSIVE_BOTH_SURVIVE (nenhuma falsificacao a re-checar).")

    if interpretive_override:
        verdict_final = "INCONCLUSIVO"
        verdict_final_reason = (
            "Veredito mecanico seria "
            f"{verdict_mechanical}, mas dividir a0_fit/IC95% pelo fator de "
            f"vies residual conhecido do Estagio 1 ({BIAS_FACTOR_LO}-"
            f"{BIAS_FACTOR_HI}x) traz a0_A e/ou a0_B de volta para dentro do "
            "intervalo -- por instrucao explicita da Secao 5 (camada "
            "interpretativa) do pre-registro, a falsificacao NAO pode ser "
            "aceita como limpa."
        )
    else:
        verdict_final = verdict_mechanical
        verdict_final_reason = (
            "Camada interpretativa nao aplicavel ou nao muda o veredito -- "
            "mesmo apos dividir pelo fator de vies residual "
            f"{BIAS_FACTOR_LO}-{BIAS_FACTOR_HI}x, a0_A/a0_B nao voltam para "
            "dentro do IC (ou o veredito mecanico ja era INCONCLUSIVE)."
        ) if interpretive_layer_applies else (
            "Veredito mecanico ja e' INCONCLUSIVE_BOTH_SURVIVE -- camada "
            "interpretativa nao se aplica por construcao (nao ha' "
            "falsificacao a re-checar)."
        )
    print(f"\n    *** VEREDITO FINAL (mecanico + interpretativo): {verdict_final} ***")
    print(f"    Razao: {verdict_final_reason}")

    # ------------------------------------------------------------------
    print("\n[9] Gatilhos adversariais da Secao 6 -- checando cada um explicitamente...")

    # Gatilho 1: a0_fit fora da faixa plausivel de AMBAS H_A e H_B por mais
    # de 1 ordem de grandeza.
    if a0_fit is not None and a0_fit > 0:
        log10_ratio_to_A = float(np.log10(a0_fit / A0_A))
        log10_ratio_to_B = float(np.log10(a0_fit / A0_B))
        trigger1_fired = bool(abs(log10_ratio_to_A) > 1.0 and abs(log10_ratio_to_B) > 1.0)
    else:
        log10_ratio_to_A = None
        log10_ratio_to_B = None
        trigger1_fired = True  # a0_fit invalido e' pior que so' fora de faixa

    # Gatilho 2 (ja' computado acima, mas re-registrado aqui por completude)
    # -- converged_bracket=True neste ponto (senao ja teriamos retornado).

    # Gatilho 3: f_multi_hat fora de 0.25-0.47.
    f_multi_in_literature_range = bool(
        F_MULTI_LITERATURE_LO <= f_multi_hat <= F_MULTI_LITERATURE_HI
    )
    f_multi_margin = (
        0.0 if f_multi_in_literature_range else
        (F_MULTI_LITERATURE_LO - f_multi_hat if f_multi_hat < F_MULTI_LITERATURE_LO
         else f_multi_hat - F_MULTI_LITERATURE_HI)
    )
    trigger3_fired = bool(not f_multi_in_literature_range and f_multi_margin > 0.1)

    # Gatilho 4: padrao de delta_obs-newt corrigido qualitativamente
    # inconsistente com a assinatura de vies do Estagio 1 (residuo pequeno,
    # 0.15-0.22 dex, concentrado nos bins de MENOR gN, mesma direcao/sinal
    # em todos os bins -- nao trocando de sinal entre bins adjacentes sem
    # razao fisica, nem excedendo 1 ordem de grandeza acima de 0.22 dex).
    max_abs_delta = float(np.max(np.abs(delta_corrected)))
    signs = np.sign(delta_corrected)
    # Bins com |delta| abaixo de SIGN_CHECK_EPS_DEX sao tratados como
    # "consistentes com zero" e EXCLUIDOS da checagem de uniformidade de
    # sinal -- necessario porque o bin-ancora e' CALIBRADO para delta~0 por
    # construcao (Passo 1), entao seu sinal (ruido numerico em torno de 0,
    # pode cair em qualquer lado) nao e' um sinal fisico real a comparar
    # contra os outros bins. Mesmo limiar de negligibilidade ja usado em
    # validate_b_recover_a0_with_contamination.py::_check_anchor_bin_mond_negligible
    # (0.01 dex). Sem esta exclusao, o proprio bin-ancora (por definicao
    # perto de zero) produziria um falso positivo de "troca de sinal" toda
    # vez que seu residuo numerico caisse do lado oposto por acaso.
    SIGN_CHECK_EPS_DEX = 0.01
    significant_mask = np.abs(delta_corrected) >= SIGN_CHECK_EPS_DEX
    if np.any(significant_mask):
        sig_signs = signs[significant_mask]
        all_same_sign_or_zero = bool(np.all(sig_signs == sig_signs[0]))
    else:
        all_same_sign_or_zero = True  # todos os bins consistentes com zero
    magnitude_within_order_of_magnitude = bool(max_abs_delta <= STAGE1_RESIDUAL_DEX_HI * 10.0)
    # "concentrado em MENOR gN" = bin 0 (menor gN) tem |delta| >= bin 4 (maior gN, ancora),
    # ja que o bin-ancora e' calibrado para delta~0 por construcao.
    concentrated_low_gN = bool(abs(delta_corrected[0]) >= abs(delta_corrected[ANCHOR_BIN]) - 1e-6)
    pattern_consistent_with_stage1_signature = bool(
        all_same_sign_or_zero and magnitude_within_order_of_magnitude
    )
    trigger4_fired = bool(not pattern_consistent_with_stage1_signature)

    # Gatilho 5: sensibilidade do IC a N_bootstrap/seed -- reexecutar com
    # semente diferente E com N_bootstrap reduzido, confirmar que o
    # veredito nao muda.
    print("    [Gatilho 5] Reexecutando bootstrap_a0_refit com semente "
          "diferente (mesmo N=2000)...")
    ci_alt_seed = sp.bootstrap_a0_refit(
        calib["final_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP_STAGE2,
        seed=SEED_STAGE2 + 999_999 + 1, x0_list=(1.0,),
    )
    print("    [Gatilho 5] Reexecutando bootstrap_a0_refit com N_bootstrap "
          "reduzido (N=1000, mesma semente base)...")
    ci_reduced_n = sp.bootstrap_a0_refit(
        calib["final_raw"], n_bins=5, n_bootstrap=1000,
        seed=SEED_STAGE2 + 999_999, x0_list=(1.0,),
    )

    def _verdict_from_ci(lo, hi):
        if lo is None or hi is None:
            return None, None
        a_surv = bool(lo <= A0_A <= hi)
        b_surv = bool(lo <= A0_B <= hi)
        if a_surv and b_surv:
            v = "INCONCLUSIVE_BOTH_SURVIVE"
        elif a_surv:
            v = "H_A_SUPPORTED_H_B_FALSIFIED"
        elif b_surv:
            v = "H_B_SUPPORTED_H_A_FALSIFIED"
        else:
            v = "BOTH_FALSIFIED"
        return v, (a_surv, b_surv)

    v_alt_seed, surv_alt_seed = _verdict_from_ci(
        ci_alt_seed["x0=1.0"]["ci95_lo_si_m_s2"], ci_alt_seed["x0=1.0"]["ci95_hi_si_m_s2"],
    )
    v_reduced_n, surv_reduced_n = _verdict_from_ci(
        ci_reduced_n["x0=1.0"]["ci95_lo_si_m_s2"], ci_reduced_n["x0=1.0"]["ci95_hi_si_m_s2"],
    )
    trigger5_fired = bool(
        (v_alt_seed is not None and v_alt_seed != verdict_mechanical)
        or (v_reduced_n is not None and v_reduced_n != verdict_mechanical)
    )
    print(f"    veredito mecanico original: {verdict_mechanical}")
    print(f"    veredito com semente alternativa: {v_alt_seed} "
          f"(IC=[{ci_alt_seed['x0=1.0']['ci95_lo_si_m_s2']}, "
          f"{ci_alt_seed['x0=1.0']['ci95_hi_si_m_s2']}])")
    print(f"    veredito com N_bootstrap=1000: {v_reduced_n} "
          f"(IC=[{ci_reduced_n['x0=1.0']['ci95_lo_si_m_s2']}, "
          f"{ci_reduced_n['x0=1.0']['ci95_hi_si_m_s2']}])")
    print(f"    Gatilho 5 (IC sensivel a N_bootstrap/seed)? {trigger5_fired}")

    print(f"\n    RESUMO DOS GATILHOS DA SECAO 6:")
    print(f"    1. a0_fit fora de ambas H_A/H_B por >1 ordem de grandeza: {trigger1_fired}")
    print(f"    2. converged_bracket=False ou f_multi_hat na borda do bracket: {trigger2_fired}")
    print(f"    3. f_multi_hat fora de 0.25-0.47 (margem>0.1): {trigger3_fired}")
    print(f"    4. padrao de delta_obs-newt inconsistente com assinatura Estagio 1: {trigger4_fired}")
    print(f"    5. IC sensivel a N_bootstrap/seed: {trigger5_fired}")

    # ------------------------------------------------------------------
    print("\n[10] Checagem secundaria de consistencia RUWE (Secao 4.1 "
          "passo 7, Secao 2 -- informativa, NAO parte da regra de decisao)...")
    ruwe_flagged = (RUWE1 > RUWE_FLAG_THRESHOLD) | (RUWE2 > RUWE_FLAG_THRESHOLD)
    frac_ruwe_flagged = float(ruwe_flagged.mean())
    print(f"    fracao de sistemas com RUWE1>{RUWE_FLAG_THRESHOLD} ou "
          f"RUWE2>{RUWE_FLAG_THRESHOLD}: {frac_ruwe_flagged:.4f}")
    print(f"    (comparar qualitativamente com frac_has_multi={frac_has_multi:.4f} "
          f"no f_multi_hat calibrado -- consistencia, nao correcao primaria)")

    # ------------------------------------------------------------------
    elapsed = time.time() - t0
    print(f"\nTempo total: {elapsed:.1f}s")

    # ------------------------------------------------------------------
    result = {
        "test_id": "SPARC-FMULTI-STAGE2",
        "preregistration_path": (
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/"
            "fmulti_selfcal_stage1/PREREGISTRATION_STAGE2.md"
        ),
        "decision_id_lock": "DISC-DEC-029",
        "analysis_script": (
            "05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/"
            "fmulti_selfcal_stage1/analysis/run_stage2_primary_analysis.py"
        ),
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "section_9_3_self_grep_check": grep_result,
        "n_discovery_used": int(n_sys),
        "holdout_seal_note": (
            "discovery_holdout_split.json foi aberto SOMENTE para extrair "
            "'discovery_pair_ids' e 'n_discovery' -- as chaves "
            "'holdout_pair_ids' e 'n_holdout' NUNCA foram acessadas neste "
            "script, em nenhum ponto (verificado pelo grep 9.3 acima)."
        ),
        "constants": {
            "G_SI": dc.G_SI, "MSUN_KG": dc.MSUN_KG, "AU_M": dc.AU_M,
            "mas_yr_to_km_s_per_pc": dc.MAS_YR_TO_KM_S_PER_PC,
            "c_light_m_s": C_LIGHT, "H0_km_s_Mpc": 70.0, "H0_si_s^-1": H0_SI,
        },
        "a0_A_holographic_bridge": {"formula": "c*H0/(2*pi)", "value_si_m_s2": A0_A},
        "a0_B_mond_emergence": {"formula": "c*H0", "value_si_m_s2": A0_B},
        "parameters_section_4_6": {
            "bin_edges_log10_gN": BIN_EDGES.tolist(),
            "anchor_bin": ANCHOR_BIN, "n_mc": N_MC, "seed_stage2": SEED_STAGE2,
            "n_bootstrap_stage2": N_BOOTSTRAP_STAGE2,
            "f_lo": F_LO, "f_hi": F_HI, "xtol": XTOL,
            "include_wobble": INCLUDE_WOBBLE,
            "real_gets_astrometric_noise": REAL_GETS_ASTROMETRIC_NOISE,
            "x0_list": list(X0_LIST),
        },
        "step1_calibrate_f_multi": {
            "f_multi_calibrated": f_multi_hat,
            "converged_bracket": converged_bracket,
            "bracket": calib["bracket"],
            "anchor_bin": calib["anchor_bin"],
            "elapsed_seconds": t_calib1 - t_calib0,
        },
        "step2_delta_obs_newt_corrected": {
            "delta_obs_newt_primary": delta_corrected.tolist(),
            "gN_bin_median_si": gN_bin_median.tolist(),
            "n_systems_per_bin": n_sys_per_bin,
            "frac_has_multi": frac_has_multi,
            "frac_nonzero_wobble": frac_nonzero_wobble,
            "delta_ci95_lo_from_final_result_bootstrap": delta_ci95_lo,
            "delta_ci95_hi_from_final_result_bootstrap": delta_ci95_hi,
        },
        "step3_fit_a0": {
            "a0_fit_x0_1p0_si_m_s2": a0_fit_x1,
            "a0_fit_x0_5p0_si_m_s2": a0_fit_x5,
            "relative_disagreement": x0_agreement,
            "converged_to_same_value": x0_converged_same,
            "a0_fit_used_si_m_s2": a0_fit,
        },
        "step4_5_bootstrap_a0_refit": {
            "n_bootstrap": N_BOOTSTRAP_STAGE2,
            "seed": SEED_STAGE2 + 999_999,
            "source": "calib['final_raw'] (NAO reconstruido manualmente -- DISC-DEC-029)",
            "ci_x0_1p0": ci["x0=1.0"],
            "ci_x0_5p0": ci["x0=5.0"],
            "x0_starting_points_agree": boot_x0_agree,
            "elapsed_seconds": t_boot1 - t_boot0,
        },
        "decision_section5": {
            "mechanical_layer": {
                "a0_ci95_used_lo_si_m_s2": a0_ci95_lo,
                "a0_ci95_used_hi_si_m_s2": a0_ci95_hi,
                "a0_A_within_ci95": a0_A_survives_mech,
                "a0_B_within_ci95": a0_B_survives_mech,
                "verdict_mechanical": verdict_mechanical,
            },
            "interpretive_layer": {
                "applies": interpretive_layer_applies,
                "bias_factor_range": [BIAS_FACTOR_LO, BIAS_FACTOR_HI],
                "debiased_ci95_lo_si_m_s2": debiased_ci_lo,
                "debiased_ci95_hi_si_m_s2": debiased_ci_hi,
                "a0_A_within_debiased_ci95": a0_A_survives_debiased,
                "a0_B_within_debiased_ci95": a0_B_survives_debiased,
                "override_applied": interpretive_override,
            },
            "verdict_final": verdict_final,
            "verdict_final_reason": verdict_final_reason,
        },
        "section6_adversarial_triggers": {
            "trigger1_a0_outside_both_by_1oom": {
                "fired": trigger1_fired,
                "log10_ratio_a0fit_to_A0_A": log10_ratio_to_A,
                "log10_ratio_a0fit_to_A0_B": log10_ratio_to_B,
            },
            "trigger2_not_converged_or_at_boundary": {
                "fired": trigger2_fired,
                "converged_bracket": converged_bracket,
                "f_multi_hat": f_multi_hat, "f_lo": F_LO, "f_hi": F_HI, "xtol": XTOL,
            },
            "trigger3_f_multi_outside_literature_range": {
                "fired": trigger3_fired,
                "f_multi_hat": f_multi_hat,
                "literature_range": [F_MULTI_LITERATURE_LO, F_MULTI_LITERATURE_HI],
                "margin_beyond_range": f_multi_margin,
            },
            "trigger4_pattern_inconsistent_with_stage1_signature": {
                "fired": trigger4_fired,
                "delta_obs_newt_primary": delta_corrected.tolist(),
                "max_abs_delta_dex": max_abs_delta,
                "all_same_sign_across_bins_excluding_near_zero": all_same_sign_or_zero,
                "sign_check_eps_dex": SIGN_CHECK_EPS_DEX,
                "bins_excluded_from_sign_check_as_near_zero": (~significant_mask).tolist(),
                "magnitude_within_1_order_of_magnitude_of_stage1_range": magnitude_within_order_of_magnitude,
                "concentrated_in_low_gN_bin_vs_anchor": concentrated_low_gN,
                "stage1_reference_residual_dex_range": [STAGE1_RESIDUAL_DEX_LO, STAGE1_RESIDUAL_DEX_HI],
            },
            "trigger5_ci_sensitive_to_bootstrap_choice": {
                "fired": trigger5_fired,
                "verdict_mechanical_original": verdict_mechanical,
                "verdict_alt_seed_N2000": v_alt_seed,
                "ci_alt_seed_N2000": ci_alt_seed["x0=1.0"],
                "verdict_reduced_N1000": v_reduced_n,
                "ci_reduced_N1000": ci_reduced_n["x0=1.0"],
            },
            "any_trigger_fired": bool(
                trigger1_fired or trigger2_fired or trigger3_fired
                or trigger4_fired or trigger5_fired
            ),
        },
        "secondary_consistency_check_ruwe": {
            "description": (
                "Checagem de consistencia SECUNDARIA (Secao 4.1 passo 7 / "
                "METHODOLOGY_ADDENDUM.md Secao 2 item 4) -- NAO parte da "
                "regra de decisao mecanica ou interpretativa da Secao 5, "
                "so' contexto informativo."
            ),
            "ruwe_flag_threshold": RUWE_FLAG_THRESHOLD,
            "frac_systems_ruwe_flagged": frac_ruwe_flagged,
            "frac_has_multi_at_f_multi_hat": frac_has_multi,
        },
        "requires_null_discovery_debunker_pass": bool(
            verdict_final != "BOTH_FALSIFIED_NO_SIGNAL_ABOVE_NOISE"
        ),
        "requires_null_discovery_debunker_pass_note": (
            "Secao 6, ultimo paragrafo: QUALQUER veredito diferente de 'nenhum "
            "sinal detectavel acima do ruido' (isto e', qualquer "
            "H_A_FALSIFICADA, H_B_FALSIFICADA, BOTH_FALSIFIED, INCONCLUSIVO, "
            "ou suporte a H_A/H_B) deve passar pelo papel de debunker de "
            "METHODOLOGY_EXTENSIONS.md Secao 5 antes de ser catalogado -- "
            "SEPARADO da reexecucao adversarial padrao do AGENTS.md passo 7. "
            "Este resultado NAO passou por essa etapa -- pendente, a ser "
            "arranjada pela sessao orquestradora."
        ),
        "elapsed_seconds": elapsed,
    }

    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nResultado completo salvo em {OUT_JSON}")
    return result


if __name__ == "__main__":
    main()
