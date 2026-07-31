---
document_id: FCD-RESULT-REVIEW
gate: FOUND_CYCLE_DETECTION_001_RESULT_REVIEW
reviewed_commit: d9d672caf817fdb6d0b2dd27a6bf5355bc8739fe
decision: A_RESULT_REVIEW_APPROVED
new_theorems: 0
math_modules_modified: 0
---

# Revisão do resultado

Revisão do que já está verificado. **Nenhum teorema novo, nenhum módulo
matemático alterado, nenhuma implementação nova.**

## Confirmação item a item

### CDR-001 — modelo executável `CONFIRMADO`

```lean
structure CycleWitness where
  baseIndex : ℕ
  period : ℕ
deriving DecidableEq, Repr, BEq
```

Dois campos, ambos `ℕ`, com docstrings que já negam a minimalidade.
Confirmada a ausência de `entryPoint`, `entryIndex`, `prefixIndex`,
`tailLength`, `cycleEntry`, `isMinimal`, `proof` e `cycleList` **como
campos**. A única ocorrência de qualquer um desses nomes no núcleo é uma
linha de documentação em `Witness.lean` que explica por que `entryPoint`
foi rejeitado — registro da decisão, não campo.

### CDR-002 — contrato `CONFIRMADO`

```lean
def CycleWitness.Valid {X : Type*} [Fintype X] (f : X → X) (x : X)
    (w : CycleWitness) : Prop :=
  w.baseIndex < Fintype.card X ∧
  0 < w.period ∧
  w.baseIndex + w.period ≤ Fintype.card X ∧
  f^[w.baseIndex + w.period] x = f^[w.baseIndex] x
```

Sem `DecidableEq`. Sem afirmação de minimalidade. A ordem das quatro
cláusulas coincide com a conclusão de
`exists_bounded_iterate_collision`, conferida contra o fonte.

### CDR-003 — instância decidível `CONFIRMADO`

```lean
instance CycleWitness.decidableValid {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) (w : CycleWitness) :
    Decidable (CycleWitness.Valid f x w) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _))
```

Somente `[Fintype X]` e `[DecidableEq X]`. Nenhum `Classical`, nenhuma
instância global de `DecidableEq X`, nenhum conflito de síntese — ver
`INSTANCE_AUDIT.md`.

### CDR-004 — enumeração `CONFIRMADO`

Ordem `baseIndex` crescente, depois `period` crescente. `@[simp]`
`cycleCandidates_zero : cycleCandidates 0 = []` e
`cycleCandidates_one : cycleCandidates 1 = [⟨0,1⟩]`, ambos por `rfl`. O
caso `baseIndex + period = n` está incluído — reconfirmado por avaliação.

### CDR-005 — caracterização `CONFIRMADO`

```text
w ∈ cycleCandidates n ↔
  w.baseIndex < n ∧ 0 < w.period ∧ w.baseIndex + w.period ≤ n
```

Assinatura impressa **sem** `Fintype`, `DecidableEq`, `Classical`, `f` e
`x`.

### CDR-006 — detector `CONFIRMADO`

```lean
def detectCycleWitness? {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) : Option CycleWitness :=
  (cycleCandidates (Fintype.card X)).find? fun w =>
    decide (CycleWitness.Valid f x w)
```

Corpo composto apenas de enumeração finita, `List.find?` e `decide` sobre
`Valid`. Confirmada a ausência de marca de não-computabilidade, de escolha
clássica construindo dado, do objeto de órbita quociente, de grafos
simples, de recursão não limitada e de valor padrão falso.

### CDR-007 — soundness `CONFIRMADO`

Prova em duas etapas: `List.find?_some`, com o predicado passado
explicitamente, e `of_decide_eq_true`. **`mem_cycleCandidates_iff` não é
dependência** — as cotas vêm do próprio `Valid`, e a soundness usa o
resultado real de `List.find?`.

### CDR-008 — completeness `CONFIRMADO`

Reutiliza `exists_bounded_iterate_collision`, `mem_cycleCandidates_iff`,
`List.find?_isSome` e `Option.isSome_iff_exists`. Nenhuma nova aplicação
do pigeonhole.

### CDR-009 — periodicidade `CONFIRMADO`

`periodic_tail_of_collision f x h.2.2.2`. Uma linha.

### CDR-010 — `periodicPts` `CONFIRMADO`

`Function.mk_mem_periodicPts h.2.1 (isPeriodicPt h)`. Consome exatamente o
`0 < w.period`.

### CDR-011 — propagação `CONFIRMADO`

`collision_propagates f x h.2.2.2 k`. Assinatura idêntica à do teorema
reutilizado.

## Semântica — reafirmada

```text
baseIndex eh o indice-base da igualdade certificada.
NAO eh o menor indice de entrada, nem o comprimento exato da cauda,
nem o primeiro estado do ciclo, nem um indice canonico.

period eh um periodo positivo testemunhado.
NAO eh Function.minimalPeriod, nem comprimento fundamental,
nem menor periodo, nem periodo canonico.
```

A busca exigida pelo gate — ocorrências de `baseIndex` associadas a
"mínimo", "menor", "entrada exata" ou "cauda exata" nos módulos — retornou
**zero**. `minimalPeriod` aparece em **três** linhas do núcleo, todas de
documentação e todas **negando** a identificação.

## Primeiro resultado versus resultado mínimo

```text
List.find? devolve o PRIMEIRO candidato aceito segundo a ordem concreta
de cycleCandidates.

Isso NAO eh o mesmo que o menor certificado segundo uma ordem
matematica provada.
```

Nenhum teorema de minimalidade existe na frente. Os quatorze teoremas de
regressão fixam valores concretos e são explicitamente rotulados como
dependentes da ordem da enumeração.

## Um defeito encontrado e corrigido nesta revisão

Os dois testes de auditoria criados aqui importam a raiz `TamesisLab` —
é assim que a cobertura do agregador é medida. Registrá-los **dentro** de
`TamesisLab.lean` criou um **import circular**, e o `lake build` falhou.
O registro foi removido: os dois testes ficam fora do agregador raiz, por
construção, e são executados por `lake env lean`. `TamesisLab.lean`
voltou exatamente ao estado do commit revisado.

## Decisão

```text
A. FOUND_CYCLE_DETECTION_001_RESULT_REVIEW_APPROVED
```

| Critério | Estado |
|---|---|
| enumeração correta e completa | `mem_cycleCandidates_iff` |
| detector executável | `#eval` em cinco modelos, mais os testes de auditoria |
| soundness e completeness corretas | revisadas linha a linha |
| instância decidível isolada | `INSTANCE_AUDIT.md` |
| build raiz cobre a frente | `UMBRELLA_COVERAGE_AUDIT.md`, 8737 jobs |
| claim corresponde aos teoremas | revisada, sem wording proibida |
| semântica não mínima clara | reafirmada em quatro documentos |
| pigeonhole não repetido | `grep` zero |
| totalização ausente | nenhuma declaração total |
| otimizações ausentes | Floyd, Brent e tabela visitada com `grep` zero |
| pegada axiomática documentada | `COMPUTABILITY_REVIEW.md` |
| desvio de governança não material | `GOVERNANCE_DEVIATION_REVIEW.md` |
