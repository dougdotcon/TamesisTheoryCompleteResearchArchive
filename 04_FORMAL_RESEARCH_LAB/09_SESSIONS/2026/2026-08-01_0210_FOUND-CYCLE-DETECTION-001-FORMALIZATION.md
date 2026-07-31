---
session_id: 2026-08-01-FOUND-CYCLE-DETECTION-001-FORMALIZATION
date: 2026-08-01
gate: FOUND_CYCLE_DETECTION_001_FORMALIZATION
authorized_action: FOUND_CYCLE_DETECTION_001_FORMALIZATION_AUTHORIZED
agent: claude-opus-5
commit_before: 8458f8af2adf7c8476bc1b853ab93175e1a0a062
decision: FOUND_CYCLE_DETECTION_001_FORMALIZATION_VERIFIED
theorems_formalized: 8
---

# Sessão — FOUND-CYCLE-DETECTION-001 · formalização

O laboratório passou a ter **um programa cuja correção e cuja completude
são teoremas**.

## Preflight

```text
HEAD                  8458f8af2adf7c8476bc1b853ab93175e1a0a062
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      03e1ec3 -> 8458f8a
```

## O que foi construído

```text
TamesisLab/Foundations/CycleDetection/
  Witness.lean       CycleWitness, Valid, instancia decidivel explicita
  Candidates.lean    cycleCandidates e sua caracterizacao
  Detector.lean      detectCycleWitness?
  Correctness.lean   soundness e completeness
  Periodicity.lean   tres pontes proposicionais
  Audit.lean         somente #check

TamesisLab/Foundations/CycleDetection.lean       agregador
TamesisLab/Tests/FoundCycleDetection001*.lean    tres testes
```

```text
1 estrutura, 3 definicoes, 1 instancia, 8 teoremas, 609 linhas.
```

## Camadas de hipótese — verificadas nas assinaturas impressas

```text
camada 0   cycleCandidates, mem_cycleCandidates_iff
           sem X, sem Fintype, sem DecidableEq

camada 1   CycleWitness.Valid
           Fintype pela cota, SEM DecidableEq

camada 2   detectCycleWitness?, _sound, _complete
           Fintype e DecidableEq

camada 3   isPeriodicPt, mem_periodicPts, propagates
           SEM DecidableEq
```

`DecidableEq X` entra em **uma única definição** e não vaza para resultado
proposicional algum.

## Reutilização

Os três teoremas de `Periodicity.lean` têm **uma linha de prova cada**:

```lean
CycleWitness.isPeriodicPt  := periodic_tail_of_collision f x h.2.2.2
CycleWitness.mem_periodicPts := Function.mk_mem_periodicPts h.2.1 (isPeriodicPt h)
CycleWitness.propagates    := collision_propagates f x h.2.2.2 k
```

A completude é um transporte de `exists_bounded_iterate_collision`, cuja
conclusão coincide termo a termo com `Valid`. **A casa dos pombos não foi
repetida**: o lema de contagem da Mathlib tem contagem `grep` zero em toda
a frente, e nenhum corpo de teorema anterior foi copiado.
`Function.iterate_add_apply` não aparece.

## Dois atritos reais

### Unificação de ordem superior

```text
exact of_decide_eq_true (List.find?_some h)
```

falhou: Lean escolheu `p := @decide (Valid f x w)` — função **constante** —
em vez do predicado. Resolvido passando
`(p := fun v => decide (CycleWitness.Valid f x v))`.

### Auditoria-zero versus docstrings

As primeiras versões documentavam as proibições dentro dos módulos, em
listas do tipo "sem X". As auditorias de tokens, de imports e do lema de
pigeonhole encontravam essas próprias menções e reportavam falso positivo.
Movidas para `COMPUTABILITY_RESULT.md`, fora do Lean. As quatro auditorias
passaram a **zero**.

## Execução

Cinco modelos, avaliados por `#eval` **e** provados por `decide` — sem
`native_decide`:

```text
Fin 1  id                     some <0,1>
Bool   id                     some <0,1>   nos dois estados
Bool   not                    some <0,2>   nos dois estados
Fin 3  0->1->2->2   de 0      some <2,1>
Fin 4  0->1->2->3->2 de 0     some <2,2>
```

Quatorze teoremas de regressão ao todo. Dois exemplos fecham o ciclo entre
execução e prova: `detectCycleWitness?_sound` aplicado a um resultado
obtido por `decide`, e `mem_periodicPts` sobre ele.

## Pegada axiomática

```text
cycleCandidates          does not depend on any axioms
os demais                [propext, Classical.choice, Quot.sound]
sorryAx                  0
```

`cycleCandidates` é o único objeto que não menciona `Fintype`, e é
exatamente o único sem pegada — confirmando a origem em `Fintype.card` e
`Finset.univ`. **Pegada axiomática não é não-computabilidade**: o detector
avaliou em cinco modelos.

## Omissões deliberadas

```yaml
detected_cycle_is_component_cycle: NAO formalizado   # CD-GAP-012
detectCycleWitness (total):        NAO formalizado   # CD-GAP-017
```

A primeira é adaptador mecânico e dispensa o import de `FunctionalGraphs`.
A segunda mantém a API garantida em `Option CycleWitness`, sem valor
padrão falso.

## Validação

```text
FoundCycleDetection001.lean            exit 0   26 s
FoundCycleDetection001Execution.lean   exit 0    2 s
FoundCycleDetection001Axioms.lean      exit 0    2 s
lake build                             PASS   8737 jobs
tokens proibidos                       0
lema de pigeonhole                     0
imports proibidos                      0
objeto de orbita quociente             0
pytest                                 PASS
labctl validate                        PASS
whitespace                             PASS, antes do git add
```

Nenhum teste removido, nenhum módulo matemático de frente anterior
alterado.

## Um defeito corrigido antes do fecho

Na primeira passagem, os agregadores `TamesisLab/Foundations.lean` e
`TamesisLab.lean` **não** foram atualizados: o patch usava uma âncora
inexistente e abortou, e a falha passou despercebida numa saída truncada.
O `lake build` do alvo padrão, portanto, não cobria a frente. Corrigido:
o contador passou de **8727** para **8737 jobs**.

## Claim

Uma, a vigésima: `EXECUTABLE-CYCLE-WITNESS-FORMAL-001`, `VERIFIED`,
`evidence_level: F`, novidade matemática e algorítmica **NONE**.

## Estado final

```text
work_status            VERIFIED
specification_status   APPROVED
formalization_status   VERIFIED
authorized_action      FOUND_CYCLE_DETECTION_001_RESULT_REVIEW_AUTHORIZED
```

Totalização, Floyd, Brent, tabela visitada, minimalidade, extração e
integração permanecem **não autorizadas**.

## Próxima ação única

Revisar a API executável, a instância decidível, os testes, a soundness, a
completeness e os limites de computabilidade antes de autorizar qualquer
otimização ou extração.
