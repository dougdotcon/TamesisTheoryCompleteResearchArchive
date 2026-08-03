import TamesisLab.Foundations.FiniteStateAbstraction.Abstraction

set_option autoImplicit false

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — a ponte executável

Uma linha de corpo. A ponte **abstrai o estado inicial** e delega à
análise já verificada.

```text
abstracao    C → A       possivelmente muitos-para-um
codificacao  A ≃ Fin n   exata, argumento SEPARADO
```

Manter as duas separadas é o que torna a fronteira observacional
visível: a perda de informação vive em `abstract`, e a codificação não
perde nada.

Nada é copiado da frente anterior — nem o detector, nem o adaptador de
runtime, nem a semântica de execução. Nenhum construtor de erro é criado
ou removido; nenhum certificado padrão existe.
-/

namespace TamesisLab.Foundations.FiniteStateAbstraction

open TamesisLab.Engineering.FiniteStateEncoding
open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection

variable {C A : Type*} {stepC : C → C} {stepA : A → A} {n : Nat}

/-- Analisa o **sistema abstrato**, partindo da observação de `start`.

O que se executa é `stepA`, sobre `A`, que possui codificação
certificada. `C` não tem codificação — e a frente inteira existe porque
ele pode nem ser finito. -/
def analyzeAbstractSystem (abstraction : CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C) :
    Except RuntimeCycleError CycleWitness :=
  analyzeEncodedSystem encoding stepA (abstraction.abstract start)

/-- **Completeness abstrata.**

A análise nunca falha, para qualquer entrada, sem pré-condição alguma do
consumidor e sem hipótese alguma sobre `C`.

O witness existe porque `A` é finito, por `CertifiedFiniteEncoding A n`.
A finitude que produz o certificado é a de `A`, **nunca** a de `C`.

Este teorema garante existência de witness **abstrato**. Ele não afirma
recorrência concreta — para isso é preciso
`analyzeAbstractSystem_reflected_sound` e sua hipótese explícita. -/
theorem analyzeAbstractSystem_complete
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C) :
    ∃ witness, analyzeAbstractSystem abstraction encoding start = .ok witness :=
  analyzeEncodedSystem_complete encoding stepA (abstraction.abstract start)

end TamesisLab.Foundations.FiniteStateAbstraction
