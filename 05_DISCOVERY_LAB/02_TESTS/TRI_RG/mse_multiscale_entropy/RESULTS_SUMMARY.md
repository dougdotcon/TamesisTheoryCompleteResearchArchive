# Resultado do fechamento dos gaps — `mse-multiscale-entropy`

**Data:** 2026-08-15. Metodologia fixada em `METHODOLOGY_NOTE.md` (commit
`b59d31b`) e pipeline (`analysis/mse_common.py`, coarse-graining de blocos
não sobrepostos + SampEn + `I(X)`=`CI`+`beta` + substitutos IAAFT como
teste PRIMÁRIO) validada contra dado sintético (commit `7f1b147`) ANTES de
qualquer cálculo real. Aplicada sem modificação aos 2 domínios
(geomagnetismo, engenharia mecânica).

## Validação — o teste central de identificabilidade desta linha

Ao contrário do que se descobriu para `alpha` do DFA (IAAFT sem poder
real, exigiu adição de teste de bootstrap por blocos), a validação
sintética confirmou que o IAAFT TEM poder real para `CI`/`beta`: no
controle positivo (PRE=ruído branco, POST=mapa logístico caótico com
marginal/espectro casados por rank-remap), `delta_CI` real ficou a ~19
desvios-padrão da distribuição nula (`p_CI=0,0`, `p_beta=0,0`). Isso
confirma empiricamente que SampEn é sensível a estrutura NÃO-LINEAR que
IAAFT não reproduz — o discriminador de identificabilidade proposto na
`METHODOLOGY_NOTE.md` funciona como esperado, e indiretamente já resolve
parte do risco de redundância com a família Hurst: se `beta`(MSE) fosse
apenas uma reparametrização de `alpha`(DFA)/H, o IAAFT teria o MESMO
problema de baixo poder que já mostrou para `alpha` — não teve.

## Domínio 1 — Geomagnetismo (índice SYM-H, tempestade de março/1989, NASA/SPDF OMNIweb)

| Variante | ΔCI | p_CI (IAAFT, bicaudal) | Δbeta | p_beta (IAAFT, bicaudal) |
|---|---|---|---|---|
| Primária | −11,541 | 0,860 | −0,160 | 0,830 |
| Robustez | −14,389 | 0,875 | −0,241 | 0,275 |

**Sem sinal em nenhuma variante.** `ΔCI` real cai bem dentro da
distribuição nula dos substitutos (médias de substituto −12,68 e −15,41,
muito próximas do `ΔCI` real observado) — a mudança de complexidade
observada é inteiramente consistente com o que um processo linear com o
mesmo espectro/amplitude já produziria.

## Domínio 2 — Engenharia mecânica (rolamento FEMTO/PRONOSTIA `Bearing1_1`, run-to-failure)

| Variante | ΔCI | p_CI (IAAFT, bicaudal) | Δbeta | p_beta (IAAFT, bicaudal) |
|---|---|---|---|---|
| Primária | −1,066 | 1,000 | +0,080 | 0,995 |
| Robustez | −2,859 | 1,000 | +0,098 | 0,160 |

**Sem sinal em nenhuma variante** — `p_CI=1,0` em ambas as variantes,
resultado inequivocamente negativo.

**Desvio metodológico declarado honestamente:** o segmento PRE (7,05
milhões de amostras) tornava o custo de SampEn proibitivo para o
protocolo de 200 substitutos (~60h+ estimadas). Decimado por *stride*
uniforme, fator 200 (`pre[::200]` → 35.266 amostras) — NÃO
block-averaging (que seria uma forma adicional de coarse-graining
sobreposta à própria pipeline). Isso não foi previsto na
`METHODOLOGY_NOTE.md` original. Risco honesto: decimação por stride pode
ter destruído estrutura de correlação de curto alcance relevante para
SampEn em escalas finas — não pode ser descartado que isso tenha
contribuído para o resultado negativo neste domínio especificamente
(diferente do domínio geomagnético, que não precisou de decimação e
também deu negativo).

## Sobre a checagem adversarial

Diferente de `dfa-multiscale-entropy` (achado forte em 1 domínio) e
`soc-avalanches` (divergência primário/secundário em 1 domínio),
`mse-multiscale-entropy` não produziu nenhum achado significativo em
nenhuma das 8 combinações testadas (2 domínios × 2 variantes × 2 canais)
— não há nada a explicar via reexecução adversarial completa ou
descoberta de nulos, e uma reexecução cega completa não foi acionada por
proporcionalidade (mesmo espírito de escalada condicional ao tamanho do
efeito já praticado nesta linha). A checagem de identificabilidade central
(risco de redundância com Hurst) já foi substancialmente resolvida na
própria etapa de validação sintética (ver acima) — o IAAFT não teria tido
poder se `CI`/`beta` fossem redundantes com `alpha`/H.

## Veredito honesto

`mse-multiscale-entropy`, como formulado e testado aqui (mesma pipeline
`I(X)`=`CI`+`beta`, sem reformulação por domínio, aplicada a 2 domínios
físicos distintos), **não produz um invariante cross-domain confiável**
— mesmo veredito já obtido para os outros 4 candidatos desta linha. Ao
contrário de `dfa-multiscale-entropy` e `soc-avalanches`, aqui não houve
sequer um achado inicial promissor em algum domínio isolado — o resultado
é negativo de forma limpa e sem ambiguidade nos 2 domínios. Isso não
invalida MSE como ferramenta (é bem estabelecida na literatura de
fisiologia/complexidade), apenas mostra que esta instanciação cross-domain
específica não sobrevive nestes 2 domínios testados com protocolo
genuinamente cego ao domínio. Nenhum `PREREGISTRATION.md` foi escrito.

## Estado da linha — 5 dos 6 candidatos considerados com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| `mse-multiscale-entropy` | Geomagnetismo, rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |

Resta apenas 1 candidato da nova busca ainda não fechado: grafo de
visibilidade (rank #3) — RQA (rank #4) também não fechado.

## Recomendação (não travada)

Toda a infraestrutura desta rodada (metodologia, pipeline validada, dados
reais de 1989/FEMTO, resultado completo) fica commitada e reaproveitável.
Próxima decisão fica com o usuário: fechar gaps do grafo de visibilidade
ou RQA, nova busca adicional, ou considerar a linha suficientemente
explorada por ora — com 5 dos 6 candidatos já considerados agora
negativos, este último ponto fica cada vez mais defensável.
