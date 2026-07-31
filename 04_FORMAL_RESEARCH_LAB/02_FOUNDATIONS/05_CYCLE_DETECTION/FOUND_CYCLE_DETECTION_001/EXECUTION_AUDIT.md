---
document_id: FCD-EXECUTION-AUDIT
tests: 5
regression_theorems: 14
---

# Auditoria de execução

Os valores abaixo são **testes de regressão da ordem da enumeração**. Não
são teoremas de minimalidade. Todos foram provados por `decide` — sem
`native_decide` — além de avaliados por `#eval`.

## Os cinco modelos

| Teste | Modelo | `#eval` | Teorema por `decide` |
|---|---|---|---|
| TEST-001 | `Fin 1`, `id` | `some ⟨0,1⟩` | `detectCycleWitness? f1 0 = some ⟨0,1⟩` |
| TEST-002 | `Bool`, `id` | `some ⟨0,1⟩` nos dois estados | dois teoremas |
| TEST-003 | `Bool`, `not` | `some ⟨0,2⟩` nos dois estados | dois teoremas |
| TEST-004 | `Fin 3`, `0→1→2→2` | `some ⟨2,1⟩` de `0` | um teorema |
| TEST-005 | `Fin 4`, `0→1→2→3→2` | `some ⟨2,2⟩` de `0` | um teorema |

## TEST-006 — demais estados

```text
Fin 3   de 1 -> some <1,1>      de 2 -> some <0,1>
Fin 4   de 1 -> some <1,2>      de 2 -> some <0,2>      de 3 -> some <0,2>
```

O `period` testemunhado coincide dentro do componente; o `baseIndex`
**não** — depende do estado inicial. Cinco teoremas por `decide`.

## Enumeração

```text
cycleCandidates 0 = []            por rfl
cycleCandidates 1 = [<0,1>]       por rfl
cycleCandidates 3   seis pares, incluindo <0,3>, <1,2>, <2,1>
cycleCandidates 4   dez pares, incluindo <0,4>, <1,3>, <2,2>, <3,1>
```

A fronteira `baseIndex + period = n` está presente em ambos.

## Encadeamento com os teoremas

Dois exemplos fecham o ciclo entre execução e prova:

```lean
example : CycleWitness.Valid f4 0 ⟨2, 2⟩ :=
  detectCycleWitness?_sound (by decide : detectCycleWitness? f4 0 = some ⟨2, 2⟩)

example : f4^[2] 0 ∈ Function.periodicPts f4 :=
  CycleWitness.mem_periodicPts
    (detectCycleWitness?_sound (by decide : detectCycleWitness? f4 0 = some ⟨2, 2⟩))
```

O primeiro converte um resultado **computado** em contrato provado. O
segundo o converte em periodicidade. É esse encadeamento que distingue
esta frente de um simples programa.

## Tempos

```text
FoundCycleDetection001.lean            exit 0    26 s
FoundCycleDetection001Execution.lean   exit 0     2 s
FoundCycleDetection001Axioms.lean      exit 0     2 s
lake build                             PASS    8737 jobs
```

Nenhum teste foi removido ou enfraquecido para o build passar. Nenhum
módulo matemático de frente anterior foi alterado.

Os dois agregadores — `TamesisLab/Foundations.lean` e `TamesisLab.lean` —
receberam as linhas de `import` da nova frente. Sem elas, o alvo padrão do
`lake build` não cobria os módulos novos: o contador passou de **8727**
para **8737 jobs**, isto é, os seis módulos do núcleo, o agregador da
frente e os três testes.
