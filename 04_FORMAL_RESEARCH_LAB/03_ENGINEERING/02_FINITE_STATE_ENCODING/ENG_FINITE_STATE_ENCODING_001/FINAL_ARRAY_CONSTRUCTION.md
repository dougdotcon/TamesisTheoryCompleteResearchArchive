---
document_id: ENC-FINAL-ARRAY-CONSTRUCTION
supersedes: ENC-TABLE-CONSTRUCTION
stage: SPECIFICATION_REVIEW
frozen: true
---

# Construção final do array

## Construção única

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

Reconfirmada no probe de revisão. A tabela bruta pública é, e será apenas,
`(buildTransitionTable e stepS).toRaw`.

Não existem `buildRawTransitionTable`, `buildValidatedTransitionTable` nem
`transitionArray`.

## Proibições reverificadas

```text
List.toArray        ausente
Fintype.elems       ausente
Finset.univ         ausente
Fintype.equivFin    ausente
Classical.choose    ausente
Trunc.out           ausente
modulo, clamp,
  getD, fallback    ausentes
```

Verificado por `grep` sobre o probe antes da execução: **zero
ocorrências** de qualquer token proibido.

## Tamanho — orientação vinculante

```lean
theorem buildTransitionTable_size (e) (stepS) :
    (buildTransitionTable e stepS).next.size = n :=
  Array.size_ofFn
```

Orientação **`table.next.size = n`**, sem orientação pública concorrente.
`.symm` é permitido localmente e é usado exatamente uma vez, dentro de
`tableIndex`.

O termo direto é mais robusto que qualquer tática aqui, e a revisão
mediu por que: no probe de axiomas,

```text
theorem sizeB1 (f : Fin n → Nat) : (Array.ofFn f).size = n := rfl
  -> error: Not a definitional equality:
     (Array.ofFn f).size is not definitionally equal to n
```

A igualdade **não** é definicional para `n` genérico — ela é teorema. Mas
`Array.size_ofFn` é aceito em modo termo porque a elaboração de termos
desdobra `buildTransitionTable`, o que `rw` e `simp` não fazem.

## Prova de `closed`

Requisitos do gate, verificados:

```text
exatamente um auxiliar central de lookup   SIM, buildTransitionTable_getElem
nenhuma correcao silenciosa                SIM
nenhum fallback                            SIM
nenhum cast disperso                       SIM, dois pontos
nenhuma segunda construcao                 SIM
```

O `show` continua obrigatório: `ValidatedTransitionTable.closed` quantifica
sobre `Fin next.size` e usa o `getElem` indexado por `Fin`, enquanto
`Array.getElem_ofFn` está enunciado sobre índice `Nat` com prova
explícita. Sem a conversão, `rw` não encontra o padrão.

## Validade por construção

`(buildTransitionTable e stepS).closed` **é** a prova de validade
estrutural, e `ValidatedTransitionTable.toRaw_valid` a converte para
`RawTransitionTable.Valid` sem uma linha nova.

`validateTransitionTable` **não** é chamada. Ela permanece na frente
anterior, para dados não confiáveis. Revalidar a tabela construída seria
admitir que a construção pode estar errada — e a construção é justamente
o que esta frente prova.
