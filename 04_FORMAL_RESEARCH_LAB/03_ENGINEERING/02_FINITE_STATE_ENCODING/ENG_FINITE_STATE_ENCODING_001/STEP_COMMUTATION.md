---
document_id: ENC-STEP-COMMUTATION
probe_status: PROBE_PROVED
---

# Comutação de um passo

## Enunciado

```lean
theorem table_step_commutes (e) (stepS) (s : S) :
    (buildTransitionTable e stepS).step (e.tableIndex stepS s)
      = e.tableIndex stepS (stepS s)
```

Igualdade em `Fin (buildTransitionTable e stepS).next.size` — **não**
apenas entre valores naturais. O enfraquecimento para `Nat` não foi
necessário e por isso não é aceito.

## Prova congelada

```lean
  apply Fin.ext
  rw [ValidatedTransitionTable.step_val, buildTransitionTable_getElem]
  show ((e.encode (stepS (e.decode (e.encode s))) : Fin n) : Nat) = _
  rw [e.decode_encode]
  exact (tableIndex_val e stepS (stepS s)).symm
```

Cinco linhas. Compilou no probe.

## DAG

```text
ValidatedTransitionTable.step_val        (frente anterior, @[simp])
    -> buildTransitionTable_getElem      (lema central de leitura)
        -> definicao de encodedStep      (por defeq, via show)
            -> decode_encode             (a lei semanticamente necessaria)
                -> tableIndex_val        (coerencia do cast)
```

## A lei correta

```text
decode_encode, NAO encode_decode.
```

O termo que aparece é `stepS (decode (encode s))`, e o que precisa
desaparecer é `decode (encode s)`. `encode_decode` trata do caso oposto,
`encode (decode i)`, e não se aplica aqui. Usar a lei errada é um erro de
direção que o probe teria rejeitado.

## O `show` intermediário

Ele força a redução de `encodedStep` e de `Fin.cast` simultaneamente, o
que nenhuma tática de reescrita faz sozinha — mesmo padrão do `show` na
construção da tabela e dos dois `show` da frente anterior. Congelado.
