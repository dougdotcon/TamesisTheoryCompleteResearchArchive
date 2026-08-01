---
document_id: ENC-FINAL-COMMUTATION-THEOREMS
supersedes: [ENC-STEP-COMMUTATION, ENC-SEMICONJUGATION, ENC-ITERATION-COMMUTATION]
stage: SPECIFICATION_REVIEW
frozen: true
---

# Teoremas de comutação — versão final

## A inversão que esta revisão fez

A especificação tinha `table_step_commutes` como o teorema provado e
`tableIndex_semiconj` como seu `.symm`. **A revisão inverteu.**

```yaml
CertifiedFiniteEncoding.tableIndex_semiconj:
  category: PUBLIC_SPECIFICATION_CORE
  role: teorema semantico PRINCIPAL, provado diretamente

CertifiedFiniteEncoding.table_step_commutes:
  category: PUBLIC_COROLLARY
  role: leitura humana; termo (semiconj s).symm
```

Motivo: a forma que a API de Mathlib consome é a semiconjugação, e ela é
usada duas vezes — em `table_iterate_commutes` e, por consequência, em
toda a cadeia até a soundness. Provar a comutação e inverter em cada uso
era ruído. O probe confirmou que a prova direta da semiconjugação tem
exatamente o mesmo tamanho.

## Orientação, registrada explicitamente

```text
Function.Semiconj f ga gb  significa  ∀ x, f (ga x) = gb (f x)
```

Logo:

```text
tableIndex_semiconj  :  ∀ s, tableIndex (stepS s) = step (tableIndex s)
table_step_commutes  :  ∀ s, step (tableIndex s) = tableIndex (stepS s)
```

Uma é o `.symm` da outra. Escrever a orientação ao contrário produz falha
de unificação — não é automático, e por isso está congelado aqui.

## Prova principal

```lean
theorem CertifiedFiniteEncoding.tableIndex_semiconj (e) (stepS) :
    Function.Semiconj (e.tableIndex stepS) stepS (buildTransitionTable e stepS).step := by
  intro s
  apply Fin.ext
  rw [ValidatedTransitionTable.step_val, buildTransitionTable_getElem]
  show ((e.encode (stepS s) : Fin n) : Nat)
      = ((e.encode (stepS (e.decode (e.encode s))) : Fin n) : Nat)
  rw [e.decode_encode]
```

Seis linhas. Compilou no probe de revisão.

A igualdade principal permanece em `Fin (buildTransitionTable e stepS).next.size`
— `Fin.ext` é aplicado **dentro** da prova, não no enunciado. Nenhum
enfraquecimento para igualdade entre naturais.

### DAG

```text
ValidatedTransitionTable.step_val           (frente anterior, @[simp])
  -> buildTransitionTable_getElem           (auxiliar interno)
      -> definicao de encodedStep           (por defeq, via show)
          -> decode_encode                  (a lei semanticamente correta)
```

### A lei usada

```text
decode_encode, e nao encode_decode.
```

O termo a eliminar é `decode (encode s)`. `encode_decode` trata de
`encode (decode i)`, o caso oposto, e não se aplica. Congelado.

## Corolário

```lean
theorem CertifiedFiniteEncoding.table_step_commutes (e) (stepS) (s : S) :
    (buildTransitionTable e stepS).step (e.tableIndex stepS s)
      = e.tableIndex stepS (stepS s) :=
  (e.tableIndex_semiconj stepS s).symm
```

## Iteradas

```lean
theorem CertifiedFiniteEncoding.table_iterate_commutes (e) (stepS) (k : Nat) (s : S) :
    ((buildTransitionTable e stepS).step)^[k] (e.tableIndex stepS s)
      = e.tableIndex stepS (stepS^[k] s) :=
  ((e.tableIndex_semiconj stepS).iterate_right k s).symm
```

Um termo, uma linha. `Function.Semiconj.iterate_right`, axiomas
`[propext]`, orientação auditada:

```lean
Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
```

Indução manual **não** é usada e não é permitida enquanto a API existir.
Se ela desaparecer ou mudar de assinatura, a formalização deve registrar
o fato como desvio explícito antes de recorrer à indução.

## Correspondência com `run?`

```lean
theorem CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate (e) (stepS) (k) (s) :
    (buildTransitionTable e stepS).toRaw.run? k ((e.encode s : Fin n) : Nat)
      = some ((e.encode (stepS^[k] s) : Fin n) : Nat)
```

O lado bruto começa no `Nat` produzido por **`encode`**, não por
`tableIndex` — exigência do gate, cumprida. `tableIndex` aparece apenas
dentro da prova.

```text
ValidatedTransitionTable.run?_eq_iterate_step
  -> tableIndex_val, no indice de entrada
      -> table_iterate_commutes
          -> tableIndex_val, no indice de saida
```

Nenhuma segunda função recursiva. `run?` e `step?` não são copiadas.
