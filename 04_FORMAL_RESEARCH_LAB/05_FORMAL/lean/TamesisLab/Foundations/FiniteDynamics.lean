import TamesisLab.Foundations.FiniteDynamics.Reachability
import TamesisLab.Foundations.FiniteDynamics.Invariants
import TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity
import TamesisLab.Foundations.FiniteDynamics.MonoidIteration
import TamesisLab.Foundations.FiniteDynamics.Counterexamples
import TamesisLab.Foundations.FiniteDynamics.Audit

/-!
# FOUND-SEMIGROUP-002 — agregador

Dinâmica discreta de ações finitas de monoides, em três camadas separadas:

```text
CAMADA A   Reachability.lean, Invariants.lean
           acao COMPLETA do monoide

CAMADA B   MonoidIteration.lean
           um gerador fixo; corolario DERIVADO

CAMADA C   EventualPeriodicity.lean
           funcao sobre tipo finito; SEM monoide
```

mais `Counterexamples.lean`, que impede a promoção de propriedades do
modelo `C3` a leis gerais.

Resultados **padrão** de dinâmica finita e do princípio da casa dos pombos.
Nenhuma novidade matemática. Nenhuma alegação física, TRI, TDTR ou
universal.

scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
mathematical_novelty: NONE
-/
