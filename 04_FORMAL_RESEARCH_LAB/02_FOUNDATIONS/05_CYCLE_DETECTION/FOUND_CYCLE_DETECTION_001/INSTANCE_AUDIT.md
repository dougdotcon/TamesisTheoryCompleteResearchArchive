---
document_id: FCD-INSTANCE-AUDIT
instances: 1
conflicts: 0
---

# Auditoria de instâncias

```yaml
instance: CycleWitness.decidableValid
namespace: TamesisLab.Foundations.CycleDetection
scope: global dentro do namespace, exportada pelo umbrella
input_typeclasses: ["Fintype X", "DecidableEq X"]
output: "Decidable (CycleWitness.Valid f x w)"
purpose: >
  Valid eh um def; a resolucao de instancias nao o desdobra. Sem esta
  declaracao, decide (Valid f x w) nao elabora e o detector nao compila.
exported_by_umbrella: true
possible_conflict: nenhum
acceptable: true
```

## Instâncias derivadas

```text
DecidableEq CycleWitness    por deriving
Repr CycleWitness           por deriving
BEq CycleWitness            por deriving
```

Todas sobre um tipo **próprio da frente**, um par de naturais. Não tocam
em tipo de biblioteca nem em tipo de outra frente.

## Teste dedicado

Criado `TamesisLab/Tests/FoundCycleDetection001InstanceAudit.lean`, que
importa a **raiz** `TamesisLab` — logo, com todas as instâncias do
laboratório em escopo — e confirma:

```text
#synth Decidable (CycleWitness.Valid f x w)   resolve
#synth DecidableEq CycleWitness               resolve
#synth Repr CycleWitness                      resolve
#synth BEq CycleWitness                       resolve
```

mais a síntese em dois casos concretos, a aplicação do detector a `Bool`,
`Fin 1`, `Fin 3` e `Fin 4`, e a coexistência com `EventuallyMeets` da
frente anterior. **Exit 0**, 80 s — o tempo reflete a importação da raiz
inteira.

Nenhum módulo matemático foi alterado para o teste passar.

## Ausências verificadas

```text
instancia global de DecidableEq X       NAO criada — eh HIPOTESE do detector
instancia de Setoid                     nenhuma
instancia de Fintype no nucleo          nenhuma
ambiguidade de sintese                  nenhuma
instancia concorrente                   nenhuma
```

O detector **recebe** `DecidableEq X`; ele não a fabrica. O teste inclui
um exemplo que só typecheck porque a hipótese está no contexto.

## Interação com as frentes anteriores

`FOUND-SEMIGROUP-002` e `FOUND-FUNCTIONAL-GRAPH-001` declaram instâncias
`Fintype` apenas em seus contraexemplos, sobre tipos próprios. Não há
interseção com as três instâncias derivadas de `CycleWitness` nem com
`decidableValid`, cujo alvo é uma proposição desta frente.

```text
conflitos reais: 0
```
