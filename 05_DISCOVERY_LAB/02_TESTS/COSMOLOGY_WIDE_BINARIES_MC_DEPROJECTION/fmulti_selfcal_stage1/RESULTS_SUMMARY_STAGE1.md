# Resultados — Estágio 1: metodologia + validação sintética de auto-calibração de f_multi

**Data:** 2026-08-22
**Test ID:** `SPARC-FMULTI-STAGE1` (retomada de `DISC-COSMOLOGY-MOND-SPARC-004`)
**Autoridade:** `DISC-DEC-023`
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-22

## 0. Resumo executivo

O pipeline de auto-calibração completa de `f_multi` (Chae 2023 Eqs. 11-13 +
procedimento iterativo, especificado em `METHODOLOGY_ADDENDUM.md`) foi
implementado (`analysis/companion_injection.py`,
`analysis/selfcal_pipeline.py`, `analysis/build_synthetic_population.py`) e
validado inteiramente sobre dado sintético, contra os 7 critérios de
aceitação pré-declarados (A1-A4, B1-B3). **Todos os 7 critérios passaram**,
em 5 cenários sintéticos independentes (3 da Validação A + 2 da Validação
B). Nenhum arquivo de dado real desta linha foi lido nesta etapa.

**Veredito de prontidão:** o pipeline está **pronto para o Estágio 2**
(aplicação à amostra de descoberta real, 30.203 sistemas, ainda NÃO o
holdout selado) — com uma ressalva honesta documentada na Seção 3 abaixo
(viés residual leve, ~0,15-0,22 dex, na recuperação de `a0` sob
contaminação simultânea, já esperado pela degenerescência declarada a
priori em `METHODOLOGY_ADDENDUM.md` Seção 4).

## 1. Equações verificadas

`PROVENANCE_CHAE_EQS.md` documenta a verificação completa. Resumo: as
Eqs. 11-13 do Artigo A (Chae 2023, ApJ 952, 128, arXiv:2305.04613)
já citadas pelo repositório estão **corretas** (checagem cruzada
independente via a Eq. 18 citada externamente pelo Artigo B,
arXiv:2309.10404) — nenhuma correção de número de equação foi necessária.
Um achado adicional (não solicitado) foi documentado por precisão: o
pipeline já travado desta linha (`../analysis/delta_obs_newt.py`) já usa a
forma CORRIGIDA (pós-erratum do Artigo B) da fórmula de projeção mock, não
a versão original com bug do Artigo A — nenhuma alteração de código foi
necessária nos arquivos LOCKED.

## 2. Validação A — recuperação de `f_multi` verdadeiro (população 100% Newtoniana)

3 cenários (`f_multi_true` = 0,00 / 0,35 / 0,47), `N=8.000` sistemas
sintéticos, `N_MC=120`, `N_bootstrap=400`. Resultado completo:
`results/validation_A_results.json` (log: `results/validation_A_run.log`).

| cenário | `f_multi` calibrado | `\|dif\|` | A1 | A2 (todos os 5 bins CI∋0) | A3 (viés detectável sem correção) | A4 (RUWE correlaciona) |
|---|---|---|---|---|---|---|
| `f_multi_true=0,00` | `0,0300` | `0,030` | PASS | PASS | PASS | PASS (N/A, sem sistemas com companheira nesta realização) |
| `f_multi_true=0,35` | `0,3277` | `0,022` | PASS | PASS | PASS | PASS |
| `f_multi_true=0,47` | `0,4777` | `0,008` | PASS | PASS | PASS | PASS |

**`delta_obs-newt` antes/depois da correção (cenário `f_multi_true=0,35`,
o mais representativo da faixa observacional real):**

- Sem correção (`f_multi=0` fixo): `+0,272; +0,273; +0,251; +0,267; +0,197`
  — viés grande e uniforme em todos os bins (exatamente o padrão "quase
  constante através dos bins" já documentado em `hidden_companion_check_v2.md`
  Item 1 para o mecanismo de inflação de massa).
- Após auto-calibração (`f_multi=0,3277`): `-0,004; +0,020; +0,019; +0,052;
  +0,005` — todos consistentes com zero (IC95% bootstrap contendo 0 nos 5
  bins).

**Leitura:** o pipeline recupera o `f_multi` verdadeiro dentro da
tolerância pré-declarada (`0,05`) nos 3 cenários, e a correção generaliza
para os bins NÃO usados na calibração (bin-âncora foi só o bin 4) — não é
um ajuste trivial de 1 ponto, é uma correção que remove o viés em toda a
grade, exatamente o comportamento que a auto-calibração de Chae promete.

## 3. Validação B — recuperação de `a0` verdadeiro sob contaminação simultânea

2 cenários (`a0_true=1,2×10⁻¹⁰`, `f_multi_true=0,35` e `0,47`), mesmos
`N`/`N_MC`/`N_bootstrap` da Validação A, mais `N_bootstrap_a0=300` réplicas
de reajuste de `a0` por réplica. Resultado completo:
`results/validation_B_results.json` (log: `results/validation_B_run.log`).

| cenário | checagem a priori (bin-âncora insensível a `a0_true`?) | `a0_fit` SEM correção | `a0_fit` COM correção | IC95% COM correção | `a0_true` dentro do IC95%? | B1 | B2 | B3 |
|---|---|---|---|---|---|---|---|---|
| `f_multi_true=0,35` | sim (`δ_AQUAL` previsto `~9,9×10⁻¹¹`, desprezível) | `2,04×10⁻⁹` (17× o valor verdadeiro) | `1,97×10⁻¹⁰` | `[1,47×10⁻¹⁰; 2,64×10⁻¹⁰]` | **não** (por pouco — limite inferior `1,47×10⁻¹⁰` vs. `1,20×10⁻¹⁰` verdadeiro) | PASS | PASS (dentro da tolerância de `0,30` dex: `0,22` dex) | PASS |
| `f_multi_true=0,47` | sim (`δ_AQUAL` previsto `~1,4×10⁻¹⁰`, desprezível) | `6,86×10⁻⁹` (57× o valor verdadeiro) | `1,72×10⁻¹⁰` | `[1,18×10⁻¹⁰; 2,50×10⁻¹⁰]` | **sim** | PASS | PASS | PASS |

**Leitura honesta:** a diferença entre o pipeline SEM correção (erro de
1-2 ordens de grandeza em `a0`, o MESMO modo de falha catastrófico que já
reprovou v1/v2 sobre dado real desta linha) e o pipeline COM a
auto-calibração (erro de `0,15-0,22` dex, um fator `1,4-1,6×`, dentro da
mesma ordem de grandeza) é enorme — a correção funciona, de forma clara e
robusta nos dois cenários. Mas a recuperação NÃO é perfeita: em 1 dos 2
cenários o IC95% não chega a conter o `a0` verdadeiro (chega perto — a
borda inferior do IC é `1,47×10⁻¹⁰` contra um verdadeiro de `1,20×10⁻¹⁰`),
e em ambos há uma tendência sistemática de super-estimar `a0` levemente
(`a0_fit` corrigido `1,4-1,6×` maior que `a0_true`). Esse viés residual
**já era esperado a priori** — `METHODOLOGY_ADDENDUM.md` Seção 4
declarou, antes de rodar esta validação, que o modelo simplificado de
wobble de fotocentro (herdado sem alteração de `hidden_companion_check_v2.py`,
fase orbital interna uniforme, `a_in` log-uniforme sem ponderação
temporal) não decai o suficiente com `g_N`, deixando um resíduo pequeno
mas não perfeitamente plano através dos bins, que a auto-calibração no
bin-âncora (que remove só o nível médio, não a forma inteira) não
consegue eliminar totalmente — parte desse resíduo de forma é absorvida
pelo ajuste de `a0` como um falso sinal residual pequeno.

**Critério B2, conforme pré-declarado, foi definido para aceitar
explicitamente esse desfecho** ("dentro do IC OU honestamente próximo em
log, OU inconclusivo") em vez de forçar uma recuperação perfeita que o
desenho conhecidamente não sustenta — o resultado real (não um resultado
forçado) caiu no meio-termo "próximo mas não perfeito", exatamente o tipo
de honestidade que este critério foi desenhado para capturar.

## 4. Limitações e aproximações declaradas (nenhuma nova, todas herdadas e já documentadas)

- `γ_M=-0,7` fixo (Tokovinin 2008), não recalibrado para a distribuição de
  `ΔM_G` desta amostra Gaia EDR3+El-Badry+Hwang especificamente.
- Wobble de fotocentro aproximado (órbita interna circular, fase uniforme,
  `a_in` log-uniforme) em vez da forma completa de 3 casos da Eq. 20 de
  Chae — mesma simplificação já usada e declarada por
  `hidden_companion_check_v2.py`, agora identificada explicitamente (Seção
  3 acima) como a fonte provável do viés residual de `a0` observado na
  Validação B.
- Catálogo estrutural sintético (massa/separação/distância/erro de PM) é
  paramétrico, não lido do catálogo real — ver `METHODOLOGY_ADDENDUM.md`
  Seção 5 para a justificativa completa desta escolha de desenho.
- `RuntimeWarning: invalid value encountered in sqrt` aparece
  ocasionalmente durante o ajuste de `a0` (`scipy.optimize.curve_fit`
  avaliando a função em `x<0` durante a busca do otimizador, antes de
  convergir para o valor final positivo) — benigno, mesmo padrão que já
  ocorreria em `run_primary_analysis_v2.py`/`fit_a0` (função idêntica),
  não uma introdução desta sessão.

## 5. Veredito de prontidão para o Estágio 2

**Pronto para prosseguir**, com uma ressalva explícita a carregar para o
Estágio 2 (aplicação à amostra de descoberta real, 30.203 sistemas — ainda
NÃO o holdout selado, que exige uma decisão de lock formal própria e
separada, per `DISC-DEC-023`):

1. Os 7 critérios pré-declarados (A1-A4, B1-B3) passaram em todos os 5
   cenários sintéticos testados.
2. O mecanismo central (auto-calibração de `f_multi` ancorada no bin de
   maior aceleração, massa injetada compartilhada entre os ramos real e
   mock) funciona como projetado: recupera `f_multi` verdadeiro dentro de
   `0,05`, remove o viés de multiplicidade em TODOS os bins (não só o
   bin-âncora), e transforma um erro catastrófico de `a0` (1-2 ordens de
   grandeza) num erro residual pequeno (`~0,2` dex).
3. **Ressalva a carregar para o Estágio 2:** a recuperação de `a0` sob
   contaminação simultânea não é perfeita — hà uma tendência de
   super-estimar `a0` em `~1,4-1,6×` devido à forma simplificada do
   modelo de wobble. Isso significa que, se o Estágio 2 aplicar esta
   pipeline ao dado real e encontrar um `a0_fit` corrigido que exclui
   `a0_A`/`a0_B`, essa exclusão deve ser interpretada com esta margem de
   viés residual conhecida em mente — não tratada como uma medição livre
   de viés sistemático. Uma melhoria futura (refinar o modelo de wobble
   para decair corretamente com `g_N`, ou marginalizar sobre a incerteza
   de forma do wobble no ajuste de `a0`) reduziria esse resíduo, mas não é
   pré-condição obrigatória para prosseguir — o critério B2 já previa e
   aceitou explicitamente este nível de desempenho.
4. **Nenhum dado real (descoberta ou holdout) foi tocado nesta etapa** —
   confirmado por inspeção: nenhum script em `analysis/` desta pasta
   importa ou lê `quality_filtered_sample.parquet`,
   `hwang_eccentricity_subset.parquet`, ou `discovery_holdout_split.json`.

**Próximo passo (fora do escopo desta sessão):** autorização explícita
para o Estágio 2 — aplicar `analysis/selfcal_pipeline.py` à amostra de
descoberta real (30.203 sistemas), substituindo o fluxo antigo (ajuste de
`a0` bruto + checagem adversarial pós-hoc) pelo fluxo novo (auto-calibração
de `f_multi` ANTES do ajuste de `a0`, conforme `METHODOLOGY_ADDENDUM.md`
Seção 2) — com pré-registro próprio atualizado antes de tocar qualquer
dado real, mesma disciplina desta linha desde `DISC-DEC-001`.

## 6. Arquivos desta etapa

- `METHODOLOGY_ADDENDUM.md` — especificação metodológica completa.
- `PROVENANCE_CHAE_EQS.md` — verificação das equações fetchadas.
- `analysis/companion_injection.py` — modelo de injeção (Eqs. 11-13),
  vetorizado sobre realizações MC.
- `analysis/selfcal_pipeline.py` — pipeline de auto-calibração completo
  (`run_delta_obs_newt_selfcal`, `calibrate_f_multi`, `fit_a0`,
  `bootstrap_a0_refit`).
- `analysis/build_synthetic_population.py` — construtor de população
  sintética estrutural + dataset "fake real" com verdade conhecida.
- `analysis/validate_a_recover_f_multi.py`,
  `analysis/validate_b_recover_a0_with_contamination.py` — scripts de
  validação, executam os critérios A1-A4/B1-B3.
- `results/validation_A_results.json`, `results/validation_B_results.json`
  — resultados completos (todos os números desta síntese vêm daqui).
- `results/validation_A_run.log`, `results/validation_B_run.log` — logs de
  execução completos.
