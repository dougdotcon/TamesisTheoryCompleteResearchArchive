# Resultado do fechamento dos gaps — `homologia-persistente` (TDA via Vietoris-Rips)

**Status: FECHADO NA ETAPA DE VALIDAÇÃO — dado real (LIGO GW150914,
S&P500/Lehman) NUNCA TOCADO.** Metodologia fixada em
`METHODOLOGY_NOTE.md` (commit `2121de0`) ANTES de qualquer cálculo
real: embedding de Takens com `m=3` FIXO (deliberadamente diferente da
regra de FNN do RQA, que já havia falhado estruturalmente para ruído
branco), desenho de sub-janelas (`N_WINDOW=200`, até 10 por segmento)
diretamente motivado pelo custo computacional já MEDIDO na Fase 0.6,
`I(X)`=persistência máxima de H1 (primário) + persistência total
(companheiro), protocolo IAAFT.

## Diagnóstico de correção de código

Passou de forma limpa: onda senoidal determinística (`m=3`,
período 50) traça um laço inequívoco em espaço de fase —
`median_max_persistence=1,476`, `median_total_persistence=1,481`,
quase idênticos entre as 4 sub-janelas (dispersão ~`3×10⁻⁶`, na escala
do próprio *dither* numérico) — confirma que a pipeline de
embedding/sub-janela/Rips/extração de persistência está correta.

## Validação sintética — achado decisivo

**Controle negativo** (fGn `H=0,7` independente): corretamente não-
significativo nos dois canais, IAAFT E bootstrap (`p=0,645`/`0,500`
IAAFT).

**Controle positivo** (ruído branco PRE vs. mapa logístico `r=4`
remapeado por posto POST — mesma técnica já usada com sucesso em
MSE/VG/RQA/entropia-de-permutação): **os DOIS canais mostraram
`IAAFT_LOW_POWER`** — `median_max_persistence`: `p=0,355`,
`sigma≈-0,85`; `median_total_persistence`: `p=0,320`, `sigma≈+0,99`.

**O fallback de bootstrap por blocos móveis pré-autorizado (Kunsch
1989), acionado automaticamente pelo baixo poder do IAAFT, TAMBÉM não
mostrou poder** em nenhum canal: `p=0,454` (máxima), `p=0,368` (total).

## Resposta à pergunta central desta rodada (Gap c de `METHODOLOGY_NOTE.md`)

A Fase 0.6 já havia medido, informalmente (senoide ruidosa, 9 níveis de
ruído), uma correlação de `r≈0,92` entre persistência máxima de H1 e
um análogo do `%DET`(RQA) no regime de degradação de estrutura mais
relevante para detectar transição — um risco de identificabilidade
CONCRETO, não hipotético. **A validação rigorosa aqui confirma que esse
risco era substantivo:** a homologia persistente, sob este desenho, NÃO
mostra poder discriminativo real além do que um substituto de espectro
casado já produziria — a mesma falta de poder que o `%DET`(RQA) já
tinha mostrado (quando computável, no redesenho de Rössler, `p=1,0`).

**Mecanismo DIFERENTE de como o RQA falhou, resultado FINAL igual:** o
RQA fechou porque o embedding compartilhado (FNN) nunca RESOLVIA para
ruído branco — `%DET`/`ENTR` nem chegavam a ser calculados. Aqui, o
embedding com `m=3` fixo resolveu perfeitamente em TODAS as ~1.200
séries (reais, substitutas, reamostras de bootstrap) — zero falhas de
`tau`. O problema não é de resolução de embedding; é que a própria
estatística de persistência (máxima ou total) simplesmente não separa o
sinal caótico genuíno do ruído colorido de espectro casado, sob este
desenho de sub-janelas. É um achado de PODER estatístico genuíno sobre
uma estatística corretamente computada e calibrada — não uma parede
estrutural de não-computabilidade.

## Decisão de fechamento

`METHODOLOGY_NOTE.md` pré-autorizava exatamente UM fallback (bootstrap
por blocos móveis) para o padrão de baixo poder — já testado, também
sem poder. Nenhuma terceira tentativa de redesenho foi autorizada.
Seguindo a mesma disciplina já usada para `RQA` (fechado na validação
após duas tentativas de controle positivo falharem): **`homologia-
persistente` é fechada AQUI, na etapa de validação — o dado real (LIGO
GW150914, S&P500/Lehman) nunca foi tocado.**

## Veredito honesto

`homologia-persistente`, sob a convenção de embedding e desenho de
sub-janelas travados a priori (`m=3`, `N_WINDOW=200`,
`K_SUBWINDOWS_MAX=10`, `I(X)`=persistência máxima/total de H1), **não
teve sua identificabilidade estabelecida em nenhum dos dois canais
declarados, mesmo após o fallback pré-autorizado.** Isso não invalida a
homologia persistente como ferramenta matemática (é bem estabelecida na
literatura de análise topológica de dados, com precedente direto e
publicado de detecção de transição de regime — Gidea & Katz 2018) —
mostra apenas que, sob os parâmetros de custo-tratável fixados aqui
(diretamente motivados pelo custo computacional real medido), a
persistência de H1 não separa estrutura caótica genuína de ruído linear
com o mesmo espectro, na mesma medida que o `%DET` do RQA também não
conseguiu.

**Isto fecha os 4 de 4 candidatos formalizados (`viable=true`) da Fase
0.6** — nenhum produziu invariante cross-domain sobrevivente. Isto é o
**11º e último candidato identificado** na linha `DISC-TRI-RG-001` a
terminar sem produzir um achado cross-domain sobrevivente (2 fechados
na etapa de validação — RQA e este —, 9 testados até o dado real, todos
negativos ou estruturalmente não-testáveis).

## Arquivos desta etapa

- `analysis/ph_common.py` (pipeline)
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`
  (validação sintética completa)
- `VALIDATION_NOTE.md` (relato honesto completo, incluindo o veredito de
  fechamento)
- `METHODOLOGY_NOTE.md` (metodologia travada antes de qualquer cálculo)

## Estado da linha e próximo passo

`TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md` serão atualizados pela
sessão orquestradora, não por este agente — mesmo padrão já usado para
os candidatos anteriores desta linha. Nenhuma reexecução adversarial é
necessária (nenhum achado positivo a explicar — validação negativa em
ambos os canais e ambos os testes de significância). Isto encerra a
Fase 0.6 completa (4/4 candidatos fechados) e, com ela, os 11 candidatos
identificados até agora nesta linha desde sua criação.
