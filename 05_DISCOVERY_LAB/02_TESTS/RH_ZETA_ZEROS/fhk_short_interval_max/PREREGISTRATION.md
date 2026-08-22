# Pré-registro: máximo de |ζ| em intervalos curtos — FHK (−3/4) vs iid/REM (−1/4)

**Status:** LOCKED
**Data de lock:** 2026-08-21
**Autor (agente/sessão):** Tamesis Discovery Lab, onda 2, frente
`DISC-RH-FHK-SHORT-INTERVAL-MAX-001` (Claude Code)
**Linha:** `DISC-RH-REAL-001`. **Governança:** `DISC-DEC-014`
(última entrada de `00_GOVERNANCE/DECISION_LEDGER.yaml`).
**Evidence level alvo:** teste pré-registrado (não exploratório) — mas ver
Seção 8: NENHUM resultado deste teste constitui alegação sobre RH.

> Escrito e travado DEPOIS do piloto de viabilidade (somente tempo), DEPOIS
> das três validações sintéticas (Seções 4–5) e ANTES de qualquer avaliação
> de ζ nos offsets do teste real. Nenhum valor de `max log|Z|` foi computado
> na banda de teste `[T, 2T]` de nenhuma das 7 alturas primárias com os
> seeds desta frente. A calibração de viés de grade (Seção 5c) avaliou ζ
> SOMENTE na banda descartável disjunta `[2T+10, 2,1T]` e registrou SOMENTE
> diferenças de refinamento (nunca os máximos). A triagem de 2026-08-21
> (`../phase0_zeta_eval_triage/`, M=300, seed 20260821, 3 alturas) é
> exploratória, anterior e independente deste lock; sua influência sobre
> este desenho está declarada na Seção 9 (limitações).

## 0. Por que este teste existe

A triagem exploratória dos itens 5/6/10 (`TRIAGE_RESULTS.md`, DISC-DEC-013)
identificou o item 10 como a única pergunta genuinamente falsificável com
modelo concorrente NOMEADO do lote: o termo subdominante do máximo de
log|ζ| em intervalos curtos da linha crítica. A triagem mediu inclinação
−0,408 ± 0,184 (M=300, 3 alturas) — compatível com AMBOS os modelos,
subpotente por desenho. `DISC-DEC-014` autorizou desenhar e travar este
pré-registro, exigindo validação de pipeline contra ground truth sintético
ANTES do lock (cumprida, Seções 4–5).

## 1. Hipóteses exatas — dois modelos concorrentes nomeados

Para intervalos de comprimento 2π na altura T, com
`M*(t₀) = max_{t∈[t₀,t₀+2π)} log|ζ(1/2+it)|`:

- **H_FHK** (Fyodorov–Hiary–Keating, arXiv:1202.4713, verificado por fetch
  no arXiv em 2026-08-21 pela triagem; ordem líder provada em
  arXiv:1612.08575, Arguin–Belius–Bourgade–Radziwiłł–Soundararajan, idem):
  `E[M*] = loglog T − (3/4)·logloglog T + O(1)` — assinatura do campo
  log-correlacionado / transição de congelamento.
- **H_iid** (modelo concorrente REM/iid): os valores de log|ζ| no intervalo
  comportam-se como ~log(T/2π) variáveis Gaussianas independentes com a
  variância de Selberg; isso dá
  `E[M*] = loglog T − (1/4)·logloglog T + O(1)`.

O coeficiente do termo `logloglog T` (−3/4 vs −1/4) é o discriminante
assintótico. **Em altura finita (T ≤ 10¹⁰) as duas famílias são
representadas por CURVAS CALIBRADAS explícitas** (Seção 4), porque as
validações mostraram que as inclinações efetivas em altura finita diferem
substancialmente dos coeficientes assintóticos — o teste decide entre as
curvas calibradas dos dois modelos, e reporta a comparação assintótica
apenas como descritor secundário (continuidade com a triagem).

## 2. Motor de avaliação e dados

- **Motor:** `rs_zeta.py` desta pasta — cópia byte a byte, com nota de
  atribuição, do motor Riemann–Siegel vetorizado validado da triagem
  (`../phase0_zeta_eval_triage/rs_zeta.py`): validação PASSOU em 5
  critérios contra mpmath e zeros reais de Odlyzko, com registro de falha
  preservado (`validation_zeta_eval_run1_FAILED.log`) e bug de fase 2π
  corrigido pré-uso. Domínio validado t ∈ [2000, 10¹¹]; erro absoluto em Z
  dentro de tolerâncias por faixa (máx 5×10⁻⁴) — desprezível para máximos
  O(1)–O(3) de log|Z|.
- **Dado real:** avaliação direta de ζ(1/2+it) via Z(t); nenhuma tabela
  externa entra na estatística.
- **Aritmética:** `|Z(t)| = |ζ(1/2+it)|`, então `max log|Z| = max log|ζ|`
  no intervalo.

## 3. Estatística de teste (exata, sem graus de liberdade restantes)

1. **Alturas primárias** (k = 0..6, ordem declarada):
   T ∈ {10⁴, 10⁵, 10⁶, 10⁷, 10⁸, 10⁹, 10¹⁰}.
2. **Offsets**: por altura, `starts = sort(default_rng(20260822·100 + k)
   .uniform(T, 2T, M_T))` — determinístico. M_T = 2000 para k=0..4;
   M=1600 em 10⁹; M=1000 em 10¹⁰ (fixados pela conta de orçamento da
   Seção 5, ANTES de qualquer computação real). Banda `[T,2T]` é disjunta
   das bandas descartáveis `[2T+10, 2,1T]` do piloto de tempo (seed
   99991111) e da calibração de grade (seed 77770707) — offsets
   descartáveis documentados em `phase0_timing.json` e
   `validation_grid_bias.json`.
3. **Grade**: 512 pontos igualmente espaçados por intervalo
   (passo 2π/512 ≈ 0,0123; ≥ 24 pontos por espaçamento médio de zeros em
   todas as alturas primárias).
4. **Correção de viés de grade** (travada, Seção 5c): à média de M* por
   altura soma-se `c_T` (Richardson 512→2048, fator 16/15), com
   `EP(c_T)` propagado: `EP_T² = sd_T²/M_T + EP(c_T)²`.
5. **Regressão**: `y_T = mean(M*)+c_T − loglog T` sobre `x_T = logloglog T`,
   WLS com intercepto livre e pesos `w_T = 1/EP_T²` (sd empírico).
   Estatística final: inclinação `b̂ ± EP(b̂)` (EP da WLS).
6. Implementação única e fechada: `run_primary.py` (fatias com checkpoint;
   `analyze` aplica exatamente as fórmulas acima e a regra da Seção 6).

## 4. Curvas calibradas dos dois modelos (TRAVADAS pelas validações)

Inclinações efetivas de altura finita `p` (mesma WLS da Seção 3, pesos de
desenho), computadas ANTES do lock pelas validações sintéticas; variantes
de discretização declaradas (canônica + estresse):

| Modelo/variante | Definição | p (inclinação efetiva) | EP(p) |
|---|---|---|---|
| **iid_v1 (canônica)** | n_T = log(T/2π) pontos iid N(0, σ²), σ² = ½·loglog T (Selberg) | **+0,0072** | ~0 (quadratura exata) |
| iid_v2 (estresse) | idem, σ² = ½·loglog(T/2π) (variância casada ao CUE) | +0,1352 | ~0 |
| iid_v3 (estresse) | n_T = log T (sobre-contagem deliberada), σ² = ½·loglog T | −0,2235 | ~0 |
| **cue_v1 (canônica)** | máximo de log\|pol. caract.\| de Haar-U(N) no círculo, N_T = log(T/2π) (densidade de Riemann–von Mangoldt) | **−0,4160** | 0,0125 (MC) |
| cue_v2 (estresse) | idem, N_T = log T | −0,6871 | 0,0141 (MC) |

Racional das canônicas: a contagem de zeros num intervalo de comprimento
2π na altura T é ~log(T/2π) (densidade RvM) — logo n_T/N_T = log(T/2π); a
variância pontual de log|ζ| é a de Selberg (½·loglog T, arXiv:1509.06827).
As variantes de estresse cobrem as ambiguidades honestas de discretização
(σ² alternativa; contagem log T). Os cinco números acima estão TRAVADOS em
`validation_iid_null.json` e `validation_cue.json` e não serão recalculados.

## 5. Validações pré-lock (todas PASSARAM; logs preservados)

- **(a) lado iid/REM** (`validate_iid_null.py`, seed 31415926): (A1) a
  curva exata do modelo recupera o coeficiente assintótico −1/4
  (inclinação −0,2292 em L=10⁷, aproximação monótona ✓); (A2) o estimador
  WLS com pesos empíricos é não-viesado sobre 400 réplicas sintéticas do
  desenho completo (viés −0,0002, tolerância 0,0077 ✓); (A3) cobertura de
  95% = 0,963 ∈ [0,917, 0,983] ✓. `validation_iid_null.{json,log}`.
- **(b) lado FHK/CUE** (`validate_cue.py`, seed 27182818, amostragem de
  Haar por QR de Ginibre com correção de fase — Mezzadri,
  arXiv:math-ph/0609050, título/autor verificados por fetch em
  2026-08-21): E[max] por N ∈ {7..23} com 8000 matrizes/N em grade 4096;
  (B1) tendência em N grandes {64,128,256}: inclinação −0,853, do lado FHK
  (aceite < −0,5) ✓; (B2) EP MC de p_cue_v1 = 0,0125 < 0,02 ✓; (B3)
  sanidade Haar ✓. Limitação declarada: N ∈ [7,23] está longe do regime
  assintótico — por isso a curva CALIBRADA (não o −3/4) é o alvo primário.
  Rodada 1 falhou na serialização JSON APÓS toda a computação
  (determinística); preservada em `validation_cue_run1_FAILED.log`,
  correção para frente, rodada 2 reproduziu os mesmos números.
  `validation_cue.{json,log}`.
- **(c) viés de grade** (`validate_grid_bias.py`, seed 77770707, banda
  descartável [2T+10, 2,1T], SÓ diferenças registradas): correções
  c_T ∈ [+0,0002, +0,0049] (todas positivas < 0,02 ✓), EP(c_T) ≤ 0,0033 ✓,
  contribuição do gradiente do viés para a inclinação = −0,0028 (<0,05) ✓ —
  o viés de grade não vira o veredito nem sem correção; com a correção
  aplicada o resíduo é de segunda ordem. `validation_grid_bias.{json,log}`.
- **Custo (piloto, somente tempo, `phase0_timing.{py,json,log}`)**: por
  intervalo @512: 5,0 ms (10⁴) … 4,16 s (10¹⁰). Custo primário projetado
  8957 s + calibração 511 s + piloto ~150 s ≈ 9,6 ks < teto 10800 s (~3 h)
  do mandato. O desenho de ~8σ da triagem (M=2000 incl. 10¹¹) NÃO cabe no
  teto (10¹¹ sozinha custaria ~15,4 s/int ⇒ >9 ks); o desenho travado
  (Seção 3) troca 10¹¹ por mais alturas baixas + M maiores e ALCANÇA poder
  projetado MAIOR (Seção 6), com 10¹¹ preservada como holdout selado.

## 6. Regra de decisão TRINÁRIA (travada) e poder

Com `b̂ ± EP(b̂)` da Seção 3 e, para cada modelo m da tabela da Seção 4,
`z_m = (b̂ − p_m)/√(EP(b̂)² + EP(p_m)²)`:

- **FHK_FAVORED** ⟺ |z_cue_v1| < 3 E |z_iid_v1| ≥ 5 E |z_iid_v2| ≥ 5 E
  |z_iid_v3| ≥ 3.
- **IID_FAVORED** ⟺ |z_iid_v1| < 3 E |z_cue_v1| ≥ 5 E |z_cue_v2| ≥ 3.
- **INCONCLUSIVE** caso contrário, com subcaso anotado:
  `NEITHER_MODEL` (ambas canônicas rejeitadas a 3σ — negativo informativo),
  `UNDERPOWERED` (ambas compatíveis), ou `PARTIAL` (exclusão de um lado sem
  os requisitos completos do outro).

Não há busca sobre estatísticas alternativas, alturas, M, grades ou pesos:
uma única inclinação, uma única regra. Sem correção de múltiplas
comparações além da própria estrutura conservadora (5σ contra o lado
rejeitado, banda estreita de 3σ no lado aceito).

**Poder (pré-computado, EPs projetados EP(b̂)=0,0369; a regra usa os EPs
medidos):** separação canônica |p_cue_v1 − p_iid_v1| = 0,423 ⇒ 10,9σ.
Bandas projetadas de veredito: FHK_FAVORED para b̂ ∈ [−0,533, −0,335];
IID_FAVORED para b̂ ∈ [−0,104, +0,118]. Poder ≈ 98% se ζ segue a curva
CUE canônica; ≈ 99% se segue a iid canônica. **Zona declarada de
inconclusão por ambiguidade de modelo:** b̂ ∈ (−0,335, −0,104) — dominada
pela variante de estresse iid_v3; um b̂ ali NÃO decide, por desenho, e será
reportado como INCONCLUSIVE/PARTIAL. Isto É um veredito trinário genuíno
com poder >95% sob ambas as hipóteses canônicas; a limitação honesta é a
zona de estresse acima.

**Checagens de sanidade mecânicas (não alteram a regra):**
S1 — nas alturas 10⁵, 10⁷, 10⁹, |mean(M*) − mean_triagem| < 4·√(EP²+EP_triagem²)
(seeds distintos; consistência de pipeline). S2 — sd empírico por altura ∈
[0,3, 0,9]. Se S1 ou S2 falhar: veredito RETIDO (`INVALID_RUN`), causa
investigada e documentada, rerun com o MESMO desenho travado. χ² da WLS
(5 g.l.) reportado como descritor de forma; não entra na regra.

**Descritor secundário (não decide nada):** z de b̂ contra os coeficientes
assintóticos −3/4 e −1/4, para continuidade com a triagem.

## 7. Holdout SELADO (declarado, NÃO computado na análise primária)

- T_holdout = 10¹¹ (regime de `zeros3` de Odlyzko), M = 600, grade 512,
  inícios `sort(default_rng(20260823).uniform(10¹¹, 2×10¹¹, 600))`.
- Custo projetado ~15,4 s/intervalo ⇒ ~2,6 h — reservado para o Gate de
  Replicação, FORA do orçamento desta análise.
- Uso no gate: agente independente computa o ponto 10¹¹ com o desenho
  acima, reestima a WLS com 8 alturas e reaplica a MESMA regra da Seção 6
  (com as curvas calibradas estendidas a 10¹¹ pelo MESMO procedimento das
  validações, incluindo CUE em N=23–25). Nenhum processo desta sessão
  toca t > 2,1×10¹⁰.
- Precedente: holdout selado de SPARC-003 (COSMOLOGY_WIDE_BINARIES).

## 8. Condições de parada e o que NÃO está sendo testado

- **Nenhuma alegação sobre RH** em nenhum desfecho — `stop_condition`
  permanente da linha `DISC-RH-REAL-001`. O teste discrimina dois modelos
  estatísticos para extremos de log|ζ| em altura finita; não prova nem
  aproxima RH, e não "confirma" a conjectura FHK completa (só o
  discriminante declarado, nas alturas declaradas).
- **Sem reformulação pós-hoc:** se o resultado sugerir estatística melhor,
  isso vira proposta para um NOVO pré-registro; este arquivo não é emendado
  além do adendo de resultado (Seção 10) e de no máximo um adendo datado
  pré-análise.
- **Qualquer veredito favorecendo um modelo (achado positivo) NÃO é
  reportado como real** até reprodução adversarial independente
  (implementação do zero a partir SOMENTE deste arquivo) — e o holdout 10¹¹
  permanece selado até esse gate. Flag para o orquestrador, sem abrir o
  holdout nesta sessão.
- Um `INCONCLUSIVE/NEITHER_MODEL` é catalogado com peso integral como
  resultado negativo informativo (nenhum dos dois modelos descreve os
  dados nas alturas acessíveis).
- Computação em primeiro plano, sem processos órfãos; orçamento da Seção 5.

## 9. Limitações declaradas (antes de ver o dado)

1. A triagem (exploratória, seed distinto) já produziu uma estimativa de
   inclinação (−0,408±0,184) compatível com a curva CUE calibrada; o
   desenho desta frente foi informado por ela (sd projetados, escolha de
   alturas). Mitigação: regra mecânica travada, amostras novas ~6,7× 
   maiores, gate adversarial obrigatório para veredito positivo.
2. Sobreposição esperada entre intervalos novos e os da triagem:
   ~75 pares em 10⁵ (3,8% dos M=2000), ~0,75 em 10⁷, ~0,008 em 10⁹ —
   influência estatística desprezível, declarada.
3. As curvas calibradas dependem dos dicionários declarados (Seção 4);
   a zona (−0,335, −0,104) é indecidível por desenho.
4. Correção de grade calibrada na banda [2T+10, 2,1T] e aplicada em
   [T, 2T] — variação do viés dentro da banda é de ordem inferior ao
   próprio EP(c_T) (densidade de zeros varia ~3% na banda).
5. CUE simulado em N ∈ [7,23]: regime pré-assintótico; é exatamente o que
   o dicionário FHK prevê para estas alturas, mas a extrapolação do
   dicionário em si é conjectural — o teste decide entre dicionários, não
   entre teoremas.

## 10. Arquivos e seeds (todos travados neste commit)

| Papel | Arquivo | Seed |
|---|---|---|
| Motor ζ (cópia atribuída) | `rs_zeta.py` | — |
| Piloto de tempo (descartável) | `phase0_timing.{py,json,log}` | 99991111 |
| Desenho + orçamento + poder | `design_power.py`, `DESIGN.json` | — |
| Validação (a) iid | `validate_iid_null.py`, `validation_iid_null.{json,log}` | 31415926 |
| Validação (b) CUE | `validate_cue.py`, `validation_cue.{json,log}`, `validation_cue_run1_FAILED.log` | 27182818 |
| Validação (c) grade | `validate_grid_bias.py`, `validation_grid_bias.{json,log}` | 77770707 |
| Análise primária | `run_primary.py`, `primary_slices/`, `primary_result.json`, `primary_run.log` | 20260822·100+k |
| Holdout (SELADO) | — (não computado) | 20260823 |

---

*Adendo pré-análise permitido: no máximo um, datado, acima desta linha de
resultado. Abaixo: preenchido somente após a análise primária.*

## [Preenchido depois da análise] Resultado

**Data da análise:** 2026-08-22 (mesma sessão do lock; nenhuma alteração de
regra, desenho, seeds ou curvas entre lock e análise). Todas as 15.600
janelas computadas na grade travada; custo real da computação sobre dado
real ≈ 8,2 ks (primária ~7,7 ks + calibração 395 s + piloto ~150 s) —
dentro do teto de 10,8 ks.

**Médias corrigidas por altura** (mean(M*)+c_T; sd; EP_total):
10⁴: 1,9223 (0,432; 0,0097) · 10⁵: 2,1271 (0,464; 0,0104) ·
10⁶: 2,2295 (0,485; 0,0109) · 10⁷: 2,3548 (0,494; 0,0111) ·
10⁸: 2,4752 (0,526; 0,0122) · 10⁹: 2,5633 (0,529; 0,0132) ·
10¹⁰: 2,6638 (0,524; 0,0167).

**Estatística primária:** `b̂ = −0,5622 ± 0,0384` (WLS, χ²(5 g.l.) = 10,11,
p≈0,07 — tensão de forma leve, descritor apenas).

**z contra as curvas travadas (Seção 4):** iid_v1: −14,83; iid_v2: −18,16;
iid_v3: −8,82; cue_v1: −3,62; cue_v2: +3,05.

**VEREDITO (regra trinária travada da Seção 6): `INCONCLUSIVE`, subcaso
`NEITHER_MODEL`** — ambas as curvas canônicas rejeitadas a ≥3σ
(|z_cue_v1| = 3,62 ≥ 3 impede FHK_FAVORED; |z_iid_v1| = 14,83 ≥ 3 impede
IID_FAVORED). Registrado com peso integral como negativo informativo,
exatamente como pré-declarado.

**Leitura honesta dentro da estrutura pré-declarada:** (i) o lado iid/REM
é excluído a ≥8,8σ em TODAS as três variantes declaradas — o dado real é
incompatível com o modelo de máximos independentes em qualquer
discretização declarada; (ii) o dado NÃO confirma o dicionário CUE
canônico: b̂ cai ENTRE as duas variantes CUE (−0,416 e −0,687), a 3,6σ da
canônica — inclinação mais íngreme que a curva CUE de tamanho casado;
(iii) descritor secundário assintótico: z vs −3/4: +4,89; z vs −1/4:
−8,13 — mesmo padrão. Nenhuma dessas leituras vira alegação até o gate
adversarial (Seção 8).

**Sanidade:** S1 PASS nas 3 alturas de cruzamento com a triagem (máx
|Δ| = 0,039 < tol 4σ ≈ 0,11–0,14); S2 PASS (sd ∈ [0,432, 0,529]) —
`sanity_checks.{py,json}` (nota de processo registrada lá: S1/S2
executadas por script separado imediatamente após `analyze`, implementando
a Seção 6 verbatim). Run `VALID`; veredito mantido.

**Holdout 10¹¹: SELADO** — nenhum t > 2,1×10¹⁰ foi avaliado por esta
frente. Permanece reservado ao Gate de Replicação.

**Flag adversarial: SIM** — o veredito formal é inconclusivo e não abre o
holdout, mas contém um componente de exclusão forte (iid ≥8,8σ) que, pela
condição de parada da Seção 8 (qualquer achado tipo p<0,05 exige
reprodução adversarial antes de ser reportado como real), fica retido como
CANDIDATO até reprodução adversarial independente. Nenhuma alegação sobre
RH em nenhuma hipótese.

Resultado completo: `primary_result.json`; log: `primary_run.log`;
sumário em `RESULTS_SUMMARY.md`.
