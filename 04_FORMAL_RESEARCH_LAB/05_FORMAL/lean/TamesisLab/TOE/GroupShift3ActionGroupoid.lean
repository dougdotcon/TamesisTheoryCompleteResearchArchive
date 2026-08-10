import Mathlib.CategoryTheory.Action
import TamesisLab.Foundations.Semigroups.Action

/-!
# TOE-3A — `Group Shift3` desbloqueando `Groupoid (ActionCategory Shift3 Regime3)`

Item Wave-2 `TOE-3a` (síntese TOE, extensão do laboratório, não Clay).
Sucessor direto de `TOE-1`/`TOE-2` (Wave-1) e do diagnóstico de
obsolescência do `TOE-3` original registrado em
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md` (`Shift3` age livre e
simplesmente transitivamente sobre `Regime3` — um torsor de grupo cíclico
de ordem 3, não apenas um monoide agindo). Zero dependência de RH/NS.

## Teste falseável tentado (exatamente este, nada mais amplo)

Construir `instance : Group Shift3`, lendo o inverso de cada transição
diretamente da tabela de `Shift3.comp` já confirmada em
`TamesisLab.Foundations.Semigroups.Regime3` (`Regime3.lean:63-70`):

```
comp forward  forward2 = identity   -- forward⁻¹  = forward2
comp forward2 forward  = identity   -- forward2⁻¹ = forward
comp identity identity = identity   -- identity⁻¹ = identity
```

e, com essa instância em escopo, confirmar que a instância genérica da
Mathlib

```
instance : Groupoid (ActionCategory G X) := CategoryTheory.groupoidOfElements _
```

(`CategoryTheory/Action.lean:139-140`, sob `variable {G} [Group G]
[MulAction G X]`, linha 137) resolve sem atrito para
`Groupoid (ActionCategory Shift3 Regime3)`, usando a `MulAction Shift3
Regime3` já verificada em `Foundations/Semigroups/Action.lean:31-34`
(FOUND-SEMIGROUP-001). Nenhuma instância `Groupoid` é redeclarada aqui —
a Mathlib já a fornece genericamente; este arquivo apenas fornece o
`Group Shift3` que faltava para ela disparar, e confirma via `inferInstance`
que de fato dispara.

## O que este arquivo NÃO estabelece

`Shift3`/`Regime3` continuam sendo o modelo finito de brinquedo de
FOUND-SEMIGROUP-001, sem significado físico. `Groupoid (ActionCategory
Shift3 Regime3)` é uma categoria de brinquedo com 3 objetos cujos Hom-sets
são todos singletons (torsor livre e transitivo — ver diagnóstico do
`TOE-3` original no plano de ataque da Onda 2); a "invertibilidade" aqui
provada é a de um grupo cíclico de ordem 3 concreto, não uma alegação
sobre reversibilidade física de nenhum tipo. Não recupera QM/GR/Yang–Mills
nem termodinâmica (`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não
produz teorema de impossibilidade nem previsão falseável, e não avança
RH nem NS.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.GroupShift3ActionGroupoid

open TamesisLab.Foundations.Semigroups
open CategoryTheory

/-- Inversa explícita de cada transição, lida diretamente da tabela de
`Shift3.comp` confirmada em `Regime3.lean:63-70`: `identity` é sua própria
inversa, `forward` e `forward2` são inversas uma da outra. -/
def shift3Inv : Shift3 → Shift3
  | .identity => .identity
  | .forward => .forward2
  | .forward2 => .forward

/-- `shift3Inv a * a = 1` para todo `a`, verificado por análise finita
exaustiva (3 casos) sobre a tabela de `Shift3.comp` já fechada — mesmo
idioma `revert`/`decide` já usado em `Theorems.lean` (FOUND-SG-002 e
FOUND-SG-005). Aqui `*` e `1` já denotam `Shift3.comp`/`Shift3.identity`
via a instância `Monoid Shift3` de `Foundations/Semigroups/Action.lean`,
que esta prova reutiliza (não reconstrói). -/
theorem shift3_inv_mul_cancel (a : Shift3) : shift3Inv a * a = 1 := by
  revert a; decide

/-- FOUND-SG-002/003/004 (via `Monoid Shift3`, `Action.lean:22-27`) somados
a `shift3Inv`/`shift3_inv_mul_cancel` fecham exatamente os dados exigidos
por `Group` (`Algebra/Group/Defs.lean:1219-1220`): os campos de
`DivInvMonoid` além de `inv` (`div`, `zpow`, `zpow_zero'`, `zpow_succ'`,
`zpow_neg'`) têm valor-padrão na própria classe da Mathlib e não precisam
ser fornecidos. A instância `Monoid Shift3` já registrada é reaproveitada
via atualização de estrutura (`{ ... with ... }`), não redeclarada. -/
instance shift3Group : Group Shift3 :=
  { (inferInstance : Monoid Shift3) with
    inv := shift3Inv
    inv_mul_cancel := shift3_inv_mul_cancel }

-- Verificações pontuais de que `Inv Shift3` corresponde exatamente à
-- tabela lida em `Regime3.lean:63-70`.
example : (Shift3.forward)⁻¹ = Shift3.forward2 := rfl
example : (Shift3.forward2)⁻¹ = Shift3.forward := rfl
example : (Shift3.identity)⁻¹ = Shift3.identity := rfl

/-- O teste central: com `Group Shift3` em escopo (e `MulAction Shift3
Regime3` já existente), a instância genérica da Mathlib
`CategoryTheory.groupoidOfElements` (`Action.lean:139-140`) resolve sem
nenhuma construção adicional local para `Groupoid (ActionCategory Shift3
Regime3)`. Nenhuma instância `Groupoid` é declarada por este arquivo —
apenas confirmada via `inferInstance`, contra a instância genérica já
fornecida pela Mathlib. -/
abbrev actionGroupoidResolved : Groupoid (ActionCategory Shift3 Regime3) := inferInstance

/-- Registro (trivial) de que o teste falseável fechou. -/
theorem toe_3a_group_shift3_unlocks_action_groupoid : True := trivial

#print axioms shift3Inv
#print axioms shift3_inv_mul_cancel
#print axioms shift3Group
#print axioms actionGroupoidResolved
#print axioms toe_3a_group_shift3_unlocks_action_groupoid

end TamesisLab.TOE.GroupShift3ActionGroupoid
