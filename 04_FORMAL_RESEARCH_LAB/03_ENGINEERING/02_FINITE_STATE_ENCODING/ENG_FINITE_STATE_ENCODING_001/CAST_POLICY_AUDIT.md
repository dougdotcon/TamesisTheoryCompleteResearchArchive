---
document_id: ENC-CAST-POLICY-AUDIT
transport_points: 2
---

# Auditoria da política de casts

## Os dois pontos, medidos

```text
Fin.cast: 3 ocorrencias
  TableConstruction.lean:71   tableIndex          — codigo
  TableConstruction.lean:75   docstring           — texto
  Commutation.lean:51         getElem privado     — codigo
```

**Duas ocorrências em código**, uma em cada direção:

```yaml
1:
  declaration: buildTransitionTable_getElem
  visibility: private
  direction: "Fin table.next.size -> Fin n"
  orientation: buildTransitionTable_size, direta

2:
  declaration: CertifiedFiniteEncoding.tableIndex
  visibility: PUBLIC_EXECUTABLE_CORE
  direction: "Fin n -> Fin table.next.size"
  orientation: buildTransitionTable_size, .symm
```

Nenhum terceiro auxiliar independente foi necessário.
`ENG_FINITE_STATE_ENCODING_001_CAST_POLICY_FAILED` **não** disparou.

## Proibições verificadas

```text
Eq.ndrec   0
cast_heq   0
HEq        0
```

## O teorema anti-correção

```lean
@[simp]
theorem CertifiedFiniteEncoding.tableIndex_val (encoding) (stepS) (s) :
    ((encoding.tableIndex stepS s : Fin (buildTransitionTable encoding stepS).next.size) : Nat)
      = ((encoding.encode s : Fin n) : Nat) :=
  rfl
```

`rfl`, e **sem axiomas** na API que o sustenta: `Fin.cast` não depende de
axioma nenhum. O transporte é reetiquetagem do limite, não cálculo.

Verificado por `decide` sob codificação permutada:

```lean
example : ((permEnc.tableIndex tailStep ⟨0, _⟩ : Fin _) : Nat) = 3 := by decide
```

## A dependência em `stepS`

```yaml
tableIndex_depends_on_stepS:
  kind: TYPE_DEPENDENCY
  value_depends_on_stepS: false
  evidence: tableIndex_val, cujo lado direito nao menciona stepS
  status: ACCEPTED_TYPE_DEPENDENCY
```

Não existe um segundo `tableIndex` sobre `Fin n`: esse papel já é de
`encode`.
