# DISC-RH-FHK-SHORT-INTERVAL-MAX-001 — Sumário de resultados

**Frente:** onda 2 (b) de `DISC-DEC-014`, sob a linha `DISC-RH-REAL-001`.
**Datas:** desenho/validações/lock 2026-08-21; análise primária 2026-08-22.
**Status do teste:** pré-registrado (`PREREGISTRATION.md`, LOCKED antes de
qualquer ζ nos offsets de teste), executado por completo, run `VALID`.
**Nenhuma alegação sobre RH** — `stop_condition` permanente da linha.

## Pergunta

O termo subdominante do máximo de log|ζ(1/2+it)| em intervalos de
comprimento 2π cresce como prevê o modelo de campo log-correlacionado
(FHK, −(3/4)·logloglogT; arXiv:1202.4713, ordem líder provada em
arXiv:1612.08575) ou como prevê o modelo concorrente nomeado de máximos
independentes (iid/REM, −(1/4)·logloglogT)? Em altura finita, o teste
compara CURVAS CALIBRADAS dos dois modelos (validações sintéticas
pré-lock), não os coeficientes assintóticos crus.

## Desenho travado (e por quê)

- 7 alturas primárias 10⁴…10¹⁰; M = 2000/2000/2000/2000/2000/1600/1000
  (15.600 janelas, ~6,7× a triagem); grade 512 pts/janela; offsets
  determinísticos U[T,2T] (seeds 20260822·100+k), disjuntos das bandas
  descartáveis do piloto e da calibração ([2T+10, 2,1T]).
- O desenho de ~8σ sugerido pela triagem (M=2000 com 10¹¹) NÃO cabia no
  teto de ~3 h: 10¹¹ foi trocada por mais alturas baixas + M maiores, com
  poder projetado MAIOR (10,9σ entre as curvas canônicas; poder ≈98–99%
  sob cada hipótese canônica), e 10¹¹ virou o holdout selado (M=600,
  seed 20260823) do Gate de Replicação.
- Custo real total sobre dado real ≈ 8,2 ks < teto 10,8 ks.

## Validações pré-lock (todas PASSARAM; logs preservados)

1. **iid/REM sintético** — estimador recupera o −1/4 assintótico
  (−0,229 em L=10⁷, monótono), viés ~0, cobertura 96,3% ∈ [91,7%, 98,3%].
2. **CUE (lado FHK)** — Haar-U(N) via QR-Ginibre (Mezzadri
  math-ph/0609050, verificado por fetch); em N grandes {64,128,256} a
  inclinação é −0,853 (assinatura FHK, aceite < −0,5). Rodada 1 falhou na
  serialização JSON após toda a computação (determinística) — preservada em
  `validation_cue_run1_FAILED.log`, rodada 2 reproduziu números idênticos.
3. **Viés de grade** — correções Richardson 512→2048 por altura
  c_T ∈ [+0,0002, +0,0049], gradiente sobre a inclinação −0,003
  (desprezível); calibrado em banda descartável, registrando SÓ diferenças.

Curvas calibradas travadas (inclinações efetivas no desenho):
iid_v1 **+0,007** · iid_v2 +0,135 · iid_v3 −0,224 ·
cue_v1 **−0,416±0,013** · cue_v2 −0,687±0,014.
Achado metodológico das validações: em T ≤ 10¹⁰ as inclinações efetivas de
ALTURA FINITA de ambos os modelos ficam longe dos assintóticos −1/4 e
−3/4 — comparar o dado cru contra −1/4 vs −3/4 seria mal-especificado; por
isso a regra travada usa as curvas calibradas.

## Resultado primário (regra travada)

| Quantidade | Valor |
|---|---|
| Inclinação medida b̂ (WLS) | **−0,5622 ± 0,0384** |
| χ²(5 g.l.) | 10,11 (descritor; p≈0,07) |
| z vs iid_v1 / v2 / v3 | −14,8 / −18,2 / **−8,8** |
| z vs cue_v1 / v2 | **−3,62** / +3,05 |
| z vs assintóticos −3/4 / −1/4 | +4,89 / −8,13 |
| Sanidade S1 (cruzamento triagem) / S2 (sd) | PASS / PASS |

**VEREDITO (trinário, travado): `INCONCLUSIVE` — subcaso `NEITHER_MODEL`.**
Ambas as curvas canônicas são rejeitadas a ≥3σ, então nem FHK_FAVORED nem
IID_FAVORED disparam. Registrado com peso integral, sem suavização.

O que o resultado diz dentro da estrutura pré-declarada (e nada além):

- **Exclusão forte do lado iid/REM:** ≥8,8σ contra TODAS as três variantes
  declaradas do modelo de máximos independentes. Este é o componente
  "tipo p<0,05" do resultado — pela condição de parada, fica **retido como
  candidato** até reprodução adversarial.
- **Não-confirmação do dicionário CUE canônico:** o dado é MAIS íngreme
  (−0,562) que a curva CUE de tamanho casado (−0,416, rejeitada a 3,6σ) e
  cai entre as duas variantes CUE declaradas. Qualitativamente do lado
  log-correlacionado; quantitativamente nenhum dicionário declarado
  descreve o dado — um negativo informativo genuíno sobre os dicionários
  de altura finita, não sobre a conjectura assintótica em si.
- **Nada sobre RH.**

## Próximos passos (decisão do orquestrador, fora desta frente)

1. **Reprodução adversarial** (obrigatória antes de qualquer reporte do
   componente de exclusão): reimplementação do zero a partir SOMENTE de
   `PREREGISTRATION.md`.
2. **Holdout 10¹¹ SELADO** (intocado; nenhum t > 2,1×10¹⁰ avaliado) —
   abrir apenas no Gate de Replicação, conforme Seção 7 do pré-registro.
3. Se o gate confirmar: a pergunta aberta legítima passa a ser "que curva
   de altura finita descreve o máximo curto de ζ?" — qualquer novo
   dicionário exige NOVO pré-registro (sem reformulação pós-hoc desta).

## Arquivos

`PREREGISTRATION.md` (LOCKED + resultado), `DESIGN.json`,
`phase0_timing.{py,json,log}`, `design_power.py`,
`validate_iid_null.py` + `validation_iid_null.{json,log}`,
`validate_cue.py` + `validation_cue.{json,log}` +
`validation_cue_run1_FAILED.log`,
`validate_grid_bias.py` + `validation_grid_bias.{json,log}`,
`rs_zeta.py` (cópia atribuída do motor validado da triagem),
`run_primary.py`, `primary_slices/` (126 fatias .npy),
`primary_result.json`, `primary_run.log`, `sanity_checks.{py,json}`.
