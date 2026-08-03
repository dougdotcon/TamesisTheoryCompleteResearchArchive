---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-AXIOM-AND-COMPUTABILITY-REVIEW
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
sorryAx: 0
local_axioms: 0
classical_choice_producing_data: 0
---

# Auditoria de axiomas e computabilidade

Medida por `#print axioms` no probe de revisão, `exit 0`.

## Tabela

| Declaração | Pegada | Computável | Typeclasses |
|---|---|---|---|
| `CertifiedFiniteAbstraction` | — | estrutura de dado | 0 |
| `analyzeAbstractSystem` | `propext, Classical.choice, Quot.sound` | **sim** | 0 |
| `CertifiedFiniteAbstraction.iterate_commutes` | `propext` | proposição | 0 |
| `analyzeAbstractSystem_observational_sound` | `propext, Classical.choice, Quot.sound` | proposição | 0 |
| `OrbitSeparating` | **nenhum** | proposição | 0 |
| `analyzeAbstractSystem_reflected_sound` | `propext, Classical.choice, Quot.sound` | proposição | 0 |
| `analyzeAbstractSystem_complete` | `propext, Classical.choice, Quot.sound` | proposição | 0 |

Auxiliares medidos, todos **sem axiomas**:

```text
orbitSeparating_iff_injOn
orbitSeparating_of_injective
boolToUnit_semiconj
boolToUnit_not_orbitSeparating
naive_cycle_reflection_is_false
unitEncoding
```

## Verificações negativas

```text
sorryAx                              0
axiomas locais declarados            0
sorry                                0
admit                                0
unsafe                               0
noncomputable                        0
Classical.choose                     0
Classical.decEq                      0
native_decide                        0
```

## Onde a pegada entra

Exatamente onde `analyzeEncodedSystem` entra — pelo **tipo**, através de
`buildTransitionTable` e do campo `closed`, como já auditado na frente
anterior. Ela não é introduzida por esta frente.

`iterate_commutes` carrega apenas `propext`, herdado de
`Function.Semiconj.iterate_right`.

## Nenhuma escolha clássica produz dado

```text
abstract              campo fornecido pelo consumidor
encode, decode        campos fornecidos pelo consumidor
Array                 construido por Array.ofFn, na frente anterior
CycleWitness executavel  devolvido por analyzeAbstractSystem, computavel
```

`analyzeAbstractSystem` avalia por `decide` em três testes concretos —
prova operacional de que a computação não está bloqueada por escolha
clássica.

## Política herdada, mantida

```text
"Nao abrir frente para remover propext, Classical.choice ou
 Quot.sound infraestruturais"
```

Esta frente não a reabre.
