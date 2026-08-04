---
document_id: FOUND-MONOVARIANT-DESCENT-001-README
work_item_id: FOUND-MONOVARIANT-DESCENT-001
specification_status: READY_FOR_REVIEW
research_role: FORMAL_PROOF_TOOL
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# FOUND-MONOVARIANT-DESCENT-001

## A segunda metade do par

```text
invariante    quantidade CONSERVADA   prova impossibilidade
monovariante  quantidade DECRESCENTE  prova ausencia de recorrencia
```

Ter uma sem a outra é ter meia ferramenta.

## A escolha de `Nat`

A medida tem valores em `Nat`, não numa ordem geral. Boa fundação vem de
graça, **zero typeclasses** são exigidas, e o resultado é o monovariante
clássico. Ordens gerais, `WellFoundedRelation` e ordinais ficam
**NÃO AUTORIZADOS**.

## O negativo, que é mais forte que o da frente anterior

```text
invariante     OrbitSeparating vale EXATAMENTE nos pontos fixos
monovariante   OrbitSeparating NAO VALE EM LUGAR NENHUM
```

Um monovariante exclui recorrência concreta em qualquer número positivo
de passos. A análise abstrata **sempre** devolve ciclo com período
positivo. Logo **todo ciclo abstrato de um sistema monovariante é
espúrio**, sem exceção.

## A lacuna de API que a frente fecha

`detectCycle?_sound` prova `0 < period`. `analyzeTransitionTable_sound`
devolve três cláusulas e **perde** a positividade antes de chegar ao
consumidor. A frente recupera, re-derivando a redução em namespace novo
com API exclusivamente pública — **sem tocar em frente encerrada**.

É o que torna o negativo livre de hipótese inventada.

## O que a frente NÃO entrega

```text
monovariante NAO e necessario para ausencia de ciclo
boa fundacao NAO basta: k - 1 falha em zero
nenhuma terminacao de programa
nenhum ordinal
nenhum problema de milenio
```
