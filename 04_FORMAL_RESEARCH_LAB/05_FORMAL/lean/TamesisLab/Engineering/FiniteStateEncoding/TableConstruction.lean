import TamesisLab.Engineering.FiniteStateEncoding.Encoding

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — construção da tabela

Uma **única** construção pública, que devolve diretamente uma
`ValidatedTransitionTable`. A tabela bruta é obtida por `.toRaw`.

`validateTransitionTable` **não** é chamada: ela existe para dados não
confiáveis, e a tabela construída aqui é justamente aquilo que esta
frente prova estar correto.

```text
orientacao unica do tamanho   table.next.size = n
ponto publico de transporte   tableIndex
teorema anti-correcao         tableIndex_val, por rfl
```
-/

namespace TamesisLab.Engineering.FiniteStateEncoding

open TamesisLab.Engineering.FiniteStateRuntime

variable {S : Type*} {n : Nat}

/-- A tabela de transições do sistema codificado.

Construída por `Array.ofFn` sobre `encodedStep`, e **validada por
construção**: o campo `closed` é a prova, não uma verificação
posterior.

O `show` da prova não é cosmético. `ValidatedTransitionTable.closed`
quantifica sobre `Fin next.size` e usa o `getElem` indexado por `Fin`,
enquanto `Array.getElem_ofFn` está enunciado sobre índice `Nat` com
prova explícita; sem a conversão, a reescrita não encontra o padrão. -/
def buildTransitionTable (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) : ValidatedTransitionTable :=
  ⟨Array.ofFn (fun i => ((encoding.encodedStep stepS i : Fin n) : Nat)), by
    intro i
    show (Array.ofFn (fun j => ((encoding.encodedStep stepS j : Fin n) : Nat)))[(i : Nat)]'i.isLt
        < (Array.ofFn (fun j => ((encoding.encodedStep stepS j : Fin n) : Nat))).size
    rw [Array.getElem_ofFn]
    exact lt_of_lt_of_eq (Fin.isLt _) Array.size_ofFn.symm⟩

/-- O tamanho da tabela é o parâmetro da codificação.

Orientação pública **única**: `size = n`. Onde a inversa for
necessária, usa-se `.symm` desta igualdade.

A prova é um termo. A igualdade **não** é definicional para `n`
genérico — `(Array.ofFn f).size` só reduz a `n` quando `n` é literal —,
mas a elaboração de termos desdobra `buildTransitionTable`, o que as
táticas de reescrita, em transparência reduzida, não fazem. -/
@[simp]
theorem buildTransitionTable_size (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) :
    (buildTransitionTable encoding stepS).next.size = n :=
  Array.size_ofFn

/-- O índice da tabela correspondente a um estado.

**Único ponto público de transporte** `Fin n → Fin table.next.size`.

`stepS` aparece porque o **tipo de retorno** menciona a tabela
construída para ele; o **valor natural** do índice não depende de
`stepS`, e é isso que `tableIndex_val` demonstra. -/
def CertifiedFiniteEncoding.tableIndex (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (s : S) : Fin (buildTransitionTable encoding stepS).next.size :=
  Fin.cast (buildTransitionTable_size encoding stepS).symm (encoding.encode s)

/-- **Teorema anti-correção da frente.**

O transporte não modifica o índice natural. É `rfl`: `Fin.cast`
preserva o campo `val` definicionalmente, e não depende de axioma
nenhum.

Análogo direto de `validateStart_sound` na frente anterior — lá o
índice pedido tinha de sobreviver à validação; aqui, ao transporte. -/
@[simp]
theorem CertifiedFiniteEncoding.tableIndex_val (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (s : S) :
    ((encoding.tableIndex stepS s :
        Fin (buildTransitionTable encoding stepS).next.size) : Nat)
      = ((encoding.encode s : Fin n) : Nat) :=
  rfl

end TamesisLab.Engineering.FiniteStateEncoding
