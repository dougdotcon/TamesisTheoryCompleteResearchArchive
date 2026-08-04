---
document_id: FOUND-UNIFORM-PRIMREC-001-README
work_item_id: FOUND-UNIFORM-PRIMREC-001
specification_status: READY_FOR_REVIEW
research_role: FORMAL_FOUNDATION
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# FOUND-UNIFORM-PRIMREC-001

## O que a ponte deixou em aberto

`FOUND-COMPUTABILITY-BRIDGE-001` provou que sobre dominio **finito** toda
funcao e primitiva recursiva, e que por isso a classificacao nao carrega
informacao algoritmica. Deixou registrado, sem prova, o enunciado onde a
pergunta volta a ter conteudo:

```lean
def UniformPrimrecStatement : Prop := Primrec2 analyzeTransitionTable
```

Sobre `RawTransitionTable x Nat` o dominio e **infinito**,
`Primrec.dom_finite` nao se aplica, e a conclusao passa a depender do que
a funcao faz.

## O resultado

```lean
theorem primrec_analyzeTransitionTable : Primrec2 analyzeTransitionTable
theorem uniformPrimrecStatement_holds : UniformPrimrecStatement
```

**`CB-GAP-001` fecha.** E o primeiro resultado de computabilidade do
laboratorio cuja prova consulta o algoritmo.

## Por que foi possivel

O obstaculo nunca foi computabilidade — era **tipo dependente**.
`analyzeTransitionTable` atravessa `Fin t.next.size`, e `Primrec` nao
conversa com isso.

A descoberta que destravou: **`run?` ja e nao dependente**,
`Nat -> Nat -> Option Nat`, e a sua recursao le-se como iterada:

```lean
theorem run?_eq_iterate : t.run? k s = (fun o => o.bind t.step?)^[k] (some s)
```

Dai `Primrec.nat_iterate` faz o trabalho. O tipo dependente sobrevive
apenas em `detectCycle?`, e sai por um **casamento**, nao por reescrita:

```lean
theorem valid_iff_rawValid :
    CycleWitness.Valid t.step start w <-> RawValid t.toRaw start w
```

A quarta clausula viaja pela ponte que a frente do runtime ja tinha,
`run?_eq_iterate_step`. As tres primeiras so precisam de
`Fintype.card_fin`.

## O que esta frente NAO afirma

```text
que exista modelo de custo
que alguma classe de complexidade esteja definida
que P vs NP tenha sido tocado
que a cota do certificado seja cota de recursos
que primitivo recursivo signifique eficiente
```

`Primrec` e uma classe **enorme** — contem torres de exponenciais. Dizer
que a analise e primitiva recursiva **nao** diz que ela e barata.
