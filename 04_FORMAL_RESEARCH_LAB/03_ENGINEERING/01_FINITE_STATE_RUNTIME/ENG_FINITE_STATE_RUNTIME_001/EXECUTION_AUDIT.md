---
document_id: RT-EXECUTION-AUDIT
tests: 10
regression_theorems: 22
---

# Auditoria de execução

Dez casos, avaliados por `#eval` **e** provados por `decide` ou `rfl`.
**Sem `native_decide`.**

| Teste | Tabela | `start` | Resultado |
|---|---|---|---|
| TEST-001 | `#[]` | 0 | `error (initialStateOutOfBounds 0 0)`; validação `ok` |
| TEST-002 | `#[1]` | 0 e **100** | `error transitionDestinationOutOfBounds` |
| TEST-003 | `#[0]` | 1 | `error (initialStateOutOfBounds 1 1)` |
| TEST-004 | `#[0]` | 0 | `ok ⟨0,1⟩` |
| TEST-005 | `#[1,0]` | 0 | `ok ⟨0,2⟩` |
| TEST-006 | `#[1,2,2]` | 0 | `ok ⟨2,1⟩` |
| TEST-007 | `#[1,2,3,2]` | 0 | `ok ⟨2,2⟩` |
| TEST-008 | `#[1,2,3,2]` | 1, 2, 3 | `⟨1,2⟩`, `⟨0,2⟩`, `⟨0,2⟩` |
| TEST-009 | `#[0,2,1]` | 0, 1, 2 | `⟨0,1⟩`, `⟨0,2⟩`, `⟨0,2⟩` |
| TEST-010 | `#[]` e `#[1,2,3,2]` | — | `run? 0 999 = some 999`; `run? 1 999 = none` |

## O oráculo

Os casos `004` a `007` reproduzem, **em forma de tabela**, exatamente os
modelos `Fin 1`, `Bool`, `Fin 3` e `Fin 4` já verificados em
`FOUND-CYCLE-DETECTION-001`. A coincidência dos certificados é evidência
independente de que a ponte `Array Nat → Fin n` preserva a dinâmica.

## O que TEST-002 congela

A tabela é inválida **e** o `start` é inválido. O resultado é o erro de
**tabela**. Esse único teste fixa a precedência que os dois teoremas de
erro provam.

## O que TEST-009 **não** é

`#[0,2,1]` tem dois componentes: `0` é ponto fixo, e `1` e `2` formam um
ciclo de dois. Isso é observável executando **três consultas
independentes** — **não** é enumeração global de componentes, e a frente
não produz tal enumeração.

## Encadeamento execução → prova

```lean
example :
    (RawTransitionTable.mk #[1, 2, 3, 2]).run? (2 + 2) 0 =
      (RawTransitionTable.mk #[1, 2, 3, 2]).run? 2 0 :=
  (analyzeTransitionTable_sound
    (by decide : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 0 = .ok ⟨2, 2⟩)).2.2
```

Um certificado **computado** por `decide` vira, pela soundness, uma
afirmação **provada** sobre a execução do array original. É o
encadeamento que dá sentido à frente inteira.

E o ramo defensivo, sob pré-condições verificadas por `decide`:

```lean
example : analyzeTransitionTable ⟨#[1, 2, 3, 2]⟩ 0
    ≠ .error .internalDetectorFailure :=
  analyzeTransitionTable_ne_internalFailure ⟨#[1, 2, 3, 2]⟩ 0 (by decide) (by decide)
```

## Tempos

```text
DynamicAnalysis.lean (isolado)              exit 0    29 s
EngFiniteStateRuntime001.lean               exit 0     2 s
EngFiniteStateRuntime001Execution.lean      exit 0     4 s
EngFiniteStateRuntime001Axioms.lean         exit 0     2 s
lake build                                  PASS    8748 jobs, 100 s
```

Os três testes têm **zero** ocorrências de `error:`. Nenhum teste foi
removido ou enfraquecido; nenhum módulo de frente anterior foi alterado.
