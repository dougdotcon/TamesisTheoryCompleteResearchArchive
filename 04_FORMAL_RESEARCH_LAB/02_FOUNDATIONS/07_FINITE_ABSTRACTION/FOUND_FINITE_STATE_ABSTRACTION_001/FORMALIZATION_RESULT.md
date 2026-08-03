---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FORMALIZATION-RESULT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
formalization_status: VERIFIED
lake_build_exit: 0
lake_build_jobs: 8767
---

# Resultado da formalização

## Build

```text
lake build            REAL_BUILD_EXIT=0
jobs                  8767
linhas "error:" reais 0
```

O código de saída foi capturado por script em arquivo — ver
[`VERIFICATION_METHOD_CORRECTION.md`](VERIFICATION_METHOD_CORRECTION.md).

## Módulos permanentes criados

```text
TamesisLab/Foundations/FiniteStateAbstraction/Abstraction.lean
TamesisLab/Foundations/FiniteStateAbstraction/AbstractAnalysis.lean
TamesisLab/Foundations/FiniteStateAbstraction/Observation.lean
TamesisLab/Foundations/FiniteStateAbstraction/OrbitSeparation.lean
TamesisLab/Foundations/FiniteStateAbstraction/Counterexample.lean
TamesisLab/Foundations/FiniteStateAbstraction/Audit.lean
TamesisLab/Foundations/FiniteStateAbstraction.lean
```

Testes:

```text
TamesisLab/Tests/FoundFiniteStateAbstraction001.lean
TamesisLab/Tests/FoundFiniteStateAbstraction001Execution.lean
TamesisLab/Tests/FoundFiniteStateAbstraction001Axioms.lean
TamesisLab/Tests/FoundFiniteStateAbstraction001UmbrellaAudit.lean
```

```text
arquivos Lean novos    11
arquivos preexistentes modificados   2 (apenas linhas de import)
```

## Elaboração isolada, módulo a módulo

Todos com `exit=0` e `errors=0`:

```text
Abstraction.lean                              exit=0 errors=0
AbstractAnalysis.lean                         exit=0 errors=0
Observation.lean                              exit=0 errors=0
OrbitSeparation.lean                          exit=0 errors=0
Counterexample.lean                           exit=0 errors=0
Audit.lean                                    exit=0 errors=0
FiniteStateAbstraction.lean                   exit=0 errors=0
FoundFiniteStateAbstraction001.lean           exit=0 errors=0
FoundFiniteStateAbstraction001Execution.lean  exit=0 errors=0
FoundFiniteStateAbstraction001Axioms.lean     exit=0 errors=0
FoundFiniteStateAbstraction001UmbrellaAudit.lean exit=0 errors=0
```

## Contagem derivada por script

Varredura dos quatro módulos do núcleo:

```text
structures   1
defs         2
theorems     4
instances    0
private      0
-------------
total        7
```

Nomes extraídos automaticamente:

```text
structure CertifiedFiniteAbstraction
theorem   CertifiedFiniteAbstraction.iterate_commutes
def       analyzeAbstractSystem
theorem   analyzeAbstractSystem_complete
theorem   analyzeAbstractSystem_observational_sound
def       OrbitSeparating
theorem   analyzeAbstractSystem_reflected_sound
```

A contagem derivada **coincide** com `PUBLIC_TOTAL = 7` congelado em
`FINAL_PUBLIC_API.md`. Nenhuma correção de contagem foi necessária.

O módulo do contraexemplo contém `10` declarações, todas `TEST_ONLY`,
fora da contagem pública.

## Tokens proibidos

```text
sorry            0
admit            0
unsafe           0
axioma local     0
noncomputable    0
Classical.choose 0
Classical.decEq  0
avaliacao nativa 0
FORBIDDEN_TOKENS 0
```

## Typeclasses no núcleo

```text
NO_TYPECLASS_BRACKETS_IN_CORE
```

Varredura por `[Fintype|Finite|DecidableEq|Nonempty|Inhabited` nos
quatro módulos centrais: nenhuma ocorrência.

## Desvios da especificação

```text
nenhum
```

As sete assinaturas foram implementadas como congeladas.

## Correção durante o gate

`FoundFiniteStateAbstraction001UmbrellaAudit.lean` falhou na primeira
elaboração:

```text
error: failed to synthesize
  Decidable (Function.Semiconj parity rotate4 rotate2)
```

Causa: `Function.Semiconj` é um `def`, e a resolução de instâncias não
o desdobra — a mesma armadilha já registrada para `CycleWitness.Valid`
em `FOUND-CYCLE-DETECTION-001`. Corrigido com
`intro i; revert i; decide`, que apresenta ao `decide` um objetivo
quantificado sobre `Fin 4`, este sim decidível.

A falha foi registrada, não mascarada.
