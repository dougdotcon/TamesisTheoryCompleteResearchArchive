---
document_id: ENC-FINAL-CAST-POLICY
supersedes: ENC-ARRAY-SIZE-AND-CAST-POLICY
stage: SPECIFICATION_REVIEW
frozen: true
transport_points: 2
---

# Política final de casts

## Dois pontos, e apenas dois

```yaml
1:
  declaration: buildTransitionTable_getElem
  visibility: INTERNAL_HELPER
  direction: "Fin table.next.size -> Fin n"
  proof: "Array.getElem_ofFn (f := ...) i.isLt   — termo de uma linha"

2:
  declaration: CertifiedFiniteEncoding.tableIndex
  visibility: PUBLIC_EXECUTABLE_CORE
  direction: "Fin n -> Fin table.next.size"
  proof: "Fin.cast (buildTransitionTable_size e stepS).symm (e.encode s)"
```

Um em cada direção. Nenhum terceiro auxiliar independente de transporte
foi necessário no probe. `STOP-ENC-005` **não** disparou.

## Proibições reverificadas no probe

```text
Eq.ndrec manual              zero ocorrencias
cast_heq                     zero
HEq como API                 zero
casts repetidos por teorema  zero
modulo, clamp, fallback      zero
```

Todo transporte adicional que aparece nas provas é **definicional** e
interno a uma linha, derivado dos dois pontos acima.

## O índice tipado

```lean
def CertifiedFiniteEncoding.tableIndex (e) (stepS) (s : S) :
    Fin (buildTransitionTable e stepS).next.size :=
  Fin.cast (buildTransitionTable_size e stepS).symm (e.encode s)
```

### A dependência em `stepS`, auditada

```yaml
tableIndex_depends_on_stepS:
  reason: >
    O tipo de retorno contem o tamanho da tabela construida para esse
    stepS, embora o valor natural do indice dependa apenas de encode.
  status: ACCEPTED_TYPE_DEPENDENCY
```

É dependência **de tipo**, não de valor — e `tableIndex_val` prova
exatamente isso: o `Nat` produzido não menciona `stepS`.

**Não** existe um segundo `tableIndex` sobre `Fin n`. Esse papel já é de
`encode`, e duplicá-lo criaria dois nomes para a mesma função.

## O teorema anti-correção

```lean
@[simp]
theorem CertifiedFiniteEncoding.tableIndex_val (e) (stepS) (s : S) :
    ((e.tableIndex stepS s : Fin (buildTransitionTable e stepS).next.size) : Nat)
      = ((e.encode s : Fin n) : Nat) :=
  rfl
```

`rfl`. `Fin.cast` preserva o campo `val` definicionalmente, e
`Fin.cast` **não depende de axioma nenhum** — medido.

A anotação `@[simp]` é uma correção desta revisão. Ela paga: no probe, as
duas reescritas de `run?_corresponds_to_typed_iterate` e as duas da
soundness passam por ela.

Verificação executável, sob codificação permutada `i ↦ 3 - i`:

```lean
example : ((permEnc.tableIndex tailStep ⟨0, _⟩ : Fin _) : Nat) = 3 := by decide
```

Passou. Nenhum módulo, nenhum `clamp`, nenhuma substituição de índice.
