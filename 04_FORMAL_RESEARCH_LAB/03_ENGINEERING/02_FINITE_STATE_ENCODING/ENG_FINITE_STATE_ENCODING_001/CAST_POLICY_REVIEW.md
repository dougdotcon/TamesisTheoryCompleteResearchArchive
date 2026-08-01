---
document_id: ENC-CAST-POLICY-REVIEW
transport_points: 2
---

# Revisão da política de transportes

## Contagem feita no código, não na documentação

```text
Fin.cast, ocorrencias totais nos modulos   3
Fin.cast, ocorrencias em CODIGO            2
  TableConstruction.lean   tableIndex
  Commutation.lean         buildTransitionTable_getElem
```

A terceira ocorrência está numa docstring que explica por que
`tableIndex_val` é `rfl`. Medido após remover os blocos `/- … -/`.

```yaml
cast_points:
  public:
    - CertifiedFiniteEncoding.tableIndex
  private:
    - buildTransitionTable_getElem
  total: 2
```

Um em cada direção. **Nenhum terceiro transporte independente.**

## Proibições

```text
Eq.ndrec   0
cast_heq   0
HEq        0
auxiliares extras de transporte   0
```

## `tableIndex`

```lean
def CertifiedFiniteEncoding.tableIndex (encoding) (stepS) (s : S) :
    Fin (buildTransitionTable encoding stepS).next.size :=
  Fin.cast (buildTransitionTable_size encoding stepS).symm (encoding.encode s)
```

`stepS` aparece porque o **tipo de retorno** menciona a tabela construída
para ele. O **valor natural** não depende de `stepS`, e é isso que o
teorema seguinte demonstra.

## `tableIndex_val` — o teorema anti-correção

```lean
@[simp]
theorem CertifiedFiniteEncoding.tableIndex_val (encoding) (stepS) (s) :
    ((encoding.tableIndex stepS s : Fin (buildTransitionTable encoding stepS).next.size) : Nat)
      = ((encoding.encode s : Fin n) : Nat) :=
  rfl
```

`rfl`. O transporte **não corrige e não altera** o índice: é
reetiquetagem do limite.

Confirmado também por execução, sob a codificação permutada `i ↦ 3 - i`:

```lean
example : ((permEnc.tableIndex tailStep ⟨0, _⟩ : Fin _) : Nat) = 3 := by decide
```
