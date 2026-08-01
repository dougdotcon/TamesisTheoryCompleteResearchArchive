---
document_id: ENC-TABLE-INDEX
anti_correction_theorem: tableIndex_val
probe_status: PROBE_PROVED
---

# `tableIndex` — o ponto decisivo

## Definição

```lean
def CertifiedFiniteEncoding.tableIndex
    (e : CertifiedFiniteEncoding S n) (stepS : S → S) (s : S) :
    Fin (buildTransitionTable e stepS).next.size :=
  Fin.cast (buildTransitionTable_size e stepS).symm (e.encode s)
```

## O teorema anti-correção

```lean
theorem tableIndex_val (e) (stepS) (s : S) :
    ((e.tableIndex stepS s : Fin (buildTransitionTable e stepS).next.size) : Nat)
      = ((e.encode s : Fin n) : Nat) :=
  rfl
```

**Provado por `rfl`.** `Fin.cast` preserva o campo `val`
definicionalmente; o transporte não é um cálculo, é uma reetiquetagem do
limite.

Isto é o análogo direto do `validateStart_sound` da frente anterior — o
teorema que impede a correção silenciosa de um índice. Lá, o índice
pedido tinha de sobreviver à validação; aqui, tem de sobreviver ao
transporte.

```text
igualdade proposicional entre termos Fin NAO basta.
A preservacao do valor Nat eh registrada, e eh por rfl.
```

## Por que `tableIndex_val` é usado duas vezes na cadeia

Ele aparece nos dois extremos de `run?_corresponds_to_typed_iterate`:

```text
a esquerda   converte o indice de entrada de encode s para tableIndex s
a direita    converte o indice de saida de volta para encode (stepS^[k] s)
```

Sem ele, a correspondência com `run?` seria enunciada sobre `tableIndex`,
que é um objeto interno desta frente. Com ele, ela é enunciada sobre
`encode`, que é o que o consumidor forneceu.

## Verificação executável

Com a codificação permutada `i ↦ 3 - i`:

```lean
example : ((permEnc.tableIndex tailStep ⟨0, _⟩ : Fin _) : Nat) = 3 := by decide
```

Passou no probe. O índice do estado `0` é `3`, e o transporte não o
alterou.
