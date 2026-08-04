import TamesisLab.Foundations.Invariants.Definitions
import TamesisLab.Foundations.FiniteStateAbstraction.Abstraction

set_option autoImplicit false

/-!
# FOUND-INVARIANT-UNREACHABILITY-001 — a ferramenta

O teorema que o laboratório não tinha: **um invariante que separa dois
estados prova que um não alcança o outro**.

```text
abstract x != abstract y   ->   nao existe k com stepC^[k] x = y
```

É a forma geral de todo argumento de paridade, coloração ou monovariante.

## A assimetria, que precisa sobreviver

```text
suficiencia   PROVADA aqui
necessidade   NAO afirmada, e NAO decorre
```

Exibir um invariante que separa é trabalho de quem quer a conclusão. A
recíproca é vacuamente verdadeira pelo invariante mais fino — a própria
relação de alcançabilidade — e por isso não diz nada. Ver `INV-GAP-001`.
-/

namespace TamesisLab.Foundations.Invariants

open TamesisLab.Foundations.FiniteStateAbstraction

variable {C A B : Type*}

/-- **A ferramenta de impossibilidade.**

Se um invariante distingue `x` de `y`, então `y` não é alcançável a
partir de `x`, por nenhum número de passos.

Nenhuma finitude é usada. `C` pode ser infinito, e na instância desta
frente ele é. -/
theorem unreachable_of_invariant_ne {abstract : C → A} {stepC : C → C}
    (h : Invariant abstract stepC) {x y : C}
    (hne : abstract x ≠ abstract y) : ¬ Reachable stepC x y := by
  rintro ⟨k, rfl⟩
  exact hne (h.iterate k x).symm

/-- Invariantes compõem: o par de dois invariantes é invariante.

Permite refinar o poder de separação sem construir nada novo — dois
invariantes fracos separam mais do que cada um sozinho. -/
theorem Invariant.pair {f : C → A} {g : C → B} {stepC : C → C}
    (hf : Invariant f stepC) (hg : Invariant g stepC) :
    Invariant (fun c => (f c, g c)) stepC := by
  intro c
  simp [hf c, hg c]

/-- Todo invariante **é** uma abstração certificada, sobre o sistema
abstrato parado.

Esta é a ponte com a cadeia de dez frentes. Ela existe para tornar
verificável o teorema negativo de `CollapseLimit.lean`, não para
sugerir que a análise abstrata seja útil aqui — `CollapseLimit.lean`
prova que não é. -/
def invariantAbstraction {abstract : C → A} {stepC : C → C}
    (h : Invariant abstract stepC) :
    CertifiedFiniteAbstraction C A stepC id :=
  { abstract := abstract, commutes := h.semiconj }

end TamesisLab.Foundations.Invariants
