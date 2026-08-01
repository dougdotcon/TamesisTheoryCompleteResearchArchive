---
document_id: ENC-SEMICONJUGATION-REVIEW
primary_result: CertifiedFiniteEncoding.tableIndex_semiconj
---

# Revisão da semiconjugação e das comutações

## Orientação, conferida no enunciado

```text
Function.Semiconj f ga gb  significa  ∀ x, f (ga x) = gb (f x)
```

Com `f = tableIndex`, `ga = stepS`, `gb = table.step`:

```text
tableIndex (stepS s) = table.step (tableIndex s)
```

É a orientação exigida, e é a que o arquivo tem.

## A prova, linha por linha

```lean
  intro s
  apply Fin.ext
  rw [ValidatedTransitionTable.step_val, buildTransitionTable_getElem]
  show ((encoding.encode (stepS s) : Fin n) : Nat)
      = ((encoding.encode (stepS (encoding.decode (encoding.encode s))) : Fin n) : Nat)
  rw [encoding.decode_encode]
```

| Exigência | Verificado |
|---|---|
| lei usada | **`decode_encode`** |
| `encode_decode` na prova | **ausente** em `Commutation.lean` |
| `DecidableEq S` | ausente |
| `Fintype S` | ausente |
| conclusão só em `Nat` | não — `Fin.ext` é aplicado **dentro** da prova |
| terceiro transporte | nenhum |

```yaml
category: PUBLIC_SPECIFICATION_CORE
semantic_role: PRIMARY_COMMUTATION_RESULT
```

## Corolário de um passo

```lean
theorem CertifiedFiniteEncoding.table_step_commutes (encoding) (stepS) (s) :
    ... := (encoding.tableIndex_semiconj stepS s).symm
```

Derivado **por simetria**, uma linha. Não existe segunda prova
independente. `PUBLIC_COROLLARY`.

## Iteradas

```lean
theorem CertifiedFiniteEncoding.table_iterate_commutes (encoding) (stepS) (k) (s) :
    ... := ((encoding.tableIndex_semiconj stepS).iterate_right k s).symm
```

`Function.Semiconj.iterate_right` usado diretamente. **Nenhuma indução
manual**, nenhuma segunda semântica, orientação correta, conclusão em
`Fin (buildTransitionTable encoding stepS).next.size`.

## Correspondência com `run?`

```lean
  have h := (buildTransitionTable encoding stepS).run?_eq_iterate_step k
    (encoding.tableIndex stepS s)
  rw [encoding.tableIndex_val stepS s] at h
  rw [h, encoding.table_iterate_commutes stepS k s,
      encoding.tableIndex_val stepS (stepS^[k] s)]
```

DAG conferido:

```text
ValidatedTransitionTable.run?_eq_iterate_step
  -> tableIndex_val, entrada
      -> table_iterate_commutes
          -> tableIndex_val, saida
```

O lado bruto começa em `(encoding.encode s : Nat)` — o objeto do
consumidor. `tableIndex` **não** é exigido de quem chama.

```text
run? copiado        nao
step? copiado       nao
nova recursao       nao
```
