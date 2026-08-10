import Mathlib.CategoryTheory.Action
import TamesisLab.Foundations.Semigroups.Regime3

/-!
# TOE-3C — Monoide `K` de 2 elementos com ação constante testemunhando
`Hom(alpha,alpha)` com dois elementos distintos em `ActionCategory K Regime3`

Item Wave-2 `TOE-3c` (síntese TOE, extensão do laboratório, não Clay).
Terceiro sucessor direto de `TOE-1` (Wave-1, `ActionCategoryRegime3.lean`),
irmão de `TOE-3a` (Wave-2, `GroupShift3ActionGroupoid.lean`) e `TOE-3b`
(Wave-2, `Shift3PretransitiveActionCategoryConnected.lean`); os três
exploram consequências estruturais diferentes da mesma descoberta
registrada no diagnóstico de obsolescência do `TOE-3` original em
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_2_2026_08_09.md`: `Shift3` age livre e
simplesmente transitivamente sobre `Regime3` (um torsor de grupo cíclico
de ordem 3), logo por `hom_as_subtype` todo `Hom`-set de `ActionCategory
Shift3 Regime3` é um singleton — nenhum candidato a par de morfismos
distintos com mesma origem/destino existe *nessa* ação. `TOE-3a`/`TOE-3b`
promovem typeclasses sobre a ação já existente; `TOE-3c`, ao contrário,
precisa de uma ação **diferente** (não livre) para ter qualquer chance de
exibir dois morfismos distintos em um mesmo `Hom`-set — daí o monoide novo
`K`, não `Shift3`. Zero dependência de RH/NS.

## Teste falseável tentado (exatamente este, nada mais amplo)

Construir um monoide `K` de 2 elementos (`identity` e `k`, com `k`
idempotente e distinto de `identity`) e uma `MulAction K Regime3` em que
`k` colapsa todo `Regime3` em `Regime3.alpha` (a ação é "constante" no
sentido de que a única transição não-trivial de `K`, `k`, tem imagem
constante igual a `alpha`; `identity` continua agindo como a identidade,
como exige `one_smul`). Com essa ação em escopo, exibir diretamente os
dois elementos distintos de `Hom(alpha,alpha)` em `ActionCategory K
Regime3`: `⟨identity, rfl⟩` e `⟨k, rfl⟩`, e confirmar que diferem.
Desvio pontual do texto literal do item, registrado e justificado
abaixo: a confirmação de distinção não é `decide` aplicado diretamente
ao tipo `Hom(alpha,alpha)` (que falha por instância — ver a nota técnica
junto a `homIdentity_ne_homK` mais abaixo no arquivo), e sim `decide`
aplicado a `K.k ≠ K.identity`, cuja conclusão é então levantada ao nível
de `Hom` por reescrita (`rw`) usando os fatos `rfl` `homIdentity.val =
K.identity` / `homK.val = K.k`.

Nota de escopo (registrada no plano de ataque, seção 7, item `TOE-3c`):
a versão mínima do teste — construir `K` e a instância `MulAction`, e
exibir os dois elementos distintos de `Hom(alpha,alpha)` — é suficiente
para o falseável; o passo adicional de colapso-por-functor
(`ActionCategory K Regime3 ⥤` alguma categoria-de-grafo) fica como
follow-on opcional não tentado aqui, pois apenas re-demonstraria a
não-injetividade já visível diretamente no `Hom`-set de dois elementos.

## Por que a ação "constante" precisa ser definida como está

Uma ação genuinamente constante em `todos` os elementos de `K` (isto é,
`m • r = alpha` para todo `m : K`, incluindo `identity`) viola o axioma
`one_smul` de `MulAction` sempre que `Regime3` tem um elemento diferente
de `alpha` (`beta`, `gamma`): exigiria `alpha = r` para todo `r`, falso.
A construção abaixo evita isso definindo `identity` como identidade
genuína (`Kact .identity r = r`) e apenas `k` como o colapso constante
(`Kact .k _ = .alpha`) — a única forma de ter uma "ação com um elemento
não-identidade constante" que ainda satisfaz os axiomas de `MulAction`.
Verificado por análise finita exaustiva (`decide`) abaixo, não apenas
alegado.

## O que este arquivo NÃO estabelece

`K`/`Regime3` são um modelo finito de brinquedo sem significado físico
algum — `K` é definido aqui pela primeira vez, especificamente para este
item, e não reaproveita `Shift3` (que é livre e não serviria ao teste,
como diagnosticado acima). `Hom(alpha,alpha)` ter dois elementos é uma
propriedade combinatória de uma categoria de brinquedo com 3 objetos, não
uma alegação física de "múltiplas transições de interface" ou análogo.
Não recupera QM/GR/Yang–Mills nem termodinâmica
(`THEORY_RECOVERY_MATRIX.md`, tudo `UNRESOLVED`), não produz teorema de
impossibilidade nem previsão falseável, e não avança RH nem NS. Não
afirma novidade matemática: monoide de 2 elementos com ação colapsante é
construção padrão.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
-/

namespace TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms

open TamesisLab.Foundations.Semigroups
open CategoryTheory

/-- O monoide `K` de dois elementos: `identity` (elemento neutro) e `k`
(o único elemento não-identidade, que será construído como idempotente).
Novo tipo indutivo definido apenas para este item — não reaproveita
`Shift3`, que é livre e não serve ao teste (ver nota no cabeçalho). -/
inductive K where
  | identity
  | k
deriving DecidableEq, Repr

/-- Enumeração finita explícita dos dois elementos de `K`, mesmo idioma
manual já usado em `Regime3`/`Shift3` (`Regime3.lean:31-49`). -/
instance : Fintype K where
  elems := {.identity, .k}
  complete := fun x => by cases x <;> decide

/-- Multiplicação de `K`: `identity` é neutro de ambos os lados; `k`
absorve tudo (`k * x = k` para qualquer `x`, incluindo `x = k`, o que
torna `k` idempotente). -/
def Kmul : K → K → K
  | .identity, x => x
  | .k, _ => .k

/-- FOUND-K-001 (local a este item) — associatividade de `Kmul`, análise
finita exaustiva (4 casos), mesmo idioma `revert`/`decide` já usado em
`Theorems.lean:20-22` (FOUND-SG-002) e `GroupShift3ActionGroupoid.lean:79`
(TOE-3a). -/
theorem Kmul_assoc (a b c : K) : Kmul (Kmul a b) c = Kmul a (Kmul b c) := by
  revert a b c; decide

/-- Identidade à esquerda: definicional, direto do primeiro `match arm`
de `Kmul`. -/
theorem Kmul_identity_left (a : K) : Kmul .identity a = a := rfl

/-- Identidade à direita: `k * identity = k` pelo segundo `match arm` de
`Kmul` (`.k, _ => .k`); `identity * identity = identity` pelo primeiro.
Análise por casos, não `decide` puro, para paralelismo com
`comp_identity` (`Theorems.lean:28-29`). -/
theorem Kmul_identity_right (a : K) : Kmul a .identity = a := by
  cases a <;> rfl

/-- `Monoid K`: `*` é `Kmul`, `1` é `identity`. Leis: `Kmul_assoc`,
`Kmul_identity_left`, `Kmul_identity_right` acima. -/
instance : Monoid K where
  mul := Kmul
  mul_assoc := Kmul_assoc
  one := .identity
  one_mul := Kmul_identity_left
  mul_one := Kmul_identity_right

/-- `k` é idempotente: `k * k = k`, direto do segundo `match arm` de
`Kmul`. Esta é exatamente a propriedade pedida pelo item ("k idempotente
não-identidade"). -/
theorem k_idempotent : Kmul .k .k = .k := rfl

/-- `k ≠ identity`: os dois elementos de `K` são de fato distintos
(`DecidableEq` derivado, análise finita). -/
theorem k_ne_identity : (K.k) ≠ K.identity := by decide

/-- A ação de `K` sobre `Regime3`: `identity` age como a identidade
genuína (necessário para `one_smul`); `k` colapsa qualquer regime em
`alpha` — a única forma de "ação constante" compatível com os axiomas de
`MulAction` (ver nota no cabeçalho). -/
def Kact : K → Regime3 → Regime3
  | .identity, r => r
  | .k, _ => .alpha

/-- FOUND-K-002 (local a este item) — compatibilidade de `Kact` com
`Kmul`: `(a * b) • r = a • (b • r)`, análise finita exaustiva (2×2×3 = 12
casos), mesmo idioma de `apply_comp` (`Theorems.lean:33-35`,
FOUND-SG-005). -/
theorem Kact_mul_smul (a b : K) (r : Regime3) :
    Kact (Kmul a b) r = Kact a (Kact b r) := by
  revert a b r; decide

/-- `MulAction K Regime3`: `•` é `Kact`. `one_smul` é definicional
(`Kact .identity r = r`, primeiro `match arm`); `mul_smul` é
`Kact_mul_smul` acima. -/
instance : MulAction K Regime3 where
  smul := Kact
  mul_smul := Kact_mul_smul
  one_smul := fun _ => rfl

/-- A categoria de ação induzida por `K ↻ Regime3`. Construção
inteiramente genérica da Mathlib (`CategoryTheory.ActionCategory`),
mesmo padrão de `RegimeCat` em `ActionCategoryRegime3.lean:54`, aplicada
aqui à nova ação `K ↻ Regime3` verificada acima. -/
abbrev KCat := ActionCategory K Regime3

-- `KCat` de fato elabora como instância de `Category`, mesma verificação
-- de `ActionCategoryRegime3.lean:58`.
#check (inferInstance : Category KCat)

/-- O primeiro morfismo `alpha ⟶ alpha`: o testemunho de que
`K.identity • Regime3.alpha = Regime3.alpha` (trivial, `identity` age
como identidade). Mesma técnica de ascrição `show KCat from _` já
confirmada necessária em `ActionCategoryRegime3.lean:78-86` (a ascrição
direta falha por perder de vista a instância `Category`/`Quiver`
registrada via `deriving Category`). -/
def homIdentity :
    (show KCat from Regime3.alpha) ⟶ (show KCat from Regime3.alpha) :=
  ⟨K.identity, rfl⟩

/-- O segundo morfismo `alpha ⟶ alpha`: o testemunho de que
`K.k • Regime3.alpha = Regime3.alpha`, que vale porque `Kact .k _ =
.alpha` para qualquer regime, em particular para `alpha`. -/
def homK :
    (show KCat from Regime3.alpha) ⟶ (show KCat from Regime3.alpha) :=
  ⟨K.k, rfl⟩

/-- O teste central do item: `homIdentity` e `homK` são morfismos
distintos em `Hom(alpha,alpha)`. Comparados via `.val` (o rótulo `K`
subjacente a cada morfismo, campo exposto pela caracterização explícita
`hom_as_subtype`/`id_val`/`comp_val` de `CategoryTheory/Action.lean:92,
121-128`, já usadas dessa forma nos morfismos de `ActionCategory` na
própria Mathlib), que reduz por `rfl` a `K.identity` e `K.k`
respectivamente — a distinção decorre então de `k_ne_identity` acima,
verificada por análise finita exaustiva (`decide`) sobre `DecidableEq
K`. -/
theorem homIdentity_val : homIdentity.val = K.identity := rfl

theorem homK_val : homK.val = K.k := rfl

-- Nota técnica: `homIdentity ≠ homK` (ou `homIdentity.val ≠ homK.val`)
-- diretamente `via decide` falha — `decide` não consegue sintetizar
-- `Decidable (↑homIdentity ≠ ↑homK)`, porque a busca de instância não
-- desdobra a torre `Quiver.Hom`/`CategoryOfElements`/`Functor.Elements`
-- por trás de `⟶` até enxergar o `Subtype K _` subjacente (a igualdade
-- `hom_as_subtype`, `CategoryTheory/Action.lean:92`, é `rfl` mas
-- opaca o bastante para a busca de instância de `Decidable`, mesmo
-- `.val` sendo acessível por notação de projeção). Confirmado por
-- tentativa direta (log de erro isolado antes de aplicar a correção
-- abaixo). A distinção é então estabelecida comparando os rótulos `K`
-- subjacentes via `.val` (`homIdentity_val`/`homK_val` acima, ambos
-- `rfl`), reduzindo ao fato `K.k ≠ K.identity` que É decidido `via
-- decide` (`k_ne_identity` acima) — exatamente o "via decide"
-- especificado no teste, aplicado no nível de `K` em vez de no nível do
-- tipo `Hom` opaco.
theorem homIdentity_ne_homK : homIdentity ≠ homK := by
  intro h
  exact k_ne_identity (by rw [← homIdentity_val, ← homK_val, h])

/-- Registro (trivial) de que o teste falseável fechou: `K` de 2
elementos com `k` idempotente não-identidade, ação constante-em-`k`, e
`Hom(alpha,alpha)` em `ActionCategory K Regime3` com (pelo menos) dois
elementos distintos, `⟨identity, rfl⟩` e `⟨k, rfl⟩`. -/
theorem toe_3c_two_distinct_endomorphisms : True := trivial

#print axioms Kmul_assoc
#print axioms Kmul_identity_left
#print axioms Kmul_identity_right
#print axioms k_idempotent
#print axioms k_ne_identity
#print axioms Kact_mul_smul
#print axioms homIdentity_val
#print axioms homK_val
#print axioms homIdentity_ne_homK
#print axioms toe_3c_two_distinct_endomorphisms

end TamesisLab.TOE.MonoidKConstantActionDistinctEndomorphisms
