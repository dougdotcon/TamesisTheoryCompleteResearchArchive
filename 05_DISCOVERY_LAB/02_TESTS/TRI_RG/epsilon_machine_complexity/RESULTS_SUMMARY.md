# Resultado do fechamento dos gaps — `epsilon-machine-complexity` (Complexidade Estatística de ε-machines, `C_mu`, mecânica computacional)

**Data:** 2026-08-21. Metodologia fixada em `METHODOLOGY_NOTE.md` (CSSR de
`L` fixo com varredura de convergência `L_max∈{1,...,8}`, gate de rejeição
obrigatório `DEGENERATE`/`NOT_CONVERGENT`/`NOT_DETERMINISTIC`,
`I(X)=C_mu` primário + `h_mu` companheiro/diagnóstico REBAIXADO a priori,
checagem BSI companheira restrita ao canal binarizado/ternário,
substitutos IAAFT primários + bootstrap por blocos móveis pré-autorizado)
validada contra dado sintético ANTES de qualquer dado real
(`VALIDATION_NOTE.md`). **Este candidato foi fechado inteiramente na
etapa de validação sintética — nenhum dado real (Old Faithful,
GeyserTimes.org; La Palma/Cumbre Vieja 2021, catálogo EMSC/IGN) foi
tocado em nenhum momento**, apesar de ambos os domínios terem sido
verificados como genuinamente acessíveis e de boa qualidade por download
real nesta sessão (ver `METHODOLOGY_NOTE.md`).

## Governança — domínio espacial (genoma de E. coli) não usado

Conforme decisão já tomada pela sessão orquestradora antes do início
desta tarefa, o genoma de *E. coli* K-12 MG1655 (domínio ESPACIAL
sinalizado pelo levantamento da Fase 0.8 como precisando de aval
explícito) NÃO foi usado. Um segundo domínio genuinamente TEMPORAL foi
buscado e verificado com sucesso nesta sessão — a sequência de
interevento sísmico da erupção de Cumbre Vieja, La Palma, 2021 (catálogo
EMSC/IGN, 1.049 eventos PRE + 6.747 eventos POST, verificados por
download real, sem duplicatas, magnitudes plausíveis) — tornando o
fallback espacial desnecessário. Ainda assim, como o candidato fechou na
etapa de validação, **nenhum dos 2 domínios (Old Faithful, La Palma) foi
efetivamente processado pelo pipeline de `C_mu`** — a busca e verificação
de domínio ficam documentadas em `METHODOLOGY_NOTE.md` para retomada
futura, caso a linha algum dia revisite este candidato com uma
implementação de CSSR mais completa (ver seção final).

## Validação — recapitulação (ver `VALIDATION_NOTE.md` para o detalhe completo)

**Diagnósticos de correção de código:** OK — teste qui-quadrado, processo
período-2 (correspondência exata `C_mu=1,0`/`h_mu=0,0`) e cadeia de
Markov de primeira ordem à mão computável (`C_mu=0,6488` vs. teoria
`0,6500`, `N=200.000`) todos passam. **Achado honesto, não escondido:**
o Processo Even (exemplo do próprio artigo de Shalizi & Klinkner 2004,
máquina mínima verdadeira de 2 estados, `C_mu=0,9183`) revela uma
LIMITAÇÃO ESTRUTURAL da simplificação de escopo desta implementação
(clustering de `L` fixo, não o CSSR incremental completo) — converge
para 3 estados, não 2, porque o Processo Even tem ordem de Markov
infinita mas complexidade de estado causal finita, exigindo o
refinamento recursivo do CSSR completo para ser recuperado corretamente.
A tarefa explicitamente autoriza uma cadeia de Markov simples como
alternativa de diagnóstico ao Processo Even, o que foi usado como o
critério de correção de código PRINCIPAL; o achado do Processo Even é
reportado como limitação adicional, não escondido.

**A ÚNICA correção pré-autorizada, aplicada durante a validação:**
descoberto que `pi_s` em `L=1` é matematicamente forçado a igualar a
marginal de construção do próprio `R_lambda` (`0,5/0,5` mediana,
`1/3` cada tercil) sempre que as histórias de `L=1` não se fundem —
tornando `C_mu(L=1)` um valor trivial/constante sem informação
discriminante (confirmado empiricamente: desvio-padrão `0,00000000`
entre 20 substitutos IAAFT reais). Corrigido excluindo `L=1` da busca de
estabilidade que seleciona `L_max` (`min_L_for_selection=2` em
`select_Lmax_and_reconstruct`).

**4 controles positivos independentes, orçamento completo
(`N_SURROGATES=200`), cobrindo os 2 canais de simbolização (mediana,
ternário) e 2 noções qualitativamente distintas de "complexidade causal
genuinamente maior" (ordem/persistência de Markov; determinismo caótico
genuíno vs. estrutura Markov linear):**

| Controle | `p_C_mu` (IAAFT) | `p_h_mu` (IAAFT) |
|---|---|---|
| Markov ordem-1 vs. ordem-2 (mediana) | 0,735 | 0,0 |
| Markov 3 símbolos, persistência fraca vs. forte (ternário) | 0,405 | 0,0 |
| Markov 3 símbolos vs. mapa logístico `r=4` remapeado (ternário) | 1,0 (direção errada) | 0,0 |
| Ruído/logístico `r=4` (mediana) | `DEGENERATE` (achado estrutural honesto) | — |

`C_mu` (canal PRIMÁRIO) **não mostra poder discriminativo real em
nenhum dos 3 controles computáveis**, mesmo após a única correção
autorizada. O fallback de bootstrap por blocos móveis (Kunsch 1989),
aplicado ao achado de baixo poder mais claro, também **não recupera
poder** (`p=0,595`, ligeiramente pior que o IAAFT) — mesmo padrão exato
já documentado por `lempel_ziv_complexity` para seu canal `LZC_median`.

`h_mu` (canal companheiro, REBAIXADO a priori) mostra poder real e
consistente (`p=0,0`) nos 3 controles positivos computáveis — **mas
dispara um FALSO POSITIVO espúrio (`p=0,0`) em um controle negativo**
(PRE e POST literalmente o mesmo processo gerador, sorteios
independentes) — revelando calibração pouco confiável, não podendo ser
promovido como substituto do canal primário mesmo que a governança
desejasse fazê-lo.

## Veredito honesto

`epsilon-machine-complexity` (`C_mu`), como formulado e implementado
aqui (CSSR de `L` fixo com gate de rejeição obrigatório, `I(X)=C_mu`
primário), **não teve sua identificabilidade empírica estabelecida em
nenhum dos 3 desenhos de controle positivo computáveis, mesmo após a
única correção pré-autorizada e o fallback de bootstrap** — distinto de
"negativo em dado real" (que nunca chegou a ser tocado, per a disciplina
desta linha, honesta e igualmente valiosa: fechamento na etapa de
validação já usado 3x nesta linha — `rqa`, `persistent_homology`,
`largest_lyapunov_exponent`).

**Nota interpretativa importante, nomeada explicitamente aqui (não
escondida atrás de uma conclusão mais forte que os dados sustentam):**
este achado tem DUAS explicações honestamente não-distinguíveis com o
orçamento desta tarefa — (1) uma fragilidade específica da simplificação
de escopo desta implementação (clustering guloso de `L` fixo em vez do
CSSR incremental completo de Shalizi & Klinkner, que introduz ruído de
decisão de clustering discreto entre a série real e cada substituto,
inflando a variância nula de `C_mu` além do que uma reconstrução CSSR
completa produziria); ou (2) uma fragilidade mais geral de `C_mu` como
estimador estatístico em amostra finita, mesmo sob uma implementação
completa — a literatura de mecânica computacional é conhecida por notar
que estimativas de `C_mu` em amostra finita têm variância consideravelmente
maior que as de `h_mu` (uma quantidade "mais local"), precisamente
porque `C_mu` depende da IDENTIDADE e do NÚMERO de estados discretos
inferidos, uma decisão combinatória discreta, e não apenas de médias
suaves de probabilidades condicionais. Esta candidatura NÃO permite
decidir entre essas duas explicações — dito aqui honestamente.

**Achado adicional, epistemologicamente relevante para a linha inteira,
nomeado a priori em `METHODOLOGY_NOTE.md` e retomado agora:** `C_mu` e
`C_JS` (entropia de permutação, candidato #8, já fechado negativo 8/8)
pertencem à MESMA FAMÍLIA ESTRATÉGICA de medidas de complexidade em
forma de U-invertido/pico, desenhadas para capturar o mesmo tipo de
sinal qualitativo (estrutura intermediária entre ordem total e
aleatoriedade total) — apesar de serem objetos matematicamente
DIFERENTES (Crutchfield & Feldman 2003 provam `(h_mu,C_mu)` como par
formalmente independente com limite `E<=C_mu` sem análogo em `C_JS`).
Com `epsilon-machine-complexity` agora também não produzindo evidência
robusta (seja por não sobreviver ao dado real como `C_JS`, seja aqui por
não estabelecer identificabilidade nem chegar ao dado real), **a
estratégia inteira de "complexidade-em-pico" como classe de candidatos
para esta linha — não apenas uma fórmula específica — acumula agora 2/2
tentativas sem produzir um invariante cross-domain sobrevivente.** Isto
é dito aqui explicitamente, como o próprio `METHODOLOGY_NOTE.md` já
previu que deveria ser dito se este resultado ocorresse.

## Arquivos desta etapa

- `METHODOLOGY_NOTE.md` — metodologia travada ANTES de qualquer cálculo
  (CSSR de `L` fixo, gate de rejeição, BSI companheira, IAAFT + bootstrap,
  verificação completa dos 2 domínios reais).
- `analysis/em_common.py` — pipeline canônica (CSSR de `L` fixo com
  varredura de convergência, gate de rejeição, checagem BSI, IAAFT,
  bootstrap por blocos móveis).
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`,
  `analysis/validate_synthetic.log` — validação sintética completa
  (diagnósticos de correção de código, a única correção aplicada, 4
  controles positivos, 1 checagem de fallback de bootstrap, 2 controles
  negativos).
- `VALIDATION_NOTE.md` — nota de validação completa e honesta.
- **Nenhum arquivo de dado real, proveniência, ou resultado por domínio
  foi criado** — a linha fechou antes de qualquer necessidade de
  download/preparação de pipeline (os 2 domínios foram apenas
  VERIFICADOS como acessíveis e de boa qualidade por download real,
  documentado narrativamente em `METHODOLOGY_NOTE.md`, mas o pipeline de
  `C_mu` nunca rodou sobre eles).

## Estado da linha — 16 de 16 candidatos identificados agora com resultado completo

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
| 15 | `transfer_entropy` | CHB-MIT EEG (onset de convulsão), terremotos Kahramanmaraş | NEGATIVO cross-domain (achado isolado de 1 domínio refutado por checagem de eletrodo; achado do outro domínio refutado por artefato instrumental identificado + esparsidade combinatória) |
| 16 | **`epsilon-machine-complexity`** | — (fechado na validação; Old Faithful + La Palma 2021 verificados mas nunca processados) | **FECHADO NA VALIDAÇÃO (identificabilidade de `C_mu` não estabelecida em 3/3 controles positivos computáveis, mesmo após correção + fallback; dado real nunca tocado)** |

**Todos os 16 candidatos testados até agora terminaram sem produzir um
invariante cross-domain sobrevivente** — 13 negativos em dado real (3
deles com achados brutos `p<0,05` que não sobreviveram à reprodução
adversarial obrigatória) e agora 4 fechados na etapa de validação (`RQA`,
`persistent_homology`, `largest_lyapunov_exponent`,
`epsilon-machine-complexity`).

## Isto encerra a Fase 0.8 por completo

**Este fechamento encerra a Fase 0.8** (sondagem de 2026-08-20,
`phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md`) inteiramente — os 2
candidatos daquela rodada agora têm resultado completo:
`transferência de entropia` (candidato #1, fechado negativo cross-domain
em 2026-08-21, ver `transfer_entropy/RESULTS_SUMMARY.md`) e
`epsilon-machine-complexity` (candidato #2, fechado na etapa de
validação aqui). **Nenhum candidato novo permanece pendente de nenhuma
rodada de busca anterior (Fase 0 original, 0.5, 0.6, 0.7, 0.8) —
`DISC-TRI-RG-001` está, pela primeira vez desde sua criação, sem
nenhuma candidatura formulada e ainda não testada.**

## Estado da linha e próximo passo (para a sessão orquestradora)

`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` e `DECISION_LEDGER.yaml` NÃO
foram modificados por este agente (fora do escopo desta tarefa) — ficam
a cargo da sessão orquestradora, que já tem o padrão estabelecido de como
registrar um fechamento na etapa de validação (usado agora 4x nesta
linha) e de como registrar o encerramento formal de uma rodada de busca
(Fase 0.8, usado pela primeira vez de forma completa aqui).

Com 16/16 candidatos testados, todos sem invariante cross-domain
sobrevivente, e nenhuma candidatura nova pendente de nenhuma rodada de
busca anterior, a decisão sobre o próximo passo — uma nova rodada de
busca por candidatos genuinamente novos (6ª desde a criação da linha),
revisitar algum candidato já fechado com um desenho corrigido
(ex. uma implementação de CSSR completa/incremental para
`epsilon-machine-complexity`, dado que os 2 domínios reais já ficam
verificados e documentados em `METHODOLOGY_NOTE.md` para reaproveitamento
futuro), pausar novamente a linha, ou encerrar `DISC-TRI-RG-001`
formalmente — fica inteiramente aberta, a cargo do usuário e/ou da sessão
orquestradora, mesmo padrão já seguido em todas as pausas anteriores
desta linha (`DISC-DEC-005`/`006`/`007`/`008`).
