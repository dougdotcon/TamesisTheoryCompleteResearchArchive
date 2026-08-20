# Checagem de confundidor — Daphnet Freezing-of-Gait, `S01R01`, variante de robustez

**Por que esta checagem foi acionada:** entre as 4 combinações
domínio×variante × 2 canais (8 testes no total), **apenas UMA
combinação cruza `p<0,05`: Daphnet, variante ROBUSTEZ, nos DOIS
canais** (`p_LZC_median=0,0`, `p_LZC_ternary=0,0` — ver
`RESULTS_SUMMARY.md`). A instrução da sessão orquestradora exige uma
checagem de reprodução adversarial/descoberta-de-nulo antes de
finalizar qualquer achado com `p<0,05` em qualquer combinação — esta
nota documenta essa checagem, feita inteiramente dentro desta sessão
(não é a reexecução adversarial independente de segundo agente do
passo 7 de `AGENTS.md`, que permanece pendente de decisão da sessão
orquestradora, mesma disciplina já usada nas notas anteriores desta
linha).

## Achado bruto que motiva a checagem

| Canal | PRE robustez | POST robustez | Δ | `p` (IAAFT) |
|---|---|---|---|---|
| `LZC_median` | 0,8132 | 0,6047 | **−0,2085** | **0,0** |
| `LZC_ternary` | 0,7472 | 0,5548 | **−0,1923** | **0,0** |

Notavelmente, a variante PRIMÁRIA do MESMO domínio (janela completa:
PRE = tudo antes do onset, POST = tudo depois, incluindo os outros 17
episódios de congelamento subsequentes) é **NÃO significativa nos dois
canais** (`p=1,0` para ambos — ver `RESULTS_SUMMARY.md`). Essa
assimetria primária/robustez é o primeiro fato a explicar: por que um
efeito aparece na janela ESTREITA perto da transição mas desaparece
quando diluído na janela completa de ~20 minutos pós-onset?

## Checagem 1 — composição de rótulo (out-of-protocol vs. congelamento) como confundidor de composição

**Preocupação nomeada:** a janela PRE-robustez é uma MISTURA de
atividade "fora de protocolo" (rótulo `0`, 40% da janela, 11.527+3.199
amostras em 2 blocos) e caminhada (rótulo `1`, 60%). A janela
POST-robustez é quase toda caminhada (rótulo `1`, 95,5%) com 9 episódios
de congelamento embutidos (rótulo `2`, 4,5%). Se a atividade "fora de
protocolo" (ex. ajuste de sensor, movimentos aleatórios de instalação)
tiver uma assinatura de LZC sistematicamente DIFERENTE da caminhada
pura, a queda observada poderia ser um artefato de COMPOSIÇÃO (menos
"fora de protocolo" no POST), não um efeito genuíno ligado à transição
de congelamento.

**Teste direto:** `LZC` recomputado (mesmo pipeline, `compute_lzc_channels`,
mediana/tercis reestimados no subconjunto) sobre subconjuntos filtrados
por rótulo, preservando ordem temporal (removendo apenas as amostras do
rótulo indesejado, não uma nova janela):

| Segmento | `n` | `LZC_median` | `LZC_ternary` |
|---|---|---|---|
| PRE robustez completa (mista) | 36.472 | 0,8132 | 0,7472 |
| PRE robustez, só caminhada (rótulo 1) | 21.746 | 0,7613 | 0,6931 |
| POST robustez completa (mista) | 39.521 | 0,6047 | 0,5548 |
| POST robustez, só caminhada (rótulo 1) | 37.727 | 0,5912 | 0,5561 |
| POST robustez, só congelamento (rótulo 2) | 1.794 | 0,9038 | 0,7983 |

**Resultado da checagem:** removendo COMPLETAMENTE a atividade fora de
protocolo do PRE e o congelamento do POST (comparação caminhada-pura
vs. caminhada-pura), a queda **PERSISTE e tem magnitude comparável**
(`LZC_median`: 0,7613→0,5912, Δ=−0,170, vs. Δ=−0,209 na comparação
completa; `LZC_ternary`: 0,6931→0,5561, Δ=−0,137, vs. Δ=−0,192 completa).
**A composição de rótulo NÃO explica o efeito** — não é um artefato de
"menos atividade fora de protocolo/mais congelamento no POST", persiste
mesmo comparando exclusivamente caminhada-com-caminhada. Achado
adicional, notável mas não a explicação principal: os episódios de
congelamento isolados (rótulo 2 puro) têm `LZC` MAIOR, não menor, que a
caminhada (`0,9038`/`0,7983` vs. `~0,76-0,59`/`~0,69-0,56`) — consistente
com a literatura de índice de congelamento (Bächlin et al. 2010): o
tremor característico do congelamento concentra energia numa banda de
3-8Hz que pode parecer MENOS previsível a uma medida como LZC do que o
padrão de marcha suave, mesmo sendo um evento de baixa mobilidade.

## Checagem 2 — glitch de sensor ou saturação exatamente no onset

**Preocupação nomeada:** o próprio dataset documenta "até algumas
centenas de ms de jitter entre a anotação e o evento real" — um
artefato de sensor ou uma anotação com viés temporal poderia produzir
uma queda espúria bem na fronteira.

**Teste direto:** inspeção da série bruta (aceleração vertical do
tornozelo, mg) nas 100 amostras antes e 400 depois do onset (amostra
72.944): nenhum valor repetido/plano suspeito, nenhuma saturação
(valores no range normal do sensor, ±5000mg), fração de diferenças
zero-consecutivas idêntica antes/depois (`0,074` em ambos os lados,
mesmo antes de qualquer subamostragem). **Desvio-padrão da aceleração
SOBE logo após o onset** (`321,9` nas 100 amostras antes → `592,6` nas
400 amostras depois) — o oposto do que um "sensor travado"/glitch
produziria (que tipicamente CONGELA o sinal, reduzindo a variância a
quase zero). Esse aumento de variância COM queda de LZC é exatamente o
padrão esperado de um tremor periódico de alta amplitude (mais energia,
mas mais previsível/repetitivo) — não um artefato de instrumentação.

## Checagem 3 — o efeito é localizado na transição ou é um desvio genérico de sessão?

**Preocupação nomeada:** se o `LZC` estiver simplesmente à deriva ao
longo da sessão (fadiga, adaptação ao protocolo) independentemente de
qualquer evento de congelamento, a "queda" observada seria um artefato
de tendência temporal genérica, não algo ligado à transição
especificamente.

**Teste direto:** PRE-robustez e POST-robustez cada um dividido em 2
metades (quartis da janela combinada de robustez, ~285-309s cada),
`LZC` recomputado em cada quarto separadamente:

| Quarto | Posição relativa ao onset | `n` | `LZC_median` | `LZC_ternary` |
|---|---|---|---|---|
| Q1 | PRE, mais distante do onset | 18.236 | 0,8220 | 0,8041 |
| Q2 | PRE, mais próximo do onset | 18.236 | 0,8072 | 0,7018 |
| Q3 | POST, mais próximo do onset | 19.760 | **0,3965** | 0,6680 |
| Q4 | POST, mais distante do onset | 19.761 | 0,7633 | 0,6269 |

**Resultado da checagem — `LZC_median`:** o valor fica ESTÁVEL dentro
do PRE (`0,822→0,807`, pequena queda gradual) e então **DESPENCA logo
após o onset** (`Q3=0,3965`, bem abaixo de qualquer valor do PRE) e
**RECUPERA parcialmente** no quarto mais distante (`Q4=0,7633`, voltando
perto dos níveis do PRE). Isso é o padrão de um **efeito TRANSIENTE
concentrado bem na transição**, não uma deriva genérica de sessão — uma
deriva genérica produziria uma queda mais ou menos linear/monótona ao
longo dos 4 quartos, não um mergulho abrupto seguido de recuperação.
Esse padrão explica DIRETAMENTE por que a variante ROBUSTEZ (janela
estreita, captura o mergulho) é significativa enquanto a PRIMÁRIA
(janela completa de ~20min pós-onset, incluindo 17 episódios
subsequentes e muita caminhada normal que dilui o mergulho transiente
numa média) não é.

**`LZC_ternary`:** o padrão é mais suave — já mostra um declínio
DENTRO do próprio PRE (`Q1=0,804→Q2=0,702`, uma queda que começa ANTES
do onset rotulado), continuando a cair no POST (`Q3=0,668→Q4=0,627`).
Isto é reportado honestamente como um padrão DIFERENTE do canal
mediano — mais consistente com uma tendência já em curso ao se
aproximar do primeiro episódio de congelamento (fenômeno pródromo de
mudança de marcha pré-congelamento, também documentado na literatura de
FoG) do que com um mergulho abrupto exatamente no onset. Não invalida o
achado (o teste de significância primário usa a janela completa PRE vs.
POST robustez, não este recorte por quartos, que é só diagnóstico), mas
é uma nuance de interpretação que difere entre os dois canais e é
relatada aqui sem forçar os dois a contarem a mesma história.

## Veredito honesto desta checagem

Nenhuma das duas explicações espúrias mais óbvias e verificáveis dentro
desta sessão (confundidor de composição de rótulo; glitch/saturação de
sensor no onset) sobrevive ao teste direto — ambas são **refutadas**
pelos dados. O padrão temporal fino (checagem 3) é **consistente com um
efeito genuíno e localizado**, fisiologicamente plausível à luz da
literatura de índice de congelamento de Bächlin et al. 2010 (tremor de
alta frequência/baixa complexidade concentrado nos instantes após o
início do congelamento). **Isto não é o mesmo que "achado
cross-domain confirmado"** — é um achado de UM sujeito, UM registro
(`S01R01`), UMA transição (o primeiro onset de congelamento da sessão),
sem nenhuma replicação através de sujeitos ou registros dentro desta
rodada (a Fase 0.7/`METHODOLOGY_NOTE.md` já nomeava `S01R01` como o
único registro inspecionado desta linha, por desenho, não por seleção
pós-resultado). A reexecução adversarial independente por um segundo
agente (passo 7 de `AGENTS.md`) permanece pendente, como em todas as
notas anteriores desta linha.

## Nenhuma ação de redesenho tomada

Nenhuma decisão de `METHODOLOGY_NOTE.md`, `R_lambda`, `I(X)`, ou
protocolo de significância foi alterada em resposta a este achado —
esta checagem é puramente diagnóstica/explicativa, não uma correção de
metodologia. O resultado numérico já reportado (`p=0,0` em ambos os
canais, variante robustez) permanece exatamente como calculado pelo
pipeline LOCKED.
