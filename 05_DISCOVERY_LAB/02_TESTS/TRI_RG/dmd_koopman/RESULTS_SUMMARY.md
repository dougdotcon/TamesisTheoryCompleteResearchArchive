# Resultado do fechamento dos gaps — `dmd_koopman` (Decomposição em Modos Dinâmicos / espectro de Koopman)

**Data:** 2026-08-20. Metodologia fixada em `METHODOLOGY_NOTE.md` (canal
primário revisado a priori — frequência/razão de amortecimento do par de
autovalores complexos conjugados menos amortecido, canal do autovalor real
demovido a diagnóstico-only desde o início) e pipeline
(`analysis/dmd_common.py`: embedding de Hankel + truncamento de posto
ótimo de Gavish & Donoho 2014 + DMD exato de Tu et al. 2014, substitutos
IAAFT como teste PRIMÁRIO de significância) validada contra dado
sintético ANTES de qualquer dado real (controle positivo de
Stuart-Landau ajustável, ver `VALIDATION_NOTE.md`). Aplicada, sem
modificação, aos 2 domínios declarados: Itália COVID-19 (lockdown de
09/03/2020) e Kīlauea 2018 (abertura de fissura de 03/05).

**Veredito honesto: `dmd_koopman` NÃO produz um invariante cross-domain
sobrevivente.** Itália COVID-19 é `NOT_COMPUTABLE` sob a regra travada
(série curta demais); Kīlauea não mostra significância no canal PRIMÁRIO
em nenhuma variante, e o único achado `p<0,05` (canal companheiro
`spectral_gap`) não sobrevive a NENHUMA das 4 checagens adversariais
rodadas.

## Recapitulação honesta da validação (ver `VALIDATION_NOTE.md`)

A validação sintética obrigatória (oscilador de Stuart-Landau,
`mu_pre=-0,3` foco estável, `mu_post=+0,3` ciclo-limite) PASSOU — mas com
uma ressalva já nomeada honestamente antes de tocar dado real: **apenas
o canal `zeta` (razão de amortecimento) mostrou poder discriminativo real
(`p=0,03` após o único ajuste pré-autorizado, `sigma:0,05→0,15`)**;
`f_dom` chegou perto mas não cruzou o limiar (`p=0,08`); o canal
companheiro `spectral_gap` NUNCA mostrou poder em nenhum dos 4 controles
sintéticos (`p` entre `0,07` e `0,835`, incluindo um valor preocupante de
`0,07` no controle NEGATIVO v1 — sinal de alerta de risco de
falso-positivo já visível antes de qualquer dado real). Isto é relevante
para interpretar o resultado de Kīlauea abaixo.

## Domínio 1 — Itália, primeira onda de COVID-19 (lockdown de 09/03/2020)

**`NOT_COMPUTABLE` nas 4 combinações (primária/robustez × canal), no
primeiro passo da pipeline (`tau`), antes de qualquer cálculo de `d`,
posto ou DMD.** Como já nomeado a priori em `METHODOLOGY_NOTE.md` §5.1
("MUITO curto para os pisos desta pipeline"): a incidência diária de
casos produz `n=38` (PRE primária) e `n=13` (POST primária) amostras —
`lag_max=min(200,floor(N/10))` cai para `3` e `1` respectivamente,
insuficiente para a informação mútua (Fraser & Swinney 1986) encontrar um
mínimo local OU para o fallback de cruzamento-por-zero da autocorrelação
resolver. Ver `data/PROVENANCE_COVID_ITALY.md` para os valores exatos e
a análise completa deste achado. **Nenhuma tentativa de afrouxar
`lag_max`/`D_MIN`/`HANKEL_D_DIVISOR` post-hoc foi feita** — as regras
foram travadas em `METHODOLOGY_NOTE.md` antes de qualquer preparação de
dado real.

| Variante | `n_pre` | `n_post` | Status |
|---|---|---|---|
| Primária | 38 | 13 | `tau_not_resolved` |
| Robustez | 19 | 6 | `tau_not_resolved` |

## Domínio 2 — Kīlauea 2018, abertura de fissura de 03/05, estação `HV.BYL..HHZ`

| Variante | Canal | PRE | POST | Δ | `p` (IAAFT) |
|---|---|---|---|---|---|
| Primária | `f_dom` (PRIMÁRIO) | 0,001387 | 0,393955 | +0,392568 | 0,765 |
| Primária | `zeta` (PRIMÁRIO) | 0,483664 | 0,508169 | +0,024505 | 1,0 |
| Primária | `spectral_gap` (companheiro) | 0,004790 | 0,494693 | **+0,489903** | **0,0** |
| Robustez | `f_dom` (PRIMÁRIO) | 0,000853 | 0,001729 | +0,000875 | 0,455 |
| Robustez | `zeta` (PRIMÁRIO) | 0,999426 | 0,988588 | −0,010838 | 0,345 |
| Robustez | `spectral_gap` (companheiro) | 0,006206 | 0,028971 | **+0,022765** | **0,0** |

**O canal PRIMÁRIO desta candidatura (`f_dom`, `zeta` — o único
validado com poder discriminativo real na etapa sintética) NÃO mostra
significância em NENHUMA das duas variantes.** O único achado `p<0,05`
é o canal COMPANHEIRO (`spectral_gap`), que nunca teve poder validado
sinteticamente (ver recapitulação acima) — um sinal de alerta desde o
início, não uma surpresa.

### Checagem de confundidor/reprodução adversarial (acionada pelo `p<0,05` do `spectral_gap`)

Ver `analysis/CONFOUND_CHECK_KILAUEA.md` in extenso. Resumo honesto: **4
checagens rodadas, o achado NÃO sobrevive a NENHUMA delas.**

| Checagem | Resultado | Veredito |
|---|---|---|
| (a) Placebo — divisão arbitrária dentro do PRE, sem transição real | `p=0,02` (spectral_gap) — significativo MESMO sem transição real; o canal PRIMÁRIO `zeta` também deu `p=0,02` aqui, apesar de não significativo na transição real | Risco de falso-positivo genérico do domínio/pipeline confirmado |
| (b) Exclusão do terremoto M6,9 (POST primária truncado 6h antes do mainshock) | `p: 0,0→0,08`; magnitude cai ~73x (Δ: 0,490→0,0067) | Efeito extremo da primária depende diretamente do M6,9, não de dinâmica precursora |
| (c) Bootstrap (Kunsch 1989), primária | `p=0,615`, delta bootstrap ~640x menor que o real | Contradiz o IAAFT — não significativo |
| (c) Bootstrap (Kunsch 1989), robustez | `p=1,0`, delta bootstrap com SINAL INVERTIDO ao real | Contradiz o IAAFT — não significativo, direção nem reproduzida |

**Conclusão adversarial:** o `p=0,0` de `spectral_gap` em Kīlauea é um
artefato — primariamente o terremoto M6,9 de flanco sul dominando
trivialmente a decomposição espectral/modal de qualquer janela que o
contenha (checagem b), agravado por uma sensibilidade genérica do
canal/domínio a divisões arbitrárias de tremor sísmico longo e
não-estacionário (checagem a), e contradito de forma direta pelo método
de significância alternativo pré-autorizado em AMBAS as variantes
(checagem c). **Não é uma assinatura genuína de bifurcação oscilatória
relacionada à erupção** — a hipótese original deste candidato.

## Veredito honesto — não produz um invariante cross-domain sobrevivente

**`dmd_koopman`, como formulado e testado aqui, NÃO produz um invariante
cross-domain sobrevivente.** Um domínio é inteiramente `NOT_COMPUTABLE`
(Itália COVID-19, comprimento de série insuficiente para a pipeline
travada). No segundo domínio (Kīlauea), o canal PRIMÁRIO — o único
formalmente validado com poder discriminativo real na etapa sintética —
não mostra sinal em nenhuma variante; o único `p<0,05` observado (canal
companheiro, nunca validado) foi investigado a fundo por reprodução
adversarial e refutado por 4 checagens independentes e concordantes.
Nenhuma alegação de "achado cross-domain" ou mesmo de "achado
intra-domínio real" é feita aqui — diferente de `lempel_ziv_complexity`
(cujo achado de Daphnet sobreviveu a 3 checagens antes de falhar em
generalização entre sujeitos), o achado de Kīlauea falha já na checagem
de confundidor mais óbvia e específica do domínio, um padrão de
refutação mais decisivo e mais rápido.

Isto não invalida DMD/decomposição de Koopman como ferramenta
estabelecida na literatura de sistemas dinâmicos/engenharia — mostra
apenas que, sob a convenção de embedding e o par de canais travados a
priori especificamente para esta linha (frequência/amortecimento do modo
complexo menos amortecido como alvo de bifurcação oscilatória tipo
Hopf), nenhum invariante cross-domain robusto emergiu nos 2 domínios
testados, e o único sinal estatístico observado tem uma explicação
mundana concreta e bem identificada (o terremoto M6,9), não uma origem
dinâmica ligada à hipótese original.

## Arquivos desta etapa

- `METHODOLOGY_NOTE.md` — metodologia travada ANTES de qualquer cálculo,
  incluindo a demoção a priori do autovalor real (redundância com
  `critical_slowing_down`) e o desenho de validação de Stuart-Landau.
- `analysis/dmd_common.py` — pipeline canônica (embedding de Hankel,
  truncamento de Gavish-Donoho, DMD exato, seleção do par complexo
  primário, gap espectral companheiro, diagnóstico de autovalor real
  demovido, IAAFT + bootstrap fallback).
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`
  — validação sintética completa (diagnóstico de senoide, controles
  positivo/negativo de Stuart-Landau v1/v2).
- `VALIDATION_NOTE.md` — nota de validação completa e honesta.
- `analysis/run_real_domain.py` — executor por domínio/variante, chamando
  `run_dmd_analysis` sem modificação.
- `data/prepare_covid_italy.py`, `data/prepare_kilauea.py` — download +
  preparação, re-executáveis.
- `data/PROVENANCE_COVID_ITALY.md`, `data/PROVENANCE_KILAUEA.md` —
  proveniência completa.
- `data/covid_italy_{pre,post}_{primary,robust}.npy`,
  `data/covid_italy_segments_meta.json` — segmentos pequenos.
- `data/kilauea_{pre,post}_{primary,robust}.npy`,
  `data/kilauea_segments_meta.json` — segmentos grandes (~150MB
  combinados, resolução nativa 100Hz não pré-decimada); **NÃO commitados**
  por instrução explícita desta etapa.
- `analysis/result_covid_italy_primary.json`,
  `analysis/result_covid_italy_robust.json`,
  `analysis/result_kilauea_primary.json`,
  `analysis/result_kilauea_robust.json` — resultados completos.
- `analysis/confound_check_kilauea.py`,
  `analysis/confound_check_kilauea_results.json`,
  `analysis/CONFOUND_CHECK_KILAUEA.md` — reprodução adversarial completa
  (4 checagens), acionada pelo `p<0,05` do canal companheiro em Kīlauea.

## Estado da linha — 14 de 14 candidatos identificados agora com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| `mse-multiscale-entropy` | Geomagnetismo (1989), rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |
| `grafo-de-visibilidade` | Geomagnetismo (2015), hidrologia/Harvey | NEGATIVO (sem achado; `d_B` estruturalmente não testável) |
| `permutation_entropy` | (ver linha própria) | NEGATIVO |
| `persistent_homology` | (ver linha própria) | FECHADO NA VALIDAÇÃO |
| `evt_hill` | (ver linha própria) | NEGATIVO |
| `kramers_moyal` | (ver linha própria) | NEGATIVO (com rebaixamento de canal) |
| `RQA` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |
| `lempel-ziv-complexity` | Daphnet FOG, Kilauea 2018 LERZ | NEGATIVO cross-domain (achado intra-domínio de 1 sujeito refutado por reexecução adversarial) |
| `largest_lyapunov_exponent` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |
| `dmd_koopman` | Itália COVID-19, Kilauea 2018 (03/05) | **NEGATIVO cross-domain (1 domínio NOT_COMPUTABLE; achado do outro refutado por 4 checagens adversariais)** |

## Estado da linha e próximo passo (para a sessão orquestradora)

`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` e `DECISION_LEDGER.yaml` NÃO
foram modificados por este agente (fora do escopo desta tarefa) — ficam a
cargo da sessão orquestradora.

**Este fechamento encerra INTEIRAMENTE a Fase 0.7** (sondagem de
2026-08-20, `phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md`): os 3 candidatos
`viable=true` identificados naquela rodada (`lempel_ziv_complexity`,
`largest_lyapunov_exponent`, `dmd_koopman`) agora têm resultado completo
— nenhum produziu um invariante cross-domain sobrevivente. Nenhum
candidato novo permanece pendente de nenhuma sondagem anterior desta
linha. `DISC-TRI-RG-001` chega a 14 candidatos testados no total (3 da
Fase 0 original + 4 da Fase 0.5 + 4 da Fase 0.6 + 3 da Fase 0.7), TODOS
NEGATIVOS ou fechados na etapa de validação — nenhum produziu um
invariante cross-domain sobrevivente até agora. Decisão sobre pausar
novamente a linha, buscar mais uma rodada de candidatos genuinamente
novos, ou encerrar `DISC-TRI-RG-001` formalmente fica com o usuário e/ou
a sessão orquestradora, mesmo padrão já seguido em todas as pausas
anteriores desta linha (`DISC-DEC-005`/`006`/`007`/`008`).
