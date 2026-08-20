# Resultado do fechamento dos gaps — `largest_lyapunov_exponent` (Maior Expoente de Lyapunov, algoritmo de Rosenstein)

**Data:** 2026-08-20. Metodologia fixada em `METHODOLOGY_NOTE.md` — gate de
FNN obrigatório e não-negociável (`R_tol=10`, `A_tol=2`, `m<=10`, REJEITE
duro sem fallback forçado), embedding compartilhado PRE/POST reaproveitado
de `rqa_common.py`, janela de Theiler via período orbital médio (convenção
de Rosenstein et al. 1993, distinta da convenção `w=tau` do RQA), curva de
divergência + critério de convergência de Kantz-Schreiber (2004) para a
região de ajuste linear, `I(X) = lambda_1` (primário) + `D2` (companheiro),
substitutos IAAFT como teste PRIMÁRIO de significância — fixada ANTES de
qualquer cálculo real. **Este candidato foi fechado inteiramente na etapa
de validação sintética — nenhum dado real (Kīlauea 2018, início explosivo
de 17/05; MIT-BIH `afdb` registro `04936`) foi tocado em nenhum momento.**

## Por que este resultado não é surpresa — o risco já estava nomeado a priori

A própria sondagem que identificou este candidato
(`phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md` seção 2) já nomeou, ANTES de
qualquer cálculo, que este candidato reusa a MESMA maquinaria de embedding
(FNN, informação mútua) que já havia travado `RQA` estruturalmente na etapa
de validação — e que o modo de falha aqui seria potencialmente PIOR
(inclinação bruta de Rosenstein não falha de forma limpa em ruído,
diferente do `NOT_COMPUTABLE` honesto de `%DET`/`ENTR`). Por isso
`METHODOLOGY_NOTE.md` exigiu, desde o início, um gate de FNN como REJEITE
duro e obrigatório, e uma validação sintética de duas etapas mirando
exatamente o desenho já auditado de `RQA`.

## Validação, tentativa 1 — controle positivo exato (PRE=ruído branco)

A validação sintética obrigatória (`analysis/validate_synthetic.py`,
`VALIDATION_NOTE.md`) confirmou (não apenas repetiu por suposição) que o
MESMO achado estrutural de `RQA` se reproduz aqui: Falsos Vizinhos Mais
Próximos NUNCA resolve `m<=10` para ruído branco Gaussiano iid — a curva de
fração de FNN obtida (`99,6%` em `m=1` até um mínimo de `17,9%` em `m=4`,
voltando a subir até `53,1%` em `m=10`) é praticamente idêntica à já
observada por RQA. Como `(m,tau)` é compartilhado entre `lambda_1` e `D2`,
a falha bloqueia AMBOS os canais simultaneamente.

**Não é bug** — dois diagnósticos de correção de código confirmaram a
pipeline antes de qualquer controle estocástico: (a) mapa logístico com
embedding FORÇADO (`m=2,tau=1`, contornando o gate só para este teste)
recuperou `lambda_1=0,563` contra o teórico `ln(2)=0,693` — mesma ordem de
grandeza e sinal corretos; (b) onda senoidal com dither, pipeline completa
(gate de FNN ativo, sem forçar `m`), resolveu embedding normalmente
(`tau=5,m=4`), `D2=0,967` (correto, perto de 1,0 para uma órbita periódica
1-D), e `lambda_1` corretamente encontrou NENHUMA região de crescimento
exponencial (comportamento correto para um sinal sem expoente de Lyapunov
genuíno positivo, não uma falha). **Nem falta de poder do IAAFT** — bootstrap
por blocos móveis testado explicitamente no ruído branco, `0/25`
reamostras resolveram o embedding, confirmando parede estrutural, não
problema de poder.

Um achado adicional, descoberto e corrigido DURANTE o diagnóstico de
código (a) — ANTES de qualquer controle de identificabilidade —: a regra
ingênua "maior janela com inclinação estável entre `m*,m*+1,m*+2`" é
insuficiente por si só, porque o platô de saturação de um atrator caótico
limitado é trivialmente "estável" (inclinação ≈0 em todo `m`) e, sendo mais
longo que a região de crescimento genuína, venceria a regra. Corrigido
adicionando um gate conjunto de qualidade de ajuste `R²>=0,95` — refinamento
mecânico da regra automatizada, documentado em `METHODOLOGY_NOTE.md` e
`lle_common.py`, não uma reformulação de hipótese após ver resultado real
ou de controle.

O controle negativo (dois sorteios independentes de fGn-like `H=0,7`, que
RESOLVE o embedding em `m=4,tau=49`) confirmou que a pipeline funciona
corretamente quando a etapa de embedding é computável: `p_lambda1=0,103`,
`p_d2=0,79`, ambos corretamente não-significativos, com `R²` alto
(`0,97`/`1,0`) nas regiões lineares identificadas — não um artefato do gate
de `R²` recém-adicionado.

## Validação, tentativa 2 — redesenho pré-autorizado (Rössler)

Acionado mecanicamente pelo resultado acima (mesmo gatilho exato já usado
por RQA): PRE=fGn-like `H=0,7`, POST=sistema de Rössler rank-remapeado
sobre o PRE. Embedding RESOLVEU desta vez (`m=4,tau=40` — coincidentemente
os MESMOS valores encontrados por RQA para o par PRE/POST equivalente,
esperado dado o mesmo código/técnica de geração). Casamento espectral
razoável (expoente do PRE=2,373, Rössler bruto=2,397, POST pós-remap=1,958).

**Resultado: `p_lambda1=1,0` (o valor bicaudal menos significativo
possível), `p_d2=0,16` (não cruza o limiar `p<0,05`, embora mais próximo
que `lambda_1`, σ-equivalente `≈1,39`).** Ambos os canais classificados
`IAAFT_LOW_POWER`. Aplicando o protocolo de decisão mecanicamente, exatamente
como pré-fixado antes de ver este resultado: `any_channel_shows_power=false`
→ **`VALIDATION_FAILED_CLOSE_AT_VALIDATION_STAGE_NO_THIRD_ATTEMPT`**.

## Veredito honesto

`largest_lyapunov_exponent`, sob a convenção de embedding travada a priori
(gate de FNN obrigatório, janela de Theiler via período orbital médio,
critério de convergência de Kantz-Schreiber com `R²>=0,95`), **não teve sua
identificabilidade estabelecida em nenhum dos dois desenhos de controle
positivo tentados** — nem o especificado originalmente (ruído branco, que
sequer resolve embedding) nem a correção subsequente (Rössler, que resolve
embedding mas não mostra poder estatístico real em nenhum dos dois canais
contra o IAAFT). Por decisão pré-fixada antes de qualquer um dos dois
resultados, nenhuma terceira tentativa foi feita e o candidato é fechado
AQUI, na etapa de validação — honesto e completo, distinto de "negativo no
dado real" (que nunca chegou a ser tocado).

Isso não invalida o Maior Expoente de Lyapunov como ferramenta estabelecida
na literatura de dinâmica não-linear (amplamente usada com sucesso em
contextos onde o sinal de entrada já tem estrutura suficiente para resolver
embedding) — mostra apenas que a validação de identificabilidade EXIGIDA
por esta linha antes de qualquer dado real não pôde ser cumprida com o
orçamento de tentativas de desenho disciplinadamente autorizado aqui, sob
esta instanciação específica de parâmetros travados a priori.

Uma nota honesta adicional, não escondida: diferente de RQA (onde ambos os
canais falharam de forma igualmente extrema no controle v2), aqui `D2`
chegou mais perto do limiar de significância (`p=0,16`) que `lambda_1`
(`p=1,0`) sem cruzá-lo — reportado como um detalhe do resultado, não como
justificativa para uma terceira tentativa (não autorizada pela disciplina
de escalonamento desta linha).

## Arquivos desta etapa

- `METHODOLOGY_NOTE.md` — metodologia travada ANTES de qualquer cálculo,
  incluindo o gate de FNN como REJEITE obrigatório e a regra automatizada
  de região linear (Kantz-Schreiber + gate de `R²`).
- `analysis/lle_common.py` — pipeline canônica (reaproveita `tau`/FNN
  auditados de `rqa/analysis/rqa_common.py` por importação direta, não
  reimplementação; implementa a curva de divergência de Rosenstein, o
  critério de convergência de Kantz-Schreiber vetorizado, `D2`, e o gate
  de REJEITE duro).
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`
  — validação sintética completa (diagnósticos de correção de código,
  controle positivo v1 e v2, controle negativo, caracterização da parede
  estrutural, checagem de bootstrap).
- `VALIDATION_NOTE.md` — nota de validação completa e honesta.
- **Nenhum arquivo de dado real, provenance, ou resultado por domínio foi
  criado** — a linha fechou antes de qualquer necessidade de download.

## Estado da linha — 13 de 13 candidatos identificados agora com resultado completo

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
| `largest_lyapunov_exponent` | — (fechado na validação) | **FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado)** |

## Estado da linha e próximo passo (para a sessão orquestradora)

`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` e `DECISION_LEDGER.yaml` NÃO
foram modificados por este agente (fora do escopo desta tarefa) — ficam a
cargo da sessão orquestradora, que já tem o padrão estabelecido de como
registrar um fechamento na etapa de validação (usado 2x agora nesta linha:
`RQA` e `largest_lyapunov_exponent`, e 1x antes disso em
`persistent_homology`).

Da sondagem `phase0/PHASE0_7_SURVEY_NEW_CANDIDATES.md`, resta 1 candidato
`viable=true` ainda não testado: **DMD / espectro de Koopman** (candidato
3, canal primário revisado para frequência/razão de amortecimento do par
de autovalores complexos menos amortecido). Esse candidato também herda
risco de embedding (Hankel/Takens) — a sondagem já recomendou checagem de
controle positivo ANTES de qualquer dado real, mesmo padrão agora
confirmado necessário 2 vezes consecutivas nesta linha (`RQA`, este
candidato). Nenhuma decisão sobre prosseguir com DMD é tomada aqui — cabe à
sessão orquestradora e/ou ao usuário.
