import Mathlib.GroupTheory.GroupAction.Defs
import Mathlib.Order.Defs.Unbundled

set_option autoImplicit false

/-!
# FOUND-SEMIGROUP-002 — Alcançabilidade (Camada A)

Alcançabilidade pela **ação completa** do monoide: `∃ m : M, m • x = y`.

Aviso de camada, vinculante: este arquivo é a Camada A. Ele **não** fala
de iteração de um gerador fixo (Camada B) nem de funções sobre tipos
finitos (Camada C). Confundir os níveis é o erro que a especificação
existe para evitar.

`M` é implícito na definição, conforme a especificação; por isso os
enunciados usam `(M := M)` explicitamente, o que também torna visível, em
cada teorema, **sobre qual monoide** a alcançabilidade é afirmada.
-/

namespace TamesisLab.Foundations.FiniteDynamics

/-- `Reachable x y`: existe uma transformação do monoide que leva `x` a `y`.

Quantifica sobre **todo** `M`, não sobre potências de um gerador. -/
def Reachable {M X : Type*} [Monoid M] [MulAction M X] (x y : X) : Prop :=
  ∃ m : M, m • x = y

/-- FSG2-REACH-001 — reflexividade, testemunhada pela identidade do monoide. -/
theorem reachable_refl {M X : Type*} [Monoid M] [MulAction M X] (x : X) :
    Reachable (M := M) x x :=
  ⟨1, one_smul M x⟩

/-- FSG2-REACH-002 — transitividade, testemunhada pela multiplicação.

A ordem segue a convenção já fixada em `FOUND-SEMIGROUP-001`: em
`(n * m) • x = n • (m • x)`, o fator `m` age primeiro. Como `m` leva `x` a
`y` e `n` leva `y` a `z`, a testemunha é `n * m`, **nesta ordem**. -/
theorem reachable_trans {M X : Type*} [Monoid M] [MulAction M X] {x y z : X}
    (hxy : Reachable (M := M) x y) (hyz : Reachable (M := M) y z) :
    Reachable (M := M) x z := by
  obtain ⟨m, hm⟩ := hxy
  obtain ⟨n, hn⟩ := hyz
  refine ⟨n * m, ?_⟩
  rw [mul_smul, hm, hn]

/-- FSG2-REACH-003a — reflexividade empacotada, **sem** instância global.

Usa `Std.Refl`, e não `IsRefl`: na revisão fixada `IsRefl` está depreciada
em favor de `Std.Refl`, com `α` implícito. -/
theorem reachable_isRefl {M X : Type*} [Monoid M] [MulAction M X] :
    Std.Refl (fun a b : X => Reachable (M := M) a b) :=
  ⟨reachable_refl⟩

/-- FSG2-REACH-003b — transitividade empacotada, **sem** instância global.

Nenhuma `instance : Preorder X` é criada. A relação depende de `M`, que
não aparece no tipo `X`; duas ações distintas sobre o mesmo `X` produziriam
instâncias incompatíveis, e `X` frequentemente já possui ordem própria. -/
theorem reachable_isTrans {M X : Type*} [Monoid M] [MulAction M X] :
    IsTrans X (fun a b : X => Reachable (M := M) a b) :=
  ⟨fun _ _ _ => reachable_trans⟩

/-- FSG2-ORBIT-001 — alcançabilidade é exatamente pertinência à órbita.

`MulAction.mem_orbit_iff` é `Iff.rfl` na revisão fixada, logo a ponte é
**definicional**. Nenhuma segunda noção de órbita é criada. -/
theorem reachable_iff_mem_orbit {M X : Type*} [Monoid M] [MulAction M X] {x y : X} :
    Reachable (M := M) x y ↔ y ∈ MulAction.orbit M x :=
  Iff.rfl

end TamesisLab.Foundations.FiniteDynamics
