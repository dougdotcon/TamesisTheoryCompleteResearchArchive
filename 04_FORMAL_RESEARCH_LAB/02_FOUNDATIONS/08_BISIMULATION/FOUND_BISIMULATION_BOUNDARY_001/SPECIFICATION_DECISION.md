---
document_id: FOUND-BISIMULATION-BOUNDARY-001-SPECIFICATION-DECISION
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
specification_status: READY_FOR_REVIEW
---

# Decisões congeladas

Todas as assinaturas foram compiladas em probe descartável antes de
serem congeladas — ver [`PROBE_RESULT.md`](PROBE_RESULT.md).

## D-01 — Três definições, separadas

```lean
def Simulates (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, abstract (stepC c) = stepA (abstract c)

def Reflects (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, ∃ c' : C, stepC c = c' ∧ abstract c' = stepA (abstract c)

def Bisimulation (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  Simulates abstract stepC stepA ∧ Reflects abstract stepC stepA
```

`Reflects` é escrito com `∃ c'` **de propósito**, mesmo sabendo que o
`c'` está determinado. Escrevê-lo já resolvido — `abstract (stepC c) =
stepA (abstract c)` — tornaria o colapso verdadeiro por definição, e o
teorema não teria conteúdo.

Esta é a decisão mais importante da especificação: **o zag precisa
parecer uma obrigação genuína**, porque em geral ele é.

## D-02 — `Simulates` é definicionalmente `Semiconj`

```lean
theorem simulates_iff_semiconj … : Simulates … ↔ Function.Semiconj … := Iff.rfl
```

`Iff.rfl`. `Simulates` existe apenas para dar nome à metade, e o teorema
registra que não há diferença.

## D-03 — O colapso é o resultado central

```lean
theorem bisimulation_iff_semiconj (abstract) (stepC) (stepA) :
    Bisimulation abstract stepC stepA ↔ Function.Semiconj abstract stepC stepA
```

## D-04 — As consequências negativas são teoremas

```text
boolToUnit_bisimulation
forgetBool_surjective
bisimulation_does_not_reflect_cycles
surjective_bisimulation_does_not_reflect_cycles
```

Nenhum arquivo destinado a falhar.

## D-05 — Reutilização integral do contraexemplo

`concreteStep`, `abstractStep`, `forgetBool`,
`boolToUnit_no_concrete_recurrence` e `boolToUnit_semiconj` vêm de
`FiniteStateAbstraction/Counterexample.lean`, **sem alteração**. A frente
anterior não é tocada.

## D-06 — Nenhuma typeclass

```text
sobre C   nenhuma
sobre A   nenhuma
```

## D-07 — O recorte é parte do resultado

Ver [`SCOPE_BOUNDARY.md`](SCOPE_BOUNDARY.md). Enunciar o colapso sem o
qualificador "determinístico total e funcional" é `STOP-BIS-001`.

## D-08 — Nada de coindução

`Bisimulation` é uma conjunção de duas proposições quantificadas, não o
maior ponto fixo de um funtor. A definição coindutiva é outra coisa e
está fora de escopo.

## O que permanece fora

```text
sistemas nao deterministicos
relacoes de transicao gerais
bissimulacao relacional
acoes rotuladas
funcoes parciais
coinducao
quocientes
extracao, CLI, parser, integracao
```
