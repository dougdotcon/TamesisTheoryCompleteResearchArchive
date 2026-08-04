---
document_id: FOUND-MONOVARIANT-DESCENT-001-RESULT-REVIEW
work_item_id: FOUND-MONOVARIANT-DESCENT-001
review_start_head: 9b773d83b7a72b4199ce9cede09eb4b844a8a131
decision: FOUND_MONOVARIANT_DESCENT_001_RESULT_REVIEW_APPROVED
---

# Revisão de resultado

## Reexecução independente

```text
lake build           exit 0, 8789 jobs, 0 erros reais
contagem derivada    7 publicas (1 def, 6 teoremas), 1 privado, 2 TEST_ONLY
Fintype              0        DecidableEq 0        instancias 0
tokens proibidos     0 em toda a arvore Lean
frentes encerradas   0 arquivos tocados
```

## A força exata

```text
Um monovariante com valores em Nat exclui ponto periodico em qualquer
numero POSITIVO de passos.

A analise abstrata SEMPRE devolve certificado, e o periodo dele e
POSITIVO -- clausula recuperada nesta frente.

Logo um sistema com monovariante NUNCA satisfaz OrbitSeparating:
todo ciclo abstrato dele e espurio.
```

## O par, agora completo

```text
invariante     separa      OrbitSeparating vale nos pontos fixos
monovariante   decresce    OrbitSeparating nao vale em lugar nenhum
```

A frente anterior deu a metade que prova **impossibilidade**. Esta deu a
metade que prova **ausência de recorrência**. As duas medem, de ângulos
opostos, o mesmo limite: abstração entrega observação, não reflexão.

## A cláusula recuperada

`detectCycle?_sound` sempre provou `0 < period`.
`analyzeTransitionTable_sound` devolve três cláusulas e **a perdia**.
Ela está de volta na superfície pública, e a recuperação **não tocou
nenhum arquivo de frente encerrada**: a redução foi reproduzida em
namespace novo a partir de API pública.

Isso é o que torna o teorema negativo livre de hipótese inventada.

## O que **não** foi provado

```text
que monovariante seja NECESSARIO para ausencia de ciclo
que boa fundacao baste sem decrescimo estrito
qualquer cota quantitativa no numero de passos
ordens gerais, ordinais, terminacao de programas
sistemas nao deterministicos
```

`strictDown_not_monovariant` compila com pegada `[propext]` e existe para
que boa fundação nunca seja lida como suficiente: `Nat` é bem fundado e
`k - 1` **não** é monovariante, porque falha em zero.

## Pegada

```text
Monovariant.iterate_lt            propext, Quot.sound
Monovariant.no_periodic_point     propext, Quot.sound
Monovariant.not_reachable_self    propext, Quot.sound
analyzeTransitionTable_period_pos propext, Classical.choice, Quot.sound
analyzeAbstractSystem_period_pos  propext, Classical.choice, Quot.sound
monovariant_not_orbitSeparating   propext, Classical.choice, Quot.sound
strictDown_not_monovariant        propext
```

`Classical.choice` entra **apenas** no que atravessa
`analyzeEncodedSystem` — pegada infraestrutural aceita, cuja remoção é
proibida.

## Os dois defeitos desta frente, registrados

1. **Contagem agregada errada na especificação**: `13` declarado contra
   `12` derivado, com um campo espúrio inventado para fechar a conta.
   Pego pela revisão de especificação. **Segundo defeito do mesmo tipo em
   duas frentes consecutivas**, no gate seguinte ao que criou a proibição.
2. **`lt_irrefl` não resolve** com o import mínimo. Trocado por
   `Nat.lt_irrefl`. Correção de tática; nenhuma assinatura mudou.

## Claim

`MONOVARIANT-REFLECTION-LIMIT-FORMAL-001`, `evidence_level: F`, novidade
`NONE`. Monovariantes são material clássico.

```text
ledger antes   25
ledger depois  26
```

## Decisão

```text
FOUND_MONOVARIANT_DESCENT_001_RESULT_REVIEW_APPROVED
```

## Ressalva

Cinco gates, mesmo agente, sessão única. Não substitui revisão externa.
