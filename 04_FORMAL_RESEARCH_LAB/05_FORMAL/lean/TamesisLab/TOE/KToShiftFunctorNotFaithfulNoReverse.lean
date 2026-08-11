import Mathlib.CategoryTheory.Action
import Mathlib.CategoryTheory.Functor.FullyFaithful
import TamesisLab.Foundations.Semigroups.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms

/-!
# TOE-4 — Comparação funtorial entre o "mundo-`Shift3`" e o "mundo-`K`":
`F : KCat ⥤ ShiftCat` não é `Faithful`, e nenhum `G : ShiftCat ⥤ KCat` com
`G.obj p = show KCat from p.back` existe

Item Wave-4 `TOE-4` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-3c`/`TOE-3d`/`TOE-3e` (Wave-2/Wave-3,
`MonoidKConstantActionDistinctEndomorphisms.lean`,
`HomKNotIsoActionCategoryK.lean`,
`MonoidKNonPretransitiveZigzagConnected.lean`), que fixaram o monoide de
brinquedo `K = {identity, k}` (`k` idempotente, absorvente, distinto de
`identity`), a `MulAction K Regime3` com `Kact .identity r = r`,
`Kact .k _ = .alpha`, e `KCat := ActionCategory K Regime3`; e de `TOE-3a`/
`TOE-3b` (Wave-2, `GroupShift3ActionGroupoid.lean`,
`Shift3PretransitiveActionCategoryConnected.lean`), que estabeleceram que
`Shift3` (monoide cíclico de 3 transições, `Foundations/Semigroups/Regime3.lean`)
age livre e simplesmente transitivamente sobre `Regime3` (torsor de grupo
cíclico de ordem 3). Zero dependência de RH/NS.

## Teste falseável tentado (exatamente este, nada mais amplo)

Porta de entrada: dois `decide` autônomos.

(a) Liberdade de `Shift3` nos três pontos-base de `Regime3` (`alpha`,
`beta`, `gamma`, que esgotam `Regime3`): `∀ x m₁ m₂, m₁ • x = m₂ • x → m₁ = m₂`
(`shift3_free` abaixo).

(b) `Hom_K(beta,gamma) = ∅` em `KCat`: nenhum `m : K` satisfaz
`m • beta = gamma` (`homK_beta_gamma_no_witness`/`homK_beta_gamma_isEmpty`
abaixo).

Depois, construir `F : KCat ⥤ ShiftCat` (funtor "morfismo único"): como
`ShiftCat := ActionCategory Shift3 Regime3` tem, para cada par de objetos
`p q`, um Hom-set que é `Nonempty` (transitividade de `Shift3`,
`apply_transitive`, `Theorems.lean:66-68`) e `Subsingleton` (liberdade,
item (a) acima — dois escalares que levam o mesmo ponto ao mesmo destino
são iguais), o campo `map` é definido por uma **tabela de casos explícita**
(`shiftBetween`, 9 casos, lida diretamente da tabela `Shift3.apply` de
`Regime3.lean:52-59`), não por `Classical.choice`/`Nonempty.some` aplicado
à instância `Nonempty`. `map_id`/`map_comp` decorrem então de
`Subsingleton.elim`, já que o Hom-set alvo tem no máximo um elemento.
Prova-se `¬ Faithful F` exibindo `homIdentity ≠ homK`
(`homIdentity_ne_homK`, `TOE-3c`) que `F.map` colapsa ambos ao único
elemento de `Hom_Shift(alpha,alpha)` — de fato `F.map homIdentity = F.map
homK` por `rfl`, já que `F.map` (por construção via `shiftBetween`) só
depende dos objetos-fonte/destino, não do rótulo `K` do morfismo dado.

Depois, fixando explicitamente a hipótese `G.obj p = show KCat from p.back`
para todo `p : ShiftCat`, prova-se que nenhum tal `G : ShiftCat ⥤ KCat`
existe: o morfismo `beta ⟶ gamma` de `Shift3` (testemunho `Shift3.forward`,
`Shift3.forward.apply Regime3.beta = Regime3.gamma` por `rfl`,
`Regime3.lean:54-56`) precisaria de imagem por `G.map` em
`Hom_K(beta,gamma)`, que é vazio por (b) — contradição.

Citações verificadas por leitura direta do arquivo:
- `CategoryTheory/Action.lean:92`: `hom_as_subtype`, `(p ⟶ q) = {m : M //
  m • p.back = q.back}`, prova `rfl`.
- `CategoryTheory/Action.lean:76-81`: `coe_back`/`back_coe`, ambas `rfl`.
- `CategoryTheory/Functor/FullyFaithful.lean:52-56`: `class Faithful (F :
  C ⥤ D) : Prop where map_injective : ∀ {X Y}, Function.Injective
  (F.map : (X ⟶ Y) → (F.obj X ⟶ F.obj Y))`.
- `K`, `Kmul`, `Kact`, `KCat`, `homIdentity`, `homK`, `homIdentity_ne_homK`
  reaproveitados byte-a-byte de `MonoidKConstantActionDistinctEndomorphisms.lean`
  (`TOE-3c`), não redeclarados.
- `Shift3`, `Regime3`, a instância `MulAction Shift3 Regime3` reaproveitados
  de `Foundations/Semigroups/{Regime3,Action}.lean`, não redeclarados.

## O que este arquivo NÃO estabelece

`K`/`Shift3`/`Regime3` continuam sendo os modelos finitos de brinquedo de
`FOUND-SEMIGROUP-001`/`TOE-3c`, sem significado físico algum. `F` não ser
`Faithful` e a inexistência de `G` (sob a hipótese explícita fixada sobre
objetos) são propriedades combinatórias de duas categorias de brinquedo com
3 objetos cada, não alegações físicas de "assimetria de interface",
"seta do tempo categórica" ou análogo — nenhuma leitura física é afirmada.
A inexistência de `G` provada aqui é condicional à hipótese explícita
`G.obj p = show KCat from p.back`; não se afirma (nem se tenta provar) a
inexistência de *qualquer* funtor `ShiftCat ⥤ KCat` sem essa restrição
sobre objetos — esse é um teste estritamente mais amplo, fora do escopo
falseável tentado aqui. Não recupera QM/GR/Yang–Mills nem termodinâmica
(`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não produz teorema de
impossibilidade físico nem previsão falseável, e não avança RH nem NS. Não
afirma novidade matemática: um funtor "morfismo único" para uma categoria
de Hom-sets singleton, e a obstrução de Hom-set vazio para funtores com
objetos fixados, são fatos padrão de teoria de categorias elementar.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open CategoryTheory

/-! ## Porta de entrada — dois `decide` autônomos -/

/-- (a) Liberdade de `Shift3` nos três pontos-base de `Regime3` (que
esgotam `Regime3` — não há um quarto ponto): se dois escalares `m₁ m₂ :
Shift3` levam o mesmo ponto `x` ao mesmo destino, então `m₁ = m₂`. Análise
finita exaustiva (3 × 3 × 3 = 27 casos, mesmo idioma `revert`/`decide` já
usado em `apply_faithful`, `Theorems.lean:59-61`, e em `TOE-3a`/`TOE-3c`). -/
theorem shift3_free (x : Regime3) (m1 m2 : Shift3) :
    m1 • x = m2 • x → m1 = m2 := by
  revert x m1 m2; decide

/-- (b) Nenhum `m : K` satisfaz `m • beta = gamma`: `Hom_K(beta,gamma)` é
vazio. Análise finita exaustiva (2 casos: `Kact .identity beta = beta ≠
gamma`, `Kact .k beta = alpha ≠ gamma`). -/
theorem homK_beta_gamma_no_witness : ¬ ∃ m : K, m • Regime3.beta = Regime3.gamma := by
  decide

/-- (b), reformulado no nível do `Hom`-set de `KCat` propriamente dito
(`hom_as_subtype`, `Action.lean:92`, `rfl`): `Hom_K(beta,gamma)` está
vazio — não apenas "não há testemunho de `K`", mas o próprio tipo `Hom`
não tem habitante. -/
theorem homK_beta_gamma_isEmpty :
    IsEmpty ((show KCat from Regime3.beta) ⟶ (show KCat from Regime3.gamma)) :=
  ⟨fun f => homK_beta_gamma_no_witness ⟨f.val, f.property⟩⟩

/-! ## `ShiftCat` — a categoria de ação induzida por `Shift3 ↻ Regime3`

Mesma construção genérica da Mathlib já usada para `KCat` (`TOE-3c`,
`MonoidKConstantActionDistinctEndomorphisms.lean:172`) e para `RegimeCat`
(`TOE-1`, `ActionCategoryRegime3.lean:54`), aplicada aqui a `Shift3 ↻
Regime3` sob o nome `ShiftCat` pedido pelo teste — não redeclara a ação,
apenas nomeia a categoria de ação já disponível via
`Foundations/Semigroups/Action.lean`. -/
abbrev ShiftCat := ActionCategory Shift3 Regime3

#check (inferInstance : Category ShiftCat)

/-! ## `F : KCat ⥤ ShiftCat` — funtor "morfismo único", campo `map` por
tabela de casos explícita -/

/-- Tabela de casos explícita (9 casos, lida diretamente de `Shift3.apply`,
`Regime3.lean:52-59`): `shiftBetween x y` é o (único, por `shift3_free`)
escalar `m : Shift3` com `m • x = y`. Construção puramente por
`match`/tabela — nenhum uso de `Classical.choice`/`Nonempty.some` para
extrair este valor de uma instância `Nonempty`. -/
def shiftBetween : Regime3 → Regime3 → Shift3
  | .alpha, .alpha => .identity
  | .alpha, .beta => .forward
  | .alpha, .gamma => .forward2
  | .beta, .alpha => .forward2
  | .beta, .beta => .identity
  | .beta, .gamma => .forward
  | .gamma, .alpha => .forward
  | .gamma, .beta => .forward2
  | .gamma, .gamma => .identity

/-- `shiftBetween x y` de fato leva `x` a `y`: verificação pontual dos 9
casos por computação definicional (`Shift3.apply` reduz por `rfl` em cada
ramo, mesma técnica de `shift3_inv_mul_cancel`/`Kact_mul_smul` já usada em
`TOE-3a`/`TOE-3c`). -/
theorem shiftBetween_spec (x y : Regime3) : shiftBetween x y • x = y := by
  cases x <;> cases y <;> rfl

/-- Certificado de que o Hom-set alvo `Hom_Shift(p,q)` é não vazio, para
todo par de objetos de `ShiftCat` — metade do par
`Nonempty`+`Subsingleton` pedido pelo teste. Testemunho explícito via
`shiftBetween`/`shiftBetween_spec`, não uma alegação abstrata de
existência. -/
instance shiftCat_hom_nonempty (p q : ShiftCat) : Nonempty (p ⟶ q) :=
  ⟨⟨shiftBetween p.back q.back, shiftBetween_spec p.back q.back⟩⟩

/-- Certificado de que o Hom-set alvo `Hom_Shift(p,q)` tem no máximo um
elemento, para todo par de objetos de `ShiftCat` — a outra metade do par
`Nonempty`+`Subsingleton`. Decorre de `shift3_free` (a): dois escalares
que levam `p.back` ao mesmo `q.back` são iguais, logo os dois morfismos
(pares `⟨escalar, prova⟩`) são iguais por `Subtype.ext`. -/
instance shiftCat_hom_subsingleton (p q : ShiftCat) : Subsingleton (p ⟶ q) :=
  ⟨fun a b => Subtype.ext (shift3_free p.back a.val b.val (a.property.trans b.property.symm))⟩

/-- O funtor "morfismo único" `F : KCat ⥤ ShiftCat`: nos objetos, mantém o
`Regime3` subjacente (`p.back`); nos morfismos, ignora o rótulo `K` do
morfismo de entrada e devolve o único morfismo de `ShiftCat` entre os
objetos correspondentes, construído por `shiftBetween` (tabela explícita,
não `Classical.choice`). `map_id`/`map_comp` decorrem de
`Subsingleton.elim` sobre `shiftCat_hom_subsingleton`, já que o Hom-set
alvo tem no máximo um elemento — quaisquer dois morfismos de `ShiftCat`
com a mesma fonte/destino coincidem automaticamente. -/
def F : KCat ⥤ ShiftCat where
  obj p := show ShiftCat from p.back
  map {p q} _ := ⟨shiftBetween p.back q.back, shiftBetween_spec p.back q.back⟩
  map_id _ := Subsingleton.elim _ _
  map_comp _ _ := Subsingleton.elim _ _

/-- `F.map` colapsa `homIdentity` e `homK` (os dois morfismos distintos
`alpha ⟶ alpha` de `KCat`, `TOE-3c`) ao mesmo morfismo de `ShiftCat`: por
construção, `F.map` (via `shiftBetween`) só depende dos objetos
fonte/destino implícitos, não do rótulo `K` do morfismo explícito
recebido — como `homIdentity` e `homK` têm a mesma fonte e o mesmo
destino (`show KCat from Regime3.alpha` em ambos os casos), `F.map
homIdentity` e `F.map homK` são o mesmo termo, `rfl`. -/
theorem F_map_homIdentity_eq_F_map_homK : F.map homIdentity = F.map homK := rfl

/-- O teste central (parte 1): `F` não é `Faithful`. Prova: supondo
`Faithful F`, `Faithful.map_injective` aplicado a
`F_map_homIdentity_eq_F_map_homK` daria `homIdentity = homK`, contradizendo
`homIdentity_ne_homK` (`TOE-3c`, `MonoidKConstantActionDistinctEndomorphisms.lean:223-225`). -/
theorem F_not_faithful : ¬ Functor.Faithful F := by
  intro h
  exact homIdentity_ne_homK (h.map_injective F_map_homIdentity_eq_F_map_homK)

/-! ## Nenhum `G : ShiftCat ⥤ KCat` com `G.obj p = show KCat from p.back`
existe -/

/-- O testemunho de que `Shift3.forward` leva `beta` a `gamma` em
`ShiftCat`, portanto um morfismo `beta ⟶ gamma` em `ShiftCat` — direto da
tabela `Shift3.apply` (`Regime3.lean:54-56`, `.forward, .beta => .gamma`),
`rfl`. -/
def shiftHomBetaGamma :
    (show ShiftCat from Regime3.beta) ⟶ (show ShiftCat from Regime3.gamma) :=
  ⟨Shift3.forward, rfl⟩

/-- O teste central (parte 2): sob a hipótese explícita `hG` de que um
funtor `G : ShiftCat ⥤ KCat` mantém os objetos subjacentes (`G.obj p =
show KCat from p.back` para todo `p`), nenhum tal `G` existe. Prova:
`G.map shiftHomBetaGamma` seria um morfismo `G.obj (show ShiftCat from
beta) ⟶ G.obj (show ShiftCat from gamma)`; reescrevendo os dois extremos
via `hG`, isso daria um habitante de `(show KCat from beta) ⟶ (show KCat
from gamma)`, i.e. (por `hom_as_subtype`) um `m : K` com `m • beta =
gamma` — contradizendo `homK_beta_gamma_no_witness` (b). -/
theorem no_reverse_functor_with_fixed_objects
    (G : ShiftCat ⥤ KCat)
    (hG : ∀ p : ShiftCat, G.obj p = show KCat from p.back) : False := by
  set pβ : ShiftCat := show ShiftCat from Regime3.beta with hpβ
  set pγ : ShiftCat := show ShiftCat from Regime3.gamma with hpγ
  have hom_pβ_pγ : pβ ⟶ pγ := shiftHomBetaGamma
  have gmap : G.obj pβ ⟶ G.obj pγ := G.map hom_pβ_pγ
  rw [hG pβ, hG pγ] at gmap
  exact homK_beta_gamma_no_witness ⟨gmap.val, gmap.property⟩

/-- Registro (trivial) de que o teste falseável fechou: `F : KCat ⥤
ShiftCat` construído por tabela explícita (não `Classical.choice`) não é
`Faithful` (parte 1), e nenhum `G : ShiftCat ⥤ KCat` fixando os objetos
como `p.back` existe, via `Hom_K(beta,gamma) = ∅` (parte 2). -/
theorem toe_4_functor_not_faithful_no_reverse : True := trivial

#print axioms shift3_free
#print axioms homK_beta_gamma_no_witness
#print axioms homK_beta_gamma_isEmpty
#print axioms shiftBetween
#print axioms shiftBetween_spec
#print axioms shiftCat_hom_nonempty
#print axioms shiftCat_hom_subsingleton
#print axioms F
#print axioms F_map_homIdentity_eq_F_map_homK
#print axioms F_not_faithful
#print axioms shiftHomBetaGamma
#print axioms no_reverse_functor_with_fixed_objects
#print axioms toe_4_functor_not_faithful_no_reverse

end TamesisLab.TOE.KToShiftFunctorNotFaithfulNoReverse
