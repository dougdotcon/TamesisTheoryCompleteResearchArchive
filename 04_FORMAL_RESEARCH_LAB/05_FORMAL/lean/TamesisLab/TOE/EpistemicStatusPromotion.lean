import Mathlib.Data.Finset.Insert
import Mathlib.Data.Fintype.Defs

/-!
# TOE-4 — port do `EpistemicStatus`/`promotion_decision` do Transition Atlas

Item de síntese TOE (extensão do laboratório, não Clay), item Wave-1 `TOE-4`.
Bookkeeping sobre a própria governança do laboratório, não física.

## O que este arquivo testa

`01_TAMESIS_CORE/03_TRANSITION_ATLAS/reports/EPISTEMIC_STATUS_POLICY.md`
descreve em prosa uma política de promoção de `epistemic_status` para
`Transition`s. `src/transition_atlas/models.py:13-25` define o enum Python
`EpistemicStatus` com exatamente 12 casos; `src/transition_atlas/promotion.py`
define `promotion_decision(transition, target)`, que calcula uma lista
`reasons` e aprova a promoção sse `reasons == []`.

Este arquivo porta `EpistemicStatus` para um tipo indutivo Lean e porta
FIELMENTE (linha a linha) apenas o cálculo booleano de `approved` de
`promotion_decision` — ignorando deliberadamente, como o teste original
pede, a lista de strings `reasons` (texto livre, sem conteúdo formal) e
todos os campos de `Transition` que `promotion_decision` também ignora
(`source_regime`, `predictions`, `competing_explanations`, etc.).

## Desvio declarado em relação ao teste original, e por quê

O teste original pedia um predicado de DOIS argumentos
`mayPromote : EpistemicStatus → EpistemicStatus → Prop`. Ler
`promotion.py` linha a linha (verificado diretamente, não apenas assumido)
mostra que isso é impossível de portar fielmente sem argumentos extras:
`promotion_decision` decide `reasons` a partir de **dois campos de dados**
de `transition` — `critical_surface.get("status")` e
`bool(transition.falsification_conditions)` — não a partir de nenhuma
comparação entre o `epistemic_status` atual (`from`) e o `target`. Omitir
esses dois booleanos produziria um predicado que ou aprova tudo ou rejeita
tudo para os alvos com verificação de evidência, o que NÃO seria uma
representação fiel do código-fonte. Por isso `mayPromote` abaixo tem
assinatura `EpistemicStatus → EpistemicStatus → Bool → Bool → Prop`: os
dois primeiros argumentos são exatamente os do pedido original (`from`,
`target`); os dois booleanos extras são os dois únicos campos de dado que
`promotion_decision` de fato lê. Isto é documentado aqui, não é um
enfraquecimento silencioso.

## Achado (honesto, não afirmado como novidade matemática)

Portar a regra literalmente para Lean expôs uma não-monotonicidade real do
código Python, exatamente o tipo de achado que o teste original previa
como resultado válido caso a regra não componha um bom pré-ordem:

1. `promotion_decision` NUNCA lê `transition.epistemic_status` (o `from`)
   em nenhum dos seus `if`s — apenas o ecoa de volta no dicionário de
   saída sob a chave `"from"`. Logo a aprovação NÃO depende do estado
   atual: `metaphorical → falsified` é APROVADA incondicionalmente pelo
   código real (nenhum dos três `if`s de `promotion_decision` testa
   `target == falsified`), ao contrário do que a leitura em prosa de
   `EPISTEMIC_STATUS_POLICY.md` ("promoções não são automáticas")
   sugeriria. Isto é formalizado abaixo como `mayPromote_ignores_source`.
2. Para `target ∈ {transition_detected, independently_replicated}`,
   `promotion_decision` acrescenta razões de rejeição
   INCONDICIONALMENTE (não a partir de nenhum campo de `transition`) —
   ou seja, nenhuma instância de `Transition`, com quaisquer dados, pode
   jamais ser aprovada para esses dois alvos por esta função. Formalizado
   abaixo como `never_approvable_iff`.

Nenhum destes dois pontos é um bug óbvio dentro do escopo deste item —
apenas uma propriedade real, verificável, do código tal como está hoje,
registrada aqui como resultado decidível e não como alegação sobre a
intenção dos autores do Python.

## O que este arquivo NÃO estabelece

Não formaliza nenhuma condição de consistência de `TOE_CONVERGENCE_CRITERIA.md`
sobre regimes/interfaces/invariantes/obstruções físicas. É infraestrutura
sobre a infraestrutura do próprio laboratório (o registro de transições),
não uma afirmação matemática sobre RH/NS/física. Não avança nenhum
problema do Millennium. Não afirma novidade matemática.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
-/

namespace TamesisLab.TOE.EpistemicStatusPromotion

/-- Porta de `transition_atlas/models.py:13-25` (`class EpistemicStatus`),
com exatamente os 12 casos do enum Python, na mesma ordem. -/
inductive EpistemicStatus where
  | metaphorical
  | conjectured
  | mathematicallySpecified
  | computationallyReproduced
  | phenomenologicallyConstrained
  | preregisteredTest
  | observationalAnomaly
  | transitionDetected
  | independentlyReplicated
  | establishedRegimeBoundary
  | falsified
  | superseded
deriving DecidableEq, Repr

/-- Enumeração finita explícita dos 12 casos. Instância manual pela mesma
razão registrada em `Foundations/Semigroups/Regime3.lean`: o derive
handler de `Fintype` da revisão de Mathlib fixada falha sob imports
mínimos. -/
instance : Fintype EpistemicStatus where
  elems := { .metaphorical, .conjectured, .mathematicallySpecified,
    .computationallyReproduced, .phenomenologicallyConstrained,
    .preregisteredTest, .observationalAnomaly, .transitionDetected,
    .independentlyReplicated, .establishedRegimeBoundary, .falsified,
    .superseded }
  complete := fun x => by cases x <;> decide

/-- Porta fiel do cálculo booleano `approved := not reasons` de
`promotion_decision` (`promotion.py`), restrito aos dois campos de dado
que a função de fato lê:
* `criticalSurfaceDerived` ~ `transition.critical_surface.get("status")
  not in {"not_derived", "candidate_not_derived"}`
* `hasFalsificationConditions` ~ `bool(transition.falsification_conditions)`

Correspondência linha a linha com `promotion.py`:
* `target == mathematically_specified`: exige AMBOS os campos (o `if`
  aninhado da superfície crítica só dispara para este alvo, e o `if` da
  falsificação se aplica a ele também por estar no mesmo bloco externo).
* `target ∈ {computationally_reproduced, preregistered_test}`: exige
  apenas `hasFalsificationConditions` (o `if` da superfície crítica tem
  `and target == mathematically_specified`, não se aplica aqui).
* `target ∈ {transition_detected, independently_replicated}`: `reasons`
  recebe entradas INCONDICIONAIS nesses dois `if`s — sempre rejeitado.
* Qualquer outro alvo: nenhum `if` de `promotion_decision` dispara,
  `reasons == []`, sempre aprovado. -/
def approved (target : EpistemicStatus)
    (criticalSurfaceDerived hasFalsificationConditions : Bool) : Bool :=
  match target with
  | .mathematicallySpecified => criticalSurfaceDerived && hasFalsificationConditions
  | .computationallyReproduced => hasFalsificationConditions
  | .preregisteredTest => hasFalsificationConditions
  | .transitionDetected => false
  | .independentlyReplicated => false
  | .metaphorical | .conjectured | .phenomenologicallyConstrained
  | .observationalAnomaly | .establishedRegimeBoundary | .falsified
  | .superseded => true

/-- Relação decidível de 4 argumentos pedida pelo teste original (`from`,
`target`, mais os dois booleanos de evidência declarados acima como
necessários para fidelidade a `promotion.py`). O argumento `from_` está
presente na assinatura por corresponder ao pedido original e ao fato de
`promotion_decision` receber o `Transition` inteiro (que carrega
`epistemic_status`) — mas não é usado no corpo, exatamente porque
`promotion_decision` também não o usa. Ver `mayPromote_ignores_source`. -/
def mayPromote (_from_ target : EpistemicStatus)
    (criticalSurfaceDerived hasFalsificationConditions : Bool) : Prop :=
  approved target criticalSurfaceDerived hasFalsificationConditions = true

instance (from_ target : EpistemicStatus) (a b : Bool) :
    Decidable (mayPromote from_ target a b) := by
  unfold mayPromote; infer_instance

/-- Achado 1, formalizado: a aprovação nunca depende do estado atual
(`from_`). Prova por `rfl` porque `mayPromote`/`approved` literalmente não
mencionam `from_` — a igualdade vale por definição, o que é a própria
demonstração formal do achado (o código Python correspondente também
nunca lê `transition.epistemic_status` em `promotion_decision`). -/
theorem mayPromote_ignores_source
    (s₁ s₂ target : EpistemicStatus) (a b : Bool) :
    mayPromote s₁ target a b ↔ mayPromote s₂ target a b := Iff.rfl

/-- Caso de teste "escolhido a dedo" do teste original: `metaphorical →
falsified` seria esperado ser REJEITADO por pular evidência intermediária
exigida, segundo a leitura em prosa da política. O código real de
`promotion_decision` na verdade APROVA esta transição incondicionalmente
(nenhum de seus três `if`s testa `target == falsified`). Este `example`
reproduz literalmente o veredito real de `promotion_decision`, não o
veredito ingenuamente esperado pela prosa — é exatamente o achado 1
acima, em caso concreto. -/
example : mayPromote .metaphorical .falsified false false := by decide

/-- Achado 2, formalizado: os únicos dois alvos jamais aprováveis por
`promotion_decision`, para NENHUMA combinação de dados de evidência, são
exatamente `transitionDetected` e `independentlyReplicated`. Verificado
por `decide` sobre os 12 alvos × 4 combinações de booleanos (checagem
finita, mesmo idioma `Fintype`/`Decidable`/`decide` já usado no
laboratório, e.g. `Foundations/Semigroups/Regime3.lean`). -/
theorem never_approvable_iff (target : EpistemicStatus) :
    (∀ a b : Bool, approved target a b = false) ↔
      target = .transitionDetected ∨ target = .independentlyReplicated := by
  revert target; decide

-- Casos de teste adicionais, reproduzindo o veredito real de
-- `promotion_decision` linha a linha para cada ramo do `match` de
-- `approved` acima.
example : approved .mathematicallySpecified true true = true := by decide
example : approved .mathematicallySpecified false true = false := by decide
example : approved .mathematicallySpecified true false = false := by decide
example : approved .computationallyReproduced true false = false := by decide
example : approved .computationallyReproduced false true = true := by decide
example : approved .preregisteredTest true false = false := by decide
example : approved .preregisteredTest false true = true := by decide
example : approved .transitionDetected true true = false := by decide
example : approved .independentlyReplicated true true = false := by decide
example : approved .conjectured false false = true := by decide
example : approved .phenomenologicallyConstrained false false = true := by decide
example : approved .observationalAnomaly false false = true := by decide
example : approved .establishedRegimeBoundary false false = true := by decide
example : approved .superseded false false = true := by decide

#print axioms mayPromote_ignores_source
#print axioms never_approvable_iff

end TamesisLab.TOE.EpistemicStatusPromotion
