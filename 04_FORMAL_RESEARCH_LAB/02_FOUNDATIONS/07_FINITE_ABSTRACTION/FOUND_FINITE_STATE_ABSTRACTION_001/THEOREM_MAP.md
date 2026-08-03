---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-THEOREM-MAP
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Mapa dos teoremas

## DAG completo

```text
Function.Semiconj (campo commutes)
        │
        ├─ Function.Semiconj.iterate_right
        │        │
        │        └─ CertifiedFiniteAbstraction.iterate_commutes
        │                     │
analyzeEncodedSystem_sound    │
        │                     │
        └──────────┬──────────┘
                   │
     analyzeAbstractSystem_observational_sound
                   │
                   ├──── OrbitSeparating (hipotese do consumidor)
                   │              │
                   └──────────────┴─ analyzeAbstractSystem_reflected_sound

analyzeEncodedSystem_complete
        │
        └─ analyzeAbstractSystem_complete
```

## Tabela

| Declaração | Categoria | Depende de | Conclui em |
|---|---|---|---|
| `CertifiedFiniteAbstraction` | executável | — | — |
| `analyzeAbstractSystem` | executável | `analyzeEncodedSystem` | `Except` |
| `iterate_commutes` | especificação | `Semiconj.iterate_right` | `A` |
| `analyzeAbstractSystem_observational_sound` | especificação | `iterate_commutes`, `analyzeEncodedSystem_sound` | `A` |
| `OrbitSeparating` | especificação | — | `Prop` |
| `analyzeAbstractSystem_reflected_sound` | especificação | observacional + `OrbitSeparating` | `C` |
| `analyzeAbstractSystem_complete` | especificação | `analyzeEncodedSystem_complete` | `Prop` |

## O que NÃO aparece no DAG

```text
casa dos pombos          nao reaplicada
detector                 nao copiado
runtime adapter          nao copiado
tabela de transicoes     nao reaberta
Set.InjOn                fora da cadeia central
injetividade global      fora da cadeia central
```

## Contraexemplo, fora da cadeia

```text
boolToUnit_semiconj
        │
        ├─ recorrencia abstrata (rfl)
        ├─ ausencia de recorrencia concreta (decide)
        └─ boolToUnit_not_orbitSeparating
```

O contraexemplo **mede** a cadeia; ele não é premissa de nenhum
resultado dela.
