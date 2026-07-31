import TamesisLab.Foundations.FiniteDynamics.Reachability

set_option autoImplicit false

/-!
# FOUND-SEMIGROUP-002 — Invariantes (Camada A)

Duas noções distintas, com nomes distintos:

* `IsInvariant I` — invariância sob **toda** a ação;
* `IsInvariantUnder a I` — invariância sob **um** elemento `a`.

## Correção de especificação (obrigatória)

A redação anterior dizia que `IsInvariantUnder a` seria "estritamente mais
fraca" que `IsInvariant`. Isso está **errado como afirmação universal**. O
enunciado correto é:

```text
IsInvariant I  implica  IsInvariantUnder a I,  para todo a.

IsInvariantUnder a PODE ser estritamente mais fraca que IsInvariant, em
acoes apropriadas.

A estrita fraqueza NAO vale uniformemente para toda acao e todo a.
```

Contraexemplo à universalidade da estrita fraqueza: se `M` é gerado por
`a`, então `IsInvariantUnder a I` implica `IsInvariant I` — as duas noções
coincidem. Portanto a implicação `IsInvariant → IsInvariantUnder` é o único
sentido demonstrável em geral, e é o que este arquivo prova
(`IsInvariant.under`). A recíproca **não** é enunciada.
-/

namespace TamesisLab.Foundations.FiniteDynamics

/-- Invariante sob a ação **completa** do monoide. -/
def IsInvariant {M X A : Type*} [Monoid M] [MulAction M X] (I : X → A) : Prop :=
  ∀ (m : M) (x : X), I (m • x) = I x

/-- Invariante sob **um** elemento `a` do monoide. -/
def IsInvariantUnder {M X A : Type*} [Monoid M] [MulAction M X]
    (a : M) (I : X → A) : Prop :=
  ∀ x : X, I (a • x) = I x

/-- FSG2-INV-001 — invariância total implica invariância sob cada elemento.

**Uma implicação, não uma equivalência.** A recíproca é falsa em geral, mas
verdadeira quando `a` gera `M`; por isso nenhuma afirmação universal de
estrita fraqueza é feita aqui. -/
theorem IsInvariant.under {M X A : Type*} [Monoid M] [MulAction M X]
    {I : X → A} (hI : IsInvariant (M := M) I) (a : M) :
    IsInvariantUnder (M := M) a I :=
  fun x => hI a x

/-- FSG2-INV-002 — um invariante total é constante ao longo da
alcançabilidade.

Direção única: o invariante **refuta** alcançabilidade quando difere; ele
nunca a demonstra. Ver `CE-005`. -/
theorem IsInvariant.of_reachable {M X A : Type*} [Monoid M] [MulAction M X]
    {I : X → A} (hI : IsInvariant (M := M) I) {x y : X}
    (hxy : Reachable (M := M) x y) :
    I y = I x := by
  obtain ⟨m, hm⟩ := hxy
  rw [← hm]
  exact hI m x

/-- FSG2-INV-003 — invariância sob `a` propaga-se a todas as potências. -/
theorem IsInvariantUnder.pow {M X A : Type*} [Monoid M] [MulAction M X]
    {a : M} {I : X → A} (hI : IsInvariantUnder (M := M) a I) (n : ℕ) (x : X) :
    I (a ^ n • x) = I x := by
  induction n generalizing x with
  | zero => rw [pow_zero, one_smul]
  | succ n ih => rw [pow_succ, mul_smul, ih (a • x), hI]

end TamesisLab.Foundations.FiniteDynamics
