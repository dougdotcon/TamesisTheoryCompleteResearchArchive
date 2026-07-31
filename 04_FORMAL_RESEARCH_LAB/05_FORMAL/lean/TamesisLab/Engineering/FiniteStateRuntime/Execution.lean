import TamesisLab.Engineering.FiniteStateRuntime.Validation
import Mathlib.Logic.Function.Iterate

set_option autoImplicit false

/-!
# ENG-FINITE-STATE-RUNTIME-001 — Execução

Duas semânticas e a ponte entre elas.

```text
step    Fin n -> Fin n     TOTAL, sobre a tabela validada
run?    Nat -> Nat -> ...  PARCIAL, sobre a tabela bruta
```

`run? 0 state = some state` **mesmo quando `state ≥ size`**. Isso não
valida o estado: `run?` é fiel ao array, e a validade da consulta pertence
a `validateStart`, que é a barreira de segurança da API dinâmica.

`run?_eq_iterate_step` é a obrigação técnica principal da frente. Sem ela,
o certificado falaria de um objeto Lean que ninguém consegue relacionar
com o dado de entrada.
-/

namespace TamesisLab.Engineering.FiniteStateRuntime

/-- A função de transição tipada. **É aqui que o dado dinâmico vira
sistema formal.**

Total por construção: o tipo não admite valor de escape, e a validação
garantiu que nenhum é necessário. -/
def ValidatedTransitionTable.step (t : ValidatedTransitionTable) :
    Fin t.next.size → Fin t.next.size :=
  fun i => ⟨t.next[i], t.closed i⟩

/-- A transição tipada é o lookup do array. Coerção explícita. -/
@[simp]
theorem ValidatedTransitionTable.step_val (t : ValidatedTransitionTable)
    (i : Fin t.next.size) :
    (t.step i : Nat) = t.next[i] :=
  rfl

/-- Um passo sobre a tabela bruta. Devolve `none` fora dos limites —
jamais um valor padrão. -/
def RawTransitionTable.step? (t : RawTransitionTable) (state : Nat) :
    Option Nat :=
  t.next[state]?

/-- Execução de exatamente `k` passos sobre a tabela bruta.

O caso zero devolve o estado **sem checar nada**. Para `k > 0`, qualquer
acesso fora do array produz `none`. -/
def RawTransitionTable.run? (t : RawTransitionTable) :
    Nat → Nat → Option Nat
  | 0, state => some state
  | steps + 1, state => do
      let nextState ← t.step? state
      t.run? steps nextState

/-- Ponte de **uma** transição: o lookup opcional na tabela bruta coincide
com a função total no domínio validado. -/
theorem ValidatedTransitionTable.step?_eq_some_step
    (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    t.toRaw.step? (i : Nat) = some ((t.step i : Fin t.next.size) : Nat) := by
  show t.next[(i : Nat)]? = some (t.next[i])
  exact getElem?_pos t.next (i : Nat) i.isLt

/-- **Ponte de iterações.** Executar a tabela bruta `k` vezes a partir de
um estado validado dá o mesmo resultado que iterar a função tipada `k`
vezes.

Três detalhes importam e foram fixados na revisão da especificação:

* o quantificador `∀ start` vem **depois** de `k`, dentro do enunciado —
  não se usa `generalizing`;
* dois `show` são necessários: o primeiro expõe o `bind` que a notação
  `do` esconde, o segundo força a redução de `Option.bind (some a) f`;
* a variante correta é `Function.iterate_succ_apply`, cuja contagem
  externa consome o passo **interno** — que é exatamente a ordem de
  recursão de `run?`. -/
theorem ValidatedTransitionTable.run?_eq_iterate_step
    (t : ValidatedTransitionTable) (k : Nat) :
    ∀ start : Fin t.next.size,
      t.toRaw.run? k (start : Nat) =
        some (((t.step)^[k] start : Fin t.next.size) : Nat) := by
  induction k with
  | zero => intro start; rfl
  | succ k ih =>
      intro start
      show (t.toRaw.step? (start : Nat)).bind (t.toRaw.run? k) = _
      rw [t.step?_eq_some_step start]
      show t.toRaw.run? k ((t.step start : Fin t.next.size) : Nat) = _
      rw [ih (t.step start), Function.iterate_succ_apply]

end TamesisLab.Engineering.FiniteStateRuntime
