---
document_id: ENC-RAW-RUN-CORRESPONDENCE
probe_status: PROBE_PROVED
---

# Correspondência com a execução bruta

## Enunciado

```lean
theorem run?_corresponds_to_typed_iterate (e) (stepS) (k : Nat) (s : S) :
    (buildTransitionTable e stepS).toRaw.run? k ((e.encode s : Fin n) : Nat)
      = some ((e.encode (stepS^[k] s) : Fin n) : Nat)
```

Este é o teorema que liga os três mundos:

```text
o Array original construido      via toRaw.run?
o Nat produzido por encode       nos dois lados
a trajetoria tipada original     stepS^[k] s
```

## Prova congelada

```lean
  have h := (buildTransitionTable e stepS).run?_eq_iterate_step k (e.tableIndex stepS s)
  rw [tableIndex_val] at h
  rw [h, table_iterate_commutes, tableIndex_val]
```

Três linhas. Compilou no probe.

## DAG

```text
ValidatedTransitionTable.run?_eq_iterate_step   (frente anterior)
    -> tableIndex_val, no indice de entrada
        -> table_iterate_commutes
            -> tableIndex_val, no indice de saida
```

Os dois usos de `tableIndex_val` são o que faz o enunciado falar de
`encode` — o objeto do consumidor — e não de `tableIndex`, que é interno.

## Nenhuma segunda execução

```text
nenhuma funcao recursiva nova;
run? NAO eh copiada;
step? NAO eh copiada;
nenhuma semantica paralela.
```

A frente anterior já provou que `run?` corresponde à iteração de `step`.
Esta frente provou que a iteração de `step` corresponde à iteração de
`stepS`. A composição é o teorema acima — e é composição, não
reimplementação.

## Verificação executável

```text
#eval (buildTransitionTable boolEnc not).toRaw.run? 3 0   ->   some 1
```

`not^[3] false = true`, e `encode true = 1`. Confere.
