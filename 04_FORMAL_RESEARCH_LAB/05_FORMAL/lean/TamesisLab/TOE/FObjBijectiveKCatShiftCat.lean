import Mathlib.CategoryTheory.Action
import TamesisLab.Foundations.Semigroups.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
import TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
import TamesisLab.TOE.NoSurjectiveReverseFunctorShiftCatKCat

/-!
# TOE-7 — `F.obj : KCat → ShiftCat` é `Bijective`

Item Wave-7 `TOE-7` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-4` (Wave-4,
`KToShiftFunctorNotFaithfulNoReverse.lean`), que constrói `F : KCat ⥤
ShiftCat` com `F.obj p := show ShiftCat from p.back`, e de `TOE-6a`
(Wave-6, `NoSurjectiveReverseFunctorShiftCatKCat.lean`), que já
constrói `e : ShiftCat ≃ KCat := (ActionCategory.objEquiv Shift3
Regime3).symm.trans (ActionCategory.objEquiv K Regime3)`. Este item
observa que `F.obj`, como função `KCat → ShiftCat`, coincide
byte-a-byte (após redução das projeções de `Equiv.trans`/`Equiv.symm`)
com `⇑e.symm`, e conclui `Function.Bijective F.obj` de
`Equiv.bijective e.symm` — sem nenhuma prova nova de bijetividade,
apenas a identificação de `F.obj` com uma equivalência já construída.

## Teste falseável tentado (exatamente este, nada mais amplo)

`theorem F_obj_bijective : Function.Bijective (F.obj : KCat →
ShiftCat)`, via: (1) `F_obj_eq_e_symm : (F.obj : KCat → ShiftCat) =
⇑e.symm`, fechado por `rfl` puro (ambos os lados reduzem
definicionalmente a `fun c => ⟨(), c.back⟩` — verificado, `simp [e,
ActionCategory.objEquiv]` sozinho não fecha, precisa de `rfl` depois;
`rfl` isolado já fecha); (2) reescrita por (1) e `Equiv.bijective
e.symm`.

Citações verificadas por leitura direta do arquivo:
- `Mathlib/Logic/Equiv/Defs.lean:184`: `protected theorem bijective (e
  : α ≃ β) : Bijective e := EquivLike.bijective e`.
- `Mathlib/CategoryTheory/Action.lean:86-90`: `def objEquiv : X ≃
  ActionCategory M X where toFun x := x; invFun x := x.back; ...`.
- `F`, `KCat`, `ShiftCat` reaproveitados byte-a-byte de
  `KToShiftFunctorNotFaithfulNoReverse.lean` (`TOE-4`), não
  redeclarados.
- `e` reaproveitado byte-a-byte de
  `NoSurjectiveReverseFunctorShiftCatKCat.lean` (`TOE-6a`), não
  redeclarado.

## O que este arquivo NÃO estabelece

`K`/`Shift3`/`Regime3` continuam sendo os modelos finitos de brinquedo
de `FOUND-SEMIGROUP-001`/`TOE-3c`, sem significado físico algum.
`Function.Bijective F.obj` é uma propriedade puramente ao nível dos
objetos (as funções entre os dois conjuntos finitos de 3 elementos
subjacentes a `KCat` e `ShiftCat`), não uma alegação sobre `F` como
funtor: `F` já não é `Faithful` (`TOE-4`) nem `Full` (`TOE-6b`) ao
nível dos morfismos, e nada aqui contradiz ou revisita esses fatos —
`F.obj` bijetivo e `F` não pleno/fiel são propriedades logicamente
independentes (a primeira é sobre objetos, as outras sobre Hom-sets).
Nenhuma leitura física é afirmada; nenhuma "assimetria de interface" ou
"seta do tempo categórica" é estabelecida ou refutada aqui. Não
recupera QM/GR/Yang–Mills nem termodinâmica
(`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não produz teorema de
impossibilidade físico nem previsão falseável, e não avança RH nem NS.
Não afirma novidade matemática: identificar uma função com uma
equivalência já construída, e daí herdar sua bijetividade via
`Equiv.bijective`, é uso padrão da Mathlib, não um resultado novo.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.FObjBijectiveKCatShiftCat

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
open TamesisLab.TOE.NoSurjectiveReverseFunctorShiftCatKCat
open CategoryTheory

/-! ## O teste central -/

/-- `F.obj : KCat → ShiftCat` coincide, ponto a ponto, com `⇑e.symm`
(`e : ShiftCat ≃ KCat`, `TOE-6a`): ambos os lados reduzem
definicionalmente a `show ShiftCat from c.back` (`fun c => ⟨(),
c.back⟩` via a instância `CoeTC`, `Action.lean:73-74`) após desdobrar
`Equiv.trans`/`Equiv.symm` e `ActionCategory.objEquiv` — `rfl` puro
fecha. -/
theorem F_obj_eq_e_symm : (F.obj : KCat → ShiftCat) = ⇑e.symm := rfl

/-- O teste central: `F.obj : KCat → ShiftCat` é `Bijective`. Prova:
`F_obj_eq_e_symm` identifica `F.obj` com `⇑e.symm`; `Equiv.bijective
e.symm` dá a bijetividade deste último. -/
theorem F_obj_bijective : Function.Bijective (F.obj : KCat → ShiftCat) :=
  F_obj_eq_e_symm ▸ e.symm.bijective

/-- Registro (trivial) de que o teste falseável fechou: `F.obj : KCat →
ShiftCat` (o funtor "morfismo único" de `TOE-4`, ao nível dos objetos)
é `Bijective`, via identificação com `e.symm` (`TOE-6a`). -/
theorem toe_7_F_obj_bijective : True := trivial

#print axioms F_obj_eq_e_symm
#print axioms F_obj_bijective
#print axioms toe_7_F_obj_bijective

end TamesisLab.TOE.FObjBijectiveKCatShiftCat
