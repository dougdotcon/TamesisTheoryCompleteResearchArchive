import Mathlib.CategoryTheory.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms

/-!
# TOE-3D — `homK` não é isomorfismo em `ActionCategory K Regime3`

Item Wave-3 `TOE-3d` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-3c` (Wave-2,
`MonoidKConstantActionDistinctEndomorphisms.lean`), que construiu o
monoide de brinquedo `K = {identity, k}` (`k` idempotente, absorvente,
distinto de `identity`), a `MulAction K Regime3` com `Kact .k _ = .alpha`,
e os dois morfismos distintos `homIdentity`, `homK : alpha ⟶ alpha` em
`ActionCategory K Regime3`. Zero dependência de RH/NS.

## Teste falseável tentado (exatamente este, nada mais amplo)

Provar `¬ IsIso homK` em `ActionCategory K Regime3`, via case-split direto
sobre Hom-como-subtipo (rota direta apenas, conforme decidido na revisão
adversarial do plano de ataque da Onda 3, seção `TOE-3d`): para qualquer
candidato-inverso `g` com `g.val ∈ {identity, k}`, usar `comp_val` +
`k_idempotent` + `k_ne_identity` para mostrar que ambas as equações de
`IsIso.out` falham (`K.k` absorvente dos dois lados). A rota alternativa
via `stabilizerIsoEnd` foi explicitamente descartada no plano (aquele
lema carrega `set_option backward.isDefEq.respectTransparency.types
false in` na própria Mathlib, sinal de desdobramento definicional frágil)
e não é tentada aqui.

Citações verificadas por leitura direta do arquivo:
- `CategoryTheory/Iso.lean:238-240`: `class IsIso (f : X ⟶ Y) : Prop where
  out : ∃ inv : Y ⟶ X, f ≫ inv = 𝟙 X ∧ inv ≫ f = 𝟙 Y`.
- `CategoryTheory/Action.lean:121-123`: `ActionCategory.id_val`,
  `Subtype.val (𝟙 x) = 1`.
- `CategoryTheory/Action.lean:125-128`: `ActionCategory.comp_val`,
  `(f ≫ g).val = g.val * f.val` (ordem "invertida" ao nível de `.val`,
  compensada abaixo).
- `Kmul`, `k_idempotent`, `k_ne_identity`, `Kmul_identity_left`,
  `Kmul_identity_right`, `homK`, `homK_val` reaproveitados byte-a-byte de
  `MonoidKConstantActionDistinctEndomorphisms.lean` (`TOE-3c`), não
  redeclarados.

Como `Kmul .k _ = .k` (segundo braço, incondicional em relação ao segundo
argumento) e `Kmul x .k` reduz a `.k` para os dois valores possíveis de
`x` (`identity` via primeiro braço — `Kmul .identity a = a`, com
`a = .k` — e `k` via `k_idempotent`), `K.k` é absorvente dos dois lados:
para qualquer candidato-inverso `g`, tanto `g * K.k` quanto `K.k * g`
reduzem a `K.k ≠ K.identity = (𝟙 alpha).val`, então nenhuma das duas
equações de `IsIso.out` pode valer, independentemente de qual `g` é
escolhido.

## O que este arquivo NÃO estabelece

`K`/`Regime3` continuam sendo o modelo finito de brinquedo de `TOE-3c`,
sem significado físico. `¬ IsIso homK` é uma propriedade combinatória de
uma categoria de brinquedo com 3 objetos (o morfismo rotulado pelo
elemento absorvente `k` do monoide `K` não tem inverso categórico), não
uma alegação física de "irreversibilidade de interface" ou análogo. Não
recupera QM/GR/Yang–Mills nem termodinâmica
(`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não produz teorema de
impossibilidade físico nem previsão falseável, e não avança RH nem NS.
Não afirma novidade matemática: um elemento absorvente não-identidade de
um monoide finito nunca é invertível é fato padrão de teoria de monoides.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.HomKNotIsoActionCategoryK

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open CategoryTheory

/-- O teste central: `homK : alpha ⟶ alpha` em `ActionCategory K Regime3`
(definido em `MonoidKConstantActionDistinctEndomorphisms.lean`, reaproveitado
aqui, não redeclarado) não é isomorfismo.

Prova: supondo `IsIso homK`, `IsIso.out` (`CategoryTheory/Iso.lean:238-240`)
dá um candidato-inverso `inv : alpha ⟶ alpha` com `homK ≫ inv = 𝟙 alpha`
(`h1`) e `inv ≫ homK = 𝟙 alpha` (`h2`). Destrutura-se `inv` como o par
`⟨g, hg⟩` da caracterização `hom_as_subtype` (mesma técnica de acesso
direto ao rótulo `K` subjacente já usada para `homIdentity`/`homK` em
`TOE-3c`), deixando `g : K` livre para case-split. Aplicando `.val` a `h1`
e `h2` e reescrevendo com `ActionCategory.comp_val`/`ActionCategory.id_val`
(`Action.lean:121-128`), `h1` vira `Kmul g homK.val = K.identity` e `h2`
vira `Kmul homK.val g = K.identity`; substituindo `homK.val = K.k`
(`homK_val`, `TOE-3c`), restam `Kmul g K.k = K.identity` e
`Kmul K.k g = K.identity`. Case-split em `g` (`identity` ou `k`, os dois
únicos construtores de `K`): no caso `identity`, `Kmul_identity_left`/
`Kmul_identity_right` (`TOE-3c`) reduzem ambas as equações a
`K.k = K.identity`; no caso `k`, `k_idempotent` (`TOE-3c`) faz o mesmo.
Em ambos os casos, `k_ne_identity` (`TOE-3c`, `decide`) contradiz
`K.k = K.identity`, fechando por `False`. -/
theorem homK_not_isIso : ¬ IsIso homK := by
  intro hiso
  obtain ⟨inv, h1, h2⟩ := hiso.out
  obtain ⟨g, hg⟩ := inv
  have hval1 : Kmul g homK.val = K.identity := congrArg Subtype.val h1
  have hval2 : Kmul homK.val g = K.identity := congrArg Subtype.val h2
  rw [homK_val] at hval1 hval2
  cases g with
  | identity =>
      rw [Kmul_identity_left] at hval1
      rw [Kmul_identity_right] at hval2
      exact k_ne_identity hval1
  | k =>
      rw [k_idempotent] at hval1
      rw [k_idempotent] at hval2
      exact k_ne_identity hval1

/-- Registro (trivial) de que o teste falseável fechou: `homK` não é
isomorfismo em `ActionCategory K Regime3`, via case-split direto sobre
`Hom`-como-subtipo, sem recorrer a `stabilizerIsoEnd`. -/
theorem toe_3d_homK_not_isIso : True := trivial

#print axioms homK_not_isIso
#print axioms toe_3d_homK_not_isIso

end TamesisLab.TOE.HomKNotIsoActionCategoryK
