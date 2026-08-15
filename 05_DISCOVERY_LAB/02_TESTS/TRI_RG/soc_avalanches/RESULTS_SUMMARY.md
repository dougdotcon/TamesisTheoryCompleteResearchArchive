# Resultado do fechamento dos gaps — `soc-avalanches`

**Data:** 2026-08-15. Metodologia fixada em `METHODOLOGY_NOTE.md` (commits
`eda7ae4`, `c7cea2e` — o segundo é um adendo pós-validação-sintética) e
pipeline (`analysis/soc_common.py`, binagem por intervalo médio entre
eventos + extração de avalanches + MLE discreta de lei de potência +
substituto Poisson + bootstrap pareado de `tau`) validada contra dado
sintético (commit `6c4e188`) ANTES de qualquer cálculo real. Aplicada sem
modificação aos 2 domínios (sismicidade de Ridgecrest 2019, flares
solares GOES/ciclo 24), com checagem adversarial completa no domínio que
mostrou divergência entre os testes primário e secundário.

## Domínio 1 — Sismicidade (Ridgecrest 2019, API FDSN do USGS)

| Variante | tau PRE | tau POST | Δtau | p (Poisson, secundário) | p (bootstrap, PRIMÁRIO) |
|---|---|---|---|---|---|
| Primária | indefinido (só 9 avalanches) | — | — | — | — |
| Robustez | 4,090 | 2,358 | −1,733 | 0,32 (não sig.) | **0,0** (sig.) |

A variante primária falhou por completo — o segmento PRE (35h entre o
pré-choque M6,4 e o mainshock M7,1) produziu só 9 avalanches, abaixo do
mínimo para ajuste MLE confiável. A variante de robustez mostrou
divergência entre os dois testes de significância: o teste primário
(bootstrap pareado) deu significativo, o secundário (substituto Poisson)
não — exatamente o tipo de sinal de alerta que já apareceu antes nesta
linha (DFA/apneia-ECG teve a mesma divergência num canal).

## Reexecução adversarial — domínio 1 (decisiva)

**Reprodução cega independente:** números batem essencialmente exatos
(≥12 dígitos significativos) — não é bug de implementação.

**Confundidor identificado desde a extração original:** o segmento PRE
não é uma linha de base quiescente — é a sequência de réplicas do PRÓPRIO
pré-choque M6,4 (taxa de eventos `mu_pre=0,0144 ev/s`, MAIOR que a taxa
média do POST no período completo, `mu_post=0,00266 ev/s`).

**Nulo ETAS subcrítico (escalada condicional já pré-declarada na
metodologia, acionada pelo `p_bootstrap_tau=0,0`):** ETAS de ramificação
subcrítica (Ogata 1988, kernel de Omori-Utsu `p=1,1`) ajustado
separadamente a PRE (`n=0,391`) e POST (`n=0,999`, satura no limite
subcrítico), 300 simulações pareadas rodadas pela mesma pipeline.
**`p_ETAS_tau=0,273` — NÃO significativo.** O `Delta_tau` real fica a
apenas ~1 desvio-padrão da distribuição nula ETAS. **O achado não
sobrevive a um nulo que já incorpora a física conhecida de sequências de
réplicas.**

**Checagem com linha de base genuinamente quiescente** (60 dias antes do
M6,4, mesma caixa geográfica, sismicidade de fundo isolada): o efeito
persiste no teste bootstrap (`p=0,0`) mesmo com o confundidor do M6,4
removido — mas isso é exatamente o esperado do próprio mecanismo mundano
(sismicidade de fundo isolada vs. sequência de réplicas densa têm
estatísticas de avalanche/ramificação estruturalmente diferentes por
Omori-Utsu, não por SOC/invariante novo), consistente com o veredito do
nulo ETAS, não uma contradição dele.

**Descoberta adversarial de nulos — achado decisivo e independente:**
dividindo a janela POST (só a sequência de réplicas do M7,1, SEM nenhuma
comparação com o PRE) em uma sub-janela inicial (mesma duração do PRE,
taxa local alta) e uma tardia (taxa local baixa), o MESMO efeito
"significativo" reaparece — `tau=2,50` (inicial) → `tau=3,51` (tardia),
`p_bootstrap_tau=0,0` — dentro de UM ÚNICO regime homogêneo, sem qualquer
transição real envolvida. Varredura sistemática de 10 blocos por toda a
janela POST de 60 dias mostra `tau` acompanhando a taxa local de eventos
(`r=-0,53`, decaimento clássico de Omori-Utsu, confirmado contra a
literatura sismológica). Desequilíbrio de tamanho de amostra
(9x mais avalanches na cauda do POST que do PRE) testado e explicitamente
REJEITADO como causa isolada (subamostrar POST ao tamanho do PRE reproduz
o `tau` do próprio POST, não do PRE, em 0 de 2000 reamostras).

**Veredito: o achado NÃO sobrevive.** Reduz-se a decaimento de Omori-Utsu
já conhecido interagindo mecanicamente com o método de binagem de
`lambda` fixo — não é um sinal SOC/cross-domain novo. O sinal só parecia
significativo contra o teste bootstrap não-paramétrico (que não modela
nenhuma estrutura de clustering/ramificação); some por completo contra um
nulo que já incorpora a física de réplicas conhecida.

## Domínio 2 — Flares solares (GOES XRS, fase de declínio do ciclo 24, 2014→2017, instrumento único GOES-15)

| Variante | tau PRE | tau POST | Δtau | p (Poisson, secundário) | p (bootstrap, PRIMÁRIO) |
|---|---|---|---|---|---|
| Primária | 3,126 | 2,671 | −0,455 | 0,875 | 0,288 |
| Robustez | 2,290 | 2,633 | +0,343 | 0,888 | 0,216 |

**Sem sinal em nenhuma variante** — nenhum teste (primário ou secundário)
atinge `p<0,05` em nenhuma variante, e a direção de `Delta_tau` até
INVERTE de sinal entre primária e robustez (e entre as sub-variantes de
sensibilidade de `lambda`). PRE ficou com amostra relativamente fina
(~3 meses, 625 eventos) dado que a janela homogênea de instrumento único
disponível deixava pouco espaço antes do máximo do ciclo — declarado como
limitação honesta, não escondida.

## Veredito honesto

`soc-avalanches`, como formulado e testado aqui (mesma pipeline `I(X)`
= `tau` via MLE + `sigma`, sem reformulação por domínio, aplicada a 2
domínios físicos distintos), **não produz um invariante cross-domain
confiável** — mesmo veredito já obtido para `critical-slowing-down`,
`wavelet-multiresolution-scaling` e `dfa-multiscale-entropy`, os 4
candidatos agora testados com rigor completo nesta linha (3 da Fase 0
original + 1 da nova rodada de busca). O achado inicialmente promissor em
sismologia foi decisivamente refutado por um nulo que já incorpora a
física de réplicas conhecida (ETAS subcrítico) e por uma descoberta
adversarial independente que reproduziu o mesmo "efeito" dentro de um
único regime homogêneo. Flares solares não mostrou sinal em nenhuma
variante. Nenhum `PREREGISTRATION.md` foi escrito.

Isto não invalida a criticalidade auto-organizada como fenômeno geral —
apenas mostra que esta instanciação específica cross-domain (binagem por
intervalo médio entre eventos, ajuste MLE de `tau`, comparação PRE/POST
via bootstrap pareado, sem reformulação por domínio) não sobrevive nestes
2 domínios testados com protocolo genuinamente cego ao domínio e checagem
adversarial completa.

## Estado da linha — 4 dos 6 candidatos novos/antigos com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |

Restam 3 candidatos da nova busca ainda não fechados: MSE (rank #2), grafo
de visibilidade (rank #3), RQA (rank #4) — ver
`phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`.

## Recomendação (não travada)

Toda a infraestrutura desta rodada (metodologia, pipeline validada, dados
reais de Ridgecrest/GOES, resultados adversariais completos) fica
commitada e reaproveitável. Próxima decisão fica com o usuário: fechar
gaps de outro candidato da nova busca (MSE tem a fundamentação formal mais
rigorosa, mas risco de redundância com Hurst; RQA já mostrou sinal de
alerta empírico de inconsistência cross-domain), nova busca adicional, ou
considerar a linha suficientemente explorada por ora.
