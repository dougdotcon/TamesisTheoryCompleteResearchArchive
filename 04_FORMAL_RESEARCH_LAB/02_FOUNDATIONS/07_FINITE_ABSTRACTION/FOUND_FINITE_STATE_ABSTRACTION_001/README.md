---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-README
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
previous_candidate_id: FOUND-FINITE-ABSTRACTION-001
status: READY
specification_status: READY_FOR_REVIEW
formalization_status: NOT_STARTED
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SEMANTIC_FOUNDATION
---

# FOUND-FINITE-STATE-ABSTRACTION-001

**Certified Finite-State Abstraction and Cycle-Reflection Boundaries**

## A cadeia

```text
sistema concreto C
        ↓ abstract : C → A
sistema abstrato A
        ↓ CertifiedFiniteEncoding A n
Fin n
        ↓ buildTransitionTable
ValidatedTransitionTable
        ↓ analyzeEncodedSystem
CycleWitness abstrato
        ↓
recorrência observacional no sistema concreto
        ↓ hipótese explícita de reflexão
recorrência concreta no sistema original
```

## As duas frases que a frente existe para deixar

```text
A análise abstrata sempre pode produzir um witness observacional.

Esse witness somente se torna uma repetição concreta quando a
abstração separa os estados relevantes da órbita.
```

## Identificador

O identificador canônico é `FOUND-FINITE-STATE-ABSTRACTION-001`. O nome
candidato anterior, `FOUND-FINITE-ABSTRACTION-001`, sobrevive apenas em
documentos históricos de portfólio e em artefatos imutáveis de gates já
encerrados. Ver [`IDENTIFIER_CANONICALIZATION_RECORD.md`](IDENTIFIER_CANONICALIZATION_RECORD.md).

## Documentos

```text
SPECIFICATION_DECISION.md          decisoes congeladas
DATA_MODEL.md                      CertifiedFiniteAbstraction
SEMICONJUGATION_ORIENTATION.md     orientacao auditada
ITERATION_CORRESPONDENCE.md        iterate_commutes
ABSTRACT_ANALYSIS_BRIDGE.md        analyzeAbstractSystem
OBSERVATIONAL_SOUNDNESS.md         resultado central
ORBIT_SEPARATION.md                OrbitSeparating
REFLECTED_SOUNDNESS.md             reflexao condicionada
ABSTRACT_COMPLETENESS.md           completeness
BOOL_TO_UNIT_COUNTEREXAMPLE.md     contraexemplo
PUBLIC_API_SPECIFICATION.md        API publica candidata
LEAN_API_AUDIT.md                  APIs reutilizadas
IMPORT_PLAN.md                     imports planejados
PROBE_RESULT.md                    evidencia do probe
TEST_PLAN.md                       testes planejados
THEOREM_MAP.md                     DAG dos teoremas
GAP_REGISTER.yaml                  vinte gaps
STOP_CONDITIONS.md                 dezoito stop conditions
CLAIM_BOUNDARY.md                  wording permitido e proibido
RESULT_BOUNDARY.md                 fronteira cientifica
STATUS.yaml                        estado da frente
```

## Escopo negativo

```text
bissimulacao        NAO
quocientes          NAO
concretizacao γ     NAO
sistemas nao deterministicos NAO
relacoes de transicao gerais NAO
extracao            NAO
CLI, parser, JSON, rede      NAO
integracao externa  NAO
```
