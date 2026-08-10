import Mathlib.CategoryTheory.Action
import TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms

/-!
# TOE-3E — `¬ IsPretransitive K Regime3`, e ainda assim
`IsConnected (ActionCategory K Regime3)` via zigzag construído à mão

Item Wave-3 `TOE-3e` (síntese TOE, extensão do laboratório, não Clay).
Continuação direta de `TOE-3c` (Wave-2, `MonoidKConstantActionDistinctEndomorphisms.lean`)
e irmão de `TOE-3d` (Wave-3, `HomKNotIsoActionCategoryK.lean`); ambos exploram
consequências estruturais diferentes do monoide de brinquedo `K = {identity, k}`
(`k` idempotente, absorvente, distinto de `identity`) agindo sobre `Regime3` via
`Kact .identity r = r`, `Kact .k _ = .alpha`. Zero dependência de RH/NS.

`TOE-3b` (Wave-2, `Shift3PretransitiveActionCategoryConnected.lean`) obteve
`IsConnected (ActionCategory Shift3 Regime3)` de graça, via a instância genérica
da Mathlib `[IsPretransitive M X] [Nonempty X] → IsConnected (ActionCategory M X)`
(`CategoryTheory/Action.lean:130-133`), porque `Shift3` é pretransitivo. A ação de
`K`, ao contrário, **não** é pretransitiva (`Kact` nunca leva `alpha` a `beta`,
pois `identity` fixa `alpha` e `k` colapsa tudo em `alpha`) — logo essa instância
genérica não dispara e não pode ser usada aqui. Este item testa se
`IsConnected (ActionCategory K Regime3)` ainda assim vale, por uma via
estruturalmente diferente: construir o zigzag manualmente e invocar
`zigzag_isConnected` diretamente, em vez de depender de pretransitividade.

## Teste falseável tentado (exatamente este, nada mais amplo)

Primeiro, como resultado autônomo: provar `¬ MulAction.IsPretransitive K Regime3`
(`Kact .identity alpha = alpha` e `Kact .k _ = .alpha`, logo nenhum `m : K` leva
`alpha` a `beta`).

Depois: provar `IsConnected (ActionCategory K Regime3)` via `zigzag_isConnected`
(`CategoryTheory/IsConnected.lean:436-437`), construindo `Zigzag` para os pares de
`Regime3` usando `Kact k beta = alpha`, `Kact k gamma = alpha` (`Zag.of_hom`/
`Zag.of_inv`/`Zigzag.trans`, `CategoryTheory/IsConnected.lean:307-345`): de
qualquer regime `r` até `alpha` há um morfismo direto rotulado `k` (pois
`Kact .k r = alpha` para todo `r`, `MonoidKConstantActionDistinctEndomorphisms.lean:148-150`),
e de `alpha` até qualquer regime `r` há o zigue-zague reverso do mesmo morfismo
(`Zag.of_inv`). Compondo os dois trechos (`Zigzag.trans`) liga qualquer par
ordenado de `Regime3` — em particular os 9 pares ordenados de `alpha, beta,
gamma` consigo mesmos e entre si, exibidos abaixo como verificação pontual.

Citações verificadas por leitura direta do arquivo:
- `Algebra/Group/Action/Pretransitive.lean`: `class MulAction.IsPretransitive
  (M α) [SMul M α] : Prop where exists_smul_eq : ∀ x y : α, ∃ m : M, m • x = y`.
- `CategoryTheory/IsConnected.lean:307-309`: `Zag.of_hom`/`Zag.of_inv`.
- `CategoryTheory/IsConnected.lean:331-345`: `Zigzag.trans`, `Zigzag.of_hom`,
  `Zigzag.of_inv`.
- `CategoryTheory/IsConnected.lean:436-437`: `zigzag_isConnected [Nonempty J]
  (h : ∀ j₁ j₂ : J, Zigzag j₁ j₂) : IsConnected J`.
- `CategoryTheory/Action.lean:94-98` (`ActionCategory.back_coe`, `@[simp]`):
  `↑x.back = x`, usada para transportar o zigzag construído sobre `Regime3` de
  volta para os objetos genéricos de `ActionCategory K Regime3`.
- `K`, `KCat`, a instância `MulAction K Regime3` reaproveitados byte-a-byte de
  `MonoidKConstantActionDistinctEndomorphisms.lean` (`TOE-3c`), não
  redeclarados.

## O que este arquivo NÃO estabelece

`K`/`Regime3` continuam sendo o modelo finito de brinquedo de `TOE-3c`, sem
significado físico. `¬ IsPretransitive K Regime3` e `IsConnected (ActionCategory
K Regime3)` são propriedades combinatórias de uma categoria de brinquedo com 3
objetos, não alegações físicas sobre "conectividade de interface" ou "acesso
completo entre regimes" apesar da sobreposição de vocabulário — nenhuma leitura
física é afirmada. `IsConnected` aqui é a noção categórica de alcançabilidade
por zigue-zague de morfismos/inversos formais (`CategoryTheory.IsConnected`),
não uma noção de conectividade topológica ou física. Este item ilustra que
`IsConnected` é estritamente mais fraco que `IsPretransitive + Nonempty`
(implicação que não reverte) — fato de teoria de categorias padrão, não
descoberta nova. Não recupera QM/GR/Yang–Mills nem termodinâmica
(`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não produz teorema de
impossibilidade físico nem previsão falseável, e não avança RH nem NS.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.MonoidKNonPretransitiveZigzagConnected

open TamesisLab.Foundations.Semigroups
open TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
open CategoryTheory

/-! ## Parte 1 — `¬ MulAction.IsPretransitive K Regime3` -/

/-- `K` não age pretransitivamente sobre `Regime3`: nenhum `m : K` leva `alpha`
a `beta`. Prova: supondo `IsPretransitive`, `exists_smul_eq alpha beta` dá um
`m : K` com `m • alpha = beta`. Case-split nos dois construtores de `K`
(`identity`, `k`) — em ambos os casos `m • alpha` reduz definicionalmente a
`alpha` (`identity` age como identidade; `k` colapsa tudo, em particular
`alpha`, em `alpha`), então a hipótese vira `alpha = beta`, refutada por
`decide` (`DecidableEq Regime3` derivado em `Regime3.lean:29`). -/
theorem k_not_isPretransitive : ¬ MulAction.IsPretransitive K Regime3 := by
  intro h
  obtain ⟨m, hm⟩ := h.exists_smul_eq Regime3.alpha Regime3.beta
  revert hm
  cases m <;> decide

/-! ## Parte 2 — `IsConnected (ActionCategory K Regime3)` via zigzag manual -/

/-- Todo regime tem um morfismo direto até `alpha` em `ActionCategory K
Regime3`, rotulado por `k`: testemunho de `K.k • r = Regime3.alpha`, que vale
por `rfl` para qualquer `r` porque o segundo braço de `Kact`
(`MonoidKConstantActionDistinctEndomorphisms.lean:148-150`) é `.k, _ => .alpha`,
incondicional em relação ao regime de entrada — cobre em particular `Kact k
beta = alpha` e `Kact k gamma = alpha`, citados no teste. -/
def homToAlpha (r : Regime3) :
    (show KCat from r) ⟶ (show KCat from Regime3.alpha) :=
  ⟨K.k, rfl⟩

/-- Quaisquer dois regimes `x`, `y` (vistos como objetos de `ActionCategory K
Regime3`) estão ligados por um `Zigzag`: percorre-se o morfismo direto `x ⟶
alpha` (`Zag.of_hom`) e depois o morfismo `y ⟶ alpha` em sentido inverso
(`Zag.of_inv`), compondo via `Zigzag.trans`. Isto cobre, em particular, os 9
pares ordenados de `Regime3.alpha`/`Regime3.beta`/`Regime3.gamma` consigo
mesmos e entre si, verificados pontualmente logo abaixo. -/
theorem k_zigzag (x y : Regime3) :
    Zigzag (show KCat from x) (show KCat from y) :=
  (Zigzag.of_hom (homToAlpha x)).trans (Zigzag.of_inv (homToAlpha y))

-- Verificação pontual dos 9 pares ordenados de `Regime3`, instância direta de
-- `k_zigzag` para cada combinação, exatamente como pedido pelo teste.
example : Zigzag (show KCat from Regime3.alpha) (show KCat from Regime3.alpha) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.alpha) (show KCat from Regime3.beta) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.alpha) (show KCat from Regime3.gamma) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.beta) (show KCat from Regime3.alpha) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.beta) (show KCat from Regime3.beta) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.beta) (show KCat from Regime3.gamma) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.gamma) (show KCat from Regime3.alpha) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.gamma) (show KCat from Regime3.beta) := k_zigzag _ _
example : Zigzag (show KCat from Regime3.gamma) (show KCat from Regime3.gamma) := k_zigzag _ _

/-- O teste central: `IsConnected (ActionCategory K Regime3)`, via
`zigzag_isConnected` (`CategoryTheory/IsConnected.lean:436-437`) aplicado a
`k_zigzag` acima, transportado dos objetos-`Regime3` (`x`, `y`) para os
objetos genéricos `p q : KCat` via `p = ↑p.back`/`q = ↑q.back`
(`ActionCategory.back_coe`, `@[simp]`, `Action.lean:94-98`), fechado por
`simpa`. A não-vacuidade exigida por `zigzag_isConnected` é fornecida por
`show KCat from Regime3.alpha`. Diferente de `TOE-3b`
(`Shift3PretransitiveActionCategoryConnected.lean`), a instância genérica
`[IsPretransitive M X] [Nonempty X] → IsConnected (ActionCategory M X)`
(`Action.lean:130-133`) não dispara aqui — `k_not_isPretransitive` (Parte 1)
mostra exatamente que sua hipótese falha para `K` — então o zigzag precisa
ser construído à mão, como feito acima. -/
theorem k_isConnected : IsConnected KCat :=
  haveI : Nonempty KCat := ⟨show KCat from Regime3.alpha⟩
  zigzag_isConnected fun p q => by
    have h := k_zigzag p.back q.back
    simpa using h

/-- Registro (trivial) de que o teste falseável fechou: `K` não age
pretransitivamente sobre `Regime3` (Parte 1), e ainda assim `ActionCategory K
Regime3` é conexa via um zigzag construído à mão em vez da instância genérica
de pretransitividade (Parte 2). -/
theorem toe_3e_nonpretransitive_still_connected_via_zigzag : True := trivial

#print axioms k_not_isPretransitive
#print axioms homToAlpha
#print axioms k_zigzag
#print axioms k_isConnected
#print axioms toe_3e_nonpretransitive_still_connected_via_zigzag

end TamesisLab.TOE.MonoidKNonPretransitiveZigzagConnected
