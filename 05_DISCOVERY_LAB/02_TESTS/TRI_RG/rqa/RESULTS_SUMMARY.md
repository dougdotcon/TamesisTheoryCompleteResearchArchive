# Resultado do fechamento dos gaps — `RQA` (Análise de Quantificação de Recorrência)

**Data:** 2026-08-18. Metodologia fixada em `METHODOLOGY_NOTE.md` (commit
`fa3edba`) — regras de parâmetro não-arbitrárias e publicadas (FNN para
`m`, informação mútua para `tau`, taxa de recorrência fixa para
`epsilon`), embedding compartilhado PRE/POST, `I(X)=%DET+ENTR`,
substitutos IAAFT como teste PRIMÁRIO — fixada ANTES de qualquer cálculo
real. **Este candidato foi fechado inteiramente na etapa de validação
sintética — nenhum dado real (rolamento IMS/Rexnord, sismologia vulcânica
de Kīlauea) foi tocado em nenhum momento.**

## Validação, tentativa 1 — controle positivo exato do Gap (b) (PRE=ruído branco)

A validação sintética obrigatória (`analysis/validate_synthetic.py`,
commit `2a1214b`, `VALIDATION_NOTE.md`) revelou um achado estrutural mais
fundamental que o de `grafo-de-visibilidade` — porque bloqueia os DOIS
canais de `I(X)` simultaneamente, não apenas um: Falsos Vizinhos Mais
Próximos (FNN, Kennel, Brown & Abarbanel 1992) NUNCA resolve `m<=10` para
ruído branco Gaussiano iid — o PRE exato especificado no Gap (b). Como
`(m,tau)` é compartilhado entre `%DET` e `ENTR` (Gap a), essa falha
bloqueia ambos os canais ao mesmo tempo, impedindo qualquer cálculo.

**Não é bug** (diagnóstico com onda senoidal determinística confirma o
código de embedding/recorrência/`%DET`/`ENTR` correto — `%DET=0,9994`
quando a grade é atingível) **nem falta de poder estatístico do IAAFT**
(bootstrap por blocos móveis testado explicitamente, 0/25 reamostras
resolveram o embedding — confirma parede estrutural, não problema de
poder). Caracterização robusta da fronteira de resolubilidade: FNN só
resolve a partir de `H(fGn)>=0,3` ou `AR(1) phi>=0,95` — ruído branco
puro e processos linearmente fracos ficam sempre fora, independente de
`N` até o teto de 5.000 do Gap (d).

O controle negativo (dois sorteios independentes de fGn-like `H=0,7`, que
RESOLVE o embedding) confirmou que o pipeline funciona corretamente
quando a etapa de embedding é computável: `p_DET=0,77`, `p_ENTR=0,70`,
ambos corretamente não-significativos.

## Adendo — redesenho do controle positivo (fixado ANTES de dado real)

Uma tentativa informal (PRE=fGn `H=0,7`, POST=mapa logístico remapeado
por posto) foi corretamente descartada pelo próprio agente de validação:
o mapa logístico tem espectro naturalmente banda-larga/quase-branco,
então remapear sua ordem sobre a marginal colorida do fGn não preserva o
casamento de espectro que o desenho exige — o IAAFT reproduziu esse
descasamento não controlado, mascarando qualquer sinal (`p=1,0` na
checagem informal, nunca formalizada).

**Correção formal, commitada ANTES de qualquer dado real (commit
`024e7a9`), com protocolo de decisão pré-fixado:** trocar a fonte
caótica de POST do mapa logístico para o sistema de Rössler (espectro
colorido/banda-limitada, mais compatível com o PRE `fGn H=0,7` já
validado). Se qualquer canal mostrasse poder real, a validação passaria
e o dado real seria tocado; se nenhum mostrasse, o candidato seria
fechado ali mesmo — decisão mecânica, sem terceira tentativa.

## Validação, tentativa 2 — controle positivo com Rössler (commit `9b0bdde`)

Embedding resolveu desta vez (`m=4, tau=40`), confirmando que a correção
de compatibilidade espectral funcionou nesse nível. Casamento espectral
bom: expoente do PRE=2,373, do Rössler bruto=2,397 (contra alvo teórico
do fGn `H=0,7`=2,4), do POST pós-remapeamento=1,958 (bom, não perfeito,
reportado honestamente).

**Resultado: `p_DET=1,0`, `p_ENTR=1,0`** — o resultado bicaudal menos
significativo possível (o `Delta` real ficou MENOR em magnitude que
quase todos os 200 substitutos, nos dois canais). Note-se um detalhe
técnico honesto: os "desvios-padrão equivalentes" calculados (~8,9 para
`DET`, ~2,8 para `ENTR`) parecem grandes isoladamente, mas isso reflete
uma distribuição nula estreita e deslocada da origem — não contradiz
`p=1,0`, já que o critério de decisão pré-fixado é o `p` bicaudal por
magnitude, não a distância à média da nula.

Aplicando o protocolo de decisão mecanicamente, exatamente como
pré-fixado antes de ver este resultado: `any_channel_shows_power=false`
→ **`VALIDATION_FAILED_CLOSE_AT_VALIDATION_STAGE_NO_THIRD_ATTEMPT`**.

## Veredito honesto

`RQA`, sob a convenção de embedding travada a priori (`R_tol=10`,
`A_tol=2`, `m<=10`, `RR_target=0,05`), **não teve sua identificabilidade
estabelecida em nenhum dos dois desenhos de controle positivo tentados**
— nem o especificado originalmente (ruído branco, que sequer resolve
embedding) nem a correção subsequente (Rössler, que resolve embedding mas
não mostra poder estatístico real contra o IAAFT). Por decisão pré-fixada
antes de qualquer um dos dois resultados, nenhuma terceira tentativa foi
feita e o candidato é fechado AQUI, na etapa de validação — um resultado
honesto e completo, distinto de "negativo no dado real" (que nunca chegou
a ser tocado) mas igualmente definitivo para os propósitos desta linha:
esta instanciação específica de RQA (regras de parâmetro publicadas,
canais `%DET`/`ENTR`, protocolo IAAFT) não é uma ferramenta utilizável
para esta busca de invariante cross-domain, sob as convenções travadas.

Isso não invalida RQA como ferramenta estabelecida na literatura de
dinâmica não-linear (é amplamente usada com sucesso em contextos onde o
sinal de entrada já tem estrutura suficiente para resolver embedding,
como os próprios domínios-alvo desta busca provavelmente teriam) — mostra
apenas que a validação de identificabilidade EXIGIDA por esta linha antes
de qualquer dado real (`METHODOLOGY_EXTENSIONS.md` Seção 1) não pôde ser
cumprida com o orçamento de tentativas de desenho disciplinadamente
autorizado aqui.

## Estado da linha — 7 de 7 candidatos identificados agora com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| `mse-multiscale-entropy` | Geomagnetismo (1989), rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |
| `grafo-de-visibilidade` | Geomagnetismo (2015), hidrologia/Harvey | NEGATIVO (sem achado em nenhum domínio; `d_B` estruturalmente não testável) |
| `RQA` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |

Todos os 7 candidatos identificados na linha `DISC-TRI-RG-001` (3 da Fase
0 original + 4 da nova busca de 2026-08-15) agora têm resultado
completo: 6 testados em dado real, todos NEGATIVO (2 com achados
isolados de 1 domínio já explicados por mecanismo convencional/nulo); 1
(`RQA`) fechado na própria etapa de validação, sem alcançar dado real.
Nenhum `PREREGISTRATION.md` foi escrito para nenhum dos 7, seguindo o
mesmo padrão de fechamento exploratório de gaps usado consistentemente
nesta linha.
