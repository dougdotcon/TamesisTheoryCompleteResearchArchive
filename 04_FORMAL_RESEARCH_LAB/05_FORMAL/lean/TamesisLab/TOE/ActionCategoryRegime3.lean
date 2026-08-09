import Mathlib.CategoryTheory.Action
import TamesisLab.Foundations.Semigroups.Action

/-!
# TOE-1 — `ActionCategory` instanciada sobre `Shift3 ↻ Regime3`

Item de síntese TOE (extensão do laboratório, não Clay), item Wave-1 TOE-1.
Zero dependência de RH/NS.

Verifica, como teste falseável único e estreito, que a construção genérica
`CategoryTheory.ActionCategory` da Mathlib (que transforma qualquer
`MulAction M X` em uma categoria, com objetos em bijeção com `X` e
morfismos `x ⟶ y` dados pelos escalares `m` com `m • x = y`) instancia
sem atrito sobre a ação `MulAction Shift3 Regime3` já construída e
VERIFICADA em `TamesisLab.Foundations.Semigroups.Action` como parte de
FOUND-SEMIGROUP-001.

`Regime3` é um tipo indutivo de 3 elementos sem significado físico
(`Foundations/Semigroups/Regime3.lean`); `Shift3` é o monoide cíclico de
3 transições agindo sobre ele. Este arquivo não afirma nenhuma leitura
física de "regime" ou "interface" — apenas testa a instanciação formal.

## O que este arquivo NÃO estabelece

Isto é uma categoria de brinquedo com 3 objetos e 3 morfismos, sem
conteúdo físico algum. Não distingue invariantes de monótonos, não dá
condições de consistência, não recupera QM/GR/YM/termodinâmica (ver
`THEORY_RECOVERY_MATRIX.md`, tudo ainda UNRESOLVED), não produz teoremas
de impossibilidade nem previsões falseáveis, e não avança RH nem NS.
Não desbloqueia o item TOE-INTERFACE-001 como escopado em
`RESEARCH_QUEUE.yaml` — no máximo um sub-item mais estreito.

Nota de fidelidade à Mathlib: o docstring de `ActionCategory` afirma
explicitamente que o tipo de objetos "não é igual a `X`, mas está em
bijeção com `X`" (`objEquiv : X ≃ ActionCategory M X`). Por isso as
afirmações abaixo sobre cardinalidade usam essa equivalência
(`Fintype.ofEquiv`) em vez de tentar reaproveitar a instância `Fintype
Regime3` diretamente sobre `ActionCategory Shift3 Regime3`, que não é
definicionalmente `Regime3`.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
-/

namespace TamesisLab.TOE

open TamesisLab.Foundations.Semigroups
open CategoryTheory

/-- A categoria de ação induzida por `Shift3 ↻ Regime3`: objetos em
bijeção com os três regimes, morfismos dados pelas transições que levam
um regime a outro. Construção inteiramente genérica da Mathlib
(`CategoryTheory.ActionCategory`), aplicada aqui à ação concreta já
verificada em FOUND-SEMIGROUP-001. -/
abbrev RegimeCat := ActionCategory Shift3 Regime3

-- `RegimeCat` de fato elabora como instância de `Category` (herdada via
-- `deriving Category` na definição de `ActionCategory`).
#check (inferInstance : Category RegimeCat)

/-- Os objetos de `RegimeCat` estão em bijeção com `Regime3`, portanto
têm cardinalidade 3. Não é a instância `Fintype Regime3` reaproveitada
por igualdade definicional (que não vale — ver nota acima), e sim
transportada explicitamente pela equivalência `objEquiv` que a própria
Mathlib fornece para essa finalidade. -/
noncomputable instance : Fintype RegimeCat :=
  Fintype.ofEquiv Regime3 (ActionCategory.objEquiv Shift3 Regime3)

theorem regimeCat_card : Fintype.card RegimeCat = 3 := by
  have h : Fintype.card RegimeCat = Fintype.card Regime3 :=
    Fintype.card_congr (ActionCategory.objEquiv Shift3 Regime3).symm
  rw [h]
  decide

-- Morfismo não identidade concreto: a transição `forward` vista como
-- morfismo `α ⟶ β` na categoria de ação, i.e. o testemunho de que
-- `Shift3.forward • Regime3.alpha = Regime3.beta`.
--
-- Nota técnica: a ascrição direta `(Regime3.alpha : RegimeCat)` foi tentada
-- primeiro e falha — o elaborador insere a coerção `CoeTC` e, ao fazer isso,
-- resolve o tipo até a estrutura `Sigma` crua por trás de `Functor.Elements`,
-- perdendo de vista a instância `Category`/`Quiver` registrada por
-- `deriving Category` para o nome `ActionCategory`. `show RegimeCat from _`
-- evita esse caminho de elaboração e funciona sem atrito; isolado e
-- confirmado em teste mínimo separado antes de aplicar aqui.
#check (⟨Shift3.forward, rfl⟩ :
  (show RegimeCat from Regime3.alpha) ⟶ (show RegimeCat from Regime3.beta))

-- O mesmo morfismo, exibido via a caracterização explícita
-- `hom_as_subtype` da Mathlib para deixar claro que é de fato um elemento
-- de `Shift3` sujeito à condição de ação, não um objeto opaco.
example :
    ((show RegimeCat from Regime3.alpha) ⟶ (show RegimeCat from Regime3.beta)) =
      { m : Shift3 // m • (show RegimeCat from Regime3.alpha).back =
        (show RegimeCat from Regime3.beta).back } :=
  ActionCategory.hom_as_subtype Shift3 Regime3 _ _

#print axioms regimeCat_card

end TamesisLab.TOE
