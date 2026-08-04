import TamesisLab.Foundations.Invariants.Definitions

set_option autoImplicit false

/-!
# FOUND-INVARIANT-UNREACHABILITY-001 — instância, TEST_ONLY

Duas declarações `TEST_ONLY` que vivem na biblioteca porque o teste
`diag_unreachable` as consome. Segue o precedente de
`FiniteStateAbstraction/Counterexample.lean`, e está declarado em
`SPECIFICATION_DECISION.md` em vez de escondido na contagem.

O tipo concreto é `Int × Int`, **infinito nas duas coordenadas**. A
escolha é deliberada: se a instância fosse finita, alguém poderia ler a
ferramenta como dependente de finitude, e ela não é.
-/

namespace TamesisLab.Foundations.Invariants

/-- Passo diagonal sobre um tipo infinito: as duas coordenadas avançam
juntas. Não tem ponto fixo, não tem ciclo, e a órbita nunca se repete. -/
def diagStep (p : Int × Int) : Int × Int := (p.1 + 1, p.2 + 1)

/-- A diferença das coordenadas é invariante, porque o passo desloca as
duas igualmente. -/
theorem diagStep_invariant :
    Invariant (fun p : Int × Int => p.1 - p.2) diagStep := by
  intro p
  simp only [diagStep]
  omega

end TamesisLab.Foundations.Invariants
