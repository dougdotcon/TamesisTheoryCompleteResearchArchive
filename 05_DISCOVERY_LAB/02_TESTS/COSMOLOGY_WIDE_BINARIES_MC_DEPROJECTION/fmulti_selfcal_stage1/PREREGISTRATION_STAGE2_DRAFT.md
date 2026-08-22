# Pré-registro (RASCUNHO): Estágio 2 — aplicação do pipeline de auto-calibração de f_multi à amostra de descoberta real

**Status:** DRAFT -- pending orchestrating-session review

**Data de criação:** 2026-08-22
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-22 (Claude Code)
**Test ID:** `SPARC-FMULTI-STAGE2` (nova ETAPA de `DISC-COSMOLOGY-MOND-SPARC-004` —
não é um `test_id` novo e independente; mesma disciplina de nomenclatura já
usada para `SPARC-FMULTI-STAGE1`)
**Autoridade para redigir este rascunho:** `DISC-DEC-027`, item (a)
**Commit em que foi travado:** N/A — este documento é um RASCUNHO, sem commit
de lock. `AGENTS.md` passo 3/4 exige commitar o pré-registro **travado**
antes de tocar dado real; `DISC-DEC-027` insere explicitamente um passo
intermediário adicional para esta frente: o agente redige mas NÃO trava — a
sessão orquestradora revisa, decide sobre os pontos assinalados na Seção 12
abaixo, e só então executa o commit de lock como ação própria e auditável,
antes de autorizar qualquer cálculo sobre dado real numa decisão subsequente.

> **ATENÇÃO — RASCUNHO, NÃO TRAVADO.** Nenhum arquivo de dado real
> (`quality_filtered_sample.parquet`, `hwang_eccentricity_subset.parquet`,
> `discovery_holdout_split.json`, ou qualquer `.parquet`/`.json` de catálogo
> real desta linha) foi lido, aberto, importado ou computado na redação deste
> documento — toda a estrutura de dado citada abaixo (colunas, contagens,
> bordas de bin, fórmulas) vem de `../PREREGISTRATION.md` e
> `METHODOLOGY_ADDENDUM.md`, documentação já escrita sobre o dado, não do
> próprio dado. Nenhum commit de lock foi criado. `Status` só pode mudar para
> `LOCKED` por ação explícita e separada da sessão orquestradora.

## 0. Por que esta etapa existe

`DISC-COSMOLOGY-MOND-SPARC-004` (`../PREREGISTRATION.md`, lida por completo
para redigir este rascunho) foi fechado `CLOSED_INCONCLUSIVE` em 2026-08-18:
o critério mecânico da Seção 5 daquele documento, aplicado literalmente ao
`δ_obs-newt` real (v2, corrigido), produziria `BOTH_FALSIFIED`, mas esse
veredito não foi aceito porque a checagem adversarial obrigatória de
multiplicidade oculta (Seção 7d daquele documento) mostrou que companheiras
não resolvidas, em magnitude inteiramente plausível pela literatura
(`f_multi=0,25-0,47`), são **sozinhas suficientes** para produzir o resíduo
observado inteiro, sem qualquer física MOND. O próprio fechamento nomeou a
precondição explícita para qualquer tentativa futura genuinamente nova
(`../PREREGISTRATION.md` linha 535): "implementar a auto-calibração completa
de `f_multi` de Chae (Eqs. 11-13) antes de qualquer ajuste de `a0`".

`SPARC-FMULTI-STAGE1` (`RESULTS_SUMMARY_STAGE1.md`, `METHODOLOGY_ADDENDUM.md`,
`PROVENANCE_CHAE_EQS.md`, `ADVERSARIAL_VERIFICATION.md`, todos lidos por
completo para redigir este rascunho) implementou exatamente essa precondição
e a validou inteiramente sobre dado sintético: 7/7 critérios pré-declarados
(A1-A4, B1-B3) passaram em 5 cenários independentes, verificado por dois
agentes adversariais separados (proveniência das equações: `SOUND`; auditoria
de código/números/circularidade: 2 problemas reais encontrados e corrigidos,
nenhum número já reportado alterado). `DISC-DEC-026` integrou esse resultado
e declarou o pipeline "pronto para o Estágio 2 ... Estágio 2 não autorizado
por esta decisão, exige pré-registro próprio."

**Este documento é esse pré-registro — em rascunho, por instrução explícita
de `DISC-DEC-027`.** Ele especifica exatamente como o pipeline já validado
(`analysis/selfcal_pipeline.py`, `analysis/companion_injection.py`, ambos
desta pasta) será aplicado, pela primeira vez, à amostra de descoberta REAL
de `DISC-COSMOLOGY-MOND-SPARC-004` (30.203 sistemas — ainda NÃO o holdout
selado de 12.944). Nenhum número deste rascunho vem de rodar o pipeline sobre
dado real — todos os parâmetros abaixo (bordas de bin, `N_MC`, `N_bootstrap`,
regra de decisão) são fixados ANTES de qualquer execução sobre dado real,
exatamente a disciplina que `AGENTS.md` passo 3 exige.

## 1. Hipótese exata (idêntica a SPARC-002/003/004, NÃO reformulada)

- **H_A:** o `a0` que melhor explica a razão de aceleração desprojetada
  (Seção 4 abaixo) é compatível (dentro do IC de 95%) com
  $a_0^A = cH_0/(2\pi) \approx 1{,}082288\times10^{-10}$ m/s² ("Ponte
  Holográfica").
- **H_B:** o mesmo `a0` é compatível com
  $a_0^B = cH_0 \approx 6{,}800218\times10^{-10}$ m/s² ("MOND Emergence").
- Mesmos valores exatos já travados em `DISC-COSMOLOGY-MOND-SPARC-002`,
  reaproveitados sem alteração em `SPARC-003` e `SPARC-004`
  (`../PREREGISTRATION.md` Seção 1). Este rascunho **não redefine H_A/H_B**
  — apenas especifica como o observável discriminador (já definido em
  `../PREREGISTRATION.md` Seção 4/4c: `δ_obs-newt` por bin) passa a ser
  computado após correção de multiplicidade oculta, em vez de bruto.
- **Nota de identificabilidade honesta** (carregada de SPARC-002/003/004
  sem diluir): $a_0^A=cH_0/(2\pi)$ reproduz uma coincidência numérica já
  conhecida na literatura MOND padrão (Milgrom, décadas antes de Tamesis,
  arXiv:2001.09729) — H_A sobreviver não é evidência de poder discriminativo
  específico de Tamesis, só consistência com um fato numérico pré-existente
  no campo. Esta ressalva se aplica igualmente aqui, e não é enfraquecida
  pela correção de multiplicidade — ela é ortogonal ao que a auto-calibração
  de `f_multi` corrige.

## 2. Fonte de dado (reaproveitada sem modificação; nenhum novo download, nenhuma nova extração)

- **Amostra de descoberta:** os mesmos **30.203 sistemas** já extraídos e
  commitados em `../../COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/data/`
  (`../PREREGISTRATION.md` Seção 2 — split `discovery_holdout_split.json`,
  seed=20260814). Este rascunho não os lê nem os recomputa; apenas descreve,
  a partir da documentação já escrita, como o Estágio 2 os usará quando
  autorizado.
- **Holdout selado (12.944 sistemas): permanece intocado** — ver Seção 8
  (linha vermelha explícita).
- **Colunas necessárias** (todas já catalogadas como disponíveis em
  `METHODOLOGY_ADDENDUM.md` Seção 1b, tabela de insumos — nenhuma nova
  coluna, nenhum novo cruzamento):
  - `M1_Msun`, `M2_Msun` (massa catalogada por componente,
    `quality_filtered_sample.parquet`) → usadas como `M1_cat`/`M2_cat` nas
    chamadas de `calibrate_f_multi()`/`run_delta_obs_newt_selfcal()` abaixo.
  - `RUWE1`, `RUWE2` — checagem de CONSISTÊNCIA secundária (Seção 6 abaixo),
    não mais o mecanismo primário de correção.
  - Erros de PM por componente (`e_pmRA1/2`, `e_pmDE1/2`, Gaia) — orçamento
    de ruído astrométrico simétrico, já travado (`PREREGISTRATION.md` Seção
    5b), reaproveitado sem alteração.
  - `e`, `e0`, `e1`, `alpha`, `dpm_sig` (`hwang_eccentricity_subset.parquet`)
    — amostragem de excentricidade (Gap a de `../PREREGISTRATION.md` Seção
    4), reaproveitada sem alteração.
  - `v_p_real`: **não é uma coluna nova** — é a mesma velocidade relativa
    projetada observada já computada e usada em SPARC-003/004,
    $v_p=4{,}74047\times10^{-3}\cdot\Delta\mu\cdot\bar d$ (`../PREREGISTRATION.md`
    linha ~173), a partir do movimento próprio diferencial Gaia real. Carrega
    ruído astrométrico Gaia genuíno por construção — por isso
    `run_delta_obs_newt_selfcal(..., real_gets_astrometric_noise=False)` é o
    valor correto para o ramo real neste Estágio (ver Seção 4.2 abaixo; a
    flag `True` é só para dado sintético "fake real" que ainda não tem
    ruído embutido, ver `build_synthetic_population.py`).
- **Bordas de bin: reaproveitadas sem modificação**, a mesma grade de 5 bins
  de quantil igual em $\log_{10}(g_N)$ já fixada em `../COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md`
  Seção 2 e já reaproveitada por `../PREREGISTRATION.md` (SPARC-004) e por
  todos os cenários de `SPARC-FMULTI-STAGE1`:

  ```text
  BIN_EDGES_LOG_GN_SPARC003 = [-11,7012; -9,1728; -8,4667; -7,9752; -7,5548; -6,5224]
  ```

  (log10 de g_N em SI, ~6.040-6.041 sistemas por bin sobre os 30.203 de
  descoberta). Importada do módulo já travado
  `../../analysis/delta_obs_newt.py::BIN_EDGES_LOG_GN_SPARC003` — **nenhum
  novo binning é definido neste rascunho nem a partir de qualquer resultado
  deste Estágio**, mesma disciplina de "nenhum binning definido a partir do
  resultado" já usada em `selfcal_pipeline.py::run_delta_obs_newt_selfcal`
  (comentário inline sobre `assign_bins_by_projected_gN`).
- **Bin-âncora: bin 4** (índice 0-4, o de maior aceleração,
  $\log_{10}(g_N)\in[-7{,}5548;-6{,}5224]$) — mesmo `ANCHOR_BIN=4` já
  hardcoded e validado em `analysis/validate_a_recover_f_multi.py` e
  `analysis/validate_b_recover_a0_with_contamination.py`, análogo ao
  $x_0\approx-8$ citado verbatim de Chae (`PROVENANCE_CHAE_EQS.md` Seção 5).

## 3. Modelo nulo / hipótese concorrente (mesmo papel que em SPARC-002/003/004, NÃO reformulado)

Teste de consistência interna entre H_A e H_B contra um canal físico
independente, não um teste de "MOND vs. Newton puro" no sentido do Artigo A
original de Chae — mesma redação de `../PREREGISTRATION.md` Seção 3,
reaproveitada sem alteração. A diferença estrutural do Estágio 2 em relação
ao fechamento `CLOSED_INCONCLUSIVE` de 2026-08-18 não é o modelo nulo, é o
tratamento do confundidor de multiplicidade oculta: antes, era testado
post-hoc contra uma faixa de valores fixos da literatura (Seção 6/7d de
`../PREREGISTRATION.md`); agora, `f_multi` é auto-calibrado como parâmetro
livre a partir do próprio dado real, ANTES do ajuste de `a0` — exatamente o
procedimento de Chae (Artigo A, `PROVENANCE_CHAE_EQS.md` Seção 5), não uma
extensão nova desta linha.

## 4. Procedimento exato

### 4.1 Visão geral (substitui, não roda ao lado do fluxo antigo v1/v2)

```text
1. calibrate_f_multi() sobre os 30.203 sistemas de descoberta reais
   -> f_multi_hat (autocalibrado, bin-ancora=4)
2. Extrair delta_obs-newt(bin) CORRIGIDO (5 valores, f_multi=f_multi_hat)
   do proprio retorno de calibrate_f_multi()["final_result"]
3. fit_a0() sobre os 5 valores corrigidos -> a0_fit (ponto central)
4. Re-executar run_delta_obs_newt_selfcal() com f_multi=f_multi_hat e
   return_raw=True (calibrate_f_multi() nao retorna _raw por padrao) para
   obter os arrays MC pareados necessarios ao bootstrap
5. bootstrap_a0_refit() sobre esse _raw -> IC95% de a0_fit
6. Aplicar a regra de decisao da Secao 5 a (a0_fit, IC95%)
7. Checagens de consistencia secundarias (RUWE alto/baixo, f_multi_hat
   dentro de 0,25-0,47) -- Secao 6
```

Isto reproduz, literalmente, o "Fluxo NOVO" já especificado (mas não
autorizado para dado real) em `METHODOLOGY_ADDENDUM.md` Seção 2 — este
rascunho não inventa um fluxo novo, apenas instancia os parâmetros exatos
(bin edges, `N_MC`, `N_bootstrap`, seed) que faltavam para rodá-lo sobre
dado real.

### 4.2 Passo 1 — auto-calibração de `f_multi` (`calibrate_f_multi()`)

Chamada exata (assinatura de `analysis/selfcal_pipeline.py::calibrate_f_multi`,
não modificada nesta frente):

```python
calib = calibrate_f_multi(
    s=s_m,                       # sepAU * AU_M, dos 30.203 sistemas de descoberta
    v_p_real=v_p_real_si,        # v_p real observado (Gaia), SI, ja' com ruido genuino
    M1_cat=M1_cat_kg, M2_cat=M2_cat_kg,   # M1_Msun/M2_Msun catalogados * MSUN_KG
    e_m=e_m, e_lo=e_lo, e_hi=e_hi, alpha_ecc=alpha_ecc, dpm_sig=dpm_sig,   # Hwang, Gap (a)
    d_mean_pc=d_mean_pc,
    pmra_err1=e_pmRA1, pmra_err2=e_pmRA2, pmde_err1=e_pmDE1, pmde_err2=e_pmDE2,
    bin_edges=BIN_EDGES_LOG_GN_SPARC003,   # Secao 2 acima, reaproveitada sem alteracao
    anchor_bin=4,
    n_mc=200,                    # ver justificativa abaixo
    seed=SEED_STAGE2,            # ver justificativa abaixo
    f_lo=0.0, f_hi=0.9,          # default da funcao, inalterado
    xtol=5e-4,                   # default da funcao (mais apertado que os 5e-3
                                  # usados nos scripts de VALIDACAO do Estagio 1,
                                  # que relaxaram xtol so' por velocidade de teste)
    include_wobble=True,         # default; a simplificacao de wobble e' a
                                  # limitacao conhecida da Secao 7, nao desligada
    n_bootstrap_final=N_BOOTSTRAP_STAGE2,   # ver justificativa abaixo
)
f_multi_hat = calib["f_multi_calibrated"]
```

**`real_gets_astrometric_noise` não aparece nesta chamada** — é um parâmetro
de `run_delta_obs_newt_selfcal()`, não de `calibrate_f_multi()` diretamente
(que a repassa com o default `False` internamente); confirmar, na
implementação real do Estágio 2, que nenhuma chamada explícita sobrescreve
esse default para `True` sobre dado real — fazer isso re-injetaria ruído
astrométrico sintético em cima de um `v_p_real` que já carrega ruído Gaia
genuíno, reintroduzindo exatamente a assimetria real-vs-mock que o bug da
Seção 5b de `../PREREGISTRATION.md` já identificou e corrigiu no pipeline
antigo. Esta é uma checagem de implementação obrigatória antes de aceitar
qualquer resultado do Estágio 2 (candidata natural a item de checklist do
Passo 7 adversarial padrão).

**Verificar `calib["converged_bracket"]` é `True`** antes de prosseguir —
se `False` (nenhuma troca de sinal de `δ_ancora(f_multi)` no intervalo
`[0,0;0,9]`), isso é, por si só, um gatilho de checagem adversarial de
descoberta de nulo (Seção 6, item (b) abaixo), não apenas um aviso.

### 4.3 Passo 2 — extrair `δ_obs-newt(bin)` corrigido

```python
delta_corrected = calib["final_result"]["delta_obs_newt_primary"]   # 5 valores
gN_bin_median   = calib["final_result"]["gN_bin_median_si"]         # 5 valores
```

Note que `calib["final_result"]` já usa `f_multi=f_multi_hat` e uma semente
DIFERENTE (`seed+777`, hardcoded em `calibrate_f_multi`) da usada na busca de
bisseção — isso é intencional (teste fora-da-amostra, já confirmado `SOUND`
por `ADVERSARIAL_VERIFICATION.md` Frente 2, item "Circularidade"), não um
bug a corrigir.

### 4.4 Passo 3 — ajuste central de `a0` (`fit_a0()`)

```python
a0_fit = fit_a0(np.array(gN_bin_median), np.array(delta_corrected), x0=1.0)
# Verificar convergencia com >=2 pontos de partida diferentes (mesma licao
# de SPARC-002, ja reaplicada em run_primary_analysis_v2.py e nas
# validacoes B do Estagio 1, x0_list=(1.0,5.0)):
a0_fit_x5 = fit_a0(np.array(gN_bin_median), np.array(delta_corrected), x0=5.0)
# a0_fit e a0_fit_x5 devem concordar (mesma ordem de grandeza, idealmente
# identicos ao nivel de precisao numerica do otimizador) antes de aceitar
# a0_fit como o valor central.
```

### 4.5 Passo 4-5 — IC de 95% via bootstrap (`bootstrap_a0_refit()`)

`calibrate_f_multi()` **não retorna** os arrays brutos pareados
(`log_ratio_real`, `log_ratio_mock`, `bin_idx`, ...) que `bootstrap_a0_refit()`
exige — é preciso reexecutar `run_delta_obs_newt_selfcal()` diretamente, com
`f_multi=f_multi_hat` fixo e `return_raw=True`, usando **a mesma semente
`seed+777`** que `calibrate_f_multi()` usou internamente para o
`final_result` (Seção 4.3), para garantir que o IC seja calculado sobre
exatamente a mesma realização MC primária já reportada como ponto central —
não uma realização nova e diferente:

```python
final_raw = run_delta_obs_newt_selfcal(
    s=s_m, v_p_real=v_p_real_si, M1_cat=M1_cat_kg, M2_cat=M2_cat_kg,
    e_m=e_m, e_lo=e_lo, e_hi=e_hi, alpha_ecc=alpha_ecc, dpm_sig=dpm_sig,
    d_mean_pc=d_mean_pc,
    pmra_err1=e_pmRA1, pmra_err2=e_pmRA2, pmde_err1=e_pmDE1, pmde_err2=e_pmDE2,
    f_multi=f_multi_hat, bin_edges=BIN_EDGES_LOG_GN_SPARC003, n_mc=200,
    seed=SEED_STAGE2 + 777,      # IDENTICO ao seed+777 interno de calibrate_f_multi
    include_wobble=True, n_bootstrap=None, return_raw=True,
)

ci = bootstrap_a0_refit(
    final_raw["_raw"], n_bins=5, n_bootstrap=N_BOOTSTRAP_STAGE2,
    seed=SEED_STAGE2 + 999_999,   # semente propria do bootstrap de a0, distinta
    x0_list=(1.0, 5.0),
)
# ci["x0=1.0"] e ci["x0=5.0"] devem concordar (mesma verificacao de
# convergencia de multiplos pontos de partida, agora sobre TODAS as
# replicas bootstrap, nao so' o ajuste central)
a0_ci95_lo = ci["x0=1.0"]["ci95_lo_si_m_s2"]
a0_ci95_hi = ci["x0=1.0"]["ci95_hi_si_m_s2"]
```

**Nota de implementação — este é o ponto de maior risco de erro silencioso
desta especificação**, sinalizado explicitamente para o Passo 7 adversarial
padrão (`AGENTS.md` item 7): um descasamento de semente entre a chamada de
`calibrate_f_multi()` (Passo 1) e a chamada direta de
`run_delta_obs_newt_selfcal(...,return_raw=True)` (Passo 4.5) produziria um
`a0_fit` central (Seção 4.4) calculado sobre uma realização MC e um IC95%
(Seção 4.5) calculado sobre OUTRA realização MC diferente — nem incorreto
individualmente, mas inconsistente entre si de um jeito que um segundo
agente revisando só os números finais não detectaria sem inspecionar as
sementes usadas em cada chamada. A reexecução adversarial padrão deve
verificar explicitamente que as duas sementes coincidem.

### 4.6 Parâmetros numéricos fixados — tabela resumo

| parâmetro | valor | origem |
|---|---|---|
| `bin_edges` | `[-11,7012;-9,1728;-8,4667;-7,9752;-7,5548;-6,5224]` | já travado, SPARC-003/004 |
| `anchor_bin` | `4` | já travado, `ANCHOR_BIN` do Estágio 1 |
| `f_lo`, `f_hi` (bracket de `f_multi`) | `0,0` / `0,9` | default de `calibrate_f_multi`, já validado |
| `xtol` (bisseção de `f_multi`) | `5×10⁻⁴` | default da função (mais apertado que a validação) |
| `include_wobble` | `True` | default; limitação conhecida (Seção 7), não desligada |
| `real_gets_astrometric_noise` | `False` (não sobrescrever) | dado real já carrega ruído Gaia genuíno |
| `N_MC` (`n_mc`) | `200` | **judgment call — ver Seção 12.1** |
| `N_bootstrap` (`n_bootstrap_final` e `bootstrap_a0_refit`) | `2000` | **judgment call — ver Seção 12.2** |
| `SEED_STAGE2` | `20260822` (proposto) | **judgment call — ver Seção 12.3** |
| `x0` do ajuste de `a0` (verificação de convergência) | `{1,0; 5,0}` | mesma convenção do Estágio 1 |

## 5. Regra de decisão a priori: H_A vs. H_B dado `a0_fit` e seu IC95%

**Camada mecânica — idêntica, NÃO reformulada, ao critério já travado em
`../PREREGISTRATION.md` Seção 5 (que por sua vez reaproveita a convenção de
SPARC-002/003):**

- **H_A falsificada** se $a_0^A\approx1{,}082288\times10^{-10}$ estiver
  fora do IC de 95% de `a0_fit` (Seção 4.5).
- **H_B falsificada** se $a_0^B\approx6{,}800218\times10^{-10}$ estiver
  fora do IC de 95%.
- Se apenas uma sobreviver: suporte a essa derivação especificamente
  (linguagem sempre relativa a este teste específico, `AGENTS.md`
  Proibições — nunca "Tamesis confirmado").
- Se nenhuma sobreviver: ambas falsificadas por este canal
  (`BOTH_FALSIFIED`).
- Se as duas sobreviverem: `INCONCLUSIVO` (mesmo veredito possível de
  SPARC-002/003/004).
- **Pré-condição obrigatória** (idêntica em espírito à Seção 4b/5 de
  `../PREREGISTRATION.md`): o checklist de revalidação sintética da Seção 9
  abaixo deve passar sob os parâmetros exatos da Seção 4.6 ANTES de aceitar
  qualquer veredito acima.

**Camada interpretativa adicional — obrigatória especificamente para este
Estágio, NÃO uma redefinição do critério mecânico acima** (mesmo padrão
estrutural já estabelecido em `../PREREGISTRATION.md` Seção 6/7e, onde um
gatilho pré-declarado exige uma checagem adicional antes de aceitar
literalmente o critério mecânico):

> Antes de catalogar qualquer veredito `H_A_FALSIFICADA`, `H_B_FALSIFICADA`
> ou `BOTH_FALSIFIED` produzido pela camada mecânica acima, verificar
> explicitamente se dividir `a0_fit` (e os dois limites do IC95%) pelo fator
> de viés residual já documentado no Estágio 1 (`1,4`-`1,6×`, Seção 7 abaixo)
> traria $a_0^A$ e/ou $a_0^B$ de volta para dentro do intervalo. **Se sim**,
> o veredito mecânico não pode ser aceito como uma falsificação limpa — deve
> ser reportado como `INCONCLUSIVO`, com a margem exata e o fator de viés
> residual documentados lado a lado no relatório final, exatamente a mesma
> disciplina já usada em `../PREREGISTRATION.md` Seção 7e ("um critério
> mecânico não pode ser aceito quando o próprio pré-registro já sinalizou,
> a priori, que um confundidor não corrigido poderia produzir exatamente
> esse padrão"). Esta camada não adiciona um novo caminho para ACEITAR H_A
> ou H_B — só impede que um `BOTH_FALSIFIED` ou uma falsificação de uma
> hipótese específica seja aceita sem essa checagem quando a margem de
> exclusão é da mesma ordem de grandeza do viés residual já conhecido.

## 6. Gatilhos obrigatórios de checagem adversarial de descoberta de nulo

Além da reexecução adversarial padrão (`AGENTS.md` passo 7 — SEMPRE
obrigatória, independente do resultado, mesmo agente separado do que rodou a
análise original), **qualquer um** dos itens abaixo aciona adicionalmente o
papel de "descoberta adversarial de nulos" no sentido operacional de
`METHODOLOGY_EXTENSIONS.md` Seção 5 (um agente instruído especificamente
como debunker convencional, não como revisor de correção de código) — mesmo
precedente já estabelecido dentro desta linha por `../PREREGISTRATION.md`
Seção 6 (checagem de multiplicidade oculta obrigatória, aplicada antes do
Gate de Replicação, não só nele):

1. **`a0_fit` corrigido cai fora da faixa plausível de AMBAS H_A e H_B por
   mais de uma ordem de grandeza** — mesma magnitude qualitativa do modo de
   falha catastrófico já documentado na Validação B do Estágio 1 (erro de
   `17×`-`57×` SEM correção de `f_multi`). Se isso ocorrer mesmo COM a
   auto-calibração aplicada, é evidência de que o pipeline não está se
   comportando sobre dado real da mesma forma que sobre dado sintético —
   sinal de um confundidor ou bug não capturado pela validação sintética,
   não uma medição de `a0` a ser aceita literalmente.
2. **`calib["converged_bracket"]` é `False`**, ou `f_multi_hat` calibrado
   cai a menos de `xtol` de `f_lo=0,0` ou `f_hi=0,9` (borda do bracket) —
   sinal de que a bisseção não encontrou uma raiz genuína dentro do
   intervalo declarado, não apenas um valor calibrado baixo/alto legítimo.
3. **`f_multi_hat` cai fora da faixa observacional da literatura
   `0,25`-`0,47`** (referência de Chae/Artigo B, Seção "0" acima) por uma
   margem grande — rebaixada a checagem de CONSISTÊNCIA secundária pelo
   `METHODOLOGY_ADDENDUM.md` Seção 2 item 4, mas um desvio grande dessa
   faixa, mesmo como checagem secundária, é motivo suficiente para o
   gatilho, não para ser silenciosamente ignorado.
4. **O padrão de `δ_obs-newt(bin)` corrigido é qualitativamente
   inconsistente com a assinatura de viés já caracterizada no Estágio 1**
   (Validação B: resíduo pequeno, `~0,15`-`0,22` dex, concentrado nos bins
   de MENOR $g_N$, mesma direção que a falha conhecida do modelo de wobble
   simplificado que não decai o suficiente com $g_N$ — Seção 7 abaixo). Um
   padrão real que inverta essa direção (resíduo crescendo com $g_N$, sinais
   trocando entre bins adjacentes sem razão física clara, ou magnitude mais
   de uma ordem acima dos `0,15`-`0,22` dex documentados) não pode ser
   atribuído ao mecanismo já conhecido e exige investigação adicional antes
   de aceitar qualquer veredito.
5. **A exclusão de H_A e/ou H_B pelo IC95% depende sensivelmente da escolha
   de `N_bootstrap` ou da semente do bootstrap** (não robusta) — checar
   explicitamente reexecutando `bootstrap_a0_refit` com uma semente
   diferente e/ou um `N_bootstrap` reduzido (ex. `1000`), confirmando que o
   veredito da Seção 5 não muda. Mesma cautela já nomeada explicitamente por
   `ADVERSARIAL_VERIFICATION.md` item 3 para a margem "por pouco" do
   resultado v2 original (`0,057` dex).

**Qualquer veredito diferente de "nenhum sinal detectável acima do ruído,
compatível com controle negativo"** — ou seja, qualquer `H_A_FALSIFICADA`,
`H_B_FALSIFICADA` específica, `BOTH_FALSIFIED`, ou suporte a H_A/H_B — deve
passar pelo papel de debunker de `METHODOLOGY_EXTENSIONS.md` Seção 5 antes de
ser catalogado, independentemente de qualquer gatilho numérico específico
acima ter disparado — mesma disciplina já aplicada por
`../PREREGISTRATION.md` Seção 6 à checagem de multiplicidade oculta.

## 7. Limitação conhecida do Estágio 1 a carregar explicitamente — viés residual de `a0` (NÃO pode ser silenciosamente descartada)

`RESULTS_SUMMARY_STAGE1.md` Seção 3/5 documenta, honestamente e ANTES de
qualquer dado real ser tocado, que a recuperação de `a0` sob contaminação de
multiplicidade simultânea (Validação B) **não é perfeita**: em ambos os
cenários sintéticos testados, `a0_fit` corrigido tende a **superestimar**
`a0_true` por um fator de `1,4`-`1,6×` (`0,15`-`0,22` dex), causa raiz já
diagnosticada — o modelo simplificado de wobble de fotocentro (órbita interna
circular, fase uniforme, `a_in` log-uniforme, herdado sem alteração de
`../analysis/hidden_companion_check_v2.py`) não decai corretamente com
$g_N$, deixando um resíduo de FORMA pequeno mas não perfeitamente plano
através dos bins que a auto-calibração no bin-âncora (que remove só o nível
médio no bin de maior aceleração, não a forma inteira nos demais) não
consegue eliminar totalmente. Em um dos dois cenários, o IC95% nem chegou a
conter `a0_true` (borda inferior `1,47×10⁻¹⁰` contra `a0_true=1,20×10⁻¹⁰`).

**Declaração explícita para este Estágio (item obrigatório, exigido por
`DISC-DEC-027`):** esta ressalva **não é diluída, não é omitida, e não é
tratada como resolvida** ao mover a pipeline de dado sintético para dado
real. Qualquer `a0_fit` real deste Estágio que exclua $a_0^A$ e/ou $a_0^B$
deve ser reportado JUNTO com este viés residual conhecido, não como uma
medição livre de viés sistemático. A camada interpretativa da Seção 5 acima
opera precisamente sobre esta ressalva — não é uma formalidade descritiva,
é um mecanismo de decisão ativo. Uma melhoria futura (refinar o modelo de
wobble para decair corretamente com $g_N$, ou marginalizar sobre a incerteza
de forma do wobble no próprio ajuste de `a0`) reduziria este resíduo, mas
**não é pré-condição** para este Estágio prosseguir — o critério B2 do
Estágio 1 já previu e aceitou este nível de desempenho antes de ver qualquer
dado real (`METHODOLOGY_ADDENDUM.md` Seção 3).

## 8. Linha vermelha explícita: o holdout selado NÃO é tocado por este Estágio, sob nenhuma circunstância

- **12.944 sistemas do holdout selado** (`../../COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/data/discovery_holdout_split.json`,
  seed=20260814) permanecem **intocados** por este Estágio — nem lidos, nem
  usados para calibrar `f_multi`, nem usados para ajustar `a0`, nem usados
  para qualquer checagem de consistência ou sanidade.
- **Nenhum script produzido para este Estágio pode importar, abrir, ou ler
  `discovery_holdout_split.json` para extrair a lista de holdout**, nem ler
  qualquer coluna de qualquer sistema classificado como holdout naquele
  arquivo — mesma checagem que `ADVERSARIAL_VERIFICATION.md` já aplicou ao
  Estágio 1 (grep de toda instrução `import`/`open`/`read` em `analysis/*.py`
  procurando os nomes dos arquivos reais desta linha) deve ser reaplicada ao
  código do Estágio 2 antes de aceitar qualquer resultado.
- **Abrir o holdout exige uma decisão de lock formal própria, futura e
  separada** — mesmo precedente já estabelecido para outras linhas desta
  trilha, reafirmado por `METHODOLOGY_ADDENDUM.md` Seção 5 e por
  `../PREREGISTRATION.md` Seção 7e ("O Gate de Replicação não é acionado...
  O holdout selado (12.944 sistemas) permanece intocado, disponível para uma
  futura tentativa"). **Este Estágio é exatamente essa futura tentativa
  nomeada — mas usar APENAS a amostra de descoberta, nunca o holdout.** O
  holdout só é aberto no Gate de Replicação (`AGENTS.md` passo 9), se e
  quando este Estágio 2 sobreviver à reexecução adversarial padrão e for
  candidato a promoção — decisão explicitamente fora do escopo deste
  rascunho e de `DISC-DEC-027`.
- Se, na implementação real do Estágio 2, qualquer script vier a precisar de
  qualquer informação estrutural (contagem, distribuição de massa, etc.) que
  só possa ser obtida abrindo o arquivo de split, extrair SOMENTE a lista de
  descoberta (30.203), nunca materializar a lista de holdout em memória nem
  em log — mesma disciplina de manuseio de dado selado já usada em outras
  linhas desta trilha.

## 9. Checklist de revalidação sintética obrigatória imediatamente antes do dado real

Prática padrão já estabelecida nesta trilha (`../PREREGISTRATION.md` Seções
4b, 4c e 5b — revalidar sob os parâmetros exatos que vão tocar dado real,
ANTES de tocar dado real, toda vez que a pipeline ou seus parâmetros
mudarem) — nenhum cenário sintético NOVO é necessário além do já existente
em `SPARC-FMULTI-STAGE1`, exceto o item 9.4 abaixo, que reexecuta um cenário
JÁ EXISTENTE sob um `N_bootstrap` diferente (não é um cenário novo, é uma
resolução mais fina do mesmo teste), especificamente porque
`ADVERSARIAL_VERIFICATION.md` item 3 já nomeou essa lacuna:

**9.1. Confirmar que a lacuna de robustez já corrigida permanece corrigida.**
`fit_a0()` deve conter a guarda `a0_fit>0`/`np.isfinite` adicionada em
resposta a `ADVERSARIAL_VERIFICATION.md` item 2 (Frente 2) — checar por
inspeção do arquivo, não assumir de memória.

**9.2. Reexecutar `validate_a_recover_f_multi.py` e
`validate_b_recover_a0_with_contamination.py` SEM alteração de lógica**,
apenas com `N_BOOTSTRAP`/`N_BOOTSTRAP_A0_REFIT` elevados para o valor exato
que o Estágio 2 usará sobre dado real (`N_bootstrap=2000`, Seção 4.6/12.2) —
confirmar que os **7 critérios A1-A4/B1-B3 continuam passando** sob o novo
`N_bootstrap`, não só sob o `N_bootstrap=300`-`400` original do Estágio 1.
Isto verifica duas coisas ao mesmo tempo: (i) que aumentar `N_bootstrap` não
introduz nenhuma instabilidade numérica ou de tempo de execução nova; (ii)
que os vereditos A1-A4/B1-B3 não dependiam, de forma frágil, do `N_bootstrap`
mais baixo original.

**9.3. Confirmar ausência de dado real** por grep de todo `import`/`open`/
`read` em `analysis/*.py` desta pasta (incluindo qualquer script novo escrito
especificamente para o Estágio 2) contra os nomes travados
(`quality_filtered_sample.parquet`, `hwang_eccentricity_subset.parquet`,
`discovery_holdout_split.json`, `catalog.parquet`) — mesma checagem que
`ADVERSARIAL_VERIFICATION.md` Frente 2 já aplicou ao Estágio 1, reaplicada
aqui como o último portão antes do dado real ser tocado pela primeira vez
por esta pipeline especificamente.

**9.4. (Prioritário, resolve a lacuna já nomeada por
`ADVERSARIAL_VERIFICATION.md` item 3.)** Reexecutar especificamente o
cenário `f_multi_true=0,35` da Validação B (o cenário "por pouco" — IC95%
original em `N_bootstrap=300` não continha `a0_true`, borda inferior
`1,47×10⁻¹⁰` vs. `a0_true=1,20×10⁻¹⁰`) sob `N_bootstrap=2000`, mesmas
sementes, e reportar explicitamente se o IC mais preciso muda o veredito B2
daquele cenário (de "não contém" para "contém", ou vice-versa). Este é
exatamente o teste que a ressalva estatística do Estágio 1 pedia para ser
feito antes do Estágio 2, não um cenário novo.

**9.5. Verificar a checagem a priori de insensibilidade do bin-âncora ao
`a0` verdadeiro** (`_check_anchor_bin_mond_negligible`, já implementada em
`validate_b_recover_a0_with_contamination.py`) continua passando sob os
parâmetros do Estágio 2 — pré-condição para o bin-âncora ser um calibrador
limpo de `f_multi` (`METHODOLOGY_ADDENDUM.md` Seção 4).

**Critério de bloqueio:** se qualquer item 9.1-9.5 falhar, o Estágio 2 NÃO
está pronto para tocar dado real — a falha específica deve ser documentada
honestamente (mesmo padrão de `METHODOLOGY_ADDENDUM.md` Seção 3, "Critério
de bloqueio") antes de qualquer nova tentativa, e antes de qualquer commit
de lock deste documento.

## 10. Correção para comparações múltiplas / reexecução adversarial padrão

Duas hipóteses pré-registradas (H_A, H_B) testadas contra o mesmo IC de um
único ajuste de 5 bins — sem busca sobre número de bins (reaproveitados
fixos de SPARC-003/004), sem busca sobre bin-âncora (fixado em 4, Seção 2),
sem busca sobre `f_multi` além da bisseção de calibração já especificada
(um único parâmetro livre, não uma varredura de modelos). Mesma contagem de
comparações de `../PREREGISTRATION.md` Seção 6, não alterada por este
Estágio. Reexecução adversarial obrigatória (`AGENTS.md` passo 7, segundo
agente, implementação independente do zero) antes de catalogar qualquer
resultado — sem exceção, independentemente de qualquer gatilho da Seção 6
ter disparado.

## 11. O que este pré-registro NÃO é / NÃO faz

- **Não redefine H_A/H_B**, a estatística de teste `δ_obs-newt`, o modelo
  nulo, os cortes de qualidade, o split discovery/holdout, ou as bordas de
  bin — todos reaproveitados verbatim de `../PREREGISTRATION.md`/
  `../COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md`.
- **Não trava.** `Status` permanece `DRAFT` até ação explícita e separada da
  sessão orquestradora, conforme `DISC-DEC-027`.
- **Não toca, lê, importa, ou computa sobre qualquer dado real** — nem a
  amostra de descoberta, nem o holdout selado. Todos os números citados
  neste documento (bordas de bin, contagens, valores de `a0_A`/`a0_B`, viés
  residual do Estágio 1) vêm de documentação já escrita sobre dado já
  processado por sessões anteriores, nunca de uma leitura nova.
- **Não abre o holdout selado** — isso permanece uma decisão de lock formal
  própria e futura, fora do escopo deste rascunho (Seção 8).
- **Não é uma reprodução byte-a-byte do Artigo A de Chae** — a
  simplificação declarada do wobble de fotocentro (Seção 7) permanece uma
  aproximação conhecida, não a forma completa de três casos da Eq. 20.
- **Não garante que a pipeline vá funcionar sobre dado real da mesma forma
  que sobre dado sintético** — é exatamente por isso que a Seção 6 declara
  gatilhos explícitos de descoberta adversarial de nulo, e a Seção 9 exige
  revalidação imediatamente antes do dado real, não apenas confiando no
  resultado já obtido em `SPARC-FMULTI-STAGE1`.

## 12. Judgment calls explícitos para revisão da sessão orquestradora

Os três parâmetros abaixo são escolhas defensáveis desta sessão, não valores
já travados em nenhum documento anterior desta linha para uso especificamente
sobre dado real do Estágio 2 — sinalizados aqui para revisão explícita ANTES
de qualquer commit de lock, por instrução de `DISC-DEC-027`.

### 12.1 `N_MC=200`

Escolhido por continuidade com a convenção JÁ TRAVADA para execuções sobre
dado real desta mesma linha de teste (`../PREREGISTRATION.md` Seção 4c
Gap(e) item 1: "`N_MC=200` realizações completas... mesma convenção de
Chae — 'the distribution of medians in a bin is well determined for N>100 MC
realizations'"), não o `N_MC=120` usado no Estágio 1 (que foi reduzido só
por velocidade de validação sintética, `RESULTS_SUMMARY_STAGE1.md` Seção 2).
Custo computacional: `200×30.203≈6,04×10⁶` avaliações de desprojeção por
ramo (real+mock) por avaliação de `f_multi` na bisseção — cerca de `6,3×`
o custo do Estágio 1 (`120×8.000≈9,6×10⁵`), mas usando as mesmas rotinas
`numpy` vetorizadas já validadas, sem laço Python por sistema. Julgamento:
razoável manter `200` por já ser o valor travado para dado real desta linha
especificamente, mas a sessão orquestradora deve confirmar que o orçamento
computacional disponível comporta isso multiplicado pelas ~2-4 avaliações
de `f_multi` que a bisseção `brentq` tipicamente precisa até convergir.

### 12.2 `N_bootstrap=2000` (tanto para `n_bootstrap_final` de
`calibrate_f_multi` quanto para `bootstrap_a0_refit`)

`ADVERSARIAL_VERIFICATION.md` item 3 (Frente 2) documentou explicitamente:
"`N_bootstrap=400`/`N_bootstrap_a0_refit=300` são baixos para um IC95%
percentil preciso (~7-10 réplicas definem cada cauda)... Recomendação para
o Estágio 2: `N_bootstrap>=1000-2000`." Este rascunho escolhe o **topo**
dessa faixa recomendada (`2000`, não `1000`): a `2000` réplicas, cada cauda
de 2,5% é definida por `~50` réplicas (vs. `~7-10` em `N=300`-`400`,
`~25` em `N=1000`) — uma redução substancial no ruído de estimação de
percentil, especificamente relevante para margens "por pouco" como a já
observada no resultado v2 original (`0,057` dex) e no cenário
`f_multi_true=0,35` da Validação B do Estágio 1. Custo computacional do
bootstrap em si é baixo relativo ao `N_MC` (reamostra índices já computados,
sem recomputar desprojeção — `run_delta_obs_newt_selfcal` docstring, "sem
custo combinatório de recomputar 1000×200 desprojeções completas"), então o
custo marginal de `2000` vs. `1000` réplicas é pequeno. **Julgamento
explícito para a sessão orquestradora confirmar:** `2000` é uma escolha desta
sessão, não uma extrapolação mecânica da recomendação (que foi "1000-2000");
se o orçamento de tempo de execução do Estágio 2 for uma restrição prática
maior do que esta sessão está avaliando, `1000` também satisfaz a
recomendação mínima documentada e é uma alternativa igualmente defensável.

### 12.3 `SEED_STAGE2=20260822`

Proposto por analogia com a convenção já usada nesta linha para sementes de
lock documentadas por data (`discovery_holdout_split.json` usa
`seed=20260814`, a data do lock daquele split) — `20260822` é a data desta
sessão de rascunho, não necessariamente a data do lock efetivo deste
documento (que pode ocorrer em outra data). **Julgamento explícito:** o
valor numérico exato da semente não tem nenhum efeito sobre a validade do
método (é apenas um ponto de partida determinístico e documentado, mesma
disciplina já aplicada a todas as sementes desta linha) — a sessão
orquestradora deve decidir se prefere fixar a semente na data efetiva do
lock deste documento (mais consistente com a convenção `discovery_holdout_split.json`)
ou manter `20260822` independentemente da data de lock (mais simples, sem
ambiguidade de "qual data conta"). Qualquer escolha é aceitável desde que
fixada ANTES da primeira execução sobre dado real e documentada no commit
de lock.

### 12.4 Nota adicional (não uma escolha numérica, um risco de implementação já sinalizado na Seção 4.5)

A necessidade de reutilizar manualmente a semente `SEED_STAGE2+777` entre a
chamada de `calibrate_f_multi()` (Passo 1) e a chamada direta de
`run_delta_obs_newt_selfcal(...,return_raw=True)` (Passo 4.5) é um detalhe de
implementação frágil — um candidato natural para `calibrate_f_multi()`
ganhar um parâmetro opcional `return_raw: bool=False` que propague para sua
chamada final interna, eliminando a necessidade de duplicar a chamada e o
risco de descasamento de semente. Esta seria uma mudança de código
aditiva (nova opção, comportamento default inalterado) sobre um módulo já
travado do Estágio 1 (`analysis/selfcal_pipeline.py`) — fora do escopo deste
rascunho de pré-registro alterar código, mas sinalizada aqui como uma
melhoria de robustez recomendada para a sessão orquestradora avaliar antes
ou depois do lock, mesmo padrão de "correção delimitada e pré-declarada"
já usada nesta trilha.

---

## [Preenchido depois da análise] Resultado

*(vazio — este documento é um rascunho; nenhuma análise sobre dado real foi
executada. Preenchido somente após o lock deste documento e a execução
autorizada em separado por `DISC-DEC-027` ou decisão subsequente.)*

## [Preenchido depois da reexecução adversarial] Veredito adversarial

*(vazio — mesma razão acima.)*
