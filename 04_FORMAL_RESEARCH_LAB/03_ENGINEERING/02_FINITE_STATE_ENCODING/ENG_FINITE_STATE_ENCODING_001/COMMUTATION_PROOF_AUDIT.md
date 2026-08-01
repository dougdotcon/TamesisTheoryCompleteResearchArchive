---
document_id: ENC-COMMUTATION-PROOF-AUDIT
---

# Auditoria das provas de comutação

## Orientação, congelada

```text
Function.Semiconj f ga gb  significa  ∀ x, f (ga x) = gb (f x)

tableIndex_semiconj  :  tableIndex (stepS s) = step (tableIndex s)
table_step_commutes  :  step (tableIndex s) = tableIndex (stepS s)
```

## O principal, como implementado

```lean
theorem CertifiedFiniteEncoding.tableIndex_semiconj (encoding) (stepS) :
    Function.Semiconj (encoding.tableIndex stepS) stepS
      (buildTransitionTable encoding stepS).step := by
  intro s
  apply Fin.ext
  rw [ValidatedTransitionTable.step_val, buildTransitionTable_getElem]
  show ((encoding.encode (stepS s) : Fin n) : Nat)
      = ((encoding.encode (stepS (encoding.decode (encoding.encode s))) : Fin n) : Nat)
  rw [encoding.decode_encode]
```

Seis linhas. `Fin.ext` é aplicado **dentro** da prova; o enunciado
permanece em `Fin (buildTransitionTable encoding stepS).next.size` e
**não** foi enfraquecido para igualdade entre naturais.

### A lei usada

```text
decode_encode.
```

O termo a eliminar é `decode (encode s)`. `encode_decode` trata do caso
oposto e não se aplica — verificado por leitura da prova: `encode_decode`
não aparece em `Commutation.lean`.

### DAG

```text
ValidatedTransitionTable.step_val         (frente anterior, @[simp])
  -> buildTransitionTable_getElem         (privado)
      -> encodedStep, por defeq via show
          -> decode_encode
```

## O corolário

```lean
theorem CertifiedFiniteEncoding.table_step_commutes (encoding) (stepS) (s) :
    (buildTransitionTable encoding stepS).step (encoding.tableIndex stepS s)
      = encoding.tableIndex stepS (stepS s) :=
  (encoding.tableIndex_semiconj stepS s).symm
```

**Não** é provado de novo. Um `.symm`.

## Iteradas

```lean
theorem CertifiedFiniteEncoding.table_iterate_commutes (encoding) (stepS) (k) (s) :
    ((buildTransitionTable encoding stepS).step)^[k] (encoding.tableIndex stepS s)
      = encoding.tableIndex stepS (stepS^[k] s) :=
  ((encoding.tableIndex_semiconj stepS).iterate_right k s).symm
```

Um termo. **Nenhuma indução manual.** `Function.Semiconj.iterate_right`
compilou sem ajuste, e `ENG_FINITE_STATE_ENCODING_001_ITERATION_API_CHANGED`
não disparou.

Contraste com a frente anterior, onde o resultado análogo custou indução
com quantificador no enunciado, dois `show` obrigatórios e a escolha
entre `iterate_succ_apply` e sua variante.

## Correspondência com `run?`

```lean
theorem CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate (encoding) (stepS) (k) (s) :
    (buildTransitionTable encoding stepS).toRaw.run? k ((encoding.encode s : Fin n) : Nat)
      = some ((encoding.encode (stepS^[k] s) : Fin n) : Nat) := by
  have h := (buildTransitionTable encoding stepS).run?_eq_iterate_step k
    (encoding.tableIndex stepS s)
  rw [encoding.tableIndex_val stepS s] at h
  rw [h, encoding.table_iterate_commutes stepS k s,
      encoding.tableIndex_val stepS (stepS^[k] s)]
```

O lado bruto começa no `Nat` de **`encode`**, não em `tableIndex` —
exigência do gate, cumprida. `tableIndex` aparece apenas dentro da prova,
e `tableIndex_val` é usado nos dois extremos.

```text
segunda funcao recursiva   0
copia de run?              0
copia de step?             0
```

## Teste intermediário

```text
lake env lean TamesisLab/Engineering/FiniteStateEncoding/Commutation.lean
exit 0, 27 s
```

`ENG_FINITE_STATE_ENCODING_001_COMMUTATION_FAILED` não disparou.
