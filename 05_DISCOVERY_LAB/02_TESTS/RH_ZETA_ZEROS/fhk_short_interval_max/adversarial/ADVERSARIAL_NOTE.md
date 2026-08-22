# ADVERSARIAL_NOTE — reprodução adversarial de DISC-RH-FHK-SHORT-INTERVAL-MAX-001

**Agente:** reprodutor adversarial independente (sessão separada da primária).
**Data:** 2026-08-22.
**Status deste arquivo:** escrito ANTES de qualquer computação real de ζ nos
offsets do teste (plano + seeds + política de subset pré-declarados aqui).

## O que foi lido antes de travar meus números

- `PREREGISTRATION.md` (spec travada) e `DESIGN.json` — SOMENTE estes.
- NÃO lidos até o lock dos meus números: `run_primary.py`, `rs_zeta.py`,
  `primary_result.json`, `primary_slices/`, `RESULTS_SUMMARY.md`,
  `sanity_checks.*`, `validation_*.{json,log}`, `primary_run.log`,
  `phase0_timing.*`, `design_power.py`, `validate_*.py`.

**Declaração de contaminação inevitável:** o adendo de resultado da análise
primária está DENTRO de `PREREGISTRATION.md` (Seção "[Preenchido depois da
análise]"), que fui instruído a ler como spec. Portanto conheço o alvo
(b̂ = −0,5622 ± 0,0384, médias por altura, z's) antes de computar. Mitigação
de honestidade: (i) minha implementação é escrita do zero, sem ler nenhum
código da primária; (ii) o pipeline é determinístico dado o spec — não há
botão contínuo para "sintonizar" o resultado sem fraude explícita; (iii)
qualquer depuração pós-primeiro-resultado que use o conhecimento do alvo
será declarada explicitamente no VERDICT, com o valor pré-depuração
preservado nos logs.

## Implementação própria (do zero)

1. **Avaliador Z(t):** fórmula de Riemann–Siegel vetorizada em numpy:
   `Z(t) = 2·Σ_{n≤N} n^{−1/2}·cos(θ(t) − t·ln n) + (−1)^{N−1}·(t/2π)^{−1/4}·C0(p)`,
   com `N = floor(√(t/2π))`, `p = √(t/2π) − N`,
   `C0(p) = Ψ(p) = cos(2π(p² − p − 1/16))/cos(2πp)` (singularidades
   removíveis em p = 1/4, 3/4 tratadas por série de Taylor local derivada
   simbolicamente via sympy, coeficientes registrados no script).
   `θ(t) = Im log Γ(1/4 + it/2) − (t/2)·ln π` exato via `scipy.special.loggamma`.
   Erro do termo C0-apenas (cota de Gabcke): ≤ 0,053·(t/2π)^{−3/4} ≤ 2,2×10⁻⁴
   em t = 10⁴, menor acima — abaixo da tolerância 5×10⁻⁴ que a spec declara
   para o motor da primária, e desprezível para máximos O(1)–O(3) de log|Z|.
2. **Validação ANTES de qualquer janela real** (registrada em
   `validation_adv.{json,log}`):
   - |ζ(1/2)| via mpmath (âncora documental) e |Z(t)| vs |ζ(1/2+it)| do
     mpmath em t moderados;
   - primeiro zero: raiz de Z perto de t = 14,134725… por bisseção no meu Z;
   - cruzamentos vs `mpmath.siegelz` (dps 30) em pontos pseudo-aleatórios
     (seed de validação 424242, NÃO relacionado aos seeds do teste) nas
     faixas t ∈ {2×10³, 10⁴, 10⁵, 10⁶, 10⁷, 10⁸, 10⁹, 10¹⁰, 2,05×10¹⁰},
     alguns pontos por faixa; tolerâncias de aceite por faixa declaradas no
     script antes de rodar: |ΔZ| ≤ 5×10⁻⁴ para t ≤ 10⁶; ≤ 1×10⁻³ para
     t ≥ 10⁷ (fase em dupla precisão ~10⁻⁵ rad em t = 10¹⁰). Se falhar:
     conserto o avaliador ANTES de tocar as janelas reais e preservo o log
     da falha.
3. **Offsets do teste (reprodução exata do spec):** por altura k = 0..6,
   `starts = numpy.sort(numpy.random.default_rng(20260822*100 + k).uniform(T, 2T, M_T))`,
   M = {2000, 2000, 2000, 2000, 2000, 1600, 1000}, T = 10⁴…10¹⁰.
4. **Grade:** 512 pontos, passo 2π/512, `t_j = t0 + j·2π/512`, j = 0..511
   (meio-aberto [t0, t0+2π), como na definição de M*). AMBIGUIDADE anotada:
   o spec diz "512 pontos igualmente espaçados por intervalo (passo
   2π/512)"; 512 pontos MAIS passo 2π/512 força a leitura meio-aberta
   (fechada daria passo 2π/511). Leitura adotada: meio-aberta.
5. **Estatística:** M*(t0) = max_j log|Z(t_j)| (log natural).
6. **Correção de grade c_T (recomputada por mim, do zero):** banda
   descartável [2T+10, 2,1T], n_cal = {80, 80, 60, 60, 24, 16, 8} conforme
   `DESIGN.json`; Richardson 512→2048:
   `c_T = (16/15)·mean(M*_2048 − M*_512)`, `EP(c_T) = (16/15)·sd(Δ)/√n_cal`.
   AMBIGUIDADES anotadas: (a) a lei exata dos offsets de calibração não
   está escrita no spec (só o seed 77770707 e a banda); adoto, por analogia
   com a lei primária, `sort(default_rng(77770707*100 + k).uniform(lo, hi, n_cal))`;
   (b) em k = 6 limito hi = 2,1T − 2π para garantir nenhum t > 2,1×10¹⁰
   (holdout selado intocado). Impacto de ambas as escolhas é de segunda
   ordem: |c_T| < 0,005 e EP(c_T) ≤ ~0,003 pela própria spec — não pode
   mover b̂ além de ~0,003, irrelevante contra separações de ~0,4.
7. **Regressão:** `y_T = mean(M*) + c_T − lnln T` sobre `x_T = lnlnln T`
   (logs naturais), WLS com intercepto livre, pesos `w_T = 1/EP_T²`,
   `EP_T² = sd_T²/M_T + EP(c_T)²` (sd empírico, ddof=1).
   `EP(b̂) = √[(XᵀWX)⁻¹]_bb` SEM reescala por χ² (pesos são variâncias
   inversas medidas; o spec reporta χ² como descritor apenas). AMBIGUIDADE
   anotada: o spec não diz explicitamente se o EP da WLS é reescalado por
   χ²/gl; a leitura não-reescalada é a que o texto suporta (χ² "não entra
   na regra") e é a que reproduz EP projetado 0,0369 do DESIGN.json.
8. **z e regra trinária:** exatamente a Seção 6, com as 5 curvas travadas
   da Seção 4: p_iid_v1 = +0,0072 (EP 0), p_iid_v2 = +0,1352 (EP 0),
   p_iid_v3 = −0,2235 (EP 0), p_cue_v1 = −0,4160 (EP 0,0125),
   p_cue_v2 = −0,6871 (EP 0,0141);
   `z_m = (b̂ − p_m)/√(EP(b̂)² + EP(p_m)²)`.
   Descritor secundário: z vs −3/4 e vs −1/4 usando só EP(b̂).
9. **Sanidade:** S2 (sd por altura ∈ [0,3, 0,9]) aplicada. S1 (cruzamento
   com a triagem) N/A para esta reprodução — substituída, com mais força,
   pela comparação célula a célula contra a primária APÓS o lock dos meus
   números.

## Orçamento e política de SUBSET (pré-declarada)

Teto ~2,5 h de computação total. Sequência: (1) validação do avaliador;
(2) benchmark de tempo por intervalo em cada altura (nas primeiras janelas
da enumeração, cujos M* são então guardados e reutilizados — nada é
recomputado com outra grade); (3) projeção de custo total.

- Se custo projetado ≤ 7000 s: **M completo** (15.600 janelas).
- Caso contrário: subset determinístico pré-declarado = **primeiras m_k
  janelas NA ORDEM DE SORTEIO do gerador (ordem pré-sort)** — nunca
  re-randomização. Justificativa da ordem pré-sort: as primeiras m da
  ordem pós-sort concentrariam os offsets no fundo da banda [T, 2T]
  (viés de altura dentro da banda); as primeiras m da ordem de sorteio são
  uma subamostra iid legítima da mesma lei. Os m_k seriam escolhidos
  proporcionalmente ao custo por altura para caber em 7000 s, e o poder
  recomputado com EP_T² = sd_T²/m_k. A escolha efetiva (M completo ou
  m_k) será registrada AQUI por adendo datado antes da computação principal.

### Adendo datado (2026-08-22, pós-benchmark, PRÉ-computação principal)

Validação do avaliador: **ALL_PASS** (`validation_adv.{json,log}`); desvio
máximo vs `mpmath.siegelz` = 2,4×10⁻⁴ (banda t≈2×10³), ~10⁻⁵–10⁻⁷ nas
bandas do teste. Benchmark (`bench.log`, 190 janelas já computadas e
GUARDADAS nos checkpoints): 0,0009 s/janela (10⁴) … 2,31 s/janela (10¹⁰).
Custo projetado M completo ≈ 3430 s + calibração ≈ 130 s ≈ 1 h < teto.
**Decisão: M COMPLETO (15.600 janelas), sem subset.** Poder = o do desenho
travado (separação canônica 0,423, ~10,9σ projetado).

## Ordem de execução

1. `sympy_psi_coeffs.py` (derivação simbólica dos coeficientes de Taylor) →
   colados em `rs_zeta_adv.py`.
2. `validate_adv.py` → `validation_adv.{json,log}` (gate: só prossigo se PASS).
3. Benchmark + adendo de subset abaixo.
4. `compute_adv.py` em fatias com checkpoint (`slices_adv/height_k.npz`),
   primeiro plano, sem processos órfãos; depois calibração c_T
   (`calibration_adv.json`).
5. `analyze_adv.py` → `adversarial_result.json` (b̂, EPs, z's, veredito
   trinário) — **LOCK dos meus números**.
6. Só então: leitura de `primary_result.json`, `RESULTS_SUMMARY.md`,
   `run_primary.py`, `primary_slices/`, logs; comparação célula a célula;
   investigação de discrepâncias; `ADVERSARIAL_VERDICT.md` (PT).

Nenhum t > 2,1×10¹⁰ será avaliado. Nenhuma alegação sobre RH em nenhum
desfecho. Sem commit/push/edições de governança.

## Adendo pós-lock (2026-08-22, após ler os arquivos da primária)

Números travados ANTES desta leitura: `adversarial_result.json`
(b̂ = −0,5635 ± 0,0385; z_iid_v1..v3 = −14,83/−18,15/−8,83;
z_cue_v1/v2 = −3,65/+3,01; veredito INCONCLUSIVE/NEITHER_MODEL). M
completo (15.600 janelas), sem redução — a decisão de subset registrada
acima (M completo, ~1h de compute real, sessão interrompida uma vez por
limite temporário de API e retomada exatamente do checkpoint, sem
recomputação nem duplicação — verificado via NaN-guard nos checkpoints
antes de retomar) foi cumprida integralmente.

Comparação célula a célula contra `primary_result.json` /
`RESULTS_SUMMARY.md` / `rs_zeta.py` (lidos SÓ agora): ver
`ADVERSARIAL_VERDICT.md` Seção 2. Resumo: concordância das médias/sd
brutas por altura a 10⁻⁸–10⁻¹³ relativo (dois motores ζ numericamente
independentes — o meu via `loggamma` exata + float64, o da primária via
Stirling + `np.longdouble`); b̂ difere por apenas −0,03 SE; todos os z's
concordam a ±0,04; veredito idêntico. Única discrepância acima do ruído
de ponto flutuante: c_T (correção de viés de grade) difere por até
0,0047 entre as duas calibrações — CAUSA: a lei exata dos offsets da
banda de calibração descartável não está escrita no pré-registro (só
banda + seed), então minha lei (declarada acima, por analogia) é
necessariamente diferente da da primária. Efeito confirmado de segunda
ordem, não move nenhum z de sinal nem o veredito — exatamente como
projetado ANTES de ver o dado.

Contaminação declarada: o adendo de resultado da primária está dentro de
`PREREGISTRATION.md`, que li como spec antes de computar — logo eu já
sabia o valor-alvo de b̂ antes de rodar meu pipeline. Ver discussão de
honestidade em `ADVERSARIAL_VERDICT.md`, seção final.
