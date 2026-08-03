import TamesisLab.Foundations.FiniteStateAbstraction.Abstraction
import TamesisLab.Foundations.FiniteStateAbstraction.AbstractAnalysis
import TamesisLab.Foundations.FiniteStateAbstraction.Observation
import TamesisLab.Foundations.FiniteStateAbstraction.OrbitSeparation
import TamesisLab.Foundations.FiniteStateAbstraction.Counterexample

/-!
# FOUND-FINITE-STATE-ABSTRACTION-001 — agregador

A fronteira entre observar e refletir.

```text
Abstraction.lean       CertifiedFiniteAbstraction, iterate_commutes
AbstractAnalysis.lean  analyzeAbstractSystem, completeness abstrata
Observation.lean       soundness observacional
OrbitSeparation.lean   OrbitSeparating, reflexao condicionada
Counterexample.lean    BOOL_TO_UNIT
```

A cadeia completa:

```text
sistema concreto C
        ↓ abstract : C → A
sistema abstrato A
        ↓ CertifiedFiniteEncoding A n
Fin n
        ↓ analyzeEncodedSystem
CycleWitness abstrato
        ↓
recorrencia observacional no sistema concreto
        ↓ hipotese explicita de separacao da orbita
recorrencia concreta no sistema original
```

## As duas frases

```text
A analise abstrata sempre pode produzir um witness observacional.

Esse witness somente se torna uma repeticao concreta quando a
abstracao separa os estados relevantes da orbita.
```

## O que esta frente NÃO prova

Que uma abstração externa real esteja correta. Que semiconjugação
implique bissimulação. Que ciclos abstratos nunca sejam espúrios. Que
uma abstração muitos-para-um reflita igualdade.

`Counterexample.lean` prova formalmente que a última é **falsa**.

scientific_value: FORMAL_SEMANTIC_FOUNDATION
mathematical_novelty: NONE
algorithmic_novelty: NONE
-/
