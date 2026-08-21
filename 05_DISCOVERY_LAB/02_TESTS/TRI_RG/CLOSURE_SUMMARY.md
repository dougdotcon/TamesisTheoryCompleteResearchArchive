# Encerramento formal — `DISC-TRI-RG-001`

**Status final: `CLOSED_NULL`** (ver `RESEARCH_PIPELINE.md` — "`CLOSED_*`
nunca é um estado envergonhado"). Encerrado a pedido explícito do usuário
em 2026-08-21, após 16 candidatos genuinamente distintos testados ao
longo de 5 rodadas de busca (Fase 0 original, 0.5, 0.6, 0.7, 0.8), todos
sem produzir um invariante cross-domain sobrevivente. Este documento
sintetiza a história completa da linha para referência futura — nenhum
arquivo individual de candidato é modificado ou invalidado por este
encerramento.

## O que esta linha tentou fazer

Buscar uma "lei de interface" cross-domain: um mapa de coarse-graining
`R_lambda: X_micro -> X_macro` e uma quantidade `I(X)`, definida UMA VEZ
(nunca redefinida por domínio), tal que em domínios reais genuinamente
diferentes (sismologia, ECG, mercados financeiros, ondas gravitacionais,
genômica, vulcanologia, epidemiologia, etc.), uma mudança `Delta I` em
torno de uma transição de regime real e documentada externamente fosse
detectável — sem ajuste ad hoc da definição de `I(X)` por domínio. Isto
testava uma hipótese específica de um programa de pesquisa mais amplo
(TRI/TDTR) sobre interfaces cross-domain do tipo renormalização — nunca
uma alegação de Problema do Millennium, e este encerramento não é uma
alegação sobre o programa TRI/TDTR como um todo, apenas sobre esta linha
empírica específica tal como formulada e testada.

## Os 16 candidatos, em ordem cronológica

| # | Candidato | Rodada | Domínios reais tocados | Resultado |
|---|---|---|---|---|
| 1 | `critical-slowing-down` | Fase 0 | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| 2 | `wavelet-multiresolution-scaling` | Fase 0 | Tohoku/sismologia, CHB-MIT EEG | NEGATIVO |
| 3 | `dfa-multiscale-entropy` | Fase 0 | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo fisiológico já conhecido, CVHR) |
| 4 | `soc-avalanches` | Fase 0.5 | Ridgecrest, flares solares GOES | NEGATIVO (achado inicial refutado por nulo ETAS subcrítico) |
| 5 | `mse-multiscale-entropy` | Fase 0.5 | Geomagnetismo 1989, rolamento FEMTO | NEGATIVO |
| 6 | `grafo-de-visibilidade` | Fase 0.5 | Geomagnetismo, hidrologia/Harvey | NEGATIVO (`d_B` estruturalmente não computável) |
| 7 | `RQA` | Fase 0.5 | — | FECHADO NA VALIDAÇÃO (embedding FNN nunca resolve para ruído fraco) |
| 8 | `permutation-entropy` | Fase 0.6 | VitalDB anestesia, European ST-T | NEGATIVO |
| 9 | `Kramers-Moyal` | Fase 0.6 | vfdb, EUR/CHF | NÃO-COMPUTÁVEL (2 razões estruturais distintas) |
| 10 | `EVT/Hill` | Fase 0.6 | PDX heat dome, Cape Fear | NEGATIVO/não-testável |
| 11 | `persistent-homology/TDA` | Fase 0.6 | — | FECHADO NA VALIDAÇÃO (sem poder vs. controle caótico, r≈0,92 com RQA) |
| 12 | `lempel-ziv-complexity` | Fase 0.7 | Daphnet FoG, Kīlauea 2018 | NEGATIVO (achado intra-sujeito refutado por reexecução adversarial) |
| 13 | `largest-lyapunov-exponent` | Fase 0.7 | — | FECHADO NA VALIDAÇÃO (mesma parede de FNN do RQA) |
| 14 | `dmd-koopman` | Fase 0.7 | Itália COVID-19, Kīlauea 2018 | NEGATIVO (achado refutado — dominado pelo terremoto M6,9) |
| 15 | `transfer-entropy` | Fase 0.8 | CHB-MIT EEG, terremotos Kahramanmaraş | NEGATIVO (achado forte refutado — artefato instrumental de baixa frequência) |
| 16 | `epsilon-machine-complexity` | Fase 0.8 | — | FECHADO NA VALIDAÇÃO (`C_mu` sem poder em 3/3 controles computáveis) |

**Resumo numérico honesto:** 9 negativos após tocar dado real (3 deles
com achados brutos `p<0,05` que não sobreviveram à reprodução
adversarial obrigatória — `soc-avalanches`, `lempel-ziv-complexity`,
`dmd-koopman`, `transfer-entropy`, na verdade 4); 2 não-computáveis por
razões estruturais de dado real (`Kramers-Moyal`, parcialmente
`EVT/Hill`); 4 fechados inteiramente na etapa de validação sintética,
sem nunca tocar dado real (`RQA`, `persistent-homology`,
`largest-lyapunov-exponent`, `epsilon-machine-complexity`).

## O padrão estrutural descoberto — a lição mais valiosa desta linha

A investigação retrospectiva (conduzida a pedido do usuário antes da
Fase 0.8) revelou que os primeiros 14 candidatos, apesar de parecerem
14 ideias distintas, colapsam em apenas ~4 eixos matemáticos latentes
independentes:

- **Eixo A — persistência/taxa de entropia** (família Hurst): `dfa`,
  `wavelet`, `mse`, `permutation_entropy`, `lempel_ziv`, e os 2
  candidatos `viable=false` da própria Fase 0.7 (`MF-DFA`, `EMD`) —
  provados, por identidade algébrica ou equivalência assintótica citada
  na literatura, estimadores diferentes da MESMA quantidade subjacente.
- **Eixo B — taxa de relaxação local** (decaimento Ornstein-Uhlenbeck):
  `critical-slowing-down`, o `kappa` de `Kramers-Moyal`, e o autovalor
  real demovido de `dmd-koopman` — provados algebricamente idênticos
  (Ritchie & Sieber 2016; confirmado de novo para DMD por 2 artigos
  2025-2026).
- **Eixo C — densidade de recorrência via embedding de Takens/Hankel**:
  `RQA`, `persistent-homology`, `largest-lyapunov-exponent`, e
  parcialmente `dmd-koopman` — todos compartilham a MESMA maquinaria de
  reconstrução de espaço de fase, que se mostrou estruturalmente frágil
  para dado real fracamente correlacionado (Falsos Vizinhos Mais
  Próximos nunca resolve `m<=10` para ruído/fGn fraco) — 3 dos 4 candidatos
  deste eixo fecharam na etapa de validação por essa exata razão
  recorrente, não por acidente independente.
- **Eixo D — estatística de cauda/eventos extremos**: `soc-avalanches`,
  `EVT/Hill` — os únicos 2 candidatos que não colapsaram nos eixos A-C,
  mas ambos esbarraram em problemas de dado real (piso de amostra,
  confundidores mundanos) mais do que em identificabilidade matemática.

A Fase 0.8 foi desenhada especificamente para escapar destes 4 eixos —
e conseguiu: `transfer-entropy` foi a primeira candidatura
bivariada/direcional de toda a linha (as 14 anteriores eram todas
univariadas), e `epsilon-machine-complexity` (`C_mu`) foi provado
matematicamente distinto de `C_JS` (já testado no Eixo A-adjacente via
entropia de permutação). Ainda assim, nenhum dos dois produziu um
invariante sobrevivente — `transfer-entropy` por um achado forte
refutado por um artefato instrumental real descoberto na reprodução
adversarial, `C_mu` por não estabelecer poder discriminativo nem no
dado sintético.

## Disciplina metodológica que se provou decisiva

- **Reprodução adversarial obrigatória para qualquer `p<0,05`**: sem
  essa disciplina, pelo menos 4 candidatos (`soc-avalanches`,
  `lempel-ziv-complexity`, `dmd-koopman`, `transfer-entropy`) teriam
  sido catalogados como achados positivos genuínos. Em todos os 4 casos,
  investigação adversarial direta (não apenas checagens estatísticas de
  robustez, mas inspeção do dado bruto) encontrou uma explicação mundana
  concreta — um nulo ETAS subcrítico, falha de generalização entre
  sujeitos, o terremoto M6,9 de Kīlauea dominando trivialmente a
  decomposição, e um artefato instrumental de baixa frequência numa
  estação sísmica que um filtro passa-alta padrão eliminou por completo.
- **Validação sintética obrigatória antes de qualquer dado real**:
  evitou gasto de recursos computacionais em 4 candidatos que já não
  tinham identificabilidade estabelecida (`RQA`, `persistent-homology`,
  `largest-lyapunov-exponent`, `epsilon-machine-complexity`), e permitiu
  fechá-los honestamente sem alegar "negativo em dado real" quando o
  dado real nunca foi tocado.
- **Escalonamento de "uma correção delimitada, depois fechar"**: usado
  repetidamente (redesenho de controle positivo do RQA para Rössler;
  correção de `L=1` trivial em `epsilon-machine-complexity`) — nunca
  permitiu ajuste aberto até encontrar um resultado favorável.
- **Rebaixamento a priori de canais redundantes**: `kappa`/`beta_D2`
  (Kramers-Moyal), `d_B` (grafo de visibilidade), autovalor real
  (DMD), `h_mu` (ε-machines) — todos identificados e documentados como
  redundantes ANTES de qualquer cálculo, não descobertos post-hoc.

## O que permanece reaproveitável

Toda a infraestrutura das 5 rodadas de busca permanece commitada:
16 `METHODOLOGY_NOTE.md`, pipelines validadas contra dado sintético,
domínios reais de mais de 20 fontes distintas (sismologia, EEG/ECG,
mercados financeiros, geofísica, genômica, vulcanologia, hidrologia,
epidemiologia), incluindo domínios verificados mas nunca processados
(Old Faithful, La Palma 2021, genoma de *E. coli*) por candidatos
fechados na validação. Nenhum destes arquivos é apagado por este
encerramento — ficam disponíveis caso a linha seja reaberta no futuro
com um candidato genuinamente novo ou uma reimplementação corrigida de
um candidato já fechado (ex. CSSR incremental completo para
`epsilon-machine-complexity`).

## Veredito final, honesto e sem inflação

**Sob os 16 candidatos testados aqui, com o rigor metodológico completo
desta linha (pré-registro de metodologia antes de dado real, validação
sintética obrigatória, protocolo de significância padronizado,
reprodução adversarial obrigatória para qualquer achado positivo),
nenhum invariante cross-domain sobrevivente foi encontrado para a
hipótese de interface TRI/TDTR tal como operacionalizada nesta linha.**

Isto NÃO é uma prova de impossibilidade — é um resultado empírico sobre
um conjunto específico, ainda que amplo e cuidadosamente diversificado,
de operacionalizações matemáticas tentadas. O padrão descoberto (colapso
em ~4 eixos latentes) sugere que a maior parte do espaço de estatísticas
não-lineares "óbvias" da literatura de séries temporais já foi
efetivamente coberta por esta busca, mesmo quando cada candidato parecia
superficialmente novo. Isto também NÃO é uma alegação sobre o programa
de pesquisa TRI/TDTR mais amplo, nem sobre a ideia de interface
cross-domain como conceito geral — é especificamente sobre esta linha
empírica, com estas 16 tentativas, sob esta disciplina metodológica.

## Registro de governança

Ver `DECISION_LEDGER.yaml`, `DISC-DEC-010` — encerramento formal a
pedido explícito do usuário, `status` de `DISC-TRI-RG-001` em
`TEST_QUEUE.yaml` mudado de `CANDIDATE_FORMULATING` para `CLOSED_NULL`
(a primeira mudança de status desta linha desde sua criação — todas as
5 pausas anteriores mantiveram `CANDIDATE_FORMULATING`, já que pausa e
encerramento formal são estados distintos nesta máquina de estados).
