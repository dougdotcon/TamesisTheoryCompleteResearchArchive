---
document_id: ENC-ARRAY-CONSTRUCTION-REVIEW
---

# Revisão da construção da tabela

## Construção única

`buildTransitionTable` é a única declaração pública que produz uma
tabela. Busca por concorrentes:

```text
buildRawTransitionTable        0
buildValidatedTransitionTable  0
transitionArray                0
```

Devolve `ValidatedTransitionTable` diretamente; a bruta surge **apenas**
por `.toRaw`.

## `Array.ofFn`

Confirmado no corpo. Proibidos e ausentes: `List.toArray`,
`Fintype.elems`, `Finset.univ`, `Fintype.equivFin`, `Classical.choose`,
`Trunc.out`, módulo, `clamp`, `getD`, fallback.

## `validateTransitionTable` — classificação da menção

```yaml
documentation_reference:
  file: TableConstruction.lean
  line: 11
  context: "docstring que diz que ela NAO eh chamada"
  executable_call: false
  mathematical_dependency: false
  violation: false
```

Medido removendo os blocos `/- … -/` antes de contar: **`0` ocorrências
em código**, `1` em documentação. A menção existe justamente para
registrar a decisão de não chamá-la.

## Tamanho

```lean
@[simp]
theorem buildTransitionTable_size (encoding) (stepS) :
    (buildTransitionTable encoding stepS).next.size = n :=
  Array.size_ofFn
```

Orientação pública **única**, `size = n`. Nenhum lema inverso redundante
existe. `.symm` aparece uma única vez, dentro de `tableIndex`.

## Campo `closed`, linha por linha

```lean
    intro i
    show (Array.ofFn (fun j => ((encoding.encodedStep stepS j : Fin n) : Nat)))[(i : Nat)]'i.isLt
        < (Array.ofFn (fun j => ((encoding.encodedStep stepS j : Fin n) : Nat))).size
    rw [Array.getElem_ofFn]
    exact lt_of_lt_of_eq (Fin.isLt _) Array.size_ofFn.symm
```

Usa exatamente `Array.getElem_ofFn`, `Fin.isLt` e `Array.size_ofFn`.
**Zero correção de valor.** A tabela é válida **por construção**, e
`validateTransitionTable` — o validador de dados não confiáveis —
permanece onde estava.

O `show` continua obrigatório: `closed` quantifica sobre `Fin next.size`
e usa o `getElem` indexado por `Fin`, enquanto `getElem_ofFn` está
enunciado sobre índice `Nat`.
