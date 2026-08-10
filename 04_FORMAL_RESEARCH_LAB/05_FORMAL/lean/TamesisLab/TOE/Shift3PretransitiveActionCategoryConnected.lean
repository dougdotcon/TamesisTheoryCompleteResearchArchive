import Mathlib.CategoryTheory.Action
import TamesisLab.Foundations.Semigroups.Action

/-!
# TOE-3B — `MulAction.IsPretransitive Shift3 Regime3` desbloqueando
`IsConnected (ActionCategory Shift3 Regime3)`

Item Wave-2 `TOE-3b` (síntese TOE, extensão do laboratório, não Clay).
Sucessor direto de `TOE-1` (Wave-1, `ActionCategoryRegime3.lean`) e irmão
de `TOE-3a` (Wave-2, `GroupShift3ActionGroupoid.lean`); os três exploram
consequências estruturais diferentes da mesma descoberta registrada no
diagnóstico de obsolescência do `TOE-3` original em
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`: `Shift3` age livre e
transitivamente sobre `Regime3`. Zero dependência de RH/NS.

## Teste falseável tentado (exatamente este, nada mais amplo)

Instanciar `MulAction.IsPretransitive Shift3 Regime3` a partir de
`apply_transitive` (`Theorems.lean:66-68`), que é definicionalmente igual
a `MulAction.IsPretransitive.exists_smul_eq` já que `smul := Shift3.apply`
por definição (`Foundations/Semigroups/Action.lean:31-34`). Com essa
instância em escopo, mais `Nonempty Regime3 := ⟨.alpha⟩` (trivial),
confirmar que a instância genérica da Mathlib

```
instance [IsPretransitive M X] [Nonempty X] : IsConnected (ActionCategory M X)
```

(`CategoryTheory/Action.lean:130-133`) resolve sem atrito para
`IsConnected (ActionCategory Shift3 Regime3)`. Nenhuma instância
`IsConnected` é redeclarada aqui — a Mathlib já a fornece genericamente;
este arquivo apenas fornece o `IsPretransitive Shift3 Regime3` e o
`Nonempty Regime3` que faltavam para ela disparar, e confirma via
`inferInstance` que de fato dispara.

## O que este arquivo NÃO estabelece

`Shift3`/`Regime3` continuam sendo o modelo finito de brinquedo de
FOUND-SEMIGROUP-001, sem significado físico. `IsConnected` é a noção
categórica de alcançabilidade por zigue-zague de morfismos/inversos
formais (`CategoryTheory.IsConnected`, ver `zigzag_isConnected`), não uma
alegação física de "regime conectado" ou "interface conectada" apesar da
sobreposição de vocabulário — nenhuma leitura física é afirmada. Não
recupera QM/GR/Yang–Mills nem termodinâmica
(`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não produz teorema de
impossibilidade nem previsão falseável, e não avança RH nem NS.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.Shift3PretransitiveActionCategoryConnected

open TamesisLab.Foundations.Semigroups
open CategoryTheory

/-- `Shift3` age pretransitivamente sobre `Regime3`: para quaisquer
regimes `x` e `y` existe uma transição `s` com `s • x = y`. Reaproveita
`apply_transitive` (`Theorems.lean:66-68`, FOUND-SG-013) sem redemonstrar
a análise finita — `s • x` e `s.apply x` são definicionalmente iguais via
a instância `MulAction Shift3 Regime3` (`Action.lean:31-34`, `smul :=
Shift3.apply`), então `apply_transitive` já tem exatamente o tipo exigido
pelo campo `exists_smul_eq` da classe. -/
instance shift3IsPretransitive : MulAction.IsPretransitive Shift3 Regime3 where
  exists_smul_eq := apply_transitive

-- `Regime3` é não vazio: `alpha` é um testemunho explícito.
instance : Nonempty Regime3 := ⟨.alpha⟩

/-- O teste central: com `IsPretransitive Shift3 Regime3` e `Nonempty
Regime3` em escopo, a instância genérica da Mathlib
(`CategoryTheory/Action.lean:130-133`) resolve sem nenhuma construção
adicional local para `IsConnected (ActionCategory Shift3 Regime3)`.
Nenhuma instância `IsConnected` é declarada por este arquivo — apenas
confirmada via `inferInstance`, contra a instância genérica já fornecida
pela Mathlib. -/
abbrev actionCategoryConnectedResolved :
    IsConnected (ActionCategory Shift3 Regime3) := inferInstance

/-- Registro (trivial) de que o teste falseável fechou. -/
theorem toe_3b_pretransitive_unlocks_action_category_connected : True := trivial

#print axioms shift3IsPretransitive
#print axioms actionCategoryConnectedResolved
#print axioms toe_3b_pretransitive_unlocks_action_category_connected

end TamesisLab.TOE.Shift3PretransitiveActionCategoryConnected
