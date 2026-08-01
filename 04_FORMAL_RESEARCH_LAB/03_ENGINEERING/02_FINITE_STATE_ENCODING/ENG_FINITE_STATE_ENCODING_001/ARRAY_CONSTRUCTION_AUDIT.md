---
document_id: ENC-ARRAY-CONSTRUCTION-AUDIT
---

# Auditoria da construção do array

## Construção única, como implementada

```lean
def buildTransitionTable (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) : ValidatedTransitionTable :=
  ⟨Array.ofFn (fun i => ((encoding.encodedStep stepS i : Fin n) : Nat)), by
    intro i
    show (Array.ofFn (fun j => ((encoding.encodedStep stepS j : Fin n) : Nat)))[(i : Nat)]'i.isLt
        < (Array.ofFn (fun j => ((encoding.encodedStep stepS j : Fin n) : Nat))).size
    rw [Array.getElem_ofFn]
    exact lt_of_lt_of_eq (Fin.isLt _) Array.size_ofFn.symm⟩
```

## Ausências verificadas por busca

```text
buildRawTransitionTable        0
buildValidatedTransitionTable  0
transitionArray                0
List.toArray                   0
Fintype.elems                  0
Finset.univ                    0
Fintype.equivFin               0
Classical.choose               0
Trunc.out                      0
modulo, clamp, getD, fallback  0
```

`validateTransitionTable`: **1 ocorrência, em docstring**, na frase que
diz que ela não é chamada. Chamadas reais, medidas após remover os blocos
de documentação: **0**.

## Validade por construção

O campo `closed` **é** a prova. `ValidatedTransitionTable.toRaw_valid` a
converte para `RawTransitionTable.Valid` sem uma linha nova, e é
exatamente isso que a completeness consome.

Revalidar a tabela construída seria admitir que a construção pode estar
errada — e a construção é o que esta frente prova.

## O `show` continua obrigatório

`ValidatedTransitionTable.closed` quantifica sobre `Fin next.size` e usa
o `getElem` indexado por `Fin`; `Array.getElem_ofFn` está enunciado sobre
índice `Nat` com prova explícita. Sem a conversão, `rw` não encontra o
padrão — comportamento medido na revisão e reconfirmado aqui.

## Tamanho

```lean
@[simp]
theorem buildTransitionTable_size (encoding) (stepS) :
    (buildTransitionTable encoding stepS).next.size = n :=
  Array.size_ofFn
```

Orientação pública única `size = n`. `.symm` aparece **uma única vez**,
dentro de `tableIndex`.

A igualdade **não** é definicional para `n` genérico; o termo funciona
porque a elaboração de termos desdobra `buildTransitionTable`, o que as
táticas de reescrita não fazem.

## Ordem dos valores

```text
next[i] = (encode (stepS (decode i)) : Nat)
```

Sem reordenação, sem normalização, sem escolha de representante. Medido
com codificação permutada `i ↦ 3 - i` sobre `0 → 1 → 2 → 3 → 2`:

```text
identidade  #[1, 2, 3, 2]
permutada   #[1, 0, 1, 2]
```
