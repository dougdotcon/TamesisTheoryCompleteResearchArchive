---
document_id: ENC-FINAL-PROBE-VALIDATION
main_probe_exit: 0
axiom_probe_exit: 0
---

# Validação final dos probes

## Contrato de cada arquivo

```yaml
FiniteStateEncodingReviewProbe.lean:
  contract: toda declaracao compila
  content: 16 declaracoes, auditoria WeakEncoding, 8 testes, 15 #eval
  expected_exit: 0
  observed_exit: 0
  seconds: 30
  lean_errors: 0

FiniteStateEncodingAxiomProbe.lean:
  contract: toda declaracao compila; somente #check e #print axioms
  content: 15 declaracoes, 16 #check, 30 #print axioms
  expected_exit: 0
  observed_exit: 0
  seconds: 3
  lean_errors: 0
```

Nenhum dos dois contém declaração destinada a falhar. O próprio `exit 0`
é a prova disso: um arquivo com uma declaração que falha não sai com
zero.

## Tokens proibidos

```text
sorry, admit, unsafe, noncomputable,
Classical.choose, Classical.decEq,
Fintype.equivFin, Trunc.out,
Option.get, getD, clamp, fallback
```

`grep` sobre os dois arquivos saiu com código `1` — **nenhuma
ocorrência**.

## Conferência do log de axiomas

```text
sorryAx          AUSENTE
axiomas locais   AUSENTES
```

## Pegada medida — inalterada em relação à revisão

```text
CertifiedFiniteEncoding.encode_injective   does not depend on any axioms
CertifiedFiniteEncoding.encodedStep        does not depend on any axioms

buildTransitionTable                       [propext, Classical.choice, Quot.sound]
buildTransitionTable_size                  [propext, Classical.choice, Quot.sound]
buildTransitionTable_getElem               [propext, Classical.choice, Quot.sound]
tableIndex                                 [propext, Classical.choice, Quot.sound]
tableIndex_val                             [propext, Classical.choice, Quot.sound]
tableIndex_semiconj                        [propext, Classical.choice, Quot.sound]
table_step_commutes                        [propext, Classical.choice, Quot.sound]
table_iterate_commutes                     [propext, Classical.choice, Quot.sound]
run?_corresponds_to_typed_iterate          [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem                       [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem_sound                 [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem_complete              [propext, Classical.choice, Quot.sound]
analyzeEncodedSystem_ne_error              [propext, Classical.choice, Quot.sound]
```

**Primeira aparição de `Classical.choice`: `buildTransitionTable`**,
pelo campo `closed`, via `Array.getElem_ofFn`. Reconfirmado.

## APIs consumidas

```text
Array.ofFn                        [propext]
Array.size_ofFn                   [propext]
Array.getElem_ofFn                [propext, Classical.choice, Quot.sound]
Fin.cast                          NENHUM
Fin.ext                           NENHUM
Option.some.inj                   NENHUM
Function.LeftInverse.injective    NENHUM
Function.RightInverse.surjective  NENHUM
Function.Semiconj.iterate_right   [propext]

ValidatedTransitionTable.step                  [propext, Quot.sound]
ValidatedTransitionTable.toRaw_valid           [propext, Quot.sound]
ValidatedTransitionTable.run?_eq_iterate_step  [propext, Quot.sound]
analyzeTransitionTable                         [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_sound                   [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_complete                [propext, Classical.choice, Quot.sound]
```

## Resultados concretos reexecutados

```text
Fin 1, id                    ok ⟨0, 1⟩
Bool, id                     #[0, 1]        ok ⟨0, 1⟩ nos dois estados
Bool, not                    #[1, 0]        ok ⟨0, 2⟩ nos dois estados
Fin 3, ponto fixo            #[1, 2, 2]     ok ⟨2, 1⟩
Fin 4, ciclo de dois         #[1, 2, 3, 2]  ok ⟨2, 2⟩
Fin 4, codificacao permutada #[1, 0, 1, 2]  ok ⟨2, 2⟩
tableIndex de 0 sob permuta  3
Empty                        #[]
exclusao de erro             concreta e universal, ambas compilam
```

`zero native_decide`. Invariância do witness concreto **não** afirmada.

## Experimentos negativos — separados

```yaml
negative_experiments:
  route: DEFINITIONAL_ARRAY_OF_FN_PROOF
  status: REJECTED_BY_PROBE
  evidence:
    - generic size equality is not definitional
    - dependent substitution route does not typecheck
  included_in_mandatory_probe: false
  rerun_required: false
  preserved_in: AXIOM_FOOTPRINT_REVIEW.md
```

Nenhum arquivo Lean deliberadamente inválido foi criado neste gate.

## Remoção

```text
/tmp/FiniteStateEncodingReviewProbe.lean   removido
/tmp/FiniteStateEncodingAxiomProbe.lean    removido
/tmp/FiniteStateEncodingAxiomProbe.log     removido
```
