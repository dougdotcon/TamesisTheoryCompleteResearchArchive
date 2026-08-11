import Mathlib.CategoryTheory.Action
import Mathlib.CategoryTheory.Functor.FullyFaithful
import TamesisLab.Foundations.Semigroups.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
import TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse

/-!
# TOE-6b — `F : KCat ⥤ ShiftCat` não é `Full`

Item Wave-6 `TOE-6b` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-4` (Wave-4,
`KToShiftFunctorNotFaithfulNoReverse.lean`), que já prova `F_not_faithful
: ¬ Functor.Faithful F` para o funtor "morfismo único" `F : KCat ⥤
ShiftCat`, mas nunca examina a outra propriedade padrão de funtores
plenos/fiéis, `Full`. Este item ataca exatamente essa lacuna: mostrar
que `F` também não é `Full`.

## Teste falseável tentado (exatamente este, nada mais amplo)

`theorem F_not_full (hF : F.Full) : False`, via:

(1) `shiftCat_hom_nonempty` (já disponível de
`KToShiftFunctorNotFaithfulNoReverse.lean:170-171`, provado para TODO
par ordenado de objetos de `ShiftCat`) aplicado ao par `(F.obj (show
KCat from beta), F.obj (show KCat from gamma))` dá um morfismo `g :
F.obj (show KCat from beta) ⟶ F.obj (show KCat from gamma)` em
`ShiftCat`.

(2) Sob a hipótese `hF : F.Full` (`class Full (F : C ⥤ D) : Prop where
map_surjective {X Y : C} : Function.Surjective (F.map (X := X) (Y :=
Y))`, `CategoryTheory/Functor/FullyFaithful.lean:45-46`),
`hF.map_surjective g` (padrão de notação-ponto legítimo do próprio
Mathlib, `FullyFaithful.lean:74-76`) dá `f : (show KCat from beta) ⟶
(show KCat from gamma)` com `F.map f = g` — os implícitos `X Y : KCat`
de `map_surjective` são resolvidos por unificação com o tipo de `g`,
que já está sintaticamente na forma `F.obj (show KCat from beta) ⟶
F.obj (show KCat from gamma)`.

(3) `f` habita `(show KCat from beta) ⟶ (show KCat from gamma)`, que é
exatamente `homK_beta_gamma_isEmpty` (`KToShiftFunctorNotFaithfulNoReverse.lean:123-125`)
— contradição direta via `IsEmpty.false`.

O argumento é, no fundo, elementar: uma função saindo de um domínio
vazio (`Hom_K(beta,gamma) = ∅`) não pode sobrejetar sobre um codomínio
não vazio (`Hom_Shift(F.obj beta, F.obj gamma)`, sempre habitado por
`shiftCat_hom_nonempty`).

Citações verificadas por leitura direta do arquivo:
- `CategoryTheory/Functor/FullyFaithful.lean:45-46`: `class Full (F : C
  ⥤ D) : Prop where map_surjective {X Y : C} : Function.Surjective
  (F.map (X := X) (Y := Y))`.
- `CategoryTheory/Functor/FullyFaithful.lean:74-76`: `theorem
  map_surjective (F : C ⥤ D) [Full F] : Function.Surjective (F.map :
  (X ⟶ Y) → (F.obj X ⟶ F.obj Y)) := Full.map_surjective` — mesmo padrão
  de notação-ponto `hF.map_surjective` reutilizado aqui.
- `F`, `shiftCat_hom_nonempty`, `homK_beta_gamma_isEmpty` reaproveitados
  byte-a-byte de `KToShiftFunctorNotFaithfulNoReverse.lean` (`TOE-4`),
  não redeclarados.
- `K`, `Kact`, `KCat` reaproveitados byte-a-byte de
  `MonoidKConstantActionDistinctEndomorphisms.lean` (`TOE-3c`), não
  redeclarados.
- `Shift3`, `Regime3`, a instância `MulAction Shift3 Regime3`
  reaproveitados de `Foundations/Semigroups/{Regime3,Action}.lean`, não
  redeclarados.

## O que este arquivo NÃO estabelece

`K`/`Shift3`/`Regime3` continuam sendo os modelos finitos de brinquedo
de `FOUND-SEMIGROUP-001`/`TOE-3c`, sem significado físico algum. `F`
não ser `Full` é uma propriedade combinatória do funtor "morfismo
único" construído em `TOE-4` entre duas categorias de brinquedo de 3
objetos (consequência direta de `Hom_K(beta,gamma)` ser vazio enquanto
`Hom_Shift` nunca é vazio), não uma alegação física de "assimetria de
interface", "seta do tempo categórica" ou análogo — nenhuma leitura
física é afirmada. Este resultado não generaliza `F_not_faithful`
(`TOE-4`) nem é generalizado por ele: `Full` e `Faithful` são
propriedades logicamente independentes de um funtor, e este arquivo
prova apenas a falha de `Full`, sob o `F` específico já construído em
`TOE-4` (não um funtor arbitrário `KCat ⥤ ShiftCat`). Não recupera
QM/GR/Yang–Mills nem termodinâmica (`THEORY_RECOVERY_MATRIX.md`, tudo
`UNRESOLVED`), não produz teorema de impossibilidade físico nem
previsão falseável, e não avança RH nem NS. Não afirma novidade
matemática: "uma função de um Hom-set vazio para um Hom-set não vazio
não pode ser sobrejetiva" é um fato elementar de teoria de conjuntos,
usado aqui como está.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.FNotFullKCatShiftCat

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
open CategoryTheory

/-! ## O teste central -/

/-- O teste central: `F : KCat ⥤ ShiftCat` (o funtor "morfismo único" de
`TOE-4`) não é `Full`. Prova: `shiftCat_hom_nonempty` dá um morfismo `g
: F.obj (show KCat from beta) ⟶ F.obj (show KCat from gamma)` em
`ShiftCat` (sempre existe, `TOE-4`); sob `hF : F.Full`,
`hF.map_surjective g` dá um preimagem `f : (show KCat from beta) ⟶
(show KCat from gamma)` em `KCat`; mas esse Hom-set é vazio
(`homK_beta_gamma_isEmpty`, `TOE-4`) — contradição via
`IsEmpty.false`. -/
theorem F_not_full (hF : F.Full) : False := by
  obtain ⟨g⟩ :=
    shiftCat_hom_nonempty (F.obj (show KCat from Regime3.beta))
      (F.obj (show KCat from Regime3.gamma))
  obtain ⟨f, _⟩ := hF.map_surjective g
  exact homK_beta_gamma_isEmpty.false f

/-- Registro (trivial) de que o teste falseável fechou: `F : KCat ⥤
ShiftCat` (o funtor "morfismo único" de `TOE-4`) não é `Full` —
complemento independente de `F_not_faithful` (`TOE-4`), mesma
observação de fundo (`Hom_K(beta,gamma) = ∅`, `Hom_Shift` sempre não
vazio), propriedade categórica diferente. -/
theorem toe_6b_F_not_full : True := trivial

#print axioms F_not_full
#print axioms toe_6b_F_not_full

end TamesisLab.TOE.FNotFullKCatShiftCat
