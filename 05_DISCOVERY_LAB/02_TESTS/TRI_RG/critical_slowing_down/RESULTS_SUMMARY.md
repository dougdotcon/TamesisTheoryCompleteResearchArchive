# Resultado do fechamento dos 3 gaps — `critical-slowing-down`

**Data:** 2026-08-14. Metodologia fixada e commitada em `METHODOLOGY_NOTE.md`
(commit `b43fde0`) ANTES de qualquer cálculo real — ver esse arquivo para a
regra de `lambda`, definição de segmento e protocolo de nulo substituto.
Pipeline única (`analysis/csd_common.py`) chamada sem modificação nos 3
domínios, por 3 agentes independentes (um por domínio), cada um proibido
de editar a pipeline. `git diff` confirmado limpo em `csd_common.py` pelos
3 agentes.

## Tabela completa (3 domínios × 2 variantes × 2 canais = 12 testes)

| Domínio | Variante | n | τ AC1 | p AC1 (unicaudal) | τ Var | p Var (unicaudal) |
|---|---|---|---|---|---|---|
| GISP2 (paleoclima) | Primária | 764 | +0,218 | 0,398 | −0,366 | 0,718 |
| GISP2 (paleoclima) | Robustez | 382 | **+0,848** | **0,032** | +0,804 | 0,058 |
| PhysioNet SDDB (cardíaco) | Primária | 35.382 | **−0,820** | 0,985 | +0,273 | 0,361 |
| PhysioNet SDDB (cardíaco) | Robustez | 17.691 | **−0,947** | 1,000 | +0,580 | 0,158 |
| NASDAQ (financeiro) | Primária | 7.351 | −0,372 | 1,000 | −0,218 | 1,000 |
| NASDAQ (financeiro) | Robustez | 3.675 | +0,627 | 0,851 | +0,547 | 1,000* |

\* canal de variância no NASDAQ sofre um "efeito teto" documentado pelo
agente: o coeficiente AR(1) ajustado ficou ligeiramente > 1 (processo
tecnicamente explosivo, `a≈1,0010`/`1,0018`) porque `log(NASDAQCOM)` é
quase um passeio aleatório puro — quase 100% dos 1000 substitutos geram
`τ=1,000` (desvio-padrão ~1e-16), tornando esse canal específico pouco
discriminante para este domínio. Não é um bug da pipeline nem foi
"corrigido" — reportado como está.

## Interpretação honesta — sem sinal robusto de cross-domain

Das **12 combinações** testadas (3 domínios × 2 variantes × 2 canais),
apenas **1** cruzou o limiar convencional de significância unicaudal
`p<0,05` (GISP2, variante robustez, canal AC1: `p=0,032`) — e mesmo esse
domínio teve seu canal companheiro de variância apenas marginal
(`p=0,058`, acima do limiar) e sua variante primária inteiramente
não-significativa. Com 12 testes unicaudais e nenhuma correção para
comparações múltiplas, o número ESPERADO de falsos positivos ao acaso sob
"nenhum efeito real em lugar nenhum" é `12×0,05=0,6` — encontrar
exatamente 1 resultado abaixo de 0,05 é inteiramente consistente com puro
acaso, não evidência de um efeito real.

Mais grave ainda: em **2 dos 3 domínios** (PhysioNet SDDB e NASDAQ
primária), o canal de AC1 — o canal mais diretamente ligado à teoria de
CSD (autovalor dominante → 0 perto de bifurcação) — mostrou tendência
FORTEMENTE NEGATIVA (`τ=−0,82`, `τ=−0,95`, `τ=−0,37`), o OPOSTO da
direção prevista por critical slowing down. Isso não é "sinal fraco" ou
"amostra insuficiente" — é uma tendência clara na direção errada.

**Veredito honesto:** aplicando a metodologia fixada a priori (a mesma
regra de `lambda`, a mesma pipeline, o mesmo protocolo de nulo
substituto, sem nenhum ajuste por domínio) aos 3 domínios que a Fase 0
havia verificado como tendo dado real e rótulo de transição real, o
candidato `critical-slowing-down`, COMO FORMULADO E TESTADO AQUI, **não
mostra um sinal cross-domain robusto**. O único resultado nominalmente
significativo (GISP2/robustez/AC1) é estatisticamente consistente com
ruído sob múltiplas comparações, e é contradito pela direção oposta
observada nos outros dois domínios.

**O que isso NÃO significa:** não significa que critical slowing down
como fenômeno geral é falso — a literatura (Scheffer 2009, Dakos
2008/2012, Lenton 2012) documenta o efeito de forma robusta em muitos
sistemas, usando frequentemente janelas de observação escolhidas com
conhecimento específico de cada sistema (ex. a extensão exata do
"período estável antes da transição" segundo cada estudo original), não
uma regra cega de fração-do-registro-disponível como a fixada aqui. O que
este resultado mostra é que a versão ESPECÍFICA e cega deste candidato —
com a regra de `lambda` genuinamente domain-agnostic exigida por
`DISC-TRI-RG-001` (nenhum conhecimento específico de cada sistema para
escolher a janela) — não produz um invariante cross-domain confiável
nestes 3 domínios e nestas 2 transições/variantes. Essa é precisamente a
pergunta que `DISC-TRI-RG-001` propôs testar, e a resposta honesta, com
este desenho, é negativa.

## Recomendação

Não travar um `PREREGISTRATION.md` para `critical-slowing-down` como
formulado — o próprio passo de fechamento de gaps já revelou que ele não
sobrevive ao teste cross-domain com uma regra verdadeiramente cega. Duas
rotas honestas seguintes, nenhuma travada ainda:

1. Considerar o candidato `wavelet-multiresolution-scaling` (rank 2 na
   síntese da Fase 0) — mas ele hoje só tem 1 domínio robusto
   (sismologia/Tohoku); precisaria de um segundo domínio limpo antes de
   qualquer teste equivalente a este.
2. Reformular `dfa-multiscale-entropy` (rank 3) em torno de uma transição
   temporal genuína dentro do mesmo sujeito/sistema, em vez da comparação
   estática de classe usada na Fase 0.
3. Nova rodada de busca por candidatos ainda não considerados.
