"""Parte 2 (debunker) -- itens (a) e RUWE cross-check.

Investiga, usando SOMENTE a amostra de descoberta (30.203 sistemas, jamais
o holdout selado nem catalog.parquet bruto -- ver nota de escopo abaixo):

(a) Os cortes de qualidade ja aplicados (R<0.01, concordancia de distancia
    3-sigma, erro relativo de PM<0.01 -- nenhum deles e' um corte de RUWE
    direto, confirmado por leitura de apply_quality_cuts.py) poderiam
    estar preferencialmente excluindo sistemas com companheiras ocultas
    mais obvias (RUWE alto)? Medido aqui por: (i) fracao residual de
    RUWE>1.4 na amostra JA CORTADA; (ii) correlacao, DENTRO da amostra ja
    cortada, entre RUWE e as duas variaveis usadas nos cortes (erro
    relativo de PM, discordancia de distancia em unidades de sigma) --
    um "gradiente perto da borda do corte" e' evidencia direta de que o
    corte trunca RUWE alto, mesmo sem ser um corte de RUWE explicito.

(d) RUWE cross-check: delta_obs-newt(bin) separado para o subconjunto
    RUWE-alto vs RUWE-baixo, ANTES e DEPOIS da correcao com f_multi_hat
    calibrado pela Parte 1 (aplicado uniformemente aos dois
    subconjuntos) -- mesmo espirito do check RUWE decisivo do fechamento
    v2 de SPARC-004 (../../../PREREGISTRATION.md Secao 7d), mas agora
    comparando a correcao unica (media da amostra inteira) contra os dois
    subconjuntos separadamente: se RUWE-alto continua mostrando residuo
    MAIOR que RUWE-baixo mesmo apos a MESMA correcao de f_multi ser
    aplicada aos dois, isso e' evidencia de um confundidor que a
    calibracao (que so' ajusta UM f_multi escalar para a amostra inteira)
    nao capturou -- analogo em espirito ao check decisivo de v2.

Escopo/disciplina do holdout: este script chama
load_discovery_sample()/build_pipeline_inputs() do driver da Parte 1
(adversarial_driver_stage2.py) -- MESMO ponto de contato unico com
discovery_holdout_split.json, MESMA disciplina (so' discovery_pair_ids
extraido, holdout_pair_ids nunca referenciado). NENHUM arquivo deste
script abre catalog.parquet (catalogo bruto El-Badry completo, 1.8M
pares, PRE-corte-de-qualidade) -- decisao deliberada e conservadora desta
sessao adversarial: mesmo catalog.parquet NAO sendo tecnicamente os
"12.944 sistemas do holdout selado" (e' um superconjunto muito maior,
anterior a qualquer split), a tarefa desta sessao pediu explicitamente
grep de catalog.parquet como um dos nomes proibidos (mesmo padrao ja'
usado para o holdout) -- tratado aqui com a mesma disciplina por cautela,
nao por exigencia textual do proprio PREREGISTRATION_STAGE2.md (que so'
proibe holdout_pair_ids especificamente). Consequencia pratica: a
comparacao do item (a) usa SOMENTE a distribuicao de RUWE DENTRO da
amostra ja cortada (nao pode comparar diretamente contra a populacao
PRE-corte, que exigiria abrir o catalogo bruto) -- suprido por
literatura externa (Lindegren 2018, El-Badry+2021) para o baseline
populacional, citada explicitamente no relatorio final, nao aqui no
codigo.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))
import adversarial_driver_stage2 as drv  # noqa: E402  (reusa load_discovery_sample, build_pipeline_inputs)
from selfcal_pipeline import run_delta_obs_newt_selfcal  # noqa: E402

OUT_DIR = THIS_DIR.parent / "results"
OUT_DIR.mkdir(exist_ok=True)

RUWE_THRESHOLD = 1.4  # Lindegren (2018), limiar padrao de "solucao astrometrica de boa qualidade"
N_MC_CHECK = 200        # mesmo N_MC do Passo 1 da Parte 1 -- consistencia de escala de ruido MC
N_BOOTSTRAP_CHECK = 500  # reduzido (checagem exploratoria, nao parte da regra de decisao pre-registrada)


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_f_multi_hat() -> float:
    """Le o f_multi_hat da PROPRIA reproducao independente (Parte 1),
    nunca do resultado do agente primario -- mantem o debunker
    inteiramente ancorado na minha propria reexecucao."""
    result_path = OUT_DIR / "result_adversarial_stage2.json"
    with open(result_path) as f:
        r = json.load(f)
    return float(r["f_multi_hat"])


def item_a_quality_cut_ruwe_analysis(disc: pd.DataFrame) -> dict:
    log("--- Item (a): cortes de qualidade vs. RUWE ---")

    ruwe_max = disc[["RUWE1", "RUWE2"]].max(axis=1).to_numpy(dtype=np.float64)
    ruwe_either = ruwe_max > RUWE_THRESHOLD
    frac_ruwe_high = float(ruwe_either.mean())
    log(f"  fracao com max(RUWE1,RUWE2)>{RUWE_THRESHOLD} NA AMOSTRA JA CORTADA: "
        f"{frac_ruwe_high:.4f} ({int(ruwe_either.sum())}/{len(disc)})")

    ruwe1 = disc["RUWE1"].to_numpy(dtype=np.float64)
    ruwe2 = disc["RUWE2"].to_numpy(dtype=np.float64)
    frac_ruwe1_high = float((ruwe1 > RUWE_THRESHOLD).mean())
    frac_ruwe2_high = float((ruwe2 > RUWE_THRESHOLD).mean())
    frac_ruwe_both_high = float(((ruwe1 > RUWE_THRESHOLD) & (ruwe2 > RUWE_THRESHOLD)).mean())
    log(f"  fracao RUWE1>1.4: {frac_ruwe1_high:.4f}  RUWE2>1.4: {frac_ruwe2_high:.4f}  "
        f"ambos>1.4: {frac_ruwe_both_high:.4f}")

    # ---- correlacao DENTRO da amostra ja cortada entre RUWE e as duas
    #      variaveis usadas pelos cortes (erro relativo de PM, discordancia
    #      de distancia em unidades de sigma) -- reconstruidas aqui
    #      identicamente a apply_quality_cuts.py (LOCKED, so' lido, nao
    #      editado), ja que a amostra ja cortada nao carrega essas colunas
    #      derivadas diretamente. ----
    d1_pc = 1000.0 / disc["Plx1"].to_numpy(dtype=np.float64)
    d2_pc = 1000.0 / disc["Plx2"].to_numpy(dtype=np.float64)
    sigma_d1 = d1_pc * (disc["e_Plx1"].to_numpy(dtype=np.float64) / disc["Plx1"].to_numpy(dtype=np.float64))
    sigma_d2 = d2_pc * (disc["e_Plx2"].to_numpy(dtype=np.float64) / disc["Plx2"].to_numpy(dtype=np.float64))
    dist_disagreement_nsigma = np.abs(d1_pc - d2_pc) / np.sqrt(sigma_d1 ** 2 + sigma_d2 ** 2)

    pm1_relerr = (np.sqrt(disc["e_pmRA1"] ** 2 + disc["e_pmDE1"] ** 2)
                  / disc["pmRA1"].abs().clip(lower=1e-9)).to_numpy(dtype=np.float64)
    pm2_relerr = (np.sqrt(disc["e_pmRA2"] ** 2 + disc["e_pmDE2"] ** 2)
                  / disc["pmRA2"].abs().clip(lower=1e-9)).to_numpy(dtype=np.float64)
    pm_relerr_max = np.maximum(pm1_relerr, pm2_relerr)

    rho_pm, p_pm = stats.spearmanr(ruwe_max, pm_relerr_max)
    rho_dist, p_dist = stats.spearmanr(ruwe_max, dist_disagreement_nsigma)
    log(f"  Spearman rho(RUWE_max, PM_relerr_max) = {rho_pm:.4f} (p={p_pm:.2e})")
    log(f"  Spearman rho(RUWE_max, dist_disagreement_nsigma) = {rho_dist:.4f} (p={p_dist:.2e})")

    # ---- gradiente perto da borda do corte: mediana de RUWE_max no
    #      quartil dos sistemas MAIS PROXIMOS do limiar de corte (0.01 de
    #      PM_relerr, 3-sigma de discordancia) vs. no quartil MAIS
    #      FOLGADO -- se o corte estivesse truncando RUWE alto, sistemas
    #      perto da borda devem ter RUWE sistematicamente mais alto que
    #      sistemas bem dentro do corte. ----
    def _edge_gradient(variable, label):
        order = np.argsort(-variable)  # do mais PROXIMO da borda (maior valor, ja que o corte e' "<") para o mais folgado
        n = len(variable)
        q1_idx = order[: n // 4]           # quartil mais proximo da borda de corte
        q4_idx = order[3 * n // 4:]        # quartil mais folgado
        med_edge = float(np.median(ruwe_max[q1_idx]))
        med_slack = float(np.median(ruwe_max[q4_idx]))
        log(f"  {label}: RUWE_max mediana no quartil PROXIMO da borda={med_edge:.4f} "
            f"vs. quartil FOLGADO={med_slack:.4f} (razao={med_edge/med_slack:.4f})")
        return dict(median_ruwe_near_edge_quartile=med_edge,
                     median_ruwe_slack_quartile=med_slack,
                     ratio=med_edge / med_slack)

    edge_pm = _edge_gradient(pm_relerr_max, "corte PM_relerr<0.01")
    edge_dist = _edge_gradient(dist_disagreement_nsigma, "corte discordancia_distancia<3sigma")

    return dict(
        ruwe_threshold=RUWE_THRESHOLD,
        frac_ruwe_max_high_post_cut=frac_ruwe_high,
        frac_ruwe1_high=frac_ruwe1_high,
        frac_ruwe2_high=frac_ruwe2_high,
        frac_both_ruwe_high=frac_ruwe_both_high,
        spearman_ruwe_vs_pm_relerr=dict(rho=float(rho_pm), p=float(p_pm)),
        spearman_ruwe_vs_dist_disagreement=dict(rho=float(rho_dist), p=float(p_dist)),
        edge_gradient_pm_cut=edge_pm,
        edge_gradient_dist_cut=edge_dist,
        note="baseline populacional pre-corte (Lindegren 2018, ~4-6% em levantamentos "
             "de aglomerados; El-Badry+2021 nota RUWE>1.4 como indicador de "
             "companheira nao resolvida) citado no relatorio final a partir de "
             "busca externa, NAO de catalog.parquet (nao aberto por este script).",
    )


def item_d_ruwe_split_delta_check(inputs: dict, disc: pd.DataFrame, f_multi_hat: float) -> dict:
    log("--- Item (d): RUWE cross-check (delta_obs-newt RUWE-alto vs RUWE-baixo) ---")
    ruwe_max = disc[["RUWE1", "RUWE2"]].max(axis=1).to_numpy(dtype=np.float64)
    mask_high = ruwe_max > RUWE_THRESHOLD
    mask_low = ~mask_high
    log(f"  n_RUWE_alto={int(mask_high.sum())}  n_RUWE_baixo={int(mask_low.sum())}")

    from delta_obs_newt import BIN_EDGES_LOG_GN_SPARC003

    results = {}
    for label, mask in (("ruwe_high", mask_high), ("ruwe_low", mask_low)):
        sub_inputs = {k: (v[mask] if hasattr(v, "__len__") and len(v) == len(disc) else v)
                      for k, v in inputs.items()}
        for f_label, f_val in (("raw_f0", 0.0), ("corrected_f_hat", f_multi_hat)):
            t0 = time.time()
            out = run_delta_obs_newt_selfcal(
                **sub_inputs, f_multi=f_val, bin_edges=BIN_EDGES_LOG_GN_SPARC003,
                n_mc=N_MC_CHECK, seed=drv.SEED_STAGE2 + 31_337,
                include_wobble=True, real_gets_astrometric_noise=False,
                n_bootstrap=N_BOOTSTRAP_CHECK,
            )
            dt = time.time() - t0
            log(f"  [{label}/{f_label}] delta_obs_newt={out['delta_obs_newt_primary']} "
                f"(n_sys_per_bin={out['n_systems_per_bin']}, {dt:.1f}s)")
            results[f"{label}__{f_label}"] = dict(
                delta_obs_newt_primary=out["delta_obs_newt_primary"],
                gN_bin_median_si=out["gN_bin_median_si"],
                n_systems_per_bin=out["n_systems_per_bin"],
                bootstrap_ci95_lo=out["bootstrap"]["ci95_lo"],
                bootstrap_ci95_hi=out["bootstrap"]["ci95_hi"],
            )

    # diferenca RUWE-alto menos RUWE-baixo, bin a bin, ANTES e DEPOIS da correcao
    d_raw_high = np.array(results["ruwe_high__raw_f0"]["delta_obs_newt_primary"])
    d_raw_low = np.array(results["ruwe_low__raw_f0"]["delta_obs_newt_primary"])
    d_corr_high = np.array(results["ruwe_high__corrected_f_hat"]["delta_obs_newt_primary"])
    d_corr_low = np.array(results["ruwe_low__corrected_f_hat"]["delta_obs_newt_primary"])

    diff_raw = (d_raw_high - d_raw_low).tolist()
    diff_corr = (d_corr_high - d_corr_low).tolist()
    log(f"  diferenca RUWE_alto - RUWE_baixo, delta_obs-newt CRU (f=0): {diff_raw}")
    log(f"  diferenca RUWE_alto - RUWE_baixo, delta_obs-newt CORRIGIDO (f={f_multi_hat:.4f}): {diff_corr}")

    return dict(
        ruwe_threshold=RUWE_THRESHOLD,
        f_multi_hat_used=f_multi_hat,
        n_bootstrap_check=N_BOOTSTRAP_CHECK,
        n_mc_check=N_MC_CHECK,
        by_subsample=results,
        diff_ruwe_high_minus_low_raw=diff_raw,
        diff_ruwe_high_minus_low_corrected=diff_corr,
    )


def main() -> None:
    t0 = time.time()
    f_multi_hat = load_f_multi_hat()
    log(f"f_multi_hat (da minha propria Parte 1) = {f_multi_hat:.4f}")

    disc = drv.load_discovery_sample()
    inputs = drv.build_pipeline_inputs(disc)

    a_result = item_a_quality_cut_ruwe_analysis(disc)
    d_result = item_d_ruwe_split_delta_check(inputs, disc, f_multi_hat)

    out = dict(
        f_multi_hat_reference=f_multi_hat,
        item_a_quality_cuts_vs_ruwe=a_result,
        item_d_ruwe_cross_check=d_result,
        runtime_seconds=time.time() - t0,
    )
    out_path = OUT_DIR / "result_debunker_quality_cuts_ruwe.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    log(f"resultado escrito em {out_path}")
    log(f"=== concluido em {time.time()-t0:.1f}s ===")


if __name__ == "__main__":
    main()
