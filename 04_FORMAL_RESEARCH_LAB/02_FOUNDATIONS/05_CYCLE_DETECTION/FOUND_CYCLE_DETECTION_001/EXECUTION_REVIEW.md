---
document_id: FCD-EXECUTION-REVIEW
models: 5
regression_theorems: 16
---

# Revisão de execução

Os cinco modelos foram reexecutados nesta revisão. Todos os valores
documentados se confirmaram.

## Resultados

| Modelo | Estado inicial | Resultado |
|---|---|---|
| `Fin 1`, `id` | `0` | `some ⟨0,1⟩` |
| `Bool`, `id` | `false` e `true` | `some ⟨0,1⟩` |
| `Bool`, `not` | `false` e `true` | `some ⟨0,2⟩` |
| `Fin 3`, `0→1→2→2` | `0` | `some ⟨2,1⟩` |
| `Fin 4`, `0→1→2→3→2` | `0` | `some ⟨2,2⟩` |

Demais estados, também reconfirmados:

```text
Fin 3   de 1 -> some <1,1>      de 2 -> some <0,1>
Fin 4   de 1 -> some <1,2>      de 2 -> some <0,2>      de 3 -> some <0,2>
```

O `period` testemunhado coincide dentro do componente; o `baseIndex`
**não** — depende do estado inicial. Isso é visível em `Fin 4`, onde os
quatro estados dão o mesmo `period = 2` e três `baseIndex` distintos.

## Estes valores dependem da ordem

```text
Os valores acima sao consequencia da ordem concreta de cycleCandidates:
baseIndex crescente, depois period crescente, e List.find? devolve o
PRIMEIRO aceito.

Se a ordem mudar, os valores mudam.

NENHUM deles eh teorema de minimalidade.
```

Esta frase é vinculante e aparece também em `RESULT_BOUNDARY.md` e em
`TEST_PLAN.md`.

## Forma da evidência

```text
#eval                      evidencia operacional dentro do elaborador
example ... := by decide   teorema de regressao, verificado pelo kernel
native_decide              NAO usado
```

Dezesseis teoremas de regressão ao todo: quatorze no arquivo de execução e
dois no de cobertura do agregador.

## Encadeamento execução → prova

```lean
example : CycleWitness.Valid f4 0 ⟨2, 2⟩ :=
  detectCycleWitness?_sound (by decide : detectCycleWitness? f4 0 = some ⟨2, 2⟩)

example : f4^[2] 0 ∈ Function.periodicPts f4 :=
  CycleWitness.mem_periodicPts
    (detectCycleWitness?_sound (by decide : detectCycleWitness? f4 0 = some ⟨2, 2⟩))
```

Um valor **computado** vira contrato **provado**, e depois periodicidade.
É esse encadeamento que distingue a frente de um programa comum.

## Tempos

```text
FoundCycleDetection001.lean               exit 0    28 s
FoundCycleDetection001Execution.lean      exit 0     3 s
FoundCycleDetection001Axioms.lean         exit 0     2 s
FoundCycleDetection001InstanceAudit.lean  exit 0    80 s
FoundCycleDetection001UmbrellaAudit.lean  exit 0     6 s
lake build                                PASS    8737 jobs, 26 s
```

Os dois testes de auditoria importam a raiz inteira; daí os 80 s do
primeiro.
