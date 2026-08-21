# Resultado do fechamento dos gaps — `transfer_entropy` (Transferência de Entropia / fluxo de informação direcionado)

**Data:** 2026-08-21. Metodologia fixada em `METHODOLOGY_NOTE.md` (KSG-CMI
com embedding de Ragwitz-Kantz por canal, TE Simbólica como estimador de
robustez, sub-janelamento para não-estacionariedade, protocolo de nulo
substituto DUPLO — IAAFT primário + deslocamento circular companheiro)
validada contra dado sintético ANTES de qualquer dado real
(`VALIDATION_NOTE.md`, controle positivo AR(1) acoplado, `p=0,0` nos 4
canais sob os 2 nulos). Aplicada, sem modificação, aos 2 domínios
declarados: CHB-MIT EEG (`chb01_03.edf`, onset de convulsão) e par de
terremotos de Kahramanmaraş, Turquia (06/02/2023).

**Veredito honesto: `transfer_entropy` NÃO produz um invariante
cross-domain sobrevivente.** CHB-MIT não mostra significância robusta em
nenhuma variante/canal (um único `p<0,05` isolado, contradito pelo nulo
primário no mesmo canal/variante, e sem replicação em pares de eletrodo
alternativos). Terremotos da Turquia mostrou inicialmente achados
`p<0,05` no canal PRIMÁRIO (`TE_net`, `TE_sum`) sob os 2 nulos — mas a
reprodução adversarial revelou que o achado é explicado por um
ARTEFATO INSTRUMENTAL de baixa frequência específico da estação `GAZ`
na janela PRE (não um sinal sísmico real), e o achado companheiro
(`STE_sum`) dispara significância mesmo numa divisão placebo sem
transição nenhuma. Este é, estruturalmente, o mesmo padrão de refutação
já visto em `dmd_koopman`/Kīlauea — um mecanismo mundano concreto
explica o achado, não dinâmica genuína ligada à hipótese original —
mas com uma descoberta adicional relevante: o mecanismo mundano aqui
nem chega a ser um evento sísmico real, é um artefato de
instrumentação.

## Recapitulação honesta da validação (ver `VALIDATION_NOTE.md`)

A validação sintética obrigatória (diagnóstico de correção de código com
Gaussianas independentes e AR(1) acoplado de direção conhecida; controle
positivo com acoplamento ligado partindo PRE-desacoplado; controle
negativo com 3 sementes independentes) **PASSOU sem necessidade do passo
de correção pré-autorizado.** O controle positivo mostrou poder
discriminativo forte nos 4 canais (`TE_net`, `TE_sum`, `STE_net`,
`STE_sum`) sob AMBOS os nulos substitutos (`p=0,0` em todos), já na
especificação literal (`c=0,5`). O controle negativo mostrou taxa de
falso-positivo `2/24~8,3%`, compatível com o nível nominal `alpha=0,05`
esperado, sem padrão sistemático nos canais primários. Isto dá confiança
de que a pipeline TEM poder discriminativo genuíno quando há acoplamento
real — o que torna os resultados negativos/refutados abaixo mais
informativos (não um caso de "instrumento cego", mas de "instrumento que
funciona e não encontrou nada que sobrevivesse a escrutínio").

## Domínio 1 — CHB-MIT EEG, `chb01_03.edf`, canais `FP1-F7`/`T7-P7`, onset de convulsão

| Variante | Canal | `Delta` | `p` IAAFT | `p` deslocamento circular |
|---|---|---|---|---|
| Primária | `TE_net` (PRIMÁRIO) | +0,0197 | 0,255 | 0,295 |
| Primária | `TE_sum` (companheiro) | +0,0038 | 0,97 | 0,96 |
| Primária | `STE_net` (robustez) | +0,0156 | 0,61 | 0,47 |
| Primária | `STE_sum` (robustez) | +0,0448 | 0,425 | 0,18 |
| Robustez | `TE_net` (PRIMÁRIO) | +0,0307 | 0,07 | 0,15 |
| Robustez | `TE_sum` (companheiro) | +0,0086 | 0,815 | 0,86 |
| Robustez | `STE_net` (robustez) | +0,0611 | 0,225 | 0,13 |
| Robustez | `STE_sum` (robustez) | -0,1738 | 0,725 | **0,025** |

**Nenhuma significância no canal PRIMÁRIO (`TE_net`) em nenhuma
variante/nulo.** O único `p<0,05` observado (`STE_sum`, robustez,
SOMENTE sob deslocamento circular — o nulo IAAFT do MESMO
canal/variante dá `p=0,725`, sem qualquer tendência) foi investigado por
reprodução adversarial (`analysis/CONFOUND_CHECK_CHBMIT.md`): não
replica em NENHUM dos 2 pares de eletrodo alternativos testados
(próximo, compartilhando eletrodo, risco máximo de condução de volume;
distante/implausível), e é plenamente compatível com a taxa de
falso-positivo de base já observada na validação sintética (`~8%`).
**Veredito: sem achado real neste domínio.**

**Ressalva de condução de volume, carregada honestamente independente
do resultado (Nolte et al. 2008):** nomeada a priori em
`METHODOLOGY_NOTE.md`, parcialmente mitigada pela montagem bipolar e
pela construção estritamente defasada no tempo de TE — não totalmente
eliminada como possibilidade em princípio, mas sem evidência de que
tenha produzido o único achado isolado observado aqui (o par mais
suscetível a condução de volume não mostrou efeito maior que um par
arbitrário).

## Domínio 2 — Terremotos de Kahramanmaraş, Turquia, 06/02/2023, estações `KO.GAZ..HHZ`/`KO.BNN..HHZ`

| Variante | Canal | `Delta` | `p` IAAFT | `p` deslocamento circular |
|---|---|---|---|---|
| Primária | `TE_net` (PRIMÁRIO) | +0,0734 | **0,04** | 0,18 |
| Primária | `TE_sum` (companheiro) | -0,1022 | **0,005** | **0,0** |
| Primária | `STE_net` (robustez) | -0,3050 | 0,285 | 1,0 |
| Primária | `STE_sum` (robustez) | +1,8794 | **0,0** | 1,0 |
| Robustez | `TE_net` (PRIMÁRIO) | -0,0303 | 0,335 | 0,075 |
| Robustez | `TE_sum` (companheiro) | -0,0977 | 0,335 | 0,08 |
| Robustez | `STE_net` (robustez) | -0,1052 | 0,535 | 0,425 |
| Robustez | `STE_sum` (robustez) | -0,0623 | 0,885 | 0,6 |

**A variante primária mostrou achados `p<0,05` no canal PRIMÁRIO
(`TE_net`) e no companheiro (`TE_sum`, sob AMBOS os nulos) — a
combinação mais forte de evidência bruta observada nesta candidatura.**
A variante de robustez não replicou nada. Reprodução adversarial
obrigatória rodada (`analysis/CONFOUND_CHECK_TURKEY_EARTHQUAKE.md`, 4
checagens completas + 1 correção de rótulo documentada honestamente).

### Descoberta central da checagem adversarial

Ao inspecionar o dado real durante a checagem, foi descoberto que a
série de RMS de `PRE/X` (GAZ) tem uma anomalia de baixa frequência
grande (até `~270x` acima do nível de fundo) ocupando os primeiros
`~10,6h` das `24h` da janela PRE — `PRE/Y` (BNN) não mostra nada de
anormal no mesmo intervalo, descartando um evento sísmico regional real
compartilhado. Um filtro passa-alta padrão de 1Hz (checagem c) remove a
anomalia quase inteiramente, confirmando um transiente instrumental de
baixa frequência (não energia sísmica genuína) — coincidente em tempo
absoluto com lacunas de dado já documentadas na proveniência.

**Resultado decisivo:** com a mesma pipeline aplicada ao dado
CORRETAMENTE filtrado (passa-alta 1Hz antes do *binning* de RMS,
refeito do zero a partir do FDSN), `TE_net`/`TE_sum` — os ÚNICOS canais
com achado bruto `p<0,05` sob ambos os nulos — **deixam de ser
significativos** (`p` entre `0,305` e `0,61`). O achado de `STE_sum`
(o outro `p<0,05` bruto) é separadamente descartado: dispara
significância (`p=0,0`, IAAFT) mesmo numa divisão PLACEBO inteiramente
dentro do PRE, sem NENHUMA transição real — sinal claro de
sobre-sensibilidade do estimador simbólico à esparsidade combinatória
neste domínio de `N` pequeno (`24³=13.824` estados possíveis contra
`~100`-`700` pontos), exatamente o risco nomeado a priori em
`METHODOLOGY_NOTE.md`, agora confirmado empiricamente.

**Nenhum dos achados `p<0,05` originais deste domínio sobrevive à
reprodução adversarial.**

## Veredito honesto — não produz um invariante cross-domain sobrevivente

**`transfer_entropy`, como formulado e testado aqui, NÃO produz um
invariante cross-domain sobrevivente.** O canal PRIMÁRIO
(`TE_net`/`TE_sum`, KSG) não mostra significância robusta em NENHUM dos
2 domínios após reprodução adversarial — o único domínio onde mostrou
achado bruto (Turquia, variante primária) teve esse achado
explicado por um artefato instrumental concreto, identificado e
demonstrado (não apenas hipotetizado), num padrão de refutação
estruturalmente idêntico ao de `dmd_koopman`/Kīlauea, e em certo sentido
mais decisivo (o "sinal" nem correspondia a atividade sísmica real). O
canal de robustez (`STE_net`/`STE_sum`, TE Simbólica) mostrou um risco
de esparsidade combinatória em `N` pequeno, nomeado a priori e agora
confirmado empiricamente — disparando significância espúria mesmo sem
transição real no domínio sísmico.

Isto não invalida a Transferência de Entropia como ferramenta
estabelecida na literatura de teoria da informação/sistemas
dinâmicos acoplados — mostra apenas que, sob a convenção de embedding
(Ragwitz-Kantz), o estimador (KSG-CMI) e o par de nulos substitutos
(IAAFT + deslocamento circular) travados a priori especificamente para
esta linha, nenhum invariante cross-domain robusto emergiu nos 2
domínios testados. A validação sintética (poder real, forte, nos 4
canais e nos 2 nulos) descarta a explicação "a pipeline nunca teria
poder mesmo com acoplamento genuíno" — o resultado negativo é
informativo, não um artefato de instrumento cego.

**Nota de honestidade adicional sobre esta candidatura especificamente:**
sendo a primeira candidatura bivariada/direcional desta linha, ela
também introduziu o primeiro caso desta linha de uma descoberta de
qualidade-de-dado (artefato instrumental) feita DURANTE a checagem
adversarial, não durante a preparação de dado. Isto reforça, de forma
concreta e não hipotética, por que a disciplina de reprodução
adversarial obrigatória desta linha existe — um achado `p<0,05` bruto
que parecia, à primeira vista, a evidência mais forte de toda esta
candidatura (dois canais, dois nulos, `p` tão baixo quanto `0,0`)
evaporou completamente sob escrutínio básico (um filtro passa-alta
padrão).

## Arquivos desta etapa

- `METHODOLOGY_NOTE.md` — metodologia travada ANTES de qualquer cálculo
  (Ragwitz-Kantz + KSG-CMI, TE Simbólica, sub-janelamento, nulo duplo
  IAAFT+deslocamento circular, mitigação obrigatória de propagação de
  onda compartilhada para o domínio sísmico).
- `analysis/te_common.py` — pipeline canônica (seleção de embedding,
  estimador KSG-CMI, TE Simbólica reaproveitando `pe_common.py`,
  sub-janelamento, substitutos IAAFT e deslocamento circular).
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`,
  `analysis/validate_synthetic.log` — validação sintética completa.
- `VALIDATION_NOTE.md` — nota de validação completa e honesta.
- `analysis/run_real_domain.py` — executor por domínio/variante, chamando
  `run_te_analysis` sem modificação.
- `data/prepare_chbmit.py`, `data/prepare_turkey_eq.py` — download +
  preparação, re-executáveis.
- `data/PROVENANCE_CHBMIT.md`, `data/PROVENANCE_TURKEY_EARTHQUAKE.md` —
  proveniência completa (incluindo lacunas reais de dado e retry de
  rede documentados honestamente).
- `data/chbmit_*.npy`, `data/turkeyeq_*.npy`, `data/*_segments_meta.json`
  — segmentos preparados (CHB-MIT ~21MB combinados, committados;
  Turquia já em RMS coarse-grained, poucos KB).
- `analysis/result_chbmit_primary.json`, `analysis/result_chbmit_robust.json`,
  `analysis/result_turkeyeq_primary.json`, `analysis/result_turkeyeq_robust.json`
  — resultados completos (ambos os nulos lado a lado).
- `analysis/confound_check_chbmit.py`,
  `analysis/confound_check_chbmit_results.json`,
  `analysis/CONFOUND_CHECK_CHBMIT.md` — reprodução adversarial completa
  (2 pares de eletrodo alternativos).
- `analysis/confound_check_turkey_eq.py`,
  `analysis/confound_check_turkey_eq_results.json`,
  `analysis/confound_check_turkey_eq_check_b_corrected.json`,
  `analysis/confound_check_turkey_eq.log`,
  `analysis/CONFOUND_CHECK_TURKEY_EARTHQUAKE.md` — reprodução
  adversarial completa (4 checagens + descoberta do artefato
  instrumental + correção de rótulo documentada honestamente).

## Estado da linha — 15 de 15 candidatos identificados agora com resultado completo

| # | Candidato | Domínios testados | Resultado |
|---|---|---|---|
| 1 | `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| 2 | `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| 3 | `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| 4 | `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| 5 | `mse-multiscale-entropy` | Geomagnetismo (1989), rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |
| 6 | `grafo-de-visibilidade` | Geomagnetismo (2015), hidrologia/Harvey | NEGATIVO (sem achado; `d_B` estruturalmente não testável) |
| 7 | `RQA` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |
| 8 | `permutation_entropy` | VitalDB (anestesia), PhysioNet European ST-T | NEGATIVO |
| 9 | `persistent_homology` | — (fechado na validação) | FECHADO NA VALIDAÇÃO |
| 10 | `evt_hill` | (ver linha própria) | NEGATIVO |
| 11 | `kramers_moyal` | (ver linha própria) | NEGATIVO (com rebaixamento de canal) |
| 12 | `lempel-ziv-complexity` | Daphnet FOG, Kilauea 2018 LERZ | NEGATIVO cross-domain (achado intra-domínio de 1 sujeito refutado por reexecução adversarial) |
| 13 | `largest_lyapunov_exponent` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |
| 14 | `dmd_koopman` | Itália COVID-19, Kilauea 2018 (03/05) | NEGATIVO cross-domain (1 domínio NOT_COMPUTABLE; achado do outro refutado por 4 checagens adversariais) |
| 15 | **`transfer_entropy`** | CHB-MIT EEG (onset de convulsão), terremotos Kahramanmaraş | **NEGATIVO cross-domain (achado isolado de 1 domínio refutado por checagem de eletrodo; achado do outro domínio refutado por artefato instrumental identificado + esparsidade combinatória)** |

## Estado da linha e próximo passo (para a sessão orquestradora)

`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` e `DECISION_LEDGER.yaml` NÃO
foram modificados por este agente (fora do escopo desta tarefa) — ficam
a cargo da sessão orquestradora.

**Este fechamento encerra a Fase 0.8** (sondagem de 2026-08-20,
`phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md`) para o candidato #1
(`transfer_entropy`, ranqueado #1 de 2 candidatos novos daquela rodada).
`DISC-TRI-RG-001` chega a 15 candidatos testados no total (3 da Fase 0
original + 4 da Fase 0.5 + 4 da Fase 0.6 + 3 da Fase 0.7 + 1 da Fase
0.8), TODOS NEGATIVOS ou fechados na etapa de validação — nenhum
produziu um invariante cross-domain sobrevivente até agora.

**1 candidato permanece pendente da Fase 0.8:** complexidade estatística
de ε-machines (`C_mu`, mecânica computacional, CSSR/Shalizi & Klinkner
2004 + Inferência Estrutural Bayesiana), ranqueado #2 de 2 candidatos
novos daquela rodada (`phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md`, seção
1) — 2 domínios já verificados por download real (GeyserTimes.org Old
Faithful; genoma completo de *E. coli* K-12 MG1655), nenhum `Delta I`
calculado ainda. O domínio do genoma é ESPACIAL, não temporal — extensão
da convenção desta linha que a própria sondagem já sinalizou precisar de
aval explícito antes de qualquer `METHODOLOGY_NOTE.md`.

Decisão sobre testar `C_mu` (encerrando toda a Fase 0.8), pausar
novamente a linha, buscar mais uma rodada de candidatos genuinamente
novos, ou encerrar `DISC-TRI-RG-001` formalmente fica com o usuário e/ou
a sessão orquestradora, mesmo padrão já seguido em todas as pausas
anteriores desta linha (`DISC-DEC-005`/`006`/`007`/`008`).
