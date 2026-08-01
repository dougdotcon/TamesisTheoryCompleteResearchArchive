import TamesisLab.Engineering.FiniteStateEncoding.TableConstruction

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-ENCODING-001 — comutações

A **semiconjugação** é o resultado semântico principal; a comutação de
um passo é seu corolário. A ordem importa: a forma que
`Function.Semiconj.iterate_right` consome é a semiconjugação, e provar a
comutação primeiro obrigaria a inverter em cada uso.

```text
Function.Semiconj f ga gb  significa  ∀ x, f (ga x) = gb (f x)
```

Aqui:

```text
tableIndex_semiconj  :  tableIndex (stepS s) = step (tableIndex s)
table_step_commutes  :  step (tableIndex s) = tableIndex (stepS s)
```

Uma é o `.symm` da outra, e escrever a orientação ao contrário produz
falha de unificação.

A lei inversa usada é **`decode_encode`**. O termo a eliminar é
`decode (encode s)`; `encode_decode` trata do caso oposto e não se
aplica.
-/

namespace TamesisLab.Engineering.FiniteStateEncoding

open TamesisLab.Engineering.FiniteStateRuntime

variable {S : Type*} {n : Nat}

/-- Leitura da tabela construída, com o índice transportado de volta.

Segundo — e último — ponto de transporte, `Fin table.next.size → Fin n`,
e o único que não é público. Termo de uma linha, por igualdade
definicional: `simp`, `unfold` e `rw` **não** provam este enunciado,
porque trabalham em transparência reduzida.

Encapsula uma redução, não uma afirmação: nenhuma hipótese matemática é
acrescentada. -/
private theorem buildTransitionTable_getElem (encoding : CertifiedFiniteEncoding S n)
    (stepS : S → S) (i : Fin (buildTransitionTable encoding stepS).next.size) :
    (buildTransitionTable encoding stepS).next[i]
      = ((encoding.encodedStep stepS
          (Fin.cast (buildTransitionTable_size encoding stepS) i) : Fin n) : Nat) :=
  Array.getElem_ofFn (f := fun j => ((encoding.encodedStep stepS j : Fin n) : Nat)) i.isLt

/-- **Resultado semântico principal.**

O índice da tabela semiconjuga a dinâmica tipada com o passo da tabela.
A igualdade é em `Fin (buildTransitionTable encoding stepS).next.size`;
`Fin.ext` é aplicado dentro da prova, e o enunciado **não** é enfraquecido
para igualdade entre valores naturais. -/
theorem CertifiedFiniteEncoding.tableIndex_semiconj
    (encoding : CertifiedFiniteEncoding S n) (stepS : S → S) :
    Function.Semiconj (encoding.tableIndex stepS) stepS
      (buildTransitionTable encoding stepS).step := by
  intro s
  apply Fin.ext
  rw [ValidatedTransitionTable.step_val, buildTransitionTable_getElem]
  show ((encoding.encode (stepS s) : Fin n) : Nat)
      = ((encoding.encode (stepS (encoding.decode (encoding.encode s))) : Fin n) : Nat)
  rw [encoding.decode_encode]

/-- Corolário legível: o passo da tabela comuta com o passo tipado.

Não é provado de novo — é o `.symm` da semiconjugação. -/
theorem CertifiedFiniteEncoding.table_step_commutes
    (encoding : CertifiedFiniteEncoding S n) (stepS : S → S) (s : S) :
    (buildTransitionTable encoding stepS).step (encoding.tableIndex stepS s)
      = encoding.tableIndex stepS (stepS s) :=
  (encoding.tableIndex_semiconj stepS s).symm

/-- Comutação de iteradas, para todo `k`.

Um termo. `Function.Semiconj.iterate_right` já encapsula a indução — na
frente anterior, o resultado análogo custou indução manual com
quantificador no enunciado e dois `show` obrigatórios. -/
theorem CertifiedFiniteEncoding.table_iterate_commutes
    (encoding : CertifiedFiniteEncoding S n) (stepS : S → S) (k : Nat) (s : S) :
    ((buildTransitionTable encoding stepS).step)^[k] (encoding.tableIndex stepS s)
      = encoding.tableIndex stepS (stepS^[k] s) :=
  ((encoding.tableIndex_semiconj stepS).iterate_right k s).symm

/-- A execução bruta da tabela construída **é** a trajetória tipada.

O lado bruto começa no `Nat` produzido por `encode` — o objeto que o
consumidor forneceu —, e não num índice interno. `tableIndex` aparece
apenas dentro da prova.

Nenhuma segunda semântica de execução é criada: `run?` e `step?` são
consumidos da frente anterior, não copiados. -/
theorem CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
    (encoding : CertifiedFiniteEncoding S n) (stepS : S → S) (k : Nat) (s : S) :
    (buildTransitionTable encoding stepS).toRaw.run? k ((encoding.encode s : Fin n) : Nat)
      = some ((encoding.encode (stepS^[k] s) : Fin n) : Nat) := by
  have h := (buildTransitionTable encoding stepS).run?_eq_iterate_step k
    (encoding.tableIndex stepS s)
  rw [encoding.tableIndex_val stepS s] at h
  rw [h, encoding.table_iterate_commutes stepS k s,
      encoding.tableIndex_val stepS (stepS^[k] s)]

end TamesisLab.Engineering.FiniteStateEncoding
