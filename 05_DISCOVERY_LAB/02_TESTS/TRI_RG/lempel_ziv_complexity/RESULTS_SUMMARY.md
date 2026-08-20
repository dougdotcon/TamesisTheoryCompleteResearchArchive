# Resultado do fechamento dos gaps — `lempel-ziv-complexity` (Complexidade de Lempel-Ziv, canais mediana/tercis)

**Data:** 2026-08-20. Metodologia fixada em `METHODOLOGY_NOTE.md`
(nenhum `PREREGISTRATION.md`, per convenção desta linha) e pipeline
(`analysis/lzc_common.py`, LZ76/Kaspar & Schuster 1987 + binarização por
mediana/`LZC_median` primário + quantização ternária por tercis/
`LZC_ternary` companheiro, teste de significância por substitutos IAAFT
com fallback pré-autorizado de bootstrap por blocos móveis) validada
contra dado sintético ANTES de qualquer dado real (ver
`VALIDATION_NOTE.md`). Aplicada, com uma correção de desempenho
descoberta e documentada no meio do caminho (ver seção própria abaixo),
aos 2 domínios declarados: Daphnet Freezing-of-Gait (`S01R01`) e Kilauea
2018 LERZ (`HV.HAT..HHZ`).

## Veredito de validação — honesto, sem suavizar, por canal (recapitulação de `VALIDATION_NOTE.md`)

**`LZC_median` (canal primário): NÃO estabeleceu poder discriminativo
real por NENHUM dos dois testes de significância disponíveis nesta
linha.** IAAFT (teste primário): `p=0,455` no controle positivo (mapa
logístico vs. ruído branco) — `IAAFT_LOW_POWER`. Bootstrap por blocos
móveis (fallback pré-autorizado, acionado automaticamente por essa
mesma razão): `p=0,95` no MESMO controle positivo — **PIOR que o
IAAFT, não melhor** — `BOOTSTRAP_LOW_POWER`. Veredito final mecânico:
`NO_POWER_ESTABLISHED_EITHER_TEST`. Isto é dito aqui explicitamente,
não escondido nem suavizado: o canal PRIMÁRIO desta linha não passou
pela validação de poder por nenhum caminho disponível.

**`LZC_ternary` (canal companheiro): teve poder IAAFT real desde o
início, sem precisar de fallback.** `p=0,0` no controle positivo
(separação total, σ-equivalente `-41,14`), corretamente não
significativo no controle negativo (`p=0,74`) e sem significância
espúria sob o controle de Hurst diferencial (`p=0,455`). Veredito:
`SURVIVES_PRIMARY_IAAFT_TEST`.

Estes dois fatos ficam visíveis aqui, lado a lado, exatamente como
determinado: o canal PRIMÁRIO desta linha não tem poder validado; o
canal COMPANHEIRO tem. Nenhum dos dois foi promovido/rebaixado por este
agente — essa decisão de governança cabe à sessão orquestradora, per
`METHODOLOGY_NOTE.md` Gap (e).

## Correção de desempenho descoberta ao aplicar o pipeline a dado real (ver `VALIDATION_NOTE.md`, adendo)

`METHODOLOGY_NOTE.md` Gap (d) assumia "o próprio parsing LZ76 é O(N) e
barato" — **falso para a implementação ingênua efetivamente usada**: o
laço aninhado i/k/l reinicia sua busca a partir de `i=0` a cada fronteira
de frase, dando ≈O(N²/log N) de trabalho total. Invisível na validação
sintética (`N=3.000`, rápido mesmo assim), mas travou o pipeline em dado
real por dezenas de minutos de CPU sem terminar sequer UMA combinação
(`N` de 36 mil a 200 mil amostras). Substituída por uma reimplementação
O(n log n) matematicamente equivalente (array de sufixos + LCP de Kasai
+ RMQ por tabela esparsa + árvore de Fenwick para estatística de ordem),
verificada bit-a-bit contra a versão ingênua em 800+ casos sintéticos e
em segmentos REAIS dos dois domínios antes de qualquer uso — ver
`VALIDATION_NOTE.md` para a prova de equivalência completa e a
reconfirmação de que `validate_synthetic.py` reexecutado após a correção
produz resultados BIT-IDÊNTICOS aos já documentados. **Correção
estritamente de desempenho de implementação — nenhuma decisão de
`R_lambda`/`I(X)`/protocolo de significância foi tocada.**

## Domínio 1 — Daphnet Freezing-of-Gait, sujeito `S01R01`

| Variante | Canal | PRE | POST | Δ | `p` (IAAFT) |
|---|---|---|---|---|---|
| Primária | `LZC_median` | 0,3187 | 0,4539 | +0,1352 | 1,0 |
| Primária | `LZC_ternary` | 0,3901 | 0,5149 | +0,1248 | 1,0 |
| Robustez | `LZC_median` | 0,8132 | 0,6047 | **−0,2085** | **0,0** |
| Robustez | `LZC_ternary` | 0,7472 | 0,5548 | **−0,1923** | **0,0** |

**Assimetria primária/robustez, honesta:** a variante PRIMÁRIA (PRE =
tudo antes do primeiro onset de congelamento, POST = tudo depois,
incluindo os outros 17 episódios subsequentes e ~20min de caminhada
intercalada) **NÃO é significativa em nenhum canal** (`p=1,0`). A
variante ROBUSTEZ (janela estreita, ~570-620s de cada lado, mais
próxima do onset) **É significativa nos DOIS canais** (`p=0,0`).

**Checagem de confundidor acionada** (`p<0,05` em pelo menos uma
combinação) — ver `analysis/CONFOUND_CHECK_DAPHNET.md` in extenso.
Resumo honesto: 3 checagens diretas feitas dentro desta sessão. (1)
Confundidor de composição de rótulo (PRE robustez mistura "fora de
protocolo"/caminhada; POST robustez mistura caminhada/congelamento) —
**REFUTADO**: a queda persiste com magnitude comparável mesmo
comparando exclusivamente caminhada-pura vs. caminhada-pura (`LZC_median`
`0,7613→0,5912`, Δ=−0,170, vs. Δ=−0,209 completo). (2) Glitch/saturação
de sensor exatamente no onset — **REFUTADO**: nenhum valor
repetido/saturado, desvio-padrão SOBE (não some) logo após o onset. (3)
Deriva genérica de sessão (não ligada ao onset especificamente) — o
recorte por quartos mostra `LZC_median` estável no PRE (`0,822→0,807`)
e então **DESPENCANDO logo após o onset** (`Q3=0,3965`) com recuperação
parcial no quarto mais distante (`Q4=0,7633`) — um mergulho TRANSIENTE
concentrado na transição, não uma deriva linear, explicando diretamente
por que a robustez (captura o mergulho) é significativa e a primária
(dilui o mergulho em ~20min de dado subsequente) não é.

**Nenhuma das explicações espúrias verificáveis dentro desta sessão
sobrevive ao teste direto.** O padrão é fisiologicamente plausível à
luz da literatura de índice de congelamento (Bächlin et al. 2010: tremor
de alta frequência/baixa complexidade concentrado no início do
congelamento). **Isto continua sendo um achado de UM sujeito, UM
registro, UMA transição** — sem replicação através de sujeitos dentro
desta rodada, e sem a reexecução adversarial independente de segundo
agente (passo 7 de `AGENTS.md`), que permanece pendente da sessão
orquestradora.

## Domínio 2 — Kilauea 2018 LERZ, estação `HV.HAT..HHZ`

| Variante | Canal | PRE | POST | Δ | `p` (IAAFT) |
|---|---|---|---|---|---|
| Primária | `LZC_median` | 0,0295 | 0,0385 | +0,0091 | 1,0 |
| Primária | `LZC_ternary` | 0,0431 | 0,0435 | +0,0004 | 1,0 |
| Robustez | `LZC_median` | 0,0465 | 0,0306 | −0,0159 | 0,805 |
| Robustez | `LZC_ternary` | 0,1324 | 0,0475 | −0,0849 | **0,09** |

**Nenhuma combinação cruza `p<0,05`** neste domínio — checagem de
confundidor NÃO acionada aqui. Nota honesta: `LZC_ternary` robustez
fica em `p=0,09`, o mais próximo do limiar entre as 6 combinações não
significativas desta linha nos dois domínios — reportado por
completude, não tratado como achado (não cruza o limiar pré-declarado).
Valores de `LZC` muito mais baixos que no Daphnet (`~0,03-0,13` vs.
`~0,3-0,8`) refletem a decimação forte exigida pelo teto de
`MAX_N_PER_SEGMENT=200.000` sobre séries de 100Hz/8,6-10,3M amostras
(fator ~22-52, ~100Hz→~2-4,5Hz efetivo, per `METHODOLOGY_NOTE.md` Gap
(d)) — sismicidade de banda relativamente estreita nessa resolução
efetiva produz uma série muito mais estruturada/previsível que
acelerometria de marcha a 64Hz.

## Veredito honesto — não produz um invariante cross-domain sobrevivente

**`lempel-ziv-complexity`, como formulado e testado aqui, NÃO produz um
invariante cross-domain sobrevivente.** O único achado com `p<0,05` em
qualquer combinação (Daphnet, variante robustez, ambos os canais) é
`intra-domínio, intra-sujeito, intra-variante` — não aparece na variante
primária do MESMO domínio, e o segundo domínio (Kilauea) não mostra
NADA em nenhuma combinação. Um invariante cross-domain exigiria, no
mínimo, um sinal coerente nos DOIS domínios — isso não acontece aqui.

Ao mesmo tempo, isto não é um nulo completo e vazio como vários
candidatos anteriores desta linha: o achado de Daphnet-robustez
sobreviveu a 3 checagens diretas de confundidor dentro desta sessão
(composição de rótulo, glitch de sensor, deriva genérica), mostra um
padrão temporal fino coerente com a fisiologia documentada de
congelamento de marcha, e é corroborado pelos DOIS canais na mesma
direção — incluindo `LZC_ternary`, o canal que teve poder IAAFT real
validado desde o início. **Mas `LZC_median` (canal primário desta
linha) não tinha poder discriminativo estabelecido por NENHUM teste de
significância antes de tocar dado real — então seu `p=0,0` aqui precisa
ser lido com essa ressalva explícita, mesmo corroborado pelo canal
companheiro.** Nenhuma alegação de "achado cross-domain" é feita aqui;
o que se relata é um sinal intra-domínio real, investigado a fundo,
não descartado nem inflado.

## Arquivos desta etapa

- `analysis/lzc_common.py` (pipeline, LOCKED desde a validação sintética
  quanto a `R_lambda`/`I(X)`/protocolo de significância; corrigido
  apenas quanto a desempenho de `lz76_complexity` — versão ingênua
  preservada como `lz76_complexity_naive` para validação cruzada, ver
  `VALIDATION_NOTE.md`)
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`,
  `VALIDATION_NOTE.md` (validação sintética completa, incl. o fallback
  de bootstrap e o adendo de correção de desempenho)
- `analysis/run_real_domain.py` (executor por domínio/variante,
  chamando `run_lzc_analysis` sem modificação)
- `data/prepare_daphnet.py`, `data/prepare_kilauea.py` (download +
  preparação, re-executáveis)
- `data/PROVENANCE_DAPHNET.md`, `data/PROVENANCE_KILAUEA.md`
  (proveniência completa)
- `data/daphnet_{pre,post}_{primary,robust}.npy`,
  `data/daphnet_segments_meta.json` (segmentos derivados, pequenos)
- `data/kilauea_{pre,post}_{primary,robust}.npy`,
  `data/kilauea_segments_meta.json` (segmentos derivados, grandes —
  ~150MB combinados, resolução nativa 100Hz não pré-decimada, per
  `PROVENANCE_KILAUEA.md`; NÃO commitados por instrução explícita desta
  etapa)
- `analysis/result_daphnet_primary.json`,
  `analysis/result_daphnet_robust.json`,
  `analysis/result_kilauea_primary.json`,
  `analysis/result_kilauea_robust.json` (resultados completos)
- `analysis/CONFOUND_CHECK_DAPHNET.md` (checagem de confundidor
  completa, acionada pelo `p<0,05` em Daphnet-robustez)

## Adendo — reexecução adversarial independente (passo 7 de `AGENTS.md`), 2026-08-20

Acionada pelo `p<0,05` em Daphnet-robustez. Um segundo agente,
independente, sem memória desta sessão, tentou ativamente quebrar o
achado por 4 rotas novas não tentadas aqui (ver `analysis/
ADVERSARIAL_REPRODUCTION_DAPHNET.md` in extenso). Veredito honesto,
misto: o número `p=0,0`/`p=0,0` de `S01R01` é bit-a-bit reproduzível, não
é bug, e sobrevive a deslocamento do ponto de corte (±120s) — mas **NÃO
sobrevive integralmente** a duas rotas novas: (1) generalização entre
sujeitos — de 4 sujeitos testados sob o MESMO pipeline travado, apenas
`S01R01` atinge significância; `S07R01` mostra o padrão INVERTIDO com
igual força estatística (`p=0,0` nos dois canais, sinal oposto);
`S03R01` mostra os dois canais discordando em sinal entre si; (2)
robustez ao método de substituto alternativo já pré-autorizado — sob
bootstrap por blocos móveis (Kunsch 1989), `LZC_ternary` (o canal com
poder IAAFT validado desde a etapa sintética) PERDE significância
(`p=0,07`), invertendo a hierarquia de confiança entre canais que a
própria validação sintética havia estabelecido. Conclusão do agente
adversarial, adotada aqui: o achado de Daphnet-robustez é uma observação
numérica real e localizada, mas NÃO deve ser tratado como "investigado e
não-refutado" no sentido forte que autorizaria avanço ao Gate de
Replicação — é, na melhor leitura honesta, uma curiosidade de um único
sujeito/registro, não um padrão fisiológico replicável dentro do próprio
dataset usado.

## Veredito final da linha, revisado após a reexecução adversarial

`lempel-ziv-complexity` **não produz um invariante cross-domain
sobrevivente** (nenhum sinal em Kilauea, em nenhuma variante) **e o
único achado intra-domínio (Daphnet-robustez) não sobrevive de forma
robusta à reexecução adversarial** (falha de generalização entre
sujeitos do mesmo dataset; perde significância sob o método de
substituto alternativo já pré-autorizado). `LZC_median` (canal primário
desta linha) nunca teve poder discriminativo validado por nenhum dos
dois testes de significância disponíveis, em nenhuma etapa. Isto é o
**12º candidato** desta linha a terminar sem produzir um achado
cross-domain sobrevivente — e, ao contrário de vários candidatos
anteriores (RQA, homologia persistente), este chegou a mostrar um sinal
`p<0,05` real em dado real antes de ser refutado por reexecução
adversarial, um padrão mais próximo do achado de `dfa-multiscale-entropy`
(efeito real de um domínio, não replicado no segundo, não promovido a
invariante) do que dos fechamentos por não-computabilidade estrutural.

## Estado da linha e próximo passo

`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` e `DECISION_LEDGER.yaml`
foram atualizados pela sessão orquestradora após integrar este resultado
e o da reexecução adversarial, mesmo padrão já usado para todos os
candidatos anteriores desta linha. Nenhum rebaixamento formal de canal
foi registrado como decisão de governança separada (diferente de
`kappa`/`beta_D2` em Kramers-Moyal ou `d_B` em grafo-de-visibilidade) —
dado que o candidato como um todo fecha sem invariante sobrevivente, a
ressalva sobre `LZC_median` já fica suficientemente documentada aqui e
em `VALIDATION_NOTE.md`, sem necessidade de uma ação de governança
adicional.
