import Mathlib.CategoryTheory.Action
import TamesisLab.Foundations.Semigroups.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
import TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse

/-!
# TOE-5 — Nenhum funtor reverso injetivo `G : ShiftCat ⥤ KCat` existe
(generalização, sem hipótese fixando objetos)

Item Wave-5 `TOE-5` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-4` (Wave-4,
`KToShiftFunctorNotFaithfulNoReverse.lean`), cujo
`no_reverse_functor_with_fixed_objects` só é provado sob a hipótese
explícita `hG : ∀ p, G.obj p = show KCat from p.back` — a própria seção
"O que este arquivo NÃO estabelece" desse arquivo (linhas 81-84) nomeia
explicitamente o caso irrestrito como fora de escopo. Este item ataca
exatamente essa lacuna, substituindo `hG` por uma hipótese estritamente
mais fraca: apenas `Function.Injective G.obj`.

## Teste falseável tentado (exatamente este, nada mais amplo)

`theorem no_injective_reverse_functor (G : ShiftCat ⥤ KCat) (hinj :
Function.Injective G.obj) : False`, via:

(1) `homK_nonempty_iff (x y : Regime3) : (∃ m : K, m • x = y) ↔ y = x ∨
y = Regime3.alpha` — análise finita exaustiva (`revert x y; decide`),
lida diretamente de `Kact` (`Kact .identity r = r`, `Kact .k _ =
.alpha`, `MonoidKConstantActionDistinctEndomorphisms.lean:148-150`): o
único jeito de `m • x = y` é `m = identity ∧ y = x`, ou `m = k ∧ y =
alpha` (para qualquer `x`).

(2) `σ : Regime3 → Regime3 := fun x => (G.obj (show ShiftCat from
x)).back` é injetivo, a partir de `hinj`: `ActionCategory.back` é
injetivo em qualquer `ActionCategory M X` (via `back_coe`,
`Action.lean:80-81`, provado abaixo como `actionCategory_back_injective`
— fato genérico da Mathlib, não específico deste modelo), e o mergulho
`x ↦ show ShiftCat from x` é invertido por `.back` (`coe_back`,
`Action.lean:76-78`); compondo as duas injetividades com `hinj`
(aplicado ao objeto de `ShiftCat`) dá injetividade de `σ`.

(3) Para `p := gamma, q := beta` e (simetricamente) `p := beta, q :=
gamma`: `shiftCat_hom_nonempty` (já disponível de
`KToShiftFunctorNotFaithfulNoReverse.lean:170-171`, provado para TODO
par ordenado de objetos de `ShiftCat`, não apenas `beta`/`gamma`) dá um
morfismo `p ⟶ q` em `ShiftCat`; `G.map` desse morfismo, lido via
`hom_as_subtype` (`Action.lean:92`, `rfl`), dá `∃ m : K, m • σ p = σ q`;
por (1), isso força `σ q = σ p ∨ σ q = alpha`. Aplicando isso às duas
escolhas simétricas de `(p,q)` acima força `σ beta = σ gamma ∨ σ beta =
alpha` e `σ gamma = σ beta ∨ σ gamma = alpha`; como `beta ≠ gamma` e `σ`
é injetivo (2), `σ beta ≠ σ gamma`, o que colapsa as duas disjunções em
`σ beta = alpha` e `σ gamma = alpha`, logo `σ beta = σ gamma` —
contradizendo diretamente `σ beta ≠ σ gamma`. Nenhum uso de
`Finite.injective_iff_bijective`: a contradição é extraída diretamente
da injetividade de `σ` sobre o par `(beta, gamma)`, sem passar por
bijetividade/sobrejetividade de `σ` em geral.

Citações verificadas por leitura direta do arquivo:
- `CategoryTheory/Action.lean:92`: `hom_as_subtype`, `(p ⟶ q) = {m : M
  // m • p.back = q.back}`, prova `rfl`.
- `CategoryTheory/Action.lean:76-78`: `coe_back (x : X) :
  ActionCategory.back (x : ActionCategory M X) = x`, `rfl`.
- `CategoryTheory/Action.lean:80-81`: `back_coe (x : ActionCategory M
  X) : ↑x.back = x`, prova por `cases x; rfl`.
- `K`, `Kact`, `KCat` reaproveitados byte-a-byte de
  `MonoidKConstantActionDistinctEndomorphisms.lean` (`TOE-3c`), não
  redeclarados.
- `ShiftCat`, `shiftCat_hom_nonempty` reaproveitados byte-a-byte de
  `KToShiftFunctorNotFaithfulNoReverse.lean` (`TOE-4`), não
  redeclarados.
- `Shift3`, `Regime3`, a instância `MulAction Shift3 Regime3`
  reaproveitados de `Foundations/Semigroups/{Regime3,Action}.lean`, não
  redeclarados.

## O que este arquivo NÃO estabelece

`K`/`Shift3`/`Regime3` continuam sendo os modelos finitos de brinquedo
de `FOUND-SEMIGROUP-001`/`TOE-3c`, sem significado físico algum. A
inexistência de `G : ShiftCat ⥤ KCat` com `G.obj` injetivo é uma
propriedade combinatória de duas categorias de brinquedo com 3 objetos
cada (essencialmente um argumento de "casas de pombo" sobre 3
elementos), não uma alegação física de "assimetria de interface", "seta
do tempo categórica" ou análogo — nenhuma leitura física é afirmada.
Este resultado é estritamente mais forte do que
`no_reverse_functor_with_fixed_objects` (`TOE-4`) no sentido de que a
hipótese é mais fraca (`Function.Injective G.obj` em vez de `∀ p, G.obj
p = show KCat from p.back`), mas continua sendo um fato de teoria de
categorias elementar sobre um modelo de brinquedo de 3 objetos, não uma
alegação de novidade matemática. Não recupera QM/GR/Yang–Mills nem
termodinâmica (`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não
produz teorema de impossibilidade físico nem previsão falseável, e não
avança RH nem NS. Não afirma novidade matemática.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.NoInjectiveReverseFunctorShiftCatKCat

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
open CategoryTheory

/-! ## (1) `homK_nonempty_iff` — caracterização exaustiva de `Hom_K` -/

/-- (1) `Hom_K(x,y)` é não vazio sse `y = x` (via `identity`) ou `y =
alpha` (via `k`, que colapsa qualquer origem em `alpha`, `Kact .k _ =
.alpha`). Análise finita exaustiva (3 × 3 = 9 casos para `(x,y)`, cada
um decidindo sobre os 2 elementos de `K`), mesmo idioma `revert`/`decide`
já usado em `shift3_free`/`homK_beta_gamma_no_witness`
(`KToShiftFunctorNotFaithfulNoReverse.lean:109-117`). -/
theorem homK_nonempty_iff (x y : Regime3) :
    (∃ m : K, m • x = y) ↔ y = x ∨ y = Regime3.alpha := by
  revert x y; decide

/-! ## (2) `σ` e sua injetividade -/

/-- Fato genérico (não específico deste modelo): `ActionCategory.back`
é injetivo em qualquer `ActionCategory M X`. Prova: `back_coe`
(`Action.lean:80-81`) diz `↑x.back = x` para todo `x : ActionCategory M
X`; se `a.back = b.back`, reescrever `back_coe a` por essa igualdade dá
`↑b.back = a`, que combinado com `back_coe b` (`↑b.back = b`) dá `a =
b`. -/
theorem actionCategory_back_injective {M : Type*} [Monoid M] {X : Type*}
    [MulAction M X] :
    Function.Injective (ActionCategory.back : ActionCategory M X → X) := by
  intro a b hab
  have ha := ActionCategory.back_coe a
  have hb := ActionCategory.back_coe b
  rw [hab] at ha
  exact ha.symm.trans hb

/-- `σ`: dado um funtor `G : ShiftCat ⥤ KCat`, `σ x` é o `Regime3`
subjacente à imagem por `G.obj` do objeto de `ShiftCat` correspondente a
`x` (via o mergulho `show ShiftCat from x`). -/
def sigma (G : ShiftCat ⥤ KCat) (x : Regime3) : Regime3 :=
  (G.obj (show ShiftCat from x)).back

/-- (2) `σ` é injetivo, dado que `G.obj` é injetivo. Prova: de `σ x = σ
y`, `actionCategory_back_injective` (aplicado em `KCat`) dá `G.obj (show
ShiftCat from x) = G.obj (show ShiftCat from y)`; `hinj` dá `show
ShiftCat from x = show ShiftCat from y`; aplicando `.back` a ambos os
lados e `coe_back` (`Action.lean:76-78`, `(show ShiftCat from x).back =
x`) a cada lado dá `x = y`. -/
theorem sigma_injective (G : ShiftCat ⥤ KCat) (hinj : Function.Injective G.obj) :
    Function.Injective (sigma G) := by
  intro x y hxy
  have hobj : G.obj (show ShiftCat from x) = G.obj (show ShiftCat from y) :=
    actionCategory_back_injective hxy
  have hcoe : (show ShiftCat from x) = (show ShiftCat from y) := hinj hobj
  calc x = (show ShiftCat from x).back := (ActionCategory.coe_back x).symm
    _ = (show ShiftCat from y).back := by rw [hcoe]
    _ = y := ActionCategory.coe_back y

/-! ## (3) O teste central -/

/-- Para todo par `(x,y) : Regime3 × Regime3`, existe `m : K` com `m •
σ x = σ y`. Prova: `shiftCat_hom_nonempty` (já disponível de `TOE-4`,
provado para TODO par ordenado de objetos de `ShiftCat`) dá um morfismo
`f : (show ShiftCat from x) ⟶ (show ShiftCat from y)`; `G.map f` é (via
`hom_as_subtype`, `Action.lean:92`, `rfl`) exatamente um par `⟨m, m • σ
x = σ y⟩`. -/
theorem sigma_hom_nonempty (G : ShiftCat ⥤ KCat) (x y : Regime3) :
    ∃ m : K, m • sigma G x = sigma G y := by
  obtain ⟨f⟩ := shiftCat_hom_nonempty (show ShiftCat from x) (show ShiftCat from y)
  have gmap :
      G.obj (show ShiftCat from x) ⟶ G.obj (show ShiftCat from y) :=
    G.map f
  exact ⟨gmap.val, gmap.property⟩

/-- O teste central: nenhum `G : ShiftCat ⥤ KCat` com `G.obj` injetivo
existe. Prova: com `σ := sigma G` injetivo (`sigma_injective`), aplicar
`sigma_hom_nonempty` + `homK_nonempty_iff` a `(gamma,beta)` dá `σ beta =
σ gamma ∨ σ beta = alpha`; aplicado (simetricamente) a `(beta,gamma)` dá
`σ gamma = σ beta ∨ σ gamma = alpha`. Como `beta ≠ gamma` e `σ` é
injetivo, `σ beta ≠ σ gamma`; isso descarta o ramo esquerdo de ambas as
disjunções, forçando `σ beta = alpha = σ gamma`, logo `σ beta = σ
gamma` — contradizendo diretamente `σ beta ≠ σ gamma`. Nenhum uso de
`Finite.injective_iff_bijective`. -/
theorem no_injective_reverse_functor (G : ShiftCat ⥤ KCat)
    (hinj : Function.Injective G.obj) : False := by
  have hsig : Function.Injective (sigma G) := sigma_injective G hinj
  have h1 :=
    (homK_nonempty_iff (sigma G Regime3.gamma) (sigma G Regime3.beta)).mp
      (sigma_hom_nonempty G Regime3.gamma Regime3.beta)
  have h2 :=
    (homK_nonempty_iff (sigma G Regime3.beta) (sigma G Regime3.gamma)).mp
      (sigma_hom_nonempty G Regime3.beta Regime3.gamma)
  have hne : sigma G Regime3.beta ≠ sigma G Regime3.gamma := by
    intro h
    exact (by decide : Regime3.beta ≠ Regime3.gamma) (hsig h)
  rcases h1 with h1 | h1
  · exact hne h1
  · rcases h2 with h2 | h2
    · exact hne h2.symm
    · exact hne (h1.trans h2.symm)

/-- Registro (trivial) de que o teste falseável fechou: nenhum `G :
ShiftCat ⥤ KCat` com `G.obj` injetivo existe — generalização de
`no_reverse_functor_with_fixed_objects` (`TOE-4`), substituindo a
hipótese `hG` (objetos fixados) por `hinj : Function.Injective G.obj`
(estritamente mais fraca). -/
theorem toe_5_no_injective_reverse_functor : True := trivial

#print axioms homK_nonempty_iff
#print axioms actionCategory_back_injective
#print axioms sigma
#print axioms sigma_injective
#print axioms sigma_hom_nonempty
#print axioms no_injective_reverse_functor
#print axioms toe_5_no_injective_reverse_functor

end TamesisLab.TOE.NoInjectiveReverseFunctorShiftCatKCat
