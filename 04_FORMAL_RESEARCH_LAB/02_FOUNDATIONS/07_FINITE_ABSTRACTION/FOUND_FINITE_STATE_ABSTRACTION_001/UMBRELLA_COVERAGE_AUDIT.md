---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-UMBRELLA-COVERAGE-AUDIT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
umbrella_exit: 0
registered_in_root: false
---

# Auditoria de cobertura pelo agregador raiz

## O arquivo

```text
TamesisLab/Tests/FoundFiniteStateAbstraction001UmbrellaAudit.lean
```

Importa **apenas** `TamesisLab` e alcança tudo por nome totalmente
qualificado.

## Por que ele NÃO está em `TamesisLab.lean`

```text
"Nao registrar testes que importam TamesisLab dentro de
 TamesisLab.lean — import circular"
```

Regra já registrada no laboratório. Consequência operacional: `lake
build` **não** o alcança, e por isso ele é executado explicitamente.
Declarar `lake build: PASS` não seria evidência sobre este arquivo.

```text
lake env lean …UmbrellaAudit.lean
  error_lines      0
  REAL_EXIT_CODE   0
```

## Cobertura verificada

```text
CertifiedFiniteAbstraction                      alcancada
analyzeAbstractSystem                           alcancada
CertifiedFiniteAbstraction.iterate_commutes     alcancada
analyzeAbstractSystem_observational_sound       alcancada
OrbitSeparating                                 alcancada
analyzeAbstractSystem_reflected_sound           alcancada
analyzeAbstractSystem_complete                  alcancada
```

Contraexemplo:

```text
Counterexample.boolToUnit_semiconj              alcancada
Counterexample.boolToUnit_not_orbitSeparating   alcancada
Counterexample.naive_cycle_reflection_is_false  alcancada
```

Frentes anteriores, ainda alcançadas pela mesma raiz:

```text
Engineering.FiniteStateEncoding.analyzeEncodedSystem_sound
Engineering.FiniteStateEncoding.analyzeEncodedSystem_complete
Engineering.FiniteStateRuntime.analyzeTransitionTable_sound
Foundations.CycleDetection.CycleWitness
```

Nenhum conflito de nomes, nenhuma ambiguidade de resolução.

## Cadeia de exportação

```text
TamesisLab
  → TamesisLab.Foundations
    → TamesisLab.Foundations.FiniteStateAbstraction
      → Abstraction, AbstractAnalysis, Observation,
        OrbitSeparation, Counterexample
  → TamesisLab.Foundations.FiniteStateAbstraction.Audit
```

Sem ciclo: `Engineering` importa `Foundations.CycleDetection`, nunca o
agregador `Foundations`.
