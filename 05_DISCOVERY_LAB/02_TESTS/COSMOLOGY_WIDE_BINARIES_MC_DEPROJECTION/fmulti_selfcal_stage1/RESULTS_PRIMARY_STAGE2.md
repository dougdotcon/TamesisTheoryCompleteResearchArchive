# Resultados — Estágio 2: análise primária sobre a amostra de descoberta real

**Data:** 2026-08-22
**Test ID:** `SPARC-FMULTI-STAGE2` (etapa de `DISC-COSMOLOGY-MOND-SPARC-004`)
**Pré-registro:** `PREREGISTRATION_STAGE2.md` (Status: LOCKED, `DISC-DEC-029`)
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-22 — agente
de análise primária (implementador). **Este documento NÃO é a reexecução
adversarial** (`AGENTS.md` passo 7) — essa é obrigatória, separada, e ainda
pendente (ver Seção 8 abaixo).
**Script:** `analysis/run_stage2_primary_analysis.py`
**Resultado numérico completo:** `results/result_stage2_primary.json`

> **Status deste resultado:** análise primária concluída, íntegra e
> reprodutível (semente fixa `SEED_STAGE2=20260822`). **NÃO catalogado**
> como fechado — pendente (1) reexecução adversarial padrão (`AGENTS.md`
> passo 7) e (2) papel de debunker de descoberta adversarial de nulos
> (`METHODOLOGY_EXTENSIONS.md` Seção 5), ambos exigidos antes de qualquer
> integração em `TEST_QUEUE.yaml`/`DECISION_LEDGER.yaml` — arranjados pela
> sessão orquestradora, fora do escopo deste agente.

## 0. Resumo executivo

A auto-calibração completa de `f_multi` (Chae 2023 Eqs. 11-13, validada
sinteticamente no Estágio 1) foi aplicada pela primeira vez à amostra de
descoberta real (**30.203 sistemas**, holdout selado de 12.944 sistemas
**nunca acessado**), exatamente conforme a sequência de chamadas da Seção 4
do pré-registro travado. `f_multi_hat=0,1037` calibrado com sucesso
(`converged_bracket=True`). O `δ_obs-newt` corrigido por essa calibração é
pequeno em todos os 5 bins (`+0,078` a `-0,0002` dex) — MUITO menor que o
sinal bruto v2 original (`+0,149` a `+0,043` dex,
`../PREREGISTRATION.md` Seção 7c). O `a0` ajustado sobre esse sinal
corrigido é `a0_fit=6,125×10⁻¹¹` m/s² (IC95% bootstrap
`[4,120×10⁻¹¹; 8,581×10⁻¹¹]`, `N_bootstrap=2000`, robusto a semente/N
alternativos).

**Veredito mecânico (Seção 5, camada 1):** $a_0^A$ e $a_0^B$ ambos FORA do
IC95% → `BOTH_FALSIFIED`.
**Veredito após a camada interpretativa obrigatória (Seção 5, camada 2):**
dividir o IC pelo fator de viés residual conhecido (1,4-1,6×) **NÃO** traz
$a_0^A$ nem $a_0^B$ de volta para dentro do intervalo — a camada
interpretativa **não muda** o veredito. **Veredito final: `BOTH_FALSIFIED`,
sujeito à reexecução adversarial e ao debunker obrigatório antes de ser
aceito como fechado.**

Dois dos cinco gatilhos adversariais pré-declarados da Seção 6 dispararam
(gatilho 3: `f_multi_hat` bem abaixo da faixa observacional 0,25-0,47;
discutido em detalhe na Seção 4 abaixo). Os outros três (bracket
não-convergido, `a0_fit` catastroficamente fora de faixa, padrão de
`δ_obs-newt` qualitativamente inconsistente com a assinatura do Estágio 1,
sensibilidade do IC a `N_bootstrap`/semente) **não** dispararam.

## 1. Amostra e insumos

- **30.203 sistemas de descoberta** carregados de
  `../COSMOLOGY_WIDE_BINARIES/data/quality_filtered_sample.parquet`
  (cruzado com `../data/hwang_eccentricity_subset.parquet`), filtrados
  pela lista `discovery_pair_ids` de
  `../COSMOLOGY_WIDE_BINARIES/data/discovery_holdout_split.json`
  (`seed=20260814`).
- **Holdout selado NUNCA tocado** — ver Seção 7 abaixo (disciplina
  explícita, checada por grep automatizado no próprio script).
- `M1_cat`/`M2_cat` de `M1_Msun`/`M2_Msun` catalogados; `v_p_real` pela
  fórmula travada $v_p=4,74047\times10^{-3}\Delta\mu\, \bar d$; excentricidade
  de Hwang (`e`,`e0`,`e1`,`alpha`,`dpm_sig`); erros de PM por componente
  (`e_pmRA1/2`,`e_pmDE1/2`) para o orçamento de ruído astrométrico simétrico
  do ramo mock.
- `v_p_real` mediana = 0,5336 km/s; `M1_cat` mediana = 0,6029 M☉, `M2_cat`
  mediana = 0,3179 M☉ (30.203 sistemas, 6.039-6.042 por bin — conferido).

## 2. Passo 1 — auto-calibração de `f_multi`

Chamada exata da Seção 4.2 do pré-registro:
`calibrate_f_multi(..., n_mc=200, seed=20260822, xtol=5e-4, f_lo=0.0,
f_hi=0.9, include_wobble=True, n_bootstrap_final=2000, return_raw=True)`.

| diagnóstico | valor |
|---|---|
| `f_multi_hat` | **0,103666** |
| `converged_bracket` | **True** |
| `δ_ancora(f_lo=0)` | +0,053889 |
| `δ_ancora(f_hi=0,9)` | −0,761547 |
| tempo de execução | 356,8 s |

O bracket confirma troca de sinal genuína (não um valor forçado na borda) —
pré-condição do gatilho 2 da Seção 6, **não disparado**.

## 3. Passo 2 — `δ_obs-newt(bin)` corrigido

Extraído de `calib["final_result"]` (semente interna `seed+777`, DIFERENTE
da usada na bisseção, teste fora-da-amostra por desenho — Seção 4.3 do
pré-registro, `SOUND` desde `ADVERSARIAL_VERIFICATION.md` Estágio 1):

| bin | `log10(gN)` | `gN_bin_median` (SI) | `n_sys` | `δ_obs-newt` corrigido | IC95% (`N=2000`) |
|---|---|---|---|---|---|
| 0 (menor gN) | [−11,7012;−9,1728] | 1,8807×10⁻¹⁰ | 6042 | **+0,0777** | [+0,0495; +0,1041] |
| 1 | [−9,1728;−8,4667] | 1,6645×10⁻⁹ | 6040 | **+0,0657** | [+0,0399; +0,0924] |
| 2 | [−8,4667;−7,9752] | 6,2203×10⁻⁹ | 6040 | **+0,0486** | [+0,0223; +0,0746] |
| 3 | [−7,9752;−7,5548] | 1,7190×10⁻⁸ | 6039 | **+0,0417** | [+0,0164; +0,0686] |
| 4 (âncora, maior gN) | [−7,5548;−6,5224] | 4,8638×10⁻⁸ | 6042 | **−0,0002** | [−0,0254; +0,0255] |

`frac_has_multi` no `f_multi_hat` calibrado = 0,1035 (bate com `f_multi_hat`,
como esperado — Bernoulli(f_multi) sobre `n_mc×n_sys`).
`frac_nonzero_wobble` = 0,1035 (idêntico, wobble só afeta sistemas com
companheira injetada, por desenho).

O bin-âncora fica, por construção, consistente com zero (IC contém 0) —
confirma que a bisseção calibrou corretamente. Os 4 bins restantes mantêm
um resíduo positivo pequeno (0,04-0,08 dex) que **declina monotonicamente**
do menor para o maior `gN` — mesma direção qualitativa (não mesma
magnitude — bem MENOR) do padrão já documentado no Estágio 1 como
assinatura do modelo de wobble simplificado que não decai o suficiente com
`gN` (Seção 4/gatilho 4 abaixo).

## 4. Passo 3 — ajuste de `a0`

`fit_a0(gN_bin_median, δ_obs-newt_corrigido, x0)`:

| `x0` | `a0_fit` (m/s²) |
|---|---|
| 1,0 | 6,124696×10⁻¹¹ |
| 5,0 | 6,124648×10⁻¹¹ |

Diferença relativa entre pontos de partida: `7,83×10⁻⁶` — **convergência
confirmada** (idêntico ao nível de precisão numérica do otimizador, muito
abaixo do limiar de 1×10⁻⁴).

## 5. Passos 4-5 — IC95% via `bootstrap_a0_refit(calib["final_raw"], ...)`

**Usado `calib["final_raw"]` diretamente (parâmetro `return_raw=True`
adicionado por `DISC-DEC-029`), NÃO uma chamada manual reconstruída de
`run_delta_obs_newt_selfcal`** — elimina por construção o risco de
descasamento de semente identificado como "ponto de maior risco de erro
silencioso" na Seção 4.5/12.4 do pré-registro. `N_bootstrap=2000`,
`seed=21260821` (`SEED_STAGE2+999999`).

| `x0` | IC95% inferior | IC95% superior |
|---|---|---|
| 1,0 (primário) | 4,119617×10⁻¹¹ | 8,580760×10⁻¹¹ |
| 5,0 | 4,016289×10⁻¹¹ | 8,580629×10⁻¹¹ |

Os dois pontos de partida concordam (diferença relativa `<5%` em ambas as
bordas) — IC usado para a decisão: **`[4,1196×10⁻¹¹; 8,5808×10⁻¹¹]`** m/s²
(refit `x0=1,0`, consistente com o `x0` do ajuste primário).

## 6. Regra de decisão (Seção 5 do pré-registro) — as duas camadas

### 6a. Camada mecânica

- $a_0^A=1,082288\times10^{-10}$: **FORA** do IC95%
  (`8,5808\times10^{-11}<a_0^A`, margem de exclusão = **0,1008 dex**
  ≈ fator 1,26×).
- $a_0^B=6,800218\times10^{-10}$: **FORA** do IC95% (margem de exclusão =
  **0,8990 dex** ≈ fator 7,93×, muito mais decisivo).
- **Veredito mecânico: `BOTH_FALSIFIED`.**

### 6b. Camada interpretativa obrigatória (viés residual 1,4-1,6× do Estágio 1)

Dividindo a borda inferior do IC por 1,6× e a superior por 1,4× (o
intervalo de-viesado mais generoso fisicamente defensável, dando a H_A/H_B
o benefício máximo da dúvida dado o range documentado do viés):

$$\text{IC de-viesado} = [4,1196\times10^{-11}/1,6;\ 8,5808\times10^{-11}/1,4]
= [2,5748\times10^{-11};\ 6,1291\times10^{-11}]$$

- $a_0^A$ dentro do IC de-viesado? **Não** (margem residual, agora
  **0,2469 dex** — a correção pelo viés PIORA a exclusão, não a resolve).
- $a_0^B$ dentro do IC de-viesado? **Não** (margem residual **1,0451 dex**).

**A camada interpretativa NÃO muda o veredito.** Isto é fisicamente
coerente, não um artefato: o viés documentado do Estágio 1 (Validação B,
`RESULTS_SUMMARY_STAGE1.md`) atua na direção de **superestimar** `a0_true`
— corrigi-lo empurra a estimativa **para baixo**. Como `a0_fit=6,125×10⁻¹¹`
já está ABAIXO tanto de $a_0^A$ quanto de $a_0^B$ (não acima, como no
cenário original que motivou a camada interpretativa — o resultado v2 bruto
de `../PREREGISTRATION.md` Seção 7c, onde o sinal NÃO-corrigido por
multiplicidade estava inflado acima de $a_0^A$), aplicar a correção de
viés na direção especificada pelo pré-registro afasta ainda mais o
intervalo de $a_0^A$/$a_0^B$, não os resgata. A checagem foi feita
honestamente, exatamente como especificada — o resultado é que ela não se
aplica de forma a reverter esta falsificação específica.

### 6c. Veredito final

**`BOTH_FALSIFIED`** (mecânico e interpretativo concordam). **Este
veredito é reportado como análise primária — NÃO está catalogado como
fechado.** Por instrução explícita do último parágrafo da Seção 6 do
pré-registro, qualquer veredito diferente de "nenhum sinal detectável acima
do ruído" (o que inclui `BOTH_FALSIFIED`) precisa passar pelo papel de
debunker de `METHODOLOGY_EXTENSIONS.md` Seção 5 antes de ser aceito — ver
Seção 8 abaixo.

## 7. Gatilhos adversariais da Seção 6 — todos os 5, checados explicitamente

| # | gatilho | disparou? | detalhe |
|---|---|---|---|
| 1 | `a0_fit` fora da faixa plausível de AMBAS H_A e H_B por >1 ordem de grandeza | **Não** | `a0_fit` está a apenas 0,2473 dex de $a_0^A$ (fator ~1,77×) — MUITO dentro de 1 ordem de grandeza; está a 1,0454 dex de $a_0^B$ (pouco acima de 1 ordem, mas a condição do gatilho exige AMBAS simultaneamente) |
| 2 | `converged_bracket=False` OU `f_multi_hat` a menos de `xtol` da borda do bracket | **Não** | `converged_bracket=True`; `f_multi_hat=0,1037` está a `0,1037` de `f_lo=0` e `0,7963` de `f_hi=0,9`, ambos ≫ `xtol=5×10⁻⁴` |
| 3 | `f_multi_hat` fora de 0,25-0,47 (margem grande) | **SIM** | `f_multi_hat=0,1037` está **0,1463** abaixo do limite inferior da faixa observacional da literatura — ver discussão abaixo |
| 4 | padrão de `δ_obs-newt` qualitativamente inconsistente com a assinatura do Estágio 1 | **Não** | Todos os 4 bins não-âncora têm o MESMO sinal (positivo), magnitude (0,04-0,08 dex) MENOR que o range de referência do Estágio 1 (0,15-0,22 dex, não maior), concentração no bin de menor `gN` declinando monotonicamente até o bin-âncora (que fica consistente com zero, como esperado por construção) — mesma direção qualitativa do Estágio 1, magnitude até mais branda |
| 5 | IC sensível à escolha de `N_bootstrap`/semente | **Não** | semente alternativa (`N=2000`): IC `[3,951×10⁻¹¹;8,569×10⁻¹¹]`, mesmo veredito `BOTH_FALSIFIED`; `N_bootstrap=1000` (mesma semente base): IC `[4,119×10⁻¹¹;8,591×10⁻¹¹]`, mesmo veredito — robusto |

**Discussão do gatilho 3 (o único disparado):** `f_multi_hat=0,1037`
calibrado é menos da metade do limite inferior da faixa observacional
agregada da literatura (0,25-0,47, referência de Chae Artigo B). Isto NÃO
invalida a calibração por si só — é uma checagem de CONSISTÊNCIA
secundária (`METHODOLOGY_ADDENDUM.md` Seção 2 item 4), não o mecanismo
primário de correção — mas é um desvio real que merece registro honesto,
não descarte silencioso, por instrução explícita do pré-registro. Leituras
possíveis (não decididas aqui, matéria para a reexecução adversarial/
debunker): (a) a amostra de 30.203 sistemas já passou por cortes de
qualidade (`R<0,01`, concordância de distância 3σ, erro relativo de PM
`<0,01`) que podem preferencialmente excluir sistemas com companheiras
ocultas mais óbvias (RUWE alto, astrometria ruidosa), tornando a fração
RESIDUAL de multiplicidade oculta nesta amostra especificamente
FILTRADA menor que a fração populacional bruta citada pela literatura; (b)
o modelo de injeção (`γ_M=-0,7` fixo, wobble simplificado) pode não
capturar toda a física necessária para que o bin-âncora precise de
`f_multi` mais alto para zerar; (c) simples variação amostral/populacional
entre este catálogo (Gaia EDR3 wide binaries, El-Badry+2021) e as amostras
que embasam a faixa 0,25-0,47 na literatura. **Não decidido aqui — matéria
declarada explicitamente para a reexecução adversarial e o debunker.**

## 8. Checagem de consistência secundária — RUWE (informativa, NÃO parte da decisão)

Fração de sistemas com `RUWE1>1,4` ou `RUWE2>1,4` (limiar padrão de
astrometria Gaia degradada): **19,15%**, quase o dobro de `frac_has_multi`
no `f_multi_hat` calibrado (**10,35%**). Qualitativamente consistente com
"existe alguma população com astrometria degradada além do que o `f_multi`
calibrado captura" — mas RUWE alto tem causas além de companheira oculta
não-resolvida (má qualidade de solução astrométrica em geral), e esta
comparação não é 1:1 (fração populacional fixa vs. probabilidade Bernoulli
por realização MC). Reportado como contexto, não usado na regra de
decisão — mesma disciplina do `METHODOLOGY_ADDENDUM.md` Seção 2 item 4.

## 9. Disciplina do holdout selado — confirmação explícita

`../COSMOLOGY_WIDE_BINARIES/data/discovery_holdout_split.json` foi aberto
**apenas** para extrair as chaves `discovery_pair_ids` (lista) e
`n_discovery` (contagem inteira, 30203) — as chaves `holdout_pair_ids` e
`n_holdout` **nunca** foram acessadas em nenhum ponto do script
`analysis/run_stage2_primary_analysis.py`. Verificado programaticamente
pela própria checagem de auto-grep 9.3 embutida no script (roda ANTES de
tocar qualquer coluna real, resultado salvo em
`results/STAGE2_9_3_GREP_CHECK.txt`): confirma ausência de qualquer
referência de I/O real a `catalog.parquet` (arquivo bruto mais amplo, não
usado) e ausência de qualquer acesso de dicionário `["holdout_pair_ids"]`
ou `["n_holdout"]` no arquivo-fonte. **`pass: true`.** Nenhum dado FÍSICO
(velocidade, massa, separação, excentricidade, RUWE) de nenhum sistema do
holdout foi lido, computado, ou usado em qualquer checagem deste Estágio.

## 10. Próximos passos obrigatórios (fora do escopo deste agente)

1. **Reexecução adversarial padrão** (`AGENTS.md` passo 7) — segundo
   agente, implementação independente do zero, mesma proveniência de dado,
   instruído a tentar refutar (não confirmar) este resultado. Item
   prioritário sinalizado pelo próprio pré-registro (Seção 4.5): confirmar
   que `calib["final_raw"]` realmente carrega a mesma semente `seed+777`
   usada para `calib["final_result"]` (mitigado por construção pelo
   parâmetro `return_raw` de `DISC-DEC-029`, mas a reexecução deve
   confirmar isso por inspeção, não só confiar na descrição).
2. **Papel de debunker de descoberta adversarial de nulos**
   (`METHODOLOGY_EXTENSIONS.md` Seção 5) — obrigatório porque o veredito
   (`BOTH_FALSIFIED`) não é "nenhum sinal detectável acima do ruído".
   Candidatos a investigar meramente citados aqui (não resolvidos): a
   discrepância do gatilho 3 (`f_multi_hat` bem abaixo da faixa da
   literatura — Seção 7 acima), e se o modelo de wobble simplificado
   (conhecidamente imperfeito, Seção 7 do pré-registro) poderia, ele
   mesmo, estar mascarando ou distorcendo o sinal residual de forma que
   uma explicação inteiramente convencional (sem qualquer física Tamesis)
   ainda dê conta do padrão observado — mesmo espírito da checagem que já
   decidiu o fechamento `CLOSED_INCONCLUSIVE` do teste anterior.
3. Só após 1 e 2: integração em `TEST_QUEUE.yaml`/`CLAIM_LEDGER.yaml`,
   decisão sobre se este resultado é candidato ao Gate de Replicação
   (`03_REPLICATION_GATE/PROTOCOL.md`, que abriria o holdout selado).

**Nenhuma linguagem além de "falsificação por este canal específico,
análise primária, pendente de reexecução adversarial e debunker" é usada
neste documento** — nenhuma alegação de "Tamesis confirmado/refutado" (
`AGENTS.md` Proibições).

## 11. Deviações do pré-registro

**Nenhuma.** Todos os parâmetros numéricos (bin edges, `anchor_bin=4`,
`n_mc=200`, `N_bootstrap=2000`, `seed=20260822`, `xtol=5×10⁻⁴`,
`include_wobble=True`, `real_gets_astrometric_noise=False` não
sobrescrito), a sequência exata de chamadas (Seção 4.1), e a regra de
decisão de duas camadas (Seção 5) foram seguidos literalmente. A única
correção feita durante esta análise foi um bug de diagnóstico NO PRÓPRIO
script deste Estágio (não no pipeline travado `selfcal_pipeline.py`/
`companion_injection.py`, ambos usados sem modificação): a heurística
inicial do gatilho 4 tratava o resíduo numérico do bin-âncora (calibrado
para ~0 por construção) como uma "troca de sinal" espúria contra os outros
bins, disparando o gatilho 4 incorretamente na primeira execução; corrigido
para excluir bins com `|δ|<0,01` dex (mesmo limiar de negligibilidade já
usado em `validate_b_recover_a0_with_contamination.py`) da checagem de
uniformidade de sinal, e a análise completa foi re-executada do zero com o
script corrigido — todos os demais números (f_multi_hat, δ_obs-newt,
a0_fit, IC95%, vereditos) são **idênticos, bit a bit**, entre a execução
original e a corrigida, confirmando que o bug estava isolado ao
diagnóstico do gatilho 4 e não afetou nenhum outro cálculo. Isto é uma
correção de bug em código de diagnóstico adversarial escrito por este
próprio agente para este Estágio, não uma reformulação de hipótese,
estatística de teste, modelo nulo, ou critério de decisão do pré-registro
— mesma disciplina já estabelecida em `../PREREGISTRATION.md` Seção 5b.
