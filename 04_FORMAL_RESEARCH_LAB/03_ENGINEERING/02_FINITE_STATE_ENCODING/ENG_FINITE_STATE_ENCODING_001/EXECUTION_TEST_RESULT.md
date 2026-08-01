---
document_id: ENC-EXECUTION-TEST-RESULT
tests: 8
native_decide: 0
---

# Resultado dos testes executáveis

Todos por `decide` e `rfl`. Zero `native_decide`.

| Teste | Sistema | Tabela | Witness |
|---|---|---|---|
| `ENC-TEST-001` | `Fin 1`, `id` | `#[0]` | `⟨0,1⟩` |
| `ENC-TEST-002` | `Bool`, `id` | `#[0,1]` | `⟨0,1⟩` nos dois estados |
| `ENC-TEST-003` | `Bool`, `not` | `#[1,0]` | `⟨0,2⟩` nos dois estados |
| `ENC-TEST-004` | `Fin 3`, `0→1→2→2` | `#[1,2,2]` | `⟨2,1⟩` |
| `ENC-TEST-005` | `Fin 4`, `0→1→2→3→2` | `#[1,2,3,2]` | `⟨2,2⟩` |
| `ENC-TEST-006` | idem, codificação `i ↦ 3-i` | `#[1,0,1,2]` | `⟨2,2⟩` |
| `ENC-TEST-007` | `Empty` | `#[]` | não há chamada bem tipada |
| `ENC-TEST-008` | exclusão de erro | — | dois erros concretos e a forma universal |

Todos formulados como teoremas de regressão, não como `#eval`: o valor
esperado está no enunciado, e o `decide` o verifica.

## `ENC-TEST-006` — o teste que justifica a frente

```text
codificacao identidade   tabela #[1, 2, 3, 2]
codificacao i ↦ 3 - i    tabela #[1, 0, 1, 2]
```

Os números mudaram completamente. E ambos produzem, pela soundness, a
mesma conclusão **no tipo original**:

```lean
tailStep^[2 + 2] ⟨0, _⟩ = tailStep^[2] ⟨0, _⟩
```

Também instanciadas sob a codificação permutada:

```text
tableIndex do estado 0 = 3          por decide
table_step_commutes                 aplicado
table_iterate_commutes com k = 4    aplicado
```

### O que **não** é afirmado

Os witnesses concretos coincidiram em `⟨2,2⟩`. **Observação de teste, não
teorema.** Provar a invariância exigiria provar que a ordem de busca do
detector não importa, o que não é resultado desta frente —
`ENC-GAP-020`, `STOP-ENC-019`.

## `ENC-TEST-007` — tipo vazio

```lean
example : (buildTransitionTable emptyEnc (fun s => s.elim)).next = #[] := by decide
```

A tabela é construída e é vazia. `analyzeEncodedSystem` exige
`start : Empty`, que não existe: **a ausência de chamada é garantida pelo
sistema de tipos**, não por verificação em tempo de execução.

Compare com a frente anterior: lá a tabela vazia era válida e a consulta
era **rejeitada com erro**, porque o índice chegava como `Nat` e podia
ser qualquer coisa.

## Teste formal

`EngFiniteStateEncoding001.lean` faz `#check` das quinze declarações
públicas e contém seis exemplos genéricos em `S` e `n` — **sem**
`Fintype`, `DecidableEq`, `Nonempty` ou `Inhabited`. Se alguma fosse
exigida, a elaboração falharia por instância ausente.

O auxiliar privado **não** é alcançável desses testes, o que é a
verificação de que ele é mesmo interno.
