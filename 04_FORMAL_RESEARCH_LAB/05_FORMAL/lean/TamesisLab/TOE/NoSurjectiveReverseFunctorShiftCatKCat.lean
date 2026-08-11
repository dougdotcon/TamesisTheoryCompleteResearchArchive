import Mathlib.CategoryTheory.Action
import Mathlib.Data.Fintype.Card
import TamesisLab.Foundations.Semigroups.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
import TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
import TamesisLab.TOE.NoInjectiveReverseFunctorShiftCatKCat

/-!
# TOE-6a — Nenhum funtor reverso sobrejetivo `G : ShiftCat ⥤ KCat` existe
(dual sobrejetivo direto de `TOE-5`)

Item Wave-6 `TOE-6a` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-5` (Wave-5,
`NoInjectiveReverseFunctorShiftCatKCat.lean`), cujo
`no_injective_reverse_functor` proíbe qualquer `G : ShiftCat ⥤ KCat`
com `G.obj` injetivo. Este item ataca o dual sobrejetivo exato: proibir
qualquer `G` com `G.obj` sobrejetivo, convertendo a hipótese de
sobrejetividade em injetividade via a equivalência de cardinalidade
finita `ShiftCat ≃ KCat` (ambas categorias de ação de 3 objetos) e
fechando pelo resultado já provado de `TOE-5`.

## Teste falseável tentado (exatamente este, nada mais amplo)

`theorem no_surjective_reverse_functor (G : ShiftCat ⥤ KCat) (hsurj :
Function.Surjective G.obj) : False`, via:

(1) `e : ShiftCat ≃ KCat := (ActionCategory.objEquiv Shift3
Regime3).symm.trans (ActionCategory.objEquiv K Regime3)` — composição de
duas instâncias de `ActionCategory.objEquiv` (`Action.lean:86`,
`objEquiv M X : X ≃ ActionCategory M X`), uma para cada modelo de
brinquedo (`Shift3 ↻ Regime3` dá `ShiftCat`, `K ↻ Regime3` dá `KCat`),
ambas já citadas e usadas em `TOE-5`.

(2) `haveI : Finite ShiftCat := Finite.of_equiv Regime3
(ActionCategory.objEquiv Shift3 Regime3)` (`Finite/Defs.lean:110`,
`Finite.of_equiv (α : Sort*) [Finite α] (f : α ≃ β) : Finite β`) —
`Finite Regime3` vem de graça da instância `Fintype Regime3`
(`Foundations/Semigroups/Regime3.lean:33`).

(3) Converter `hsurj : Function.Surjective G.obj` em `Function.Injective
G.obj` via `(Finite.injective_iff_surjective_of_equiv e).mpr hsurj`
(`Data/Fintype/Card.lean:348`, `theorem
Finite.injective_iff_surjective_of_equiv {f : α → β} (e : α ≃ β)
[Finite α] : Injective f ↔ Surjective f`, aqui com `α := ShiftCat`,
`β := KCat`, `f := G.obj`).

(4) Fechar diretamente via `no_injective_reverse_functor G` (`TOE-5`,
já provado, reaproveitado byte-a-byte, não redemonstrado).

Citações verificadas por leitura direta do arquivo:
- `CategoryTheory/Action.lean:86`: `def objEquiv : X ≃ ActionCategory M
  X`, com `left_inv := coe_back`, `right_inv := back_coe` (linhas
  77/81).
- `Mathlib/Data/Fintype/Card.lean:348`: `theorem
  Finite.injective_iff_surjective_of_equiv {f : α → β} (e : α ≃ β)
  [Finite α] : Injective f ↔ Surjective f` (dentro de `namespace
  Finite`, `variable [Finite α]` na linha 322).
- `Mathlib/Data/Finite/Defs.lean:110`: `theorem Finite.of_equiv (α :
  Sort*) [h : Finite α] (f : α ≃ β) : Finite β`.
- `K`, `Kact`, `KCat` reaproveitados byte-a-byte de
  `MonoidKConstantActionDistinctEndomorphisms.lean` (`TOE-3c`), não
  redeclarados.
- `ShiftCat` reaproveitado byte-a-byte de
  `KToShiftFunctorNotFaithfulNoReverse.lean` (`TOE-4`), não
  redeclarado.
- `no_injective_reverse_functor` reaproveitado byte-a-byte de
  `NoInjectiveReverseFunctorShiftCatKCat.lean` (`TOE-5`), não
  redemonstrado.
- `Shift3`, `Regime3`, a instância `MulAction Shift3 Regime3`
  reaproveitados de `Foundations/Semigroups/{Regime3,Action}.lean`, não
  redeclarados.

## O que este arquivo NÃO estabelece

`K`/`Shift3`/`Regime3` continuam sendo os modelos finitos de brinquedo
de `FOUND-SEMIGROUP-001`/`TOE-3c`, sem significado físico algum. A
inexistência de `G : ShiftCat ⥤ KCat` com `G.obj` sobrejetivo é uma
propriedade combinatória de duas categorias de brinquedo com 3 objetos
cada (consequência direta, via cardinalidade finita igual, do fato de
`TOE-5`), não uma alegação física de "assimetria de interface", "seta
do tempo categórica" ou análogo — nenhuma leitura física é afirmada.
Este resultado não é logicamente mais forte do que `no_injective_reverse_functor`
(`TOE-5`): sobrejetividade e injetividade de `G.obj` são equivalentes
apenas porque `ShiftCat` e `KCat` têm a mesma cardinalidade finita
(3), uma propriedade específica deste par de modelos de brinquedo, não
um fato genérico sobre funtores quaisquer. Não recupera QM/GR/Yang–Mills
nem termodinâmica (`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não
produz teorema de impossibilidade físico nem previsão falseável, e não
avança RH nem NS. Não afirma novidade matemática: a equivalência
`Injective ↔ Surjective` entre tipos finitos equipotentes é um fato
padrão da Mathlib (`Finite.injective_iff_surjective_of_equiv`), usado
aqui como está, não generalizado nem reprovado.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.NoSurjectiveReverseFunctorShiftCatKCat

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
open TamesisLab.TOE.NoInjectiveReverseFunctorShiftCatKCat
open CategoryTheory

/-! ## (1) A equivalência de cardinalidade `ShiftCat ≃ KCat` -/

/-- `e`: `ShiftCat` e `KCat` são ambas equipotentes a `Regime3` (via
`ActionCategory.objEquiv`, `Action.lean:86`), portanto equipotentes
entre si. Composição de duas instâncias já citadas em `TOE-5`, nenhuma
maquinaria nova. -/
def e : ShiftCat ≃ KCat :=
  (ActionCategory.objEquiv Shift3 Regime3).symm.trans
    (ActionCategory.objEquiv K Regime3)

/-! ## (2)-(4) O teste central -/

/-- O teste central: nenhum `G : ShiftCat ⥤ KCat` com `G.obj`
sobrejetivo existe. Prova: `Finite ShiftCat` via `Finite.of_equiv`
aplicado a `objEquiv Shift3 Regime3` (`Regime3` é finito por
`Fintype`); `Finite.injective_iff_surjective_of_equiv e` converte
`hsurj` em `Function.Injective G.obj`; fecha-se via
`no_injective_reverse_functor` (`TOE-5`, já provado, sem
redemonstração). -/
theorem no_surjective_reverse_functor (G : ShiftCat ⥤ KCat)
    (hsurj : Function.Surjective G.obj) : False := by
  haveI : Finite ShiftCat :=
    Finite.of_equiv Regime3 (ActionCategory.objEquiv Shift3 Regime3)
  exact no_injective_reverse_functor G
    ((Finite.injective_iff_surjective_of_equiv e).mpr hsurj)

/-- Registro (trivial) de que o teste falseável fechou: nenhum `G :
ShiftCat ⥤ KCat` com `G.obj` sobrejetivo existe — dual sobrejetivo
direto de `no_injective_reverse_functor` (`TOE-5`), via a equivalência
de cardinalidade finita `ShiftCat ≃ KCat`. -/
theorem toe_6a_no_surjective_reverse_functor : True := trivial

#print axioms e
#print axioms no_surjective_reverse_functor
#print axioms toe_6a_no_surjective_reverse_functor

end TamesisLab.TOE.NoSurjectiveReverseFunctorShiftCatKCat
