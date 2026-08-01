---
document_id: ENC-TABLE-CONSTRUCTION
probe_status: PROBE_PROVED
---

# Construção da tabela

## Assinatura única

```lean
def buildTransitionTable (e : CertifiedFiniteEncoding S n) (stepS : S → S) :
    ValidatedTransitionTable :=
  ⟨Array.ofFn (fun i => ((e.encodedStep stepS i : Fin n) : Nat)), by
    intro i
    show (Array.ofFn (fun j => ((e.encodedStep stepS j : Fin n) : Nat)))[(i : Nat)]'i.isLt
        < (Array.ofFn (fun j => ((e.encodedStep stepS j : Fin n) : Nat))).size
    rw [Array.getElem_ofFn]
    exact lt_of_lt_of_eq (Fin.isLt _) Array.size_ofFn.symm⟩
```

**Compilou no probe.** Uma única construção pública; a tabela bruta é
`(buildTransitionTable e stepS).toRaw`.

## Por que `Array.ofFn`

```text
computavel                 sim
axiomas                    [propext]
#eval                      #[1, 2, 3] no probe do portfolio
tamanho provavel           Array.size_ofFn
leitura provavel           Array.getElem_ofFn
```

Proibidos, e nenhum foi usado: `List.toArray` de enumeração manual,
`Fintype.elems`, `Finset.univ`, escolha clássica, fallback, módulo,
`clamp`.

## O `show` não é cosmético

A prova de `closed` recebe `i : Fin (Array.ofFn f).size` e o objetivo usa
o `getElem` **indexado por `Fin`**. `Array.getElem_ofFn` está enunciado
sobre índice `Nat` com prova explícita. Sem o `show` que converte a
forma, `rw [Array.getElem_ofFn]` **falha** — medido: *"Did not find an
occurrence of the pattern"*.

Esse é o mesmo padrão que a frente anterior descobriu para o `bind` da
notação `do`: a conversão explícita é obrigatória, e fica congelada aqui
para que a formalização não a redescubra.

## Validade por construção

O campo `closed` da estrutura **é** a prova de validade. Consequência
direta:

```lean
(buildTransitionTable e stepS).toRaw_valid
```

já fornece `RawTransitionTable.Valid`, reutilizando o teorema da frente
anterior sem uma linha nova.

`validateTransitionTable` **não** é chamada. Ela existe para dados não
confiáveis; a tabela construída aqui não é dado não confiável, e
revalidá-la seria admitir que a construção pode estar errada.

## Ordem dos valores

```text
next[i] = (encode (stepS (decode i)) : Nat)
```

O índice `i` **é** o estado, na codificação fornecida. Não há
reordenação, não há normalização, não há escolha de representante.
Medido com codificação permutada `i ↦ 3 - i` sobre `0 → 1 → 2 → 3 → 2`:

```text
#[1, 0, 1, 2]
```

que é exatamente `3 - tailStep (3 - j)` para cada `j`.
